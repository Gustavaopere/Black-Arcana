package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
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

import java.lang.reflect.Method;
import java.util.Optional;
import java.util.UUID;

@GameTestHolder(BlackArcanaMod.MOD_ID)
@PrefixGameTestTemplate(false)
public final class EchoArmamentGameTests {
    private static final String RUNTIME =
        "dev.gustavopere.blackarcana.integration.neoforge.MinecraftEchoArmamentRuntime";

    private EchoArmamentGameTests() { }

    @SuppressWarnings("removal")
    @GameTest(template = "foundation_empty", timeoutTicks = 80)
    public static void heldWeaponBecomesSanitizedProfileWithoutMutatingSource(GameTestHelper helper) throws Exception {
        var player = helper.makeMockServerPlayerInLevel();
        var server = helper.getLevel().getServer();
        ItemStack source = new ItemStack(Items.DIAMOND_SWORD);
        source.set(DataComponents.CUSTOM_NAME, Component.literal("Private Blade Name"));
        player.setItemInHand(InteractionHand.MAIN_HAND, source);

        Object result = rememberHeldWeapon(server, player.getUUID(), "black_arcana:test_echo_blade");

        helper.assertTrue(decision(result).allowed(), "eligible held weapon must be rememberable");
        ProjectedWeaponProfile profile = resultProfile(result).orElseThrow();
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
        helper.assertTrue(findProfile(server, player.getUUID(), "black_arcana:test_echo_blade").isPresent(),
            "sanitized profile must be stored in bounded server memory");
        helper.succeed();
    }

    @SuppressWarnings("removal")
    @GameTest(template = "foundation_empty", timeoutTicks = 80)
    public static void unsupportedContainerItemIsRejectedWithoutMemoryEntry(GameTestHelper helper) throws Exception {
        var player = helper.makeMockServerPlayerInLevel();
        var server = helper.getLevel().getServer();
        player.setItemInHand(InteractionHand.MAIN_HAND, new ItemStack(Items.CHEST));

        Object result = rememberHeldWeapon(server, player.getUUID(), "black_arcana:test_bad_echo");

        helper.assertTrue(!decision(result).allowed(), "ordinary storage item must not become a weapon echo profile");
        helper.assertTrue(decision(result).code().equals("echo_armament_unsupported_item"),
            "unsupported item denial must be explicit and stable");
        helper.assertTrue(resultProfile(result).isEmpty(), "denied capture must not return a profile");
        helper.assertTrue(findProfile(server, player.getUUID(), "black_arcana:test_bad_echo").isEmpty(),
            "denied capture must not create registry state");
        helper.succeed();
    }

    @SuppressWarnings("removal")
    @GameTest(template = "foundation_empty", timeoutTicks = 80)
    public static void manifestationIsServerOnlyAndExpiresWithoutCreatingItemEntity(GameTestHelper helper) throws Exception {
        var player = helper.makeMockServerPlayerInLevel();
        var server = helper.getLevel().getServer();
        player.setItemInHand(InteractionHand.MAIN_HAND, new ItemStack(Items.DIAMOND_SWORD));
        String profileId = "black_arcana:test_ephemeral_echo";
        helper.assertTrue(decision(rememberHeldWeapon(server, player.getUUID(), profileId)).allowed(),
            "test profile must be remembered before manifestation");

        int itemEntitiesBefore = helper.getLevel().getEntitiesOfClass(
            ItemEntity.class, player.getBoundingBox().inflate(8.0D)).size();
        int heldCountBefore = player.getMainHandItem().getCount();
        long nowTick = server.getTickCount();

        Object manifested = manifest(server, player.getUUID(), profileId, nowTick, 5L);

        helper.assertTrue(decision(manifested).allowed(), "remembered profile must manifest ephemerally");
        helper.assertTrue(resultManifestation(manifested).isPresent(), "successful manifestation must return a handle");
        helper.assertTrue(activeEchoes(server, player.getUUID()) == 1,
            "manifestation must consume exactly one bounded echo slot");
        helper.assertTrue(player.getMainHandItem().getCount() == heldCountBefore,
            "manifestation must not consume or duplicate the source stack");
        helper.assertTrue(helper.getLevel().getEntitiesOfClass(
                ItemEntity.class, player.getBoundingBox().inflate(8.0D)).size() == itemEntitiesBefore,
            "manifestation must not create a persistent/drop-capable ItemEntity");

        tick(server, nowTick + 5L);
        helper.assertTrue(activeEchoes(server, player.getUUID()) == 0,
            "expired echo must release its budget slot");
        helper.succeed();
    }

    @SuppressWarnings("removal")
    @GameTest(template = "foundation_empty", timeoutTicks = 80)
    public static void ownerLogoutCleansManifestationsAndReleasesBudget(GameTestHelper helper) throws Exception {
        var player = helper.makeMockServerPlayerInLevel();
        var server = helper.getLevel().getServer();
        player.setItemInHand(InteractionHand.MAIN_HAND, new ItemStack(Items.IRON_SWORD));
        String profileId = "black_arcana:test_logout_echo";
        helper.assertTrue(decision(rememberHeldWeapon(server, player.getUUID(), profileId)).allowed(),
            "test profile must be remembered before manifestation");
        long nowTick = server.getTickCount();
        helper.assertTrue(decision(manifest(server, player.getUUID(), profileId, nowTick, 200L)).allowed(),
            "test echo must manifest before logout cleanup");
        helper.assertTrue(activeEchoes(server, player.getUUID()) == 1,
            "test must begin with one active echo");

        onPlayerLoggedOut(new PlayerEvent.PlayerLoggedOutEvent(player));

        helper.assertTrue(activeEchoes(server, player.getUUID()) == 0,
            "logout must atomically remove owner echoes and release budget");
        helper.succeed();
    }

