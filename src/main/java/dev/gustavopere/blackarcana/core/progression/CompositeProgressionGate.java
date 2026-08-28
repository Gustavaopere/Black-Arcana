package dev.gustavopere.blackarcana.core.progression;

import dev.gustavopere.blackarcana.api.ArcanaCastRequest;
import dev.gustavopere.blackarcana.api.ArcanaDecision;
import dev.gustavopere.blackarcana.api.ArcanaServices.ProgressionGate;

import java.util.List;
import java.util.Objects;

/** Ordered fail-closed progression composition. The first denial is preserved for HUD diagnostics. */
public final class CompositeProgressionGate implements ProgressionGate {
    public static final int MAX_GATES = 8;
    private final List<ProgressionGate> gates;

    public CompositeProgressionGate(List<ProgressionGate> gates) {
        Objects.requireNonNull(gates, "gates");
        if (gates.isEmpty() || gates.size() > MAX_GATES) {
            throw new IllegalArgumentException("progression gate count must be between 1 and " + MAX_GATES);
        }
        this.gates = gates.stream().map(gate -> Objects.requireNonNull(gate, "gate")).toList();
    }

    public static CompositeProgressionGate of(ProgressionGate... gates) {
        return new CompositeProgressionGate(List.of(gates));
    }

    @Override
    public ArcanaDecision check(ArcanaCastRequest request) {
        Objects.requireNonNull(request, "request");
        for (ProgressionGate gate : gates) {
            ArcanaDecision decision = Objects.requireNonNull(gate.check(request), "progression gate decision");
            if (!decision.allowed()) return decision;
        }
        return ArcanaDecision.allow();
    }
}
