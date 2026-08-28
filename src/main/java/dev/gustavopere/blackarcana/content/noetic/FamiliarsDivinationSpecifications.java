package dev.gustavopere.blackarcana.content.noetic;

import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.core.domain.ArcanaDomain;
import dev.gustavopere.blackarcana.core.domain.SpellImplementationSpec;
import dev.gustavopere.blackarcana.core.domain.SpellImplementationSpecRegistry;
import dev.gustavopere.blackarcana.core.world.WorldEffectMode;

import java.util.List;
import java.util.Objects;

public final class FamiliarsDivinationSpecifications {
    public static final ArcanaSpellId ASTRAL_SEVERANCE = ArcanaSpellId.parse("black_arcana:astral_severance");
    public static final ArcanaSpellId NAMESCRY = ArcanaSpellId.parse("black_arcana:namescry");
    public static final ArcanaSpellId GAZE_OF_STILLNESS = ArcanaSpellId.parse("black_arcana:gaze_of_stillness");
    public static final ArcanaSpellId NULLIFYING_GAZE = ArcanaSpellId.parse("black_arcana:nullifying_gaze");
    public static final ArcanaSpellId OCCULT_APPRAISAL = ArcanaSpellId.parse("black_arcana:occult_appraisal");
    public static final ArcanaSpellId BORROWED_SIGHT = ArcanaSpellId.parse("black_arcana:borrowed_sight");
    public static final ArcanaSpellId PACT_SANCTUARY = ArcanaSpellId.parse("black_arcana:pact_sanctuary");
    private FamiliarsDivinationSpecifications() { }

    public static List<SpellImplementationSpec> all() {
        return List.of(
            spec(ASTRAL_SEVERANCE, "Project a bounded non-combat viewpoint while the physical body remains vulnerable.", "Black Arcana session core + Eidolon flavor", "channel", "caster-owned viewpoint within loaded range", "mana/channel", 300L, "range<=96; duration<=400t", "T3 Noetic", "body damage/logout/unload returns immediately"),
            spec(NAMESCRY, "Channel limited remote perception of an explicitly resolved loaded target.", "Eidolon ritual or Black Arcana core", "channel/focus", "loaded same-dimension target; players require consent/covenant", "focus item + mana", 400L, "range<=96; metadata=allowlist", "T3 Noetic", "no force-load and no hostile player privacy bypass"),
            spec(GAZE_OF_STILLNESS, "Maintain reciprocal facing and LOS to impose bounded movement suppression.", "Iron's active spell + Black Arcana CC policy", "channeled gaze", "one server-resolved living target", "mana per tick", 200L, "control duration uses diminishing returns and hard cap", "T2 Noetic", "boss/player duration multipliers apply"),
            spec(NULLIFYING_GAZE, "Remove only effects explicitly tagged or adapted as nullifiable.", "Iron's + explicit adapters", "channeled gaze", "one target in LOS", "mana/channel", 300L, "only allowlisted nullifiable effects", "T3 Noetic", "unknown/protected effects remain untouched"),
            spec(OCCULT_APPRAISAL, "Reveal a small approved metadata projection rather than arbitrary target state.", "Black Arcana presentation", "short channel", "loaded target in range/LOS", "small mana cost", 80L, "metadata fields are server allowlisted", "T2 Noetic", "private container/NBT data is not exposed"),
            spec(BORROWED_SIGHT, "Channel the viewpoint of an owned familiar or explicitly consenting bond.", "Ars familiar adapter + Black Arcana camera/session logic", "channel", "owned familiar, loaded and same-dimension", "mana/channel", 200L, "range<=96; duration<=400t", "T2 Noetic", "foreign familiar/player denied; unload/logout returns"),
            spec(PACT_SANCTUARY, "A familiar-centered bounded aura suppresses hostility from eligible ordinary mobs.", "Ars familiar adapter + bounded aura runtime", "familiar aura", "owned familiar and <=32 eligible nearby mobs", "upkeep", 400L, "targets<=32; range bounded by config ceiling", "T3 Noetic", "boss/event mobs excluded; no permanent faction mutation")
        );
    }

    private static SpellImplementationSpec spec(ArcanaSpellId id, String fantasy, String host, String invocation, String target, String cost, long cooldown, String scaling, String gate, String safety) {
        return new SpellImplementationSpec(id, ArcanaDomain.FAMILIARS_DIVINATION, fantasy, host, invocation, target, cost, cooldown, scaling, gate, WorldEffectMode.OFF, safety,
            "range/duration/entity caps, consent/covenant/privacy policy and cleanup semantics",
            "docs/design/candidate-specifications.md#" + id.path().replace('_', '-'));
    }

    public static void installInto(SpellImplementationSpecRegistry registry) {
        Objects.requireNonNull(registry, "registry"); all().forEach(registry::register);
    }
}
