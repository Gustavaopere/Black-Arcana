package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.content.forbidden.DomainReturnPoint;
import dev.gustavopere.blackarcana.content.forbidden.InnerDominionSessionJournal;
import net.minecraft.nbt.CompoundTag;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.Map;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;

class InnerDominionSavedDataTest {
    private static InnerDominionSessionJournal.ReturnRoute route(String dimension, double x) {
        return new InnerDominionSessionJournal.ReturnRoute(
            new DomainReturnPoint(dimension, x, 64.0D, 1.0D),
            new DomainReturnPoint(dimension, x + 1.0D, 64.0D, 1.0D));
    }

    @Test void snapshotsRoundTripWithoutLosingRecoveryRoutes() {
        UUID sessionId = UUID.randomUUID();
        UUID owner = UUID.randomUUID();
        UUID guest = UUID.randomUUID();
        var session = new InnerDominionSessionJournal.Session(
            sessionId,
            owner,
            1_234L,
            Map.of(
                owner, route("minecraft:overworld", 2.5D),
                guest, route("minecraft:the_nether", -4.5D)));

        CompoundTag encoded = InnerDominionSavedData.encode(List.of(session));
        List<InnerDominionSessionJournal.Session> decoded = InnerDominionSavedData.decode(encoded);

        assertEquals(List.of(session), decoded);
    }

    @Test void emptySnapshotRoundTripsAsEmptyRecoveryJournal() {
        assertEquals(List.of(), InnerDominionSavedData.decode(InnerDominionSavedData.encode(List.of())));
    }
}
