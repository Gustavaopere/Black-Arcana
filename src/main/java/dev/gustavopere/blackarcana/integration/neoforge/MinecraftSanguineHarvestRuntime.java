package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.content.blood.BloodSafetyCeilings;
import dev.gustavopere.blackarcana.content.blood.SanguineHarvestPlanner;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntime;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntimeManager;
import dev.gustavopere.blackarcana.core.world.EntityInteractionType;
import dev.gustavopere.blackarcana.core.world.EntityProtectionFacts;
import dev.gustavopere.blackarcana.core.world.ProtectionQuery;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Set;
import java.util.UUID;

/** Server-authoritative one-pulse settlement for Sanguine Harvest. */
public final class MinecraftSanguineHarvestRuntime {
    /** Canonical global hard ceiling for entities inspected by one spatial query. */
    public static final int MAX_INSPECTED_CANDIDATES = 256;
    /** Sanguine Harvest uses the ordinary ward hard radius until Stage 08 tightens defaults. */
    public static final double MAX_RANGE = 32.0D;

    private MinecraftSanguineHarvestRuntime() { }

    public static HarvestResult harvest(
        MinecraftServer server,
        UUID casterId,
        List<UUID> targetIds,
        int maxTargets,
        double maxTotalYield,
        double maxDrainPerTarget,
        double range,
        Map<UUID, Double> antiFarmWeights
    ) {
        Objects.requireNonNull(server, "server");
        Objects.requireNonNull(casterId, "casterId");
        Objects.requireNonNull(targetIds, "targetIds");
        Objects.requireNonNull(antiFarmWeights, "antiFarmWeights");

        ArcanaDecision requestValidation = validateRequest(
            targetIds,
            maxTargets,
            maxTotalYield,
            maxDrainPerTarget,
            range,
            antiFarmWeights);
        if (!requestValidation.allowed()) return new HarvestResult(requestValidation, 0.0D, 0);

        LivingEntity caster = findLoadedLivingEntity(server, casterId);
        if (caster == null || !caster.isAlive() || !(caster.level() instanceof ServerLevel casterLevel)) {
            return HarvestResult.denied(
                "sanguine_harvest_caster_unavailable",
                "Sanguine Harvest requires a loaded living caster on a server level");
        }

        ArcanaServerRuntime runtime = ArcanaServerRuntimeManager.get(server).orElse(null);
        if (runtime == null) {
            return HarvestResult.denied(
                "sanguine_harvest_runtime_unavailable",
                "Black Arcana server runtime is unavailable");
        }

        double rangeSquared = range * range;
        Set<UUID> seen = new HashSet<>();
        List<SanguineHarvestPlanner.Candidate> candidates = new ArrayList<>();
        for (UUID targetId : targetIds) {
            if (targetId == null || targetId.equals(casterId) || !seen.add(targetId)) continue;
            LivingEntity target = findLoadedLivingEntity(server, targetId);
            if (!isSpatiallyEligible(caster, casterLevel, target, rangeSquared)) continue;
            EntityProtectionFacts facts = MinecraftEntityProtectionResolver.resolve(server, caster, target);
            if (target instanceof Player || facts.boss()) continue;
            if (!authorizeTarget(runtime, caster, target, casterLevel, facts).allowed()) continue;

            double weight = antiFarmWeights.getOrDefault(targetId, 0.0D);
            double availableHealth = Math.max(0.0D, target.getHealth());
            candidates.add(new SanguineHarvestPlanner.Candidate(
                targetId,
                Math.min(maxDrainPerTarget, availableHealth),
                weight,
                true));
        }

        final SanguineHarvestPlanner.HarvestPlan plan;
        try {
            plan = SanguineHarvestPlanner.plan(candidates, maxTargets, maxTotalYield);
        } catch (IllegalArgumentException invalidPlan) {
            return HarvestResult.denied(
                "sanguine_harvest_plan_invalid",
                "Sanguine Harvest request violates bounded planner rules");
        }

        double actualYield = 0.0D;
        int drainedTargets = 0;
        for (SanguineHarvestPlanner.Drain drain : plan.drains()) {
            LivingEntity target = findLoadedLivingEntity(server, drain.entityId());
            if (!isSpatiallyEligible(caster, casterLevel, target, rangeSquared)) continue;
            EntityProtectionFacts facts = MinecraftEntityProtectionResolver.resolve(server, caster, target);
            if (target instanceof Player || facts.boss()) continue;
            if (!authorizeTarget(runtime, caster, target, casterLevel, facts).allowed()) continue;

            double remainingBudget = maxTotalYield - actualYield;
            if (remainingBudget <= 0.0D) break;
            float requestedDrain = (float) Math.min(drain.amount(), remainingBudget);
            if (!Float.isFinite(requestedDrain) || requestedDrain <= 0.0F) continue;

            float beforeHealth = target.getHealth();
            boolean accepted = target.hurt(
                target.damageSources().indirectMagic(caster, caster),
                requestedDrain);
            if (!accepted) continue;

            double actualLoss = Math.max(0.0D, beforeHealth - target.getHealth());
            actualLoss = Math.min(actualLoss, remainingBudget);
            if (actualLoss <= 0.0D) continue;
            actualYield += actualLoss;
            drainedTargets++;
        }

        return new HarvestResult(ArcanaDecision.allow(), actualYield, drainedTargets);
    }

