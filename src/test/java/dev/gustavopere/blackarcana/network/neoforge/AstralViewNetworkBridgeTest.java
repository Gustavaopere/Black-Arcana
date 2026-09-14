package dev.gustavopere.blackarcana.network.neoforge;

import dev.gustavopere.blackarcana.network.ArcanaProtocol;
import dev.gustavopere.blackarcana.network.AstralViewPayload;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.Test;

import java.util.UUID;
import java.util.concurrent.atomic.AtomicReference;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

class AstralViewNetworkBridgeTest {
    @AfterEach
    void resetHandler() {
        AstralSeveranceNetworkBridge.installViewHandler((player, payload) -> { });
    }

    @Test
    void installedClientHandlerReceivesValidatedAstralViewPayload() {
        AstralViewPayload payload = new AstralViewPayload(
                ArcanaProtocol.VERSION,
                AstralViewPayload.Action.BEGIN,
                UUID.randomUUID(),
                23);
        AtomicReference<AstralViewPayload> received = new AtomicReference<>();
        AstralSeveranceNetworkBridge.installViewHandler((player, instruction) -> received.set(instruction));

        AstralSeveranceNetworkBridge.dispatchViewClientbound(null, payload);

        assertEquals(payload, received.get());
    }

    @Test
    void clientHandlerInstallationFailsClosedOnNull() {
        assertThrows(NullPointerException.class, () -> AstralSeveranceNetworkBridge.installViewHandler(null));
    }
}
