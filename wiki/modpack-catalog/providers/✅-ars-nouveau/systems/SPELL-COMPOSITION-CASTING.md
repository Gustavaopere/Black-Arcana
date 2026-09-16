# Ars Nouveau — Spell Composition & Casting Authority

State: `SOURCE-PINNED 5.13.1 / CORE PIPELINE AUDITED / RUNTIME+CONFIG QA PENDING`

Exact release checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`.

## Canonical spell model

Ars Nouveau owns a compositional spell grammar. A spell is an ordered sequence of registered `AbstractSpellPart` entries. Core 5.13.1 exposes 85 production spell parts: 5 Forms/Methods, 13 Augments and 67 Effects. Addons may register additional parts in the same provider registry, but that does not transfer ownership of the cast pipeline away from Ars Nouveau.

`SpellTier` defines provider tiers `ars_nouveau:one`, `two`, `three` and `creative` with numeric values 1, 2, 3 and 99.

## Spell Books / caster tools

Core spell books are:

- `ars_nouveau:novice_spell_book` — `SpellTier.ONE`;
- `ars_nouveau:apprentice_spell_book` — `SpellTier.TWO`;
- `ars_nouveau:archmage_spell_book` — `SpellTier.THREE`;
- `ars_nouveau:creative_spell_book` — creative-only tier 99.

`SpellBook` implements the Ars `ICasterTool` surface and stores a `SpellCaster` data component with 10 slots by default. Using a non-creative book server-side raises the mana capability's remembered book tier when appropriate and synchronizes glyph-count bonus state. The client UI selects spell slots; selection itself is not cast authority.

Other Ars caster tools (for example Wand, Caster Tome, Spell Bow/Crossbow and other provider items) still converge on Ars caster/resolver contracts. Their existence is not a reason for Black Arcana to create a second Ars cast path.

## Client intent → server cast

`AbstractCaster.castOnServer()` sends provider packet `ars_nouveau:cast_spell`. `PacketCastSpell` carries selected slot, camera rotation and hand. On server receipt, Ars re-reads the caster from the actual held stack with `SpellCasterRegistry.from(stack)` and resolves the selected spell there.

The server-side `AbstractCaster.castSpell(...)` then:

1. obtains the actual held stack;
2. rejects non-server worlds;
3. applies provider `modifySpellBeforeCasting`;
4. validates spell structure;
5. creates `SpellContext` / wrapped caster / `SpellResolver`;
6. performs provider ray trace and resolves entity/block/general casting through the appropriate Form;
7. leaves mana settlement to `SpellResolver`.

Client camera rotation is still user intent. It does not make client-authored spell cost, target eligibility or effects authoritative.

## Validation and mana settlement

`SpellResolver.canCast()` runs the provider spell validator before checking mana. `SpellResolver.getResolveCost()` uses the spell's configured cost minus provider discounts, then fires `SpellCostCalcEvent.Pre` and clamps the result to at least zero.

For a successful Form resolution, `SpellResolver` calls `expendMana()`. The amount actually expended is recalculated through `SpellCostCalcEvent.Post` and clamped to at least zero. Turret casters are explicitly exempted by the provider's `expendMana()` branch and therefore must not be treated as manual player mana settlement.

Effects resolve server-side through `SpellResolveEvent` and `EffectResolveEvent` hooks plus block/entity spell-resolve capabilities. Child contexts used by Rune, Linger, Wall, Burst, Orbit and similar effects remain Ars-owned continuation of the provider cast, not independent Black Arcana casts.

## Default starter glyphs

`GlyphRegistry.getDefaultStartingSpells()` is config-driven. The source defaults are the spell parts whose `defaultedStarterGlyph()` returns true. In the exact 5.13.1 release checkpoint these are:

1. `ars_nouveau:glyph_projectile` — Projectile;
2. `ars_nouveau:glyph_touch` — Touch;
3. `ars_nouveau:glyph_self` — Self;
4. `ars_nouveau:glyph_break` — Break;
5. `ars_nouveau:glyph_harm` — Harm.

Runtime server config can change the `starter` flag, so this list is the **5.13.1 source default**, not an assertion that a customized pack config must keep all five enabled as starters.

## Learning authority

Non-starter glyph knowledge is persisted by Ars player data. Using a Glyph item server-side:

- rejects a disabled glyph;
- rejects a glyph already known or currently considered a starter;
- calls the provider `unlockGlyph` capability path;
- synchronizes player data;
- updates the mana capability's glyph-count bonus when needed;
- consumes one Glyph item in non-infinite-material modes.

Black Arcana and RPG Skill Tree must not maintain a second canonical "known Ars glyphs" ledger.

## Black Arcana boundary

- Ars owns glyph identity, spell grammar, validation, caster slots, mana cost/discounts, effect resolution and Ars projectile/child-context lifecycle.
- Black Arcana must not wrap each Effect into a second independent cast, charge Ars mana again, or award multiple cast causalities for one composed spell.
- RPG Skill Tree may observe a real provider contract for progression/mastery but must not replace Ars glyph learning or perk/thread ownership.
- Destructive Black Arcana mechanics still route through `WorldEffectPolicy`; provider-native Ars world effects are catalogued for overlap/deduplication, not as permission to bypass Black Arcana safety.