    private static ArcanaDecision validateRequest(
        List<UUID> targetIds,
        int maxTargets,
        double maxTotalYield,
        double maxDrainPerTarget,
        double range,
        Map<UUID, Double> antiFarmWeights
    ) {
        if (targetIds.size() > MAX_INSPECTED_CANDIDATES) {
            return ArcanaDecision.deny(
                "sanguine_harvest_inspection_cap",
                "Sanguine Harvest candidate list exceeds the spatial-query hard ceiling");
        }
        if (maxTargets <= 0 || maxTargets > BloodSafetyCeilings.MAX_HARVEST_TARGETS) {
            return ArcanaDecision.deny(
                "sanguine_harvest_target_cap",
                "Sanguine Harvest target cap is outside hard bounds");
        }
        if (!Double.isFinite(maxTotalYield) || maxTotalYield <= 0.0D) {
            return ArcanaDecision.deny(
                "sanguine_harvest_yield_invalid",
                "Sanguine Harvest total yield budget must be finite and positive");
        }
        if (!Double.isFinite(maxDrainPerTarget) || maxDrainPerTarget <= 0.0D) {
            return ArcanaDecision.deny(
                "sanguine_harvest_drain_invalid",
                "Sanguine Harvest per-target drain must be finite and positive");
        }
        if (!Double.isFinite(range) || range <= 0.0D || range > MAX_RANGE) {
            return ArcanaDecision.deny(
                "sanguine_harvest_range_invalid",
                "Sanguine Harvest range is outside the ordinary ward hard ceiling");
        }
        for (Map.Entry<UUID, Double> entry : antiFarmWeights.entrySet()) {
            if (entry.getKey() == null || entry.getValue() == null
                || !Double.isFinite(entry.getValue())
                || entry.getValue() < 0.0D
                || entry.getValue() > 1.0D) {
                return ArcanaDecision.deny(
                    "sanguine_harvest_weight_invalid",
                    "Sanguine Harvest anti-farm weights must be finite values in [0,1]");
            }
        }
        return ArcanaDecision.allow();
    }

    private static boolean isSpatiallyEligible(
        LivingEntity caster,
        ServerLevel casterLevel,
        LivingEntity target,
        double rangeSquared
    ) {
        return target != null
            && target.isAlive()
            && target.level() == casterLevel
            && caster.distanceToSqr(target) <= rangeSquared
            && caster.hasLineOfSight(target);
    }

    private static ArcanaDecision authorizeTarget(
        ArcanaServerRuntime runtime,
        LivingEntity caster,
        LivingEntity target,
        ServerLevel level,
        EntityProtectionFacts facts
    ) {
        return runtime.entityInteractionAdmission().authorize(
            EntityInteractionType.DAMAGE,
            facts,
            new ProtectionQuery(
                caster.getUUID(),
                level.dimension().location().toString(),
                target.getUUID().toString(),
                EntityInteractionType.DAMAGE))
            .decision();
    }

    private static LivingEntity findLoadedLivingEntity(MinecraftServer server, UUID entityId) {
        for (ServerLevel level : server.getAllLevels()) {
            Entity entity = level.getEntity(entityId);
            if (entity instanceof LivingEntity living) return living;
        }
        return null;
    }

    public record HarvestResult(ArcanaDecision decision, double totalYield, int drainedTargets) {
        public HarvestResult {
            Objects.requireNonNull(decision, "decision");
            if (!Double.isFinite(totalYield) || totalYield < 0.0D) {
                throw new IllegalArgumentException("totalYield must be finite and non-negative");
            }
            if (drainedTargets < 0 || drainedTargets > BloodSafetyCeilings.MAX_HARVEST_TARGETS) {
                throw new IllegalArgumentException("drainedTargets outside hard bounds");
            }
            if (!decision.allowed() && (totalYield != 0.0D || drainedTargets != 0)) {
                throw new IllegalArgumentException("denied harvest cannot report settled yield");
            }
        }

        public static HarvestResult denied(String code, String detail) {
            return new HarvestResult(ArcanaDecision.deny(code, detail), 0.0D, 0);
        }
    }
}
