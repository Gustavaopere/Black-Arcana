package dev.gustavopere.blackarcana.content.cinder;

import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.core.domain.ArcanaDomain;
import dev.gustavopere.blackarcana.core.domain.SpellImplementationSpec;
import dev.gustavopere.blackarcana.core.domain.SpellImplementationSpecRegistry;
import dev.gustavopere.blackarcana.core.world.WorldEffectMode;

import java.util.List;
import java.util.Objects;

public final class BlackPyreDomainSpecifications {
    public static final ArcanaSpellId BLACK_PYRE = ArcanaSpellId.parse("black_arcana:black_pyre");

    private BlackPyreDomainSpecifications() { }

    public static List<SpellImplementationSpec> all() {
        return List.of(new SpellImplementationSpec(
            BLACK_PYRE,
            ArcanaDomain.BLACK_FLAME,
            "Forbidden soul-fire damages eligible entities while terrain presentation spreads only through a bounded Black Arcana frontier.",
            "Iron's active cast + optional causal Malum spirit amplification + Black Arcana world safety",
            "active cast or placed ignition point",
            "server-resolved entities and already-loaded cells only; mutation protection and friendly-fire policy apply",
            "mana plus optional bounded causal spirit amplification",
            300L,
            "entityDamage=clamp(base*scale); cells<=256; spreadPerTick<=16; radius<=12; lifetime<=1200",
            "T3 Cinder",
            WorldEffectMode.TEMPORARY,
            "entity damage remains policy-controlled when terrain effects are disabled; bosses and players use explicit caps",
            "damage cap, radius, cell cap, spread/tick, lifetime, concurrent frontiers, world mode, PvP/boss multipliers",
            "plans/07-spell-domains/✅-05-black-flame.md"));
    }

    public static void installInto(SpellImplementationSpecRegistry registry) {
        Objects.requireNonNull(registry, "registry");
        all().forEach(registry::register);
    }
}
