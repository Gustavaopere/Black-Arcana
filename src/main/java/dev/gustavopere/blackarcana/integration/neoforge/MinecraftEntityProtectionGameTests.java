package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntime;
import dev.gustavopere.blackarcana.core.world.ChunkRef;
import dev.gustavopere.blackarcana.core.world.DefaultEntityInteractionPolicy;
import dev.gustavopere.blackarcana.core.world.EntityInteractionType;
import dev.gustavopere.blackarcana.core.world.ProtectionQuery;
import net.minecraft.core.BlockPos;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.level.GameType;
import net.minecraft.world.scores.PlayerTeam;
import net.minecraft.world.scores.Scoreboard;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;

@GameTestHolder(BlackArcanaMod.MOD_ID)
@PrefixGameTestTemplate(false)
public final class MinecraftEntityProtectionGameTests {
    private MinecraftEntityProtectionGameTests() { }

    @GameTest(template = "foundation_empty", timeoutTicks = 40)
    public static void serverPvpSettingProtectsPlayerTargets(GameTestHelper helper) {
        var caster = helper.makeMockPlayer(GameType.SURVIVAL);
        var target = helper.makeMockPlayer(GameType.SURVIVAL);
        var server = helper.getLevel().getServer();
        boolean previousPvp = server.isPvpAllowed();
        try {
            server.setPvpAllowed(false);
            var facts = MinecraftEntityProtectionResolver.resolve(server, caster, target);
            helper.assertTrue(facts.player(), "target player fact must be derived from the server entity");
            helper.assertTrue(!facts.invulnerable(), "survival fixture must not be classified as privileged/invulnerable");
            helper.assertTrue(!facts.serverPvpEnabled(), "resolver must read the live server PvP setting");
            var authorization = DefaultEntityInteractionPolicy.safeDefaults()
                .authorize(EntityInteractionType.DAMAGE, facts);
            helper.assertTrue(
                !authorization.decision().allowed() && "pvp_disabled".equals(authorization.decision().code()),
                "hostile player interaction must fail when server PvP is disabled");
        } finally {
            server.setPvpAllowed(previousPvp);
        }
        helper.succeed();
    }

    @GameTest(template = "foundation_empty", timeoutTicks = 40)
    public static void scoreboardAllianceProtectsTarget(GameTestHelper helper) {
        var caster = helper.makeMockPlayer(GameType.SURVIVAL);
        var target = helper.spawnWithNoFreeWill(EntityType.ZOMBIE, new BlockPos(3, 2, 1));
        Scoreboard scoreboard = helper.getLevel().getScoreboard();
        String teamName = "ba_gt_ally";
        PlayerTeam existing = scoreboard.getPlayerTeam(teamName);
        if (existing != null) scoreboard.removePlayerTeam(existing);
        PlayerTeam team = scoreboard.addPlayerTeam(teamName);
        try {
            scoreboard.addPlayerToTeam(caster.getScoreboardName(), team);
            scoreboard.addPlayerToTeam(target.getScoreboardName(), team);
            var facts = MinecraftEntityProtectionResolver.resolve(helper.getLevel().getServer(), caster, target);
            helper.assertTrue(facts.alliedWithCaster(), "scoreboard teammates must resolve as allied");
            var authorization = DefaultEntityInteractionPolicy.safeDefaults()
                .authorize(EntityInteractionType.CONTROL, facts);
            helper.assertTrue(
                !authorization.decision().allowed() && "target_allied".equals(authorization.decision().code()),
                "allied hostile control must be denied");
        } finally {
            scoreboard.removePlayerTeam(team);
        }
        helper.succeed();
    }

