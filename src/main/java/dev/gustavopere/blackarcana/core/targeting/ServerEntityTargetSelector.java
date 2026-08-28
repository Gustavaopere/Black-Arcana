package dev.gustavopere.blackarcana.core.targeting;

import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaServices;
import dev.gustavopere.blackarcana.api.ArcanaTargetReference;
import dev.gustavopere.blackarcana.api.ArcanaTargetSpec;
import net.minecraft.core.BlockPos;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.projectile.Projectile;
import net.minecraft.world.level.ClipContext;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.BlockHitResult;
import net.minecraft.world.phys.HitResult;
import net.minecraft.world.phys.Vec3;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import java.util.Optional;
import java.util.UUID;
import java.util.function.Function;

/**
 * Minecraft server target adapter for target kinds whose geometry is fully
 * defined by {@link ArcanaTargetSpec}. It never treats client coordinates as
 * authoritative and performs a loaded-chunk preflight before block raycasts.
 *
 * CONE, CYLINDER and LINKED deliberately remain unsupported until their own
 * canonical geometry/link contracts exist instead of relying on hidden defaults.
 */
public final class ServerEntityTargetSelector implements ArcanaServices.TargetSelector {
    private static final double RAY_ENTITY_INFLATION = 0.3D;
    private static final double CHUNK_PREFLIGHT_STEP = 8.0D;

    private final MinecraftServer server;
    private final Function<ArcanaCastRequest, ArcanaTargetSpec> specResolver;

    public ServerEntityTargetSelector(
            MinecraftServer server,
            Function<ArcanaCastRequest, ArcanaTargetSpec> specResolver
    ) {
        this.server = Objects.requireNonNull(server, "server");
        this.specResolver = Objects.requireNonNull(specResolver, "specResolver");
    }

    @Override
    public ArcanaServices.TargetResolution resolve(ArcanaCastRequest request) {
        ArcanaTargetSpec spec = Objects.requireNonNull(specResolver.apply(request), "target spec");
        ServerPlayer caster = server.getPlayerList().getPlayer(request.context().casterId());
        if (caster == null || !caster.isAlive()) {
            return ArcanaServices.TargetResolution.denied("caster is not a live server player");
        }

        if (!caster.level().dimension().location().toString().equals(request.context().dimensionId())) {
            return ArcanaServices.TargetResolution.denied("caster dimension changed before target resolution");
        }

        return switch (spec.kind()) {
            case SELF -> ArcanaServices.TargetResolution.resolved(
                    new ArcanaTargetReference.EntityRef(caster.getUUID()).canonical());
            case ENTITY -> resolveExplicitEntity(caster, request, spec, false);
            case PROJECTILE -> resolveExplicitEntity(caster, request, spec, true);
            case BLOCK -> resolveBlockRay(caster, spec);
            case RAY -> resolveEntityRay(caster, spec);
            case SPHERE -> resolveSphere(caster, spec);
            case CONE, CYLINDER, LINKED -> ArcanaServices.TargetResolution.denied(
                    "target kind requires an explicit geometry/link contract: " + spec.kind());
        };
    }

    private static ArcanaServices.TargetResolution resolveExplicitEntity(
            ServerPlayer caster,
            ArcanaCastRequest request,
            ArcanaTargetSpec spec,
            boolean requireProjectile
    ) {
        if (request.targetHint().isBlank()) {
            return ArcanaServices.TargetResolution.denied("entity target hint is missing");
        }

        final UUID targetUuid;
        try {
            targetUuid = parseEntityHint(request.targetHint());
        } catch (IllegalArgumentException ex) {
            return ArcanaServices.TargetResolution.denied("entity target hint is not a valid entity reference");
        }

        ServerLevel level = caster.serverLevel();
        Entity target = level.getEntity(targetUuid);
        if (target == null) {
            return ArcanaServices.TargetResolution.denied("target is not naturally loaded in caster dimension");
        }
        if (requireProjectile && !(target instanceof Projectile)) {
            return ArcanaServices.TargetResolution.denied("target is not a projectile");
        }

        TargetCandidate candidate = candidate(caster, target, caster.distanceToSqr(target));
        List<TargetCandidate> selected = BoundedTargeting.select(spec, List.of(candidate));
        if (selected.isEmpty()) {
            return ArcanaServices.TargetResolution.denied("target rejected by range/LOS/player/friendly policy");
        }
        return ArcanaServices.TargetResolution.resolved(selected.getFirst().targetId());
    }

