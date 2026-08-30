package dev.gustavopere.blackarcana.integration.neoforge;

import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.content.forbidden.DomainReturnPoint;
import dev.gustavopere.blackarcana.content.forbidden.DomainReturnSelector;
import dev.gustavopere.blackarcana.content.forbidden.ForbiddenDomainSafetyCeilings;
import dev.gustavopere.blackarcana.content.forbidden.InnerDominionSessionJournal;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.event.server.ServerStoppedEvent;

import java.util.ArrayList;
import java.util.Collections;
import java.util.IdentityHashMap;
import java.util.LinkedHashMap;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;
import java.util.UUID;

/**
 * Server-authoritative localized lifecycle boundary for Inner Dominion.
 *
 * Stage 07 deliberately keeps the domain in the already-loaded world instead of creating
 * dynamic dimensions. Opening captures immutable server-derived return routes for a bounded
 * participant set. Closing revalidates every route immediately before movement and removes
 * the journal entry only after every loaded participant has settled successfully.
 *
 * Recovery obligations are mirrored into overworld SavedData after every journal mutation.
 * A volatile-state cache miss therefore rehydrates the bounded journal rather than silently
 * losing sessions after a restart or runtime cache reset.
 */
public final class MinecraftInnerDominionRuntime {
    private static final double SETTLED_EPSILON_SQUARED = 1.0E-6D;
    private static final int[][] FALLBACK_OFFSETS = {
        {1, 0}, {-1, 0}, {0, 1}, {0, -1},
        {1, 1}, {1, -1}, {-1, 1}, {-1, -1}
    };

    private static final Map<MinecraftServer, State> STATES =
        Collections.synchronizedMap(new IdentityHashMap<>());

    private MinecraftInnerDominionRuntime() { }

    public static void register(IEventBus gameBus) {
        Objects.requireNonNull(gameBus, "gameBus");
        gameBus.addListener(MinecraftInnerDominionRuntime::onServerStopped);
    }

