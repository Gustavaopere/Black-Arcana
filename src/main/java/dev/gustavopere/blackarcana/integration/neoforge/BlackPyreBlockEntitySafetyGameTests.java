package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import dev.gustavopere.blackarcana.core.world.TemporaryMutationKey;
import net.minecraft.core.BlockPos;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.entity.ChestBlockEntity;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;

@GameTestHolder(BlackArcanaMod.MOD_ID)
@PrefixGameTestTemplate(false)
public final class BlackPyreBlockEntitySafetyGameTests {
    private BlackPyreBlockEntitySafetyGameTests() { }

    @GameTest(template = "foundation_empty", timeoutTicks = 100)
    public static void minecraftMutationBackendRejectsBlockEntityWithoutLosingInventory(GameTestHelper helper) {
        BlockPos pos = helper.absolutePos(new BlockPos(2, 1, 2));
        helper.getLevel().setBlock(pos, Blocks.CHEST.defaultBlockState(), Block.UPDATE_ALL);
        ChestBlockEntity chest = (ChestBlockEntity) helper.getLevel().getBlockEntity(pos);
        helper.assertTrue(chest != null, "test fixture must create a chest block entity");
        chest.setItem(0, new ItemStack(Items.DIAMOND, 3));
        chest.setChanged();

        MinecraftTemporaryBlockBackend backend = new MinecraftTemporaryBlockBackend(helper.getLevel().getServer());
        TemporaryMutationKey key = new TemporaryMutationKey(
            helper.getLevel().dimension().location().toString(),
            pos.asLong());
        String expected = backend.readLoadedState(key).orElseThrow();
        boolean replaced = backend.replaceIfCurrent(
            key,
            expected,
            MinecraftTemporaryBlockBackend.encodeState(Blocks.BLACKSTONE.defaultBlockState()));

        helper.assertTrue(!replaced, "world mutation backend must fail closed for block-entity targets");
        helper.assertTrue(helper.getLevel().getBlockState(pos).is(Blocks.CHEST),
            "failed mutation must leave the chest block intact");
        ChestBlockEntity after = (ChestBlockEntity) helper.getLevel().getBlockEntity(pos);
        helper.assertTrue(after != null && after.getItem(0).is(Items.DIAMOND) && after.getItem(0).getCount() == 3,
            "failed mutation must preserve block-entity inventory/NBT");
        helper.succeed();
    }

    @GameTest(template = "foundation_empty", timeoutTicks = 100)
    public static void minecraftMutationBackendRejectsUnbreakableTerrain(GameTestHelper helper) {
        BlockPos pos = helper.absolutePos(new BlockPos(4, 1, 2));
        helper.getLevel().setBlock(pos, Blocks.BEDROCK.defaultBlockState(), Block.UPDATE_ALL);

        MinecraftTemporaryBlockBackend backend = new MinecraftTemporaryBlockBackend(helper.getLevel().getServer());
        TemporaryMutationKey key = new TemporaryMutationKey(
            helper.getLevel().dimension().location().toString(),
            pos.asLong());
        String expected = backend.readLoadedState(key).orElseThrow();
        boolean replaced = backend.replaceIfCurrent(
            key,
            expected,
            MinecraftTemporaryBlockBackend.encodeState(Blocks.BLACKSTONE.defaultBlockState()));

        helper.assertTrue(!replaced, "world mutation backend must fail closed for unbreakable terrain");
        helper.assertTrue(helper.getLevel().getBlockState(pos).is(Blocks.BEDROCK),
            "failed mutation must preserve unbreakable terrain");
        helper.succeed();
    }
}
