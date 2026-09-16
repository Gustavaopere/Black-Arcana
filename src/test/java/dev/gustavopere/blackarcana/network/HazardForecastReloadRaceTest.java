package dev.gustavopere.blackarcana.network;

import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.api.hazard.ArcaneDangerTier;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.Test;

import java.lang.reflect.Method;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assertions.fail;

class HazardForecastReloadRaceTest {
    private static final String SPELL_ID = "black_arcana:reload_race_spell";
    private static final ArcanaSpellId SPELL = ArcanaSpellId.parse(SPELL_ID);

    @AfterEach
    void clearClientState() {
        ClientArcanaSyncState.clear();
    }

    @Test
    void lateForecastFromPreviousPreflightRevisionCannotReappearAfterReload() {
        HazardPreflightPayload preflight = preflight();
        ClientArcanaSyncState.replaceHazardPreflight(preflight);

        long staleRequestId = nextForecastRequestId();
        replaceForecast(forecast(staleRequestId));
        assertEquals(staleRequestId,
            ClientArcanaSyncState.hazardResistanceForecast(SPELL).orElseThrow().requestId());

        // A datapack/provider reload is a revision boundary even when the resulting static
        // tier and resistance thresholds happen to be byte-for-byte identical.
        ClientArcanaSyncState.replaceHazardPreflight(preflight);
        assertTrue(ClientArcanaSyncState.hazardResistanceForecast(SPELL).isEmpty());

        // This response was already in flight before the reload and must stay invalidated.
        replaceForecast(forecast(staleRequestId));
        assertTrue(ClientArcanaSyncState.hazardResistanceForecast(SPELL).isEmpty(),
            "a forecast issued before the current preflight revision must not reappear after reload");

        long currentRequestId = nextForecastRequestId();
        replaceForecast(forecast(currentRequestId));
        assertEquals(currentRequestId,
            ClientArcanaSyncState.hazardResistanceForecast(SPELL).orElseThrow().requestId());
    }

    private static HazardPreflightPayload preflight() {
        return new HazardPreflightPayload(
            ArcanaProtocol.VERSION,
            List.of(new HazardPreflightPayload.Entry(
                SPELL_ID,
                ArcaneDangerTier.DANGEROUS.name(),
                12.0D,
                24.0D)));
    }

    private static HazardResistanceForecastPayload forecast(long requestId) {
        return new HazardResistanceForecastPayload(
            ArcanaProtocol.VERSION,
            requestId,
            SPELL_ID,
            true,
            HazardResistanceForecastPayload.Status.BELOW_RECOMMENDED.name(),
            ArcaneDangerTier.DANGEROUS.name(),
            16.0D,
            12.0D,
            24.0D,
            true,
            HazardResistanceForecastPayload.GateStatus.CLEAR.name());
    }

    private static long nextForecastRequestId() {
        try {
            Method method = ClientArcanaSyncState.class.getDeclaredMethod(
                "nextHazardResistanceForecastRequestId");
            method.setAccessible(true);
            return (long) method.invoke(null);
        } catch (ReflectiveOperationException exception) {
            return fail("Client forecast request IDs must be allocated by revision-aware sync state", exception);
        }
    }

    private static void replaceForecast(HazardResistanceForecastPayload payload) {
        try {
            Method method = ClientArcanaSyncState.class.getDeclaredMethod(
                "replaceHazardResistanceForecast",
                HazardResistanceForecastPayload.class);
            method.setAccessible(true);
            method.invoke(null, payload);
        } catch (ReflectiveOperationException exception) {
            fail("Client forecast acceptance needs a testable revision-aware state seam", exception);
        }
    }
}
