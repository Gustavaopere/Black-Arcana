package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.BlackArcanaMod;
import dev.gustavopere.blackarcana.api.hazard.ArcanaDamageProvenance;
import dev.gustavopere.blackarcana.api.hazard.ArcaneBacklashPolicy;
import dev.gustavopere.blackarcana.api.hazard.ArcaneBacklashSettlement;
import dev.gustavopere.blackarcana.api.hazard.ArcaneConfirmedDamage;
import dev.gustavopere.blackarcana.api.hazard.ArcaneEmergencyProtectionSnapshot;
import dev.gustavopere.blackarcana.api.hazard.ArcaneHazardSnapshot;
import dev.gustavopere.blackarcana.api.hazard.ArcaneResistanceSnapshot;
import dev.gustavopere.blackarcana.core.hazard.ArcaneBacklashProtectionAttemptTracker;
import dev.gustavopere.blackarcana.core.hazard.ArcaneDamageProvenanceTracker;
import dev.gustavopere.blackarcana.core.hazard.ArcaneEmergencyProtectionCoordinator;
import dev.gustavopere.blackarcana.core.hazard.ArcaneHazardRuntime;
import dev.gustavopere.blackarcana.core.hazard.ArcaneLethalBacklashProtection;
import dev.gustavopere.blackarcana.core.hazard.PendingBacklashRegistry;
import dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntimeManager;
import dev.gustavopere.blackarcana.persistence.BlackArcanaSavedData;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.LivingEntity;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.event.entity.living.LivingDamageEvent;
import net.neoforged.neoforge.event.entity.player.PlayerEvent;
import net.neoforged.neoforge.event.server.ServerStartedEvent;
import net.neoforged.neoforge.event.server.ServerStoppedEvent;
import net.neoforged.neoforge.event.tick.ServerTickEvent;

import java.util.Collections;
import java.util.IdentityHashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;
import java.util.UUID;

/**
 * NeoForge translation layer for Stage 05A causal damage accounting.
 * Missing provenance is terminal: no attacker/spell heuristics are used.
 */
public final class MinecraftArcaneDamagePipeline {
    public static final int DEFAULT_MAX_HAZARD_SESSIONS = 16_384;
    public static final int DEFAULT_MAX_TRACKED_DAMAGE_SOURCES = 65_536;
    public static final int DEFAULT_MAX_PENDING_CASTERS = 16_384;
    public static final int DEFAULT_MAX_TRACKED_BACKLASH_ATTEMPTS = 65_536;

    public record DamageAttempt(boolean invoked, boolean accepted, String code) {
        public DamageAttempt {
            Objects.requireNonNull(code, "code");
            if (invoked && !code.isEmpty()) throw new IllegalArgumentException("invoked attempt cannot carry denial code");
            if (!invoked && code.isBlank()) throw new IllegalArgumentException("denied attempt requires a code");
            if (!invoked && accepted) throw new IllegalArgumentException("non-invoked attempt cannot be accepted");
        }

        public static DamageAttempt invoked(boolean accepted) { return new DamageAttempt(true, accepted, ""); }
        public static DamageAttempt denied(String code) { return new DamageAttempt(false, false, code); }
    }

    private record ServerState(
        ArcaneHazardRuntime hazards,
        ArcaneDamageProvenanceTracker<DamageSource> provenance,
        PendingBacklashRegistry pendingBacklash,
        ArcaneBacklashProtectionAttemptTracker<DamageSource> backlashProtectionAttempts,
        ArcaneEmergencyProtectionCoordinator emergencyProtection
    ) { }

    private static final Map<MinecraftServer, ServerState> STATES =
        Collections.synchronizedMap(new IdentityHashMap<>());

    private MinecraftArcaneDamagePipeline() { }

    public static void register(IEventBus gameBus) {
        Objects.requireNonNull(gameBus, "gameBus");
        gameBus.addListener(MinecraftArcaneDamagePipeline::onServerStarted);
        gameBus.addListener(MinecraftArcaneDamagePipeline::onServerTick);
        gameBus.addListener(MinecraftArcaneDamagePipeline::onPlayerLoggedIn);
        gameBus.addListener(MinecraftArcaneDamagePipeline::onLivingDamagePre);
        gameBus.addListener(MinecraftArcaneDamagePipeline::onLivingDamagePost);
        gameBus.addListener(MinecraftArcaneDamagePipeline::onServerStopped);
    }

    public static ArcaneHazardRuntime.ActivationResult activate(
        MinecraftServer server,
        ArcaneHazardSnapshot snapshot,
        ArcaneResistanceSnapshot resistance,
        ArcaneBacklashPolicy policy
    ) {
        return activate(server, snapshot, resistance, policy, ArcaneEmergencyProtectionSnapshot.empty());
    }

