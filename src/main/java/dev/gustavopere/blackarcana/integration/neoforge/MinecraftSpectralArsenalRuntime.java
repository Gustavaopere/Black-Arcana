package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.content.projection.ProjectedWeaponProfile;
import dev.gustavopere.blackarcana.content.projection.ProjectionBudgetTracker;
import dev.gustavopere.blackarcana.content.projection.ProjectionSafetyCeilings;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerPlayer;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.event.entity.player.PlayerEvent;
import net.neoforged.neoforge.event.server.ServerStoppedEvent;
import net.neoforged.neoforge.event.tick.ServerTickEvent;

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
 * Server-owned Spectral Arsenal planning/runtime boundary.
 *
 * It consumes only sanitized {@link ProjectedWeaponProfile} snapshots previously registered by
 * Echo Armament. Live ItemStacks, data components, NBT and capabilities never enter this state;
 * the host may render/materialize a projectile only while its ephemeral handle remains valid.
 */
public final class MinecraftSpectralArsenalRuntime {
    /** Technical ceiling only. Stage 08/config owns final spell lifetime below this value. */
    public static final long ABSOLUTE_MAX_PROJECTILE_LIFETIME_TICKS = 20L * 60L * 60L;

    private static final Map<MinecraftServer, State> STATES =
        Collections.synchronizedMap(new IdentityHashMap<>());

    private MinecraftSpectralArsenalRuntime() { }

    public static void register(IEventBus gameBus) {
        Objects.requireNonNull(gameBus, "gameBus");
        gameBus.addListener(MinecraftSpectralArsenalRuntime::onServerTick);
        gameBus.addListener(MinecraftSpectralArsenalRuntime::onPlayerLoggedOut);
        gameBus.addListener(MinecraftSpectralArsenalRuntime::onServerStopped);
    }

    public static VolleyResult launchVolley(
            MinecraftServer server,
            UUID ownerId,
            List<String> profileIds,
            long nowTick,
            long lifetimeTicks,
            double maxDamagePerProjectile
    ) {
        Objects.requireNonNull(server, "server");
        Objects.requireNonNull(ownerId, "ownerId");
        Objects.requireNonNull(profileIds, "profileIds");

        if (nowTick < 0L) {
            return VolleyResult.denied("spectral_arsenal_invalid_time", "Volley creation tick must be non-negative");
        }
        try {
            ProjectionBudgetTracker.validateVolleySize(profileIds.size());
        } catch (IllegalArgumentException invalidCount) {
            return VolleyResult.denied(
                "spectral_arsenal_projectile_count",
                "Spectral Arsenal projectile count exceeds the hard volley ceiling");
        }
        if (lifetimeTicks <= 0L || lifetimeTicks > ABSOLUTE_MAX_PROJECTILE_LIFETIME_TICKS) {
            return VolleyResult.denied(
                "spectral_arsenal_projectile_lifetime",
                "Spectral Arsenal projectile lifetime is outside the technical safety ceiling");
        }
        if (!Double.isFinite(maxDamagePerProjectile)
                || maxDamagePerProjectile <= 0.0D
                || maxDamagePerProjectile > ProjectionSafetyCeilings.MAX_RAW_ATTACK_DAMAGE) {
            return VolleyResult.denied(
                "spectral_arsenal_damage_cap",
                "Spectral Arsenal projectile damage cap is outside the technical safety ceiling");
        }

        ServerPlayer owner = server.getPlayerList().getPlayer(ownerId);
        if (owner == null || !owner.isAlive()) {
            return VolleyResult.denied(
                "spectral_arsenal_owner_unavailable",
                "Spectral Arsenal owner must be loaded and alive");
        }

        // Resolve the entire sanitized input set before touching budget/state. This prevents a
        // missing/invalid profile later in the list from producing a partial volley.
        List<ProjectedWeaponProfile> resolvedProfiles = new ArrayList<>(profileIds.size());
        List<Double> resolvedDamage = new ArrayList<>(profileIds.size());
        for (String profileId : profileIds) {
            if (profileId == null) {
                return VolleyResult.denied(
                    "spectral_arsenal_profile_missing",
                    "Spectral Arsenal profile id cannot be null");
            }
            var profile = MinecraftEchoArmamentRuntime.findProfile(server, ownerId, profileId);
            if (profile.isEmpty()) {
                return VolleyResult.denied(
                    "spectral_arsenal_profile_missing",
                    "Requested sanitized Spectral Arsenal profile is not registered");
            }
            ProjectedWeaponProfile sanitized = profile.get();
            double damage = Math.min(sanitized.attackDamageContribution(), maxDamagePerProjectile);
            if (!Double.isFinite(damage) || damage <= 0.0D) {
                return VolleyResult.denied(
                    "spectral_arsenal_profile_damage",
                    "Requested sanitized profile has no eligible positive bounded attack damage");
            }
            resolvedProfiles.add(sanitized);
            resolvedDamage.add(damage);
        }

        final long expiresAtTick;
        try {
            expiresAtTick = Math.addExact(nowTick, lifetimeTicks);
        } catch (ArithmeticException overflow) {
            return VolleyResult.denied(
                "spectral_arsenal_projectile_lifetime",
                "Spectral Arsenal projectile expiry overflowed server tick range");
        }

        State state = state(server);
        synchronized (state) {
            if (!state.budget.tryAcquireEchoes(ownerId, resolvedProfiles.size())) {
                return VolleyResult.denied(
                    "spectral_arsenal_active_capacity",
                    "Active Spectral Arsenal projection budget is full for owner");
            }

            List<SpectralProjectileHandle> launched = new ArrayList<>(resolvedProfiles.size());
            for (int index = 0; index < resolvedProfiles.size(); index++) {
                SpectralProjectileHandle handle = new SpectralProjectileHandle(
                    UUID.randomUUID(),
                    ownerId,
                    resolvedProfiles.get(index),
                    resolvedDamage.get(index),
                    nowTick,
                    expiresAtTick);
                state.projectiles.put(handle.projectileId(), handle);
                launched.add(handle);
            }
            return VolleyResult.allowed(launched);
        }
    }

