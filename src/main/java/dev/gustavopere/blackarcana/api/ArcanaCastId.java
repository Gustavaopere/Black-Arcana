package dev.gustavopere.blackarcana.api;

import java.util.Objects;
import java.util.UUID;

public record ArcanaCastId(UUID value) {
    public ArcanaCastId {
        Objects.requireNonNull(value, "value");
    }

    public static ArcanaCastId random() {
        return new ArcanaCastId(UUID.randomUUID());
    }

    public static ArcanaCastId parse(String value) {
        Objects.requireNonNull(value, "value");
        return new ArcanaCastId(UUID.fromString(value));
    }

    public String canonical() {
        return value.toString();
    }
}
