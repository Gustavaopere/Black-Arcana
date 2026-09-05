package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import net.minecraft.core.BlockPos;
import net.minecraft.core.component.DataComponents;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.network.chat.Component;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.block.Blocks;
import net.neoforged.neoforge.common.damagesource.DamageContainer;
import net.neoforged.neoforge.event.entity.living.LivingDamageEvent;
import net.neoforged.neoforge.event.entity.player.PlayerEvent;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;

import java.lang.reflect.Method;
import java.util.UUID;

@GameTestHolder(BlackArcanaMod.MOD_ID)
@PrefixGameTestTemplate(false)
public final class EphemeralTemperingGameTests {
    private static final String RUNTIME =
        "dev.gustavopere.blackarcana.integration.neoforge.MinecraftEphemeralTemperingRuntime";

    private EphemeralTemperingGameTests() { }

    @SuppressWarnings("removal")
    @GameTest(template = "foundation_empty", timeoutTicks = 80)
    public static void meleeTemperingIsTemporaryBoundedAndNeverMutatesSourceComponents(GameTestHelper helper) throws Exception {
        var owner = helper.makeMockServerPlayerInLevel();
        var target = helper.spawnWithNoFreeWill(EntityType.COW, new BlockPos(3, 2, 1));
        var server = helper.getLevel().getServer();
        long nowTick = server.getTickCount();

        ItemStack source = new ItemStack(Items.DIAMOND_SWORD);
        source.set(DataComponents.CUSTOM_NAME, Component.literal("Lâmina Original"));
        owner.setItemInHand(InteractionHand.MAIN_HAND, source);
        ItemStack before = source.copy();

        Object applied = apply(server, owner.getUUID(), "MELEE_DAMAGE", 2.0D, nowTick, 5L, 1);
        helper.assertTrue(decision(applied).allowed(), "eligible melee weapon must accept a bounded temporary tempering overlay");
        helper.assertTrue(activeStacks(server, owner.getUUID()) == 1,
            "one admitted tempering must create exactly one active overlay stack");
        helper.assertTrue(ItemStack.isSameItemSameComponents(source, before),
            "applying Ephemeral Tempering must not mutate the held ItemStack components");

        LivingDamageEvent.Pre damage = new LivingDamageEvent.Pre(
            target,
            new DamageContainer(target.damageSources().playerAttack(owner), 3.0F));
        onLivingDamage(damage);
        helper.assertTrue(Math.abs(damage.getNewDamage() - 5.0F) < 0.001F,
            "MELEE_DAMAGE tempering must add its bounded overlay to vanilla player-attack final damage");

        Object overflow = apply(server, owner.getUUID(), "MELEE_DAMAGE", 2.0D, nowTick, 5L, 1);
        helper.assertTrue(!decision(overflow).allowed(), "configured one-stack tempering must reject a second stack");
        helper.assertTrue("ephemeral_tempering_stack_cap".equals(decision(overflow).code()),
            "stack-cap denial must expose a stable code");
        helper.assertTrue(activeStacks(server, owner.getUUID()) == 1,
            "denied stacking must leave active overlay accounting unchanged");

        tick(server, nowTick + 5L);
        helper.assertTrue(activeStacks(server, owner.getUUID()) == 0,
            "expired tempering overlay must be removed completely");
        LivingDamageEvent.Pre afterExpiry = new LivingDamageEvent.Pre(
            target,
            new DamageContainer(target.damageSources().playerAttack(owner), 3.0F));
        onLivingDamage(afterExpiry);
        helper.assertTrue(Math.abs(afterExpiry.getNewDamage() - 3.0F) < 0.001F,
            "expiry must restore unmodified melee damage behavior");
        helper.assertTrue(ItemStack.isSameItemSameComponents(source, before),
            "expiry/restoration must not require or leave any ItemStack component mutation");
        helper.succeed();
    }

