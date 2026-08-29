package dev.gustavopere.blackarcana.core.ritual;

import java.util.Objects;

public record RitualDefinition(
        ArcanaRitualId id,
        long commitDelayTicks,
        long completionDelayTicks
) {
    public static final long MAX_DURATION_TICKS = 20L * 60L * 60L;

    public RitualDefinition {
        Objects.requireNonNull(id, "id");
        if (commitDelayTicks < 0L || commitDelayTicks > MAX_DURATION_TICKS) {
            throw new IllegalArgumentException("commitDelayTicks outside bounds");
        }
        if (completionDelayTicks < commitDelayTicks || completionDelayTicks > MAX_DURATION_TICKS) {
            throw new IllegalArgumentException("completionDelayTicks must be >= commit delay and bounded");
        }
    }
}
