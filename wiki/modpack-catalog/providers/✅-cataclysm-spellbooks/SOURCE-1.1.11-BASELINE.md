# Cataclysm: Spellbooks — public 1.1.11-labelled source baseline

Status: `BASELINE ONLY — NOT THE INSTALLED 1.1.13 REGISTRY`

This document records facts from the official public 1.21.1 repository at commit `82a0af71f051058fe515c8b1cb9168e7f972f41c`.

The physical Black Arcana pack instead contains `cataclysm_spellbooks-1.1.13-1.21.jar`. The public repository still declares `mod_version=1.1.11-1.21`, so none of the registry rows below are promoted to current-1.1.13 identity without separate current-artifact evidence.

## Source identity

- Upstream: `AceTheEldritchKing/Cataclysm_Spellbooks_1.21.1`
- Commit: `82a0af71f051058fe515c8b1cb9168e7f972f41c`
- Commit date: `2026-03-29`
- Source-declared mod id: `cataclysm_spellbooks`
- Source-declared version: `1.1.11-1.21`
- Source-declared Minecraft: `1.21.1`
- Source-declared NeoForge baseline: `21.1.219`
- Source-declared Iron's baseline: `1.21-3.8.0`

This is a **public-source baseline**, not evidence that the installed 1.1.13 binary is source-equivalent.

## Registered spell count in this snapshot

`SpellRegistries.java` contains exactly **34 concrete `registerSpell(...)` registrations** in this source snapshot.

Comments describing planned/WIP spells are intentionally excluded. In particular, the large Abyssal rework list, Blood concepts, additional Ender/Fire/Ice concepts and the Technomancy design list are comments rather than registrations in this snapshot.

| Source grouping | Concrete registrations |
| --- | ---: |
| Abyssal | 7 |
| Ender | 4 |
| Evocation | 1 |
| Holy | 3 |
| Fire / Ignis | 9 |
| Ice / Maledictus | 4 |
| Nature/Sand section | 6 |
| **Total** | **34** |

## Concrete registration inventory

The symbols below are the exact Java registration symbols and implementation classes visible in `SpellRegistries.java`. They are baseline evidence only.

| Source grouping | Registration symbol | Implementation class | Source comment / semantic label |
| --- | --- | --- | --- |
| Abyssal | `VOID_BEAM` | `VoidBeamSpell` | Void Beam |
| Abyssal | `ABYSSAL_BLAST` | `AbyssalBlastSpell` | Abyssal Blast |
| Abyssal | `DIMENSIONAL_RIFT` | `DimensionalRiftSpell` | Dimensional Rift |
| Abyssal | `DEPTH_CHARGE` | `DepthChargeSpell` | Depth Charge |
| Abyssal | `ABYSSAL_PREDATOR` | `AbyssalPredatorSpell` | Abyssal Predator |
| Abyssal | `ABYSSAL_SLASH` | `AbyssalSlashSpell` | Tidal Tear in source comment |
| Abyssal | `TIDAL_GRAB` | `TidalGrabSpell` | Tidal Claw / grab |
| Ender | `VOID_RUNE` | `VoidRuneSpell` | Void Rune |
| Ender | `VOID_BULWARK` | `VoidRuneBulwarkSpell` | Void Bulwark |
| Ender | `GRAVITY_STORM` | `GravityStormSpell` | Gravity Storm |
| Ender | `GRAVITATION_PULL` | `GravitationPullSpell` | Gravitational Pull |
| Evocation | `PILFER` | `PilferSpell` | Steal / Pilfer |
| Holy | `CONJURE_KOBOLDIATOR` | `ConjureKoboldiatorSpell` | Summon Koboldiator |
| Holy | `CONJURE_KOBOLETON` | `ConjureKoboletonSpell` | Summon Koboleton |
| Holy | `THOTHS_WITNESS` | `ThothsWitnessSpell` | Thoth's Witness |
| Fire | `INCINERATION` | `IncinerationSpell` | Incineration |
| Fire | `INFERNAL_STRIKE` | `InfernalStrikeSpell` | Infernal Strike |
| Fire | `CONJURE_IGNITED_REINFORCEMENT` | `ConjureIgnitedReinforcement` | Summon Ignited reinforcement |
| Fire | `HELLISH_BLADE` | `HellishBladeSpell` | Hellish Blade |
| Fire | `BONE_STORM` | `BoneStormSpell` | Bone Storm |
| Fire | `BONE_PIERCE` | `BonePierceSpell` | Blazing Bone Spit / Bone Pierce |
| Fire | `ASHEN_BREATH` | `AshenBreathSpell` | Ashen Breath |
| Fire | `ABYSS_FIREBALL` | `AbyssFireballSpell` | Abyss Fireball |
| Fire | `TECTONIC_TREMBLE` | `TectonicTrembleSpell` | Tectonic Tremble |
| Ice | `MALEVOLENT_BATTLEFIELD` | `MalevolentBattlefieldSpell` | Malevolent Battlefield |
| Ice | `FORGONE_RAGE` | `ForgoneRageSpell` | Forgone Rage |
| Ice | `CONJURE_THRALL` | `ConjureThrallsSpell` | Conjure Thrall |
| Ice | `CURSED_RUSH` | `CursedRushSpell` | Cursed Rush |
| Nature/Sand section | `SANDSTORM` | `SandstormSpell` | Sandstorm |
| Nature/Sand section | `DESERT_WINDS` | `DesertWindsSpell` | Desert Winds |
| Nature/Sand section | `MONOLITH_CRASH` | `MonolithCrashSpell` | Monolith Crash |
| Nature/Sand section | `AMETHYST_PUNCTURE` | `AmethystPunctureSpell` | Amethyst Puncture |
| Nature/Sand section | `CONJURE_AMETHYST_CRAB` | `ConjureAmethystCrabSpell` | Summon Amethyst Crab |
| Nature/Sand section | `PHARAOHS_WRATH` | `PharaohsWrathSpell` | Pharaoh's Wrath |

