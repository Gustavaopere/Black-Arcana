package dev.gustavopere.blackarcana.network.neoforge;

import dev.gustavopere.blackarcana.network.ArcanaProtocol;
import dev.gustavopere.blackarcana.network.ChannelBeginResultPayload;
import dev.gustavopere.blackarcana.network.ChannelCapabilityPayload;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.concurrent.atomic.AtomicReference;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

class ChannelNetworkBridgeTest {
    @AfterEach
    void resetClientHandlers() {
        ChannelNetworkBridge.installBeginResultHandler((player, payload) -> { });
        ChannelNetworkBridge.installCapabilityHandler((player, payload) -> { });
    }

    @Test
    void installedBeginResultHandlerReceivesValidatedPayload() {
        ChannelBeginResultPayload payload = new ChannelBeginResultPayload(
                ArcanaProtocol.VERSION,
                "11111111-1111-1111-1111-111111111111",
                true,
                "ok",
                "channel accepted");
        AtomicReference<ChannelBeginResultPayload> received = new AtomicReference<>();
        ChannelNetworkBridge.installBeginResultHandler((player, result) -> received.set(result));

        ChannelNetworkBridge.dispatchBeginResultClientbound(null, payload);

        assertEquals(payload, received.get());
    }

    @Test
    void installedCapabilityHandlerReceivesValidatedPayload() {
        ChannelCapabilityPayload payload = new ChannelCapabilityPayload(
                ArcanaProtocol.VERSION,
                List.of(new ChannelCapabilityPayload.Entry("black_arcana:channel_probe", 5L, 40L)));
        AtomicReference<ChannelCapabilityPayload> received = new AtomicReference<>();
        ChannelNetworkBridge.installCapabilityHandler((player, snapshot) -> received.set(snapshot));

        ChannelNetworkBridge.dispatchCapabilityClientbound(null, payload);

        assertEquals(payload, received.get());
    }

    @Test
    void handlerInstallationFailsClosedOnNull() {
        assertThrows(NullPointerException.class, () -> ChannelNetworkBridge.installBeginHandler(null));
        assertThrows(NullPointerException.class, () -> ChannelNetworkBridge.installReleaseHandler(null));
        assertThrows(NullPointerException.class, () -> ChannelNetworkBridge.installCancelHandler(null));
        assertThrows(NullPointerException.class, () -> ChannelNetworkBridge.installBeginResultHandler(null));
        assertThrows(NullPointerException.class, () -> ChannelNetworkBridge.installCapabilityHandler(null));
    }
}
