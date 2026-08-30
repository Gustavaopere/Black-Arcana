package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import dev.gustavopere.blackarcana.content.projection.ProjectedWeaponProfile;
import dev.gustavopere.blackarcana.content.projection.ProjectionSafetyCeilings;
import net.minecraft.core.component.DataComponents;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.network.chat.Component;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.entity.item.ItemEntity;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.neoforged.neoforge.event.entity.player.PlayerEvent;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;

@GameTestHolder(BlackArcanaMod.MOD_ID)
@PrefixGameTestTemplate(false)
public final class EchoArmamentGameTests {
    private EchoArmamentGameTests() { }

    @SuppressWarnings("removal")
    @GameTest(template = "foundation_empty", timeoutTicks = 80)
    public static void heldWeaponBecomesSanitizedProfileWithoutMutatingSource(GameTestHelper helper) {
        var player = helper.makeMockServerPlayerInLevel();
        var server = helper.getLevel().getServer();
        ItemStack source = new ItemStack(Items.DIAMOND_SWORD);
        source.set(DataComponents.CUSTOM_NAME, Component.literal("Private Blade Name"));
        player.setItemInHand(InteractionHand.MAIN_HAND, source);

        var result = MinecraftEchoArmamentRuntime.rememberHeldWeapon(
            server,
            player.getUUID(),
            "black_arcana:test_echo_blade");

        helper.assertTrue(result.decision().allowed(), "eligible held weapon must be rememberable");
        ProjectedWeaponProfile profile = result.profile().orElseThrow();
        helper.assertTrue(profile.sourceItemId().equals("minecraft:diamond_sword"),
            "profile must retain only the stable source item registry id");
        helper.assertTrue(profile.archetype() == ProjectedWeaponProfile.Archetype.MELEE,
            "diamond sword must sanitize as melee projection input");
        helper.assertTrue(profile.attackDamageContribution() > 0.0D
                && profile.attackDamageContribution() <= ProjectionSafetyCeilings.MAX_RAW_ATTACK_DAMAGE,
            "observed attack damage must remain within hard projection ceiling");
        helper.assertTrue(profile.attackSpeed() > 0.0D && profile.attackSpeed() <= 20.0D,
            "observed attack speed must remain within technical bounds");
        helper.assertTrue(source.getHoverName().getString().equals("Private Blade Name"),
            "remembering a weapon must not mutate or strip source item components");
        helper.assertTrue(MinecraftEchoArmamentRuntime.findProfile(
                server, player.getUUID(), "black_arcana:test_echo_blade").isPresent(),
            "sanitized profile must be stored in bounded server memory");
        helper.succeed();
    }

    @SuppressWarnings("removal")
    @GameTest(template = "foundation_empty", timeoutTicks = 80)
    public static void unsupportedContainerItemIsRejectedWithoutMemoryEntry(GameTestHelper helper) {
        var player = helper.makeMockServerPlayerInLevel();
        var server = helper.getLevel().getServer();
        player.setItemInHand(InteractionHand.MAIN_HAND, new ItemStack(Items.CHEST));

        var result = MinecraftEchoArmamentRuntime.rememberHeldWeapon(
            server,
            player.getUUID(),
            "black_arcana:test_bad_echo");

        helper.assertTrue(!result.decision().allowed(), "ordinary storage item must not become a weapon echo profile");
        helper.assertTrue(result.decision().code().equals("echo_armament_unsupported_item"),
            "unsupported item denial must be explicit and stable");
        helper.assertTrue(result.profile().isEmpty(), "denied capture must not return a profile");
        helper.assertTrue(MinecraftEchoArmamentRuntime.findProfile(
                server, player.getUUID(), "black_arcana:test_bad_echo").isEmpty(),
            "denied capture must not create registry state");
        helper.succeed();
    }

