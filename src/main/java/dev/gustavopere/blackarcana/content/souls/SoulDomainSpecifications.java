package dev.gustavopere.blackarcana.content.souls;

import dev.gustavopere.blackarcana.api.ArcanaSpellId;
import dev.gustavopere.blackarcana.core.domain.ArcanaDomain;
import dev.gustavopere.blackarcana.core.domain.SpellImplementationSpec;
import dev.gustavopere.blackarcana.core.domain.SpellImplementationSpecRegistry;
import dev.gustavopere.blackarcana.core.world.WorldEffectMode;

import java.util.List;
import java.util.Objects;

public final class SoulDomainSpecifications {
    public static final ArcanaSpellId MORTAL_LEDGER = ArcanaSpellId.parse("black_arcana:mortal_ledger");
    public static final ArcanaSpellId SPIRIT_SIGHT = ArcanaSpellId.parse("black_arcana:spirit_sight");

    private SoulDomainSpecifications() { }

    public static List<SpellImplementationSpec> all() {
        return List.of(
            new SpellImplementationSpec(
                MORTAL_LEDGER,
                ArcanaDomain.SOULS_DEATH,
                "Eligible credited deaths fill a bounded ledger that can form a few atomically consumed Soul Anchors.",
                "Malum spirit economy + Black Arcana death-prevention state",
                "passive credited-death ledger plus explicit anchor formation",
                "caster-owned death state; qualifying death sources only",
                "typed Malum spirit value or configured fallback only when explicitly enabled",
                0L,
                "credit=baseSpiritValue*antiFarmWeight; anchor forms at configured finite threshold",
                "T4 Sepulchral",
                WorldEffectMode.OFF,
                "hard anchor cap, one activation per death event, configurable PvP/boss semantics",
                "anchor cap, eligible deaths, anti-farm weights, threshold, recovery lockout",
                "docs/design/candidate-specifications.md#mortal-ledger--soul-anchor"),
            new SpellImplementationSpec(
                SPIRIT_SIGHT,
                ArcanaDomain.SOULS_DEATH,
                "Reveal supported spirit/occult traces without becoming a generic entity or player-wallhack.",
                "Malum/Eidolon adapters plus Black Arcana trace whitelist",
                "low-cost toggle/presentation effect",
                "only whitelisted supported occult traces within host visibility rules",
                "low/toggle upkeep",
                0L,
                "visibility=providerAvailable && traceKind in explicitWhitelist",
                "T1 Sepulchral",
                WorldEffectMode.COSMETIC,
                "never reveals hidden players or private container data",
                "range/presentation density and provider-specific supported trace categories",
                "docs/design/candidate-specifications.md#spirit-sight")
        );
    }

    public static void installInto(SpellImplementationSpecRegistry registry) {
        Objects.requireNonNull(registry, "registry");
        all().forEach(registry::register);
    }
}
