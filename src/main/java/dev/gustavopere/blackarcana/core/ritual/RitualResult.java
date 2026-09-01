package dev.gustavopere.blackarcana.core.ritual;

import dev.gustavopere.blackarcana.api.ArcanaDecision;

import java.util.Objects;

public record RitualResult(Status status, String code, String detail) {
    public enum Status {
        STARTED,
        INTERRUPTED_PRECOMMIT,
        INTERRUPTED_POSTCOMMIT,
        DENIED_REQUIREMENT,
        DENIED_REPLAY,
        DENIED_ANCHOR_BUSY,
        DENIED_CAPACITY,
        DENIED_NOT_ACTIVE
    }

    public RitualResult {
        Objects.requireNonNull(status, "status");
        Objects.requireNonNull(code, "code");
        Objects.requireNonNull(detail, "detail");
    }

    public static RitualResult started() {
        return new RitualResult(Status.STARTED, "ok", "");
    }

    public static RitualResult denied(Status status, ArcanaDecision decision) {
        if (decision.allowed()) throw new IllegalArgumentException("denied result requires denied decision");
        return new RitualResult(status, decision.code(), decision.detail());
    }

    public static RitualResult of(Status status, String code, String detail) {
        return new RitualResult(status, code, detail);
    }
}
