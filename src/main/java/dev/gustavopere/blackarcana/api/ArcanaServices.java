package dev.gustavopere.blackarcana.api;

import java.util.Objects;

public final class ArcanaServices {
    private ArcanaServices() {
    }

    @FunctionalInterface
    public interface ProgressionGate {
        ArcanaDecision check(ArcanaCastRequest request);
    }

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

        default boolean reserved() {
            return decision().allowed();
        }

        void commit();
        void refund();
    }

    @FunctionalInterface
    public interface TargetSelector {
        TargetResolution resolve(ArcanaCastRequest request);
    }

    @FunctionalInterface
    public interface WorldEffectPolicy {
        ArcanaDecision authorize(ArcanaCastRequest request, TargetResolution target);
    }

    @FunctionalInterface
    public interface ArcanaEffect {
        EffectResult apply(ArcanaCastRequest request, TargetResolution target);
    }

    public record TargetResolution(boolean resolved, String targetId, String detail) {
        public TargetResolution {
            Objects.requireNonNull(targetId, "targetId");
            Objects.requireNonNull(detail, "detail");
        }

        public static TargetResolution resolved(String targetId) {
            return new TargetResolution(true, targetId, "");
        }

        public static TargetResolution denied(String detail) {
            return new TargetResolution(false, "", detail);
        }
    }

    public record EffectResult(boolean success, String detail) {
        public EffectResult {
            Objects.requireNonNull(detail, "detail");
        }

        public static EffectResult ok() {
            return new EffectResult(true, "");
        }

        public static EffectResult failed(String detail) {
            return new EffectResult(false, detail);
        }
    }
}
