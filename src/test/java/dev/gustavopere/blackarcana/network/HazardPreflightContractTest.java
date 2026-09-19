package dev.gustavopere.blackarcana.network;

import dev.gustavopere.blackarcana.api.hazard.ArcaneDangerTier;
import dev.gustavopere.blackarcana.api.hazard.ArcaneInsufficientResistancePolicy;
import dev.gustavopere.blackarcana.network.neoforge.HazardPreflightPacket;
import io.netty.buffer.ByteBuf;
import io.netty.buffer.Unpooled;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

class HazardPreflightContractTest {
    @AfterEach
    void clearClientState() {
        ClientArcanaSyncState.clear();
    }

    @Test
    void hazardPreflightIsBoundedAndServerDescriptiveOnly() {
        HazardPreflightPayload.Entry entry = new HazardPreflightPayload.Entry(
                "black_arcana:dangerous_spell",
                ArcaneDangerTier.DANGEROUS.name(),
                ArcaneInsufficientResistancePolicy.ALLOW_WITH_RISK.name(),
                12.0D,
                24.0D);
        HazardPreflightPayload payload = new HazardPreflightPayload(ArcanaProtocol.VERSION, List.of(entry));

        assertEquals(ArcaneDangerTier.DANGEROUS, entry.parsedTier());
        assertEquals(ArcaneInsufficientResistancePolicy.ALLOW_WITH_RISK, entry.parsedBelowMinimumPolicy());
        assertEquals(24.0D, entry.recommendedArcaneResistance());
        assertEquals(1, payload.entries().size());

        assertThrows(IllegalArgumentException.class, () -> new HazardPreflightPayload.Entry(
                entry.spellId(), entry.dangerTier(), Double.NaN, entry.recommendedArcaneResistance()));
        assertThrows(IllegalArgumentException.class, () -> new HazardPreflightPayload.Entry(
                entry.spellId(), entry.dangerTier(), 30.0D, 20.0D));
        assertThrows(IllegalArgumentException.class, () -> new HazardPreflightPayload.Entry(
                entry.spellId(), "NOT_A_TIER", 0.0D, 0.0D));
        assertThrows(IllegalArgumentException.class, () -> new HazardPreflightPayload.Entry(
                entry.spellId(), entry.dangerTier(), "NOT_A_POLICY", 0.0D, 0.0D));
        assertThrows(IllegalArgumentException.class, () -> new HazardPreflightPayload(
                ArcanaProtocol.VERSION,
                java.util.Collections.nCopies(ArcanaProtocol.MAX_HAZARD_PREFLIGHT_ENTRIES + 1, entry)));
    }

    @Test
    void policyAwarePreflightPacketRoundTrips() {
        HazardPreflightPayload payload = new HazardPreflightPayload(
            ArcanaProtocol.VERSION,
            List.of(new HazardPreflightPayload.Entry(
                "black_arcana:policy_roundtrip",
                ArcaneDangerTier.DANGEROUS.name(),
                ArcaneInsufficientResistancePolicy.ALLOW_WITH_RISK.name(),
                20.0D,
                40.0D)));
        HazardPreflightPacket packet = HazardPreflightPacket.from(payload);
        ByteBuf buffer = Unpooled.buffer();
        try {
            HazardPreflightPacket.STREAM_CODEC.encode(buffer, packet);
            HazardPreflightPacket decoded = HazardPreflightPacket.STREAM_CODEC.decode(buffer);
            assertEquals(packet, decoded);
            assertEquals(
                ArcaneInsufficientResistancePolicy.ALLOW_WITH_RISK,
                decoded.toDomain().entries().getFirst().parsedBelowMinimumPolicy());
        } finally {
            buffer.release();
        }
    }

    @Test
    void hazardPreflightRejectsDuplicateSpellIds() {
        HazardPreflightPayload.Entry first = new HazardPreflightPayload.Entry(
                "black_arcana:test", ArcaneDangerTier.UNSTABLE.name(), 4.0D, 8.0D);
        HazardPreflightPayload.Entry second = new HazardPreflightPayload.Entry(
                "black_arcana:test", ArcaneDangerTier.DANGEROUS.name(), 10.0D, 20.0D);

        assertThrows(IllegalArgumentException.class, () -> new HazardPreflightPayload(
                ArcanaProtocol.VERSION, List.of(first, second)));
    }

    @Test
    void clientHazardStateIsReplacedAndClearedRatherThanAccumulated() {
        HazardPreflightPayload first = new HazardPreflightPayload(
                ArcanaProtocol.VERSION,
                List.of(new HazardPreflightPayload.Entry(
                        "black_arcana:first", ArcaneDangerTier.UNSTABLE.name(), 2.0D, 4.0D)));
        HazardPreflightPayload second = new HazardPreflightPayload(
                ArcanaProtocol.VERSION,
                List.of(new HazardPreflightPayload.Entry(
                        "black_arcana:second", ArcaneDangerTier.FORBIDDEN.name(), 20.0D, 40.0D)));

        ClientArcanaSyncState.replaceHazardPreflight(first);
        assertEquals(1, ClientArcanaSyncState.hazardPreflightSnapshot().size());

        ClientArcanaSyncState.replaceHazardPreflight(second);
        assertEquals(1, ClientArcanaSyncState.hazardPreflightSnapshot().size());
        assertTrue(ClientArcanaSyncState.hazardPreflightSnapshot().keySet().stream()
                .anyMatch(id -> id.canonical().equals("black_arcana:second")));

        ClientArcanaSyncState.clear();
        assertTrue(ClientArcanaSyncState.hazardPreflightSnapshot().isEmpty());
    }

    @Test
    void authoritativeDenialDetailIsPreservedVerbatimByTheClientPayload() {
        CastResultPayload denial = new CastResultPayload(
                ArcanaProtocol.VERSION,
                "11111111-1111-1111-1111-111111111111",
                "DENIED_PROGRESSION",
                "arcane_resistance_required",
                "Requires Arcane Resistance 12.0");

        assertEquals("Requires Arcane Resistance 12.0", denial.detail());
    }
}
