package dev.gustavopere.blackarcana.core.world;

import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaDecision;

import java.util.ArrayList;
import java.util.Collection;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;
import java.util.UUID;

/**
 * Bounded lifecycle tracker for temporary block mutations.
 * It never loads chunks: an unavailable state lookup simply leaves restoration pending.
 */
public final class TemporaryMutationTracker {
    private final int maxEntries;
    private final Map<TemporaryMutationKey, TemporaryWorldMutation> entries = new LinkedHashMap<>();

    public TemporaryMutationTracker(int maxEntries) {
        if (maxEntries <= 0) throw new IllegalArgumentException("maxEntries must be positive");
        this.maxEntries = maxEntries;
    }

    public synchronized RegistrationResult register(
        TemporaryMutationKey key,
        UUID ownerId,
        ArcanaCastId castId,
        String observedCurrentState,
        String replacementState,
        long expiresAtTick
    ) {
        Objects.requireNonNull(key, "key");
        Objects.requireNonNull(ownerId, "ownerId");
        Objects.requireNonNull(castId, "castId");
        Objects.requireNonNull(observedCurrentState, "observedCurrentState");
        Objects.requireNonNull(replacementState, "replacementState");
        if (expiresAtTick < 0L) throw new IllegalArgumentException("expiresAtTick cannot be negative");

        TemporaryWorldMutation previous = entries.get(key);
        if (previous == null && entries.size() >= maxEntries) {
            return RegistrationResult.denied("temporary_mutation_capacity", "Temporary mutation tracker is full");
        }

        String original = previous != null && previous.replacementState().equals(observedCurrentState)
            ? previous.originalState()
            : observedCurrentState;
        long effectiveExpiry = previous != null && previous.replacementState().equals(observedCurrentState)
            ? Math.max(previous.expiresAtTick(), expiresAtTick)
            : expiresAtTick;

        TemporaryWorldMutation mutation = new TemporaryWorldMutation(
            key, ownerId, castId, original, replacementState, effectiveExpiry);
        entries.put(key, mutation);
        return RegistrationResult.accepted(mutation, previous);
    }

    /** Undo a just-created tracking record only when it is still the current record. */
    public synchronized boolean rollbackRegistration(RegistrationResult registration) {
        Objects.requireNonNull(registration, "registration");
        if (!registration.decision().allowed() || registration.mutation() == null) return false;
        TemporaryWorldMutation current = entries.get(registration.mutation().key());
        if (!registration.mutation().equals(current)) return false;
        if (registration.previousMutation() == null) {
            entries.remove(registration.mutation().key());
        } else {
            entries.put(registration.mutation().key(), registration.previousMutation());
        }
        return true;
    }

    public synchronized List<ExpiryAction> inspectExpired(long nowTick, int maxChecks, StateReader reader) {
        Objects.requireNonNull(reader, "reader");
        if (maxChecks <= 0) throw new IllegalArgumentException("maxChecks must be positive");
        List<ExpiryAction> actions = new ArrayList<>();
        int checked = 0;
        for (TemporaryWorldMutation mutation : List.copyOf(entries.values())) {
            if (checked >= maxChecks) break;
            if (mutation.expiresAtTick() > nowTick) continue;
            checked++;

            Optional<String> current = Objects.requireNonNull(reader.read(mutation.key()), "state lookup");
            if (current.isEmpty()) {
                actions.add(ExpiryAction.unavailable(mutation));
                continue;
            }
            if (!current.get().equals(mutation.replacementState())) {
                entries.remove(mutation.key());
                actions.add(ExpiryAction.dropChanged(mutation, current.get()));
                continue;
            }
            actions.add(ExpiryAction.restore(mutation));
        }
        return List.copyOf(actions);
    }

    public synchronized boolean confirmRestored(TemporaryMutationKey key, String observedStateAfterRestore) {
        Objects.requireNonNull(key, "key");
        Objects.requireNonNull(observedStateAfterRestore, "observedStateAfterRestore");
        TemporaryWorldMutation mutation = entries.get(key);
        if (mutation == null) return false;
        if (!mutation.originalState().equals(observedStateAfterRestore)) return false;
        entries.remove(key);
        return true;
    }

    public synchronized int size() {
        return entries.size();
    }

    public synchronized List<TemporaryWorldMutation> snapshot() {
        return List.copyOf(entries.values());
    }

    public synchronized int restoreSnapshot(Collection<TemporaryWorldMutation> snapshot) {
        Objects.requireNonNull(snapshot, "snapshot");
        entries.clear();
        int restored = 0;
        for (TemporaryWorldMutation mutation : snapshot) {
            if (mutation == null || restored >= maxEntries) continue;
            entries.put(mutation.key(), mutation);
            restored++;
        }
        return restored;
    }

    @FunctionalInterface
    public interface StateReader {
        /** Empty means the chunk/world is unavailable and must not be force-loaded. */
        Optional<String> read(TemporaryMutationKey key);
    }

    public record RegistrationResult(
        ArcanaDecision decision,
        TemporaryWorldMutation mutation,
        TemporaryWorldMutation previousMutation
    ) {
        public RegistrationResult {
            Objects.requireNonNull(decision, "decision");
            if (decision.allowed() != (mutation != null)) {
                throw new IllegalArgumentException("accepted registration must carry exactly one mutation");
            }
            if (!decision.allowed() && previousMutation != null) {
                throw new IllegalArgumentException("denied registration cannot carry previous mutation state");
            }
        }

        public static RegistrationResult accepted(
            TemporaryWorldMutation mutation,
            TemporaryWorldMutation previousMutation
        ) {
            return new RegistrationResult(
                ArcanaDecision.allow(),
                Objects.requireNonNull(mutation, "mutation"),
                previousMutation);
        }

        public static RegistrationResult denied(String code, String detail) {
            return new RegistrationResult(ArcanaDecision.deny(code, detail), null, null);
        }
    }

    public record ExpiryAction(Kind kind, TemporaryWorldMutation mutation, String observedState) {
        public ExpiryAction {
            Objects.requireNonNull(kind, "kind");
            Objects.requireNonNull(mutation, "mutation");
            observedState = observedState == null ? "" : observedState;
        }

        public enum Kind { RESTORE, DROP_CHANGED, UNAVAILABLE }

        public static ExpiryAction restore(TemporaryWorldMutation mutation) {
            return new ExpiryAction(Kind.RESTORE, mutation, mutation.replacementState());
        }

        public static ExpiryAction dropChanged(TemporaryWorldMutation mutation, String observedState) {
            return new ExpiryAction(Kind.DROP_CHANGED, mutation, observedState);
        }

        public static ExpiryAction unavailable(TemporaryWorldMutation mutation) {
            return new ExpiryAction(Kind.UNAVAILABLE, mutation, "");
        }
    }
}
