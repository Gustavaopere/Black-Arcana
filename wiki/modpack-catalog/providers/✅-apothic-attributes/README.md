# Apothic Attributes 2.10.1

## Status

`SOURCE-VERSION-PINNED EXACT 2.10.1 / COMBAT+ATTRIBUTE+EFFECT SUPPORT PROVIDER / 0 STANDALONE SPELLS / COMPONENT #42 CANDIDATE`

Apothic Attributes is a combat/attribute/effect support provider, not a spell engine. The exact 2.10.1 source exposes attributes, effects, potions, damage types, equipment-slot abstractions, item modifier composition, cooldown support, networking/config synchronization and combat-rule hooks. No provider-owned standalone spell, glyph or ritual registration surface was observed in the exact source tree.

## Physical identity

- artifact: `ApothicAttributes-1.21.1-2.10.1.jar`
- mod id: `apothic_attributes`
- version: `2.10.1`
- physical SHA-1: `6a6b84d09801621df5cc2c8a68f35bd93a6cda0f`
- Minecraft: `1.21.1`
- loader: NeoForge
- physical NeoForge: `21.1.248`
- physical Placebo: `9.9.2`
- physical Curios: `9.5.1+1.21.1`

## Exact official source pin

`Shadows-of-Fire/Apothic-Attributes@686361b2c7b0e76bf4158890bb8a2e42ef805622`

The pinned 1.21 branch commit is titled `2.10.1`. Its build metadata declares:

- `modid=apothic_attributes`
- `version=2.10.1`
- Minecraft `1.21.1`
- Java 21
- NeoForge build baseline `21.1.235`
- required Placebo `9.9.0`
- optional Curios

Generated runtime metadata requires Minecraft `>=1.21.1`, NeoForge `>=21.1.235` and Placebo `>=9.9.0`, side BOTH. The physical pack satisfies those declared minimums. Version-range satisfaction is not promoted to byte-for-byte source/JAR reproducibility.

## Closed semantic surface

The exact source closes:

- 2 synchronized custom registries;
- 22 attributes;
- 7 mob effects;
- 31 potions;
- 37 generated brewing mixes;
- 5 damage-type keys/data entries;
- 2 data components;
- 3 attachments;
- 7 built-in equipment-slot objects and 11 slot groups;
- 3 provider tag contracts;
- 1 particle and 1 sound;
- 2 clientbound PLAY payloads;
- 7 common mixins + 1 client mixin;
- combat/attribute event runtime;
- public server-side `AbilityCooldowns` API;
- optional Curios attribute/modifier bridge.

Standalone semantic spells/glyphs/rituals: **0 observed**.

## Authority and deduplication

- **Apothic Attributes** owns its armor/protection formula replacement, penetration/shred semantics, crits, auxiliary damage, dodge, life steal/overheal, projectile/arrow modifiers, healing/XP/mining modifiers, potion/effect behavior and its `AbilityCooldowns` subsystem.
- **Curios** remains authority for Curios inventory/slot state. Apothic only bridges attribute-modifier presentation/composition when Curios is loaded.
- **Black Arcana** remains authority for BA casting, transactional costs, BA cooldowns/charges, targeting, Corruption, Strain, Arcane Danger, Backlash and WorldEffectPolicy.
- **RPG Skill Tree** remains progression/Mastery/perk authority only through real contracts.

Similarity does not create a bridge. In particular, `apothic_attributes:cooldown_reduction` is not automatically applied to Black Arcana cooldowns, and BA Backlash must not be routed through Apothic crit/life-steal/auxiliary-damage proc paths.

## Important exact-source observations

- `DetonationEffect` consumes remaining fire ticks on its last tick but its exact `hurt(...)` call uses `ALObjects.DamageTypes.BLEEDING`, even though `DamageTypes.DETONATION` is separately registered/tagged. This catalog records the literal source behavior and does not silently repair or reinterpret it.
- `current_hp_damage` is tagged physical and excluded from Apothic critical strikes.
- `detonation`, `fire_damage` and `cold_damage` are tagged as NeoForge magic damage.
- bleeding/detonation/fire/cold bypass armor in the provider datapack tags.
- both provider payloads are clientbound; no provider C2S cast-intent path was found.

## Evidence boundary

Confirmed: exact physical identity/hash, exact public 2.10.1 source-version pin, complete central registry inventory and source-visible runtime/config/network/mixin surfaces.

Not claimed: byte-for-byte public-source/JAR reproducibility; full-modpack runtime interaction with every combat provider; any Black Arcana integration hook not explicitly exposed by the provider.

See:

- [`REGISTRY-AND-CONTENT-SURFACE.md`](./REGISTRY-AND-CONTENT-SURFACE.md)
- [`COMBAT-ATTRIBUTE-RUNTIME.md`](./COMBAT-ATTRIBUTE-RUNTIME.md)
- [`EFFECTS-POTIONS-AND-BREWING.md`](./EFFECTS-POTIONS-AND-BREWING.md)
- [`COOLDOWN-NETWORK-AND-CONFIG.md`](./COOLDOWN-NETWORK-AND-CONFIG.md)
- [`CURIOS-AND-MODIFIER-HOOKS.md`](./CURIOS-AND-MODIFIER-HOOKS.md)
- [`EVIDENCE-AND-PROVENANCE.md`](./EVIDENCE-AND-PROVENANCE.md)
