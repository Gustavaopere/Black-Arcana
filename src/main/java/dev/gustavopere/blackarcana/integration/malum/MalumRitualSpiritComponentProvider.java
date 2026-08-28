package dev.gustavopere.blackarcana.integration.malum;

import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.core.ritual.ArcanaRitualId;
import dev.gustavopere.blackarcana.core.ritual.RitualComponentProvider;
import dev.gustavopere.blackarcana.core.ritual.RitualComponentReservation;
import dev.gustavopere.blackarcana.core.ritual.RitualContext;
import dev.gustavopere.blackarcana.core.ritual.RitualDefinition;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Set;
import java.util.UUID;

/** Transactional ritual component provider backed by discrete Malum spirit shards. */
public final class MalumRitualSpiritComponentProvider implements RitualComponentProvider {
    public static final int MAX_RITUAL_REQUIREMENTS = 512;
    public static final int MAX_AFFINITIES_PER_RITUAL = 8;

    private final MalumSpiritAccess access;
    private final Map<ArcanaRitualId, List<MalumRitualSpiritRequirement>> requirements;

    public MalumRitualSpiritComponentProvider(
            MalumSpiritAccess access,
            Map<ArcanaRitualId, ? extends List<MalumRitualSpiritRequirement>> requirements
    ) {
        this.access = Objects.requireNonNull(access, "access");
        Objects.requireNonNull(requirements, "requirements");
        if (requirements.size() > MAX_RITUAL_REQUIREMENTS) {
            throw new IllegalArgumentException("too many Malum ritual requirement definitions");
        }
        Map<ArcanaRitualId, List<MalumRitualSpiritRequirement>> copy = new LinkedHashMap<>();
        requirements.forEach((id, values) -> {
            Objects.requireNonNull(id, "ritual id");
            Objects.requireNonNull(values, "spirit requirements");
            if (values.isEmpty() || values.size() > MAX_AFFINITIES_PER_RITUAL) {
                throw new IllegalArgumentException("Malum ritual affinity count outside bounds");
            }
            List<MalumRitualSpiritRequirement> bounded = List.copyOf(values);
            Set<String> affinities = new HashSet<>();
            for (MalumRitualSpiritRequirement requirement : bounded) {
                Objects.requireNonNull(requirement, "spirit requirement");
                if (!affinities.add(requirement.affinity())) {
                    throw new IllegalArgumentException("duplicate Malum ritual spirit affinity: " + requirement.affinity());
                }
            }
            copy.put(id, bounded);
        });
        this.requirements = Map.copyOf(copy);
    }

    @Override
    public ArcanaDecision check(RitualDefinition definition, RitualContext context, long nowTick) {
        List<MalumRitualSpiritRequirement> required = requirements.get(definition.id());
        if (required == null) {
            return ArcanaDecision.deny(
                    "malum_ritual_requirements_missing",
                    "no Malum spirit requirements are configured for this ritual");
        }
        for (MalumRitualSpiritRequirement requirement : required) {
            final int available;
            try {
                available = access.count(context.casterId(), requirement.affinity());
            } catch (RuntimeException | LinkageError failure) {
                return ArcanaDecision.deny(
                        "malum_ritual_spirit_query_failed",
                        "Malum spirit inventory query failed closed");
            }
            if (available < requirement.amount()) {
                return ArcanaDecision.deny(
                        "insufficient_malum_ritual_spirits",
                        "Requires " + requirement.amount() + " " + requirement.affinity()
                                + " spirits but only " + available + " are available");
            }
        }
        return ArcanaDecision.allow();
    }

    @Override
    public RitualComponentReservation reserve(RitualDefinition definition, RitualContext context, long nowTick) {
        ArcanaDecision preflight = check(definition, context, nowTick);
        if (!preflight.allowed()) {
            return RitualComponentReservation.denied(preflight.code(), preflight.detail());
        }

        List<MalumRitualSpiritRequirement> required = requirements.get(definition.id());
        UUID casterId = context.casterId();
        List<MalumRitualSpiritRequirement> deducted = new ArrayList<>(required.size());
        for (MalumRitualSpiritRequirement requirement : required) {
            final ArcanaDecision decision;
            try {
                decision = Objects.requireNonNull(
                        access.adjust(casterId, requirement.affinity(), -requirement.amount()),
                        "spirit adjustment decision");
            } catch (RuntimeException | LinkageError failure) {
                refund(casterId, deducted);
                return RitualComponentReservation.denied(
                        "malum_ritual_spirit_reservation_failed",
                        "Malum spirit reservation failed closed");
            }
            if (!decision.allowed()) {
                refund(casterId, deducted);
                return RitualComponentReservation.denied(decision.code(), decision.detail());
            }
            deducted.add(requirement);
        }

        List<MalumRitualSpiritRequirement> reserved = List.copyOf(deducted);
        return RitualComponentReservation.reserved(
                () -> { },
                () -> refund(casterId, reserved));
    }

    private void refund(UUID casterId, List<MalumRitualSpiritRequirement> deducted) {
        RuntimeException first = null;
        for (int index = deducted.size() - 1; index >= 0; index--) {
            MalumRitualSpiritRequirement requirement = deducted.get(index);
            try {
                ArcanaDecision result = Objects.requireNonNull(
                        access.adjust(casterId, requirement.affinity(), requirement.amount()),
                        "spirit refund decision");
                if (!result.allowed()) {
                    throw new IllegalStateException("Malum ritual spirit refund denied: " + result.code());
                }
            } catch (RuntimeException failure) {
                if (first == null) first = failure;
                else first.addSuppressed(failure);
            }
        }
        if (first != null) throw first;
    }
}
