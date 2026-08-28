package dev.gustavopere.blackarcana.content.space;

import org.junit.jupiter.api.Test;

import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ThroughputWindowTest {
    @Test
    void limiterResetsOnlyOnNextServerSecondWindow() {
        ThroughputWindow limiter = new ThroughputWindow(2);
        UUID owner = UUID.randomUUID();
        assertTrue(limiter.tryAcquire(owner, 0L));
        assertTrue(limiter.tryAcquire(owner, 19L));
        assertFalse(limiter.tryAcquire(owner, 19L));
        assertTrue(limiter.tryAcquire(owner, 20L));
    }
}
