package dev.gustavopere.blackarcana.api.hazard;

import java.util.Objects;
import java.util.UUID;

/** Unique subordinate damage identity under one root ArcanaCastId. */
public record ArcanaDamageInstanceId(UUID value) {
    public ArcanaDamageInstanceId {
        Objects.requireNonNull(value, "value");
    }

    public static ArcanaDamageInstanceId random() {
        return new ArcanaDamageInstanceId(UUID.randomUUID());
    }

    public static ArcanaDamageInstanceId parse(String value) {
        Objects.requireNonNull(value, "value");
        return new ArcanaDamageInstanceId(UUID.fromString(value));
    }

    public String canonical() {
        return value.toString();
    }
}
