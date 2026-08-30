package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.content.noetic.DivinationVisibilityPolicy;
import dev.gustavopere.blackarcana.content.noetic.FamiliarSafetyCeilings;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.item.ItemStack;

import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;
import java.util.Objects;
import java.util.Set;
import java.util.UUID;

/**
 * Server-authoritative remote perception boundary for Namescry.
 *
 * <p>The runtime resolves targets only from the caster's already-loaded ServerLevel. It never creates
 * a chunk ticket or searches other dimensions. Player targets remain fail-closed until Black Arcana
 * has an explicit server-side consent/covenant authorization provider; no client-supplied boolean is
 * accepted as authority.</p>
 */
public final class MinecraftNamescryRuntime {
    private MinecraftNamescryRuntime() { }

    public static NamescryResult namescry(
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
            return NamescryResult.denied(
                "namescry_range_config",
                "Namescry range is outside the noetic safety ceiling");
        }

        LivingEntity caster = findLoadedLivingEntity(server, casterId);
        if (caster == null || !caster.isAlive() || !(caster.level() instanceof ServerLevel casterLevel)) {
            return NamescryResult.denied(
                "namescry_caster_unavailable",
                "Namescry requires a loaded living caster");
        }

        Entity target = casterLevel.getEntity(targetId);
        if (target == null || !target.isAlive()) {
            return NamescryResult.denied(
                "namescry_target_unavailable",
                "Namescry resolves only a currently loaded target in the caster dimension");
        }

        double distanceSquared = caster.distanceToSqr(target);
        if (!Double.isFinite(distanceSquared)) {
            return NamescryResult.denied(
                "namescry_target_invalid",
                "Namescry target distance is not finite");
        }
        double distance = Math.sqrt(distanceSquared);
        if (distance > maxRange) {
            return NamescryResult.denied(
                "namescry_range",
                "Namescry target is outside configured range");
        }

        if (target instanceof ServerPlayer) {
            return NamescryResult.denied(
                "namescry_player_authorization",
                "Namescry player targets require server-side consent or covenant authorization");
        }

        DivinationVisibilityPolicy policy = new DivinationVisibilityPolicy(maxRange);
        DivinationVisibilityPolicy.Facts facts = new DivinationVisibilityPolicy.Facts(
            true,
            true,
            false,
            false,
            false,
            distance);
        if (!policy.canNamescry(facts)) {
            return NamescryResult.denied(
                "namescry_policy",
                "Namescry target was denied by the server visibility policy");
        }

        Set<String> allowedFields = policy.filterMetadata(requestedFields);
        Map<String, String> metadata = new LinkedHashMap<>();
        for (String field : allowedFields) {
            String value = value(field, target);
            if (value != null) metadata.put(field, value);
        }
        return new NamescryResult(ArcanaDecision.allow(), Map.copyOf(metadata));
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

    public record NamescryResult(ArcanaDecision decision, Map<String, String> metadata) {
        public NamescryResult {
            Objects.requireNonNull(decision, "decision");
            metadata = Map.copyOf(Objects.requireNonNull(metadata, "metadata"));
            if (!decision.allowed() && !metadata.isEmpty()) {
                throw new IllegalArgumentException("denied Namescry cannot expose metadata");
            }
        }

        private static NamescryResult denied(String code, String detail) {
            return new NamescryResult(ArcanaDecision.deny(code, detail), Map.of());
        }
    }
}
