package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.api.hazard.*;
import net.minecraft.core.BlockPos;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.level.GameType;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;

import java.util.EnumMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;

@GameTestHolder(BlackArcanaMod.MOD_ID)
@PrefixGameTestTemplate(false)
public final class ArcaneBacklashGameTests {
    private ArcaneBacklashGameTests() { }

    @GameTest(template = "foundation_empty", timeoutTicks = 60)
    public static void confirmedMultiHitDamageProducesExactNonRecursiveBacklash(GameTestHelper helper) {
        ServerPlayer caster = helper.makeMockPlayer(GameType.SURVIVAL);
        helper.assertTrue(
            !caster.getAbilities().invulnerable,
            "backlash fixture must be a vulnerable survival player");
        var firstTarget = helper.spawnWithNoFreeWill(EntityType.ZOMBIE, new BlockPos(3, 2, 1));
        var secondTarget = helper.spawnWithNoFreeWill(EntityType.ZOMBIE, new BlockPos(5, 2, 1));
        var server = helper.getLevel().getServer();
        long now = server.overworld().getGameTime();
        ArcanaCastId cast = ArcanaCastId.parse("70000000-0000-0000-0000-000000000001");
        ArcanaSpellId spell = ArcanaSpellId.parse("black_arcana:backlash_gametest");
        ArcaneDangerProfile profile = new ArcaneDangerProfile(
            ArcaneDangerTier.FORBIDDEN, 1.0D, 0.0D, 0.0D, 200L, 16);
        ArcaneHazardSnapshot hazard = new ArcaneHazardSnapshot(
            cast, spell, caster.getUUID(), helper.getLevel().dimension().location().toString(), now, profile);
        helper.assertTrue(
            MinecraftArcaneDamagePipeline.activate(server, hazard, zeroResistance(), ArcaneBacklashPolicy.canonical()).activated(),
            "hazard session must activate");

        float casterBefore = caster.getHealth();
        var first = MinecraftArcaneDamagePipeline.hurtAttributed(
            firstTarget,
            firstTarget.damageSources().magic(),
            4.0F,
            provenance(cast, caster.getUUID(), spell, "70000000-0000-0000-0000-000000000002"));
        var second = MinecraftArcaneDamagePipeline.hurtAttributed(
            secondTarget,
            secondTarget.damageSources().magic(),
            3.0F,
            provenance(cast, caster.getUUID(), spell, "70000000-0000-0000-0000-000000000003"));

        helper.assertTrue(first.invoked() && first.accepted(), "first attributed hit must be accepted");
        helper.assertTrue(second.invoked() && second.accepted(), "second attributed hit must be accepted");
        helper.assertTrue(firstTarget.getHealth() == firstTarget.getMaxHealth() - 4.0F, "first target must lose four health");
        helper.assertTrue(secondTarget.getHealth() == secondTarget.getMaxHealth() - 3.0F, "second target must lose three health");
        helper.assertTrue(caster.getHealth() == casterBefore - 7.0F, "zero resistance must produce exact 1:1 backlash");

        var ledger = MinecraftArcaneDamagePipeline.hazardRuntime(server).orElseThrow()
            .backlashLedgers().find(cast).orElseThrow();
        helper.assertTrue(ledger.confirmedEligibleDamage() == 7.0D, "backlash itself must never recurse into eligible damage");
        helper.assertTrue(ledger.backlashSettled() == 7.0D, "ledger must settle exactly seven backlash damage");
        helper.succeed();
    }

    private static ArcanaDamageProvenance provenance(
        ArcanaCastId cast,
        UUID caster,
        ArcanaSpellId spell,
        String damageId
    ) {
        return new ArcanaDamageProvenance(
            cast,
            ArcanaDamageInstanceId.parse(damageId),
            caster,
            spell,
            ArcaneDamageFamily.DIRECT,
            true);
    }

    private static ArcaneResistanceSnapshot zeroResistance() {
        Map<ArcaneResistanceSourceCategory, Double> categories = new EnumMap<>(ArcaneResistanceSourceCategory.class);
        for (ArcaneResistanceSourceCategory category : ArcaneResistanceSourceCategory.values()) categories.put(category, 0.0D);
        return new ArcaneResistanceSnapshot(0.0D, 1.0D, 100.0D, 1_000.0D, List.of(), categories, List.of());
    }
}
