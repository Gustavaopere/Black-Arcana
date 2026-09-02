package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.api.ArcanaServices.CostReservation;
import dev.gustavopere.blackarcana.content.blood.BloodPriceHealthAccess;
import dev.gustavopere.blackarcana.content.blood.BloodSafetyCeilings;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.Entity;

import java.util.Objects;
import java.util.UUID;
import java.util.concurrent.atomic.AtomicBoolean;

/** NeoForge adapter that reserves only a player's real health for Blood Price. */
public final class NeoForgeBloodPriceHealthAccess implements BloodPriceHealthAccess {
    private static final float EPSILON = 0.0001F;

    private final MinecraftServer server;

    public NeoForgeBloodPriceHealthAccess(MinecraftServer server) {
        this.server = Objects.requireNonNull(server, "server");
    }

    @Override
    public double currentHealth(UUID casterId) {
        return requirePlayer(casterId).getHealth();
    }

    @Override
    public CostReservation reserve(UUID casterId, double amount, double minimumRemainingHealth) {
        Objects.requireNonNull(casterId, "casterId");
        if (!Double.isFinite(amount) || amount < 0.0D || amount > Float.MAX_VALUE) {
            return denied("blood_price_health_amount_invalid", "Blood Price health amount is outside supported bounds");
        }
        if (!Double.isFinite(minimumRemainingHealth)
            || minimumRemainingHealth < BloodSafetyCeilings.MIN_BLOOD_PRICE_REMAINING_HEALTH
            || minimumRemainingHealth > Float.MAX_VALUE) {
            return denied("blood_price_health_floor_invalid", "Blood Price minimum health floor is outside supported bounds");
        }

        final ServerPlayer player;
        try {
            player = requirePlayer(casterId);
        } catch (RuntimeException failure) {
            return denied("blood_price_player_unavailable", failure.getMessage());
        }

        float before = player.getHealth();
        if (!Float.isFinite(before) || before <= 0.0F) {
            return denied("blood_price_player_not_alive", "Blood Price requires a living caster");
        }
        double remaining = (double) before - amount;
        if (remaining + EPSILON < minimumRemainingHealth) {
            return denied(
                "insufficient_blood_price_health",
                "Blood Price would cross the configured minimum remaining health");
        }
        if (amount <= EPSILON) return NoOpReservation.INSTANCE;

        float target = (float) remaining;
        if (target + EPSILON < minimumRemainingHealth) {
            return denied(
                "insufficient_blood_price_health",
                "Blood Price float conversion would cross the configured minimum remaining health");
        }

        player.setHealth(target);
        float after = player.getHealth();
        if (Math.abs(after - target) > EPSILON) {
            player.setHealth(before);
            return denied(
                "blood_price_health_adjustment_modified",
                "Another health hook modified the Blood Price reservation");
        }
        return new HealthReservation(player, (float) amount);
    }

    private ServerPlayer requirePlayer(UUID playerId) {
        Objects.requireNonNull(playerId, "playerId");
        ServerPlayer listed = server.getPlayerList().getPlayer(playerId);
        if (listed != null) return listed;
        for (ServerLevel level : server.getAllLevels()) {
            Entity entity = level.getEntity(playerId);
            if (entity instanceof ServerPlayer player) return player;
        }
        throw new IllegalStateException("player is not online on this server");
    }

    private static CostReservation denied(String code, String detail) {
        return new DeniedReservation(ArcanaDecision.deny(code, detail));
    }

    private record DeniedReservation(ArcanaDecision decision) implements CostReservation {
        private DeniedReservation {
            Objects.requireNonNull(decision, "decision");
            if (decision.allowed()) throw new IllegalArgumentException("denied reservation requires denial decision");
        }
        @Override public void commit() { throw new IllegalStateException("cannot commit denied health reservation"); }
        @Override public void refund() { }
    }

    private enum NoOpReservation implements CostReservation {
        INSTANCE;
        @Override public ArcanaDecision decision() { return ArcanaDecision.allow(); }
        @Override public void commit() { }
        @Override public void refund() { }
    }

    private static final class HealthReservation implements CostReservation {
        private final ServerPlayer player;
        private final float amount;
        private final AtomicBoolean terminal = new AtomicBoolean();

        private HealthReservation(ServerPlayer player, float amount) {
            this.player = Objects.requireNonNull(player, "player");
            this.amount = amount;
        }

        @Override
        public ArcanaDecision decision() {
            return ArcanaDecision.allow();
        }

        @Override
        public void commit() {
            terminal.compareAndSet(false, true);
        }

        @Override
        public void refund() {
            if (!terminal.compareAndSet(false, true)) return;
            if (!player.isAlive() || player.getHealth() <= 0.0F) return;
            float restored = Math.min(player.getMaxHealth(), player.getHealth() + amount);
            player.setHealth(restored);
        }
    }
}
