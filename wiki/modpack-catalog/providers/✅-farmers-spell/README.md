# Farmer's Spell 'n Spellbooks 1.0.5.1

Status: `EXACT SOURCE-PINNED 1.0.5.1 CATALOG / 6 REGISTERED SPELL IDENTITIES / HOST-NATIVE SCROLL-FORGE REACHABILITY / COMPONENT #63 / CURRENT-HOST RUNTIME QA FAIL-CLOSED`

## Installed authority

- Current JAR: `farmers-spell-n-spellbook-1.0.5.1-1.21.1.jar`
- Mod id: `farmers_spell`
- Runtime version: `1.0.5.1-1.21.1`
- Minecraft / loader: `1.21.1` / NeoForge
- Physical SHA-1: `f77355e029af39bbaba3854e10cc087a608351ff`
- Physical CurseForge hash: `810347191`
- License: `All Rights Reserved`
- Provider class: `MIXED`
- Required providers: Iron's Spells 'n Spellbooks, Farmer's Delight and GeckoLib

The physical modlist remains authority for the installed JAR/runtime/hash. Public source is used only to close factual registry, dependency, acquisition and interoperability surfaces; it is not treated as a binary hash proof of the physical artifact.

## Exact official source checkpoint

The current 1.21.1 public source is pinned to:

- repository: `GLDYM/Farmers-Spell-n-Spellbook`
- commit: `b7cbb40316a9ccbbc2ce2b56b3023647261ce569`
- tree: `83f54cd2415b424d1fc209191f6a3f90bd919312`
- recursive tree: complete (`truncated=false`)
- commit purpose: version bump from `1.0.5.0-1.21.1` to `1.0.5.1-1.21.1`

The exact source declares Minecraft `1.21.1`, NeoForge build `21.1.238`, Java 21 and `ARR`. Its runtime metadata requires Iron's `[3.16.0,)`, Farmer's Delight `[1.2.8,)` and GeckoLib `[4.7.5.1,)`.

## Provider role

Farmer's Spell is not only a bridge. It owns a dedicated Gluttony spell school and six Iron's spell registrations while also adding magical cooking, food, gear, effects, Foodgeist progression and related support content. Under the canonical taxonomy this is a `MIXED` provider.

The semantic spell inventory is closed in [EXACT-1.0.5.1-SPELL-INVENTORY.md](EXACT-1.0.5.1-SPELL-INVENTORY.md).

## Acquisition and reachability

The Gluttony school sets `allowLooting=false`, so generic random Iron's scroll loot must not be claimed as the route for these spells.

Provider data instead defines `farmers_spell:gluttony_focus` with `#minecraft:foods` and `farmers_spell:foodgeist_seasoning`. The public Iron's 3.16.3 source-line Scroll Forge contract resolves a school from a matching focus and presents that school's spells subject to enabled/craftable/player gates. No Farmer's Spell override of those three spell gates was found for the six registered classes.

Foodgeist Seasoning itself is also connected to provider-owned survival surfaces: Foodgeist spawning around provider cooking blocks, successful Foodgeist interaction reward and Foodgeist entity loot. Therefore the provider has a host-native acquisition route without Black Arcana fabricating one.

This closes catalog reachability, not final probability/economy balance or assembled-pack runtime acceptance.

## Authority and deduplication

Iron's Spells 'n Spellbooks remains authority for its generic spell registry, mana/cast lifecycle, school/focus and Scroll Forge substrate. Farmer's Spell owns Gluttony-specific school/content semantics and its provider progression. Farmer's Delight remains authority for its base food/cooking substrate.

Black Arcana must not create parallel authority for:

- Gluttony school identity or spell-power attribute;
- the six provider spell registrations;
- Iron's mana/cooldown/cast settlement for those spells;
- Scroll Forge/focus acquisition;
- Foodgeist spawn/reward progression;
- provider projectiles, area entities or status effects;
- magical-cooking recipe/state ownership.

A future Black Arcana integration must use a verified provider/host-native boundary and preserve one causal settlement. Black Arcana remains authority over Black Arcana casting, Arcane Danger, Corruption, Strain, persistence and `WorldEffectPolicy`.

## Current runtime ceiling

Catalog/source identity is closed, but current-host runtime compatibility is not.

- source build: NeoForge `21.1.238`; physical pack: `21.1.248`;
- source build: Farmer's Delight `1.3.2`; physical pack: `1.3.4`;
- source build and physical pack: GeckoLib `4.9.2`;
- provider has seven required mixins, including three client/render mixins;
- physical Iron's is `3.16.3`, matching the public source line used for narrow SchoolType/Scroll Forge interpretation by version label; no cryptographic source/binary equivalence is claimed;
- client boot, dedicated-server boot, mixin application, provider progression and representative execution of all six spells remain direct QA work.

Dependency ranges or version-label equality are not a runtime PASS.

## Semantic disposition

Phase 2BO contributes **+6 `COUNTED_SOURCE_PINNED`** semantic spell identities.

The Gluttony school is taxonomy/support for the six actions and is not counted as a seventh object under the current semantic metric. At the Phase 2BO checkpoint, the shared-ledger state was **1322 strict semantic objects / 63 of 100 provider components**. That pair is a historical Phase 2BO snapshot, not a live aggregate; current aggregate totals are maintained in the shared semantic/component ledgers. These catalog values do not certify current-host runtime compatibility.

## Clean-room boundary

The upstream is All Rights Reserved. Black Arcana retains only factual identities, physical SHA-1/CurseForge hash, registry/count/type relationships, narrow acquisition relationships and interoperability risk facts. No upstream implementation bodies, assets, localization prose, models, sounds or creative text are copied or adapted.
