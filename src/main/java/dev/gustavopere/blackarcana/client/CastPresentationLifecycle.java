package dev.gustavopere.blackarcana.client;

import dev.gustavopere.blackarcana.api.ArcanaCastId;
import dev.gustavopere.blackarcana.api.ArcanaCastResult;
import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.network.CastResultPayload;

import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;

/**
 * Pure physical-client presentation lifecycle for Stage 05.15.
 *
 * <p>This model owns only bounded audiovisual correlation semantics. It does not perform cast
 * admission, target resolution, world queries, provider calls, rendering, resource spending or
 * cooldown settlement. A local intent is always anticipatory; only server-authored facts may
 * settle it.</p>
 */
public final class CastPresentationLifecycle {
    /** Authority vocabulary frozen by the 05.15 planning contract. */
    public enum Authority {
        LOCAL_INTENT_PRESENTATION,
        SERVER_AUTHORED_FORECAST,
        AUTHORITATIVE_CAST_RESULT,
        SERVER_OWNED_RUNTIME_EVENT,
        CLIENT_DECORATIVE_EFFECT,
        PROVIDER_OWNED_PRESENTATION,
        UNKNOWN_OR_UNAVAILABLE
    }

    /** Minimal state needed by the provider-free intent/result correlation tranche. */
    public enum State {
        ANTICIPATING,
        SUCCEEDED,
        DENIED,
        FAILED
    }

    /**
     * Surface-neutral cue state. Spell identity is optional because an unmatched authoritative
     * result proves its cast result but does not prove which locally visible spell/target it should
     * be attached to.
     */
    public record Cue(
            ArcanaCastId castId,
            Optional<ArcanaSpellId> spellId,
            Authority authority,
            State state,
            long updatedTick
    ) {
        public Cue {
            Objects.requireNonNull(castId, "castId");
            Objects.requireNonNull(spellId, "spellId");
            Objects.requireNonNull(authority, "authority");
            Objects.requireNonNull(state, "state");
        }

        /** True only for facts that may settle a cast presentation. */
        public boolean authoritative() {
            return authority == Authority.AUTHORITATIVE_CAST_RESULT
                    || authority == Authority.SERVER_OWNED_RUNTIME_EVENT;
        }

        public boolean settled() {
            return state != State.ANTICIPATING;
        }
    }

    /** Presentation-only sensory policy. These values never participate in gameplay validation. */
    public record SensoryPolicy(double particleDensity, boolean reducedMotion, boolean reducedFlashes) {
        public SensoryPolicy {
            if (!Double.isFinite(particleDensity) || particleDensity < 0.0D || particleDensity > 1.0D) {
                throw new IllegalArgumentException("particleDensity must be finite and within [0, 1]");
            }
        }

        public boolean decorativeParticlesEnabled() {
            return particleDensity > 0.0D;
        }

        public boolean nonessentialMotionAllowed() {
            return !reducedMotion;
        }

        public boolean flashHeavyEffectsAllowed() {
            return !reducedFlashes;
        }
    }

    private final int maxEntries;
    private final long staleAgeTicks;
    private final Map<ArcanaCastId, Cue> cues = new LinkedHashMap<>();

    public CastPresentationLifecycle(int maxEntries, long staleAgeTicks) {
        if (maxEntries <= 0) throw new IllegalArgumentException("maxEntries must be positive");
        if (staleAgeTicks <= 0L) throw new IllegalArgumentException("staleAgeTicks must be positive");
        this.maxEntries = maxEntries;
        this.staleAgeTicks = staleAgeTicks;
    }

    /**
     * Records bounded local anticipation. Re-observing an existing cast id is idempotent and can
     * never downgrade a settled authoritative result back to anticipation.
     */
    public Cue recordLocalIntent(ArcanaCastId castId, ArcanaSpellId spellId, long tick) {
        Objects.requireNonNull(castId, "castId");
        Objects.requireNonNull(spellId, "spellId");
        Cue existing = cues.get(castId);
        if (existing != null) return existing;

        Cue cue = new Cue(
                castId,
                Optional.of(spellId),
                Authority.LOCAL_INTENT_PRESENTATION,
                State.ANTICIPATING,
                tick);
        cues.put(castId, cue);
        enforceEntryBound();
        return cue;
    }

    /**
     * Settles a cast from the authoritative generic result contract. If no matching local intent is
     * present, spell identity stays unavailable rather than being guessed from current selection or aim.
     */
    public Cue acceptAuthoritativeResult(CastResultPayload payload, long tick) {
        Objects.requireNonNull(payload, "payload");
        ArcanaCastId castId = ArcanaCastId.parse(payload.castId());
        Cue existing = cues.get(castId);
        if (existing != null && existing.settled()) return existing;

        Optional<ArcanaSpellId> spellId = existing == null ? Optional.empty() : existing.spellId();
        ArcanaCastResult.Status status = ArcanaCastResult.Status.valueOf(payload.status());
        State state = switch (status) {
            case SUCCESS -> State.SUCCEEDED;
            case EFFECT_FAILED -> State.FAILED;
            case DENIED_INGRESS,
                    DENIED_IDENTITY,
                    DENIED_REPLAY,
                    DENIED_CHANNEL,
                    DENIED_PROGRESSION,
                    DENIED_COOLDOWN,
                    DENIED_TARGET,
                    DENIED_COST,
                    DENIED_WORLD_POLICY,
                    DENIED_HAZARD -> State.DENIED;
        };

        Cue cue = new Cue(
                castId,
                spellId,
                Authority.AUTHORITATIVE_CAST_RESULT,
                state,
                tick);
        cues.put(castId, cue);
        enforceEntryBound();
        return cue;
    }

    public Optional<Cue> find(ArcanaCastId castId) {
        return Optional.ofNullable(cues.get(Objects.requireNonNull(castId, "castId")));
    }

    public int size() {
        return cues.size();
    }

    /** Removes entries strictly older than the configured maximum age. */
    public void evictStale(long currentTick) {
        Iterator<Map.Entry<ArcanaCastId, Cue>> iterator = cues.entrySet().iterator();
        while (iterator.hasNext()) {
            Cue cue = iterator.next().getValue();
            if (currentTick - cue.updatedTick() > staleAgeTicks) iterator.remove();
        }
    }

    /** Session/resource teardown hook; no presentation correlation survives this call. */
    public void clear() {
        cues.clear();
    }

    private void enforceEntryBound() {
        while (cues.size() > maxEntries) {
            Iterator<ArcanaCastId> iterator = cues.keySet().iterator();
            if (!iterator.hasNext()) return;
            iterator.next();
            iterator.remove();
        }
    }
}
