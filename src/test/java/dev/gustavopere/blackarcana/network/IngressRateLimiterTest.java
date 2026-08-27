package dev.gustavopere.blackarcana.network;

import org.junit.jupiter.api.Test;

import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class IngressRateLimiterTest {
    private static final UUID CASTER = UUID.fromString("28c0ad10-9dfa-41c6-a32c-303f0ef31815");

    @Test
    void limiterRejectsExcessRequestsUntilWindowExpires() {
        IngressRateLimiter limiter = new IngressRateLimiter(2, 20, 8);
        assertTrue(limiter.claim(CASTER, 100).allowed());
        assertTrue(limiter.claim(CASTER, 101).allowed());
        var denied = limiter.claim(CASTER, 102);
        assertFalse(denied.allowed());
        assertEquals("rate_limited", denied.code());
        assertTrue(limiter.claim(CASTER, 120).allowed());
    }

    @Test
    void casterBucketsAreBoundedAndExpiredBucketsArePruned() {
        IngressRateLimiter limiter = new IngressRateLimiter(1, 10, 1);
        assertTrue(limiter.claim(CASTER, 1).allowed());
        UUID other = UUID.fromString("33333333-3333-3333-3333-333333333333");
        assertEquals("ingress_limiter_saturated", limiter.claim(other, 2).code());
        assertTrue(limiter.claim(other, 11).allowed());
        assertEquals(1, limiter.trackedCasters());
    }
}
