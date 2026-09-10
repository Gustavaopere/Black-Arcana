package dev.gustavopere.blackarcana.client;

import java.util.Objects;

/** Pure client-presentation arbitration for independent transient HUD channels. */
final class ContextualFeedbackOrchestration {
    private ContextualFeedbackOrchestration() {
    }

    static Decision decide(
            BlackArcanaClientConfig.FeedbackLevel level,
            boolean selectionRecent,
            boolean resultRecent,
            CastingUxSemantics.AdmissionState resultState
    ) {
        Objects.requireNonNull(level, "level");
        boolean showSelectionContext = selectionRecent
                && level != BlackArcanaClientConfig.FeedbackLevel.MINIMAL;

        if (!resultRecent) {
            return new Decision(showSelectionContext, false);
        }

        Objects.requireNonNull(resultState, "resultState");
        boolean showAuthoritativeResult = switch (resultState) {
            case CAST_DENIED, CAST_FAILED -> true;
            case CAST_SUCCEEDED -> level == BlackArcanaClientConfig.FeedbackLevel.VERBOSE;
            case FORECAST_CLEAR, FORECAST_BLOCKED, FORECAST_UNAVAILABLE ->
                    throw new IllegalArgumentException("forecast state is not an authoritative cast result");
        };
        return new Decision(showSelectionContext, showAuthoritativeResult);
    }

    record Decision(boolean showSelectionContext, boolean showAuthoritativeResult) {
    }
}
