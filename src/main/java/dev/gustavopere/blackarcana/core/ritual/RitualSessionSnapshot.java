package dev.gustavopere.blackarcana.core.ritual;

import java.util.Objects;

public record RitualSessionSnapshot(
        ArcanaRitualId ritualId,
        RitualActivationId activationId,
        RitualContext context,
        long startedAtTick,
        long commitAtTick,
        long completeAtTick,
        RitualSessionState state
) {
    public RitualSessionSnapshot {
        Objects.requireNonNull(ritualId, "ritualId");
        Objects.requireNonNull(activationId, "activationId");
        Objects.requireNonNull(context, "context");
        Objects.requireNonNull(state, "state");
        if (startedAtTick < 0L || commitAtTick < startedAtTick || completeAtTick < commitAtTick) {
            throw new IllegalArgumentException("invalid ritual session timeline");
        }
    }
}
