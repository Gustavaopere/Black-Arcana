package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.core.ritual.RitualAnchor;
import dev.gustavopere.blackarcana.core.ritual.RitualResult;
import dev.gustavopere.blackarcana.core.ritual.VeilAnchorActivationService;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntime;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntimeManager;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.event.entity.player.PlayerInteractEvent;

import java.util.Objects;
import java.util.function.Function;

/**
 * Player-facing Veil Anchor: sneak + main-hand Echo Shard on the center Crying Obsidian.
 * The surrounding 3x3 altar is player-built with four Amethyst Blocks at the cardinals
 * and four Soul Sand blocks on the diagonals. No debug command or world mutation.
 */
public final class MinecraftVeilAnchorConsecrationRuntime {
    private static final double MAX_DISTANCE_SQUARED = 36.0D;

    private MinecraftVeilAnchorConsecrationRuntime() { }

    public static void register(IEventBus bus) {
        Objects.requireNonNull(bus, "bus");
        bus.addListener(MinecraftVeilAnchorConsecrationRuntime::onRightClickBlock);
    }

    private static void onRightClickBlock(PlayerInteractEvent.RightClickBlock event) {
        if (event.getHand() != InteractionHand.MAIN_HAND
                || !event.getEntity().isShiftKeyDown()
                || !event.getItemStack().is(Items.ECHO_SHARD)
                || !event.getLevel().getBlockState(event.getPos()).is(Blocks.CRYING_OBSIDIAN)) {
            return;
        }

        // Match the client/server interaction pipeline. Only the server makes decisions.
        event.setCanceled(true);
        event.setCancellationResult(InteractionResult.SUCCESS);
        if (!(event.getLevel() instanceof ServerLevel level)
                || !(event.getEntity() instanceof ServerPlayer player)) {
            return;
        }

        BlockPos center = event.getPos();
        if (!isPermitted(level, player, center) || !isValidAnchor(level, center)) {
            player.displayClientMessage(Component.translatable(
                    "ritual.black_arcana.veil_anchor.denied", "grand_ritual_anchor_invalid"), true);
            return;
        }

        ArcanaServerRuntime runtime = ArcanaServerRuntimeManager.get(level.getServer()).orElse(null);
        if (runtime == null) {
            player.displayClientMessage(Component.translatable(
                    "ritual.black_arcana.veil_anchor.denied", "server_runtime_unavailable"), true);
            return;
        }
        long nowTick = level.getServer().overworld().getGameTime();
        RitualAnchor anchor = new RitualAnchor(
                level.dimension().location().toString(), center.asLong());
        RitualResult result = VeilAnchorActivationService.start(runtime, player.getUUID(), anchor, nowTick);
        if (result.status() == RitualResult.Status.STARTED) {
            player.displayClientMessage(Component.translatable(
                    "ritual.black_arcana.veil_anchor.started"), true);
        } else {
            player.displayClientMessage(Component.translatable(
                    "ritual.black_arcana.veil_anchor.denied", result.code()), true);
        }
    }

    /** Server-only permission gate; re-used by the Malum requirement binding at commit/completion. */
    public static boolean isPermitted(ServerLevel level, ServerPlayer player, BlockPos center) {
        return player.serverLevel() == level
                && player.isAlive()
                && !player.isSpectator()
                && player.distanceToSqr(center.getX() + 0.5D,
                        center.getY() + 0.5D, center.getZ() + 0.5D) <= MAX_DISTANCE_SQUARED
                && level.mayInteract(player, center)
                && player.mayUseItemAt(center, Direction.UP, player.getMainHandItem());
    }

    /** Never force-load the chunk of an altar cell while checking its shape. */
    public static boolean isValidAnchor(ServerLevel level, BlockPos center) {
        return matchesLayout(center, cell -> {
            if (!level.getWorldBorder().isWithinBounds(cell)
                    || level.getChunkSource().getChunkNow(cell.getX() >> 4, cell.getZ() >> 4) == null) {
                return null;
            }
            return level.getBlockState(cell).getBlock();
        });
    }

    /** Bounded, side-effect-free pattern check for deterministic tests. */
    public static boolean matchesLayout(BlockPos center, Function<BlockPos, Block> blockAt) {
        Objects.requireNonNull(center, "center");
        Objects.requireNonNull(blockAt, "blockAt");
        if (blockAt.apply(center) != Blocks.CRYING_OBSIDIAN) return false;
        for (Direction side : Direction.Plane.HORIZONTAL) {
            if (blockAt.apply(center.relative(side)) != Blocks.AMETHYST_BLOCK) return false;
        }
        return blockAt.apply(center.offset(1, 0, 1)) == Blocks.SOUL_SAND
                && blockAt.apply(center.offset(1, 0, -1)) == Blocks.SOUL_SAND
                && blockAt.apply(center.offset(-1, 0, 1)) == Blocks.SOUL_SAND
                && blockAt.apply(center.offset(-1, 0, -1)) == Blocks.SOUL_SAND;
    }
}
