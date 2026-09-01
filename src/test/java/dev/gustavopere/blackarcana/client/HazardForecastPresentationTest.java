package dev.gustavopere.blackarcana.client;

import dev.gustavopere.blackarcana.api.hazard.ArcaneDangerTier;
import dev.gustavopere.blackarcana.network.ArcanaProtocol;
import dev.gustavopere.blackarcana.network.HazardPreflightPayload;
import dev.gustavopere.blackarcana.network.HazardResistanceForecastPayload;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
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

    @Test
    void gateForecastUsesOnlyBoundedCategoricalTranslationKeys() {
        assertEquals(
            "hazard.black_arcana.gate.clear",
            BlackArcanaHudLayer.gateStatusTranslationKey(HazardResistanceForecastPayload.GateStatus.CLEAR));
        assertEquals(
            "hazard.black_arcana.gate.identity",
            BlackArcanaHudLayer.gateStatusTranslationKey(HazardResistanceForecastPayload.GateStatus.IDENTITY));
        assertEquals(
            "hazard.black_arcana.gate.progression",
            BlackArcanaHudLayer.gateStatusTranslationKey(HazardResistanceForecastPayload.GateStatus.PROGRESSION));
        assertEquals(
            "hazard.black_arcana.gate.cooldown",
            BlackArcanaHudLayer.gateStatusTranslationKey(HazardResistanceForecastPayload.GateStatus.COOLDOWN));
        assertEquals(
            "hazard.black_arcana.gate.cost",
            BlackArcanaHudLayer.gateStatusTranslationKey(HazardResistanceForecastPayload.GateStatus.COST));
        assertEquals(
            "hazard.black_arcana.gate.unavailable",
            BlackArcanaHudLayer.gateStatusTranslationKey(HazardResistanceForecastPayload.GateStatus.UNAVAILABLE));
    }

    @Test
    void loadoutHazardTooltipUsesStaticServerAuthoredPreflight() {
        HazardPreflightPayload.Entry dangerous = new HazardPreflightPayload.Entry(
            "black_arcana:test",
            ArcaneDangerTier.FORBIDDEN.name(),
            20.0D,
            35.0D);

        assertEquals(
            BlackArcanaHudLayer.preflightLine(dangerous),
            BlackArcanaLoadoutScreen.hazardTooltip(dangerous).orElseThrow());
        assertTrue(BlackArcanaLoadoutScreen.hazardTooltip(null).isEmpty());
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
