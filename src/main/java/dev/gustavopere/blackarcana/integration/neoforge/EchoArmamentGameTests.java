package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import dev.gustavopere.blackarcana.content.projection.ProjectedWeaponProfile;
import dev.gustavopere.blackarcana.content.projection.ProjectionSafetyCeilings;
import net.minecraft.core.component.DataComponents;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.network.chat.Component;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
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
}
