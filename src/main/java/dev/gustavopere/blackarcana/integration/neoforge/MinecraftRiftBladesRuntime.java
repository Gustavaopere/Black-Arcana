package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.content.projection.ProjectionSafetyCeilings;
import dev.gustavopere.blackarcana.content.space.SafeDestinationPolicy;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntime;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntimeManager;
import dev.gustavopere.blackarcana.core.world.ChunkRef;
import dev.gustavopere.blackarcana.core.world.EntityEffectLimits;
import dev.gustavopere.blackarcana.core.world.EntityInteractionAuthorization;
import dev.gustavopere.blackarcana.core.world.EntityInteractionType;
import dev.gustavopere.blackarcana.core.world.EntityProtectionFacts;
import dev.gustavopere.blackarcana.core.world.ProtectionQuery;
import net.minecraft.core.BlockPos;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.RelativeMovement;
import net.minecraft.world.phys.AABB;
import net.neoforged.neoforge.common.Tags;

import java.util.Objects;
import java.util.Set;
import java.util.UUID;

/**
 * Server-authoritative settlement boundary for the marked-hit portion of Rift Blades.
 * Damage and optional caster displacement are admitted independently. A failed landing never
 * rolls back an already-authorized hit, and no chunk is force-loaded for gap-close.
 */
public final class MinecraftRiftBladesRuntime {
    private static final SafeDestinationPolicy DESTINATION_POLICY = new SafeDestinationPolicy();

    private MinecraftRiftBladesRuntime() { }

    public static StrikeResult resolveMarkedStrike(
            MinecraftServer server,
            UUID casterId,
            UUID targetId,
            double requestedDamage,
            double landingX,
            double landingY,
            double landingZ,
            double maxGapCloseBlocks
    ) {
        Objects.requireNonNull(server, "server");
        Objects.requireNonNull(casterId, "casterId");
        Objects.requireNonNull(targetId, "targetId");

        if (!Double.isFinite(requestedDamage) || requestedDamage <= 0.0D) {
            return StrikeResult.denied("rift_blades_invalid_damage", "Requested Rift Blades damage must be finite and positive");
        }
        if (!Double.isFinite(maxGapCloseBlocks) || maxGapCloseBlocks < 0.0D
                || maxGapCloseBlocks > EntityEffectLimits.ABSOLUTE_MAX_DISPLACEMENT_BLOCKS) {
            return StrikeResult.denied("rift_blades_invalid_gap_close", "Requested gap-close limit is outside displacement safety bounds");
        }
        if (!Double.isFinite(landingX) || !Double.isFinite(landingY) || !Double.isFinite(landingZ)) {
            return StrikeResult.denied("rift_blades_invalid_landing", "Landing candidate must use finite coordinates");
        }

        LivingEntity caster = findLoadedLivingEntity(server, casterId);
        LivingEntity target = findLoadedLivingEntity(server, targetId);
        if (caster == null || target == null || !caster.isAlive() || !target.isAlive()) {
            return StrikeResult.denied("rift_blades_endpoint_unavailable", "Caster and marked target must be loaded living entities");
        }
        if (!(caster.level() instanceof ServerLevel level) || target.level() != level) {
            return StrikeResult.denied("rift_blades_dimension_mismatch", "Marked strike endpoints must share one loaded server level");
        }

        ArcanaServerRuntime runtime = ArcanaServerRuntimeManager.get(server).orElse(null);
        if (runtime == null) {
            return StrikeResult.denied("rift_blades_runtime_unavailable", "Black Arcana server runtime is unavailable");
        }

        EntityInteractionAuthorization damageAuthorization = authorizeDamage(server, runtime, caster, target, level);
        if (!damageAuthorization.decision().allowed()) {
            return new StrikeResult(damageAuthorization.decision(), 0.0D, false);
        }

        // Hard technical ceiling only. Stage 08 owns final spell balance below this boundary.
        double boundedDamage = Math.min(requestedDamage, ProjectionSafetyCeilings.MAX_RAW_ATTACK_DAMAGE);

        LivingEntity liveCaster = findLoadedLivingEntity(server, casterId);
        LivingEntity liveTarget = findLoadedLivingEntity(server, targetId);
        if (liveCaster != caster || liveTarget != target || !caster.isAlive() || !target.isAlive()) {
            return StrikeResult.denied("rift_blades_endpoint_changed", "Marked strike endpoint changed before damage settlement");
        }
        EntityInteractionAuthorization settlementAuthorization = authorizeDamage(server, runtime, caster, target, level);
        if (!settlementAuthorization.decision().allowed()) {
            return new StrikeResult(settlementAuthorization.decision(), 0.0D, false);
        }

        float healthBefore = target.getHealth();
        target.hurt(target.damageSources().indirectMagic(caster, caster), (float) boundedDamage);
        double damageDealt = Math.max(0.0D, (double) healthBefore - target.getHealth());
        if (damageDealt <= 0.0D || !caster.isAlive()) {
            return new StrikeResult(ArcanaDecision.allow(), damageDealt, false);
        }

        double policyGapLimit = Math.min(
            maxGapCloseBlocks,
            settlementAuthorization.limits().maxDisplacementBlocks());
        if (policyGapLimit <= 0.0D || !withinGapLimit(caster, landingX, landingY, landingZ, policyGapLimit)) {
            return new StrikeResult(ArcanaDecision.allow(), damageDealt, false);
        }

        if (!safeLanding(server, runtime, caster, level, landingX, landingY, landingZ)) {
            return new StrikeResult(ArcanaDecision.allow(), damageDealt, false);
        }

        // Re-resolve immediately before displacement so stale/unloaded/dead caster state cannot
        // be used to cross the already-validated destination boundary.
        LivingEntity settlementCaster = findLoadedLivingEntity(server, casterId);
        if (settlementCaster != caster || !caster.isAlive()
                || !safeLanding(server, runtime, caster, level, landingX, landingY, landingZ)) {
            return new StrikeResult(ArcanaDecision.allow(), damageDealt, false);
        }

        boolean teleported = caster.teleportTo(
            level,
            landingX,
            landingY,
            landingZ,
            Set.<RelativeMovement>of(),
            caster.getYRot(),
            caster.getXRot());
        return new StrikeResult(ArcanaDecision.allow(), damageDealt, teleported);
    }

