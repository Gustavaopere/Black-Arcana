package dev.gustavopere.blackarcana.core.hazard;

import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.api.hazard.ArcanaDamageInstanceId;
import dev.gustavopere.blackarcana.api.hazard.ArcaneDangerTier;
import dev.gustavopere.blackarcana.api.hazard.ArcaneHazardSettledEvent;
import org.junit.jupiter.api.Test;

import java.util.UUID;
import java.util.concurrent.atomic.AtomicInteger;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

class ArcaneHazardObserverRegistryTest {
    @Test
    void publishesDeterministicallyAndIsolatesObserverFailures() {
        ArcaneHazardObserverRegistry registry = new ArcaneHazardObserverRegistry();
        AtomicInteger delivered = new AtomicInteger();
        registry.register("black_arcana:a", event -> delivered.incrementAndGet());
        registry.register("black_arcana:b", event -> { throw new IllegalStateException("synthetic failure"); });
        registry.register("black_arcana:c", event -> delivered.incrementAndGet());

        var result = registry.publish(event());

        assertEquals(2, delivered.get());
        assertEquals(2, result.delivered());
        assertEquals(java.util.List.of("black_arcana:b"), result.failedObserverIds());
    }

    @Test
    void duplicateObserverIdsAreRejected() {
        ArcaneHazardObserverRegistry registry = new ArcaneHazardObserverRegistry();
        registry.register("black_arcana:test", event -> {});
        assertThrows(IllegalArgumentException.class,
            () -> registry.register("black_arcana:test", event -> {}));
    }

    private static ArcaneHazardSettledEvent event() {
        return new ArcaneHazardSettledEvent(
            ArcanaCastId.random(),
            ArcanaDamageInstanceId.random(),
            ArcanaSpellId.parse("black_arcana:test"),
            UUID.randomUUID(),
            ArcaneDangerTier.DANGEROUS,
            8.0D, 8.0D, 4.0D, 1.0D, 2.0D);
    }
}
