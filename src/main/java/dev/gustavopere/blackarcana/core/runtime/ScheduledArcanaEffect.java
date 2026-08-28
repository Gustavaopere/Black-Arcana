package dev.gustavopere.blackarcana.core.runtime;

import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaServices;

import java.util.Objects;

/**
 * Adapter for effects whose work must be spread across server ticks.
 *
 * Planning is synchronous and must not mutate the world. Once the work item is
 * accepted by the bounded scheduler the cast is considered successfully
 * started, allowing the normal engine to commit its reserved cost and cooldown.
 * A saturated queue fails before commit, so the engine refunds the reservation.
 */
public final class ScheduledArcanaEffect implements ArcanaServices.ArcanaEffect {
    @FunctionalInterface
    public interface Planner {
        PlannedWork plan(ArcanaCastRequest request, ArcanaServices.TargetResolution target);
    }

    private final BoundedWorkScheduler scheduler;
    private final Planner planner;

    public ScheduledArcanaEffect(BoundedWorkScheduler scheduler, Planner planner) {
        this.scheduler = Objects.requireNonNull(scheduler, "scheduler");
        this.planner = Objects.requireNonNull(planner, "planner");
    }

    @Override
    public ArcanaServices.EffectResult apply(
            ArcanaCastRequest request,
            ArcanaServices.TargetResolution target
    ) {
        PlannedWork planned = Objects.requireNonNull(planner.plan(request, target), "planned work");
        if (!scheduler.enqueue(planned.item())) {
            return ArcanaServices.EffectResult.failed("effect scheduler queue is saturated");
        }
        return new ArcanaServices.EffectResult(true, planned.acceptedDetail());
    }

    public record PlannedWork(BoundedWorkScheduler.WorkItem item, String acceptedDetail) {
        public PlannedWork {
            Objects.requireNonNull(item, "item");
            Objects.requireNonNull(acceptedDetail, "acceptedDetail");
        }

        public static PlannedWork of(BoundedWorkScheduler.WorkItem item) {
            return new PlannedWork(item, "scheduled");
        }
    }
}
