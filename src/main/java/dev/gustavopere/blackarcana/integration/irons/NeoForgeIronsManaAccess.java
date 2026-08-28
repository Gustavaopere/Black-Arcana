package dev.gustavopere.blackarcana.integration.irons;

import dev.gustavopere.blackarcana.api.ArcanaDecision;
import io.redspace.ironsspellbooks.api.magic.MagicData;
import io.redspace.ironsspellbooks.api.registry.AttributeRegistry;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerPlayer;
import net.neoforged.neoforge.network.PacketDistributor;

import java.lang.reflect.Constructor;
import java.lang.reflect.InvocationTargetException;
import java.util.Objects;
import java.util.UUID;

/** Iron's 3.16.x server mana adapter. Internal packet usage is reflection-isolated. */
public final class NeoForgeIronsManaAccess implements IronsManaAccess {
    private static final String SYNC_PACKET = "io.redspace.ironsspellbooks.network.SyncManaPacket";
    private static final float EPSILON = 0.001F;

    private final MinecraftServer server;
    private final Constructor<?> syncPacketConstructor;

    private NeoForgeIronsManaAccess(MinecraftServer server, Constructor<?> syncPacketConstructor) {
        this.server = Objects.requireNonNull(server, "server");
        this.syncPacketConstructor = Objects.requireNonNull(syncPacketConstructor, "syncPacketConstructor");
    }

    public static NeoForgeIronsManaAccess probe(MinecraftServer server) throws ReflectiveOperationException {
        Objects.requireNonNull(server, "server");
        Class<?> packetClass = Class.forName(SYNC_PACKET, false, NeoForgeIronsManaAccess.class.getClassLoader());
        Constructor<?> constructor = packetClass.getConstructor(MagicData.class);
        if (!CustomPacketPayload.class.isAssignableFrom(packetClass)) {
            throw new NoSuchMethodException("Iron's SyncManaPacket no longer implements CustomPacketPayload");
        }
        return new NeoForgeIronsManaAccess(server, constructor);
    }

    @Override
    public IronsManaSnapshot snapshot(UUID playerId) {
        ServerPlayer player = requirePlayer(playerId);
        MagicData data = MagicData.getPlayerMagicData(player);
        float current = data.getMana();
        float maximum = (float) player.getAttributeValue(AttributeRegistry.MAX_MANA);
        return new IronsManaSnapshot(current, Math.max(0.0F, maximum));
    }

    @Override
    public ArcanaDecision adjust(UUID playerId, float delta) {
        if (!Float.isFinite(delta)) {
            return ArcanaDecision.deny("irons_mana_delta_invalid", "Iron's mana delta must be finite");
        }

        ServerPlayer player;
        try {
            player = requirePlayer(playerId);
        } catch (RuntimeException failure) {
            return ArcanaDecision.deny("irons_player_unavailable", failure.getMessage());
        }

        MagicData data = MagicData.getPlayerMagicData(player);
        float before = data.getMana();
        float maximum = Math.max(0.0F, (float) player.getAttributeValue(AttributeRegistry.MAX_MANA));
        double rawTarget = (double) before + delta;
        if (rawTarget < -EPSILON) {
            return ArcanaDecision.deny("insufficient_irons_mana", "Iron's mana changed before reservation");
        }
        float target = (float) Math.max(0.0D, Math.min(maximum, rawTarget));

        data.setMana(target);
        float after = data.getMana();
        if (Math.abs(after - target) > EPSILON) {
            data.setMana(before);
            syncBestEffort(player, data);
            return ArcanaDecision.deny(
                "irons_mana_adjustment_modified",
                "Another Iron's mana hook modified or canceled the requested adjustment");
        }

        ArcanaDecision sync = sync(player, data);
        if (sync.allowed()) return sync;

        data.setMana(before);
        syncBestEffort(player, data);
        return sync;
    }

    private ServerPlayer requirePlayer(UUID playerId) {
        Objects.requireNonNull(playerId, "playerId");
        ServerPlayer player = server.getPlayerList().getPlayer(playerId);
        if (player == null) throw new IllegalStateException("player is not online on this server");
        return player;
    }

    private ArcanaDecision sync(ServerPlayer player, MagicData data) {
        try {
            Object rawPacket = syncPacketConstructor.newInstance(data);
            if (!(rawPacket instanceof CustomPacketPayload payload)) {
                return ArcanaDecision.deny(
                    "irons_mana_sync_incompatible",
                    "Iron's mana sync packet no longer implements CustomPacketPayload");
            }
            PacketDistributor.sendToPlayer(player, payload);
            return ArcanaDecision.allow();
        } catch (InstantiationException | IllegalAccessException | InvocationTargetException | RuntimeException failure) {
            return ArcanaDecision.deny(
                "irons_mana_sync_failed",
                "Iron's mana synchronization failed: " + failure.getClass().getSimpleName());
        }
    }

    private void syncBestEffort(ServerPlayer player, MagicData data) {
        sync(player, data);
    }
}
