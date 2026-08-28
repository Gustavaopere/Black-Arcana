package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntime;
import dev.gustavopere.blackarcana.core.world.TemporaryMutationKey;
import dev.gustavopere.blackarcana.persistence.BlackArcanaSavedData;
import net.minecraft.core.BlockPos;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.world.level.block.Blocks;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;

import java.util.UUID;

@GameTestHolder(BlackArcanaMod.MOD_ID)
@PrefixGameTestTemplate(false)
public final class WorldSafetyPersistenceGameTests {
    private WorldSafetyPersistenceGameTests() { }

    @GameTest(template = "foundation_empty", timeoutTicks = 40)
    public static void temporaryRollbackRecordSurvivesSavedDataRoundTrip(GameTestHelper helper) {
        ArcanaServerRuntime source = ArcanaServerRuntime.createDefault();
        long now = helper.getLevel().getGameTime();
        BlockPos absolute = helper.absolutePos(new BlockPos(1, 2, 1));
        TemporaryMutationKey key = new TemporaryMutationKey(
            helper.getLevel().dimension().location().toString(),
            absolute.asLong());
        String original = MinecraftTemporaryBlockBackend.encodeState(Blocks.STONE.defaultBlockState());
        String replacement = MinecraftTemporaryBlockBackend.encodeState(Blocks.OBSIDIAN.defaultBlockState());
        UUID owner = UUID.fromString("33333333-3333-3333-3333-333333333333");
        ArcanaCastId castId = ArcanaCastId.parse("44444444-4444-4444-4444-444444444444");

        var registration = source.temporaryMutations().register(
            key,
            owner,
            castId,
            original,
            replacement,
            now + 100L);
        helper.assertTrue(registration.decision().allowed(), "source rollback record must register");

        BlackArcanaSavedData data = new BlackArcanaSavedData();
        data.capture(
            source.cooldowns(),
            source.charges(),
            source.loadouts(),
            source.temporaryMutations(),
            now);
        CompoundTag encoded = data.save(new CompoundTag(), helper.getLevel().registryAccess());
        BlackArcanaSavedData decoded = BlackArcanaSavedData.load(encoded, helper.getLevel().registryAccess());

        ArcanaServerRuntime restored = ArcanaServerRuntime.createDefault();
        decoded.restore(
            restored.cooldowns(),
            restored.charges(),
            restored.loadouts(),
            restored.temporaryMutations(),
            now);

        helper.assertTrue(restored.temporaryMutations().size() == 1, "rollback record must survive NBT round-trip");
        var mutation = restored.temporaryMutations().snapshot().getFirst();
        helper.assertTrue(mutation.key().equals(key), "dimension and block position must survive restart state");
        helper.assertTrue(mutation.ownerId().equals(owner), "temporary mutation owner must survive restart state");
        helper.assertTrue(mutation.castId().equals(castId), "temporary mutation cast id must survive restart state");
        helper.assertTrue(mutation.originalState().equals(original), "original block state must survive restart state");
        helper.assertTrue(mutation.replacementState().equals(replacement), "replacement block state must survive restart state");
        helper.assertTrue(mutation.expiresAtTick() == now + 100L, "expiry must survive restart state");
        helper.succeed();
    }
}
