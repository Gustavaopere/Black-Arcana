package dev.gustavopere.blackarcana.core.ritual;

import dev.gustavopere.blackarcana.api.ArcanaDecision;

import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Objects;

/**
 * Bounded dispatch table for ritual requirements, component transactions and outcomes.
 * Missing bindings fail closed; no ritual becomes free merely because an integration is absent.
 */
public final class RitualBindingRegistry {
    private final int maxBindings;
    private final Map<ArcanaRitualId, Binding> bindings = new LinkedHashMap<>();

    public RitualBindingRegistry(int maxBindings) {
        if (maxBindings <= 0 || maxBindings > 4_096) {
            throw new IllegalArgumentException("maxBindings outside bounds");
        }
        this.maxBindings = maxBindings;
    }

    public synchronized void register(
            ArcanaRitualId id,
            RitualRequirementEvaluator requirements,
            RitualComponentProvider components,
            RitualOutcomeExecutor outcomes
    ) {
        Objects.requireNonNull(id, "id");
        Binding binding = new Binding(requirements, components, outcomes);
        if (bindings.containsKey(id)) {
            throw new IllegalStateException("duplicate ritual binding: " + id.canonical());
        }
        if (bindings.size() >= maxBindings) {
            throw new IllegalStateException("ritual binding registry is full");
        }
        bindings.put(id, binding);
    }

    public synchronized boolean contains(ArcanaRitualId id) {
        return bindings.containsKey(Objects.requireNonNull(id, "id"));
    }

    public RitualRequirementEvaluator requirements() {
        return (definition, context, nowTick) -> {
            Binding binding = binding(definition.id());
            if (binding == null) return missing();
            try {
                return Objects.requireNonNull(
                        binding.requirements.check(definition, context, nowTick),
                        "ritual requirement decision");
            } catch (RuntimeException | LinkageError failure) {
                return ArcanaDecision.deny("ritual_requirement_failed", "ritual requirement binding failed closed");
            }
        };
    }

    public RitualComponentProvider components() {
        return new RitualComponentProvider() {
            @Override
            public ArcanaDecision check(RitualDefinition definition, RitualContext context, long nowTick) {
                Binding binding = binding(definition.id());
                if (binding == null) return missing();
                try {
                    return Objects.requireNonNull(
                            binding.components.check(definition, context, nowTick),
                            "ritual component decision");
                } catch (RuntimeException | LinkageError failure) {
                    return ArcanaDecision.deny("ritual_component_check_failed", "ritual component binding failed closed");
                }
            }

            @Override
            public RitualComponentReservation reserve(RitualDefinition definition, RitualContext context, long nowTick) {
                Binding binding = binding(definition.id());
                if (binding == null) {
                    ArcanaDecision missing = missing();
                    return RitualComponentReservation.denied(missing.code(), missing.detail());
                }
                try {
                    return Objects.requireNonNull(
                            binding.components.reserve(definition, context, nowTick),
                            "ritual component reservation");
                } catch (RuntimeException | LinkageError failure) {
                    return RitualComponentReservation.denied(
                            "ritual_component_reserve_failed",
                            "ritual component binding failed closed");
                }
            }
        };
    }

    public RitualOutcomeExecutor outcomes() {
        return (definition, context, nowTick) -> {
            Binding binding = binding(definition.id());
            if (binding == null) return missing();
            try {
                return Objects.requireNonNull(
                        binding.outcomes.execute(definition, context, nowTick),
                        "ritual outcome decision");
            } catch (RuntimeException | LinkageError failure) {
                return ArcanaDecision.deny("ritual_outcome_failed", "ritual outcome binding failed closed");
            }
        };
    }

    private synchronized Binding binding(ArcanaRitualId id) {
        return bindings.get(id);
    }

    private static ArcanaDecision missing() {
        return ArcanaDecision.deny(
                "ritual_binding_missing",
                "ritual has no installed server-side binding");
    }

    private record Binding(
            RitualRequirementEvaluator requirements,
            RitualComponentProvider components,
            RitualOutcomeExecutor outcomes
    ) {
        private Binding {
            Objects.requireNonNull(requirements, "requirements");
            Objects.requireNonNull(components, "components");
            Objects.requireNonNull(outcomes, "outcomes");
        }
    }
}