    public static int activeProjectiles(MinecraftServer server, UUID ownerId) {
        Objects.requireNonNull(server, "server");
        Objects.requireNonNull(ownerId, "ownerId");
        State state = STATES.get(server);
        if (state == null) return 0;
        synchronized (state) {
            return state.budget.activeEchoes(ownerId);
        }
    }

    /** Public for deterministic GameTests; normal production invocation is ServerTickEvent.Post. */
    public static void tick(MinecraftServer server, long nowTick) {
        Objects.requireNonNull(server, "server");
        State state = STATES.get(server);
        if (state == null) return;
        synchronized (state) {
            Iterator<Map.Entry<UUID, SpectralProjectileHandle>> iterator = state.projectiles.entrySet().iterator();
            while (iterator.hasNext()) {
                SpectralProjectileHandle handle = iterator.next().getValue();
                boolean expired = handle.expiresAtTick() <= nowTick;
                ServerPlayer owner = server.getPlayerList().getPlayer(handle.ownerId());
                boolean ownerUnavailable = owner == null || !owner.isAlive();
                if (expired || ownerUnavailable) {
                    iterator.remove();
                    state.budget.releaseEchoes(handle.ownerId(), 1);
                }
            }
            if (state.projectiles.isEmpty()) STATES.remove(server);
        }
    }

    private static State state(MinecraftServer server) {
        synchronized (STATES) {
            return STATES.computeIfAbsent(server, ignored -> new State());
        }
    }

    private static void clearOwner(MinecraftServer server, UUID ownerId) {
        State state = STATES.get(server);
        if (state == null) return;
        synchronized (state) {
            int removed = 0;
            Iterator<Map.Entry<UUID, SpectralProjectileHandle>> iterator = state.projectiles.entrySet().iterator();
            while (iterator.hasNext()) {
                if (iterator.next().getValue().ownerId().equals(ownerId)) {
                    iterator.remove();
                    removed++;
                }
            }
            if (removed > 0) state.budget.releaseEchoes(ownerId, removed);
            if (state.projectiles.isEmpty()) STATES.remove(server);
        }
    }

    private static void onServerTick(ServerTickEvent.Post event) {
        tick(event.getServer(), event.getServer().getTickCount());
    }

    static void onPlayerLoggedOut(PlayerEvent.PlayerLoggedOutEvent event) {
        MinecraftServer server = event.getEntity().level().getServer();
        if (server == null) return;
        clearOwner(server, event.getEntity().getUUID());
    }

    private static void onServerStopped(ServerStoppedEvent event) {
        STATES.remove(event.getServer());
    }

    public record SpectralProjectileHandle(
        UUID projectileId,
        UUID ownerId,
        ProjectedWeaponProfile profile,
        double damage,
        long createdTick,
        long expiresAtTick
    ) {
        public SpectralProjectileHandle {
            Objects.requireNonNull(projectileId, "projectileId");
            Objects.requireNonNull(ownerId, "ownerId");
            Objects.requireNonNull(profile, "profile");
            if (!Double.isFinite(damage)
                    || damage <= 0.0D
                    || damage > ProjectionSafetyCeilings.MAX_RAW_ATTACK_DAMAGE) {
                throw new IllegalArgumentException("Spectral Arsenal projectile damage outside hard ceiling");
            }
            if (createdTick < 0L || expiresAtTick <= createdTick) {
                throw new IllegalArgumentException("invalid Spectral Arsenal projectile lifetime");
            }
        }
    }

    public record VolleyResult(ArcanaDecision decision, List<SpectralProjectileHandle> projectiles) {
        public VolleyResult {
            Objects.requireNonNull(decision, "decision");
            projectiles = List.copyOf(Objects.requireNonNull(projectiles, "projectiles"));
            if (!decision.allowed() && !projectiles.isEmpty()) {
                throw new IllegalArgumentException("denied Spectral Arsenal volley cannot carry projectile handles");
            }
            if (projectiles.size() > ProjectionSafetyCeilings.MAX_PROJECTILES_PER_VOLLEY) {
                throw new IllegalArgumentException("Spectral Arsenal volley exceeds hard projectile ceiling");
            }
        }

        public int launchedCount() {
            return projectiles.size();
        }

        private static VolleyResult allowed(List<SpectralProjectileHandle> projectiles) {
            return new VolleyResult(ArcanaDecision.allow(), projectiles);
        }

        private static VolleyResult denied(String code, String detail) {
            return new VolleyResult(ArcanaDecision.deny(code, detail), List.of());
        }
    }

    private static final class State {
        private final ProjectionBudgetTracker budget =
            new ProjectionBudgetTracker(ProjectionSafetyCeilings.MAX_ACTIVE_ECHOES);
        private final Map<UUID, SpectralProjectileHandle> projectiles = new LinkedHashMap<>();
    }
}
