package dev.gustavopere.blackarcana.content.blood;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;

class EquilibriumTransferPlannerTest {
    @Test
    void transferIsBoundedBySourceFloorAndTargetCapacityWithoutCreatingHealth() {
        var plan = EquilibriumTransferPlanner.plan(30.0D, 40.0D, 5.0D, 20.0D, 20.0D, 4.0D);
        assertEquals(15.0D, plan.transferred(), 1.0E-9);
        assertEquals(15.0D, plan.sourceAfter(), 1.0E-9);
        assertEquals(20.0D, plan.targetAfter(), 1.0E-9);
        assertEquals(35.0D, plan.sourceAfter() + plan.targetAfter(), 1.0E-9);
    }

    @Test
    void deadEndpointCannotBeResurrectedByTransfer() {
        var plan = EquilibriumTransferPlanner.plan(20.0D, 20.0D, 0.0D, 20.0D, 10.0D, 1.0D);
        assertFalse(plan.applicable());
        assertEquals(0.0D, plan.transferred());
    }

    @Test
    void hardTransferCeilingCannotBeRaised() {
        assertThrows(IllegalArgumentException.class,
            () -> EquilibriumTransferPlanner.plan(100.0D, 100.0D, 1.0D, 100.0D, 41.0D, 1.0D));
    }
}
