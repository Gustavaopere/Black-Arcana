package dev.gustavopere.blackarcana.api;

import java.util.Objects;

public record ArcanaCastResult(Status status, String code, String detail) {
    public enum Status {
        SUCCESS,
        DENIED_IDENTITY,
        DENIED_REPLAY,
        DENIED_PROGRESSION,
        DENIED_COOLDOWN,
        DENIED_TARGET,
        DENIED_COST,
        DENIED_WORLD_POLICY,
        EFFECT_FAILED
    }

    public ArcanaCastResult {
        Objects.requireNonNull(status, "status");
        Objects.requireNonNull(code, "code");
        Objects.requireNonNull(detail, "detail");
    }

    public static ArcanaCastResult success(String detail) {
        return new ArcanaCastResult(Status.SUCCESS, "ok", detail);
    }

    public static ArcanaCastResult denied(Status status, ArcanaDecision decision) {
        if (status == Status.SUCCESS) throw new IllegalArgumentException("denial cannot use SUCCESS status");
        return new ArcanaCastResult(status, decision.code(), decision.detail());
    }
}