    @GameTest(template = "foundation_empty", timeoutTicks = 60)
    public static void bossesReceiveCapsInsteadOfBlanketImmunity(GameTestHelper helper) {
        var caster = helper.makeMockPlayer(GameType.SURVIVAL);
        var boss = helper.spawnWithNoFreeWill(EntityType.WITHER, new BlockPos(4, 2, 1));
        var facts = MinecraftEntityProtectionResolver.resolve(helper.getLevel().getServer(), caster, boss);
        helper.assertTrue(facts.boss(), "c:bosses membership must be recognized by the server resolver");

        var policy = DefaultEntityInteractionPolicy.safeDefaults();
        var damage = policy.authorize(EntityInteractionType.DAMAGE, facts);
        var execution = policy.authorize(EntityInteractionType.EXECUTION, facts);
        helper.assertTrue(damage.decision().allowed(), "boss damage must remain possible under boss-specific caps");
        helper.assertTrue(
            damage.limits().damageMultiplierCap() == 1.0D,
            "boss damage multiplier must use the safe cap");
        helper.assertTrue(
            !execution.decision().allowed() && "boss_execution_blocked".equals(execution.decision().code()),
            "boss execution must be explicitly blocked");
        boss.discard();
        helper.succeed();
    }

    @GameTest(template = "foundation_empty", timeoutTicks = 40)
    public static void invulnerableTargetsAreDenied(GameTestHelper helper) {
        var caster = helper.makeMockPlayer(GameType.SURVIVAL);
        var target = helper.spawnWithNoFreeWill(EntityType.ZOMBIE, new BlockPos(3, 2, 1));
        target.setInvulnerable(true);
        var facts = MinecraftEntityProtectionResolver.resolve(helper.getLevel().getServer(), caster, target);
        helper.assertTrue(facts.invulnerable(), "resolver must derive entity invulnerability from server state");
        var authorization = DefaultEntityInteractionPolicy.safeDefaults()
            .authorize(EntityInteractionType.DISPLACEMENT, facts);
        helper.assertTrue(
            !authorization.decision().allowed() && "target_invulnerable".equals(authorization.decision().code()),
            "invulnerable targets must reject hostile displacement");
        helper.succeed();
    }

    @GameTest(template = "foundation_empty", timeoutTicks = 40)
    public static void protectedAndUnloadedDestinationsFailClosed(GameTestHelper helper) {
        var caster = helper.makeMockPlayer(GameType.SURVIVAL);
        ArcanaServerRuntime runtime = ArcanaServerRuntime.createDefault();
        MinecraftTemporaryBlockBackend backend =
            new MinecraftTemporaryBlockBackend(helper.getLevel().getServer());
        runtime.installWorldBackend(backend, backend);
        runtime.protectionAdapters().register(
            "gametest_claims",
            query -> query.targetId().startsWith("protected:")
                ? ArcanaDecision.deny("claim_protected", "synthetic protected destination")
                : ArcanaDecision.allow());

        String dimension = helper.getLevel().dimension().location().toString();
        BlockPos loadedPos = helper.absolutePos(new BlockPos(1, 2, 1));
        ChunkRef loadedChunk = new ChunkRef(dimension, loadedPos.getX() >> 4, loadedPos.getZ() >> 4);
        ProtectionQuery protectedQuery = new ProtectionQuery(
            caster.getUUID(),
            dimension,
            "protected:" + loadedPos.asLong(),
            EntityInteractionType.DISPLACEMENT);
        var protectedDecision = runtime.protectedDestinationGuard().orElseThrow()
            .authorize(loadedChunk, protectedQuery);
        helper.assertTrue(
            !protectedDecision.allowed() && "claim_protected".equals(protectedDecision.code()),
            "loaded destination denied by a protection adapter must stay denied");

        ChunkRef unloadedChunk = new ChunkRef(
            dimension,
            loadedChunk.chunkX() + 2048,
            loadedChunk.chunkZ() + 2048);
        ProtectionQuery unloadedQuery = new ProtectionQuery(
            caster.getUUID(),
            dimension,
            "unloaded:destination",
            EntityInteractionType.DISPLACEMENT);
        var unloadedDecision = runtime.protectedDestinationGuard().orElseThrow()
            .authorize(unloadedChunk, unloadedQuery);
        helper.assertTrue(
            !unloadedDecision.allowed() && "world_chunk_unloaded".equals(unloadedDecision.code()),
            "displacement must not force-load an invalid/unloaded destination");
        helper.succeed();
    }
}
