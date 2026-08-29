package dev.gustavopere.blackarcana.content.forbidden;

import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.core.domain.ArcanaDomain;
import dev.gustavopere.blackarcana.core.domain.SpellImplementationSpec;
import dev.gustavopere.blackarcana.core.domain.SpellImplementationSpecRegistry;
import dev.gustavopere.blackarcana.core.world.WorldEffectMode;

import java.util.List;
import java.util.Objects;

public final class ForbiddenDomainSpecifications {
    public static final ArcanaSpellId INNER_DOMINION = ArcanaSpellId.parse("black_arcana:inner_dominion");
    private ForbiddenDomainSpecifications() { }

    public static List<SpellImplementationSpec> all() {
        return List.of(new SpellImplementationSpec(
            INNER_DOMINION, ArcanaDomain.FORBIDDEN_DOMAINS,
            "Open a temporary caster-owned localized rulespace and guarantee every participant a validated return route.",
            "Black Arcana session core; invocation may be Iron's or a grand ritual",
            "T4 activation after ritual/knowledge unlock",
            "bounded server-selected participants; nested-domain participation denied",
            "high composite resource plus long cooldown", 2_400L,
            "radius<=32; duration<=2400t; participants<=16; activeSessions<=4",
            "T4 Forbidden", WorldEffectMode.OFF,
            "player participation follows server policy; bosses may receive domain-specific caps rather than execution semantics",
            "radius, duration, participants, active sessions, return fallback and PvP/boss policy",
            "docs/design/candidate-specifications.md#inner-dominion"));
    }

    public static void installInto(SpellImplementationSpecRegistry registry) {
        Objects.requireNonNull(registry, "registry");
        all().forEach(registry::register);
    }
}
