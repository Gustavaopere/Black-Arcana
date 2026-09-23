# Hazen N Stuff — 1.4.0.14

Status: `COUNTED_SOURCE_PINNED / +38 SEMANTIC SPELLS / CATALOG ✅ / RUNTIME QA FAIL-CLOSED`

## Current physical identity

The current sibling physical dossier at `neoforge-rpg-skilltree@278b427023136d7c43d85dc188d0eac1ac85ef3a` confirms:

- JAR: `hazennstuff-1.4.0.14.jar`;
- mod id: `hazennstuff`;
- runtime version: `1.4.0.14`;
- physical SHA-1: `3be20bacb44c1923348ab6f61b685eec6aacfdcd`;
- Minecraft: 1.21.1;
- physical host stack: Iron's Spells 'n Spellbooks 3.16.3 + HazentouveLib 1.0.9.

The exact public source checkpoint used for this catalog is:

`Hazentouvel/Hazen_N_Stuff@5fcaf39cf399609f6c1c87d14f8d4807098c9cce`

That commit is titled `1.4.0.14 beta.`, and its `gradle.properties` declares `mod_id=hazennstuff`, `mod_version=1.4.0.14`, Minecraft 1.21.1 and PolyForm Shield licensing.

This establishes a version-correlated **source pin**, not byte-for-byte equivalence between source output and the separately hashed physical JAR. The semantic inventory is therefore `COUNTED_SOURCE_PINNED`, not `COUNTED_EXACT`.

## Exact source-pinned spell registry

The release-pinned `HnSSpellRegistries` owns one Iron's `DeferredRegister<AbstractSpell>` under namespace `hazennstuff` and contains exactly **38 active spell registrations**.

Registry-level source inspection records:

- 38 active `Supplier<AbstractSpell>` registrations;
- 0 `if (...)` statements in the registry class;
- 0 `ModList` references in the registry class;
- 0 config references in the registry class.

The exact source localization contains 41 root `spell.hazennstuff.<id>` keys. Three are not active registrations in this release and are excluded:

- `hazennstuff:brimstone_hellblast` — localization-only;
- `hazennstuff:reign_of_tyros` — class/localization present, but its exact release registration line is commented;
- `hazennstuff:supernova` — localization-only.

The active 38 are cataloged in [SOURCE-1.4.0.14-SPELL-INVENTORY.md](./SOURCE-1.4.0.14-SPELL-INVENTORY.md).

## School/family distribution

The exact release registry groups the 38 active identities as:

| Family / school surface | Count |
|---|---:|
| Ender | 1 |
| Blood | 2 |
| Fire | 5 |
| Ice | 2 |
| Lightning | 3 |
| Nature | 4 |
| Evocation | 2 |
| Holy | 1 |
| Radiance | 4 |
| Shadow | 4 |
| Eldritch | 1 |
| Cosmic | 4 |
| Hydro | 5 |
| **Total** | **38** |

The grouping above follows the provider's own release registry organization. It does not rename provider schools or collapse them into Black Arcana domains.

## Crafting / reachability closure

No concrete registered spell class in the pinned release declares its own `allowCrafting`, `isEnabled` or `canBeCraftedBy` override.

Provider abstract spell bases add a special `canBeCraftedBy` gate to exactly three registered identities:

- `hazennstuff:golden_shower` — requires the provider's Golden Shower Spellbook;
- `hazennstuff:nights_edge_strike` — requires Night's Edge or True Night's Edge;
- `hazennstuff:scorching_slash` — requires Raven's Bane.

The same exact release source packages crafting recipes for the Golden Shower Spellbook, Night's Edge and Raven's Bane. These recipes also carry the corresponding spell/affinity identity, so those three special gates have a provider-owned survival acquisition path at catalog level.

For custom school focuses:

