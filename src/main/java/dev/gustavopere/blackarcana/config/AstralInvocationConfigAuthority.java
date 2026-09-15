package dev.gustavopere.blackarcana.config;

import java.util.Collection;
import java.util.List;
import java.util.Objects;
import java.util.Optional;

/**
 * Atomically published server-owned Astral invocation parameters.
 *
 * <p>Absent or empty configuration is deliberately {@link Optional#empty()}. This authority never derives
 * gameplay values from safety ceilings, fixtures, provider themes, or presentation data.</p>
 */
public final class AstralInvocationConfigAuthority {
    private static volatile Optional<AstralInvocationDataDefinition.Invocation> CURRENT = Optional.empty();

    private AstralInvocationConfigAuthority() { }

    public static Optional<AstralInvocationDataDefinition.Invocation> current() {
        return CURRENT;
    }

    static synchronized void reload(Collection<AstralInvocationDataDefinition> definitions) {
        Objects.requireNonNull(definitions, "definitions");
        List<AstralInvocationDataDefinition> snapshot = List.copyOf(definitions);
        if (snapshot.size() > 1) {
            throw new IllegalArgumentException("at most one Astral invocation profile may be active");
        }

        Optional<AstralInvocationDataDefinition.Invocation> next = Optional.empty();
        if (!snapshot.isEmpty()) {
            AstralInvocationDataDefinition definition = Objects.requireNonNull(snapshot.getFirst(), "definition");
            List<String> errors = definition.validate();
            if (!errors.isEmpty()) {
                throw new IllegalArgumentException("invalid Astral invocation config: " + String.join("; ", errors));
            }
            next = Optional.of(definition.toInvocation());
        }

        CURRENT = next;
    }
}
