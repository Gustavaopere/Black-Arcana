package dev.gustavopere.blackarcana.content.blood;

import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.core.domain.ArcanaDomain;
import dev.gustavopere.blackarcana.core.domain.SpellImplementationSpec;
import dev.gustavopere.blackarcana.core.domain.SpellImplementationSpecRegistry;
import dev.gustavopere.blackarcana.core.world.WorldEffectMode;

import java.util.List;
import java.util.Objects;

/** Frozen Stage 01 contracts for the Blood & Curses mechanics implemented by Stage 07. */
public final class BloodDomainSpecifications {
    public static final ArcanaSpellId SANGUINE_HARVEST = ArcanaSpellId.parse("black_arcana:sanguine_harvest");
    public static final ArcanaSpellId SYMPATHETIC_WOUND = ArcanaSpellId.parse("black_arcana:sympathetic_wound");
    public static final ArcanaSpellId BLOOD_PRICE = ArcanaSpellId.parse("black_arcana:blood_price");
    public static final ArcanaSpellId LAW_OF_RECURRENCE = ArcanaSpellId.parse("black_arcana:law_of_recurrence");
    public static final ArcanaSpellId EQUILIBRIUM_RITE = ArcanaSpellId.parse("black_arcana:equilibrium_rite");

    private BloodDomainSpecifications() { }

    public static List<SpellImplementationSpec> all() {
        return List.of(
            new SpellImplementationSpec(
                SANGUINE_HARVEST,
                ArcanaDomain.BLOOD_CURSES,
                "A bounded occult harvest converts eligible nearby life into one configured benefit budget.",
                "Eidolon/Malum composite with Black Arcana bounded planner",
                "ritual or owned ward activation",
                "bounded eligible living targets; PvP/entity policy revalidated server-side",
                "ritual setup plus activation/upkeep",
                200L,
                "yield=sum(min(weightedDrain,remainingBudget)); targets<=configuredCap",
                "T3 Sanguine",
                WorldEffectMode.OFF,
                "players follow server policy; bosses use explicit eligibility/yield caps",
                "target cap, total yield, anti-farm weights, eligible tags, player policy",
                "docs/design/candidate-specifications.md#sanguine-harvest"),
            new SpellImplementationSpec(
                SYMPATHETIC_WOUND,
                ArcanaDomain.BLOOD_CURSES,
                "An occult link echoes a capped fraction of qualifying direct damage from caster to target.",
                "Malum/Eidolon flavor with Black Arcana damage-link core",
                "active link cast after occult unlock",
                "one server-resolved living target; link breaks on expiry/death/dimension policy",
                "health/spirit plus link cooldown",
                200L,
                "mirror=min(directDamage*fraction,eventCap,lifetimeRemaining)",
                "T3 Sanguine",
                WorldEffectMode.OFF,
                "separate player/boss multipliers; reflected/shared damage never re-enters the link",
                "fraction, event cap, lifetime cap, duration, player/boss policy",
                "docs/design/candidate-specifications.md#sympathetic-wound"),
            new SpellImplementationSpec(
                BLOOD_PRICE,
                ArcanaDomain.BLOOD_CURSES,
                "A knowledge-gated cost substitution pays a bounded part of an ordinary cast with real health.",
                "Black Arcana cost composition",
                "cost-provider modifier; not a separate combat cast",
                "caster only",
                "real health at intentionally inefficient exchange rate",
                0L,
                "healthCost=(baseCost*fraction)*healthPerResource; remainingResource=baseCost-(baseCost*fraction)",
                "T2 Sanguine knowledge/perk gate",
                WorldEffectMode.OFF,
                "not target-facing; cannot use absorption/temp health and cannot cross health floor",
                "maximum substitution fraction, exchange rate, minimum remaining health",
                "docs/design/candidate-specifications.md#blood-price"),
            new SpellImplementationSpec(
                LAW_OF_RECURRENCE,
                ArcanaDomain.BLOOD_CURSES,
                "A timed bargain adapts to repeated recognized damage families while punishing family changes.",
                "Iron's/core damage-family policy",
                "defensive timed state",
                "caster only; server-classified damage families",
                "mana/health plus cooldown",
                400L,
                "resistance=min(stack*step,resistanceCap); vulnerability=min(switches*step,vulnerabilityCap)",
                "T3 Sanguine",
                WorldEffectMode.OFF,
                "ordinary resistance remains below total immunity; unknown families use conservative classification",
                "duration, stack cap, resistance cap, vulnerability cap/floor, family mapping",
                "docs/design/candidate-specifications.md#law-of-recurrence"),
            new SpellImplementationSpec(
                EQUILIBRIUM_RITE,
                ArcanaDomain.BLOOD_CURSES,
                "A high-tier rite transfers a bounded eligible amount of current health without creating life.",
                "Iron's/Eidolon invocation with Black Arcana health transaction",
                "high-tier active cast or ritual unlock",
                "one living target; both endpoints revalidated immediately before commit",
                "high composite resource plus long cooldown",
                1_200L,
                "transfer=min(requested,sourceAvailableAboveFloor,targetMissingHealth,hardCap)",
                "T4 Sanguine",
                WorldEffectMode.OFF,
                "hostile players disabled/restricted by policy; bosses/protected targets default denied or tightly capped",
                "transfer cap, source floor, boss/player policy, cooldown and explicit cost",
                "docs/design/candidate-specifications.md#equilibrium-rite")
        );
    }

    public static void installInto(SpellImplementationSpecRegistry registry) {
        Objects.requireNonNull(registry, "registry");
        all().forEach(registry::register);
    }
}
