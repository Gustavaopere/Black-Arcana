# Malum

Status: `PHASE 2 — PROVIDER AUDIT IN PROGRESS`

## Runtime identity

- Provider: **Malum**
- Installed JAR: `malum-1.21.1-1.8.2.jar`
- Runtime version: `1.8.2`
- Loader/game: NeoForge 1.21.1
- Role: `SPIRIT ARCANA / SPIRIT RESOURCE / RITE / TOTEM / PACT PROVIDER`
- Installed ecosystem additions: Gaze `1.1.7.1`, Malum: Vestis, JEI Malum.

The current modlist is authoritative for installed `1.8.2`.

## Version / source boundary

The public `SammySemicolon/Malum-Mod` `1.21.1` branch is newer than the installed artifact. At the time of this audit its `gradle.properties` reports **Malum 1.9.0**, while the pack runs **1.8.2**.

Therefore Phase 2 separates evidence:

- facts independently documented for 1.8.2 or visible in pack/current public release metadata may be treated as installed-provider facts;
- registry/content found only on the newer 1.9.0 source branch is marked **NEWER-BRANCH EVIDENCE — VERIFY IN 1.8.2**;
- no 1.9.0-only capability is counted as installed coverage until confirmed against 1.8.2.

The upstream repository metadata does not currently expose a GitHub license object and the current source branch itself declares `mod_license=All Rights Reserved`. Public distribution pages may display other license metadata, but Black Arcana must treat implementation reuse as **not authorized by this audit** until exact artifact/source licensing is reconciled in the provenance ledger.

## Installed 1.8.2 provider identity — proven

Malum is a spirit/soul-magic system where spirits are **typed provider resources**, not a generic mana bar. Current project guides and public 1.8.2 evidence establish:

- spirit harvesting / Spirit Reaping from creatures;
- typed spirits used as crafting/ritual ingredients;
- Spirit Infusion;
- Spirit Focusing;
- Spirit Rites / totem magic;
- spirit-powered gear, runes, tools, weapons and curios;
- Encyclopedia Arcana progression.

An issue explicitly filed against **Malum 1.8.2** shows datapack recipe syntax consuming typed spirit resources such as `malum:earthen`, confirming that provider-owned spirit typing is part of the installed line.

## Spirit type registry

### Newer 1.9.0 branch evidence — verification required for installed 1.8.2

The current 1.21.1 source branch registers nine Spirit Arcana types:

1. `malum:sacred`
2. `malum:wicked`
3. `malum:arcane`
4. `malum:eldritch`
5. `malum:aerial`
6. `malum:aqueous`
7. `malum:earthen`
8. `malum:infernal`
9. `malum:umbral`

The first eight are also grouped as base/aspected spirits in current source. `umbral` has a specialized `UmbralSpiritArcanaType`.

**Do not yet claim all nine exist unchanged in installed 1.8.2.** Exact 1.8.2 registry extraction remains required. At minimum, typed spirit resource semantics and `earthen` are directly supported for the installed release line.

## Spirit Rites

Malum Totem/Spirit Rite magic is a persistent area/world-effect system and is semantically distinct from instant Iron's spellcasting.

### Newer 1.9.0 branch rite registry — verify against 1.8.2

Current branch defines 24 named rites, grouped in six families of four:

#### Sacred-style group

- Rite of Healing
- Rite of Nourishment
- Rite of Nurturing
- Rite of Lust

#### Wicked-style group

- Rite of Harming
- Rite of Empowerment
- Rite of Culling
- Rite of Raising

#### Aerial-style group

- Rite of Howling Gale
- Rite of Sky Tether
- Rite of Gravity
- Rite of Ascension

#### Aqueous-style group

- Rite of Flowing Grasp
- Rite of Good Tides (`rite_of_good_ties` registry path in current source)
- Rite of Soaking
- Rite of Sapping

#### Earthen-style group

- Rite of Stone Ward
- Rite of Oaken Might
- Rite of Creation
- Rite of Destruction

#### Infernal-style group

- Rite of Burning Fervor
- Rite of Fiery Embrace
- Rite of Smelting
- Rite of Quickening

The current branch's rite-effect registry confirms effect families including healing, nourishment, nurturing, animal love, harming, empowerment, culling, monster raising, wind/sky/gravity effects, fluid/growth/extraction effects, stone/creation/destruction and infernal/smelting/furnace acceleration.

These names are **not yet counted as exact installed 1.8.2 capability coverage** until artifact/version reconciliation is complete.

## Geas / Pacts / Oaths / Authorities

### Newer 1.9.0 branch evidence — high relevance to Binding, but not yet installed-proof

The current source branch contains a first-class `GeasEffectType` registry with **34 active entries** across Pacts, Oaths and Authorities.

Active pact names include, among others:

