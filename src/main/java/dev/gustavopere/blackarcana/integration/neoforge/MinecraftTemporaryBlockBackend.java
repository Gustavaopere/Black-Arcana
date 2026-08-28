package dev.gustavopere.blackarcana.integration.neoforge;

import com.mojang.brigadier.exceptions.CommandSyntaxException;
import dev.gustavopere.blackarcana.core.world.ChunkRef;
import dev.gustavopere.blackarcana.core.world.LoadedChunkGuard;
import dev.gustavopere.blackarcana.core.world.TemporaryBlockBackend;
import dev.gustavopere.blackarcana.core.world.TemporaryMutationKey;
import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.Registries;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.nbt.NbtUtils;
import net.minecraft.nbt.TagParser;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.BlockState;

import java.util.Objects;
import java.util.Optional;

/**
 * NeoForge/Minecraft adapter for Black Arcana temporary block lifecycle.
 *
 * Invariants:
 * - resolves only already-loaded chunks via getChunkNow;
 * - never acquires chunk tickets or asks Minecraft to generate/load a chunk;
 * - rejects block-entity states so inventories and arbitrary BE NBT are not lost;
 * - applies compare-and-set writes with drops suppressed.
 */
public final class MinecraftTemporaryBlockBackend
    implements TemporaryBlockBackend, LoadedChunkGuard.LoadedChunkProbe {

    private static final int UPDATE_FLAGS = Block.UPDATE_ALL | Block.UPDATE_SUPPRESS_DROPS;

    private final MinecraftServer server;

    public MinecraftTemporaryBlockBackend(MinecraftServer server) {
        this.server = Objects.requireNonNull(server, "server");
    }

    @Override
    public Optional<String> readLoadedState(TemporaryMutationKey key) {
        Objects.requireNonNull(key, "key");
        ServerLevel level = level(key.dimensionId());
        if (level == null) return Optional.empty();
        BlockPos pos = BlockPos.of(key.packedBlockPos());
        if (!isLoaded(level, pos)) return Optional.empty();
        return Optional.of(encodeState(level.getBlockState(pos)));
    }

    @Override
    public boolean replaceIfCurrent(
        TemporaryMutationKey key,
        String expectedState,
        String replacementState
    ) {
        Objects.requireNonNull(key, "key");
        Objects.requireNonNull(expectedState, "expectedState");
        Objects.requireNonNull(replacementState, "replacementState");

        ServerLevel level = level(key.dimensionId());
        if (level == null) return false;
        BlockPos pos = BlockPos.of(key.packedBlockPos());
        if (!isLoaded(level, pos)) return false;

        BlockState current = level.getBlockState(pos);
        if (!encodeState(current).equals(expectedState)) return false;

        BlockState replacement = decodeState(level, replacementState);
        if (current.hasBlockEntity() || replacement.hasBlockEntity()) return false;

        return level.setBlock(pos, replacement, UPDATE_FLAGS);
    }

    @Override
    public boolean isLoaded(ChunkRef chunk) {
        Objects.requireNonNull(chunk, "chunk");
        ServerLevel level = level(chunk.dimensionId());
        return level != null && level.getChunkSource().getChunkNow(chunk.chunkX(), chunk.chunkZ()) != null;
    }

    static String encodeState(BlockState state) {
        return NbtUtils.writeBlockState(Objects.requireNonNull(state, "state")).toString();
    }

    static BlockState decodeState(ServerLevel level, String encoded) {
        Objects.requireNonNull(level, "level");
        Objects.requireNonNull(encoded, "encoded");
        final CompoundTag tag;
        try {
            tag = TagParser.parseTag(encoded);
        } catch (CommandSyntaxException failure) {
            throw new IllegalArgumentException("invalid persisted block state", failure);
        }
        return NbtUtils.readBlockState(
            level.registryAccess().lookupOrThrow(Registries.BLOCK),
            tag);
    }

    private ServerLevel level(String dimensionId) {
        ResourceLocation location = ResourceLocation.tryParse(dimensionId);
        if (location == null) return null;
        ResourceKey<Level> key = ResourceKey.create(Registries.DIMENSION, location);
        return server.getLevel(key);
    }

    private static boolean isLoaded(ServerLevel level, BlockPos pos) {
        return level.getChunkSource().getChunkNow(pos.getX() >> 4, pos.getZ() >> 4) != null;
    }
}
