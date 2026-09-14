package dev.gustavopere.blackarcana.config;

import dev.gustavopere.blackarcana.content.noetic.AstralSeveranceRuntime;

import java.util.Collection;
import java.util.List;
import java.util.Objects;
import java.util.Optional;

/**
 * Atomically published server-owned Astral control limits.
 *
 * <p>The default and empty-reload state is deliberately {@link Optional#empty()}; callers must fail closed
 * rather than deriving movement values from safety ceilings or test fixtures.</p>
 */
public final class AstralControlConfigAuthority {
    private static volatile Optional<AstralSeveranceRuntime.ControlLimits> CURRENT = Optional.empty();

    private AstralControlConfigAuthority() { }

    public static Optional<AstralSeveranceRuntime.ControlLimits> currentLimits() {
        return CURRENT;
    }

    static synchronized void reload(Collection<AstralControlDataDefinition> definitions) {
        Objects.requireNonNull(definitions, "definitions");
        List<AstralControlDataDefinition> snapshot = List.copyOf(definitions);
        if (snapshot.size() > 1) {
            throw new IllegalArgumentException("at most one Astral control profile may be active");
        }

        Optional<AstralSeveranceRuntime.ControlLimits> next = Optional.empty();
        if (!snapshot.isEmpty()) {
            AstralControlDataDefinition definition = Objects.requireNonNull(snapshot.getFirst(), "definition");
            List<String> errors = definition.validate();
            if (!errors.isEmpty()) {
                throw new IllegalArgumentException("invalid Astral control config: " + String.join("; ", errors));
            }
            next = Optional.of(definition.toRuntimeLimits());
        }

        CURRENT = next;
    }
}
