package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.content.noetic.DivinationVisibilityPolicy;
import dev.gustavopere.blackarcana.content.noetic.FamiliarSafetyCeilings;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;

import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;
import java.util.Objects;
import java.util.Set;
import java.util.UUID;

/** Server-authoritative privacy boundary for Occult Appraisal. */
public final class MinecraftOccultAppraisalRuntime {
    private MinecraftOccultAppraisalRuntime() { }

    public static AppraisalResult appraise(
            MinecraftServer server,
            UUID casterId,
            UUID targetId,
            double maxRange,
            Set<String> requestedFields
    ) {
        Objects.requireNonNull(server, "server");
        Objects.requireNonNull(casterId, "casterId");
        Objects.requireNonNull(targetId, "targetId");
        Objects.requireNonNull(requestedFields, "requestedFields");

        if (!Double.isFinite(maxRange) || maxRange <= 0.0D || maxRange > FamiliarSafetyCeilings.MAX_SCRY_RANGE) {
            return AppraisalResult.denied(
                "occult_appraisal_range_config",
                "Occult Appraisal range is outside the noetic safety ceiling");
        }

        LivingEntity caster = findLoadedLivingEntity(server, casterId);
        if (caster == null || !caster.isAlive() || !(caster.level() instanceof ServerLevel casterLevel)) {
            return AppraisalResult.denied(
                "occult_appraisal_caster_unavailable",
                "Occult Appraisal requires a loaded living caster");
        }

        Entity target = casterLevel.getEntity(targetId);
        if (target == null || !target.isAlive()) {
            return AppraisalResult.denied(
                "occult_appraisal_target_unavailable",
                "Occult Appraisal resolves only a currently loaded target in the caster dimension");
        }
        if (target instanceof Player) {
            return AppraisalResult.denied(
                "occult_appraisal_player_privacy",
                "Player targets require an explicit server privacy or consent policy before metadata may be exposed");
        }

        double distanceSquared = caster.distanceToSqr(target);
        double rangeSquared = maxRange * maxRange;
        if (!Double.isFinite(distanceSquared) || distanceSquared > rangeSquared) {
            return AppraisalResult.denied(
                "occult_appraisal_range",
                "Occult Appraisal target is outside configured range");
        }
        if (!caster.hasLineOfSight(target)) {
            return AppraisalResult.denied(
                "occult_appraisal_los",
                "Occult Appraisal requires server-validated line of sight");
        }

        DivinationVisibilityPolicy policy = new DivinationVisibilityPolicy(maxRange);
        Set<String> allowedFields = policy.filterMetadata(requestedFields);
        if (allowedFields.isEmpty()) {
            return AppraisalResult.denied(
                "occult_appraisal_no_approved_metadata",
                "Occult Appraisal request contains no server-approved metadata fields");
        }

        Map<String, String> metadata = new LinkedHashMap<>();
        for (String field : allowedFields) {
            String value = value(field, target);
            if (value != null) metadata.put(field, value);
        }
        return new AppraisalResult(ArcanaDecision.allow(), Map.copyOf(metadata));
    }

    private static LivingEntity findLoadedLivingEntity(MinecraftServer server, UUID entityId) {
        for (ServerLevel level : server.getAllLevels()) {
            Entity entity = level.getEntity(entityId);
            if (entity instanceof LivingEntity living) return living;
        }
        return null;
    }

    private static String value(String field, Entity target) {
        if (!(target instanceof LivingEntity living)) {
            return "occult_trace".equals(field) ? "none" : null;
        }
        return switch (field) {
            case "health" -> String.format(Locale.ROOT, "%.3f/%.3f", living.getHealth(), living.getMaxHealth());
            case "held_item" -> BuiltInRegistries.ITEM.getKey(living.getMainHandItem().getItem()).toString();
            case "status_effects" -> Integer.toString(living.getActiveEffects().size());
            case "armor_summary" -> Integer.toString(equippedArmorPieces(living));
            case "occult_trace" -> "none";
            default -> null;
        };
    }

    private static int equippedArmorPieces(LivingEntity living) {
        int count = 0;
        for (ItemStack stack : living.getArmorSlots()) {
            if (!stack.isEmpty()) count++;
        }
        return count;
    }

    public record AppraisalResult(ArcanaDecision decision, Map<String, String> metadata) {
        public AppraisalResult {
            Objects.requireNonNull(decision, "decision");
            metadata = Map.copyOf(Objects.requireNonNull(metadata, "metadata"));
            if (!decision.allowed() && !metadata.isEmpty()) {
                throw new IllegalArgumentException("denied Occult Appraisal cannot expose metadata");
            }
        }

        private static AppraisalResult denied(String code, String detail) {
            return new AppraisalResult(ArcanaDecision.deny(code, detail), Map.of());
        }
    }
}
