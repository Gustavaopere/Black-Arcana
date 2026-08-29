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
            BLACK_PYRE, ArcanaDomain.BLACK_FLAME,
            "Forbidden soul-fire damages eligible entities while terrain presentation spreads only through a bounded Black Arcana frontier.",
            "Iron's active cast + optional Malum spirit amplification + Black Arcana world safety",
            "active cast or placed ignition point",
            "server-resolved entities and loaded cells only; protected blocks and friendly-fire policy apply",
            "mana plus optional bounded spirit amplification", 300L,
            "entityDamage=clamp(base*scale); cells<=256; spreadPerTick<=16; radius<=12",
            "T3 Cinder", WorldEffectMode.TEMPORARY,
            "entity damage remains policy-controlled when terrain effects are disabled; bosses use explicit caps",
            "damage cap, radius, cell cap, spread/tick, lifetime, concurrent frontiers, PvP/boss multipliers",
            "docs/design/candidate-specifications.md#black-pyre"));
    }

    public static void installInto(SpellImplementationSpecRegistry registry) {
        Objects.requireNonNull(registry, "registry");
        all().forEach(registry::register);
    }
}
