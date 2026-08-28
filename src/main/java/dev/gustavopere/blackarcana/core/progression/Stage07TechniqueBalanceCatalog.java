package dev.gustavopere.blackarcana.core.progression;

import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.content.blood.BloodDomainSpecifications;
import dev.gustavopere.blackarcana.content.cinder.BlackPyreDomainSpecifications;
import dev.gustavopere.blackarcana.content.forbidden.ForbiddenDomainSpecifications;
import dev.gustavopere.blackarcana.content.noetic.FamiliarsDivinationSpecifications;
import dev.gustavopere.blackarcana.content.projection.ProjectionDomainSpecifications;
import dev.gustavopere.blackarcana.content.souls.SoulDomainSpecifications;
import dev.gustavopere.blackarcana.content.space.SpaceDomainSpecifications;

import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Objects;
import java.util.Set;

/**
 * Frozen Stage 08 balance review for every production technique introduced by Stage 07.
 * There is intentionally no tier-default fallback: missing review data is a release error.
 */
public final class Stage07TechniqueBalanceCatalog {
    private static final Map<ArcanaSpellId, TechniqueBudgetProfile> PROFILES = build();

    private Stage07TechniqueBalanceCatalog() { }

    public static TechniqueBudgetProfile require(ArcanaSpellId id) {
        Objects.requireNonNull(id, "id");
        TechniqueBudgetProfile profile = PROFILES.get(id);
        if (profile == null) throw new IllegalStateException("missing explicit Stage 08 balance budget: " + id.canonical());
        return profile;
    }

    public static Map<ArcanaSpellId, TechniqueBudgetProfile> snapshot() {
        return PROFILES;
    }

    public static Set<ArcanaSpellId> ids() {
        return PROFILES.keySet();
    }

