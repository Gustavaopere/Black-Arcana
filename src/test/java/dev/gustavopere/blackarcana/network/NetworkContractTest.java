package dev.gustavopere.blackarcana.network;

import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaCastResult;
import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

class NetworkContractTest {
    @Test
    void incompatibleProtocolIsRejectedImmediately() {
        assertThrows(IllegalArgumentException.class, () -> new CastIntentPayload(
                ArcanaProtocol.VERSION + 1,
                "11111111-1111-1111-1111-111111111111",
                "black_arcana:test_spell",
                0,
                ""));
    }

    @Test
    void castIntentCarriesOnlyBoundedIntent() {
        CastIntentPayload payload = new CastIntentPayload(
                ArcanaProtocol.VERSION,
                "11111111-1111-1111-1111-111111111111",
                "black_arcana:test_spell",
                3,
                "entity:22222222-2222-2222-2222-222222222222");
        assertEquals("black_arcana:test_spell", payload.parsedSpellId().canonical());

        assertThrows(IllegalArgumentException.class, () -> new CastIntentPayload(
                ArcanaProtocol.VERSION,
                payload.castId(),
                payload.spellId(),
                ArcanaProtocol.MAX_LOADOUT_SLOTS,
                ""));
        assertThrows(IllegalArgumentException.class, () -> new CastIntentPayload(
                ArcanaProtocol.VERSION,
                payload.castId(),
                payload.spellId(),
                0,
                "x".repeat(ArcanaProtocol.MAX_TARGET_HINT_LENGTH + 1)));
        assertThrows(IllegalArgumentException.class, () -> new CastIntentPayload(
                ArcanaProtocol.VERSION,
                payload.castId(),
                "black_arcana:" + "a".repeat(ArcanaProtocol.MAX_RESOURCE_ID_LENGTH),
                0,
                ""));
    }

    @Test
    void resultAndSnapshotsAreBounded() {
        CastResultPayload result = CastResultPayload.from(
                ArcanaCastId.parse("11111111-1111-1111-1111-111111111111"),
                ArcanaCastResult.success("ok"));
        assertEquals("SUCCESS", result.status());

        assertThrows(IllegalArgumentException.class, () -> new CooldownSnapshotPayload(
                ArcanaProtocol.VERSION,
                java.util.Collections.nCopies(
                        ArcanaProtocol.MAX_COOLDOWN_ENTRIES + 1,
                        new CooldownSnapshotPayload.Entry("black_arcana:test", 1))));

        assertThrows(IllegalArgumentException.class, () -> new SpellPresentationPayload(
                ArcanaProtocol.VERSION,
                java.util.Collections.nCopies(
                        ArcanaProtocol.MAX_PRESENTATION_ENTRIES + 1,
                        new SpellPresentationPayload.Entry("black_arcana:test", "spell.black_arcana.test", "black_arcana:test"))));
    }

    @Test
    void snapshotsRejectDuplicateKeysAtTheProtocolBoundary() {
        assertThrows(IllegalArgumentException.class, () -> new CooldownSnapshotPayload(
                ArcanaProtocol.VERSION,
                List.of(
                        new CooldownSnapshotPayload.Entry("black_arcana:shared", 10),
                        new CooldownSnapshotPayload.Entry("black_arcana:shared", 20))));

        assertThrows(IllegalArgumentException.class, () -> new SpellPresentationPayload(
                ArcanaProtocol.VERSION,
                List.of(
                        new SpellPresentationPayload.Entry(
                                "black_arcana:test", "spell.black_arcana.test", "black_arcana:test"),
                        new SpellPresentationPayload.Entry(
                                "black_arcana:test", "spell.black_arcana.test_alt", "black_arcana:test_alt"))));
    }
}