    @SuppressWarnings("removal")
    @GameTest(template = "foundation_empty", timeoutTicks = 80)
    public static void miningTemperingFollowsExactHeldStackAndUnsupportedItemFailsClosed(GameTestHelper helper) throws Exception {
        var owner = helper.makeMockServerPlayerInLevel();
        var server = helper.getLevel().getServer();
        long nowTick = server.getTickCount();

        ItemStack tool = new ItemStack(Items.IRON_PICKAXE);
        owner.setItemInHand(InteractionHand.MAIN_HAND, tool);
        ItemStack before = tool.copy();

        Object applied = apply(server, owner.getUUID(), "MINING_SPEED", 1.5D, nowTick, 20L, 2);
        helper.assertTrue(decision(applied).allowed(), "eligible digging tool must accept MINING_SPEED tempering");
        PlayerEvent.BreakSpeed speed = new PlayerEvent.BreakSpeed(
            owner,
            Blocks.STONE.defaultBlockState(),
            2.0F,
            new BlockPos(0, 0, 0));
        onBreakSpeed(speed);
        helper.assertTrue(Math.abs(speed.getNewSpeed() - 3.0F) < 0.001F,
            "MINING_SPEED tempering must multiply the mutable NeoForge break-speed event");
        helper.assertTrue(ItemStack.isSameItemSameComponents(tool, before),
            "mining tempering must not encode temporary state into the tool stack");

        owner.setItemInHand(InteractionHand.MAIN_HAND, new ItemStack(Items.CHEST));
        PlayerEvent.BreakSpeed swapped = new PlayerEvent.BreakSpeed(
            owner,
            Blocks.STONE.defaultBlockState(),
            2.0F,
            new BlockPos(0, 0, 0));
        onBreakSpeed(swapped);
        helper.assertTrue(Math.abs(swapped.getNewSpeed() - 2.0F) < 0.001F,
            "tempering must not transfer to a replacement stack merely because the owner is the same");

        Object unsupported = apply(server, owner.getUUID(), "MINING_SPEED", 1.5D, nowTick, 20L, 2);
        helper.assertTrue(!decision(unsupported).allowed(), "ordinary container item must be rejected by Ephemeral Tempering");
        helper.assertTrue("ephemeral_tempering_unsupported_item".equals(decision(unsupported).code()),
            "unsupported-item denial must expose a stable code");
        helper.succeed();
    }

    private static Object apply(
        net.minecraft.server.MinecraftServer server,
        UUID ownerId,
        String mode,
        double magnitude,
        long nowTick,
        long lifetimeTicks,
        int maxStacks
    ) throws Exception {
        Class<?> runtime = Class.forName(RUNTIME);
        Method method = runtime.getMethod(
            "apply",
            net.minecraft.server.MinecraftServer.class,
            UUID.class,
            String.class,
            double.class,
            long.class,
            long.class,
            int.class);
        return method.invoke(null, server, ownerId, mode, magnitude, nowTick, lifetimeTicks, maxStacks);
    }

    private static int activeStacks(net.minecraft.server.MinecraftServer server, UUID ownerId) throws Exception {
        Class<?> runtime = Class.forName(RUNTIME);
        return (int) runtime.getMethod("activeStacks", net.minecraft.server.MinecraftServer.class, UUID.class)
            .invoke(null, server, ownerId);
    }

    private static void tick(net.minecraft.server.MinecraftServer server, long nowTick) throws Exception {
        Class<?> runtime = Class.forName(RUNTIME);
        runtime.getMethod("tick", net.minecraft.server.MinecraftServer.class, long.class).invoke(null, server, nowTick);
    }

    private static void onLivingDamage(LivingDamageEvent.Pre event) throws Exception {
        Class<?> runtime = Class.forName(RUNTIME);
        Method method = runtime.getDeclaredMethod("onLivingDamage", LivingDamageEvent.Pre.class);
        method.setAccessible(true);
        method.invoke(null, event);
    }

    private static void onBreakSpeed(PlayerEvent.BreakSpeed event) throws Exception {
        Class<?> runtime = Class.forName(RUNTIME);
        Method method = runtime.getDeclaredMethod("onBreakSpeed", PlayerEvent.BreakSpeed.class);
        method.setAccessible(true);
        method.invoke(null, event);
    }

    private static ArcanaDecision decision(Object result) throws Exception {
        return (ArcanaDecision) result.getClass().getMethod("decision").invoke(result);
    }
}
