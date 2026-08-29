package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.content.blood.SympatheticWoundService;
import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.Registries;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.MinecraftServer;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.damagesource.DamageType;
import net.minecraft.world.entity.EntityType;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;

import java.lang.reflect.Method;

@GameTestHolder(BlackArcanaMod.MOD_ID)
@PrefixGameTestTemplate(false)
public final class SympatheticWoundGameTests {
    private static final ResourceKey<DamageType> SYMPATHETIC_WOUND = ResourceKey.create(
        Registries.DAMAGE_TYPE,
        ResourceLocation.fromNamespaceAndPath(BlackArcanaMod.MOD_ID, "sympathetic_wound"));

    private SympatheticWoundGameTests() { }

    @GameTest(template = "foundation_empty", timeoutTicks = 60)
    public static void mirroredDamageIsAttributedAndCannotRecurseThroughCrossLinks(GameTestHelper helper) throws Exception {
        var first = helper.spawnWithNoFreeWill(EntityType.COW, new BlockPos(2, 2, 1));
        var second = helper.spawnWithNoFreeWill(EntityType.COW, new BlockPos(5, 2, 1));
        helper.assertTrue(first.getArmorValue() == 0 && second.getArmorValue() == 0,
            "fixture entities must have no armor mitigation");

        MinecraftServer server = helper.getLevel().getServer();
        long now = server.overworld().getGameTime();

        Class<?> runtime = Class.forName(
            "dev.gustavopere.blackarcana.integration.neoforge.MinecraftSympatheticWoundRuntime");
        Method bind = runtime.getMethod(
            "bind",
            MinecraftServer.class,
            SympatheticWoundService.LinkSpec.class);

        ArcanaDecision firstLink = (ArcanaDecision) bind.invoke(null, server, new SympatheticWoundService.LinkSpec(
            first.getUUID(), second.getUUID(), now + 40L, 0.50D, 10.0D, 20.0D));
        ArcanaDecision secondLink = (ArcanaDecision) bind.invoke(null, server, new SympatheticWoundService.LinkSpec(
            second.getUUID(), first.getUUID(), now + 40L, 0.50D, 10.0D, 20.0D));
        helper.assertTrue(firstLink.allowed() && secondLink.allowed(), "cross-links must bind on the active server runtime");

        float firstBefore = first.getHealth();
        float secondBefore = second.getHealth();
        helper.assertTrue(first.hurt(first.damageSources().magic(), 8.0F), "fixture direct damage must be accepted");

        helper.assertTrue(first.getHealth() == firstBefore - 8.0F,
            "generated sympathetic damage must not recurse through the reverse link");
        helper.assertTrue(second.getHealth() == secondBefore - 4.0F,
            "mirror fraction must apply before ordinary target-side mitigation");

        DamageSource mirroredSource = second.getLastDamageSource();
        helper.assertTrue(mirroredSource != null && mirroredSource.is(SYMPATHETIC_WOUND),
            "mirrored damage must carry the dedicated Sympathetic Wound damage type");
        helper.assertTrue(mirroredSource.getEntity() == first,
            "the wounded source entity must remain attributed as the causing entity");
        helper.succeed();
    }
}
