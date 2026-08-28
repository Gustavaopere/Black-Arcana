package dev.gustavopere.blackarcana.core.ritual;

import java.util.Objects;
import java.util.UUID;

public record RitualActivationId(UUID value) {
    public RitualActivationId {
        Objects.requireNonNull(value, "value");
    }

    public static RitualActivationId parse(String value) {
        return new RitualActivationId(UUID.fromString(Objects.requireNonNull(value, "value")));
    }

    public String canonical() {
        return value.toString();
    }
}