    private static Map<ArcanaSpellId, TechniqueBudgetProfile> build() {
        Map<ArcanaSpellId, TechniqueBudgetProfile> values = new LinkedHashMap<>();

        // Blood & Curses
        add(values, p(BloodDomainSpecifications.SANGUINE_HARVEST, TechniqueTier.T3, 4, 6, 1, 0, 3, 5, 5, 7, 6, 7, 5,
            "Eidolon/Malum ritual economy", "Bounded multi-target sustain is compensated by ritual setup, anti-farm weighting and cooldown."));
        add(values, p(BloodDomainSpecifications.SYMPATHETIC_WOUND, TechniqueTier.T3, 6, 1, 4, 0, 1, 5, 5, 4, 7, 6, 5,
            "Iron's single-target damage spells", "Echo damage is event- and lifetime-capped and cannot recurse."));
        add(values, p(BloodDomainSpecifications.BLOOD_PRICE, TechniqueTier.T2, 0, 0, 0, 0, 2, 6, 6, 3, 8, 8, 1,
            "Black Arcana composite costs", "Utility is paid with real health at an intentionally inefficient exchange rate."));
        add(values, p(BloodDomainSpecifications.LAW_OF_RECURRENCE, TechniqueTier.T3, 0, 0, 3, 0, 7, 3, 4, 3, 7, 5, 6,
            "Iron's defensive spell cadence", "Resistance remains below immunity and family switching creates vulnerability."));
        add(values, p(BloodDomainSpecifications.EQUILIBRIUM_RITE, TechniqueTier.T4_FORBIDDEN, 3, 0, 3, 0, 8, 8, 3, 7, 9, 9, 9,
            "Eidolon high-impact ritual cadence", "Health is transferred, never created; source floor, hard cap and long cooldown constrain value."));

        // Souls & Death
        add(values, p(SoulDomainSpecifications.MORTAL_LEDGER, TechniqueTier.T4_FORBIDDEN, 0, 0, 0, 0, 9, 8, 3, 9, 10, 9, 8,
            "Malum spirit economy", "Death prevention requires credited deaths, finite thresholds and a hard Soul Anchor cap."));
        add(values, p(SoulDomainSpecifications.SPIRIT_SIGHT, TechniqueTier.T1, 0, 0, 0, 0, 0, 5, 6, 1, 1, 2, 1,
            "Malum/Eidolon occult presentation", "Whitelist-only trace visibility cannot reveal players or arbitrary private data."));

        // Projection & Arsenal
        add(values, p(ProjectionDomainSpecifications.EPHEMERAL_TEMPERING, TechniqueTier.T2, 4, 0, 0, 0, 3, 4, 5, 3, 3, 5, 4,
            "Iron's temporary buff cadence", "Only transient bounded modifiers are permitted; persistent NBT mutation is forbidden."));
        add(values, p(ProjectionDomainSpecifications.ECHO_ARMAMENT, TechniqueTier.T2, 4, 0, 0, 0, 2, 5, 5, 3, 3, 4, 3,
            "Iron's conjured weapon utility", "Sanitized profiles are clamped and can never materialize as inventory items."));
        add(values, p(ProjectionDomainSpecifications.RIFT_BLADES, TechniqueTier.T2, 6, 2, 2, 5, 0, 2, 4, 2, 4, 5, 4,
            "Iron's projectile/mobility spells", "Damage and safe displacement have independent hard caps and collision validation."));
        add(values, p(ProjectionDomainSpecifications.SPECTRAL_ARSENAL, TechniqueTier.T3, 8, 6, 2, 0, 0, 4, 4, 4, 5, 7, 7,
            "Iron's high-tier projectile volleys", "Volley count, active echoes and per-projectile damage are independently bounded."));
        add(values, p(ProjectionDomainSpecifications.OATHFORGED_ASCENSION, TechniqueTier.T4_FORBIDDEN, 6, 0, 0, 0, 7, 8, 2, 10, 9, 10, 8,
            "Eidolon/Malum grand ritual economy", "Permanent gain uses allowlisted sacrifices, sublinear returns and an immutable point cap."));

        // Space & Displacement
        add(values, p(SpaceDomainSpecifications.THRESHOLD_GATE, TechniqueTier.T2, 0, 2, 2, 8, 0, 7, 4, 5, 5, 5, 4,
            "Ars Nouveau warp utilities", "Only paired loaded endpoints are legal and throughput is bounded."));
        add(values, p(SpaceDomainSpecifications.VEILSTEP_REFLEX, TechniqueTier.T2, 0, 0, 1, 8, 3, 4, 4, 1, 4, 5, 5,
            "Ars Blink / Iron's mobility", "Consumes a finite charge and accepts only server-generated safe destinations."));
        add(values, p(SpaceDomainSpecifications.ANCHOR_RECALL, TechniqueTier.T2, 0, 0, 0, 8, 0, 5, 4, 2, 4, 4, 4,
            "Ars warp/recall utilities", "Owned-projectile age, range, dimension and collision rules constrain recall."));
        add(values, p(SpaceDomainSpecifications.RECIPROCAL_TRANSPOSITION, TechniqueTier.T3, 0, 0, 5, 9, 0, 7, 3, 5, 8, 7, 6,
            "Ars displacement utilities", "Atomic endpoint revalidation, consent/PvP rules and pair charges compensate high mobility."));
        add(values, p(SpaceDomainSpecifications.VECTOR_REVERSAL, TechniqueTier.T2, 2, 3, 5, 6, 0, 3, 5, 2, 4, 4, 3,
            "Iron's knockback/control spells", "Speed, target count and player/boss displacement multipliers are capped."));

        // Black Pyre
        add(values, p(BlackPyreDomainSpecifications.BLACK_PYRE, TechniqueTier.T3, 7, 8, 3, 0, 0, 5, 3, 4, 8, 7, 7,
            "Iron's AoE damage + Stage 04 world safety", "Entity damage and temporary terrain frontier have separate caps, budgets and lifetimes."));

        // Forbidden Domains
        add(values, p(ForbiddenDomainSpecifications.INNER_DOMINION, TechniqueTier.T4_FORBIDDEN, 5, 9, 8, 6, 7, 10, 2, 9, 10, 10, 10,
            "Black Arcana grand-domain runtime", "Participant, radius, duration and concurrent-session ceilings plus guaranteed return routes bound the effect."));

        // Familiars & Divination
        add(values, p(FamiliarsDivinationSpecifications.ASTRAL_SEVERANCE, TechniqueTier.T3, 0, 0, 0, 7, 0, 9, 4, 4, 8, 5, 6,
            "Ars familiar/view utilities", "Physical body remains vulnerable; loaded-range, duration and forced-return rules limit scouting."));
        add(values, p(FamiliarsDivinationSpecifications.NAMESCRY, TechniqueTier.T3, 0, 0, 0, 0, 0, 9, 3, 7, 9, 6, 7,
            "Eidolon divination ritual cadence", "Loaded same-dimension targets, consent/covenant and metadata allowlists prevent privacy bypass."));
        add(values, p(FamiliarsDivinationSpecifications.GAZE_OF_STILLNESS, TechniqueTier.T2, 0, 0, 7, 0, 0, 3, 4, 2, 5, 5, 4,
            "Iron's crowd-control spells", "Reciprocal LOS/facing plus diminishing-return duration and boss/player multipliers bound control."));
        add(values, p(FamiliarsDivinationSpecifications.NULLIFYING_GAZE, TechniqueTier.T3, 0, 0, 7, 0, 0, 7, 3, 3, 7, 6, 6,
            "Iron's dispel utility", "Only explicitly tagged/adapted nullifiable effects may be removed."));
        add(values, p(FamiliarsDivinationSpecifications.OCCULT_APPRAISAL, TechniqueTier.T2, 0, 0, 0, 0, 0, 7, 6, 1, 2, 2, 2,
            "Vanilla/occult inspection utility", "Server allowlist exposes a small metadata projection, never arbitrary NBT/container state."));
        add(values, p(FamiliarsDivinationSpecifications.BORROWED_SIGHT, TechniqueTier.T2, 0, 0, 0, 4, 0, 7, 5, 2, 3, 4, 4,
            "Ars familiar viewpoint", "Only owned/consenting loaded same-dimension bonds are eligible and sessions are duration-bounded."));
        add(values, p(FamiliarsDivinationSpecifications.PACT_SANCTUARY, TechniqueTier.T3, 0, 6, 7, 0, 6, 6, 3, 4, 6, 6, 6,
            "Ars familiar aura utility", "Aura target count/range are bounded; bosses/event mobs are excluded and factions are never mutated."));

        return Map.copyOf(values);
    }

    private static TechniqueBudgetProfile p(
        ArcanaSpellId id, TechniqueTier tier,
        int burst, int area, int control, int mobility, int survivability, int utility, int efficiency,
        int setup, int risk, int resource, int cooldown,
        String benchmarkSource, String note
    ) {
        return new TechniqueBudgetProfile(id, tier, burst, area, control, mobility, survivability, utility, efficiency,
            setup, risk, resource, cooldown,
            new BalanceBenchmark(benchmarkSource, "Minecraft 1.21.1 pack baseline", note));
    }

    private static void add(Map<ArcanaSpellId, TechniqueBudgetProfile> values, TechniqueBudgetProfile profile) {
        TechniqueBudgetProfile previous = values.putIfAbsent(profile.spellId(), profile);
        if (previous != null) throw new IllegalStateException("duplicate technique balance budget: " + profile.spellId().canonical());
        if (!profile.assess().withinBudget()) {
            throw new IllegalStateException("technique exceeds tier budget: " + profile.spellId().canonical());
        }
    }
}
