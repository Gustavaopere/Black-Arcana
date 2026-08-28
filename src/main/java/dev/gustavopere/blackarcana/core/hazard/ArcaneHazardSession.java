package dev.gustavopere.blackarcana.core.hazard;

import dev.gustavopere.blackarcana.api.hazard.ArcanaDamageInstanceId;
import dev.gustavopere.blackarcana.api.hazard.ArcanaDamageProvenance;
import dev.gustavopere.blackarcana.api.hazard.ArcaneHazardSnapshot;

import java.util.HashSet;
import java.util.Objects;
import java.util.Set;

/** Bounded mutable ledger shell for one immutable root hazard snapshot. */
public final class ArcaneHazardSession {
    public enum ClaimResult {
        ACCEPTED,
        DUPLICATE,
        PROVENANCE_MISMATCH,
        PROFILE_LIMIT,
        EXPIRED,
        CLOSED
    }

    private final ArcaneHazardSnapshot snapshot;
    private final long expiresAtTick;
    private final Set<ArcanaDamageInstanceId> seenDamageInstances = new HashSet<>();
    private boolean closed;

    public ArcaneHazardSession(ArcaneHazardSnapshot snapshot) {
        this.snapshot = Objects.requireNonNull(snapshot, "snapshot");
        this.expiresAtTick = saturatingAdd(snapshot.activatedAtTick(), snapshot.profile().damageLeaseTicks());
    }

    public synchronized ClaimResult claim(ArcanaDamageProvenance provenance, long currentTick) {
        Objects.requireNonNull(provenance, "provenance");
        if (currentTick < 0L) throw new IllegalArgumentException("currentTick cannot be negative");
        if (closed) return ClaimResult.CLOSED;
        if (isExpired(currentTick)) {
            closed = true;
            return ClaimResult.EXPIRED;
        }
        if (!matchesRoot(provenance)) return ClaimResult.PROVENANCE_MISMATCH;
        if (seenDamageInstances.contains(provenance.damageInstanceId())) return ClaimResult.DUPLICATE;
        if (seenDamageInstances.size() >= snapshot.profile().maxDamageInstances()) return ClaimResult.PROFILE_LIMIT;
        seenDamageInstances.add(provenance.damageInstanceId());
        return ClaimResult.ACCEPTED;
    }

    public synchronized void close() {
        closed = true;
    }

    public synchronized boolean closed() {
        return closed;
    }

    public synchronized int seenDamageInstances() {
        return seenDamageInstances.size();
    }

    public ArcaneHazardSnapshot snapshot() {
        return snapshot;
    }

    public long expiresAtTick() {
        return expiresAtTick;
    }

    public boolean isExpired(long currentTick) {
        if (currentTick < 0L) throw new IllegalArgumentException("currentTick cannot be negative");
        return currentTick >= expiresAtTick;
    }

    private boolean matchesRoot(ArcanaDamageProvenance provenance) {
        return snapshot.rootCastId().equals(provenance.rootCastId())
            && snapshot.casterId().equals(provenance.casterId())
            && snapshot.spellId().equals(provenance.spellId());
    }

    private static long saturatingAdd(long first, long second) {
        if (second > Long.MAX_VALUE - first) return Long.MAX_VALUE;
        return first + second;
    }
}
