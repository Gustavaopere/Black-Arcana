package dev.gustavopere.blackarcana.network.neoforge;

import dev.gustavopere.blackarcana.network.ArcanaProtocol;
import dev.gustavopere.blackarcana.network.CastResultPayload;
import dev.gustavopere.blackarcana.network.ChannelBeginIntentPayload;
import dev.gustavopere.blackarcana.network.ChannelBeginResultPayload;
import dev.gustavopere.blackarcana.network.ChannelCancelIntentPayload;
import dev.gustavopere.blackarcana.network.ChannelCapabilityPayload;
import dev.gustavopere.blackarcana.network.ChannelReleaseIntentPayload;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.concurrent.atomic.AtomicReference;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ChannelNetworkBridgeTest {
    private static final String CAST_ID = "11111111-1111-1111-1111-111111111111";

    @AfterEach
    void resetHandlers() {
        ChannelNetworkBridge.installBeginHandler((player, payload) -> new ChannelBeginResultPayload(
                ArcanaProtocol.VERSION, payload.castId(), false, "handler_reset", "test reset"));
        ChannelNetworkBridge.installReleaseHandler((player, payload) -> new CastResultPayload(
                ArcanaProtocol.VERSION, payload.castId(), "DENIED_CHANNEL", "handler_reset", "test reset"));
        ChannelNetworkBridge.installCancelHandler((player, payload) -> false);
        ChannelNetworkBridge.installBeginResultHandler((player, payload) -> { });
        ChannelNetworkBridge.installCapabilityHandler((player, payload) -> { });
    }

    @Test
    void installedBeginResultHandlerReceivesValidatedPayload() {
        ChannelBeginResultPayload payload = new ChannelBeginResultPayload(
                ArcanaProtocol.VERSION,
                CAST_ID,
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
    void installedServerHandlersReceiveValidatedDomainPayloads() {
        ChannelBeginIntentPayload begin = new ChannelBeginIntentPayload(
                ArcanaProtocol.VERSION, CAST_ID, "black_arcana:channel_probe", 0);
        ChannelBeginResultPayload beginResult = new ChannelBeginResultPayload(
                ArcanaProtocol.VERSION, CAST_ID, true, "ok", "channel accepted");
        AtomicReference<ChannelBeginIntentPayload> receivedBegin = new AtomicReference<>();
        ChannelNetworkBridge.installBeginHandler((player, payload) -> {
            receivedBegin.set(payload);
            return beginResult;
        });

        ChannelReleaseIntentPayload release = new ChannelReleaseIntentPayload(
                ArcanaProtocol.VERSION, CAST_ID, "self");
        CastResultPayload releaseResult = new CastResultPayload(
                ArcanaProtocol.VERSION, CAST_ID, "SUCCESS", "ok", "released");
        AtomicReference<ChannelReleaseIntentPayload> receivedRelease = new AtomicReference<>();
        ChannelNetworkBridge.installReleaseHandler((player, payload) -> {
            receivedRelease.set(payload);
            return releaseResult;
        });

        ChannelCancelIntentPayload cancel = new ChannelCancelIntentPayload(ArcanaProtocol.VERSION, CAST_ID);
        AtomicReference<ChannelCancelIntentPayload> receivedCancel = new AtomicReference<>();
        ChannelNetworkBridge.installCancelHandler((player, payload) -> {
            receivedCancel.set(payload);
            return true;
        });

        assertEquals(beginResult, ChannelNetworkBridge.dispatchBeginServerbound(null, begin));
        assertEquals(begin, receivedBegin.get());
        assertEquals(releaseResult, ChannelNetworkBridge.dispatchReleaseServerbound(null, release));
        assertEquals(release, receivedRelease.get());
        assertTrue(ChannelNetworkBridge.dispatchCancelServerbound(null, cancel));
        assertEquals(cancel, receivedCancel.get());
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
