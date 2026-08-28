package dev.gustavopere.blackarcana.core.world;

import dev.gustavopere.blackarcana.api.ArcanaDecision;

import java.util.Objects;

public record EntityInteractionAuthorization(ArcanaDecision decision, EntityEffectLimits limits) {
    public EntityInteractionAuthorization {
        Objects.requireNonNull(decision, "decision");
        Objects.requireNonNull(limits, "limits");
    }

    public static EntityInteractionAuthorization allow(EntityEffectLimits limits) {
        return new EntityInteractionAuthorization(ArcanaDecision.allow(), limits);
    }

    public static EntityInteractionAuthorization deny(String code, String detail, EntityEffectLimits limits) {
        return new EntityInteractionAuthorization(ArcanaDecision.deny(code, detail), limits);
    }
}
