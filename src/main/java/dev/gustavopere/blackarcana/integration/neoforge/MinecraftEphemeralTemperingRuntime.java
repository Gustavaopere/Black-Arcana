package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.content.projection.ProjectedWeaponProfile;
import dev.gustavopere.blackarcana.content.projection.ProjectionSafetyCeilings;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.damagesource.DamageTypes;
import net.minecraft.world.item.DiggerItem;
import net.minecraft.world.item.ItemStack;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.event.entity.living.LivingDamageEvent;
import net.neoforged.neoforge.event.entity.player.PlayerEvent;
import net.neoforged.neoforge.event.server.ServerStoppedEvent;
import net.neoforged.neoforge.event.tick.ServerTickEvent;

import java.lang.ref.WeakReference;
import java.util.ArrayList;
import java.util.Collections;
import java.util.IdentityHashMap;
import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.UUID;

/**
 * Server-owned temporary modifier overlays for Ephemeral Tempering.
 *
 * The runtime never writes temporary components/NBT/attributes into an ItemStack. Instead an
 * overlay is bound to the exact in-memory stack instance that was held when the cast settled and
 * is consulted only at approved NeoForge mutation hooks. Replacing the held stack therefore does
 * not transfer the tempering effect. Final balance remains Stage 08/config-owned below the hard
 * technical ceilings enforced here.
 */
public final class MinecraftEphemeralTemperingRuntime {
    private static final int MAX_TRACKED_OWNERS = 4096;
    public static final long ABSOLUTE_MAX_LIFETIME_TICKS = 20L * 60L * 60L;

    private static final Map<MinecraftServer, State> STATES =
        Collections.synchronizedMap(new IdentityHashMap<>());

    private MinecraftEphemeralTemperingRuntime() { }

    public static void register(IEventBus gameBus) {
        Objects.requireNonNull(gameBus, "gameBus");
        gameBus.addListener(MinecraftEphemeralTemperingRuntime::onLivingDamage);
        gameBus.addListener(MinecraftEphemeralTemperingRuntime::onBreakSpeed);
        gameBus.addListener(MinecraftEphemeralTemperingRuntime::onServerTick);
        gameBus.addListener(MinecraftEphemeralTemperingRuntime::onPlayerLoggedOut);
        gameBus.addListener(MinecraftEphemeralTemperingRuntime::onServerStopped);
    }

    public static ApplyResult apply(
            MinecraftServer server,
            UUID ownerId,
            String modeId,
            double magnitude,
            long nowTick,
            long lifetimeTicks,
            int maxStacks
    ) {
        Objects.requireNonNull(server, "server");
        Objects.requireNonNull(ownerId, "ownerId");
        Objects.requireNonNull(modeId, "modeId");

        Mode mode = Mode.parse(modeId);
        if (mode == null) {
            return ApplyResult.denied(
                "ephemeral_tempering_mode_unsupported",
                "Requested Ephemeral Tempering mode has no safe runtime hook");
        }
        if (nowTick < 0L) {
            return ApplyResult.denied(
                "ephemeral_tempering_invalid_time",
                "Ephemeral Tempering creation tick must be non-negative");
        }
        if (lifetimeTicks <= 0L || lifetimeTicks > ABSOLUTE_MAX_LIFETIME_TICKS) {
            return ApplyResult.denied(
                "ephemeral_tempering_invalid_lifetime",
                "Ephemeral Tempering lifetime is outside the technical safety ceiling");
        }
        if (maxStacks <= 0 || maxStacks > ProjectionSafetyCeilings.MAX_ACTIVE_ECHOES) {
            return ApplyResult.denied(
                "ephemeral_tempering_invalid_stack_cap",
                "Ephemeral Tempering stack cap is outside the technical safety ceiling");
        }
        if (!validMagnitude(mode, magnitude)) {
            return ApplyResult.denied(
                "ephemeral_tempering_invalid_magnitude",
                "Ephemeral Tempering magnitude is outside the technical safety ceiling");
        }

        ServerPlayer owner = server.getPlayerList().getPlayer(ownerId);
        if (owner == null || !owner.isAlive()) {
            return ApplyResult.denied(
                "ephemeral_tempering_owner_unavailable",
                "Ephemeral Tempering owner must be loaded and alive");
        }

        ItemStack held = owner.getMainHandItem();
        if (!eligible(mode, held)) {
            return ApplyResult.denied(
                "ephemeral_tempering_unsupported_item",
                "Held item is not eligible for the configured Ephemeral Tempering mode");
        }

        final long expiresAtTick;
        try {
            expiresAtTick = Math.addExact(nowTick, lifetimeTicks);
        } catch (ArithmeticException overflow) {
            return ApplyResult.denied(
                "ephemeral_tempering_invalid_lifetime",
                "Ephemeral Tempering expiry overflowed server tick range");
        }

        State state = state(server);
        synchronized (state) {
            pruneOwner(state, ownerId, nowTick);
            List<Overlay> overlays = state.byOwner.get(ownerId);
            if (overlays == null) {
                if (state.byOwner.size() >= MAX_TRACKED_OWNERS) {
                    return ApplyResult.denied(
                        "ephemeral_tempering_owner_capacity",
                        "Ephemeral Tempering owner capacity is full");
                }
                overlays = new ArrayList<>();
                state.byOwner.put(ownerId, overlays);
            }
            if (overlays.size() >= maxStacks) {
                if (overlays.isEmpty()) state.byOwner.remove(ownerId);
                return ApplyResult.denied(
                    "ephemeral_tempering_stack_cap",
                    "Ephemeral Tempering stack cap is already reached");
            }

            Overlay overlay = new Overlay(
                UUID.randomUUID(),
                ownerId,
                mode,
                magnitude,
                nowTick,
                expiresAtTick,
                new WeakReference<>(held));
            overlays.add(overlay);
            return ApplyResult.allowed(overlay.overlayId(), mode.id, expiresAtTick);
        }
    }

