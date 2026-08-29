package dev.gustavopere.blackarcana.core.ritual;

import java.util.Objects;
import java.util.UUID;

/** Stable idempotency key for durable ritual outcomes. */
public record RitualCompletionKey(ArcanaRitualId ritualId, Scope scope, String subjectId) {
    public static final int MAX_SUBJECT_ID_LENGTH = 256;

    public RitualCompletionKey {
        Objects.requireNonNull(ritualId, "ritualId");
        Objects.requireNonNull(scope, "scope");
        Objects.requireNonNull(subjectId, "subjectId");
        if (subjectId.isBlank() || subjectId.length() > MAX_SUBJECT_ID_LENGTH) {
            throw new IllegalArgumentException("ritual completion subjectId must be non-blank and bounded");
        }
    }

    public static RitualCompletionKey forAnchor(ArcanaRitualId ritualId, RitualAnchor anchor) {
        Objects.requireNonNull(anchor, "anchor");
        return new RitualCompletionKey(
            ritualId,
            Scope.ANCHOR,
            anchor.dimensionId() + '@' + anchor.packedBlockPos());
    }

    public static RitualCompletionKey forCaster(ArcanaRitualId ritualId, UUID casterId) {
        return new RitualCompletionKey(
            ritualId,
            Scope.CASTER,
            Objects.requireNonNull(casterId, "casterId").toString());
    }

    public enum Scope {
        ANCHOR,
        CASTER
    }
}
