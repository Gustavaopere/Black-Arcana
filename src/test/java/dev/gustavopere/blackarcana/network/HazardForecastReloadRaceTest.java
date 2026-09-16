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
    void lateForecastFromOutstandingPreviousRevisionRequestCannotReappearAfterReload() {
        HazardPreflightPayload preflight = preflight();
        ClientArcanaSyncState.replaceHazardPreflight(preflight);

        long acceptedRequestId = nextForecastRequestId();
        replaceForecast(forecast(acceptedRequestId));
        assertEquals(acceptedRequestId,
            ClientArcanaSyncState.hazardResistanceForecast(SPELL).orElseThrow().requestId());

        // Allocate another request while the old revision is still current, but deliberately leave
        // its response outstanding so the reload happens while this request is genuinely in flight.
        long staleOutstandingRequestId = nextForecastRequestId();
        assertTrue(staleOutstandingRequestId > acceptedRequestId);

        // A datapack/provider reload is a revision boundary even when the resulting static
        // tier and resistance thresholds happen to be byte-for-byte identical.
        ClientArcanaSyncState.replaceHazardPreflight(preflight);
        assertTrue(ClientArcanaSyncState.hazardResistanceForecast(SPELL).isEmpty());

        // The first response for the higher-ID request was issued under the previous revision and
        // arrives only now. It must not repopulate state after the reload boundary.
        replaceForecast(forecast(staleOutstandingRequestId));
        assertTrue(ClientArcanaSyncState.hazardResistanceForecast(SPELL).isEmpty(),
            "an outstanding request allocated before the current preflight revision must stay invalid after reload");

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
