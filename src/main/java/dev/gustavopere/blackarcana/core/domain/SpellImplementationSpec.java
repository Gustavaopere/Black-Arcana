package dev.gustavopere.blackarcana.core.domain;

import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.core.world.WorldEffectMode;

import java.util.Objects;

/**
 * Implementation-facing checklist required for every Stage 07 spell/mechanic.
 * This is descriptive metadata only; gameplay authority remains in the server runtime.
 */
public record SpellImplementationSpec(
    ArcanaSpellId spellId,
    ArcanaDomain domain,
    String fantasy,
    String hostIntegration,
    String invocation,
    String targetRules,
    String resourceCost,
    long cooldownTicks,
    String scalingEquation,
    String progressionGate,
    WorldEffectMode worldEffectMode,
    String bossPvpBehavior,
    String configSurface,
    String provenance
) {
    public static final long ABSOLUTE_MAX_COOLDOWN_TICKS = 20L * 60L * 60L;

    public SpellImplementationSpec {
        Objects.requireNonNull(spellId, "spellId");
        Objects.requireNonNull(domain, "domain");
        Objects.requireNonNull(worldEffectMode, "worldEffectMode");
        fantasy = bounded(fantasy, "fantasy");
        hostIntegration = bounded(hostIntegration, "hostIntegration");
        invocation = bounded(invocation, "invocation");
        targetRules = bounded(targetRules, "targetRules");
        resourceCost = bounded(resourceCost, "resourceCost");
        scalingEquation = bounded(scalingEquation, "scalingEquation");
        progressionGate = bounded(progressionGate, "progressionGate");
        bossPvpBehavior = bounded(bossPvpBehavior, "bossPvpBehavior");
        configSurface = bounded(configSurface, "configSurface");
        provenance = bounded(provenance, "provenance");
        if (cooldownTicks < 0L || cooldownTicks > ABSOLUTE_MAX_COOLDOWN_TICKS) {
            throw new IllegalArgumentException("cooldownTicks outside technical bounds");
        }
    }

    private static String bounded(String value, String field) {
        Objects.requireNonNull(value, field);
        String trimmed = value.trim();
        if (trimmed.isEmpty() || trimmed.length() > 512) {
            throw new IllegalArgumentException(field + " must be non-blank and <= 512 characters");
        }
        return trimmed;
    }
}
