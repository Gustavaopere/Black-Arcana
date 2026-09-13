package dev.gustavopere.blackarcana.client;

import java.util.Objects;
import java.util.Optional;

/** Pure bounded transient state for the generic Stage 05.15 client cue layer. */
final class CastPresentationPulseState {
    private final long anticipationDurationTicks;
    private final long resultDurationTicks;
    private Pulse active;

    CastPresentationPulseState(long anticipationDurationTicks, long resultDurationTicks) {
        if (anticipationDurationTicks <= 0L) {
            throw new IllegalArgumentException("anticipationDurationTicks must be positive");
        }
        if (resultDurationTicks <= 0L) {
            throw new IllegalArgumentException("resultDurationTicks must be positive");
        }
        this.anticipationDurationTicks = anticipationDurationTicks;
        this.resultDurationTicks = resultDurationTicks;
    }

    void accept(CastAudiovisualOrchestration.Directive directive, long tick) {
        Objects.requireNonNull(directive, "directive");
        current(tick);

        long duration = directive.kind() == CastAudiovisualOrchestration.Kind.ANTICIPATION
                ? anticipationDurationTicks
                : resultDurationTicks;
        Pulse next = new Pulse(
                directive.kind(),
                directive.authority(),
                tick,
                tick + duration,
                directive.optionalMotionAllowed(),
                directive.flashHeavyEffectsAllowed());

        if (active != null && priority(next.kind()) < priority(active.kind())) {
            return;
        }
        active = next;
    }

    Optional<Pulse> current(long tick) {
        if (active == null) return Optional.empty();
        if (tick >= active.expiresAtTick()) {
            active = null;
            return Optional.empty();
        }
        return Optional.of(active);
    }

    int activeCount() {
        return active == null ? 0 : 1;
    }

    void clear() {
        active = null;
    }

    private static int priority(CastAudiovisualOrchestration.Kind kind) {
        return switch (kind) {
            case ANTICIPATION -> 1;
            case RESULT_SUCCESS -> 2;
            case RESULT_DENIED, RESULT_FAILED -> 3;
        };
    }

    record Pulse(
            CastAudiovisualOrchestration.Kind kind,
            CastPresentationLifecycle.Authority authority,
            long startedTick,
            long expiresAtTick,
            boolean optionalMotionAllowed,
            boolean flashHeavyEffectsAllowed
    ) {
        Pulse {
            Objects.requireNonNull(kind, "kind");
            Objects.requireNonNull(authority, "authority");
            if (expiresAtTick <= startedTick) {
                throw new IllegalArgumentException("pulse expiry must follow its start tick");
            }
        }

        boolean authoritativeOutcome() {
            return authority == CastPresentationLifecycle.Authority.AUTHORITATIVE_CAST_RESULT
                    || authority == CastPresentationLifecycle.Authority.SERVER_OWNED_RUNTIME_EVENT;
        }

        boolean visualShapeRequired() {
            return authoritativeOutcome() && kind != CastAudiovisualOrchestration.Kind.ANTICIPATION;
        }
    }
}