    @SuppressWarnings("removal")
    @GameTest(template = "foundation_empty", timeoutTicks = 80)
    public static void activeEchoBudgetRejectsFortyNinthManifestation(GameTestHelper helper) throws Exception {
        var player = helper.makeMockServerPlayerInLevel();
        var server = helper.getLevel().getServer();
        player.setItemInHand(InteractionHand.MAIN_HAND, new ItemStack(Items.NETHERITE_SWORD));
        String profileId = "black_arcana:test_budget_echo";
        helper.assertTrue(decision(rememberHeldWeapon(server, player.getUUID(), profileId)).allowed(),
            "test profile must be remembered before saturation");
        long nowTick = server.getTickCount();

        for (int index = 0; index < ProjectionSafetyCeilings.MAX_ACTIVE_ECHOES; index++) {
            helper.assertTrue(decision(manifest(server, player.getUUID(), profileId, nowTick, 200L)).allowed(),
                "every echo up to the hard active cap must be admitted");
        }
        helper.assertTrue(activeEchoes(server, player.getUUID()) == ProjectionSafetyCeilings.MAX_ACTIVE_ECHOES,
            "active echo accounting must stop exactly at the hard cap");

        Object overflow = manifest(server, player.getUUID(), profileId, nowTick, 200L);
        helper.assertTrue(!decision(overflow).allowed(), "the 49th concurrent echo must fail closed");
        helper.assertTrue(decision(overflow).code().equals("echo_armament_active_capacity"),
            "overflow denial must use the stable active-capacity code");
        helper.assertTrue(resultManifestation(overflow).isEmpty(),
            "capacity denial must never return an untracked manifestation");

        onPlayerLoggedOut(new PlayerEvent.PlayerLoggedOutEvent(player));
        helper.assertTrue(activeEchoes(server, player.getUUID()) == 0,
            "cleanup after saturation must release every budget slot");
        helper.succeed();
    }

    private static Object rememberHeldWeapon(net.minecraft.server.MinecraftServer server, UUID ownerId, String profileId)
        throws Exception {
        Class<?> runtime = Class.forName(RUNTIME);
        return runtime.getMethod("rememberHeldWeapon", net.minecraft.server.MinecraftServer.class, UUID.class, String.class)
            .invoke(null, server, ownerId, profileId);
    }

    private static Optional<ProjectedWeaponProfile> findProfile(
        net.minecraft.server.MinecraftServer server, UUID ownerId, String profileId) throws Exception {
        Class<?> runtime = Class.forName(RUNTIME);
        Object value = runtime.getMethod("findProfile", net.minecraft.server.MinecraftServer.class, UUID.class, String.class)
            .invoke(null, server, ownerId, profileId);
        @SuppressWarnings("unchecked")
        Optional<ProjectedWeaponProfile> profile = (Optional<ProjectedWeaponProfile>) value;
        return profile;
    }

    private static Object manifest(
        net.minecraft.server.MinecraftServer server, UUID ownerId, String profileId, long nowTick, long lifetimeTicks)
        throws Exception {
        Class<?> runtime = Class.forName(RUNTIME);
        return runtime.getMethod(
                "manifest", net.minecraft.server.MinecraftServer.class, UUID.class, String.class, long.class, long.class)
            .invoke(null, server, ownerId, profileId, nowTick, lifetimeTicks);
    }

    private static int activeEchoes(net.minecraft.server.MinecraftServer server, UUID ownerId) throws Exception {
        Class<?> runtime = Class.forName(RUNTIME);
        return (int) runtime.getMethod("activeEchoes", net.minecraft.server.MinecraftServer.class, UUID.class)
            .invoke(null, server, ownerId);
    }

    private static void tick(net.minecraft.server.MinecraftServer server, long nowTick) throws Exception {
        Class<?> runtime = Class.forName(RUNTIME);
        runtime.getMethod("tick", net.minecraft.server.MinecraftServer.class, long.class).invoke(null, server, nowTick);
    }

    private static void onPlayerLoggedOut(PlayerEvent.PlayerLoggedOutEvent event) throws Exception {
        Class<?> runtime = Class.forName(RUNTIME);
        Method method = runtime.getDeclaredMethod("onPlayerLoggedOut", PlayerEvent.PlayerLoggedOutEvent.class);
        method.setAccessible(true);
        method.invoke(null, event);
    }

    private static ArcanaDecision decision(Object result) throws Exception {
        return (ArcanaDecision) result.getClass().getMethod("decision").invoke(result);
    }

    private static Optional<ProjectedWeaponProfile> resultProfile(Object result) throws Exception {
        @SuppressWarnings("unchecked")
        Optional<ProjectedWeaponProfile> profile =
            (Optional<ProjectedWeaponProfile>) result.getClass().getMethod("profile").invoke(result);
        return profile;
    }

    private static Optional<?> resultManifestation(Object result) throws Exception {
        return (Optional<?>) result.getClass().getMethod("manifestation").invoke(result);
    }
}
