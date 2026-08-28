package dev.gustavopere.blackarcana.core.runtime;

import org.junit.jupiter.api.Test;

import java.util.concurrent.atomic.AtomicInteger;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

class BoundedWorkSchedulerTest {
    @Test
    void workNeverExceedsPerTickBudget() {
        BoundedWorkScheduler scheduler = new BoundedWorkScheduler(8, 5);
        AtomicInteger remaining = new AtomicInteger(8);
        assertTrue(scheduler.enqueue(granted -> {
            int consumed = Math.min(granted, remaining.get());
            int left = remaining.addAndGet(-consumed);
            return left == 0
                    ? BoundedWorkScheduler.StepResult.complete(consumed)
                    : BoundedWorkScheduler.StepResult.pending(consumed);
        }));

        var first = scheduler.tick();
        assertEquals(5, first.consumedUnits());
        assertEquals(1, first.queuedItems());

        var second = scheduler.tick();
        assertEquals(3, second.consumedUnits());
        assertEquals(1, second.completedItems());
        assertEquals(0, second.queuedItems());
    }

    @Test
    void eachPendingItemRunsAtMostOncePerTick() {
        BoundedWorkScheduler scheduler = new BoundedWorkScheduler(4, 10);
        AtomicInteger calls = new AtomicInteger();
        scheduler.enqueue(granted -> {
            calls.incrementAndGet();
            return BoundedWorkScheduler.StepResult.pending(0);
        });

        scheduler.tick();
        assertEquals(1, calls.get());
        scheduler.tick();
        assertEquals(2, calls.get());
    }

    @Test
    void queueCapacityFailsClosed() {
        BoundedWorkScheduler scheduler = new BoundedWorkScheduler(1, 1);
        assertTrue(scheduler.enqueue(granted -> BoundedWorkScheduler.StepResult.pending(0)));
        assertFalse(scheduler.enqueue(granted -> BoundedWorkScheduler.StepResult.complete(0)));
    }

    @Test
    void itemCannotClaimMoreThanGrantedBudget() {
        BoundedWorkScheduler scheduler = new BoundedWorkScheduler(1, 2);
        scheduler.enqueue(granted -> BoundedWorkScheduler.StepResult.complete(granted + 1));
        assertThrows(IllegalStateException.class, scheduler::tick);
    }

    @Test
    void configuredFailureHandlerCanDropOneBadItemWithoutBlockingOthers() {
        AtomicInteger failures = new AtomicInteger();
        AtomicInteger healthyCalls = new AtomicInteger();
        BoundedWorkScheduler scheduler = new BoundedWorkScheduler(4, 4, failure -> failures.incrementAndGet());
        scheduler.enqueue(granted -> { throw new IllegalStateException("boom"); });
        scheduler.enqueue(granted -> {
            healthyCalls.incrementAndGet();
            return BoundedWorkScheduler.StepResult.complete(1);
        });

        var result = scheduler.tick();
        assertEquals(1, failures.get());
        assertEquals(1, result.failedItems());
        assertEquals(1, healthyCalls.get());
        assertEquals(0, result.queuedItems());
    }
}
