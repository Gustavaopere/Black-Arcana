package dev.gustavopere.blackarcana.integration.rpg;

import dev.gustavopere.blackarcana.api.ArcanaDecision;
import java.util.Objects;
import java.util.Optional;

public record RpgProgressionQuery(ArcanaDecision decision, Optional<RpgProgressionSnapshot> snapshot) {
    public RpgProgressionQuery {
        Objects.requireNonNull(decision, "decision");
        Objects.requireNonNull(snapshot, "snapshot");
        if (decision.allowed() != snapshot.isPresent()) {
            throw new IllegalArgumentException("allowed query must contain exactly one snapshot");
        }
    }

    public static RpgProgressionQuery success(RpgProgressionSnapshot snapshot) {
        return new RpgProgressionQuery(ArcanaDecision.allow(), Optional.of(Objects.requireNonNull(snapshot)));
    }

    public static RpgProgressionQuery denied(String code, String detail) {
        return new RpgProgressionQuery(ArcanaDecision.deny(code, detail), Optional.empty());
    }
}