    private static EntityInteractionAuthorization authorizeDamage(
            MinecraftServer server,
            ArcanaServerRuntime runtime,
            LivingEntity caster,
            LivingEntity target,
            ServerLevel level
    ) {
        EntityProtectionFacts facts = MinecraftEntityProtectionResolver.resolve(server, caster, target);
        return runtime.entityInteractionAdmission().authorize(
            EntityInteractionType.DAMAGE,
            facts,
            new ProtectionQuery(
                caster.getUUID(),
                level.dimension().location().toString(),
                target.getUUID().toString(),
                EntityInteractionType.DAMAGE));
    }

    private static boolean withinGapLimit(
            LivingEntity caster,
            double landingX,
            double landingY,
            double landingZ,
            double limit
    ) {
        double dx = landingX - caster.getX();
        double dy = landingY - caster.getY();
        double dz = landingZ - caster.getZ();
        return dx * dx + dy * dy + dz * dz <= limit * limit;
    }

    private static boolean safeLanding(
            MinecraftServer server,
            ArcanaServerRuntime runtime,
            LivingEntity caster,
            ServerLevel level,
            double landingX,
            double landingY,
            double landingZ
    ) {
        if (caster.getType().is(Tags.EntityTypes.TELEPORTING_NOT_SUPPORTED)) return false;

        BlockPos landing = BlockPos.containing(landingX, landingY, landingZ);
        boolean loaded = level.getChunkSource().getChunkNow(landing.getX() >> 4, landing.getZ() >> 4) != null;
        AABB landingBox = caster.getBoundingBox().move(
            landingX - caster.getX(),
            landingY - caster.getY(),
            landingZ - caster.getZ());
        boolean border = level.getWorldBorder().isWithinBounds(landingBox);
        boolean collisionFree = loaded && level.noCollision(caster, landingBox);
        boolean fluidAllowed = loaded
            && level.getFluidState(landing).isEmpty()
            && level.getFluidState(landing.above()).isEmpty();
        boolean vehicleUnsafe = caster.isPassenger() || caster.isVehicle();

        boolean protectionAllowed = false;
        if (loaded) {
            var guard = runtime.protectedDestinationGuard().orElse(null);
            if (guard != null) {
                ArcanaDecision protectedDecision = guard.authorize(
                    new ChunkRef(level.dimension().location().toString(), landing.getX() >> 4, landing.getZ() >> 4),
                    new ProtectionQuery(
                        caster.getUUID(),
                        level.dimension().location().toString(),
                        caster.getUUID().toString(),
                        EntityInteractionType.DISPLACEMENT));
                protectionAllowed = protectedDecision.allowed();
            }
        }

        SafeDestinationPolicy.Decision decision = DESTINATION_POLICY.validate(
            new SafeDestinationPolicy.Facts(
                loaded,
                border,
                collisionFree,
                collisionFree,
                fluidAllowed,
                true,
                protectionAllowed,
                vehicleUnsafe));
        return decision.allowed();
    }

    private static LivingEntity findLoadedLivingEntity(MinecraftServer server, UUID entityId) {
        for (ServerLevel level : server.getAllLevels()) {
            Entity entity = level.getEntity(entityId);
            if (entity instanceof LivingEntity living) return living;
        }
        return null;
    }

    public record StrikeResult(ArcanaDecision decision, double damageDealt, boolean gapClosed) {
        public StrikeResult {
            Objects.requireNonNull(decision, "decision");
            if (!Double.isFinite(damageDealt) || damageDealt < 0.0D) {
                throw new IllegalArgumentException("damageDealt must be finite and non-negative");
            }
            if (!decision.allowed() && (damageDealt != 0.0D || gapClosed)) {
                throw new IllegalArgumentException("denied Rift Blades result cannot carry settlement effects");
            }
            if (gapClosed && damageDealt <= 0.0D) {
                throw new IllegalArgumentException("Rift Blades cannot gap-close without real damage settlement");
            }
        }

        public static StrikeResult denied(String code, String detail) {
            return new StrikeResult(ArcanaDecision.deny(code, detail), 0.0D, false);
        }
    }
}
