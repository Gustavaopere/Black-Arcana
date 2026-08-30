package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.content.souls.SpiritSightPolicy;
import dev.gustavopere.blackarcana.content.souls.SpiritTraceProvider;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;

import java.util.List;
import java.util.Set;
import java.util.UUID;
import java.util.concurrent.atomic.AtomicBoolean;

@GameTestHolder(BlackArcanaMod.MOD_ID)
@PrefixGameTestTemplate(false)
public final class SpiritSightGameTests {
    private SpiritSightGameTests() { }

    @SuppressWarnings("removal")
    @GameTest(template = "foundation_empty", timeoutTicks = 80)
    public static void providerAbsenceRevealsNothing(GameTestHelper helper) {
        var player = helper.makeMockServerPlayerInLevel();
        var server = helper.getLevel().getServer();
        SpiritSightPolicy.Policy policy = new SpiritSightPolicy.Policy(
            16.0D,
            40L,
            Set.of(SpiritSightPolicy.TraceKind.SOUL),
            false);

        ArcanaDecision activation = MinecraftSpiritSightRuntime.activate(server, player.getUUID(), policy);
        helper.assertTrue(activation.allowed(), "Spirit Sight must activate without fabricating a provider");
        helper.assertTrue(MinecraftSpiritSightRuntime.visibleTraces(server, player.getUUID()).isEmpty(),
            "provider absence must reveal no synthetic traces");
        helper.succeed();
    }

    @SuppressWarnings("removal")
    @GameTest(template = "foundation_empty", timeoutTicks = 80)
    public static void radiusCategoryPrivacyAndProviderDisappearanceAreFailClosed(GameTestHelper helper) {
        var player = helper.makeMockServerPlayerInLevel();
        var server = helper.getLevel().getServer();
        var position = player.position();
        AtomicBoolean available = new AtomicBoolean(true);

        SpiritTraceProvider provider = new SpiritTraceProvider() {
            @Override
            public String providerId() {
                return "black_arcana:test_spirit_sight";
            }

            @Override
            public List<Trace> query(Query query) {
                if (!available.get()) return List.of();
                return List.of(
                    new Trace(UUID.randomUUID(), position.x + 2.0D, position.y, position.z,
                        SpiritSightPolicy.TraceKind.SOUL, false),
                    new Trace(UUID.randomUUID(), position.x + 2.0D, position.y, position.z,
                        SpiritSightPolicy.TraceKind.ECHO, false),
                    new Trace(UUID.randomUUID(), position.x + 2.0D, position.y, position.z,
                        SpiritSightPolicy.TraceKind.SOUL, true),
                    new Trace(UUID.randomUUID(), position.x + 40.0D, position.y, position.z,
                        SpiritSightPolicy.TraceKind.SOUL, false));
            }
        };

        ArcanaDecision registered = MinecraftSpiritSightRuntime.registerProvider(server, provider);
        helper.assertTrue(registered.allowed(), "bounded Spirit Sight provider registration must succeed");

        SpiritSightPolicy.Policy policy = new SpiritSightPolicy.Policy(
            16.0D,
            40L,
            Set.of(SpiritSightPolicy.TraceKind.SOUL),
            false);
        helper.assertTrue(MinecraftSpiritSightRuntime.activate(server, player.getUUID(), policy).allowed(),
            "Spirit Sight activation must succeed for loaded living caster");

        List<SpiritTraceProvider.Trace> visible = MinecraftSpiritSightRuntime.visibleTraces(server, player.getUUID());
        helper.assertTrue(visible.size() == 1,
            "radius, category and private-data filters must leave exactly one visible trace; actual=" + visible.size());
        helper.assertTrue(visible.getFirst().kind() == SpiritSightPolicy.TraceKind.SOUL,
            "visible trace must retain its real provider-backed category");

        available.set(false);
        helper.assertTrue(MinecraftSpiritSightRuntime.visibleTraces(server, player.getUUID()).isEmpty(),
            "provider disappearance must immediately remove its traces instead of caching synthetic state");
        helper.assertTrue(MinecraftSpiritSightRuntime.unregisterProvider(server, provider.providerId()),
            "test provider must be removable without leaving visible state");
        helper.succeed();
    }

    @SuppressWarnings("removal")
    @GameTest(template = "foundation_empty", timeoutTicks = 80)
    public static void timedSessionExpiresAndStopsRevealing(GameTestHelper helper) {
        var player = helper.makeMockServerPlayerInLevel();
        var server = helper.getLevel().getServer();
        var position = player.position();
        SpiritTraceProvider provider = new SpiritTraceProvider() {
            @Override
            public String providerId() {
                return "black_arcana:test_spirit_sight_expiry";
            }

            @Override
            public List<Trace> query(Query query) {
                return List.of(new Trace(UUID.randomUUID(), position.x + 1.0D, position.y, position.z,
                    SpiritSightPolicy.TraceKind.SOUL, false));
            }
        };
        MinecraftSpiritSightRuntime.registerProvider(server, provider);
        SpiritSightPolicy.Policy policy = new SpiritSightPolicy.Policy(
            8.0D,
            2L,
            Set.of(SpiritSightPolicy.TraceKind.SOUL),
            false);
        MinecraftSpiritSightRuntime.activate(server, player.getUUID(), policy);
        helper.assertTrue(MinecraftSpiritSightRuntime.visibleTraces(server, player.getUUID()).size() == 1,
            "active Spirit Sight session must expose eligible provider trace");

        helper.runAfterDelay(4L, () -> {
            helper.assertTrue(!MinecraftSpiritSightRuntime.isActive(server, player.getUUID()),
                "expired Spirit Sight session must be pruned");
            helper.assertTrue(MinecraftSpiritSightRuntime.visibleTraces(server, player.getUUID()).isEmpty(),
                "expired session must reveal no traces");
            MinecraftSpiritSightRuntime.unregisterProvider(server, provider.providerId());
            helper.succeed();
        });
    }
}