    public static OpenSessionResult openLocalizedSession(
            MinecraftServer server,
            UUID sessionId,
            UUID ownerId,
            List<UUID> participantIds,
            double radius,
            long durationTicks
    ) {
        Objects.requireNonNull(server, "server");
        Objects.requireNonNull(sessionId, "sessionId");
        Objects.requireNonNull(ownerId, "ownerId");
        Objects.requireNonNull(participantIds, "participantIds");

        if (!Double.isFinite(radius) || radius <= 0.0D
                || radius > ForbiddenDomainSafetyCeilings.MAX_RADIUS_BLOCKS) {
            return OpenSessionResult.denied(
                "inner_dominion_radius_config",
                "Inner Dominion radius is outside the hard forbidden-domain ceiling");
        }
        if (durationTicks <= 0L || durationTicks > ForbiddenDomainSafetyCeilings.MAX_DURATION_TICKS) {
            return OpenSessionResult.denied(
                "inner_dominion_duration",
                "Inner Dominion duration is outside the hard forbidden-domain ceiling");
        }
        if (participantIds.isEmpty() || participantIds.size() > ForbiddenDomainSafetyCeilings.MAX_PARTICIPANTS) {
            return OpenSessionResult.denied(
                "inner_dominion_participants",
                "Inner Dominion participant request is empty or exceeds the hard cap");
        }

        LinkedHashSet<UUID> uniqueParticipants = new LinkedHashSet<>();
        for (UUID participantId : participantIds) {
            if (participantId == null) {
                return OpenSessionResult.denied(
                    "inner_dominion_participants",
                    "Inner Dominion participant ids cannot be null");
            }
            uniqueParticipants.add(participantId);
        }
        if (!uniqueParticipants.contains(ownerId)) {
            return OpenSessionResult.denied(
                "inner_dominion_owner_missing",
                "Inner Dominion owner must be included in the participant set");
        }
        if (uniqueParticipants.size() > ForbiddenDomainSafetyCeilings.MAX_PARTICIPANTS) {
            return OpenSessionResult.denied(
                "inner_dominion_participants",
                "Inner Dominion unique participant set exceeds the hard cap");
        }

        ServerPlayer owner = loadedAlivePlayer(server, ownerId);
        if (owner == null) {
            return OpenSessionResult.denied(
                "inner_dominion_owner_unavailable",
                "Inner Dominion owner must be a loaded living server player");
        }

        String dimensionId = owner.serverLevel().dimension().location().toString();
        double radiusSquared = radius * radius;
        Map<UUID, ServerPlayer> participants = new LinkedHashMap<>();

        // Validate the requested localized participant set before preparing return routes so
        // radius/dimension/availability diagnostics are never masked by fallback preparation.
        for (UUID participantId : uniqueParticipants) {
            ServerPlayer participant = loadedAlivePlayer(server, participantId);
            if (participant == null) {
                return OpenSessionResult.denied(
                    "inner_dominion_participant_unavailable",
                    "Every Inner Dominion participant must be loaded and alive when the session opens");
            }
            if (!participant.serverLevel().dimension().location().toString().equals(dimensionId)) {
                return OpenSessionResult.denied(
                    "inner_dominion_dimension",
                    "Localized Inner Dominion participants must begin in the owner's dimension");
            }
            if (participant.distanceToSqr(owner) > radiusSquared) {
                return OpenSessionResult.denied(
                    "inner_dominion_radius",
                    "Inner Dominion participant lies outside the requested localized radius");
            }
            participants.put(participantId, participant);
        }

        Map<UUID, InnerDominionSessionJournal.ReturnRoute> routes = new LinkedHashMap<>();
        for (Map.Entry<UUID, ServerPlayer> entry : participants.entrySet()) {
            ServerPlayer participant = entry.getValue();
            DomainReturnPoint origin = point(participant);
            DomainReturnPoint fallback = findFallback(server, participant, origin).orElse(null);
            if (fallback == null) {
                return OpenSessionResult.denied(
                    "inner_dominion_return_route",
                    "Inner Dominion could not capture a distinct loaded and protected fallback route");
            }
            routes.put(entry.getKey(), new InnerDominionSessionJournal.ReturnRoute(origin, fallback));
        }

        long now = server.overworld().getGameTime();
        State state = state(server);
        InnerDominionSessionJournal.OpenResult opened = state.journal.open(
            sessionId,
            ownerId,
            now,
            durationTicks,
            routes);
        return switch (opened) {
            case OPENED -> {
                state.persist();
                yield new OpenSessionResult(ArcanaDecision.allow(), true, routes.size());
            }
            case DUPLICATE_SESSION -> OpenSessionResult.denied(
                "inner_dominion_duplicate_session",
                "Inner Dominion session id is already active");
            case NESTED_PARTICIPANT -> OpenSessionResult.denied(
                "inner_dominion_nested_participant",
                "Inner Dominion participants cannot join nested domain sessions");
            case CAPACITY -> OpenSessionResult.denied(
                "inner_dominion_capacity",
                "Server Inner Dominion session capacity is full");
            case INVALID_DURATION -> OpenSessionResult.denied(
                "inner_dominion_invalid_session",
                "Inner Dominion session failed bounded journal validation");
        };
    }

