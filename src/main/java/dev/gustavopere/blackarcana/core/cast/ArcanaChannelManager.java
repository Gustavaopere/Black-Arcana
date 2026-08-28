package dev.gustavopere.blackarcana.core.cast;

import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaChannelSpec;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;

import java.util.HashMap;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;
import java.util.UUID;

public final class ArcanaChannelManager {
    private final int maxSessions;
    private final Map<UUID, Session> sessions = new HashMap<>();

    public ArcanaChannelManager(int maxSessions) {
        if (maxSessions <= 0) throw new IllegalArgumentException("maxSessions must be positive");
        this.maxSessions = maxSessions;
    }

    public synchronized ArcanaDecision begin(
            UUID casterId,
            ArcanaCastId castId,
            ArcanaSpellId spellId,
            long serverTick,
            ArcanaChannelSpec spec
    ) {
        return begin(casterId, castId, spellId, 0, serverTick, spec);
    }

    public synchronized ArcanaDecision begin(
            UUID casterId,
            ArcanaCastId castId,
            ArcanaSpellId spellId,
            int loadoutSlot,
            long serverTick,
            ArcanaChannelSpec spec
    ) {
        Objects.requireNonNull(casterId, "casterId");
        Objects.requireNonNull(castId, "castId");
        Objects.requireNonNull(spellId, "spellId");
        Objects.requireNonNull(spec, "spec");
        if (loadoutSlot < 0 || loadoutSlot >= ArcanaCastRequest.MAX_LOADOUT_SLOTS) {
            throw new IllegalArgumentException("loadoutSlot outside cast request bounds");
        }
        if (serverTick < 0L) throw new IllegalArgumentException("serverTick cannot be negative");
        pruneExpired(serverTick);

        if (sessions.containsKey(casterId)) {
            return ArcanaDecision.deny("channel_already_active", "caster already has an active channel");
        }
        if (sessions.size() >= maxSessions) {
            return ArcanaDecision.deny("channel_manager_saturated", "channel session capacity reached");
        }

        sessions.put(casterId, new Session(castId, spellId, loadoutSlot, serverTick, spec));
        return ArcanaDecision.allow();
    }

    public synchronized ReleaseResult release(UUID casterId, ArcanaCastId castId, long serverTick) {
        Objects.requireNonNull(casterId, "casterId");
        Objects.requireNonNull(castId, "castId");
        if (serverTick < 0L) throw new IllegalArgumentException("serverTick cannot be negative");

        Session session = sessions.get(casterId);
        if (session == null) {
            return ReleaseResult.denied("channel_missing", "no active channel for caster");
        }
        if (!session.castId().equals(castId)) {
            return ReleaseResult.denied("channel_id_mismatch", "release does not match active channel");
        }
        if (serverTick < session.startedAtTick()) {
            return ReleaseResult.denied("clock_regression", "server tick precedes channel start");
        }

        long elapsed = serverTick - session.startedAtTick();
        if (elapsed > session.spec().maximumTicks()) {
            sessions.remove(casterId);
            return ReleaseResult.denied("channel_expired", "channel exceeded maximum duration");
        }
        if (elapsed < session.spec().minimumTicks()) {
            return ReleaseResult.denied("channel_too_short", "channel has not reached minimum duration");
        }

        sessions.remove(casterId);
        return ReleaseResult.released(new ReleasedChannel(
                session.castId(), session.spellId(), session.loadoutSlot(), elapsed));
    }

    public synchronized boolean cancel(UUID casterId, ArcanaCastId castId) {
        Objects.requireNonNull(casterId, "casterId");
        Objects.requireNonNull(castId, "castId");
        Session session = sessions.get(casterId);
        if (session == null || !session.castId().equals(castId)) return false;
        sessions.remove(casterId);
        return true;
    }

    public synchronized int pruneExpired(long serverTick) {
        if (serverTick < 0L) throw new IllegalArgumentException("serverTick cannot be negative");
        int before = sessions.size();
        sessions.entrySet().removeIf(entry -> {
            Session session = entry.getValue();
            return serverTick >= session.startedAtTick()
                    && serverTick - session.startedAtTick() > session.spec().maximumTicks();
        });
        return before - sessions.size();
    }

    public synchronized int activeSessions() {
        return sessions.size();
    }

    private record Session(
            ArcanaCastId castId,
            ArcanaSpellId spellId,
            int loadoutSlot,
            long startedAtTick,
            ArcanaChannelSpec spec
    ) { }

    public record ReleasedChannel(
            ArcanaCastId castId,
            ArcanaSpellId spellId,
            int loadoutSlot,
            long channelTicks
    ) { }

    public record ReleaseResult(ArcanaDecision decision, Optional<ReleasedChannel> released) {
        public ReleaseResult {
            Objects.requireNonNull(decision, "decision");
            Objects.requireNonNull(released, "released");
            if (decision.allowed() != released.isPresent()) {
                throw new IllegalArgumentException("allowed release must contain released channel and denial must not");
            }
        }

        public static ReleaseResult denied(String code, String detail) {
            return new ReleaseResult(ArcanaDecision.deny(code, detail), Optional.empty());
        }

        public static ReleaseResult released(ReleasedChannel channel) {
            return new ReleaseResult(ArcanaDecision.allow(), Optional.of(Objects.requireNonNull(channel, "channel")));
        }
    }
}
