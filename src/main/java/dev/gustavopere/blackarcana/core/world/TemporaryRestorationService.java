package dev.gustavopere.blackarcana.core.world;

import java.util.List;
import java.util.Objects;
import java.util.Optional;
import java.util.concurrent.atomic.AtomicInteger;

/** Bounded restoration processor. Unloaded chunks remain pending and are never ticketed/loaded. */
public final class TemporaryRestorationService {
    private final TemporaryMutationTracker tracker;
    private final TemporaryBlockBackend backend;

    public TemporaryRestorationService(TemporaryMutationTracker tracker, TemporaryBlockBackend backend) {
        this.tracker = Objects.requireNonNull(tracker, "tracker");
        this.backend = Objects.requireNonNull(backend, "backend");
    }

    public TickResult tick(long nowTick, int maxChecks) {
        AtomicInteger readFailures = new AtomicInteger();
        List<TemporaryMutationTracker.ExpiryAction> actions = tracker.inspectExpired(
            nowTick,
            maxChecks,
            key -> {
                try {
                    return Objects.requireNonNull(backend.readLoadedState(key), "loaded state");
                } catch (RuntimeException | LinkageError failure) {
                    // Treat a failed read like an unavailable chunk so the rollback record
                    // remains pending, but expose the failure separately in telemetry.
                    readFailures.incrementAndGet();
                    return Optional.empty();
                }
            });
        int restored = 0;
        int changed = 0;
        int unavailable = 0;
        int failures = readFailures.get();

        for (TemporaryMutationTracker.ExpiryAction action : actions) {
            switch (action.kind()) {
                case DROP_CHANGED -> changed++;
                case UNAVAILABLE -> unavailable++;
                case RESTORE -> {
                    TemporaryWorldMutation mutation = action.mutation();
                    try {
                        boolean applied = backend.replaceIfCurrent(
                            mutation.key(),
                            mutation.replacementState(),
                            mutation.originalState());
                        if (applied && tracker.confirmRestored(mutation.key(), mutation.originalState())) {
                            restored++;
                        } else {
                            failures++;
                        }
                    } catch (RuntimeException | LinkageError failure) {
                        // Keep the record pending; retry later rather than orphaning a temporary mutation.
                        failures++;
                    }
                }
            }
        }
        return new TickResult(restored, changed, unavailable, failures);
    }

    public record TickResult(int restored, int changedByOthers, int unavailable, int failures) {
        public TickResult {
            if (restored < 0 || changedByOthers < 0 || unavailable < 0 || failures < 0) {
                throw new IllegalArgumentException("restoration counters cannot be negative");
            }
        }
    }
}
