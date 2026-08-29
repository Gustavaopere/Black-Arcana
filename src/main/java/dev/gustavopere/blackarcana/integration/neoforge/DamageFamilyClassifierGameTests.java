package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import net.minecraft.core.BlockPos;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.damagesource.DamageTypes;
import net.minecraft.world.entity.EntityType;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;

import java.lang.reflect.Method;

@GameTestHolder(BlackArcanaMod.MOD_ID)
@PrefixGameTestTemplate(false)
public final class DamageFamilyClassifierGameTests {
    private DamageFamilyClassifierGameTests() { }

    @GameTest(template = "foundation_empty", timeoutTicks = 60)
    public static void semanticTagsProduceStableFamiliesAndUnknownTypesFallBackToRegistryKey(GameTestHelper helper) throws Exception {
        var fixture = helper.spawnWithNoFreeWill(EntityType.COW, new BlockPos(2, 2, 1));

        assertFamily(helper, fixture.damageSources().source(DamageTypes.IN_FIRE), "black_arcana:fire");
        assertFamily(helper, fixture.damageSources().source(DamageTypes.ARROW), "black_arcana:projectile");
        assertFamily(helper, fixture.damageSources().source(DamageTypes.EXPLOSION), "black_arcana:explosion");
        assertFamily(helper, fixture.damageSources().source(DamageTypes.FALL), "black_arcana:fall");
        assertFamily(helper, fixture.damageSources().source(DamageTypes.DROWN), "black_arcana:drowning");
        assertFamily(helper, fixture.damageSources().source(DamageTypes.FREEZE), "black_arcana:freezing");
        assertFamily(helper, fixture.damageSources().source(DamageTypes.LIGHTNING_BOLT), "black_arcana:lightning");
        assertFamily(helper, fixture.damageSources().source(DamageTypes.MAGIC), "black_arcana:magic");
        assertFamily(helper, fixture.damageSources().source(SympatheticWoundDamageTypes.SYMPATHETIC_WOUND),
            "black_arcana:sympathetic_wound");
        helper.succeed();
    }

    private static void assertFamily(GameTestHelper helper, DamageSource source, String expected) throws Exception {
        Class<?> classifier = Class.forName(
            "dev.gustavopere.blackarcana.integration.neoforge.MinecraftDamageFamilyClassifier");
        Method classify = classifier.getMethod("classify", DamageSource.class);
        String actual = (String) classify.invoke(null, source);
        helper.assertTrue(expected.equals(actual),
            "expected damage family " + expected + " but got " + actual);
    }
}
