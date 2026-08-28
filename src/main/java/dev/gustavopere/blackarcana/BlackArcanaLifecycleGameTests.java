package dev.gustavopere.blackarcana;

import dev.gustavopere.blackarcana.api.ArcanaCastContext;
import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaCooldownSpec;
import dev.gustavopere.blackarcana.api.ArcanaCost;
import dev.gustavopere.blackarcana.api.ArcanaSpellDefinition;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.api.ArcanaTargetSpec;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntime;
import dev.gustavopere.blackarcana.core.targeting.ServerEntityTargetSelector;
import net.minecraft.core.BlockPos;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.world.entity.EntityType;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;

import java.util.Map;
import java.util.concurrent.atomic.AtomicReference;

@GameTestHolder(BlackArcanaMod.MOD_ID)
@PrefixGameTestTemplate(false)
public final class BlackArcanaLifecycleGameTests {
    private BlackArcanaLifecycleGameTests() { }

    @SuppressWarnings("removal")
    @GameTest(template = "foundation_empty", timeoutTicks = 40)
    public static void serverEntityTargetingRespectsFriendlyPolicy(GameTestHelper helper) {
        var caster = helper.makeMockServerPlayerInLevel();
        BlockPos casterPos = helper.absolutePos(new BlockPos(1, 2, 1));
        caster.teleportTo(casterPos.getX() + 0.5D, casterPos.getY(), casterPos.getZ() + 0.5D);
        var target = helper.spawnWithNoFreeWill(EntityType.ZOMBIE, new BlockPos(4, 2, 1));

        var scoreboard = caster.getScoreboard();
        String teamName = "ba_" + caster.getUUID().toString().substring(0, 8);
        var team = scoreboard.addPlayerTeam(teamName);
        try {
            scoreboard.addPlayerToTeam(caster.getScoreboardName(), team);
            scoreboard.addPlayerToTeam(target.getScoreboardName(), team);
            helper.assertTrue(caster.isAlliedTo(target), "scoreboard team must establish vanilla allied state");

            AtomicReference<ArcanaTargetSpec> spec = new AtomicReference<>(new ArcanaTargetSpec(
                    ArcanaTargetSpec.Kind.ENTITY,
                    8.0D,
                    1,
                    false,
                    false,
                    false));
            ServerEntityTargetSelector selector = new ServerEntityTargetSelector(
                    helper.getLevel().getServer(),
                    request -> spec.get());
            ArcanaCastRequest request = new ArcanaCastRequest(
                    ArcanaCastId.random(),
                    syntheticSpell(),
                    new ArcanaCastContext(
                            caster.getUUID(),
                            helper.getLevel().getGameTime(),
                            helper.getLevel().dimension().location().toString()),
                    0,
                    target.getUUID().toString());

            helper.assertTrue(
                    !selector.resolve(request).resolved(),
                    "friendly entity must be rejected when allowFriendly=false");

            spec.set(new ArcanaTargetSpec(
                    ArcanaTargetSpec.Kind.ENTITY,
                    8.0D,
                    1,
                    false,
                    false,
                    true));
            helper.assertTrue(
                    selector.resolve(request).resolved(),
                    "same friendly entity must resolve when allowFriendly=true");
        } finally {
            scoreboard.removePlayerTeam(team);
        }
        helper.succeed();
    }

    @SuppressWarnings("removal")
    @GameTest(template = "foundation_empty", timeoutTicks = 40)
    public static void playerDeathDoesNotResetPersistentCooldown(GameTestHelper helper) {
        var caster = helper.makeMockServerPlayerInLevel();
        ArcanaSpellDefinition spell = syntheticSpell();
        long now = helper.getLevel().getGameTime();

        ArcanaServerRuntime runtime = ArcanaServerRuntime.createDefault();
        runtime.cooldownPolicies().replaceAll(
                Map.of(spell.id(), new ArcanaCooldownSpec("black_arcana:death_probe", 100L, true)),
                Map.of());

        ArcanaCastRequest beforeDeath = request(caster, spell, now);
        runtime.cooldowns().start(beforeDeath);
        helper.assertTrue(!runtime.cooldowns().check(request(caster, spell, now + 1L)).allowed(),
                "cooldown must be active before death");

        // Exercise Minecraft's real ServerPlayer death route. The GameTest mock logs the death
        // but does not preserve the normal post-death alive/dead state, so the contract under
        // test is the server-owned cooldown state keyed by the same player UUID.
        caster.die(helper.getLevel().damageSources().generic());

        ArcanaCastRequest afterDeath = new ArcanaCastRequest(
                ArcanaCastId.random(),
                spell,
                new ArcanaCastContext(
                        caster.getUUID(),
                        now + 2L,
                        helper.getLevel().dimension().location().toString()));
        helper.assertTrue(
                !runtime.cooldowns().check(afterDeath).allowed(),
                "death must not clear caster-global persistent cooldown state");
        helper.assertTrue(runtime.cooldowns().size() == 1,
                "death must not remove the persistent cooldown entry");
        helper.succeed();
    }

    private static ArcanaCastRequest request(
            net.minecraft.server.level.ServerPlayer caster,
            ArcanaSpellDefinition spell,
            long tick
    ) {
        return new ArcanaCastRequest(
                ArcanaCastId.random(),
                spell,
                new ArcanaCastContext(
                        caster.getUUID(),
                        tick,
                        caster.serverLevel().dimension().location().toString()));
    }

    private static ArcanaSpellDefinition syntheticSpell() {
        return new ArcanaSpellDefinition(
                ArcanaSpellId.parse("black_arcana:lifecycle_probe"),
                "spell.black_arcana.lifecycle_probe",
                "black_arcana:lifecycle_probe",
                new ArcanaCost("black_arcana:synthetic", 1.0),
                false);
    }
}