- Hazen adds `hazennstuff:stardust` to the HazentouveLib Cosmic focus;
- Hazen adds `hazennstuff:glowing_mushroom` to the HazentouveLib Radiance focus;
- Hazen adds `hazennstuff:shadow_scale` and `hazennstuff:nightmare_fuel` to the HazentouveLib Shadow focus;
- Hazen adds `hazennstuff:arcane_sea_shell` to the Ace's Spell Utils Hydro focus;
- Hazen adds `hazennstuff:charred_bones` to Iron's Fire focus;
- Hazen adds `hazennstuff:overgrown_bone` to Iron's Nature focus.

The current physical HazentouveLib 1.0.9 line is corroborated by public source commit `641acf4e9e254f1af9f59b2eb2251ff0f1fcfc08` (`HazentouveLib 1.0.9`). That source places its Cosmic, Shadow and Radiance focus tags into Iron's `school_focus`; the Hazen 1.4.0.14 release populates those focus tags. Hazen itself places the Hydro focus tag into Iron's `school_focus`.

This is sufficient for **catalog-level reachability** under the same Iron's host contract used by other source-pinned addons. It is not an assembled-pack runtime PASS.

## Public-page drift

The current sibling dossier preserves a 24-spell public-documentation baseline. That is useful publisher coverage but is not the release registry denominator.

The exact 1.4.0.14 source registry proves 38 active registrations. The public page therefore must not be used to truncate the installed-release catalog to 24.

Later source on the `1.21.1` branch also differs from the pinned release. For example, later source contains `coruscated_discharge`, while the pinned 1.4.0.14 registry does not register it. Later branch state is not projected backward into the installed release.

## Semantic catalog consequence

Hazen N Stuff contributes:

- **+38 `COUNTED_SOURCE_PINNED` semantic spell identities**;
- 3 non-active localization roots excluded (two localization-only plus one commented registration);
- no duplicate count for focuses, equipment, projectiles, effects, schools or spell containers.

The previously reconstructed strict semantic minimum of **1344** therefore becomes **1382**.

Hazen is an additional physically certified magic component discovered after the older 100-component technical denominator was established. It closes the next known provider component, but the old `68/100` ratio must now be treated as historical until the full current sibling modlist is re-based. Do not publish a new technical percentage from the stale denominator.

## Authority boundary

- Iron's Spells 'n Spellbooks owns the host spell registry, base casting, mana, cooldown and generic scroll/focus contract.
- HazentouveLib owns the shared Radiance/Shadow/Cosmic school infrastructure used by this ecosystem.
- Ace's Spell Utils owns its Hydro school/focus infrastructure.
- Hazen N Stuff owns its `hazennstuff` spell identities, provider gear, special unlock items and provider-local behavior.
- Black Arcana does not copy or reimplement Hazen spell bodies, assets, formulas or provider settlement.
- RPG Skill Tree remains progression/Mastery/perk authority only through real integration boundaries.

## Clean-room / license boundary

The source metadata declares PolyForm Shield. This catalog uses the public source only for factual interoperability/catalog facts: registry identities, class ownership, release-correlated configuration shape, focus/tag relationships and acquisition existence.

No provider implementation body, assets, recipes, localization prose or formulas are copied into Black Arcana. The source pin is catalog evidence, not implementation authority.

## Runtime state — fail-closed

Still unverified in the exact assembled modpack:

- dedicated-server boot with Hazen N Stuff 1.4.0.14 + HazentouveLib 1.0.9 + Iron's 3.16.3;
- actual registry sync and client connection;
- deployed Iron's generic spell enable/crafting config;
- cast/cancel/cooldown behavior for all 38 spells;
- exactly-once settlement for damage/projectiles/summons/effects;
- multiplayer caster/owner attribution;
- reload/restart behavior;
- provider compatibility with Ars Nouveau, Malum, Obscure Tooltips and Discerning the Eldritch;
- numerical balance and world/protection behavior.

Those runtime gates do not erase the source-pinned semantic catalog; they prevent claiming runtime compatibility or Black Arcana integration.

## Result

**✅ Cataloged at source-pinned semantic level: 38/38 active 1.4.0.14 spell registrations.**

Runtime/provider integration remains fail-closed until direct assembled-pack evidence exists.
