package dev.gustavopere.blackarcana.content.blood;

import org.junit.jupiter.api.Test;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

class SanguineHarvestPlannerTest {
    @Test
    void targetAndYieldBudgetsBoundFarmProcessing() {
        List<SanguineHarvestPlanner.Candidate> candidates = new ArrayList<>();
        for (int i = 0; i < 100; i++) {
            candidates.add(new SanguineHarvestPlanner.Candidate(UUID.randomUUID(), 5.0D, i == 0 ? 0.20D : 1.0D, true));
        }
        var plan = SanguineHarvestPlanner.plan(candidates, 24, 20.0D);
        assertEquals(5, plan.drains().size());
        assertEquals(20.0D, plan.totalYield(), 1.0E-9);
        assertEquals(1.0D, plan.drains().getFirst().amount(), 1.0E-9, "anti-farm weight must reduce the first target yield");
    }

    @Test
    void hardTargetCeilingCannotBeRaisedByCaller() {
        assertThrows(IllegalArgumentException.class, () -> SanguineHarvestPlanner.plan(List.of(), 65, 10.0D));
    }
}
