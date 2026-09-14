package dev.gustavopere.blackarcana.core.runtime;

import dev.gustavopere.blackarcana.api.ArcanaCastContext;
import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaCastResult;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.network.ArcanaProtocol;
import dev.gustavopere.blackarcana.network.ChannelBeginIntentPayload;
import dev.gustavopere.blackarcana.network.ChannelReleaseIntentPayload;
import org.junit.jupiter.api.Test;

import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;

class ArcanaServerRuntimeChannelIngressRateLimitTest {
    private static final UUID CASTER = UUID.fromString("8bc90d7d-c1f9-4d8a-a7f3-ea63cf27e18f");
    private static final String SPELL = "black_arcana:channel_rate_limit_probe";

    @Test
    void channelNetworkActionsShareBoundedServerIngressBudget() {
        ArcanaServerRuntime runtime = new ArcanaServerRuntime(1, 8, 8);
        ArcanaCastContext context = new ArcanaCastContext(CASTER, 100L, "minecraft:overworld");
        ArcanaCastId castId = ArcanaCastId.random();

        ArcanaDecision first = runtime.beginChannel(context, new ChannelBeginIntentPayload(
                ArcanaProtocol.VERSION,
                castId.canonical(),
                SPELL,
                0));
        assertEquals("channel_not_configured", first.code(),
                "first bounded network action may reach normal channel authority checks");

        ArcanaCastResult second = runtime.releaseChannel(context, new ChannelReleaseIntentPayload(
                ArcanaProtocol.VERSION,
                castId.canonical(),
                ""));
        assertEquals(ArcanaCastResult.Status.DENIED_INGRESS, second.status(),
                "channel C2S actions must not bypass the server ingress limiter");
        assertEquals("rate_limited", second.code(),
                "BEGIN and RELEASE must share one bounded channel ingress budget per caster");
    }
}