    public static int activeStacks(MinecraftServer server, UUID ownerId) {
        Objects.requireNonNull(server, "server");
        Objects.requireNonNull(ownerId, "ownerId");
        State state = STATES.get(server);
        if (state == null) return 0;
        synchronized (state) {
            pruneOwner(state, ownerId, server.getTickCount());
            List<Overlay> overlays = state.byOwner.get(ownerId);
            return overlays == null ? 0 : overlays.size();
        }
    }

    /** Public for deterministic GameTests; production invocation is ServerTickEvent.Post. */
    public static void tick(MinecraftServer server, long nowTick) {
        Objects.requireNonNull(server, "server");
        State state = STATES.get(server);
        if (state == null) return;
        synchronized (state) {
            Iterator<Map.Entry<UUID, List<Overlay>>> iterator = state.byOwner.entrySet().iterator();
            while (iterator.hasNext()) {
                Map.Entry<UUID, List<Overlay>> entry = iterator.next();
                UUID ownerId = entry.getKey();
                ServerPlayer owner = server.getPlayerList().getPlayer(ownerId);
                if (owner == null || !owner.isAlive()) {
                    iterator.remove();
                    continue;
                }
                entry.getValue().removeIf(overlay -> overlay.expired(nowTick) || overlay.boundStack.get() == null);
                if (entry.getValue().isEmpty()) iterator.remove();
            }
            if (state.byOwner.isEmpty()) STATES.remove(server);
        }
    }

    static void onLivingDamage(LivingDamageEvent.Pre event) {
        if (!event.getSource().is(DamageTypes.PLAYER_ATTACK)) return;
        if (!(event.getSource().getEntity() instanceof ServerPlayer owner)) return;
        MinecraftServer server = owner.level().getServer();
        if (server == null) return;

        State state = STATES.get(server);
        if (state == null) return;
        synchronized (state) {
            pruneOwner(state, owner.getUUID(), server.getTickCount());
            List<Overlay> overlays = state.byOwner.get(owner.getUUID());
            if (overlays == null || overlays.isEmpty()) return;

            ItemStack held = owner.getMainHandItem();
            double bonus = 0.0D;
            for (Overlay overlay : overlays) {
                if (overlay.mode != Mode.MELEE_DAMAGE || overlay.boundStack.get() != held) continue;
                bonus += overlay.magnitude;
                if (bonus >= ProjectionSafetyCeilings.MAX_RAW_ATTACK_DAMAGE) {
                    bonus = ProjectionSafetyCeilings.MAX_RAW_ATTACK_DAMAGE;
                    break;
                }
            }
            if (bonus <= 0.0D) return;
            double adjusted = (double) event.getNewDamage() + bonus;
            event.setNewDamage((float) Math.min((double) Float.MAX_VALUE, adjusted));
        }
    }

    static void onBreakSpeed(PlayerEvent.BreakSpeed event) {
        if (!(event.getEntity() instanceof ServerPlayer owner)) return;
        MinecraftServer server = owner.level().getServer();
        if (server == null) return;

        State state = STATES.get(server);
        if (state == null) return;
        synchronized (state) {
            pruneOwner(state, owner.getUUID(), server.getTickCount());
            List<Overlay> overlays = state.byOwner.get(owner.getUUID());
            if (overlays == null || overlays.isEmpty()) return;

            ItemStack held = owner.getMainHandItem();
            double multiplier = 1.0D;
            for (Overlay overlay : overlays) {
                if (overlay.mode != Mode.MINING_SPEED || overlay.boundStack.get() != held) continue;
                multiplier *= overlay.magnitude;
                if (!Double.isFinite(multiplier)
                        || multiplier >= ProjectionSafetyCeilings.MAX_RAW_ATTACK_DAMAGE) {
                    multiplier = ProjectionSafetyCeilings.MAX_RAW_ATTACK_DAMAGE;
                    break;
                }
            }
            if (multiplier <= 1.0D) return;
            double adjusted = (double) event.getNewSpeed() * multiplier;
            event.setNewSpeed((float) Math.min((double) Float.MAX_VALUE, adjusted));
        }
    }