    public static CloseSessionResult closeSession(MinecraftServer server, UUID sessionId) {
        Objects.requireNonNull(server, "server");
        Objects.requireNonNull(sessionId, "sessionId");
        State state = state(server);

        InnerDominionSessionJournal.Session session = state.journal.snapshot().stream()
            .filter(candidate -> candidate.sessionId().equals(sessionId))
            .findFirst()
            .orElse(null);
        if (session == null) {
            return CloseSessionResult.denied(
                "inner_dominion_session_missing",
                "Inner Dominion session is not active");
        }

        List<Settlement> settlements = new ArrayList<>(session.participants().size());
        int fallbackReturns = 0;
        for (Map.Entry<UUID, InnerDominionSessionJournal.ReturnRoute> entry : session.participants().entrySet()) {
            ServerPlayer participant = loadedAlivePlayer(server, entry.getKey());
            if (participant == null) {
                return CloseSessionResult.denied(
                    "inner_dominion_participant_unavailable",
                    "Inner Dominion retains the journal while a participant cannot be safely returned");
            }
            InnerDominionSessionJournal.ReturnRoute route = entry.getValue();

            // A participant already standing at the captured origin is already settled; running
            // that no-op through landing collision checks can falsely classify its own occupied
            // position as blocked. Only participants that actually need movement use the shared
            // safe-destination resolver.
            if (atPoint(participant, route.origin())) {
                settlements.add(new Settlement(participant, route.origin(), false, false));
                continue;
            }

            DomainReturnPoint chosen = DomainReturnSelector.choose(
                route.origin(),
                route.fallback(),
                point -> safeDestination(server, participant, point)).orElse(null);
            if (chosen == null) {
                return CloseSessionResult.denied(
                    "inner_dominion_return_unavailable",
                    "No validated Inner Dominion return route is currently available");
            }
            boolean usedFallback = !chosen.equals(route.origin());
            if (usedFallback) fallbackReturns++;
            settlements.add(new Settlement(participant, chosen, usedFallback, true));
        }

        // Immediate all-participant revalidation before the first movement mutation.
        for (Settlement settlement : settlements) {
            if (!settlement.movementRequired()) {
                if (!atPoint(settlement.player(), settlement.destination())) {
                    return CloseSessionResult.denied(
                        "inner_dominion_return_changed",
                        "Inner Dominion settled participant moved before close settlement");
                }
                continue;
            }
            if (!safeDestination(server, settlement.player(), settlement.destination())) {
                return CloseSessionResult.denied(
                    "inner_dominion_return_changed",
                    "Inner Dominion return destination changed before settlement");
            }
        }

        try {
            for (Settlement settlement : settlements) {
                if (!settlement.movementRequired()) continue;
                DomainReturnPoint destination = settlement.destination();
                settlement.player().setPos(destination.x(), destination.y(), destination.z());
            }
        } catch (RuntimeException movementFailure) {
            return CloseSessionResult.denied(
                "inner_dominion_return_failed",
                "Inner Dominion return movement failed; recovery journal remains active");
        }

        if (state.journal.close(sessionId).isEmpty()) {
            return CloseSessionResult.denied(
                "inner_dominion_session_changed",
                "Inner Dominion session changed before close settlement");
        }
        state.persist();
        return new CloseSessionResult(
            ArcanaDecision.allow(),
            true,
            settlements.size(),
            fallbackReturns);
    }

