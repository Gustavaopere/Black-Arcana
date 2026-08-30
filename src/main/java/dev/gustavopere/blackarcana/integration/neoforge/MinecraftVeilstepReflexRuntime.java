package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.content.space.LiminalSafetyCeilings;
import dev.gustavopere.blackarcana.content.space.VeilstepCandidateSelector;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.RelativeMovement;
import net.minecraft.world.phys.Vec3;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.event.entity.player.PlayerEvent;
import net.neoforged.neoforge.event.server.ServerStoppedEvent;

import java.util.ArrayList;
import java.util.Collections;
import java.util.IdentityHashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Set;
import java.util.UUID;

/**
 * Server-authoritative Veilstep Reflex state and settlement boundary.
 *
 * Host adapters own threat classification and resource-to-charge conversion. This runtime only
 * stores explicitly granted bounded charges, enforces an internal cooldown, evaluates a bounded
 * list of server-generated candidate positions through the shared destination resolver and
 * consumes one charge only after a teleport actually settles.
 */
public final class MinecraftVeilstepReflexRuntime {
    private static final VeilstepCandidateSelector SELECTOR =
        new VeilstepCandidateSelector(new dev.gustavopere.blackarcana.content.space.SafeDestinationPolicy());
    private static final Map<MinecraftServer, Map<UUID, State>> STATES =
        Collections.synchronizedMap(new IdentityHashMap<>());

    private MinecraftVeilstepReflexRuntime() { }

    public static void register(IEventBus gameBus) {
        Objects.requireNonNull(gameBus, "gameBus");
        gameBus.addListener(MinecraftVeilstepReflexRuntime::onPlayerLoggedOut);
        gameBus.addListener(MinecraftVeilstepReflexRuntime::onServerStopped);
    }

    /**
     * Replaces the host-owned charge balance without changing an already-active cooldown.
     * How mana/items become charges is deliberately outside this Stage 07 runtime.
     */
    public static ArcanaDecision setCharges(
            MinecraftServer server,
            UUID casterId,
            int charges,
            int maxCharges
    ) {
        Objects.requireNonNull(server, "server");
        Objects.requireNonNull(casterId, "casterId");
        if (maxCharges <= 0 || charges < 0 || charges > maxCharges) {
            return ArcanaDecision.deny(
                "veilstep_invalid_charge_state",
                "Veilstep charges must be between zero and the positive host-configured cap");
        }
        ServerPlayer caster = server.getPlayerList().getPlayer(casterId);
        if (caster == null || !caster.isAlive()) {
            return ArcanaDecision.deny(
                "veilstep_caster_unavailable",
                "Veilstep charges can be assigned only to a loaded living caster");
        }

        synchronized (STATES) {
            Map<UUID, State> byCaster = STATES.computeIfAbsent(server, ignored -> new java.util.LinkedHashMap<>());
            State previous = byCaster.get(casterId);
            long cooldownUntilTick = previous == null ? 0L : previous.cooldownUntilTick;
            byCaster.put(casterId, new State(charges, maxCharges, cooldownUntilTick));
        }
        return ArcanaDecision.allow();
    }

    public static int charges(MinecraftServer server, UUID casterId) {
        Objects.requireNonNull(server, "server");
        Objects.requireNonNull(casterId, "casterId");
        synchronized (STATES) {
            Map<UUID, State> byCaster = STATES.get(server);
            State state = byCaster == null ? null : byCaster.get(casterId);
            return state == null ? 0 : state.charges;
        }
    }