    public static ArcaneHazardRuntime.ActivationResult activate(
        MinecraftServer server,
        ArcaneHazardSnapshot snapshot,
        ArcaneResistanceSnapshot resistance,
        ArcaneBacklashPolicy policy,
        ArcaneEmergencyProtectionSnapshot emergencyProtectionSnapshot
    ) {
        Objects.requireNonNull(server, "server");
        ServerState state = STATES.get(server);
        if (state == null) return ArcaneHazardRuntime.ActivationResult.denied("hazard_runtime_unavailable");
        return activateHazardRuntime(
            state.hazards(),
            snapshot,
            resistance,
            policy,
            emergencyProtectionSnapshot);
    }

    static ArcaneHazardRuntime.ActivationResult activateHazardRuntime(
        ArcaneHazardRuntime runtime,
        ArcaneHazardSnapshot snapshot,
        ArcaneResistanceSnapshot resistance,
        ArcaneBacklashPolicy policy,
        ArcaneEmergencyProtectionSnapshot emergencyProtectionSnapshot
    ) {
        Objects.requireNonNull(runtime, "runtime");
        Objects.requireNonNull(snapshot, "snapshot");
        Objects.requireNonNull(resistance, "resistance");
        Objects.requireNonNull(policy, "policy");
        Objects.requireNonNull(emergencyProtectionSnapshot, "emergencyProtectionSnapshot");
        return runtime.activate(snapshot, resistance, policy, emergencyProtectionSnapshot);
    }

    static Optional<ArcaneBacklashProtectionAttemptTracker.Attempt> protectionAttempt(
        ArcaneHazardRuntime hazards,
        ArcanaDamageProvenance provenance
    ) {
        Objects.requireNonNull(hazards, "hazards");
        Objects.requireNonNull(provenance, "provenance");
        if (!provenance.hazardEligible()) return Optional.empty();
        return hazards.sessions().find(provenance.rootCastId())
            .filter(session -> session.snapshot().rootCastId().equals(provenance.rootCastId()))
            .filter(session -> session.snapshot().casterId().equals(provenance.casterId()))
            .filter(session -> session.snapshot().spellId().equals(provenance.spellId()))
            .map(session -> new ArcaneBacklashProtectionAttemptTracker.Attempt(
                provenance.rootCastId(),
                provenance.damageInstanceId(),
                provenance.casterId(),
                session.snapshot().profile().emergencyProtectionAllowed(),
                session.emergencyProtectionSnapshot()));
    }

    public static Optional<ArcaneHazardRuntime> hazardRuntime(MinecraftServer server) {
        ServerState state = STATES.get(Objects.requireNonNull(server, "server"));
        return state == null ? Optional.empty() : Optional.of(state.hazards());
    }

    public static DamageAttempt hurtAttributed(
        LivingEntity target,
        DamageSource source,
        float requestedDamage,
        ArcanaDamageProvenance provenance
    ) {
        Objects.requireNonNull(target, "target");
        Objects.requireNonNull(source, "source");
        Objects.requireNonNull(provenance, "provenance");
        if (!Float.isFinite(requestedDamage) || requestedDamage < 0.0F) {
            throw new IllegalArgumentException("requestedDamage must be finite and non-negative");
        }
        if (!(target.level() instanceof ServerLevel level)) return DamageAttempt.denied("server_level_required");
        ServerState state = STATES.get(level.getServer());
        if (state == null) return DamageAttempt.denied("hazard_runtime_unavailable");
        if (!state.provenance().register(source, provenance)) return DamageAttempt.denied("damage_provenance_capacity");
        try {
            return DamageAttempt.invoked(target.hurt(source, requestedDamage));
        } finally {
            state.provenance().release(source);
        }
    }

    private static void onServerStarted(ServerStartedEvent event) {
        MinecraftServer server = event.getServer();
        PendingBacklashRegistry pendingBacklash = new PendingBacklashRegistry(
            DEFAULT_MAX_PENDING_CASTERS,
            PendingBacklashRegistry.ABSOLUTE_MAX_PENDING_PER_PLAYER);
        BlackArcanaSavedData.get(server).restorePendingBacklash(pendingBacklash);
        STATES.put(server, new ServerState(
            new ArcaneHazardRuntime(DEFAULT_MAX_HAZARD_SESSIONS),
            new ArcaneDamageProvenanceTracker<>(DEFAULT_MAX_TRACKED_DAMAGE_SOURCES),
            pendingBacklash,
            new ArcaneBacklashProtectionAttemptTracker<>(DEFAULT_MAX_TRACKED_BACKLASH_ATTEMPTS),
            new ArcaneEmergencyProtectionCoordinator(List.of())));
    }

    private static void onServerTick(ServerTickEvent.Post event) {
        ServerState state = STATES.get(event.getServer());
        if (state != null) state.hazards().tick(event.getServer().overworld().getGameTime());
    }

