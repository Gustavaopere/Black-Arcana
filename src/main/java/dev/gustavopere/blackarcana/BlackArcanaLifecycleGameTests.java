package dev.gustavopere.blackarcana;

import dev.gustavopere.blackarcana.api.ArcanaCastContext;
import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaCooldownSpec;
import dev.gustavopere.blackarcana.api.ArcanaCost;
import dev.gustavopere.blackarcana.api.ArcanaSpellDefinition;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntime;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;

import java.util.Map;

@GameTestHolder(BlackArcanaMod.MOD_ID)
@PrefixGameTestTemplate(false)
public final class BlackArcanaLifecycleGameTests {
    private BlackArcanaLifecycleGameTests() { }

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

        // Exercise the real ServerPlayer death route. GameTest's embedded mock logs the
        // death but does not preserve the normal post-death alive/dead lifecycle state,
        // so the contract here is the server-owned cooldown keyed by the same UUID.
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
