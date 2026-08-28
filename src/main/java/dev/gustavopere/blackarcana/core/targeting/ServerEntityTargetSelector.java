package dev.gustavopere.blackarcana.core.targeting;

import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaServices;
import dev.gustavopere.blackarcana.api.ArcanaTargetGeometry;
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
 * Minecraft server target adapter. All coordinates/entity sets are resolved
 * from live server state; client target data is advisory only for explicit
 * ENTITY/PROJECTILE selection. No path intentionally force-loads chunks.
 */
public final class ServerEntityTargetSelector implements ArcanaServices.TargetSelector {
    private static final double RAY_ENTITY_INFLATION = 0.3D;
    private static final double CHUNK_PREFLIGHT_STEP = 8.0D;
    private static final int MAX_LINK_CANDIDATES = ArcanaTargetSpec.ABSOLUTE_MAX_TARGETS * 4;

    private final MinecraftServer server;
    private final Function<ArcanaCastRequest, ArcanaTargetSpec> specResolver;
    private final Function<ArcanaCastRequest, ArcanaTargetGeometry> geometryResolver;
    private final LinkedTargetResolver linkedTargetResolver;

    public ServerEntityTargetSelector(
            MinecraftServer server,
            Function<ArcanaCastRequest, ArcanaTargetSpec> specResolver
    ) {
        this(server, specResolver, request -> ArcanaTargetGeometry.none(), LinkedTargetResolver.none());
    }

    public ServerEntityTargetSelector(
            MinecraftServer server,
            Function<ArcanaCastRequest, ArcanaTargetSpec> specResolver,
            Function<ArcanaCastRequest, ArcanaTargetGeometry> geometryResolver,
            LinkedTargetResolver linkedTargetResolver
    ) {
        this.server = Objects.requireNonNull(server, "server");
        this.specResolver = Objects.requireNonNull(specResolver, "specResolver");
        this.geometryResolver = Objects.requireNonNull(geometryResolver, "geometryResolver");
        this.linkedTargetResolver = Objects.requireNonNull(linkedTargetResolver, "linkedTargetResolver");
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
            case CONE -> resolveCone(caster, request, spec);
            case CYLINDER -> resolveCylinder(caster, request, spec);
            case LINKED -> resolveLinked(caster, request, spec);
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
        return resolution(selected, "explicit target rejected");
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

        return resolution(BoundedTargeting.select(spec, candidates), "entity ray found no valid target");
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

        return resolution(BoundedTargeting.select(spec, candidates), "sphere found no valid target");
    }

    private ArcanaServices.TargetResolution resolveCone(
            ServerPlayer caster,
            ArcanaCastRequest request,
            ArcanaTargetSpec spec
    ) {
        ArcanaTargetGeometry geometry = Objects.requireNonNull(
                geometryResolver.apply(request), "target geometry");
        if (!(geometry instanceof ArcanaTargetGeometry.Cone cone)) {
            return ArcanaServices.TargetResolution.denied("cone target requires ArcanaTargetGeometry.Cone");
        }

        ServerLevel level = caster.serverLevel();
        Vec3 origin = caster.getEyePosition(1.0F);
        Vec3 facing = caster.getViewVector(1.0F);
        AABB bounds = caster.getBoundingBox().inflate(spec.maxRange());
        List<TargetCandidate> candidates = new ArrayList<>();

        for (LivingEntity entity : level.getEntitiesOfClass(
                LivingEntity.class,
                bounds,
                entity -> entity != caster)) {
            Vec3 toTarget = entity.position().subtract(origin);
            if (!TargetGeometryMath.withinCone(
                    facing.x, facing.y, facing.z,
                    toTarget.x, toTarget.y, toTarget.z,
                    cone)) {
                continue;
            }
            candidates.add(candidate(caster, entity, caster.distanceToSqr(entity)));
        }

        return resolution(BoundedTargeting.select(spec, candidates), "cone found no valid target");
    }

    private ArcanaServices.TargetResolution resolveCylinder(
            ServerPlayer caster,
            ArcanaCastRequest request,
            ArcanaTargetSpec spec
    ) {
        ArcanaTargetGeometry geometry = Objects.requireNonNull(
                geometryResolver.apply(request), "target geometry");
        if (!(geometry instanceof ArcanaTargetGeometry.Cylinder cylinder)) {
            return ArcanaServices.TargetResolution.denied("cylinder target requires ArcanaTargetGeometry.Cylinder");
        }
        if (cylinder.radius() > spec.maxRange() || cylinder.halfHeight() > spec.maxRange()) {
            return ArcanaServices.TargetResolution.denied("cylinder geometry exceeds target maxRange");
        }

        ServerLevel level = caster.serverLevel();
        Vec3 center = caster.position();
        AABB bounds = caster.getBoundingBox().inflate(
                cylinder.radius(), cylinder.halfHeight(), cylinder.radius());
        List<TargetCandidate> candidates = new ArrayList<>();

        for (LivingEntity entity : level.getEntitiesOfClass(
                LivingEntity.class,
                bounds,
                entity -> entity != caster)) {
            Vec3 position = entity.position();
            if (!TargetGeometryMath.withinCylinder(
                    position.x - center.x,
                    position.y - center.y,
                    position.z - center.z,
                    cylinder)) {
                continue;
            }
            candidates.add(candidate(caster, entity, caster.distanceToSqr(entity)));
        }

        return resolution(BoundedTargeting.select(spec, candidates), "cylinder found no valid target");
    }

    private ArcanaServices.TargetResolution resolveLinked(
            ServerPlayer caster,
            ArcanaCastRequest request,
            ArcanaTargetSpec spec
    ) {
        LinkedTargetCandidates.Result normalized = LinkedTargetCandidates.normalize(
                linkedTargetResolver.resolve(request, caster),
                MAX_LINK_CANDIDATES);
        if (!normalized.valid()) {
            return ArcanaServices.TargetResolution.denied(normalized.detail());
        }

        ServerLevel level = caster.serverLevel();
        List<TargetCandidate> candidates = new ArrayList<>(normalized.uniqueIds().size());
        for (UUID targetId : normalized.uniqueIds()) {
            Entity target = level.getEntity(targetId);
            if (target == null) continue;
            candidates.add(candidate(caster, target, caster.distanceToSqr(target)));
        }

        return resolution(BoundedTargeting.select(spec, candidates), "linked set found no valid target");
    }

    private static ArcanaServices.TargetResolution resolution(
            List<TargetCandidate> selected,
            String emptyReason
    ) {
        if (selected.isEmpty()) return ArcanaServices.TargetResolution.denied(emptyReason);
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
