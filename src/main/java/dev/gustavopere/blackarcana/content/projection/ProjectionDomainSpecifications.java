package dev.gustavopere.blackarcana.content.projection;

import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.core.domain.ArcanaDomain;
import dev.gustavopere.blackarcana.core.domain.SpellImplementationSpec;
import dev.gustavopere.blackarcana.core.domain.SpellImplementationSpecRegistry;
import dev.gustavopere.blackarcana.core.world.WorldEffectMode;

import java.util.List;
import java.util.Objects;

public final class ProjectionDomainSpecifications {
    public static final ArcanaSpellId EPHEMERAL_TEMPERING = ArcanaSpellId.parse("black_arcana:ephemeral_tempering");
    public static final ArcanaSpellId ECHO_ARMAMENT = ArcanaSpellId.parse("black_arcana:echo_armament");
    public static final ArcanaSpellId RIFT_BLADES = ArcanaSpellId.parse("black_arcana:rift_blades");
    public static final ArcanaSpellId SPECTRAL_ARSENAL = ArcanaSpellId.parse("black_arcana:spectral_arsenal");
    public static final ArcanaSpellId OATHFORGED_ASCENSION = ArcanaSpellId.parse("black_arcana:oathforged_ascension");

    private ProjectionDomainSpecifications() { }

    public static List<SpellImplementationSpec> all() {
        return List.of(
            spec(EPHEMERAL_TEMPERING, "Temporarily enhance an eligible held item through a bounded modifier profile.", "Iron's/Malum adapter", "held eligible item", "mana/spirit + cooldown", 200L, "temporary modifiers only; no persistent NBT/stat mutation", "T2 Eidetic Arsenal", "modifier caps/stacking/eligible items", "#ephemeral-tempering"),
            spec(ECHO_ARMAMENT, "Remember a sanitized weapon profile and manifest a temporary echo that cannot become a real item.", "Iron's/core", "caster-owned sanitized profile", "mana + memory slot", 120L, "profile values clamped to hard projection ceilings", "T2 Eidetic Arsenal", "profile slots/lifetime/use permissions", "#echo-armament"),
            spec(RIFT_BLADES, "Conjure bounded spectral blades with an optional safe gap-close on a marked hit.", "Iron's + Black Arcana destination validation", "server-resolved entity and safe landing", "Iron's mana + cooldown", 160L, "damage and displacement independently capped", "T2 Eidetic Arsenal", "projectile count/range/collision", "#rift-blades"),
            spec(SPECTRAL_ARSENAL, "Fire a bounded volley from sanitized registered weapon profiles without cloning live items.", "Iron's + projected-profile registry", "bounded target set / sanitized profiles", "mana per volley/projectile", 300L, "volley damage bounded independently from source item NBT", "T3 Eidetic Arsenal", "profile/damage/projectile/active-echo caps", "#spectral-arsenal"),
            spec(OATHFORGED_ASCENSION, "Grand ritual converts eligible sacrifices into finite enhancement points with diminishing returns.", "Eidolon/Malum ritual + core ledger", "ritual-owned eligible sacrifices", "consumed items + spirits/materials", 0L, "points=floor((eligibleValue/scale)^exponent), exponent<1, hard-capped", "T4 Eidetic Arsenal", "point cap/curve/input allowlist/recursion guard", "#oathforged-ascension")
        );
    }

    private static SpellImplementationSpec spec(ArcanaSpellId id, String fantasy, String host, String target,
                                                 String cost, long cooldown, String scaling, String gate,
                                                 String config, String provenanceAnchor) {
        return new SpellImplementationSpec(id, ArcanaDomain.PROJECTION_ARSENAL, fantasy, host,
            "direct cast or ritual as specified", target, cost, cooldown, scaling, gate,
            WorldEffectMode.OFF,
            "player/boss damage or displacement uses frozen Stage 04 entity policy",
            config,
            "docs/design/candidate-specifications.md" + provenanceAnchor);
    }

    public static void installInto(SpellImplementationSpecRegistry registry) {
        Objects.requireNonNull(registry, "registry");
        all().forEach(registry::register);
    }
}
