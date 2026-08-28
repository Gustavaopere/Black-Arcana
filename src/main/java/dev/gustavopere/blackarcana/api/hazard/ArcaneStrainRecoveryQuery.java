package dev.gustavopere.blackarcana.api.hazard;

import java.util.Objects;
import java.util.UUID;

/** Server-owned facts available to strain recovery providers. */
public record ArcaneStrainRecoveryQuery(UUID playerId, long serverTick, double storedUnits) {
    public ArcaneStrainRecoveryQuery {
        Objects.requireNonNull(playerId, "playerId");
        if (serverTick < 0L) throw new IllegalArgumentException("serverTick cannot be negative");
        if (!Double.isFinite(storedUnits) || storedUnits < 0.0D) {
            throw new IllegalArgumentException("storedUnits must be finite and non-negative");
        }
    }
}
