package dev.gustavopere.blackarcana;

import dev.gustavopere.blackarcana.content.noetic.FamiliarOwnershipProvider;
import dev.gustavopere.blackarcana.content.noetic.NoeticObservationKind;
import dev.gustavopere.blackarcana.content.noetic.NoeticSafetyCeilings;
import dev.gustavopere.blackarcana.integration.neoforge.MinecraftNoeticRuntime;
import net.minecraft.core.BlockPos;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.network.chat.Component;
import net.minecraft.world.entity.EntityType;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;

import java.util.UUID;

@GameTestHolder(BlackArcanaMod.MOD_ID)
@PrefixGameTestTemplate(false)
public final class BlackArcanaNoeticGameTests {
    private BlackArcanaNoeticGameTests() { }

    @SuppressWarnings("removal")
    @GameTest(template = "foundation_empty", timeoutTicks = 80)
    public static void loadedObservationProducesOnlyBoundedWhitelistedSnapshot(GameTestHelper helper) {
        var server = helper.getLevel().getServer();
        var viewer = helper.makeMockServerPlayerInLevel();
        var target = helper.spawnWithNoFreeWill(EntityType.COW, new BlockPos(3, 2, 3));
        target.setCustomName(Component.literal("N".repeat(NoeticSafetyCeilings.MAX_DISPLAY_NAME_LENGTH + 32)));
        viewer.teleportTo(target.getX() + 2.0D, target.getY(), target.getZ());

        try {
            var decision = MinecraftNoeticRuntime.startObservation(
                    server,
                    viewer.getUUID(),
                    target.getUUID(),
                    NoeticObservationKind.NAMESCRY,
                    20,
                    false);
            helper.assertTrue(decision.allowed(),
                    "already-loaded same-dimension NPC must pass bounded Namescry admission: " + decision.code());
            helper.assertTrue(MinecraftNoeticRuntime.activeObservations(server) == 1,
                    "successful observation must create exactly one server-owned session");

            var snapshot = MinecraftNoeticRuntime.observationSnapshot(server, viewer.getUUID()).orElse(null);
            helper.assertTrue(snapshot != null, "live observation must expose its sanitized perception snapshot");
            if (snapshot != null) {
                helper.assertTrue(snapshot.targetId().equals(target.getUUID()),
                        "snapshot identity must remain the admitted loaded target");
                helper.assertTrue("minecraft:cow".equals(snapshot.entityTypeId()),
                        "snapshot may expose only the whitelisted entity type id");
                helper.assertTrue(snapshot.displayName().length() <= NoeticSafetyCeilings.MAX_DISPLAY_NAME_LENGTH,
                        "snapshot display name must remain inside its hard privacy/size bound");
                helper.assertTrue(snapshot.activeEffectIds().size() <= NoeticSafetyCeilings.MAX_EFFECT_IDS,
                        "snapshot effect metadata must remain bounded");
                helper.assertTrue(snapshot.mainHandItemId() != null && !snapshot.mainHandItemId().isBlank(),
                        "snapshot may expose the whitelisted main-hand item id only");
            }
        } finally {
            MinecraftNoeticRuntime.clearEntity(server, viewer.getUUID());
            MinecraftNoeticRuntime.clearEntity(server, target.getUUID());
        }

        helper.assertTrue(MinecraftNoeticRuntime.activeStateCount(server) == 0,
                "explicit cleanup must leave no active Noetic observation/astral/gaze/sanctuary state");
        helper.succeed();
    }

    @SuppressWarnings("removal")
    @GameTest(template = "foundation_empty", timeoutTicks = 80)
    public static void astralSeveranceUsesDedicatedServerOwnedIdentityAndExactReturn(GameTestHelper helper) {
        var server = helper.getLevel().getServer();
        var caster = helper.makeMockServerPlayerInLevel();

        try {
            var start = MinecraftNoeticRuntime.activateAuthorizedAstralProjection(
                    server,
                    caster.getUUID(),
                    20,
                    8.0D);
            helper.assertTrue(start.decision().allowed(),
                    "authorized loaded living caster must enter the dedicated Astral lifecycle: "
                            + start.decision().code());
            var projection = start.projection().orElse(null);
            helper.assertTrue(projection != null,
                    "successful Astral lifecycle activation must allocate one server-owned identity");
            if (projection != null) {
                helper.assertTrue(projection.casterId().equals(caster.getUUID()),
                        "projection caster identity must remain the physical player");
                helper.assertTrue(projection.physicalBodyId().equals(caster.getUUID()),
                        "projection must never replace the physical body identity");
                helper.assertTrue(!MinecraftNoeticRuntime.requestAstralReturn(
                                server, caster.getUUID(), UUID.randomUUID()),
                        "foreign/stale projection identity must not terminate the active session");
                helper.assertTrue(MinecraftNoeticRuntime.requestAstralReturn(
                                server, caster.getUUID(), projection.projectionId()),
                        "exact server-authored projection identity must permit explicit return");
                helper.assertTrue(!MinecraftNoeticRuntime.requestAstralReturn(
                                server, caster.getUUID(), projection.projectionId()),
                        "replayed explicit return must be an idempotent no-op");
            }
            helper.assertTrue(MinecraftNoeticRuntime.activeAstralProjections(server) == 0,
                    "explicit return must leave no active Astral projection");
        } finally {
            MinecraftNoeticRuntime.clearEntity(server, caster.getUUID());
        }

        helper.assertTrue(MinecraftNoeticRuntime.activeStateCount(server) == 0,
                "Astral lifecycle GameTest cleanup must leave no Stage 07.07 state");
        helper.succeed();
    }

