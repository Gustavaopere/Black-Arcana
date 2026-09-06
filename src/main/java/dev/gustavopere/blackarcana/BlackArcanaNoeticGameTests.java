package dev.gustavopere.blackarcana;

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
                    NoeticObservationKind.ASTRAL_SEVERANCE,
                    20,
                    false);
            helper.assertTrue(decision.allowed(),
                    "already-loaded same-dimension target must pass bounded Astral Severance admission: "
                            + decision.code());
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
                "explicit cleanup must leave no active Noetic session/gaze/sanctuary state");
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
    public static void borrowedSightForeignTargetFailsClosedAndCleanupIsIdempotent(GameTestHelper helper) {
        var server = helper.getLevel().getServer();
        var viewer = helper.makeMockServerPlayerInLevel();
        var foreignTarget = helper.spawnWithNoFreeWill(EntityType.COW, new BlockPos(3, 2, 3));
        viewer.teleportTo(foreignTarget.getX() + 2.0D, foreignTarget.getY(), foreignTarget.getZ());

        var decision = MinecraftNoeticRuntime.startObservation(
                server,
                viewer.getUUID(),
                foreignTarget.getUUID(),
                NoeticObservationKind.BORROWED_SIGHT,
                20,
                false);
        helper.assertTrue(!decision.allowed(),
                "Borrowed Sight must fail closed when no provider explicitly confirms target ownership");
        helper.assertTrue("noetic_borrowed_sight_authority".equals(decision.code()),
                "foreign/unsupported ownership denial must remain explicit: " + decision.code());
        helper.assertTrue(MinecraftNoeticRuntime.activeObservations(server) == 0,
                "failed Borrowed Sight must not allocate a session");

        helper.assertTrue(MinecraftNoeticRuntime.clearEntity(server, viewer.getUUID()) == 0,
                "cleanup after denied admission must be an idempotent no-op");
        helper.assertTrue(MinecraftNoeticRuntime.clearEntity(server, viewer.getUUID()) == 0,
                "repeated cleanup must remain an idempotent no-op");
        helper.assertTrue(MinecraftNoeticRuntime.activeStateCount(server) == 0,
                "denied foreign observation must leave no active Noetic state");
        helper.succeed();
    }
}
