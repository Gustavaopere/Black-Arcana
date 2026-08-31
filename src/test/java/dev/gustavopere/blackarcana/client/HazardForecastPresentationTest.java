package dev.gustavopere.blackarcana.client;

import dev.gustavopere.blackarcana.api.hazard.ArcaneDangerTier;
import dev.gustavopere.blackarcana.network.ArcanaProtocol;
import dev.gustavopere.blackarcana.network.HazardPreflightPayload;
import dev.gustavopere.blackarcana.network.HazardResistanceForecastPayload;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class HazardForecastPresentationTest {
    @Test
    void forecastIsUsedOnlyWhenItMatchesCurrentStaticDangerRevision() {
        HazardPreflightPayload.Entry current = new HazardPreflightPayload.Entry(
            "black_arcana:test",
            ArcaneDangerTier.DANGEROUS.name(),
            12.0D,
            24.0D);
        HazardResistanceForecastPayload matching = forecast(
            ArcaneDangerTier.DANGEROUS, 12.0D, 24.0D, true);
        HazardResistanceForecastPayload staleTier = forecast(
            ArcaneDangerTier.UNSTABLE, 12.0D, 24.0D, true);
        HazardResistanceForecastPayload staleThreshold = forecast(
            ArcaneDangerTier.DANGEROUS, 10.0D, 20.0D, true);
        HazardResistanceForecastPayload rateLimitedNormal = forecast(
            ArcaneDangerTier.NORMAL, 0.0D, 0.0D, false);

        assertTrue(BlackArcanaHudLayer.forecastMatchesPreflight(current, matching));
        assertFalse(BlackArcanaHudLayer.forecastMatchesPreflight(current, staleTier));
        assertFalse(BlackArcanaHudLayer.forecastMatchesPreflight(current, staleThreshold));
        assertFalse(BlackArcanaHudLayer.forecastMatchesPreflight(current, rateLimitedNormal));
    }

    private static HazardResistanceForecastPayload forecast(
        ArcaneDangerTier tier,
        double minimum,
        double recommended,
        boolean available
    ) {
        return new HazardResistanceForecastPayload(
            ArcanaProtocol.VERSION,
            1L,
            "black_arcana:test",
            available,
            (available
                ? HazardResistanceForecastPayload.Status.RECOMMENDED
                : HazardResistanceForecastPayload.Status.UNAVAILABLE).name(),
            tier.name(),
            available ? recommended : 0.0D,
            minimum,
            recommended);
    }
}