    @SuppressWarnings("removal")
    @GameTest(template = "foundation_empty", timeoutTicks = 80)
    public static void playerNamescryWithoutConsentFailsClosed(GameTestHelper helper) {
        var server = helper.getLevel().getServer();
        var viewer = helper.makeMockServerPlayerInLevel();
        var foreignPlayer = helper.makeMockServerPlayerInLevel();
        viewer.teleportTo(foreignPlayer.getX() + 2.0D, foreignPlayer.getY(), foreignPlayer.getZ());

        helper.assertTrue(!viewer.getUUID().equals(foreignPlayer.getUUID()),
                "privacy GameTest requires two distinct player identities");
        try {
            var decision = MinecraftNoeticRuntime.startObservation(
                    server,
                    viewer.getUUID(),
                    foreignPlayer.getUUID(),
                    NoeticObservationKind.NAMESCRY,
                    20,
                    false);
            helper.assertTrue(!decision.allowed(), "foreign player Namescry must fail closed without explicit consent");
            helper.assertTrue("noetic_namescry_player_privacy".equals(decision.code()),
                    "foreign player privacy denial must remain explicit and stable: " + decision.code());
            helper.assertTrue(MinecraftNoeticRuntime.activeObservations(server) == 0,
                    "denied Namescry must not allocate an observation session");
        } finally {
            MinecraftNoeticRuntime.clearEntity(server, viewer.getUUID());
            MinecraftNoeticRuntime.clearEntity(server, foreignPlayer.getUUID());
        }
        helper.succeed();
    }

    @SuppressWarnings("removal")
    @GameTest(template = "foundation_empty", timeoutTicks = 80)
    public static void borrowedSightForeignFamiliarFailsClosedAndCleanupIsIdempotent(GameTestHelper helper) {
        var server = helper.getLevel().getServer();
        var viewer = helper.makeMockServerPlayerInLevel();
        var foreignFamiliar = helper.spawnWithNoFreeWill(EntityType.COW, new BlockPos(3, 2, 3));
        viewer.teleportTo(foreignFamiliar.getX() + 2.0D, foreignFamiliar.getY(), foreignFamiliar.getZ());

        UUID foreignFamiliarId = foreignFamiliar.getUUID();
        boolean providerRegistered = MinecraftNoeticRuntime.registerFamiliarOwnershipProvider(
                server,
                new FamiliarOwnershipProvider() {
                    @Override
                    public String providerId() {
                        return "black_arcana:gametest_foreign_familiar";
                    }

                    @Override
                    public Result ownership(UUID ownerId, Object candidate) {
                        if (candidate instanceof net.minecraft.world.entity.Entity entity
                                && foreignFamiliarId.equals(entity.getUUID())) {
                            return Result.NOT_OWNED;
                        }
                        return Result.UNSUPPORTED;
                    }
                });
        helper.assertTrue(providerRegistered || MinecraftNoeticRuntime.familiarProviderCount(server) > 0,
                "foreign familiar test requires one explicit ownership provider boundary");

        var decision = MinecraftNoeticRuntime.startObservation(
                server,
                viewer.getUUID(),
                foreignFamiliar.getUUID(),
                NoeticObservationKind.BORROWED_SIGHT,
                20,
                false);
        helper.assertTrue(!decision.allowed(),
                "Borrowed Sight must fail closed when a provider explicitly reports foreign ownership");
        helper.assertTrue("noetic_borrowed_sight_authority".equals(decision.code()),
                "foreign familiar ownership denial must remain explicit: " + decision.code());
        helper.assertTrue(MinecraftNoeticRuntime.activeObservations(server) == 0,
                "failed Borrowed Sight must not allocate a session");

        helper.assertTrue(MinecraftNoeticRuntime.clearEntity(server, viewer.getUUID()) == 0,
                "cleanup after denied admission must be an idempotent no-op");
        helper.assertTrue(MinecraftNoeticRuntime.clearEntity(server, viewer.getUUID()) == 0,
                "repeated cleanup must remain an idempotent no-op");
        helper.assertTrue(MinecraftNoeticRuntime.activeStateCount(server) == 0,
                "denied foreign familiar observation must leave no active Noetic state");
        helper.succeed();
    }
}
