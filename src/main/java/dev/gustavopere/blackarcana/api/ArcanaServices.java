package dev.gustavopere.blackarcana.api;

import java.util.List;
import java.util.Objects;

public final class ArcanaServices {
    private ArcanaServices() {}

    @FunctionalInterface
    public interface CastRequestValidator { ArcanaDecision check(ArcanaCastRequest request); }

    @FunctionalInterface
    public interface ReplayGuard { ArcanaDecision claim(ArcanaCastRequest request); }

    @FunctionalInterface
    public interface ProgressionGate { ArcanaDecision check(ArcanaCastRequest request); }

    public interface CooldownService {
        ArcanaDecision check(ArcanaCastRequest request);
        void start(ArcanaCastRequest request);
    }

    public interface CostProvider {
        ArcanaDecision check(ArcanaCastRequest request);
        CostReservation reserve(ArcanaCastRequest request);
    }

    public interface CostReservation {
        ArcanaDecision decision();
        default boolean reserved() { return decision().allowed(); }
        void commit();
        void refund();
    }

    @FunctionalInterface
    public interface TargetSelector { TargetResolution resolve(ArcanaCastRequest request); }

    @FunctionalInterface
    public interface WorldEffectPolicy { ArcanaDecision authorize(ArcanaCastRequest request, TargetResolution target); }

    @FunctionalInterface
    public interface ArcanaEffect { EffectResult apply(ArcanaCastRequest request, TargetResolution target); }

    /**
     * Side-effect hook invoked only after the effect succeeded, the resource
     * transaction committed and cooldown state started. Observer failures must
     * never retroactively invalidate an already committed cast.
     */
    @FunctionalInterface
    public interface CastSuccessObserver {
        void onSuccess(ArcanaCastRequest request, TargetResolution target, EffectResult effectResult);

        static CastSuccessObserver noop() {
            return (request, target, effectResult) -> { };
        }
    }

    /**
     * Bounded target set resolved entirely on the server. Single-target callers
     * may continue using {@link #targetId()} as a primary-target convenience.
     */
    public record TargetResolution(boolean resolved, List<String> targetIds, String detail) {
        public TargetResolution {
            Objects.requireNonNull(targetIds, "targetIds");
            Objects.requireNonNull(detail, "detail");
            targetIds = List.copyOf(targetIds);
            if (targetIds.size() > ArcanaTargetSpec.ABSOLUTE_MAX_TARGETS) {
                throw new IllegalArgumentException("target resolution exceeds absolute target cap");
            }
            if (resolved && targetIds.isEmpty()) {
                throw new IllegalArgumentException("resolved target set cannot be empty");
            }
            if (!resolved && !targetIds.isEmpty()) {
                throw new IllegalArgumentException("denied target set must be empty");
            }
            for (String targetId : targetIds) {
                if (targetId == null || targetId.isBlank()) {
                    throw new IllegalArgumentException("target ids cannot be null/blank");
                }
            }
        }

        public String targetId() {
            return targetIds.isEmpty() ? "" : targetIds.getFirst();
        }

        public static TargetResolution resolved(String targetId) {
            return new TargetResolution(true, List.of(Objects.requireNonNull(targetId, "targetId")), "");
        }

        public static TargetResolution resolved(List<String> targetIds) {
            return new TargetResolution(true, targetIds, "");
        }

        public static TargetResolution denied(String detail) {
            return new TargetResolution(false, List.of(), detail);
        }
    }

    public record EffectResult(boolean success, String detail) {
        public EffectResult { Objects.requireNonNull(detail, "detail"); }
        public static EffectResult ok() { return new EffectResult(true, ""); }
        public static EffectResult failed(String detail) { return new EffectResult(false, detail); }
    }
}