    public static TriggerResult trigger(
            MinecraftServer server,
            UUID casterId,
            List<Vec3> candidates,
            long nowTick,
            long cooldownTicks,
            boolean protectedThreat
    ) {
        Objects.requireNonNull(server, "server");
        Objects.requireNonNull(casterId, "casterId");
        Objects.requireNonNull(candidates, "candidates");
        if (nowTick < 0L) {
            return denied(server, casterId, "veilstep_invalid_time", "Veilstep trigger tick must be non-negative");
        }
        if (cooldownTicks <= 0L) {
            return denied(server, casterId, "veilstep_invalid_cooldown", "Veilstep internal cooldown must be positive");
        }
        if (candidates.size() > LiminalSafetyCeilings.MAX_SAFE_SEARCH_CANDIDATES) {
            return denied(server, casterId, "veilstep_candidate_cap", "Veilstep safe-position search exceeds the hard candidate ceiling");
        }
        if (protectedThreat) {
            return denied(server, casterId, "veilstep_protected_threat", "Protected or unavoidable threat is not eligible for Veilstep");
        }

        final long cooldownUntil;
        try {
            cooldownUntil = Math.addExact(nowTick, cooldownTicks);
        } catch (ArithmeticException overflow) {
            return denied(server, casterId, "veilstep_invalid_cooldown", "Veilstep cooldown overflowed server tick range");
        }

        ServerPlayer caster = server.getPlayerList().getPlayer(casterId);
        if (caster == null || !caster.isAlive() || !(caster.level() instanceof ServerLevel level)) {
            return denied(server, casterId, "veilstep_caster_unavailable", "Veilstep caster must be loaded and alive");
        }

        synchronized (STATES) {
            Map<UUID, State> byCaster = STATES.get(server);
            State state = byCaster == null ? null : byCaster.get(casterId);
            if (state == null || state.charges <= 0) {
                return TriggerResult.denied("veilstep_no_charge", "Veilstep has no available charge", 0, state == null ? 0L : state.cooldownUntilTick);
            }
            if (nowTick < state.cooldownUntilTick) {
                return TriggerResult.denied("veilstep_cooldown", "Veilstep internal cooldown is still active", state.charges, state.cooldownUntilTick);
            }
            if (candidates.isEmpty()) {
                return TriggerResult.denied("veilstep_no_safe_destination", "Veilstep safe-position search produced no candidates", state.charges, state.cooldownUntilTick);
            }

            List<VeilstepCandidateSelector.Candidate> evaluated = new ArrayList<>(candidates.size());
            for (int index = 0; index < candidates.size(); index++) {
                Vec3 candidate = Objects.requireNonNull(candidates.get(index), "candidate");
                MinecraftSafeDestinationResolver.Result result = MinecraftSafeDestinationResolver.evaluate(
                    server,
                    caster,
                    level,
                    candidate.x,
                    candidate.y,
                    candidate.z);
                evaluated.add(new VeilstepCandidateSelector.Candidate(Integer.toString(index), result.facts()));
            }

            var selected = SELECTOR.select(evaluated);
            if (selected.isEmpty()) {
                return TriggerResult.denied(
                    "veilstep_no_safe_destination",
                    "No Veilstep candidate passed authoritative destination validation",
                    state.charges,
                    state.cooldownUntilTick);
            }

            int selectedIndex;
            try {
                selectedIndex = Integer.parseInt(selected.get().destinationId());
            } catch (NumberFormatException corruptSelection) {
                return TriggerResult.denied(
                    "veilstep_selection_invalid",
                    "Veilstep candidate selector returned an invalid internal destination id",
                    state.charges,
                    state.cooldownUntilTick);
            }
            Vec3 landing = candidates.get(selectedIndex);

            // Re-resolve immediately before movement so a block/protection/vehicle change cannot
            // turn a previously-safe candidate into a stale teleport settlement.
            ServerPlayer settlementCaster = server.getPlayerList().getPlayer(casterId);
            if (settlementCaster != caster || !caster.isAlive() || caster.level() != level) {
                return TriggerResult.denied(
                    "veilstep_endpoint_changed",
                    "Veilstep caster changed before teleport settlement",
                    state.charges,
                    state.cooldownUntilTick);
            }
            MinecraftSafeDestinationResolver.Result settlement = MinecraftSafeDestinationResolver.evaluate(
                server,
                caster,
                level,
                landing.x,
                landing.y,
                landing.z);
            if (!settlement.allowed()) {
                return TriggerResult.denied(
                    "veilstep_no_safe_destination",
                    "Selected Veilstep destination became unsafe before settlement",
                    state.charges,
                    state.cooldownUntilTick);
            }

            boolean teleported = caster.teleportTo(
                level,
                landing.x,
                landing.y,
                landing.z,
                Set.<RelativeMovement>of(),
                caster.getYRot(),
                caster.getXRot());
            if (!teleported) {
                return TriggerResult.denied(
                    "veilstep_teleport_failed",
                    "Minecraft rejected Veilstep teleport settlement",
                    state.charges,
                    state.cooldownUntilTick);
            }

            state.charges--;
            state.cooldownUntilTick = cooldownUntil;
            return TriggerResult.allowed(state.charges, state.cooldownUntilTick);
        }
    }

    private static TriggerResult denied(
            MinecraftServer server,
            UUID casterId,
            String code,
            String detail
    ) {
        synchronized (STATES) {
            Map<UUID, State> byCaster = STATES.get(server);
            State state = byCaster == null ? null : byCaster.get(casterId);
            return TriggerResult.denied(
                code,
                detail,
                state == null ? 0 : state.charges,
                state == null ? 0L : state.cooldownUntilTick);
        }
    }

    private static void onPlayerLoggedOut(PlayerEvent.PlayerLoggedOutEvent event) {
        MinecraftServer server = event.getEntity().level().getServer();
        if (server == null) return;
        synchronized (STATES) {
            Map<UUID, State> byCaster = STATES.get(server);
            if (byCaster == null) return;
            byCaster.remove(event.getEntity().getUUID());
            if (byCaster.isEmpty()) STATES.remove(server);
        }
    }

    private static void onServerStopped(ServerStoppedEvent event) {
        STATES.remove(event.getServer());
    }

    public record TriggerResult(
        ArcanaDecision decision,
        boolean teleported,
        int remainingCharges,
        long cooldownUntilTick
    ) {
        public TriggerResult {
            Objects.requireNonNull(decision, "decision");
            if (remainingCharges < 0 || cooldownUntilTick < 0L) {
                throw new IllegalArgumentException("Veilstep result state cannot be negative");
            }
            if (decision.allowed() != teleported) {
                throw new IllegalArgumentException("Veilstep allow result must correspond to successful teleport");
            }
        }

        private static TriggerResult allowed(int remainingCharges, long cooldownUntilTick) {
            return new TriggerResult(ArcanaDecision.allow(), true, remainingCharges, cooldownUntilTick);
        }

        private static TriggerResult denied(
                String code,
                String detail,
                int remainingCharges,
                long cooldownUntilTick
        ) {
            return new TriggerResult(
                ArcanaDecision.deny(code, detail),
                false,
                remainingCharges,
                cooldownUntilTick);
        }
    }

    private static final class State {
        private int charges;
        private final int maxCharges;
        private long cooldownUntilTick;

        private State(int charges, int maxCharges, long cooldownUntilTick) {
            this.charges = charges;
            this.maxCharges = maxCharges;
            this.cooldownUntilTick = cooldownUntilTick;
        }
    }
}
