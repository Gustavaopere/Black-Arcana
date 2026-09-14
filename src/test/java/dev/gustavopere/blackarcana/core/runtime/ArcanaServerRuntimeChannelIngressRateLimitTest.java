package dev.gustavopere.blackarcana.core.runtime;

import dev.gustavopere.blackarcana.api.ArcanaCastContext;
import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaCastResult;
import dev.gustavopere.blackarcana.api.ArcanaChannelSpec;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.network.ArcanaProtocol;
import dev.gustavopere.blackarcana.network.ChannelBeginIntentPayload;
import dev.gustavopere.blackarcana.network.ChannelCancelIntentPayload;
import dev.gustavopere.blackarcana.network.ChannelReleaseIntentPayload;
import org.junit.jupiter.api.Test;

import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ArcanaServerRuntimeChannelIngressRateLimitTest {
    private static final UUID CASTER = UUID.fromString("8bc90d7d-c1f9-4d8a-a7f3-ea63cf27e18f");
    private static final String SPELL = "black_arcana:channel_rate_limit_probe";

    @Test
    void channelBeginSharesBoundedServerIngressBudget() {
        ArcanaServerRuntime runtime = new ArcanaServerRuntime(1, 8, 8);
        ArcanaCastContext context = new ArcanaCastContext(CASTER, 100L, "minecraft:overworld");

        ArcanaDecision first = runtime.beginChannel(context, new ChannelBeginIntentPayload(
                ArcanaProtocol.VERSION,
                ArcanaCastId.random().canonical(),
                SPELL,
                0));
        assertEquals("channel_not_configured", first.code(),
                "first BEGIN may reach normal channel authority checks");

        ArcanaDecision second = runtime.beginChannel(context, new ChannelBeginIntentPayload(
                ArcanaProtocol.VERSION,
                ArcanaCastId.random().canonical(),
                SPELL,
                0));
        assertEquals("rate_limited", second.code(),
                "new channel admission must share the bounded cast ingress budget per caster");
    }

    @Test
    void physicalReleaseRemainsTerminalAfterIngressBudgetIsExhausted() {
        ArcanaServerRuntime runtime = new ArcanaServerRuntime(1, 8, 8);
        ArcanaCastContext context = new ArcanaCastContext(CASTER, 100L, "minecraft:overworld");
        ArcanaCastId activeCast = ArcanaCastId.random();
        assertTrue(runtime.channels().begin(
                CASTER,
                activeCast,
                ArcanaSpellId.parse(SPELL),
                0,
                context.serverTick(),
                new ArcanaChannelSpec(0L, 40L)).allowed());

        ArcanaDecision budgetConsumer = runtime.beginChannel(context, new ChannelBeginIntentPayload(
                ArcanaProtocol.VERSION,
                ArcanaCastId.random().canonical(),
                "black_arcana:unconfigured_rate_limit_probe",
                0));
        assertEquals("channel_not_configured", budgetConsumer.code());

        ArcanaCastResult release = runtime.releaseChannel(context, new ChannelReleaseIntentPayload(
                ArcanaProtocol.VERSION,
                activeCast.canonical(),
                ""));
        assertNotEquals(ArcanaCastResult.Status.DENIED_INGRESS, release.status(),
                "RELEASE must remain processable after the admission budget is exhausted");
        assertEquals(0, runtime.channels().activeSessions(),
                "physical key release must settle the exact server session instead of trapping it until timeout");
    }

    @Test
    void cancelRemainsTerminalAfterIngressBudgetIsExhausted() {
        ArcanaServerRuntime runtime = new ArcanaServerRuntime(1, 8, 8);
        ArcanaCastContext context = new ArcanaCastContext(CASTER, 100L, "minecraft:overworld");
        ArcanaCastId activeCast = ArcanaCastId.random();
        assertTrue(runtime.channels().begin(
                CASTER,
                activeCast,
                ArcanaSpellId.parse(SPELL),
                0,
                context.serverTick(),
                new ArcanaChannelSpec(0L, 40L)).allowed());

        ArcanaDecision budgetConsumer = runtime.beginChannel(context, new ChannelBeginIntentPayload(
                ArcanaProtocol.VERSION,
                ArcanaCastId.random().canonical(),
                "black_arcana:unconfigured_rate_limit_probe",
                0));
        assertEquals("channel_not_configured", budgetConsumer.code());

        assertTrue(runtime.cancelChannel(context, new ChannelCancelIntentPayload(
                ArcanaProtocol.VERSION,
                activeCast.canonical())),
                "CANCEL must remain processable after the admission budget is exhausted");
        assertEquals(0, runtime.channels().activeSessions());
    }
}
