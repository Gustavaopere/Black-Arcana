package dev.gustavopere.blackarcana.core.runtime;

import dev.gustavopere.blackarcana.api.ArcanaCastContext;
import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaCost;
import dev.gustavopere.blackarcana.api.ArcanaServices;
import dev.gustavopere.blackarcana.api.ArcanaSpellDefinition;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import org.junit.jupiter.api.Test;

import java.util.UUID;
import java.util.concurrent.atomic.AtomicInteger;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ScheduledArcanaEffectTest {
    private static final ArcanaSpellDefinition SPELL = new ArcanaSpellDefinition(
            ArcanaSpellId.parse("black_arcana:scheduled_probe"),
            "spell.black_arcana.scheduled_probe",
            "black_arcana:scheduled_probe",
            new ArcanaCost("black_arcana:test", 1.0),
            false);

    @Test
    void acceptedWorkRunsOnlyWhenSchedulerReceivesTickBudget() {
        BoundedWorkScheduler scheduler = new BoundedWorkScheduler(2, 1);
        AtomicInteger work = new AtomicInteger();
        ScheduledArcanaEffect effect = new ScheduledArcanaEffect(
                scheduler,
                (request, target) -> ScheduledArcanaEffect.PlannedWork.of(granted -> {
                    work.incrementAndGet();
                    return BoundedWorkScheduler.StepResult.complete(1);
                }));

        var result = effect.apply(request(), ArcanaServices.TargetResolution.resolved("synthetic:self"));
        assertTrue(result.success());
        assertEquals(0, work.get());
        assertEquals(1, scheduler.queuedItems());

        scheduler.tick();
        assertEquals(1, work.get());
        assertEquals(0, scheduler.queuedItems());
    }

    @Test
    void saturatedSchedulerFailsBeforeWorkAdmission() {
        BoundedWorkScheduler scheduler = new BoundedWorkScheduler(1, 1);
        scheduler.enqueue(granted -> BoundedWorkScheduler.StepResult.pending(0));
        ScheduledArcanaEffect effect = new ScheduledArcanaEffect(
                scheduler,
                (request, target) -> ScheduledArcanaEffect.PlannedWork.of(
                        granted -> BoundedWorkScheduler.StepResult.complete(1)));

        var result = effect.apply(request(), ArcanaServices.TargetResolution.resolved("synthetic:self"));
        assertFalse(result.success());
        assertEquals("effect scheduler queue is saturated", result.detail());
        assertEquals(1, scheduler.queuedItems());
    }

    private static ArcanaCastRequest request() {
        return new ArcanaCastRequest(
                SPELL,
                new ArcanaCastContext(
                        UUID.fromString("28c0ad10-9dfa-41c6-a32c-303f0ef31815"),
                        100L,
                        "minecraft:overworld"));
    }
}
