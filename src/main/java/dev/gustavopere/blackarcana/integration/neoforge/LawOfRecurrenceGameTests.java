package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.content.blood.LawOfRecurrenceTracker;
import net.minecraft.core.BlockPos;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.server.MinecraftServer;
import net.minecraft.world.damagesource.DamageTypes;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;

import java.lang.reflect.Method;
import java.util.UUID;

@GameTestHolder(BlackArcanaMod.MOD_ID)
@PrefixGameTestTemplate(false)
public final class LawOfRecurrenceGameTests {
    private LawOfRecurrenceGameTests() { }

    @GameTest(template = "foundation_empty", timeoutTicks = 80)
    public static void repeatedFamilyBuildsResistanceAndSwitchAppliesVulnerability(GameTestHelper helper) throws Exception {
        var target = helper.spawnWithNoFreeWill(EntityType.COW, new BlockPos(2, 2, 1));
        helper.assertTrue(target.getArmorValue() == 0, "fixture must not add armor mitigation");
        var maxHealth = target.getAttribute(Attributes.MAX_HEALTH);
        helper.assertTrue(maxHealth != null, "fixture requires the vanilla max-health attribute");
        maxHealth.setBaseValue(20.0D);
        helper.assertTrue(close(target.getMaxHealth(), 20.0F), "fixture must expose 20 real HP before damage assertions");

        MinecraftServer server = helper.getLevel().getServer();
        LawOfRecurrenceTracker.Policy policy = new LawOfRecurrenceTracker.Policy(
            0.10D, 0.40D, 0.15D, 0.60D, 8, 4, 40L);

        ArcanaDecision activated = activate(server, target.getUUID(), policy);
        helper.assertTrue(activated.allowed(), "Law of Recurrence must activate on a live server runtime");
        helper.assertTrue(isActive(server, target.getUUID()), "activated caster must own an active Law session");

        target.setHealth(20.0F);
        target.invulnerableTime = 0;
        helper.assertTrue(target.hurt(target.damageSources().source(DamageTypes.MAGIC), 10.0F),
            "first fixture hit must be accepted");
        helper.assertTrue(close(target.getHealth(), 11.0F),
            "first recognized family hit must receive one resistance stack; actualHealth=" + target.getHealth());

        target.setHealth(20.0F);
        target.invulnerableTime = 0;
        helper.assertTrue(target.hurt(target.damageSources().source(DamageTypes.MAGIC), 10.0F),
            "second fixture hit must be accepted");
        helper.assertTrue(close(target.getHealth(), 12.0F),
            "repeated family must build the second resistance stack; actualHealth=" + target.getHealth());

        target.setHealth(20.0F);
        target.invulnerableTime = 0;
        helper.assertTrue(target.hurt(target.damageSources().source(DamageTypes.IN_FIRE), 10.0F),
            "switched fixture hit must be accepted");
        helper.assertTrue(close(target.getHealth(), 9.65F),
            "family switch must combine one new-family resistance stack with bounded vulnerability; actualHealth="
                + target.getHealth());
        helper.succeed();
    }

    @GameTest(template = "foundation_empty", timeoutTicks = 80)
    public static void timedStateExpiresAndIsPruned(GameTestHelper helper) throws Exception {
        var target = helper.spawnWithNoFreeWill(EntityType.COW, new BlockPos(2, 2, 1));
        MinecraftServer server = helper.getLevel().getServer();
        LawOfRecurrenceTracker.Policy policy = new LawOfRecurrenceTracker.Policy(
            0.10D, 0.40D, 0.15D, 0.60D, 8, 4, 2L);

        ArcanaDecision activated = activate(server, target.getUUID(), policy);
        helper.assertTrue(activated.allowed(), "short Law of Recurrence session must activate");
        helper.assertTrue(isActive(server, target.getUUID()),
            "activation must create a session for this caster even when other GameTests run concurrently");
        helper.assertTrue(activeSessions(server) <= LawOfRecurrenceTracker.ABSOLUTE_MAX_TRACKED_CASTERS,
            "global Law session count must stay within the hard runtime ceiling");

        helper.runAfterDelay(4L, () -> {
            try {
                helper.assertTrue(!isActive(server, target.getUUID()),
                    "this caster's expired Law of Recurrence session must be pruned by server tick");
                helper.assertTrue(activeSessions(server) <= LawOfRecurrenceTracker.ABSOLUTE_MAX_TRACKED_CASTERS,
                    "parallel sessions must remain bounded after pruning");
                helper.succeed();
            } catch (Exception failure) {
                helper.fail("failed to inspect Law of Recurrence runtime: " + failure.getMessage());
            }
        });
    }

    private static ArcanaDecision activate(
        MinecraftServer server,
        UUID casterId,
        LawOfRecurrenceTracker.Policy policy
    ) throws Exception {
        Class<?> runtime = Class.forName(
            "dev.gustavopere.blackarcana.integration.neoforge.MinecraftLawOfRecurrenceRuntime");
        Method activate = runtime.getMethod(
            "activate",
            MinecraftServer.class,
            UUID.class,
            LawOfRecurrenceTracker.Policy.class);
        return (ArcanaDecision) activate.invoke(null, server, casterId, policy);
    }

    private static int activeSessions(MinecraftServer server) throws Exception {
        Class<?> runtime = Class.forName(
            "dev.gustavopere.blackarcana.integration.neoforge.MinecraftLawOfRecurrenceRuntime");
        Method activeSessions = runtime.getMethod("activeSessions", MinecraftServer.class);
        return (int) activeSessions.invoke(null, server);
    }

    private static boolean isActive(MinecraftServer server, UUID casterId) throws Exception {
        Class<?> runtime = Class.forName(
            "dev.gustavopere.blackarcana.integration.neoforge.MinecraftLawOfRecurrenceRuntime");
        Method isActive = runtime.getMethod("isActive", MinecraftServer.class, UUID.class);
        return (boolean) isActive.invoke(null, server, casterId);
    }

    private static boolean close(float actual, float expected) {
        return Math.abs(actual - expected) <= 0.01F;
    }
}
