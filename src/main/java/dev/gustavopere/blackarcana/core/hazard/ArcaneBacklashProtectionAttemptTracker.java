package dev.gustavopere.blackarcana.core.hazard;

import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.hazard.ArcanaDamageInstanceId;
import dev.gustavopere.blackarcana.api.hazard.ArcaneEmergencyProtectionSnapshot;

import java.util.IdentityHashMap;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;
import java.util.UUID;

/**
 * Bounded identity tracker bridging one synchronous platform backlash source into its frozen
 * emergency-protection attempt. Tokens are compared by object identity intentionally.
 */
public final class ArcaneBacklashProtectionAttemptTracker<T> {
    public static final int ABSOLUTE_MAX_TRACKED = 65_536;

    public record Attempt(
        ArcanaCastId rootCastId,
        ArcanaDamageInstanceId damageInstanceId,
        UUID casterId,
        boolean protectionAllowed,
        ArcaneEmergencyProtectionSnapshot emergencyProtectionSnapshot
    ) {
        public Attempt {
            Objects.requireNonNull(rootCastId, "rootCastId");
            Objects.requireNonNull(damageInstanceId, "damageInstanceId");
            Objects.requireNonNull(casterId, "casterId");
            Objects.requireNonNull(emergencyProtectionSnapshot, "emergencyProtectionSnapshot");
        }
    }

    private final int maxTracked;
    private final Map<T, Attempt> tracked = new IdentityHashMap<>();

    public ArcaneBacklashProtectionAttemptTracker(int maxTracked) {
        if (maxTracked <= 0 || maxTracked > ABSOLUTE_MAX_TRACKED) {
            throw new IllegalArgumentException("maxTracked outside absolute bounds");
        }
        this.maxTracked = maxTracked;
    }

    public synchronized boolean register(T token, Attempt attempt) {
        Objects.requireNonNull(token, "token");
        Objects.requireNonNull(attempt, "attempt");
        if (tracked.containsKey(token) || tracked.size() >= maxTracked) return false;
        tracked.put(token, attempt);
        return true;
    }

    public synchronized Optional<Attempt> find(T token) {
        return Optional.ofNullable(tracked.get(Objects.requireNonNull(token, "token")));
    }

    public synchronized Optional<Attempt> release(T token) {
        return Optional.ofNullable(tracked.remove(Objects.requireNonNull(token, "token")));
    }

    public synchronized int size() {
        return tracked.size();
    }
}
