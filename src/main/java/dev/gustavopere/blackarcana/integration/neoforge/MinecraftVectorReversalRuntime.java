package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.content.space.LiminalSafetyCeilings;
import dev.gustavopere.blackarcana.content.space.VectorImpulseLimiter;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntime;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntimeManager;
import dev.gustavopere.blackarcana.core.world.EntityInteractionAuthorization;
import dev.gustavopere.blackarcana.core.world.EntityInteractionType;
import dev.gustavopere.blackarcana.core.world.EntityProtectionFacts;
import dev.gustavopere.blackarcana.core.world.ProtectionQuery;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.phys.Vec3;

import java.util.ArrayList;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Objects;
import java.util.Set;
import java.util.UUID;

/**
 * Server-authoritative settlement boundary for Space-domain Vector Reversal.
 *
 * <p>The host spell adapter owns targeting/presentation and submits explicit target identities.
 * Black Arcana resolves those identities again from server state, applies the canonical entity
 * interaction policy, deduplicates targets and mutates velocity only after an immediate settlement
 * revalidation. No chunks are force-loaded and fall distance is deliberately preserved.</p>
 */
public final class MinecraftVectorReversalRuntime {
    public static final double DEFAULT_INTENSITY = 1.5D;
    public static final double DEFAULT_MAX_SPEED = 2.5D;
    public static final int DEFAULT_MAX_ENTITIES = 4;
    public static final double DEFAULT_PLAYER_MULTIPLIER = 0.75D;
    public static final double DEFAULT_BOSS_MULTIPLIER = 0.5D;

    private MinecraftVectorReversalRuntime() { }

    public static VectorReversalResult applyDefault(
            MinecraftServer server,
            UUID casterId,
            List<UUID> targetIds,
            double directionX,
            double directionY,
            double directionZ
    ) {
        return apply(
            server,
            casterId,
            targetIds,
            directionX,
            directionY,
            directionZ,
            DEFAULT_INTENSITY,
            DEFAULT_MAX_SPEED,
            DEFAULT_MAX_ENTITIES,
            DEFAULT_PLAYER_MULTIPLIER,
            DEFAULT_BOSS_MULTIPLIER);
    }