    public static ParticipantRecoveryResult recoverParticipant(MinecraftServer server, UUID participantId) {
        Objects.requireNonNull(server, "server");
        Objects.requireNonNull(participantId, "participantId");
        State state = state(server);

        InnerDominionSessionJournal.Session session = state.journal.snapshot().stream()
            .filter(candidate -> candidate.participants().containsKey(participantId))
            .findFirst()
            .orElse(null);
        if (session == null) {
            return ParticipantRecoveryResult.denied(
                "inner_dominion_participant_not_pending",
                "Player has no pending Inner Dominion return obligation");
        }

        ServerPlayer participant = loadedAlivePlayer(server, participantId);
        if (participant == null) {
            return ParticipantRecoveryResult.denied(
                "inner_dominion_participant_unavailable",
                "Inner Dominion participant must be loaded and alive before recovery settlement");
        }

        InnerDominionSessionJournal.ReturnRoute route = session.participants().get(participantId);
        DomainReturnPoint destination;
        boolean usedFallback;
        boolean movementRequired;
        if (atPoint(participant, route.origin())) {
            destination = route.origin();
            usedFallback = false;
            movementRequired = false;
        } else {
            destination = DomainReturnSelector.choose(
                route.origin(),
                route.fallback(),
                point -> safeDestination(server, participant, point)).orElse(null);
            if (destination == null) {
                return ParticipantRecoveryResult.denied(
                    "inner_dominion_return_unavailable",
                    "No validated Inner Dominion return route is currently available");
            }
            usedFallback = !destination.equals(route.origin());
            movementRequired = true;
        }

        if (movementRequired && !safeDestination(server, participant, destination)) {
            return ParticipantRecoveryResult.denied(
                "inner_dominion_return_changed",
                "Inner Dominion return destination changed before participant recovery settlement");
        }
        if (!movementRequired && !atPoint(participant, destination)) {
            return ParticipantRecoveryResult.denied(
                "inner_dominion_return_changed",
                "Inner Dominion participant moved before recovery settlement");
        }

        try {
            if (movementRequired) {
                participant.setPos(destination.x(), destination.y(), destination.z());
            }
        } catch (RuntimeException movementFailure) {
            return ParticipantRecoveryResult.denied(
                "inner_dominion_return_failed",
                "Inner Dominion participant return movement failed; recovery obligation remains active");
        }

        InnerDominionSessionJournal.SettleResult settled = state.journal.settleParticipant(
            session.sessionId(),
            participantId);
        return switch (settled) {
            case PARTICIPANT_SETTLED -> {
                state.persist();
                yield new ParticipantRecoveryResult(ArcanaDecision.allow(), true, false, usedFallback);
            }
            case SESSION_CLOSED -> {
                state.persist();
                yield new ParticipantRecoveryResult(ArcanaDecision.allow(), true, true, usedFallback);
            }
            case SESSION_MISSING, PARTICIPANT_MISSING -> ParticipantRecoveryResult.denied(
                "inner_dominion_session_changed",
                "Inner Dominion recovery obligation changed before participant settlement");
        };
    }

    public static int activeSessions(MinecraftServer server) {
        Objects.requireNonNull(server, "server");
        return state(server).journal.activeSessions();
    }

    private static Optional<DomainReturnPoint> findFallback(
            MinecraftServer server,
            ServerPlayer participant,
            DomainReturnPoint origin
    ) {
        for (int[] offset : FALLBACK_OFFSETS) {
            DomainReturnPoint candidate = new DomainReturnPoint(
                origin.dimensionId(),
                origin.x() + offset[0],
                origin.y(),
                origin.z() + offset[1]);
            if (safeDestination(server, participant, candidate)) return Optional.of(candidate);
        }
        return Optional.empty();
    }

    private static boolean atPoint(ServerPlayer player, DomainReturnPoint point) {
        if (!player.serverLevel().dimension().location().toString().equals(point.dimensionId())) return false;
        double dx = player.getX() - point.x();
        double dy = player.getY() - point.y();
        double dz = player.getZ() - point.z();
        return dx * dx + dy * dy + dz * dz <= SETTLED_EPSILON_SQUARED;
    }

    private static State state(MinecraftServer server) {
        synchronized (STATES) {
            return STATES.computeIfAbsent(server, State::new);
        }
    }

    private static ServerPlayer loadedAlivePlayer(MinecraftServer server, UUID playerId) {
        ServerPlayer player = server.getPlayerList().getPlayer(playerId);
        return player != null && player.isAlive() ? player : null;
    }

    private static DomainReturnPoint point(ServerPlayer player) {
        return new DomainReturnPoint(
            player.serverLevel().dimension().location().toString(),
            player.getX(),
            player.getY(),
            player.getZ());
    }

    private static boolean safeDestination(
            MinecraftServer server,
            ServerPlayer participant,
            DomainReturnPoint point
    ) {
        ServerLevel level = loadedLevel(server, point.dimensionId());
        if (level == null) return false;
        return MinecraftSafeDestinationResolver.evaluate(
            server,
            participant,
            level,
            point.x(),
            point.y(),
            point.z()).allowed();
    }

    private static ServerLevel loadedLevel(MinecraftServer server, String dimensionId) {
        for (ServerLevel level : server.getAllLevels()) {
            if (level.dimension().location().toString().equals(dimensionId)) return level;
        }
        return null;
    }

