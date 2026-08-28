package dev.gustavopere.blackarcana.core.progression;

import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class TechniqueBudgetProfileTest {
    private static final BalanceBenchmark BENCHMARK = new BalanceBenchmark("Black Arcana pack benchmark", "2026-08", "placeholder methodology reference until measured pack values are frozen");

    @Test void compensatedTechniqueCanFitTierBudget() {
        var profile = new TechniqueBudgetProfile(ArcanaSpellId.parse("black_arcana:test"), TechniqueTier.T2,
            6, 4, 4, 2, 2, 4, 3, 5, 4, 5, 6, BENCHMARK);
        assertTrue(profile.assess().withinBudget());
        assertEquals(0D, profile.assess().overshoot());
    }

    @Test void outlierIsExplicitInsteadOfSilentlyAccepted() {
        var profile = new TechniqueBudgetProfile(ArcanaSpellId.parse("black_arcana:outlier"), TechniqueTier.T1,
            10, 10, 10, 10, 10, 10, 10, 0, 0, 0, 0, BENCHMARK);
        assertFalse(profile.assess().withinBudget());
        assertTrue(profile.assess().overshoot() > 0D);
    }
}