    public static VectorReversalResult apply(
            MinecraftServer server,
            UUID casterId,
            List<UUID> targetIds,
            double directionX,
            double directionY,
            double directionZ,
            double requestedIntensity,
            double maxSpeed,
            int maxEntities,
            double playerMultiplier,
            double bossMultiplier
    ) {
        Objects.requireNonNull(server, "server");
        Objects.requireNonNull(casterId, "casterId");
        Objects.requireNonNull(targetIds, "targetIds");

        Vec3 direction = new Vec3(directionX, directionY, directionZ);
        if (!finite(directionX, directionY, directionZ) || direction.lengthSqr() <= 1.0E-12D) {
            return VectorReversalResult.denied("vector_reversal_direction", "Vector direction must be finite and non-zero");
        }
        if (!Double.isFinite(requestedIntensity) || requestedIntensity <= 0.0D) {
            return VectorReversalResult.denied("vector_reversal_intensity", "Vector intensity must be finite and positive");
        }
        if (!Double.isFinite(maxSpeed) || maxSpeed <= 0.0D) {
            return VectorReversalResult.denied("vector_reversal_speed", "Vector speed cap must be finite and positive");
        }
        if (maxEntities <= 0 || maxEntities > LiminalSafetyCeilings.MAX_VECTOR_TARGETS) {
            return VectorReversalResult.denied("vector_reversal_target_cap", "Vector target cap exceeds the hard Liminal ceiling");
        }
        if (!validMultiplier(playerMultiplier) || !validMultiplier(bossMultiplier)) {
            return VectorReversalResult.denied("vector_reversal_multiplier", "Vector target multipliers must be finite values in [0, 1]");
        }

        LivingEntity caster = findLoadedLivingEntity(server, casterId);
        if (caster == null || !caster.isAlive() || !(caster.level() instanceof ServerLevel level)) {
            return VectorReversalResult.denied("vector_reversal_caster_unavailable", "Caster must be a loaded living server entity");
        }

        ArcanaServerRuntime runtime = ArcanaServerRuntimeManager.get(server).orElse(null);
        if (runtime == null) {
            return VectorReversalResult.denied("vector_reversal_runtime_unavailable", "Black Arcana server runtime is unavailable");
        }

        Set<UUID> uniqueTargets = new LinkedHashSet<>();
        for (UUID targetId : targetIds) {
            if (targetId == null || targetId.equals(casterId)) continue;
            uniqueTargets.add(targetId);
            if (uniqueTargets.size() >= maxEntities) break;
        }
        if (uniqueTargets.isEmpty()) {
            return VectorReversalResult.denied("vector_reversal_no_targets", "No distinct eligible target identities were supplied");
        }

        Vec3 normalizedDirection = direction.normalize();
        List<SettlementCandidate> candidates = new ArrayList<>(uniqueTargets.size());
        int deniedTargets = 0;
        for (UUID targetId : uniqueTargets) {
            LivingEntity target = findLoadedLivingEntity(server, targetId);
            if (target == null || !target.isAlive() || target.level() != level) {
                deniedTargets++;
                continue;
            }
            EntityProtectionFacts facts = MinecraftEntityProtectionResolver.resolve(server, caster, target);
            EntityInteractionAuthorization authorization = authorize(runtime, level, caster, target, facts);
            if (!authorization.decision().allowed()) {
                deniedTargets++;
                continue;
            }
            double policyIntensity = Math.min(requestedIntensity, authorization.limits().maxDisplacementBlocks());
            double semanticMultiplier = facts.player()
                ? playerMultiplier
                : (facts.boss() ? bossMultiplier : 1.0D);
            double settledIntensity = policyIntensity * semanticMultiplier;
            if (settledIntensity <= 0.0D) {
                deniedTargets++;
                continue;
            }
            candidates.add(new SettlementCandidate(targetId, target, settledIntensity));
        }

        if (candidates.isEmpty()) {
            return new VectorReversalResult(
                ArcanaDecision.deny("vector_reversal_no_authorized_targets", "All supplied targets failed displacement admission"),
                0,
                deniedTargets);
        }

        int affected = 0;
        for (SettlementCandidate candidate : candidates) {
            LivingEntity target = findLoadedLivingEntity(server, candidate.targetId());
            if (target == null
                    || target != candidate.target()
                    || !target.isAlive()
                    || target.level() != level) {
                deniedTargets++;
                continue;
            }

            EntityProtectionFacts settlementFacts = MinecraftEntityProtectionResolver.resolve(server, caster, target);
            EntityInteractionAuthorization settlementAuthorization = authorize(
                runtime, level, caster, target, settlementFacts);
            if (!settlementAuthorization.decision().allowed()) {
                deniedTargets++;
                continue;
            }

            double policyIntensity = Math.min(
                candidate.intensity(),
                settlementAuthorization.limits().maxDisplacementBlocks());
            if (policyIntensity <= 0.0D) {
                deniedTargets++;
                continue;
            }

            Vec3 impulse = normalizedDirection.scale(policyIntensity);
            Vec3 settledVelocity = VectorImpulseLimiter.clamp(
                target.getDeltaMovement().add(impulse),
                maxSpeed);
            target.setDeltaMovement(settledVelocity);
            affected++;
        }

        if (affected == 0) {
            return new VectorReversalResult(
                ArcanaDecision.deny("vector_reversal_settlement_failed", "No target remained eligible at displacement settlement"),
                0,
                deniedTargets);
        }
        return new VectorReversalResult(ArcanaDecision.allow(), affected, deniedTargets);
    }

    private static EntityInteractionAuthorization authorize(
            ArcanaServerRuntime runtime,
            ServerLevel level,
            LivingEntity caster,
            LivingEntity target,
            EntityProtectionFacts facts
    ) {
        return runtime.entityInteractionAdmission().authorize(
            EntityInteractionType.DISPLACEMENT,
            facts,
            new ProtectionQuery(
                caster.getUUID(),
                level.dimension().location().toString(),
                target.getUUID().toString(),
                EntityInteractionType.DISPLACEMENT));
    }

    private static LivingEntity findLoadedLivingEntity(MinecraftServer server, UUID entityId) {
        for (ServerLevel level : server.getAllLevels()) {
            Entity entity = level.getEntity(entityId);
            if (entity instanceof LivingEntity living) return living;
        }
        return null;
    }

    private static boolean finite(double x, double y, double z) {
        return Double.isFinite(x) && Double.isFinite(y) && Double.isFinite(z);
    }

    private static boolean validMultiplier(double value) {
        return Double.isFinite(value) && value >= 0.0D && value <= 1.0D;
    }

    private record SettlementCandidate(UUID targetId, LivingEntity target, double intensity) {
        private SettlementCandidate {
            Objects.requireNonNull(targetId, "targetId");
            Objects.requireNonNull(target, "target");
            if (!Double.isFinite(intensity) || intensity <= 0.0D) {
                throw new IllegalArgumentException("settlement intensity must be finite and positive");
            }
        }
    }

    public record VectorReversalResult(ArcanaDecision decision, int affectedTargets, int deniedTargets) {
        public VectorReversalResult {
            Objects.requireNonNull(decision, "decision");
            if (affectedTargets < 0 || deniedTargets < 0) {
                throw new IllegalArgumentException("Vector Reversal result counts cannot be negative");
            }
        }

        public static VectorReversalResult denied(String code, String detail) {
            return new VectorReversalResult(ArcanaDecision.deny(code, detail), 0, 0);
        }
    }
}
