package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import dev.gustavopere.blackarcana.api.ArcanaCastContext;
import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaCost;
import dev.gustavopere.blackarcana.api.ArcanaServices;
import dev.gustavopere.blackarcana.api.ArcanaSpellDefinition;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.core.world.ConfigurableWorldEffectPolicy;
import dev.gustavopere.blackarcana.core.world.WorldEffectMode;
import dev.gustavopere.blackarcana.core.world.WorldEffectPolicyConfig;
import dev.gustavopere.blackarcana.core.world.WorldEffectProfile;
import dev.gustavopere.blackarcana.core.world.WorldEffectProfileRegistry;
import dev.gustavopere.blackarcana.core.world.WorldMutationClass;
import dev.gustavopere.blackarcana.core.world.WorldMutationType;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;

import java.util.Map;
import java.util.UUID;

@GameTestHolder(BlackArcanaMod.MOD_ID)
@PrefixGameTestTemplate(false)
public final class WorldEffectPolicyGameTests {
    private WorldEffectPolicyGameTests() { }

    @GameTest(template = "foundation_empty", timeoutTicks = 20)
    public static void worldEffectModesEnforceIncreasingMutationCeilings(GameTestHelper helper) {
        helper.assertTrue(!allows(helper, WorldEffectMode.OFF, WorldMutationClass.COSMETIC), "OFF must deny cosmetic mutation");
        helper.assertTrue(allows(helper, WorldEffectMode.COSMETIC, WorldMutationClass.COSMETIC), "COSMETIC must allow cosmetic fields");
        helper.assertTrue(!allows(helper, WorldEffectMode.COSMETIC, WorldMutationClass.TEMPORARY), "COSMETIC must deny temporary blocks");
        helper.assertTrue(allows(helper, WorldEffectMode.TEMPORARY, WorldMutationClass.TEMPORARY), "TEMPORARY must allow temporary blocks");
        helper.assertTrue(!allows(helper, WorldEffectMode.TEMPORARY, WorldMutationClass.LIMITED), "TEMPORARY must deny limited permanent work");
        helper.assertTrue(allows(helper, WorldEffectMode.LIMITED, WorldMutationClass.LIMITED), "LIMITED must allow bounded persistent work");
        helper.assertTrue(!allows(helper, WorldEffectMode.LIMITED, WorldMutationClass.PERMANENT), "LIMITED must deny unrestricted permanent work");
        helper.assertTrue(allows(helper, WorldEffectMode.FULL, WorldMutationClass.PERMANENT), "FULL must allow permanent-class work within hard caps");
        helper.succeed();
    }

    private static boolean allows(GameTestHelper helper, WorldEffectMode mode, WorldMutationClass mutationClass) {
        ArcanaSpellId id = ArcanaSpellId.parse("black_arcana:policy_" + mode.name().toLowerCase() + "_" + mutationClass.name().toLowerCase());
        WorldEffectProfileRegistry profiles = new WorldEffectProfileRegistry();
        profiles.register(id, new WorldEffectProfile(
            mutationClass == WorldMutationClass.COSMETIC ? WorldMutationType.VISUAL_FIELD : WorldMutationType.TEMPORARY_BLOCK,
            mutationClass,
            1,
            false));
        ConfigurableWorldEffectPolicy policy = new ConfigurableWorldEffectPolicy(
            profiles,
            new WorldEffectPolicyConfig(mode, 8, true, Map.of()));
        ArcanaCastRequest request = new ArcanaCastRequest(
            ArcanaCastId.random(),
            new ArcanaSpellDefinition(
                id,
                "spell." + id.namespace() + "." + id.path(),
                "black_arcana:textures/spell/policy_probe.png",
                new ArcanaCost("black_arcana:synthetic", 1.0D),
                true),
            new ArcanaCastContext(
                UUID.fromString("55555555-5555-5555-5555-555555555555"),
                helper.getLevel().getGameTime(),
                helper.getLevel().dimension().location().toString()));
        return policy.authorize(request, ArcanaServices.TargetResolution.resolved("policy-probe")).allowed();
    }
}
