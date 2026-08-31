package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.api.hazard.*;
import net.minecraft.core.BlockPos;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.damagesource.DamageSource;
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

    @SuppressWarnings("removal")
    @GameTest(template = "foundation_empty", timeoutTicks = 60)
    public static void confirmedMultiHitDamageProducesExactNonRecursiveBacklash(GameTestHelper helper) {
        ServerPlayer caster = helper.makeMockServerPlayerInLevel();
        caster.setGameMode(GameType.SURVIVAL);
        caster.getAbilities().invulnerable = false;
        caster.getAbilities().instabuild = false;
        caster.onUpdateAbilities();
        helper.assertTrue(
            !caster.getAbilities().invulnerable,
            "backlash fixture must be a vulnerable survival server player");
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

    @SuppressWarnings("removal")
    @GameTest(template = "foundation_empty", timeoutTicks = 60)
    public static void dedicatedBacklashSourceIsAttackerlessAndUnattributed(GameTestHelper helper) {
        ServerPlayer caster = helper.makeMockServerPlayerInLevel();
        caster.setGameMode(GameType.SURVIVAL);
        caster.getAbilities().invulnerable = false;
        caster.getAbilities().instabuild = false;
        caster.onUpdateAbilities();

        var server = helper.getLevel().getServer();
        long now = server.overworld().getGameTime();
        ArcanaCastId cast = ArcanaCastId.parse("76000000-0000-0000-0000-000000000001");
        ArcanaSpellId spell = ArcanaSpellId.parse("black_arcana:terminal_backlash_gametest");
        ArcaneDangerProfile profile = new ArcaneDangerProfile(
            ArcaneDangerTier.FORBIDDEN, 1.0D, 0.0D, 0.0D, 200L, 16);
        ArcaneHazardSnapshot hazard = new ArcaneHazardSnapshot(
            cast, spell, caster.getUUID(), helper.getLevel().dimension().location().toString(), now, profile);
        var activation = MinecraftArcaneDamagePipeline.activate(
            server,
            hazard,
            zeroResistance(),
            ArcaneBacklashPolicy.canonical());
        helper.assertTrue(activation.activated(), "terminal-backlash hazard session must activate; code=" + activation.code());

        DamageSource source = caster.damageSources().source(ArcaneBacklashDamageTypes.ARCANE_BACKLASH);
        helper.assertTrue(source.is(ArcaneBacklashDamageTypes.ARCANE_BACKLASH), "source must use the dedicated Arcane Backlash damage type");
        helper.assertTrue(source.getEntity() == null, "Arcane Backlash must not expose an attacker entity for lifesteal/proc credit");
        helper.assertTrue(source.getDirectEntity() == null, "Arcane Backlash must not expose a direct attacker for crit/proc credit");

        float before = caster.getHealth();
        helper.assertTrue(caster.hurt(source, 2.0F), "dedicated Backlash source must reach Minecraft damage");
        helper.assertTrue(caster.getHealth() == before - 2.0F, "dedicated Backlash source must apply the requested terminal health damage");

        var runtime = MinecraftArcaneDamagePipeline.hazardRuntime(server).orElseThrow();
        var ledger = runtime.backlashLedgers().find(cast).orElseThrow();
        var session = runtime.sessions().find(cast).orElseThrow();
        helper.assertTrue(ledger.confirmedEligibleDamage() == 0.0D, "unattributed Backlash must not create offensive eligible damage");
        helper.assertTrue(ledger.backlashSettled() == 0.0D, "unattributed Backlash must not settle recursive Backlash");
        helper.assertTrue(session.seenDamageInstances() == 0, "unattributed Backlash must not claim a damage-instance id");
        helper.succeed();
    }

    @SuppressWarnings("removal")
    @GameTest(template = "foundation_empty", timeoutTicks = 80)
    public static void projectileDotChainAndOwnedSummonAttributionRespectFrozenPolicy(GameTestHelper helper) {
        ServerPlayer caster = helper.makeMockServerPlayerInLevel();
        caster.setGameMode(GameType.SURVIVAL);
        caster.getAbilities().invulnerable = false;
        caster.getAbilities().instabuild = false;
        caster.onUpdateAbilities();
        helper.assertTrue(
            !caster.getAbilities().invulnerable,
            "attribution fixture must be a vulnerable survival server player");

        var projectileTarget = helper.spawnWithNoFreeWill(EntityType.ZOMBIE, new BlockPos(2, 2, 1));
        var dotTarget = helper.spawnWithNoFreeWill(EntityType.ZOMBIE, new BlockPos(3, 2, 1));
        var chainTarget = helper.spawnWithNoFreeWill(EntityType.ZOMBIE, new BlockPos(4, 2, 1));
        var deniedSummonTarget = helper.spawnWithNoFreeWill(EntityType.ZOMBIE, new BlockPos(5, 2, 1));
        var optedSummonTarget = helper.spawnWithNoFreeWill(EntityType.ZOMBIE, new BlockPos(6, 2, 1));

        var server = helper.getLevel().getServer();
        long now = server.overworld().getGameTime();
        UUID casterId = caster.getUUID();
        ArcanaSpellId spell = ArcanaSpellId.parse("black_arcana:attribution_gametest");
        ArcaneDangerProfile profile = new ArcaneDangerProfile(
            ArcaneDangerTier.FORBIDDEN, 1.0D, 0.0D, 0.0D, 200L, 16);

        ArcanaCastId standardCast = ArcanaCastId.parse("72000000-0000-0000-0000-000000000001");
        ArcaneHazardSnapshot standardHazard = new ArcaneHazardSnapshot(
            standardCast,
            spell,
            casterId,
            helper.getLevel().dimension().location().toString(),
            now,
            profile);
        var standardActivation = MinecraftArcaneDamagePipeline.activate(
            server,
            standardHazard,
            zeroResistance(),
            ArcaneBacklashPolicy.canonical());
        helper.assertTrue(
            standardActivation.activated(),
            "standard hazard session must activate; code=" + standardActivation.code());

        float casterBefore = caster.getHealth();
        var projectile = MinecraftArcaneDamagePipeline.hurtAttributed(
            projectileTarget,
            projectileTarget.damageSources().magic(),
            2.0F,
            provenance(
                standardCast,
                casterId,
                spell,
                "71000000-0000-0000-0000-000000000002",
                ArcaneDamageFamily.PROJECTILE));
        var dot = MinecraftArcaneDamagePipeline.hurtAttributed(
            dotTarget,
            dotTarget.damageSources().magic(),
            2.0F,
            provenance(
                standardCast,
                casterId,
                spell,
                "71000000-0000-0000-0000-000000000003",
                ArcaneDamageFamily.DAMAGE_OVER_TIME));
        var chain = MinecraftArcaneDamagePipeline.hurtAttributed(
            chainTarget,
            chainTarget.damageSources().magic(),
            2.0F,
            provenance(
                standardCast,
                casterId,
                spell,
                "71000000-0000-0000-0000-000000000004",
                ArcaneDamageFamily.CHAIN));
        var deniedSummon = MinecraftArcaneDamagePipeline.hurtAttributed(
            deniedSummonTarget,
            deniedSummonTarget.damageSources().magic(),
            2.0F,
            provenance(
                standardCast,
                casterId,
                spell,
                "71000000-0000-0000-0000-000000000005",
                ArcaneDamageFamily.OWNED_SUMMON));

        helper.assertTrue(projectile.invoked() && projectile.accepted(), "projectile hit must reach Minecraft damage");
        helper.assertTrue(dot.invoked() && dot.accepted(), "DoT hit must reach Minecraft damage");
        helper.assertTrue(chain.invoked() && chain.accepted(), "chain hit must reach Minecraft damage");
        helper.assertTrue(deniedSummon.invoked() && deniedSummon.accepted(), "non-opted summon still deals normal target damage");
        helper.assertTrue(
            caster.getHealth() == casterBefore - 6.0F,
            "canonical policy must settle projectile, DoT and chain but exclude owned summon");

        var standardLedger = MinecraftArcaneDamagePipeline.hazardRuntime(server).orElseThrow()
            .backlashLedgers().find(standardCast).orElseThrow();
        helper.assertTrue(
            standardLedger.confirmedEligibleDamage() == 6.0D,
            "non-opted owned summon must not enter confirmed eligible damage");
        helper.assertTrue(
            standardLedger.backlashSettled() == 6.0D,
            "zero resistance must settle the three eligible families exactly 1:1");

        ArcanaCastId optedCast = ArcanaCastId.parse("72000000-0000-0000-0000-000000000006");
        ArcaneHazardSnapshot optedHazard = new ArcaneHazardSnapshot(
            optedCast,
            spell,
            casterId,
            helper.getLevel().dimension().location().toString(),
            now,
            profile);
        ArcaneBacklashPolicy summonOptIn = new ArcaneBacklashPolicy(
            true,
            0.0D,
            ArcaneBacklashPolicy.ABSOLUTE_MAX_BACKLASH_PER_SETTLEMENT,
            ArcaneBacklashPolicy.ABSOLUTE_MAX_TOTAL_ELIGIBLE_DAMAGE);
        var optedActivation = MinecraftArcaneDamagePipeline.activate(
            server,
            optedHazard,
            zeroResistance(),
            summonOptIn);
        helper.assertTrue(
            optedActivation.activated(),
            "owned-summon opt-in hazard session must activate; code=" + optedActivation.code());

        var optedSummon = MinecraftArcaneDamagePipeline.hurtAttributed(
            optedSummonTarget,
            optedSummonTarget.damageSources().magic(),
            2.0F,
            provenance(
                optedCast,
                casterId,
                spell,
                "71000000-0000-0000-0000-000000000007",
                ArcaneDamageFamily.OWNED_SUMMON));
        helper.assertTrue(optedSummon.invoked() && optedSummon.accepted(), "opted owned summon must deal normal target damage");
        helper.assertTrue(
            caster.getHealth() == casterBefore - 8.0F,
            "explicit summon opt-in must add exact 1:1 backlash at zero resistance");

        var optedLedger = MinecraftArcaneDamagePipeline.hazardRuntime(server).orElseThrow()
            .backlashLedgers().find(optedCast).orElseThrow();
        helper.assertTrue(optedLedger.confirmedEligibleDamage() == 2.0D, "opted summon must enter eligible damage");
        helper.assertTrue(optedLedger.backlashSettled() == 2.0D, "opted summon must settle exact 1:1 backlash");
        helper.succeed();
    }

    private static ArcanaDamageProvenance provenance(
        ArcanaCastId cast,
        UUID caster,
        ArcanaSpellId spell,
        String damageId
    ) {
        return provenance(cast, caster, spell, damageId, ArcaneDamageFamily.DIRECT);
    }

    private static ArcanaDamageProvenance provenance(
        ArcanaCastId cast,
        UUID caster,
        ArcanaSpellId spell,
        String damageId,
        ArcaneDamageFamily family
    ) {
        return new ArcanaDamageProvenance(
            cast,
            ArcanaDamageInstanceId.parse(damageId),
            caster,
            spell,
            family,
            true);
    }

    private static ArcaneResistanceSnapshot zeroResistance() {
        Map<ArcaneResistanceSourceCategory, Double> categories = new EnumMap<>(ArcaneResistanceSourceCategory.class);
        for (ArcaneResistanceSourceCategory category : ArcaneResistanceSourceCategory.values()) categories.put(category, 0.0D);
        return new ArcaneResistanceSnapshot(0.0D, 1.0D, 100.0D, 1_000.0D, List.of(), categories, List.of());
    }
}