- Pact of Defiance
- Pact of the Parasite
- Pact of the Lifeweaver
- Pact of the Warlock
- Pact of the Reaper
- Pact of the Berserker
- Pact of the Fortress
- Pact of the Shield
- Pact of Reciprocation
- Pact of the Shattering Addict
- Pact of the Arcanaphage
- Pact of Rune Exploitation
- Pact of Self Care
- Pact of the High Priest
- Pact of Patience Repaid
- Pact of the Windswept
- Pact of the Continuing Shot
- Pact of the Skybreaker
- Pact of Contentedness
- Pact of the Lone Druid
- Pact of the Profane Ascetic
- Pact of the Profane Glutton
- Pact of Combustion
- Pact of the Prospector
- Pact of the Blastweaver
- Pact of Wyrd Reconstruction

Current branch also registers six Oaths and two Authorities.

Two multiplayer `Bond` concepts are present only as **commented-out source prototypes**:

- Bond of Beloved Chains — proposed shared visibility/healing/no-friendly-fire semantics;
- Bond of Death's Seekers — proposed distributed damage/scythe/armor tradeoffs.

These commented entries are **not gameplay and must never be counted as provider coverage**. They are recorded only because they show the provider's design vocabulary.

### Binding consequence

Until exact 1.8.2 verification is complete, Black Arcana must assume that generic `pact/geas/oath` design is collision-prone. The intended Arcana Vincular delta should stay centered on **cross-provider typed relationship + external resource routing + transactional reserve/commit/refund**, not merely on naming a buff a Pact.

## Spirit-resource authority

A Malum spirit is not interchangeable with:

- Goety Soul Energy;
- Eidolon Soul Shards;
- Iron's mana;
- blood mB / Hematic Reservoir;
- Infernal Lava mB;
- Toxony affinity/toxicity;
- generic XP or health.

Black Arcana's current Malum bridge already follows the correct authority principle: real provider spirit resources are queried/consumed/refunded by typed identity rather than synthesized from generic death events. Exact death→spirit attribution remains fail-closed where no causal provider hook proves the generated value.

## Soulbinding / crafting surface

The current source family includes explicit `Soulbinding` recipes and Spirit Infusion/Focusing recipes that consume typed spirit counts. Even before every recipe is enumerated, this establishes an important dedup rule:

- `soulbinding` in Malum is a provider crafting/process term;
- Black Arcana must not use the same term for an unrelated generic player-to-player binding system without clear namespace/UI distinction;
- recipes that spend Malum spirits must continue to spend Malum spirits rather than a converted generic `soul mana` balance.

Exact 1.8.2 Soulbinding recipe catalog remains pending.

## Divine / Infernal overlap

If confirmed in installed 1.8.2, Sacred and Infernal spirits create **resource-level thematic overlap** with the planned Divine and Infernal schools. This does not make Malum the owner of Holy miracles or the Nether-only Infernal Lava reservoir, but it blocks treating `sacred essence` or `infernal spirit` as newly invented resources.

The intended separation should remain:

- Malum Sacred/Infernal Spirit → typed spirit arcana reagent/resource;
- Divine/Celestial → Holy/miracle/theurgy authority and celestial conditions/providers;
- Infernal Lava → Nether-only external fluid/reservoir authority for Black Arcana's future Infernal system.

## Acquisition / progression

Malum progression is provider-owned through:

- Encyclopedia Arcana;
- spirit harvesting/reaping;
- Spirit Infusion;
- Spirit Focusing;
- totems / Spirit Rites;
- soulbinding/ritual/crafting chains;
- equipment and spirit-based materials.

Black Arcana should not grant Malum spirit knowledge merely because a player learns a Black Arcana Soul/Binding perk.

## Installed addon boundaries

### Gaze 1.1.7.1

Extends Malum's ecosystem and must be cataloged separately where it adds player-facing capabilities.

### Malum: Vestis

Equipment/vanity extension; classify capability-by-capability rather than assuming new spell authority.

### JEI Malum

UI/recipe support, not a spell provider.

## Deduplication consequences

Malum materially occupies or threatens overlap with:

- typed soul/spirit resources;
- spirit harvesting;
- spirit crafting/infusion/focusing;
- persistent totem/rite effects;
- pacts/geas/oaths if present in the installed line;
- healing/harming/raising/gravity/ward/smelting effect families through rites;
- sacred/infernal thematic resources.

This strongly narrows the Black Arcana gaps:

- no generic `spirit mana`;
- no duplicate spirit-harvest economy;
- no generic pact system until 1.8.2 Geas presence is verified;
- no new Sacred/Infernal spirit reagent names that collide with Malum;
- Arcana Vincular remains viable specifically as a cross-provider typed router/relationship system.

## Open audit items

- extract exact installed 1.8.2 spirit type registry;
- determine which of the current 24 rites existed in 1.8.2 and record exact recipes/ranges/effects;
- determine whether Geas/Pacts/Oaths/Authorities are present in 1.8.2 or are 1.9.0 additions;
- enumerate 1.8.2 Soulbinding recipes;
- catalog Spirit Reaping causal hooks and exact output identity;
- catalog Gaze and Vestis capability deltas;
- identify public integration/API surfaces safe for Black Arcana;
- reconcile exact license/provenance for the installed 1.8.2 source line.

## Phase 3 gate

Malum-related implementation is `BLOCKED` until exact 1.8.2 artifact capability reconciliation is complete.
