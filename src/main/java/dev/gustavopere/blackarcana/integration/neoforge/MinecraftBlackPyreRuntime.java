package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.api.ArcanaTargetSpec;
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

import java.util.LinkedHashSet;
import java.util.List;
import java.util.Objects;
import java.util.Set;
import java.util.UUID;

/**
 * Server-authoritative Black Pyre entity-damage boundary.
 *
 * <p>Terrain presentation is intentionally fail-closed until Stage 04 exposes a protection-query
 * contract whose semantics explicitly cover block/world mutation. Reusing CONTROL or
 * DISPLACEMENT for terrain claims would misrepresent the frozen safety API. Entity damage remains
 * independently functional through the canonical DAMAGE admission route.</p>
 */
public final class MinecraftBlackPyreRuntime {
    /** Technical ceiling only. Stage 08 owns final damage balance below this boundary. */
    public static final double ABSOLUTE_MAX_RAW_DAMAGE = 100.0D;

    private static final String TERRAIN_NOT_REQUESTED = "terrain_not_requested";
    private static final String TERRAIN_PROTECTION_CONTRACT_MISSING =
        "black_pyre_terrain_protection_contract_missing";

    private MinecraftBlackPyreRuntime() { }

    public static BlackPyreResult igniteDefault(
            MinecraftServer server,
            UUID casterId,
            List<UUID> targetIds,
            double requestedDamage,
            boolean terrainRequested
    ) {
        Objects.requireNonNull(server, "server");
        Objects.requireNonNull(casterId, "casterId");
        Objects.requireNonNull(targetIds, "targetIds");

        String terrainCode = terrainRequested
            ? TERRAIN_PROTECTION_CONTRACT_MISSING
            : TERRAIN_NOT_REQUESTED;

        if (!Double.isFinite(requestedDamage) || requestedDamage <= 0.0D) {
            return BlackPyreResult.denied(
                "black_pyre_invalid_damage",
                "Requested Black Pyre damage must be finite and positive",
                terrainCode);
        }

        LivingEntity caster = findLoadedLivingEntity(server, casterId);
        if (caster == null || !caster.isAlive() || !(caster.level() instanceof ServerLevel level)) {
            return BlackPyreResult.denied(
                "black_pyre_caster_unavailable",
                "Black Pyre caster must be a loaded living server entity",
                terrainCode);
        }

        ArcanaServerRuntime runtime = ArcanaServerRuntimeManager.get(server).orElse(null);
        if (runtime == null) {
            return BlackPyreResult.denied(
                "black_pyre_runtime_unavailable",
                "Black Arcana server runtime is unavailable",
                terrainCode);
        }

        Set<UUID> uniqueTargets = new LinkedHashSet<>();
        for (UUID targetId : targetIds) {
            if (targetId == null || targetId.equals(casterId)) continue;
            uniqueTargets.add(targetId);
            if (uniqueTargets.size() >= ArcanaTargetSpec.ABSOLUTE_MAX_TARGETS) break;
        }
        if (uniqueTargets.isEmpty()) {
            return BlackPyreResult.denied(
                "black_pyre_no_targets",
                "No distinct Black Pyre target identities were supplied",
                terrainCode);
        }

        double boundedDamage = Math.min(requestedDamage, ABSOLUTE_MAX_RAW_DAMAGE);
        int damagedTargets = 0;
        double totalDamageDealt = 0.0D;

        for (UUID targetId : uniqueTargets) {
            LivingEntity target = findLoadedLivingEntity(server, targetId);
            if (target == null || !target.isAlive() || target.level() != level) continue;

            EntityProtectionFacts facts = MinecraftEntityProtectionResolver.resolve(server, caster, target);
            EntityInteractionAuthorization authorization = authorize(runtime, level, caster, target, facts);
            if (!authorization.decision().allowed()) continue;

            // Re-resolve and re-authorize immediately before the side effect. A target changing
            // dimension, dying, becoming allied/protected or otherwise changing identity fails closed.
            LivingEntity settlementTarget = findLoadedLivingEntity(server, targetId);
            if (settlementTarget == null
                    || settlementTarget != target
                    || !target.isAlive()
                    || target.level() != level) {
                continue;
            }
            EntityProtectionFacts settlementFacts =
                MinecraftEntityProtectionResolver.resolve(server, caster, target);
            EntityInteractionAuthorization settlementAuthorization =
                authorize(runtime, level, caster, target, settlementFacts);
            if (!settlementAuthorization.decision().allowed()) continue;

            // EntityEffectLimits.damageMultiplierCap is an upper bound, not a balance multiplier.
            // Stage 08 may choose a lower spell-specific multiplier. Until then Black Pyre never
            // amplifies raw requested damage merely because the standard policy cap is > 1.
            double policyMultiplier = Math.min(1.0D, settlementAuthorization.limits().damageMultiplierCap());
            double settlementDamage = boundedDamage * policyMultiplier;
            if (!Double.isFinite(settlementDamage) || settlementDamage <= 0.0D) continue;

            float healthBefore = target.getHealth();
            target.hurt(target.damageSources().indirectMagic(caster, caster), (float) settlementDamage);
            double actualDamage = Math.max(0.0D, (double) healthBefore - target.getHealth());
            if (actualDamage <= 0.0D) continue;

            damagedTargets++;
            totalDamageDealt += actualDamage;
        }

        if (damagedTargets == 0) {
            return new BlackPyreResult(
                ArcanaDecision.deny(
                    "black_pyre_no_authorized_targets",
                    "No supplied target remained eligible for Black Pyre damage settlement"),
                0,
                0.0D,
                false,
                terrainCode);
        }

        return new BlackPyreResult(
            ArcanaDecision.allow(),
            damagedTargets,
            totalDamageDealt,
            false,
            terrainCode);
    }

    private static EntityInteractionAuthorization authorize(
            ArcanaServerRuntime runtime,
            ServerLevel level,
            LivingEntity caster,
            LivingEntity target,
            EntityProtectionFacts facts
    ) {
        return runtime.entityInteractionAdmission().authorize(
            EntityInteractionType.DAMAGE,
            facts,
            new ProtectionQuery(
                caster.getUUID(),
                level.dimension().location().toString(),
                target.getUUID().toString(),
                EntityInteractionType.DAMAGE));
    }

    private static LivingEntity findLoadedLivingEntity(MinecraftServer server, UUID entityId) {
        for (ServerLevel level : server.getAllLevels()) {
            Entity entity = level.getEntity(entityId);
            if (entity instanceof LivingEntity living) return living;
        }
        return null;
    }

    public record BlackPyreResult(
        ArcanaDecision decision,
        int damagedTargets,
        double damageDealt,
        boolean terrainApplied,
        String terrainCode
    ) {
        public BlackPyreResult {
            Objects.requireNonNull(decision, "decision");
            Objects.requireNonNull(terrainCode, "terrainCode");
            if (damagedTargets < 0) {
                throw new IllegalArgumentException("damagedTargets cannot be negative");
            }
            if (!Double.isFinite(damageDealt) || damageDealt < 0.0D) {
                throw new IllegalArgumentException("damageDealt must be finite and non-negative");
            }
            if (terrainCode.isBlank()) {
                throw new IllegalArgumentException("terrainCode cannot be blank");
            }
            if (terrainApplied) {
                throw new IllegalArgumentException(
                    "Black Pyre terrain cannot be marked applied before a block-protection contract exists");
            }
        }

        public static BlackPyreResult denied(String code, String detail, String terrainCode) {
            return new BlackPyreResult(
                ArcanaDecision.deny(code, detail),
                0,
                0.0D,
                false,
                terrainCode);
        }
    }
}
