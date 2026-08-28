package dev.gustavopere.blackarcana;

import dev.gustavopere.blackarcana.api.ArcanaCastContext;
import dev.gustavopere.blackarcana.api.ArcanaCastEngine;
import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaCastResult;
import dev.gustavopere.blackarcana.api.ArcanaCooldownSpec;
import dev.gustavopere.blackarcana.api.ArcanaCost;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.api.ArcanaServices;
import dev.gustavopere.blackarcana.api.ArcanaSpellDefinition;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.core.cast.BoundedReplayGuard;
import dev.gustavopere.blackarcana.core.cast.CompositeCastRequestValidator;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntime;
import dev.gustavopere.blackarcana.network.ArcanaProtocol;
import dev.gustavopere.blackarcana.network.CastIntentPayload;
import dev.gustavopere.blackarcana.persistence.BlackArcanaSavedData;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.nbt.CompoundTag;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;

import java.util.List;
import java.util.Map;
import java.util.UUID;

@GameTestHolder(BlackArcanaMod.MOD_ID)
@PrefixGameTestTemplate(false)
public final class BlackArcanaGameTests {
    private BlackArcanaGameTests() {
    }

    @GameTest(template = "foundation_empty", timeoutTicks = 20)
    public static void foundationLoadsOnDedicatedGameTestServer(GameTestHelper helper) {
        helper.assertTrue("black_arcana".equals(BlackArcanaMod.MOD_ID), "canonical mod id must remain stable");
        helper.succeed();
    }

    @GameTest(template = "foundation_empty", timeoutTicks = 40)
    public static void syntheticArcanaCoreCastRunsWithoutOptionalMagicMods(GameTestHelper helper) {
        UUID caster = UUID.fromString("28c0ad10-9dfa-41c6-a32c-303f0ef31815");
        ArcanaSpellDefinition spell = syntheticSpell();

        ArcanaServerRuntime runtime = ArcanaServerRuntime.createDefault();
        runtime.spells().replaceAll(List.of(spell));
        runtime.loadouts().setLoadout(caster, List.of(spell.id()));
        runtime.cooldownPolicies().replaceAll(
                Map.of(spell.id(), new ArcanaCooldownSpec("black_arcana:gametest_probe", 20L, true)),
                Map.of());

        ArcanaServices.CostProvider freeSyntheticCost = new ArcanaServices.CostProvider() {
            @Override
            public ArcanaDecision check(ArcanaCastRequest request) {
                return ArcanaDecision.allow();
            }

            @Override
            public ArcanaServices.CostReservation reserve(ArcanaCastRequest request) {
                return new ArcanaServices.CostReservation() {
                    @Override
                    public ArcanaDecision decision() {
                        return ArcanaDecision.allow();
                    }

                    @Override
                    public void commit() { }

                    @Override
                    public void refund() { }
                };
            }
        };

        ArcanaCastEngine engine = new ArcanaCastEngine(
                new CompositeCastRequestValidator(List.of(runtime.spells(), runtime.loadouts())),
                new BoundedReplayGuard(32, 100L),
                request -> ArcanaDecision.allow(),
                runtime.cooldowns(),
                request -> ArcanaServices.TargetResolution.resolved("synthetic:self"),
                freeSyntheticCost,
                (request, target) -> ArcanaDecision.allow(),
                (request, target) -> ArcanaServices.EffectResult.ok());
        runtime.installEngine(spell.id(), engine);

        long now = helper.getLevel().getGameTime();
        ArcanaCastContext context = new ArcanaCastContext(
                caster,
                now,
                helper.getLevel().dimension().location().toString());

        var first = runtime.handle(context, new CastIntentPayload(
                ArcanaProtocol.VERSION,
                ArcanaCastId.random().canonical(),
                spell.id().canonical(),
                0,
                ""));
        helper.assertTrue(
                ArcanaCastResult.Status.SUCCESS.name().equals(first.status()),
                "synthetic core cast must succeed through ingress and engine");

        var second = runtime.handle(context, new CastIntentPayload(
                ArcanaProtocol.VERSION,
                ArcanaCastId.random().canonical(),
                spell.id().canonical(),
                0,
                ""));
        helper.assertTrue(
                ArcanaCastResult.Status.DENIED_COOLDOWN.name().equals(second.status()),
                "successful cast must start its server-owned cooldown");
        helper.succeed();
    }

    @GameTest(template = "foundation_empty", timeoutTicks = 40)
    public static void savedDataRoundTripsCooldownAndLoadoutState(GameTestHelper helper) {
        UUID caster = UUID.fromString("28c0ad10-9dfa-41c6-a32c-303f0ef31815");
        ArcanaSpellDefinition spell = syntheticSpell();
        long now = helper.getLevel().getGameTime();
        ArcanaCastRequest request = new ArcanaCastRequest(
                spell,
                new ArcanaCastContext(caster, now, helper.getLevel().dimension().location().toString()));

        ArcanaServerRuntime source = ArcanaServerRuntime.createDefault();
        source.cooldownPolicies().replaceAll(
                Map.of(spell.id(), new ArcanaCooldownSpec("black_arcana:gametest_probe", 40L, true)),
                Map.of());
        source.loadouts().setLoadout(caster, List.of(spell.id()));
        source.cooldowns().start(request);

        BlackArcanaSavedData data = new BlackArcanaSavedData();
        data.capture(source.cooldowns(), source.charges(), source.loadouts(), now);
        CompoundTag encoded = data.save(new CompoundTag(), helper.getLevel().registryAccess());
        BlackArcanaSavedData decoded = BlackArcanaSavedData.load(encoded, helper.getLevel().registryAccess());

        ArcanaServerRuntime restored = ArcanaServerRuntime.createDefault();
        restored.cooldownPolicies().replaceAll(
                Map.of(spell.id(), new ArcanaCooldownSpec("black_arcana:gametest_probe", 40L, true)),
                Map.of());
        decoded.restore(restored.cooldowns(), restored.charges(), restored.loadouts(), now);

        helper.assertTrue(restored.cooldowns().size() == 1, "persistent cooldown must survive NBT round-trip");
        helper.assertTrue(
                restored.loadouts().getLoadout(caster).equals(List.of(spell.id())),
                "server-owned loadout must survive NBT round-trip");
        helper.assertTrue(
                !restored.cooldowns().check(new ArcanaCastRequest(
                        spell,
                        new ArcanaCastContext(caster, now + 1L, helper.getLevel().dimension().location().toString()))).allowed(),
                "restored cooldown must still deny before ready tick");
        helper.succeed();
    }

    private static ArcanaSpellDefinition syntheticSpell() {
        return new ArcanaSpellDefinition(
                ArcanaSpellId.parse("black_arcana:gametest_probe"),
                "spell.black_arcana.gametest_probe",
                "black_arcana:textures/spell/gametest_probe.png",
                new ArcanaCost("black_arcana:synthetic", 1.0),
                false);
    }
}
