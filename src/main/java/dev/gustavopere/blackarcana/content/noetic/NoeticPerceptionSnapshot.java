package dev.gustavopere.blackarcana.content.noetic;

import java.util.ArrayList;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Objects;
import java.util.UUID;

/**
 * Whitelisted read-only perception payload for Stage 07.07.
 *
 * <p>The schema deliberately excludes arbitrary NBT, inventories, capabilities and provider-private state.</p>
 */
public record NoeticPerceptionSnapshot(
        UUID targetId,
        String entityTypeId,
        String displayName,
        double healthFraction,
        List<String> activeEffectIds,
        String mainHandItemId
) {
    private static final int MAX_RESOURCE_ID_LENGTH = 160;

    public NoeticPerceptionSnapshot {
        Objects.requireNonNull(targetId, "targetId");
        entityTypeId = boundedResourceId(entityTypeId, "minecraft:unknown");
        displayName = boundedDisplayName(displayName);
        healthFraction = sanitizeHealthFraction(healthFraction);
        activeEffectIds = sanitizeEffects(activeEffectIds);
        mainHandItemId = boundedResourceId(mainHandItemId, "minecraft:air");
    }

    public static NoeticPerceptionSnapshot sanitized(
            UUID targetId,
            String entityTypeId,
            String displayName,
            double healthFraction,
            List<String> activeEffectIds,
            String mainHandItemId
    ) {
        return new NoeticPerceptionSnapshot(
                targetId,
                entityTypeId,
                displayName,
                healthFraction,
                activeEffectIds,
                mainHandItemId);
    }

    private static String boundedDisplayName(String input) {
        Objects.requireNonNull(input, "displayName");
        String sanitized = stripControls(input);
        if (sanitized.length() > NoeticSafetyCeilings.MAX_DISPLAY_NAME_LENGTH) {
            return sanitized.substring(0, NoeticSafetyCeilings.MAX_DISPLAY_NAME_LENGTH);
        }
        return sanitized;
    }

    private static List<String> sanitizeEffects(List<String> input) {
        Objects.requireNonNull(input, "activeEffectIds");
        LinkedHashSet<String> deduplicated = new LinkedHashSet<>();
        for (String effectId : input) {
            if (deduplicated.size() >= NoeticSafetyCeilings.MAX_EFFECT_IDS) break;
            deduplicated.add(boundedResourceId(effectId, "minecraft:unknown"));
        }
        return List.copyOf(new ArrayList<>(deduplicated));
    }

    private static double sanitizeHealthFraction(double value) {
        if (!Double.isFinite(value)) return 0.0D;
        if (value <= 0.0D) return 0.0D;
        return Math.min(1.0D, value);
    }

    private static String boundedResourceId(String input, String fallback) {
        Objects.requireNonNull(fallback, "fallback");
        if (input == null) return fallback;
        String normalized = stripControls(input.trim());
        if (normalized.isEmpty()) return fallback;
        if (normalized.length() > MAX_RESOURCE_ID_LENGTH) {
            normalized = normalized.substring(0, MAX_RESOURCE_ID_LENGTH);
        }
        return normalized;
    }

    private static String stripControls(String input) {
        StringBuilder out = new StringBuilder(input.length());
        for (int i = 0; i < input.length(); i++) {
            char current = input.charAt(i);
            if (!Character.isISOControl(current)) out.append(current);
        }
        return out.toString();
    }
}
