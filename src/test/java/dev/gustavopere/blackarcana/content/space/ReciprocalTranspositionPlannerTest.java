package dev.gustavopere.blackarcana.content.space;

import org.junit.jupiter.api.Test;

import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ReciprocalTranspositionPlannerTest {
    @Test
    void validEndpointsProduceVersionedAtomicPlanAndConsentFailureDenies() {
        var planner = new ReciprocalTranspositionPlanner(new SafeDestinationPolicy());
        var first = new ReciprocalTranspositionPlanner.Endpoint(UUID.randomUUID(), 5L, true, SafeDestinationPolicyTest.valid());
        var second = new ReciprocalTranspositionPlanner.Endpoint(UUID.randomUUID(), 9L, true, SafeDestinationPolicyTest.valid());
        var plan = planner.plan(first, second);
        assertTrue(plan.allowed());
        assertEquals(5L, plan.firstVersion());
        assertEquals(9L, plan.secondVersion());

        var denied = planner.plan(first,
            new ReciprocalTranspositionPlanner.Endpoint(UUID.randomUUID(), 10L, false, SafeDestinationPolicyTest.valid()));
        assertEquals("consent_denied", denied.code());
    }
}
