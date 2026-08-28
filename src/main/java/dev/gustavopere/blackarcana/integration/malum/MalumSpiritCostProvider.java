package dev.gustavopere.blackarcana.integration.malum;

import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaCost;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.api.ArcanaServices.CostProvider;
import dev.gustavopere.blackarcana.api.ArcanaServices.CostReservation;

import java.util.Objects;
import java.util.UUID;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.regex.Pattern;

/** Transactional Black Arcana cost provider backed by discrete Malum spirit shards. */
public final class MalumSpiritCostProvider implements CostProvider {
    public static final int ABSOLUTE_MAX_SPIRIT_COST = 64;
    private static final Pattern AFFINITY = Pattern.compile("[a-z0-9_./-]{1,48}");

    private final MalumSpiritAccess access;

    public MalumSpiritCostProvider(MalumSpiritAccess access) {
        this.access = Objects.requireNonNull(access, "access");
    }

    @Override
    public ArcanaDecision check(ArcanaCastRequest request) {
        Objects.requireNonNull(request, "request");
        ParsedCost parsed;
        try {
            parsed = parse(request.spell().cost());
        } catch (RuntimeException failure) {
            return ArcanaDecision.deny("malum_spirit_cost_invalid", failure.getMessage());
        }

        int available;
        try {
            available = access.count(request.context().casterId(), parsed.affinity());
        } catch (RuntimeException failure) {
            return ArcanaDecision.deny(
                "malum_spirit_query_failed",
                "Malum spirit inventory could not be queried: " + failure.getClass().getSimpleName());
        }
        if (available < parsed.amount()) {
            return ArcanaDecision.deny(
                "insufficient_malum_spirits",
                "Requires " + parsed.amount() + " " + parsed.affinity() + " spirits but only " + available + " are available");
        }
        return ArcanaDecision.allow();
    }

    @Override
    public CostReservation reserve(ArcanaCastRequest request) {
        Objects.requireNonNull(request, "request");
        ArcanaDecision preflight = check(request);
        if (!preflight.allowed()) return new DeniedReservation(preflight);

        ParsedCost parsed;
        try {
            parsed = parse(request.spell().cost());
        } catch (RuntimeException failure) {
            return new DeniedReservation(ArcanaDecision.deny("malum_spirit_cost_invalid", failure.getMessage()));
        }
        if (parsed.amount() == 0) return NoOpReservation.INSTANCE;

        UUID casterId = request.context().casterId();
        ArcanaDecision deducted;
        try {
            deducted = Objects.requireNonNull(
                access.adjust(casterId, parsed.affinity(), -parsed.amount()),
                "spirit adjustment decision");
        } catch (RuntimeException failure) {
            deducted = ArcanaDecision.deny(
                "malum_spirit_reservation_failed",
                "Malum spirit reservation failed: " + failure.getClass().getSimpleName());
        }
        if (!deducted.allowed()) return new DeniedReservation(deducted);
        return new SpiritReservation(access, casterId, parsed.affinity(), parsed.amount());
    }

    static ParsedCost parse(ArcanaCost cost) {
        Objects.requireNonNull(cost, "cost");
        if (!cost.resourceId().startsWith(MalumIntegrationIds.RESOURCE_PREFIX)) {
            throw new IllegalArgumentException("resource is not a Malum spirit affinity");
        }
        if (cost.unit() != ArcanaCost.Unit.FLAT) {
            throw new IllegalArgumentException("Malum spirit costs must be flat discrete counts");
        }
        String affinity = cost.resourceId().substring(MalumIntegrationIds.RESOURCE_PREFIX.length());
        if (!AFFINITY.matcher(affinity).matches()) {
            throw new IllegalArgumentException("invalid Malum spirit affinity");
        }
        if (cost.amount() != Math.rint(cost.amount())) {
            throw new IllegalArgumentException("Malum spirit costs must be whole shard counts");
        }
        int amount = Math.toIntExact((long) cost.amount());
        if (amount < 0 || amount > ABSOLUTE_MAX_SPIRIT_COST) {
            throw new IllegalArgumentException("Malum spirit cost exceeds bounded shard limit");
        }
        return new ParsedCost(affinity, amount);
    }

    record ParsedCost(String affinity, int amount) { }

    private record DeniedReservation(ArcanaDecision decision) implements CostReservation {
        private DeniedReservation {
            Objects.requireNonNull(decision, "decision");
            if (decision.allowed()) throw new IllegalArgumentException("denied reservation requires denial decision");
        }
        @Override public void commit() { throw new IllegalStateException("cannot commit denied spirit reservation"); }
        @Override public void refund() { }
    }

    private enum NoOpReservation implements CostReservation {
        INSTANCE;
        @Override public ArcanaDecision decision() { return ArcanaDecision.allow(); }
        @Override public void commit() { }
        @Override public void refund() { }
    }

    private static final class SpiritReservation implements CostReservation {
        private final MalumSpiritAccess access;
        private final UUID casterId;
        private final String affinity;
        private final int amount;
        private final AtomicBoolean terminal = new AtomicBoolean();

        private SpiritReservation(MalumSpiritAccess access, UUID casterId, String affinity, int amount) {
            this.access = access;
            this.casterId = casterId;
            this.affinity = affinity;
            this.amount = amount;
        }

        @Override public ArcanaDecision decision() { return ArcanaDecision.allow(); }
        @Override public void commit() { terminal.compareAndSet(false, true); }

        @Override
        public void refund() {
            if (!terminal.compareAndSet(false, true)) return;
            ArcanaDecision refund = access.adjust(casterId, affinity, amount);
            if (!refund.allowed()) {
                throw new IllegalStateException("Malum spirit refund failed: " + refund.code());
            }
        }
    }
}
