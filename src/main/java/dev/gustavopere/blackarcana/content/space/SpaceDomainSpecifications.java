package dev.gustavopere.blackarcana.content.space;

import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.core.domain.ArcanaDomain;
import dev.gustavopere.blackarcana.core.domain.SpellImplementationSpec;
import dev.gustavopere.blackarcana.core.domain.SpellImplementationSpecRegistry;
import dev.gustavopere.blackarcana.core.world.WorldEffectMode;

import java.util.List;
import java.util.Objects;

public final class SpaceDomainSpecifications {
    public static final ArcanaSpellId THRESHOLD_GATE = ArcanaSpellId.parse("black_arcana:threshold_gate");
    public static final ArcanaSpellId VEILSTEP_REFLEX = ArcanaSpellId.parse("black_arcana:veilstep_reflex");
    public static final ArcanaSpellId ANCHOR_RECALL = ArcanaSpellId.parse("black_arcana:anchor_recall");
    public static final ArcanaSpellId RECIPROCAL_TRANSPOSITION = ArcanaSpellId.parse("black_arcana:reciprocal_transposition");
    public static final ArcanaSpellId VECTOR_REVERSAL = ArcanaSpellId.parse("black_arcana:vector_reversal");

    private SpaceDomainSpecifications() { }

    public static List<SpellImplementationSpec> all() {
        return List.of(
            spec(THRESHOLD_GATE, "Paired loaded thresholds move eligible entities with bounded throughput.", "Ars integration where practical", "paired server-owned endpoints", "source/mana/upkeep", 80L, "T2 Liminal", "throughput/ownership/PvP/dimension rules", "#threshold-gate"),
            spec(VEILSTEP_REFLEX, "Consume a bounded charge to blink to the first safe nearby server-generated position.", "Iron's/Ars adapter", "caster and incoming eligible threat", "mana + charge/internal cooldown", 100L, "T2 Liminal", "safe-search radius/candidate cap/protected damage tags", "#veilstep-reflex"),
            spec(ANCHOR_RECALL, "Recall to a recent owned marked projectile after full destination validation.", "Ars or Iron's", "owned projectile only", "mana + cooldown", 120L, "T2 Liminal", "age/range/dimension/collision limits", "#anchor-recall"),
            spec(RECIPROCAL_TRANSPOSITION, "Atomically exchange two eligible entities/items on loaded endpoints.", "Ars + Black Arcana transaction core", "two loaded endpoints with immediate revalidation", "pair charge + host resource", 160L, "T3 Liminal", "throughput/consent/PvP/endpoint-version policy", "#reciprocal-transposition"),
            spec(VECTOR_REVERSAL, "Apply a bounded directional impulse to one or a bounded target set.", "Iron's", "server-resolved entity or bounded area", "mana + cooldown", 80L, "T2 Liminal", "speed/fall-distance/entity-count/boss-player multipliers", "#vector-reversal")
        );
    }

    private static SpellImplementationSpec spec(ArcanaSpellId id, String fantasy, String host, String target,
                                                 String cost, long cooldown, String gate, String config,
                                                 String provenanceAnchor) {
        return new SpellImplementationSpec(id, ArcanaDomain.SPACE_DISPLACEMENT, fantasy, host,
            "direct/triggered cast as specified", target, cost, cooldown,
            "movement is clamped by the relevant Liminal hard ceiling and revalidated immediately before mutation",
            gate, WorldEffectMode.OFF,
            "hostile player movement follows server PvP/consent; bosses receive explicit displacement caps",
            config,
            "docs/design/candidate-specifications.md" + provenanceAnchor);
    }

    public static void installInto(SpellImplementationSpecRegistry registry) {
        Objects.requireNonNull(registry, "registry");
        all().forEach(registry::register);
    }
}
