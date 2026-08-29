package dev.gustavopere.blackarcana.content.blood;

import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;
import java.util.UUID;

/**
 * Bounded link runtime for Sympathetic Wound. Only DIRECT damage may be mirrored;
 * generated mirror events are explicitly marked SHARED and therefore cannot recurse.
 */
public final class SympatheticWoundService {
    public static final int ABSOLUTE_MAX_LINKS = 4096;

    private final int maxLinks;
    private final Map<UUID, LinkState> byCaster = new LinkedHashMap<>();

    public SympatheticWoundService(int maxLinks) {
        if (maxLinks <= 0 || maxLinks > ABSOLUTE_MAX_LINKS) {
            throw new IllegalArgumentException("maxLinks outside absolute bounds");
        }
        this.maxLinks = maxLinks;
    }

    public synchronized void bind(LinkSpec spec) {
        Objects.requireNonNull(spec, "spec");
        if (!byCaster.containsKey(spec.casterId()) && byCaster.size() >= maxLinks) {
            throw new IllegalStateException("Sympathetic Wound link registry is full");
        }
        byCaster.put(spec.casterId(), new LinkState(spec, spec.lifetimeDamageBudget()));
    }

    public synchronized boolean breakLink(UUID casterId) {
        return byCaster.remove(Objects.requireNonNull(casterId, "casterId")) != null;
    }

    public synchronized Optional<DamageEvent> mirror(DamageEvent incoming, long nowTick) {
        Objects.requireNonNull(incoming, "incoming");
        if (incoming.provenance() != DamageProvenance.DIRECT) return Optional.empty();
        LinkState state = byCaster.get(incoming.victimId());
        if (state == null) return Optional.empty();
        if (nowTick >= state.spec.expiresAtTick() || state.remainingBudget <= 0.0D) {
            byCaster.remove(incoming.victimId());
            return Optional.empty();
        }

        double mirrored = Math.min(
            incoming.amount() * state.spec.mirrorFraction(),
            Math.min(state.spec.perEventCap(), state.remainingBudget));
        if (mirrored <= 0.0D) return Optional.empty();
        state.remainingBudget -= mirrored;
        DamageEvent result = new DamageEvent(
            incoming.eventId(),
            state.spec.targetId(),
            mirrored,
            DamageProvenance.SYMPATHETIC_WOUND);
        if (state.remainingBudget <= 0.0D) byCaster.remove(incoming.victimId());
        return Optional.of(result);
    }

    public synchronized int pruneExpired(long nowTick) {
        if (nowTick < 0L) throw new IllegalArgumentException("nowTick cannot be negative");
        int removed = 0;
        Iterator<LinkState> iterator = byCaster.values().iterator();
        while (iterator.hasNext()) {
            LinkState state = iterator.next();
            if (nowTick >= state.spec.expiresAtTick() || state.remainingBudget <= 0.0D) {
                iterator.remove();
                removed++;
            }
        }
        return removed;
    }

    public synchronized int size() {
        return byCaster.size();
    }

    public synchronized double remainingBudget(UUID casterId) {
        LinkState state = byCaster.get(Objects.requireNonNull(casterId, "casterId"));
        return state == null ? 0.0D : state.remainingBudget;
    }

    public record LinkSpec(
        UUID casterId,
        UUID targetId,
        long expiresAtTick,
        double mirrorFraction,
        double perEventCap,
        double lifetimeDamageBudget
    ) {
        public LinkSpec {
            Objects.requireNonNull(casterId, "casterId");
            Objects.requireNonNull(targetId, "targetId");
            if (casterId.equals(targetId)) throw new IllegalArgumentException("caster and target must differ");
            if (expiresAtTick < 0L) throw new IllegalArgumentException("expiresAtTick cannot be negative");
            boundedPositive(mirrorFraction, BloodSafetyCeilings.MAX_SYMPATHETIC_MIRROR_FRACTION, "mirrorFraction");
            boundedPositive(perEventCap, BloodSafetyCeilings.MAX_SYMPATHETIC_DAMAGE_PER_EVENT, "perEventCap");
            boundedPositive(lifetimeDamageBudget, BloodSafetyCeilings.MAX_SYMPATHETIC_LIFETIME_BUDGET, "lifetimeDamageBudget");
        }
    }

    public record DamageEvent(UUID eventId, UUID victimId, double amount, DamageProvenance provenance) {
        public DamageEvent {
            Objects.requireNonNull(eventId, "eventId");
            Objects.requireNonNull(victimId, "victimId");
            Objects.requireNonNull(provenance, "provenance");
            if (!Double.isFinite(amount) || amount <= 0.0D) {
                throw new IllegalArgumentException("damage amount must be finite and positive");
            }
        }
    }

    public enum DamageProvenance {
        DIRECT,
        SYMPATHETIC_WOUND,
        OTHER_PROPAGATED
    }

    private static void boundedPositive(double value, double max, String field) {
        if (!Double.isFinite(value) || value <= 0.0D || value > max) {
            throw new IllegalArgumentException(field + " outside hard bounds");
        }
    }

    private static final class LinkState {
        private final LinkSpec spec;
        private double remainingBudget;

        private LinkState(LinkSpec spec, double remainingBudget) {
            this.spec = spec;
            this.remainingBudget = remainingBudget;
        }
    }
}
