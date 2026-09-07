package dev.gustavopere.blackarcana.network.neoforge;

import dev.gustavopere.blackarcana.content.noetic.NoeticObservationKind;
import dev.gustavopere.blackarcana.network.ArcanaProtocol;
import dev.gustavopere.blackarcana.network.NoeticViewPayload;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.Test;

import java.util.concurrent.atomic.AtomicReference;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

class NoeticViewNetworkBridgeTest {
    @AfterEach
    void resetHandler() {
        NoeticViewNetworkBridge.installClientHandler((player, payload) -> { });
    }

    @Test
    void installedClientHandlerReceivesValidatedBorrowedSightPayload() {
        NoeticViewPayload payload = new NoeticViewPayload(
                ArcanaProtocol.VERSION,
                NoeticViewPayload.Action.BEGIN,
                NoeticObservationKind.BORROWED_SIGHT,
                23);
        AtomicReference<NoeticViewPayload> received = new AtomicReference<>();
        NoeticViewNetworkBridge.installClientHandler((player, instruction) -> received.set(instruction));

        NoeticViewNetworkBridge.dispatchClientbound(null, payload);

        assertEquals(payload, received.get());
    }

    @Test
    void clientHandlerInstallationFailsClosedOnNull() {
        assertThrows(NullPointerException.class, () -> NoeticViewNetworkBridge.installClientHandler(null));
    }
}
