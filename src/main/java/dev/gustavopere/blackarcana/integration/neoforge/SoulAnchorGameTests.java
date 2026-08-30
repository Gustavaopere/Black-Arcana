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
        boolean accepted = player.hurt(player.damageSources().magic(), 100.0F);
        SoulAnchorLedger.Snapshot after = (SoulAnchorLedger.Snapshot) snapshot.invoke(null, server, player.getUUID());

        helper.assertTrue(accepted,
            "fixture fatal damage must be accepted; actualHealth=" + player.getHealth()
                + ", anchors=" + after.anchors()
                + ", recoveryUntil=" + after.recoveryUntilTick());
        helper.assertTrue(player.isAlive(), "fatal damage must be canceled while an eligible Soul Anchor exists");
        helper.assertTrue(Math.abs(player.getHealth() - 6.0F) <= 0.01F,
            "Soul Anchor must restore the configured bounded health amount; actual=" + player.getHealth()
                + ", anchors=" + after.anchors()
                + ", recoveryUntil=" + after.recoveryUntilTick());
        helper.assertTrue(after.anchors() == 0, "fatal event must consume exactly one Soul Anchor");
        helper.assertTrue(after.recoveryUntilTick() > server.overworld().getGameTime(),
            "successful prevention must start the configured recovery lockout");
        helper.succeed();
    }
}
