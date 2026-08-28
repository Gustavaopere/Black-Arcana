package dev.gustavopere.blackarcana.integration.ars;

import com.hollingsworth.arsnouveau.api.mana.IManaCap;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.LivingEntity;

import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.Objects;
import java.util.UUID;

/** Ars Nouveau 5.13.x mana adapter using only IManaCap as a compiled provider contract. */
public final class NeoForgeArsManaAccess implements ArsManaAccess {
    private static final String CAPABILITY_REGISTRY = "com.hollingsworth.arsnouveau.setup.registry.CapabilityRegistry";
    private static final String MANA_CAP = "com.hollingsworth.arsnouveau.common.capability.ManaCap";
    private static final double EPSILON = 0.000001D;

    private final MinecraftServer server;
    private final Method getMana;
    private final Method syncToClient;

    private NeoForgeArsManaAccess(MinecraftServer server, Method getMana, Method syncToClient) {
        this.server = Objects.requireNonNull(server, "server");
        this.getMana = Objects.requireNonNull(getMana, "getMana");
        this.syncToClient = Objects.requireNonNull(syncToClient, "syncToClient");
    }

    public static NeoForgeArsManaAccess probe(MinecraftServer server) throws ReflectiveOperationException {
        Objects.requireNonNull(server, "server");
        ClassLoader loader = NeoForgeArsManaAccess.class.getClassLoader();
        Class<?> registry = Class.forName(CAPABILITY_REGISTRY, false, loader);
        Class<?> concreteMana = Class.forName(MANA_CAP, false, loader);
        if (!IManaCap.class.isAssignableFrom(concreteMana)) {
            throw new NoSuchMethodException("Ars ManaCap no longer implements IManaCap");
        }
        Method getMana = registry.getMethod("getMana", LivingEntity.class);
        Method sync = concreteMana.getMethod("syncToClient", ServerPlayer.class);
        return new NeoForgeArsManaAccess(server, getMana, sync);
    }

    @Override
    public ArsManaSnapshot snapshot(UUID playerId) {
        ServerPlayer player = requirePlayer(playerId);
        ManaHandle handle = requireMana(player);
        return new ArsManaSnapshot(handle.cap().getCurrentMana(), handle.cap().getMaxMana());
    }

    @Override
    public ArcanaDecision adjust(UUID playerId, double delta) {
        if (!Double.isFinite(delta)) {
            return ArcanaDecision.deny("ars_mana_delta_invalid", "Ars mana delta must be finite");
        }

        ServerPlayer player;
        ManaHandle handle;
        try {
            player = requirePlayer(playerId);
            handle = requireMana(player);
        } catch (RuntimeException failure) {
            return ArcanaDecision.deny("ars_mana_unavailable", failure.getMessage());
        }

        IManaCap cap = handle.cap();
        double before = cap.getCurrentMana();
        double maximum = Math.max(0.0D, cap.getMaxMana());
        double rawTarget = before + delta;
        if (rawTarget < -EPSILON) {
            return ArcanaDecision.deny("insufficient_ars_mana", "Ars mana changed before reservation");
        }
        double target = Math.max(0.0D, Math.min(maximum, rawTarget));
        double after = cap.setMana(target);
        if (!Double.isFinite(after) || Math.abs(after - target) > EPSILON) {
            cap.setMana(before);
            syncBestEffort(handle.raw(), player);
            return ArcanaDecision.deny(
                "ars_mana_adjustment_modified",
                "Ars mana capability did not accept the requested adjustment");
        }

        ArcanaDecision sync = sync(handle.raw(), player);
        if (sync.allowed()) return sync;

        cap.setMana(before);
        syncBestEffort(handle.raw(), player);
        return sync;
    }

    private ServerPlayer requirePlayer(UUID playerId) {
        Objects.requireNonNull(playerId, "playerId");
        ServerPlayer player = server.getPlayerList().getPlayer(playerId);
        if (player == null) throw new IllegalStateException("player is not online on this server");
        return player;
    }

    private ManaHandle requireMana(ServerPlayer player) {
        try {
            Object raw = getMana.invoke(null, player);
            if (!(raw instanceof IManaCap cap)) {
                throw new IllegalStateException("Ars mana capability is absent or incompatible for player");
            }
            return new ManaHandle(raw, cap);
        } catch (IllegalAccessException | InvocationTargetException failure) {
            throw new IllegalStateException("Ars mana capability query failed", failure);
        }
    }

    private ArcanaDecision sync(Object rawMana, ServerPlayer player) {
        try {
            syncToClient.invoke(rawMana, player);
            return ArcanaDecision.allow();
        } catch (IllegalAccessException | InvocationTargetException | RuntimeException failure) {
            return ArcanaDecision.deny(
                "ars_mana_sync_failed",
                "Ars mana synchronization failed: " + failure.getClass().getSimpleName());
        }
    }

    private void syncBestEffort(Object rawMana, ServerPlayer player) {
        sync(rawMana, player);
    }

    private record ManaHandle(Object raw, IManaCap cap) {
        private ManaHandle {
            Objects.requireNonNull(raw, "raw");
            Objects.requireNonNull(cap, "cap");
        }
    }
}