    private static void onLivingDamagePre(LivingDamageEvent.Pre event) {
        if (!(event.getEntity() instanceof ServerPlayer caster)) return;
        if (!event.getSource().is(ArcaneBacklashDamageTypes.ARCANE_BACKLASH)) return;
        MinecraftServer server = caster.serverLevel().getServer();
        ServerState state = STATES.get(server);
        if (state == null) return;

        ArcaneBacklashProtectionAttemptTracker.Attempt attempt =
            state.backlashProtectionAttempts().find(event.getSource()).orElse(null);
        if (attempt == null || !caster.getUUID().equals(attempt.casterId())) return;

        var runtime = ArcanaServerRuntimeManager.get(server).orElse(null);
        if (runtime == null) return;

        ArcaneLethalBacklashProtection.Result result = ArcaneLethalBacklashProtection.resolve(
            attempt.casterId(),
            attempt.damageInstanceId(),
            event.getNewDamage(),
            caster.getHealth(),
            caster.getAbsorptionAmount(),
            attempt.protectionAllowed(),
            attempt.emergencyProtectionSnapshot(),
            runtime.emergencyProtection(),
            server.overworld().getGameTime(),
            state.emergencyProtection());
        if (!result.consumed()) return;

        event.setNewDamage((float) result.remainingDamage());
        BlackArcanaSavedData.get(server).captureHazards(
            runtime.corruption(),
            runtime.strain(),
            runtime.emergencyProtection());
    }

    private static void onLivingDamagePost(LivingDamageEvent.Post event) {
        if (!(event.getEntity().level() instanceof ServerLevel level)) return;
        MinecraftServer server = level.getServer();
        ServerState state = STATES.get(server);
        if (state == null) return;

        ArcanaDamageProvenance provenance = state.provenance().find(event.getSource()).orElse(null);
        if (provenance == null) return;

        ArcaneBacklashSettlement settlement = state.hazards().settle(new ArcaneConfirmedDamage(
            provenance,
            event.getNewDamage(),
            server.overworld().getGameTime()));
        if (settlement.status() != ArcaneBacklashSettlement.Status.SETTLED || settlement.backlashDamage() <= 0.0D) return;

        ServerPlayer caster = findCaster(server, provenance.casterId());
        if (caster == null) {
            boolean fullyRecorded = state.pendingBacklash().accrue(provenance.casterId(), settlement.backlashDamage());
            double persistedAmount = state.pendingBacklash().pending(provenance.casterId());
            boolean fullyPersisted = BlackArcanaSavedData.get(server)
                .updatePendingBacklash(provenance.casterId(), persistedAmount);
            if (!fullyRecorded || !fullyPersisted) {
                BlackArcanaMod.LOGGER.error(
                    "Pending Arcane Backlash hit a safety ceiling for caster {}; debt was clamped",
                    provenance.casterId());
            }
            return;
        }
        applyBacklash(
            caster,
            settlement.backlashDamage(),
            state,
            protectionAttempt(state.hazards(), provenance).orElse(null));
    }

    private static void onPlayerLoggedIn(PlayerEvent.PlayerLoggedInEvent event) {
        if (!(event.getEntity() instanceof ServerPlayer player)) return;
        MinecraftServer server = player.serverLevel().getServer();
        ServerState state = STATES.get(server);
        if (state == null) return;
        double pending = state.pendingBacklash().drain(player.getUUID());
        if (pending <= 0.0D) return;
        BlackArcanaSavedData.get(server).updatePendingBacklash(player.getUUID(), 0.0D);
        applyBacklash(player, pending);
    }

    private static void onServerStopped(ServerStoppedEvent event) {
        STATES.remove(event.getServer());
    }

    private static ServerPlayer findCaster(MinecraftServer server, UUID casterId) {
        ServerPlayer listed = server.getPlayerList().getPlayer(casterId);
        if (listed != null) return listed;
        for (ServerLevel level : server.getAllLevels()) {
            Entity entity = level.getEntity(casterId);
            if (entity instanceof ServerPlayer player) return player;
        }
        return null;
    }

    private static void applyBacklash(ServerPlayer caster, double amount) {
        applyBacklash(caster, amount, null, null);
    }

    private static void applyBacklash(
        ServerPlayer caster,
        double amount,
        ServerState state,
        ArcaneBacklashProtectionAttemptTracker.Attempt attempt
    ) {
        float bounded = (float) Math.min(amount, 1_000_000.0D);
        if (bounded <= 0.0F) return;
        DamageSource source = caster.damageSources().source(ArcaneBacklashDamageTypes.ARCANE_BACKLASH);
        if (state == null || attempt == null || !state.backlashProtectionAttempts().register(source, attempt)) {
            caster.hurt(source, bounded);
            return;
        }
        try {
            caster.hurt(source, bounded);
        } finally {
            state.backlashProtectionAttempts().release(source);
        }
    }
}