    private static ArcanaServices.TargetResolution resolveBlockRay(ServerPlayer caster, ArcanaTargetSpec spec) {
        ServerLevel level = caster.serverLevel();
        Vec3 start = caster.getEyePosition(1.0F);
        Vec3 end = start.add(caster.getViewVector(1.0F).scale(spec.maxRange()));
        if (!rayPathLoaded(level, start, end)) {
            return ArcanaServices.TargetResolution.denied("block ray crosses an unloaded chunk");
        }

        BlockHitResult hit = level.clip(new ClipContext(
                start,
                end,
                ClipContext.Block.COLLIDER,
                ClipContext.Fluid.NONE,
                caster));
        if (hit.getType() == HitResult.Type.MISS) {
            return ArcanaServices.TargetResolution.denied("block ray did not hit a block");
        }

        BlockPos pos = hit.getBlockPos();
        if (!level.hasChunkAt(pos)) {
            return ArcanaServices.TargetResolution.denied("block target chunk is not loaded");
        }
        return ArcanaServices.TargetResolution.resolved(new ArcanaTargetReference.BlockRef(
                level.dimension().location().toString(),
                pos.getX(),
                pos.getY(),
                pos.getZ()).canonical());
    }

    private static ArcanaServices.TargetResolution resolveEntityRay(ServerPlayer caster, ArcanaTargetSpec spec) {
        ServerLevel level = caster.serverLevel();
        Vec3 start = caster.getEyePosition(1.0F);
        Vec3 requestedEnd = start.add(caster.getViewVector(1.0F).scale(spec.maxRange()));
        if (!rayPathLoaded(level, start, requestedEnd)) {
            return ArcanaServices.TargetResolution.denied("entity ray crosses an unloaded chunk");
        }

        BlockHitResult blockHit = level.clip(new ClipContext(
                start,
                requestedEnd,
                ClipContext.Block.COLLIDER,
                ClipContext.Fluid.NONE,
                caster));
        Vec3 end = blockHit.getType() == HitResult.Type.MISS ? requestedEnd : blockHit.getLocation();

        AABB corridor = new AABB(
                Math.min(start.x, end.x),
                Math.min(start.y, end.y),
                Math.min(start.z, end.z),
                Math.max(start.x, end.x),
                Math.max(start.y, end.y),
                Math.max(start.z, end.z)).inflate(1.0D);

        List<TargetCandidate> candidates = new ArrayList<>();
        for (LivingEntity entity : level.getEntitiesOfClass(
                LivingEntity.class,
                corridor,
                entity -> entity != caster)) {
            AABB hitBox = entity.getBoundingBox().inflate(RAY_ENTITY_INFLATION);
            Optional<Vec3> intersection = hitBox.contains(start)
                    ? Optional.of(start)
                    : hitBox.clip(start, end);
            if (intersection.isEmpty()) continue;
            candidates.add(candidate(caster, entity, start.distanceToSqr(intersection.get())));
        }

        List<TargetCandidate> selected = BoundedTargeting.select(spec, candidates);
        if (selected.isEmpty()) {
            return ArcanaServices.TargetResolution.denied("entity ray found no valid target");
        }
        return ArcanaServices.TargetResolution.resolved(
                selected.stream().map(TargetCandidate::targetId).toList());
    }

    private static ArcanaServices.TargetResolution resolveSphere(ServerPlayer caster, ArcanaTargetSpec spec) {
        ServerLevel level = caster.serverLevel();
        AABB bounds = caster.getBoundingBox().inflate(spec.maxRange());
        List<TargetCandidate> candidates = new ArrayList<>();

        for (LivingEntity entity : level.getEntitiesOfClass(
                LivingEntity.class,
                bounds,
                entity -> entity != caster)) {
            candidates.add(candidate(caster, entity, caster.distanceToSqr(entity)));
        }

        List<TargetCandidate> selected = BoundedTargeting.select(spec, candidates);
        if (selected.isEmpty()) {
            return ArcanaServices.TargetResolution.denied("sphere found no valid target");
        }
        return ArcanaServices.TargetResolution.resolved(
                selected.stream().map(TargetCandidate::targetId).toList());
    }

    private static TargetCandidate candidate(ServerPlayer caster, Entity target, double distanceSquared) {
        return new TargetCandidate(
                new ArcanaTargetReference.EntityRef(target.getUUID()).canonical(),
                distanceSquared,
                true,
                target.isAlive(),
                caster.hasLineOfSight(target),
                target instanceof ServerPlayer,
                caster.isAlliedTo(target));
    }

    private static UUID parseEntityHint(String hint) {
        if (hint.startsWith("entity|")) {
            ArcanaTargetReference reference = ArcanaTargetReference.parse(hint);
            if (reference instanceof ArcanaTargetReference.EntityRef entityRef) {
                return entityRef.entityId();
            }
            throw new IllegalArgumentException("target reference is not an entity");
        }
        return UUID.fromString(hint);
    }

    private static boolean rayPathLoaded(ServerLevel level, Vec3 start, Vec3 end) {
        double distance = start.distanceTo(end);
        int samples = Math.max(1, (int) Math.ceil(distance / CHUNK_PREFLIGHT_STEP));
        for (int sample = 0; sample <= samples; sample++) {
            double fraction = sample / (double) samples;
            Vec3 point = start.lerp(end, fraction);
            if (!level.hasChunkAt(BlockPos.containing(point.x, point.y, point.z))) {
                return false;
            }
        }
        return true;
    }
}
