package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.api.hazard.ArcaneDamageFamily;
import dev.gustavopere.blackarcana.api.hazard.ArcanaDamageInstanceId;
import dev.gustavopere.blackarcana.api.hazard.ArcanaDamageProvenance;
import dev.gustavopere.blackarcana.api.hazard.ArcaneBacklashPolicy;
import dev.gustavopere.blackarcana.api.hazard.ArcaneDangerProfile;
import dev.gustavopere.blackarcana.api.hazard.ArcaneDangerTier;
import dev.gustavopere.blackarcana.api.hazard.ArcaneHazardSnapshot;
import dev.gustavopere.blackarcana.api.hazard.ArcaneResistanceSnapshot;
import dev.gustavopere.blackarcana.api.hazard.ArcaneResistanceSourceCategory;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntimeManager;
import net.minecraft.core.BlockPos;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.level.GameType;
import net.minecraft.world.scores.PlayerTeam;
import net.minecraft.world.scores.Scoreboard;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;

import java.util.EnumMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;

@GameTestHolder(BlackArcanaMod.MOD_ID)
@PrefixGameTestTemplate(false)
public final class ArcaneHazardProtectionGameTests {
    private ArcaneHazardProtectionGameTests() { }

    @SuppressWarnings("removal")
    @GameTest(template = "foundation_empty", timeoutTicks = 100)
    public static void attributedHazardDamageRespectsStage04AdmissionBeforeSettlement(GameTestHelper helper) {
        var caster = helper.makeMockServerPlayerInLevel();
        caster.setGameMode(GameType.SURVIVAL);
        caster.getAbilities().invulnerable = false;
        caster.getAbilities().instabuild = false;
        caster.onUpdateAbilities();
        var server = helper.getLevel().getServer();
        var runtime = ArcanaServerRuntimeManager.get(server).orElseThrow();
        long now = server.overworld().getGameTime();
        ArcanaCastId cast = ArcanaCastId.parse("71000000-0000-0000-0000-000000000001");
        ArcanaSpellId spell = ArcanaSpellId.parse("black_arcana:protection_gametest");
        ArcaneDangerProfile profile = new ArcaneDangerProfile(
            ArcaneDangerTier.FORBIDDEN, 1.0D, 0.0D, 0.0D, 200L, 16);
        ArcaneHazardSnapshot hazard = new ArcaneHazardSnapshot(
            cast, spell, caster.getUUID(), helper.getLevel().dimension().location().toString(), now, profile);
        helper.assertTrue(
            MinecraftArcaneDamagePipeline.activate(server, hazard, zeroResistance(), ArcaneBacklashPolicy.canonical()).activated(),
            "hazard session must activate");

        var playerTarget = helper.makeMockPlayer(GameType.SURVIVAL);
        float playerHealth = playerTarget.getHealth();
        boolean previousPvp = server.isPvpAllowed();
        try {
            server.setPvpAllowed(false);
            var deniedPvp = MinecraftProtectedArcaneDamageGateway.hurtAttributed(
                caster,
                playerTarget,
                playerTarget.damageSources().magic(),
                4.0F,
                provenance(cast, caster.getUUID(), spell, "71000000-0000-0000-0000-000000000002"));
            helper.assertTrue(
                !deniedPvp.invoked() && "pvp_disabled".equals(deniedPvp.code()),
                "PvP-disabled player damage must be denied before target.hurt");
            helper.assertTrue(playerTarget.getHealth() == playerHealth, "denied PvP damage must not change target health");
        } finally {
            server.setPvpAllowed(previousPvp);
        }

        var alliedTarget = helper.spawnWithNoFreeWill(EntityType.ZOMBIE, new BlockPos(3, 2, 1));
        Scoreboard scoreboard = helper.getLevel().getScoreboard();
        String teamName = "ba_hazard_ally";
        PlayerTeam existing = scoreboard.getPlayerTeam(teamName);
        if (existing != null) scoreboard.removePlayerTeam(existing);
        PlayerTeam team = scoreboard.addPlayerTeam(teamName);
        try {
            scoreboard.addPlayerToTeam(caster.getScoreboardName(), team);
            scoreboard.addPlayerToTeam(alliedTarget.getScoreboardName(), team);
            float alliedHealth = alliedTarget.getHealth();
            var deniedAllied = MinecraftProtectedArcaneDamageGateway.hurtAttributed(
                caster,
                alliedTarget,
                alliedTarget.damageSources().magic(),
                3.0F,
                provenance(cast, caster.getUUID(), spell, "71000000-0000-0000-0000-000000000003"));
            helper.assertTrue(
                !deniedAllied.invoked() && "target_allied".equals(deniedAllied.code()),
                "allied damage must be denied by the Stage 04 team policy");
            helper.assertTrue(alliedTarget.getHealth() == alliedHealth, "denied allied damage must not change target health");
        } finally {
            scoreboard.removePlayerTeam(team);
        }

        var protectedTarget = helper.spawnWithNoFreeWill(EntityType.ZOMBIE, new BlockPos(5, 2, 1));
        String protectedId = "entity:" + protectedTarget.getUUID();
        runtime.protectionAdapters().register(
            "hazard_gametest_claims",
            query -> protectedId.equals(query.targetId())
                ? ArcanaDecision.deny("claim_protected", "synthetic protected entity")
                : ArcanaDecision.allow());
        float protectedHealth = protectedTarget.getHealth();
        var deniedClaim = MinecraftProtectedArcaneDamageGateway.hurtAttributed(
            caster,
            protectedTarget,
            protectedTarget.damageSources().magic(),
            2.0F,
            provenance(cast, caster.getUUID(), spell, "71000000-0000-0000-0000-000000000004"));
        helper.assertTrue(
            !deniedClaim.invoked() && "claim_protected".equals(deniedClaim.code()),
            "protection adapters must deny attributed hazard damage before target.hurt");
        helper.assertTrue(protectedTarget.getHealth() == protectedHealth, "protected target health must remain unchanged");

        var boss = helper.spawnWithNoFreeWill(EntityType.WITHER, new BlockPos(7, 2, 1));
        float bossHealth = boss.getHealth();
        float casterHealth = caster.getHealth();
        var allowedBoss = MinecraftProtectedArcaneDamageGateway.hurtAttributed(
            caster,
            boss,
            boss.damageSources().magic(),
            1.0F,
            provenance(cast, caster.getUUID(), spell, "71000000-0000-0000-0000-000000000005"));
        helper.assertTrue(allowedBoss.invoked() && allowedBoss.accepted(), "boss damage must remain allowed under Stage 04 boss caps");
        helper.assertTrue(boss.getHealth() == bossHealth - 1.0F, "allowed boss hit must damage the boss exactly once");
        helper.assertTrue(caster.getHealth() == casterHealth - 1.0F, "only confirmed allowed damage may settle 1:1 backlash");

        var ledger = MinecraftArcaneDamagePipeline.hazardRuntime(server).orElseThrow()
            .backlashLedgers().find(cast).orElseThrow();
        helper.assertTrue(ledger.confirmedEligibleDamage() == 1.0D,
            "denied PvP/allied/protected hits must never enter confirmed hazard accounting");
        helper.assertTrue(ledger.backlashSettled() == 1.0D,
            "only the allowed boss hit may produce backlash settlement");
        boss.discard();
        alliedTarget.discard();
        protectedTarget.discard();
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
        for (ArcaneResistanceSourceCategory category : ArcaneResistanceSourceCategory.values()) {
            categories.put(category, 0.0D);
        }
        return new ArcaneResistanceSnapshot(0.0D, 1.0D, 100.0D, 1_000.0D, List.of(), categories, List.of());
    }
}
