# Apprentice's Codex — integration and deduplication rules

Source/catalog checkpoint: `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e` / installed `0.9.7.1`.

## Authority

Apprentice's Codex is an Iron's-native spell/content/equipment/utility provider.

- **Iron's Spells 'n Spellbooks** owns canonical spell schools, mana, standard cast lifecycle and base spell registry semantics.
- **Apprentice's Codex** owns its 83 spell implementations, custom entities/blocks/items, recast state, internal support equipment and optional compatibility behavior.
- **Black Arcana** remains authoritative for its own casting pipeline, Corruption, Strain, hazards, rituals, world-safety policy, forbidden-magic domains and persistence.
- **RPG Skill Tree** does not become runtime authority for Apprentice's Codex casts; any progression bridge must observe a real, causally safe provider boundary.

## No duplicate mana or cast settlement

A cast of `apprenticecodex:*` is an Iron's/Apprentice provider cast.

Black Arcana must not:

1. charge a second mana/resource cost for the same provider cast;
2. replay provider damage/healing/world effects in its own pipeline;
3. manufacture a second cooldown or recast state;
4. convert provider projectiles/entities into Black Arcana-owned damage sources after they are already settled;
5. treat chained provider effects as independent Black Arcana proc opportunities.

If a future bridge needs to award progression, it must preserve one causal identity and deduplicate repeated entity/projectile callbacks.

## Chaos overlap

Apprentice's Codex already covers a large amount of high-energy combat fantasy:

- summoned firearms and blades;
- explosive shells;
- homing missiles;
- broad force/heat waves;
- rapid barrages;
- mobile summoned weapons.

A spell does not become Black Arcana **Chaos** merely because it uses volatile visuals, random-looking projectiles or red/magenta particles. Chaos needs domain-specific instability/risk/cost semantics that are mechanically distinct from these provider spells.

## Order overlap

The provider also covers:

- Force Field;
- Mystic Shield;
- guard/stance weapon spells;
- detection and controlled utility;
- placed traps/totems;
- structured spellcasting equipment.

Black Arcana **Order** therefore needs imposed-law, seal, constraint, enforcement or deterministic-rule semantics rather than another generic barrier/defensive stance.

## Binding overlap

Apprentice's Codex includes companion constructs, summoned autonomous weapons, `Tamer's Pocket`, personal storage/domain-adjacent utility and ownership-bound summoned objects.

These do **not** automatically equal Black Arcana's typed persistent Binding contracts, but they occupy adjacent player-facing convenience niches. Black Arcana must not add a generic pet-storage or summon-recall spell without demonstrating a materially different persistent binding contract.

## Divination overlap

Direct overlap exists with Black Arcana Familiars & Divination planning:

- `Remote Eye` — remote vision;
- `Sense Evil` — detection/highlighting;
- `Deep Sensor` — vibration sensing through walls;
- `Treasure Divination` — proximity information;
- `Search Beacon` — structure-location workflow;
- `Terra Resonance` — gemstone detection through walls;
- `Otherworld Lens` — remote/alternate viewing surface.

Black Arcana divination must integrate/deduplicate instead of reproducing these capabilities under new names.

## World effects

Provider-local world-changing behavior remains provider-owned. Examples include Frost Rune placement, Catch Flame ignition, Earth Forge, World Flatter, Linear Build, Mage Light/Wizardlamp placement and similar spell-specific actions.

A future Black Arcana observer must not invoke `WorldEffectPolicy` as a second settlement layer **after** the provider has already performed an allowed world effect. Conversely, Black Arcana-originated destructive effects still require its own `WorldEffectPolicy`; provider behavior is not an exemption for Black Arcana casts.

## Optional compatibility

The exact source tree contains optional-development/compat surfaces for mods such as Create, Malum, Sable, Iron's Jewelry, Epic Fight and others. Development dependencies alone do not prove that a specific runtime seam is active in the user's pack.

For each future bridge:

1. verify the exact installed provider version from the modlist;
2. inspect the exact 0.9.7.1 compatibility code or public API seam;
3. confirm server/client authority;
4. preserve provider-native resource/cooldown/cast semantics;
5. fail closed if the seam cannot be proven safe.

## Canonical catalog path

The canonical provider tree is:

`wiki/modpack-catalog/providers/apprentice-codex/`

The older `providers/apprentices-codex/` placeholder tree is legacy and is removed by Phase 2L after its still-valid overlap notes are consolidated here.