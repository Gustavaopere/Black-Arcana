package dev.gustavopere.blackarcana.api;

import java.util.Objects;

public record ArcanaDecision(boolean allowed, String code, String detail) {
    public ArcanaDecision {
        Objects.requireNonNull(code, "code");
        Objects.requireNonNull(detail, "detail");
    }

    public static ArcanaDecision allow() {
        return new ArcanaDecision(true, "ok", "");
    }

    public static ArcanaDecision deny(String code, String detail) {
        return new ArcanaDecision(false, code, detail);
    }
}