    static void onPlayerLoggedOut(PlayerEvent.PlayerLoggedOutEvent event) {
        MinecraftServer server = event.getEntity().level().getServer();
        if (server == null) return;
        State state = STATES.get(server);
        if (state == null) return;
        synchronized (state) {
            state.byOwner.remove(event.getEntity().getUUID());
            if (state.byOwner.isEmpty()) STATES.remove(server);
        }
    }

    private static void onServerTick(ServerTickEvent.Post event) {
        tick(event.getServer(), event.getServer().getTickCount());
    }

    private static void onServerStopped(ServerStoppedEvent event) {
        STATES.remove(event.getServer());
    }

    private static boolean validMagnitude(Mode mode, double magnitude) {
        if (!Double.isFinite(magnitude)) return false;
        return switch (mode) {
            case MELEE_DAMAGE -> magnitude > 0.0D
                && magnitude <= ProjectionSafetyCeilings.MAX_RAW_ATTACK_DAMAGE;
            case MINING_SPEED -> magnitude >= 1.0D
                && magnitude <= ProjectionSafetyCeilings.MAX_RAW_ATTACK_DAMAGE;
        };
    }

    private static boolean eligible(Mode mode, ItemStack held) {
        if (held.isEmpty()) return false;
        return switch (mode) {
            case MELEE_DAMAGE -> MinecraftEchoArmamentRuntime
                .sanitize("black_arcana:ephemeral_tempering_probe", held)
                .filter(profile -> profile.archetype() == ProjectedWeaponProfile.Archetype.MELEE)
                .isPresent();
            case MINING_SPEED -> held.getItem() instanceof DiggerItem;
        };
    }

    private static State state(MinecraftServer server) {
        synchronized (STATES) {
            return STATES.computeIfAbsent(server, ignored -> new State());
        }
    }

    private static void pruneOwner(State state, UUID ownerId, long nowTick) {
        List<Overlay> overlays = state.byOwner.get(ownerId);
        if (overlays == null) return;
        overlays.removeIf(overlay -> overlay.expired(nowTick) || overlay.boundStack.get() == null);
        if (overlays.isEmpty()) state.byOwner.remove(ownerId);
    }

    private enum Mode {
        MELEE_DAMAGE("MELEE_DAMAGE"),
        MINING_SPEED("MINING_SPEED");

        private final String id;

        Mode(String id) {
            this.id = id;
        }

        private static Mode parse(String id) {
            for (Mode mode : values()) {
                if (mode.id.equals(id)) return mode;
            }
            return null;
        }
    }

    private static final class Overlay {
        private final UUID overlayId;
        private final UUID ownerId;
        private final Mode mode;
        private final double magnitude;
        private final long createdTick;
        private final long expiresAtTick;
        private final WeakReference<ItemStack> boundStack;

        private Overlay(
            UUID overlayId,
            UUID ownerId,
            Mode mode,
            double magnitude,
            long createdTick,
            long expiresAtTick,
            WeakReference<ItemStack> boundStack
        ) {
            this.overlayId = Objects.requireNonNull(overlayId, "overlayId");
            this.ownerId = Objects.requireNonNull(ownerId, "ownerId");
            this.mode = Objects.requireNonNull(mode, "mode");
            this.magnitude = magnitude;
            this.createdTick = createdTick;
            this.expiresAtTick = expiresAtTick;
            this.boundStack = Objects.requireNonNull(boundStack, "boundStack");
        }

        private boolean expired(long nowTick) {
            return expiresAtTick <= nowTick;
        }
    }

    public record ApplyResult(ArcanaDecision decision, UUID overlayId, String mode, long expiresAtTick) {
        public ApplyResult {
            Objects.requireNonNull(decision, "decision");
            Objects.requireNonNull(mode, "mode");
            if (!decision.allowed() && overlayId != null) {
                throw new IllegalArgumentException("denied Ephemeral Tempering result cannot carry overlay id");
            }
            if (decision.allowed() && (overlayId == null || expiresAtTick <= 0L)) {
                throw new IllegalArgumentException("allowed Ephemeral Tempering result requires an active overlay");
            }
        }

        private static ApplyResult allowed(UUID overlayId, String mode, long expiresAtTick) {
            return new ApplyResult(ArcanaDecision.allow(), overlayId, mode, expiresAtTick);
        }

        private static ApplyResult denied(String code, String detail) {
            return new ApplyResult(ArcanaDecision.deny(code, detail), null, "", 0L);
        }
    }

    private static final class State {
        private final Map<UUID, List<Overlay>> byOwner = new LinkedHashMap<>();
    }
}