    private static void onServerStopped(ServerStoppedEvent event) {
        STATES.remove(event.getServer());
    }

    private record Settlement(
        ServerPlayer player,
        DomainReturnPoint destination,
        boolean fallback,
        boolean movementRequired
    ) {
        private Settlement {
            Objects.requireNonNull(player, "player");
            Objects.requireNonNull(destination, "destination");
            if (!movementRequired && fallback) {
                throw new IllegalArgumentException("no-op Inner Dominion settlement cannot report fallback movement");
            }
        }
    }

    private static final class State {
        private final InnerDominionSavedData savedData;
        private final InnerDominionSessionJournal journal;

        private State(MinecraftServer server) {
            savedData = server.overworld().getDataStorage().computeIfAbsent(
                InnerDominionSavedData.factory(),
                InnerDominionSavedData.DATA_NAME);
            journal = new InnerDominionSessionJournal(
                ForbiddenDomainSafetyCeilings.MAX_ACTIVE_SESSIONS,
                ForbiddenDomainSafetyCeilings.MAX_PARTICIPANTS,
                ForbiddenDomainSafetyCeilings.MAX_DURATION_TICKS);
            journal.restore(savedData.sessions(), server.overworld().getGameTime());
        }

        private void persist() {
            savedData.replaceSessions(journal.snapshot());
        }
    }

    public record OpenSessionResult(ArcanaDecision decision, boolean opened, int participantCount) {
        public OpenSessionResult {
            Objects.requireNonNull(decision, "decision");
            if (!decision.allowed() && opened) {
                throw new IllegalArgumentException("denied Inner Dominion open cannot report success");
            }
            if (participantCount < 0 || participantCount > ForbiddenDomainSafetyCeilings.MAX_PARTICIPANTS) {
                throw new IllegalArgumentException("participantCount outside Inner Dominion bounds");
            }
        }

        private static OpenSessionResult denied(String code, String detail) {
            return new OpenSessionResult(ArcanaDecision.deny(code, detail), false, 0);
        }
    }

    public record CloseSessionResult(
        ArcanaDecision decision,
        boolean closed,
        int returnedParticipants,
        int fallbackReturns
    ) {
        public CloseSessionResult {
            Objects.requireNonNull(decision, "decision");
            if (!decision.allowed() && closed) {
                throw new IllegalArgumentException("denied Inner Dominion close cannot report success");
            }
            if (returnedParticipants < 0 || returnedParticipants > ForbiddenDomainSafetyCeilings.MAX_PARTICIPANTS) {
                throw new IllegalArgumentException("returnedParticipants outside Inner Dominion bounds");
            }
            if (fallbackReturns < 0 || fallbackReturns > returnedParticipants) {
                throw new IllegalArgumentException("fallbackReturns outside settled participant count");
            }
        }

        private static CloseSessionResult denied(String code, String detail) {
            return new CloseSessionResult(ArcanaDecision.deny(code, detail), false, 0, 0);
        }
    }

    public record ParticipantRecoveryResult(
        ArcanaDecision decision,
        boolean recovered,
        boolean sessionClosed,
        boolean usedFallback
    ) {
        public ParticipantRecoveryResult {
            Objects.requireNonNull(decision, "decision");
            if (!decision.allowed() && (recovered || sessionClosed || usedFallback)) {
                throw new IllegalArgumentException("denied Inner Dominion participant recovery cannot report settlement");
            }
            if (sessionClosed && !recovered) {
                throw new IllegalArgumentException("closed Inner Dominion recovery session must report participant recovery");
            }
            if (usedFallback && !recovered) {
                throw new IllegalArgumentException("Inner Dominion fallback return requires successful recovery");
            }
        }

        private static ParticipantRecoveryResult denied(String code, String detail) {
            return new ParticipantRecoveryResult(ArcanaDecision.deny(code, detail), false, false, false);
        }
    }
}
