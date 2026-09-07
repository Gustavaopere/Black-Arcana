# Cataclysm: Spellbooks — technical audit

## State

`EXTERNAL PROVIDER / INSTALLED 1.1.13 BETA / PUBLIC 1.1.11-LABELLED SOURCE BASELINE / EXACT CURRENT REGISTRY BLOCKED`

## Evidence ladder

### Authority 1 — physical pack

The current Black Arcana modlist contains:

- JAR: `cataclysm_spellbooks-1.1.13-1.21.jar`
- mod id: `cataclysm_spellbooks`
- runtime version: `1.1.13-1.21`

This is the authority for installed identity.

### Authority 2 — current publisher file metadata

CurseForge File ID `8792628` confirms:

- filename `cataclysm_spellbooks-1.1.13-1.21.jar`;
- NeoForge;
- Minecraft `1.21.1`;
- Beta channel;
- upload date `2026-09-02`;
- publisher delta: updated art, more spells ported, bug fixes and a new boss;
- explicit beta stability warning.

The current project description states **65 new spells** and identifies Abyssal and Technomancy as provider schools.

### Authority 3 — public source baseline only

Official repository: `AceTheEldritchKing/Cataclysm_Spellbooks_1.21.1`.

Pinned factual snapshot: `82a0af71f051058fe515c8b1cb9168e7f972f41c`.

At that commit:

- `gradle.properties` still declares `mod_version=1.1.11-1.21`;
- the source cannot be assumed equivalent to the installed 1.1.13 beta;
- `SpellRegistries.java` contains 34 concrete `registerSpell(...)` calls;
- `CSSchoolRegistry.java` registers Abyssal, Technomancy and Sand;
- Technomancy has zero concrete registrations in that old `SpellRegistries.java` despite its school existing.

The detailed 34-entry inventory is in [`SOURCE-1.1.11-BASELINE.md`](SOURCE-1.1.11-BASELINE.md).

## What the baseline can establish

The old source is strong enough to prove historical/provider identity and semantic occupancy, including:

- Abyssal combat/control and underwater magic;
- Ender/void/gravity capabilities;
- Evocation theft;
- Holy Cataclysm-derived summons;
- a large Fire/Ignis line;
- Ice/Maledictus combat and summon effects;
- Sand/desert content using a provider-owned Sand sub-school;
- provider-native spell classes built on Iron's spell API.

It also proves that provider-owned schools can delegate selected mechanics back to Iron's. For example, the Sand sub-school uses its own school resource id while reusing Iron's Nature spell power/resistance and Nature damage/cast sound.

## What the baseline cannot establish

The old source does **not** prove for 1.1.13:

- the 65 exact current spell resource IDs;
- exact current school distribution;
- exact current rarity/levels/cooldowns;
- mana/cast/range/damage/healing formulas;
- current acquisition/loot/crafting rules;
- current spellbook/item/entity/effect registries;
- the identity or behavior of the new 1.1.13 boss;
- which old WIP comments became implemented;
- which old implementations were removed, renamed or reworked.

The arithmetic gap `65 - 34 = 31` is only a provider-scale difference between two evidence surfaces. It is not an exact release diff.

## Baseline examples — do not promote to 1.1.13 balance

### Void Beam

At the pinned 1.1.11-labelled source snapshot, `VoidBeamSpell` declares:

- resource id `cataclysm_spellbooks:void_beam`;
- Abyssal school;
- Epic minimum rarity;
- max level 3;
- cooldown 20 seconds;
- base mana 100 + 10/level;
- base spell power 5 + 5/level;
- Instant cast;
- target helper range 32;
- recast count `1 + spellLevel`.

These are **baseline facts only**.

### Sandstorm

At the same snapshot, `SandstormSpell` declares:

- resource id `cataclysm_spellbooks:sandstorm`;
- provider Sand school;
- Rare minimum rarity;
- max level 3;
- cooldown 30 seconds;
- base mana 60 + 10/level;
- base spell power 2 + 2/level;
- cast time 25 ticks;
- Long cast type.

Again, none of those numbers is current until 1.1.13 is independently proven.

## Acquisition evidence boundary

The older source includes provider-native acquisition restrictions for some families. For example, historical Ignis spell code checks Cataclysm resources such as Burning Ashes. That establishes a real provider-owned progression pattern, but exact current 1.1.13 acquisition must be revalidated before any recipe/loot table is canonized.

Black Arcana must preserve provider-native acquisition where it remains current rather than replacing it with a duplicate Black Arcana economy for thematic uniformity.

## Architecture / authority consequence

- Iron's owns the standard spell substrate it exposes to addons.
- Cataclysm: Spellbooks owns its spell/content registrations and provider-local state.
- L_Ender's Cataclysm owns original Cataclysm entities/materials/mechanics.
- Black Arcana owns only Black Arcana runtime and may observe/integrate through a real boundary.

No Cataclysm: Spellbooks cast may be double-settled by Black Arcana. No second mana charge, duplicate cooldown, duplicate damage/heal, duplicate summon or duplicate world effect is allowed merely because Black Arcana is tracking Arcane Danger or semantic overlap.

## Deduplication gates

The exact 1.1.13 current table remains required before finalizing:

- **Infernal** against Fire/Ignis/soul-fire providers;
- **Order** against Technomancy control/construct/projectile capabilities;
- **Chaos** against boss-derived spectacle/reality-like effects;
- future Space/Displacement additions against provider Void/gravity content;
- summon/familiar candidates against provider summon roles.

The old 34-entry baseline is enough to reject obvious duplicates, but not enough to prove a gap.

## License / clean-room finding

At the pinned source commit:

- `TEMPLATE_LICENSE.txt` contains **PolyForm Shield License 1.0.0**;
- `gradle.properties` declares `mod_license=All Rights Reserved`;
- current CurseForge metadata labels the project PolyForm Shield License 1.0.0.

This is not treated as a source-reuse grant for Black Arcana. PolyForm Shield also includes a noncompete restriction. The project therefore uses the source only as `REFERENCE_ONLY` factual evidence; no code/assets are copied or adapted.

## Current blocking condition

The official CurseForge download path was reached and verified, but the permitted tools did not receive the binary JAR payload for inspection. No decompilation was performed and no current bytecode was inferred from the stale source.

**PENDÊNCIA — REQUER ARTEFATO EXATO / NAVEGAÇÃO EXTERNA CAPAZ DE ENTREGAR O BINÁRIO**

Required closure sequence:

1. obtain the exact `cataclysm_spellbooks-1.1.13-1.21.jar` through an authorized inspectable path;
2. verify artifact hash/metadata;
3. enumerate current spell/school/item/entity/effect registries without copying implementation;
4. reconcile the exact 65 current spell identities against the 34-entry public-source baseline;
5. extract only factual current configs/contracts needed by the catalog;
6. run full-pack/runtime QA for any compatibility assertion;
7. only then close the provider's exact-current Phase 2 spell inventory gate.