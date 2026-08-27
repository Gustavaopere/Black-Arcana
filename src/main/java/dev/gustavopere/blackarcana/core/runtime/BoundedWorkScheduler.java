package dev.gustavopere.blackarcana.core.runtime;

import java.util.ArrayDeque;
import java.util.Objects;
import java.util.Queue;

public final class BoundedWorkScheduler {
    private final int maxQueuedItems;
    private final int budgetPerTick;
    private final Queue<WorkItem> queue = new ArrayDeque<>();

    public BoundedWorkScheduler(int maxQueuedItems, int budgetPerTick) {
        if (maxQueuedItems <= 0) throw new IllegalArgumentException("maxQueuedItems must be positive");
        if (budgetPerTick <= 0) throw new IllegalArgumentException("budgetPerTick must be positive");
        this.maxQueuedItems = maxQueuedItems;
        this.budgetPerTick = budgetPerTick;
    }

    public synchronized boolean enqueue(WorkItem item) {
        Objects.requireNonNull(item, "item");
        if (queue.size() >= maxQueuedItems) return false;
        queue.add(item);
        return true;
    }

    public synchronized TickResult tick() {
        int remainingBudget = budgetPerTick;
        int completed = 0;
        int initialItems = queue.size();

        for (int processed = 0; processed < initialItems && remainingBudget > 0; processed++) {
            WorkItem item = queue.remove();
            StepResult result = Objects.requireNonNull(item.step(remainingBudget), "step result");
            if (result.consumedUnits() < 0 || result.consumedUnits() > remainingBudget) {
                throw new IllegalStateException("work item consumed outside granted budget");
            }

            remainingBudget -= result.consumedUnits();
            if (result.complete()) completed++;
            else queue.add(item);
        }

        return new TickResult(budgetPerTick - remainingBudget, completed, queue.size());
    }

    public synchronized int queuedItems() {
        return queue.size();
    }

    @FunctionalInterface
    public interface WorkItem {
        StepResult step(int grantedBudget);
    }

    public record StepResult(int consumedUnits, boolean complete) {
        public StepResult {
            if (consumedUnits < 0) throw new IllegalArgumentException("consumedUnits cannot be negative");
        }

        public static StepResult complete(int consumedUnits) {
            return new StepResult(consumedUnits, true);
        }

        public static StepResult pending(int consumedUnits) {
            return new StepResult(consumedUnits, false);
        }
    }

    public record TickResult(int consumedUnits, int completedItems, int queuedItems) { }
}