    @SuppressWarnings("removal")
    @GameTest(template = "foundation_empty", timeoutTicks = 80)
    public static void manifestationIsServerOnlyAndExpiresWithoutCreatingItemEntity(GameTestHelper helper) {
        var player = helper.makeMockServerPlayerInLevel();
        var server = helper.getLevel().getServer();
        player.setItemInHand(InteractionHand.MAIN_HAND, new ItemStack(Items.DIAMOND_SWORD));
        String profileId = "black_arcana:test_ephemeral_echo";
        helper.assertTrue(MinecraftEchoArmamentRuntime.rememberHeldWeapon(server, player.getUUID(), profileId)
                .decision().allowed(),
            "test profile must be remembered before manifestation");

        int itemEntitiesBefore = helper.getLevel().getEntitiesOfClass(
            ItemEntity.class, player.getBoundingBox().inflate(8.0D)).size();
        int heldCountBefore = player.getMainHandItem().getCount();
        long nowTick = server.getTickCount();

        var manifested = MinecraftEchoArmamentRuntime.manifest(
            server, player.getUUID(), profileId, nowTick, 5L);

        helper.assertTrue(manifested.decision().allowed(), "remembered profile must manifest ephemerally");
        helper.assertTrue(manifested.manifestation().isPresent(), "successful manifestation must return a handle");
        helper.assertTrue(MinecraftEchoArmamentRuntime.activeEchoes(server, player.getUUID()) == 1,
            "manifestation must consume exactly one bounded echo slot");
        helper.assertTrue(player.getMainHandItem().getCount() == heldCountBefore,
            "manifestation must not consume or duplicate the source stack");
        helper.assertTrue(helper.getLevel().getEntitiesOfClass(
                ItemEntity.class, player.getBoundingBox().inflate(8.0D)).size() == itemEntitiesBefore,
            "manifestation must not create a persistent/drop-capable ItemEntity");

        MinecraftEchoArmamentRuntime.tick(server, nowTick + 5L);
        helper.assertTrue(MinecraftEchoArmamentRuntime.activeEchoes(server, player.getUUID()) == 0,
            "expired echo must release its budget slot");
        helper.succeed();
    }

    @SuppressWarnings("removal")
    @GameTest(template = "foundation_empty", timeoutTicks = 80)
    public static void ownerLogoutCleansManifestationsAndReleasesBudget(GameTestHelper helper) {
        var player = helper.makeMockServerPlayerInLevel();
        var server = helper.getLevel().getServer();
        player.setItemInHand(InteractionHand.MAIN_HAND, new ItemStack(Items.IRON_SWORD));
        String profileId = "black_arcana:test_logout_echo";
        helper.assertTrue(MinecraftEchoArmamentRuntime.rememberHeldWeapon(server, player.getUUID(), profileId)
                .decision().allowed(),
            "test profile must be remembered before manifestation");
        long nowTick = server.getTickCount();
        helper.assertTrue(MinecraftEchoArmamentRuntime.manifest(
                server, player.getUUID(), profileId, nowTick, 200L).decision().allowed(),
            "test echo must manifest before logout cleanup");
        helper.assertTrue(MinecraftEchoArmamentRuntime.activeEchoes(server, player.getUUID()) == 1,
            "test must begin with one active echo");

        MinecraftEchoArmamentRuntime.onPlayerLoggedOut(new PlayerEvent.PlayerLoggedOutEvent(player));

        helper.assertTrue(MinecraftEchoArmamentRuntime.activeEchoes(server, player.getUUID()) == 0,
            "logout must atomically remove owner echoes and release budget");
        helper.succeed();
    }

    @SuppressWarnings("removal")
    @GameTest(template = "foundation_empty", timeoutTicks = 80)
    public static void activeEchoBudgetRejectsFortyNinthManifestation(GameTestHelper helper) {
        var player = helper.makeMockServerPlayerInLevel();
        var server = helper.getLevel().getServer();
        player.setItemInHand(InteractionHand.MAIN_HAND, new ItemStack(Items.NETHERITE_SWORD));
        String profileId = "black_arcana:test_budget_echo";
        helper.assertTrue(MinecraftEchoArmamentRuntime.rememberHeldWeapon(server, player.getUUID(), profileId)
                .decision().allowed(),
            "test profile must be remembered before saturation");
        long nowTick = server.getTickCount();

        for (int index = 0; index < ProjectionSafetyCeilings.MAX_ACTIVE_ECHOES; index++) {
            helper.assertTrue(MinecraftEchoArmamentRuntime.manifest(
                    server, player.getUUID(), profileId, nowTick, 200L).decision().allowed(),
                "every echo up to the hard active cap must be admitted");
        }
        helper.assertTrue(MinecraftEchoArmamentRuntime.activeEchoes(server, player.getUUID())
                == ProjectionSafetyCeilings.MAX_ACTIVE_ECHOES,
            "active echo accounting must stop exactly at the hard cap");

        var overflow = MinecraftEchoArmamentRuntime.manifest(
            server, player.getUUID(), profileId, nowTick, 200L);
        helper.assertTrue(!overflow.decision().allowed(), "the 49th concurrent echo must fail closed");
        helper.assertTrue(overflow.decision().code().equals("echo_armament_active_capacity"),
            "overflow denial must use the stable active-capacity code");
        helper.assertTrue(overflow.manifestation().isEmpty(),
            "capacity denial must never return an untracked manifestation");

        MinecraftEchoArmamentRuntime.onPlayerLoggedOut(new PlayerEvent.PlayerLoggedOutEvent(player));
        helper.assertTrue(MinecraftEchoArmamentRuntime.activeEchoes(server, player.getUUID()) == 0,
            "cleanup after saturation must release every budget slot");
        helper.succeed();
    }
}
