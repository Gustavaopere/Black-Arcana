package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.content.souls.SoulAnchorLedger;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.server.MinecraftServer;
import net.minecraft.world.level.GameType;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;

import java.lang.reflect.Method;
import java.util.UUID;

@GameTestHolder(BlackArcanaMod.MOD_ID)
@PrefixGameTestTemplate(false)
public final class SoulAnchorGameTests {
    private SoulAnchorGameTests() { }

    @SuppressWarnings("removal")
    @GameTest(template = "foundation_empty", timeoutTicks = 80)
    public static void fatalPlayerDeathConsumesOneAnchorAndRestoresHealth(GameTestHelper helper) throws Exception {
        var player = helper.makeMockServerPlayerInLevel();
        player.setGameMode(GameType.SURVIVAL);
        player.getAbilities().invulnerable = false;
        player.getAbilities().instabuild = false;
        player.onUpdateAbilities();

        MinecraftServer server = helper.getLevel().getServer();
        SoulAnchorLedger.Policy policy = new SoulAnchorLedger.Policy(2, 10.0D, 100.0D, 600L, 64);

        Class<?> runtime = Class.forName(
            "dev.gustavopere.blackarcana.integration.neoforge.MinecraftSoulAnchorRuntime");
        Method configure = runtime.getMethod(
            "configure", MinecraftServer.class, SoulAnchorLedger.Policy.class, float.class);
        ArcanaDecision configured = (ArcanaDecision) configure.invoke(null, server, policy, 6.0F);
        helper.assertTrue(configured.allowed(), "Soul Anchor runtime must accept an explicit bounded policy");

        Method creditDeath = runtime.getMethod(
            "creditDeath", MinecraftServer.class, UUID.class, SoulAnchorLedger.DeathCredit.class);
        SoulAnchorLedger.CreditResult credit = (SoulAnchorLedger.CreditResult) creditDeath.invoke(
            null,
            server,
            player.getUUID(),
            new SoulAnchorLedger.DeathCredit(UUID.randomUUID(), 10.0D, 1.0D, true));
        helper.assertTrue(credit.credited(), "fixture death credit must enter the configured Mortal Ledger");

        Method formAnchor = runtime.getMethod("formAnchor", MinecraftServer.class, UUID.class);
        helper.assertTrue((boolean) formAnchor.invoke(null, server, player.getUUID()),
            "fixture must form exactly one Soul Anchor");
        Method snapshot = runtime.getMethod("snapshot", MinecraftServer.class, UUID.class);

        player.setHealth(4.0F);
        player.invulnerableTime = 0;
        player.die(player.damageSources().magic());
        SoulAnchorLedger.Snapshot after = (SoulAnchorLedger.Snapshot) snapshot.invoke(null, server, player.getUUID());

        helper.assertTrue(player.isAlive(), "fatal death event must be canceled while an eligible Soul Anchor exists");
        helper.assertTrue(Math.abs(player.getHealth() - 6.0F) <= 0.01F,
            "Soul Anchor must restore the configured bounded health amount; actual=" + player.getHealth()
                + ", anchors=" + after.anchors()
                + ", recoveryUntil=" + after.recoveryUntilTick());
        helper.assertTrue(after.anchors() == 0, "fatal event must consume exactly one Soul Anchor");
        helper.assertTrue(after.recoveryUntilTick() > server.overworld().getGameTime(),
            "successful prevention must start the configured recovery lockout");
        helper.succeed();
    }

    @SuppressWarnings("removal")
    @GameTest(template = "foundation_empty", timeoutTicks = 80)
    public static void runtimeReconfigureRehydratesPersistedLedgerAndDeathIds(GameTestHelper helper) throws Exception {
        var player = helper.makeMockServerPlayerInLevel();
        player.setGameMode(GameType.SURVIVAL);
        player.getAbilities().invulnerable = false;
        player.getAbilities().instabuild = false;
        player.onUpdateAbilities();

        MinecraftServer server = helper.getLevel().getServer();
        SoulAnchorLedger.Policy policy = new SoulAnchorLedger.Policy(2, 10.0D, 100.0D, 600L, 64);
        UUID creditedDeathId = UUID.randomUUID();

        Class<?> runtime = Class.forName(
            "dev.gustavopere.blackarcana.integration.neoforge.MinecraftSoulAnchorRuntime");
        Method configure = runtime.getMethod(
            "configure", MinecraftServer.class, SoulAnchorLedger.Policy.class, float.class);
        Method creditDeath = runtime.getMethod(
            "creditDeath", MinecraftServer.class, UUID.class, SoulAnchorLedger.DeathCredit.class);
        Method formAnchor = runtime.getMethod("formAnchor", MinecraftServer.class, UUID.class);
        Method snapshot = runtime.getMethod("snapshot", MinecraftServer.class, UUID.class);

        ArcanaDecision firstConfiguration = (ArcanaDecision) configure.invoke(null, server, policy, 5.0F);
        helper.assertTrue(firstConfiguration.allowed(), "initial Soul Anchor runtime configuration must succeed");
        SoulAnchorLedger.CreditResult firstCredit = (SoulAnchorLedger.CreditResult) creditDeath.invoke(
            null,
            server,
            player.getUUID(),
            new SoulAnchorLedger.DeathCredit(creditedDeathId, 10.0D, 1.0D, true));
        helper.assertTrue(firstCredit.credited(), "initial credited death must be persisted");
        helper.assertTrue((boolean) formAnchor.invoke(null, server, player.getUUID()),
            "initial persisted spirit must form one anchor");

        ArcanaDecision reconfigured = (ArcanaDecision) configure.invoke(null, server, policy, 7.0F);
        helper.assertTrue(reconfigured.allowed(), "runtime must rehydrate the persisted bounded ledger");

        SoulAnchorLedger.Snapshot restored = (SoulAnchorLedger.Snapshot) snapshot.invoke(null, server, player.getUUID());
        helper.assertTrue(restored.anchors() == 1, "rehydration must preserve the formed anchor");
        helper.assertTrue(restored.recentDeathEventIds().contains(creditedDeathId),
            "rehydration must preserve credited death ids for exactly-once accounting");

        SoulAnchorLedger.CreditResult duplicate = (SoulAnchorLedger.CreditResult) creditDeath.invoke(
            null,
            server,
            player.getUUID(),
            new SoulAnchorLedger.DeathCredit(creditedDeathId, 10.0D, 1.0D, true));
        helper.assertTrue(!duplicate.credited(), "rehydrated ledger must reject duplicate death credit");

        player.setHealth(4.0F);
        player.invulnerableTime = 0;
        player.die(player.damageSources().magic());
        SoulAnchorLedger.Snapshot after = (SoulAnchorLedger.Snapshot) snapshot.invoke(null, server, player.getUUID());

        helper.assertTrue(player.isAlive(), "rehydrated anchor must still prevent the fatal death event");
        helper.assertTrue(Math.abs(player.getHealth() - 7.0F) <= 0.01F,
            "rehydrated runtime must use the new configured restore amount");
        helper.assertTrue(after.anchors() == 0, "rehydrated anchor must be consumed exactly once");
        helper.assertTrue(after.recoveryUntilTick() > server.overworld().getGameTime(),
            "rehydrated runtime must persist the post-revival lockout");
        helper.succeed();
    }
}