## Provider-owned school registry in the baseline

`CSSchoolRegistry.java` registers three provider-owned `SchoolType` entries:

1. `cataclysm_spellbooks:abyssal`
   - provider-owned power/resistance attributes;
   - provider-owned Abyssal damage type;
   - provider Abyssal focus tag.
2. `cataclysm_spellbooks:technomancy`
   - provider-owned power/resistance attributes;
   - provider-owned Technomancy damage type;
   - provider Technomancy focus tag.
3. `cataclysm_spellbooks:sand`
   - explicitly described in source as a **Sand sub-school**;
   - reuses Iron's Nature spell power/resistance and Nature damage/cast sound;
   - uses a provider school id while inheriting Nature-facing mechanics.

The 1.1.11-labelled `SpellRegistries.java` snapshot has no concrete Technomancy spell registrations despite registering the Technomancy school. That is direct evidence that this source snapshot predates the current 65-spell surface and cannot stand in for 1.1.13.

## Example exact baseline spell contract

`VoidBeamSpell` proves the level of detail available in the old source without making it current:

- baseline resource id: `cataclysm_spellbooks:void_beam`;
- baseline school: Abyssal;
- baseline minimum rarity: Epic;
- baseline max level: 3;
- baseline cooldown: 20 s;
- baseline base mana: 100;
- baseline mana/level: 10;
- baseline base spell power: 5;
- baseline spell power/level: 5;
- baseline cast time: 0;
- baseline cast type: Instant;
- baseline target helper range: 32 blocks;
- baseline recasts: `1 + spellLevel`.

`SandstormSpell` similarly proves the provider-owned Sand sub-school in the baseline:

- baseline resource id: `cataclysm_spellbooks:sandstorm`;
- baseline school: `cataclysm_spellbooks:sand`;
- baseline minimum rarity: Rare;
- baseline max level: 3;
- baseline cooldown: 30 s;
- baseline base mana: 60;
- baseline mana/level: 10;
- baseline base spell power: 2;
- baseline spell power/level: 2;
- baseline cast time: 25 ticks;
- baseline cast type: Long.

These numbers are useful for historical semantic comparison only. They are **not current 1.1.13 balance values**.

## Numerical gap to the current public provider claim

The current publisher page states **65 new spells**. This baseline contains **34 registered spells**. The arithmetic difference is **31**, but that number must not be interpreted as “31 exact new spell IDs” because the intervening releases may add, remove, rename, port or rework registrations.

What can safely be concluded is only that the public 1.1.11-labelled registry snapshot is materially incomplete relative to the current advertised provider surface.

## Licensing / clean-room boundary

The same upstream commit contains `TEMPLATE_LICENSE.txt` with PolyForm Shield License 1.0.0, while `gradle.properties` still declares `mod_license=All Rights Reserved`. CurseForge currently labels the project PolyForm Shield License 1.0.0.

Because the source metadata is not internally uniform and PolyForm Shield contains a noncompete restriction, this repository treats the upstream source as **read-only factual reference only**. No Cataclysm: Spellbooks code, assets, models, sounds or text are copied/adapted into Black Arcana.

## Promotion rule

Nothing in this file becomes a current 1.1.13 per-spell contract until one of the following exists:

- the exact installed/distributed 1.1.13 JAR is inspected through an authorized technical path; or
- the publisher exposes matching 1.1.13 source/API/documentation that proves the current registry/value.

Until then, exact current registry IDs, per-spell costs, cooldowns, damage formulas and acquisition remain fail-closed.