package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.content.souls.SoulAnchorLedger;
import dev.gustavopere.blackarcana.persistence.SoulAnchorSavedData;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerPlayer;
import net.neoforged.bus.api.EventPriority;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.event.entity.living.LivingDeathEvent;
import net.neoforged.neoforge.event.server.ServerStoppedEvent;

import java.util.Collections;
import java.util.IdentityHashMap;
import java.util.Map;
import java.util.Objects;
import java.util.UUID;

/**
 * Server-authoritative Soul Anchor lifecycle bridge.
 *
 * Balance remains externally configured: this runtime does not choose spirit thresholds,
 * anchor caps, lockout duration or restored health. It only owns atomic death prevention,
 * bounded ledger state and durable settlement.
 */
public final class MinecraftSoulAnchorRuntime {
    private static final Map<MinecraftServer, ServerState> STATES =
        Collections.synchronizedMap(new IdentityHashMap<>());

    private MinecraftSoulAnchorRuntime() { }

    public static void register(IEventBus gameBus) {
        Objects.requireNonNull(gameBus, "gameBus");
        gameBus.addListener(
            EventPriority.LOWEST,
            false,
            LivingDeathEvent.class,
            MinecraftSoulAnchorRuntime::onLivingDeath);
        gameBus.addListener(MinecraftSoulAnchorRuntime::onServerStopped);
    }

    public static ArcanaDecision configure(
        MinecraftServer server,
        SoulAnchorLedger.Policy policy,
        float restoreHealth
    ) {
        Objects.requireNonNull(server, "server");
        Objects.requireNonNull(policy, "policy");
        if (!Float.isFinite(restoreHealth) || restoreHealth <= 0.0F) {
            return ArcanaDecision.deny(
                "soul_anchor_restore_health_invalid",
                "Soul Anchor restore health must be finite and positive");
        }

        SoulAnchorSavedData savedData = SoulAnchorSavedData.get(server);
        SoulAnchorLedger ledger = new SoulAnchorLedger(policy);
        try {
            ledger.restore(savedData.snapshots());
        } catch (IllegalArgumentException | IllegalStateException incompatibleState) {
            return ArcanaDecision.deny(
                "soul_anchor_persisted_state_incompatible",
                "Persisted Soul Anchor state exceeds the configured bounded policy");
        }

        STATES.put(server, new ServerState(ledger, savedData, restoreHealth));
        return ArcanaDecision.allow();
    }

    public static SoulAnchorLedger.CreditResult creditDeath(
        MinecraftServer server,
        UUID ownerId,
        SoulAnchorLedger.DeathCredit credit
    ) {
        Objects.requireNonNull(server, "server");
        Objects.requireNonNull(ownerId, "ownerId");
        Objects.requireNonNull(credit, "credit");
        ServerState state = STATES.get(server);
        if (state == null) return new SoulAnchorLedger.CreditResult(false, 0.0D, 0.0D);

        synchronized (state) {
            SoulAnchorLedger.CreditResult result = state.ledger.creditDeath(ownerId, credit);
            if (result.credited()) persist(state);
            return result;
        }
    }

    public static boolean formAnchor(MinecraftServer server, UUID ownerId) {
        Objects.requireNonNull(server, "server");
        Objects.requireNonNull(ownerId, "ownerId");
        ServerState state = STATES.get(server);
        if (state == null) return false;

        synchronized (state) {
            boolean formed = state.ledger.formAnchor(ownerId);
            if (formed) persist(state);
            return formed;
        }
    }

    public static SoulAnchorLedger.Snapshot snapshot(MinecraftServer server, UUID ownerId) {
        Objects.requireNonNull(server, "server");
        Objects.requireNonNull(ownerId, "ownerId");
        ServerState state = STATES.get(server);
        if (state == null) return new SoulAnchorLedger.Snapshot(ownerId, 0.0D, 0, 0L);
        synchronized (state) {
            return state.ledger.snapshot(ownerId);
        }
    }

    private static void onLivingDeath(LivingDeathEvent event) {
        if (!(event.getEntity() instanceof ServerPlayer player)) return;
        MinecraftServer server = player.getServer();
        if (server == null) return;
        ServerState state = STATES.get(server);
        if (state == null) return;

        synchronized (state) {
            float restoredHealth = Math.min(state.restoreHealth, player.getMaxHealth());
            if (!Float.isFinite(restoredHealth) || restoredHealth <= 0.0F) return;

            long nowTick = server.overworld().getGameTime();
            SoulAnchorLedger.AnchorConsumeResult consume = state.ledger.consumeForDeath(
                player.getUUID(),
                UUID.randomUUID(),
                nowTick);
            if (!consume.consumed()) return;

            persist(state);
            event.setCanceled(true);
            player.setHealth(restoredHealth);
        }
    }

    private static void onServerStopped(ServerStoppedEvent event) {
        STATES.remove(event.getServer());
    }

    private static void persist(ServerState state) {
        state.savedData.replaceSnapshots(state.ledger.snapshotAll());
    }

    private static final class ServerState {
        private final SoulAnchorLedger ledger;
        private final SoulAnchorSavedData savedData;
        private final float restoreHealth;

        private ServerState(
            SoulAnchorLedger ledger,
            SoulAnchorSavedData savedData,
            float restoreHealth
        ) {
            this.ledger = Objects.requireNonNull(ledger, "ledger");
            this.savedData = Objects.requireNonNull(savedData, "savedData");
            this.restoreHealth = restoreHealth;
        }
    }
}
