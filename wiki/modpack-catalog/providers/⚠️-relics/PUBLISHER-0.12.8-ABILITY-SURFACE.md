# Relics 0.12.8 — publisher/current-doc ability surface

## Evidence boundary

Physical authority:

`neoforge-rpg-skilltree@d7c99d23ef1b38fe62c86a362ec521ced8861f96`

Installed identity:

- `relics-1.21.1-0.12.8.jar`;
- mod id `relics`;
- runtime `0.12.8`;
- SHA-1 `1fe7d57ebfa56ebd0aeecfed01075f8b55b94ef7`.

Exact publisher artifact:

`https://www.curseforge.com/minecraft/mc-mods/relics-mod/files/8158315`

Current official docs:

`https://www.shatterbyte.com/docs/mods/relics/`

This inventory is clean-room documentation of public identities and high-level behavior. It does not copy implementation bodies.

## Release correlation

The exact publisher 0.12.8 changelog says that 0.12.8 adds **Shield of Retaliation**.

The current official docs list Shield of Retaliation among the base Relics roster. This establishes a strong version-line correlation between the current docs and the installed 0.12.8 content surface.

It does not prove that every current docs datum is byte-identical to the installed JAR.

## Current documented base relic roster

The current official Relics index lists exactly 20 base identities:

| # | Relic |
|---:|---|
| 1 | Leafy Mantle |
| 2 | Springy Boot |
| 3 | Kinetic Belt |
| 4 | Reflective Necklace |
| 5 | Jellyfish Necklace |
| 6 | Midnight Mantle |
| 7 | Roller Skate |
| 8 | Chorus Staff |
| 9 | Piglin Mask |
| 10 | Cut Glass Boot |
| 11 | Ring of the Seven Deadly Sins |
| 12 | Sphere of Self-Sacrifice |
| 13 | Hunting Belt |
| 14 | Chef's Hat |
| 15 | Clot of Time |
| 16 | Rider Flute |
| 17 | Experience Disperser |
| 18 | Glitchy Mantle |
| 19 | Ghostly Mantle |
| 20 | Shield of Retaliation |

Roster cardinality: **20 current documented base relics**.

This is a relic/item count, **not** the semantic action numerator.

## Explicit current-doc ability identities observed

The current publisher documentation exposes at least the following named provider abilities:

| Relic | Ability identities explicitly observed |
|---|---|
| Leafy Mantle | Camouflage |
| Reflective Necklace | Damage Condensation |
| Jellyfish Necklace | Aquatic Regeneration; Electric Discharge |
| Midnight Mantle | Lunar Phase; Shadow; Constellation; Starfall |
| Roller Skate | Acceleration |
| Chorus Staff | Teleportation |
| Piglin Mask | Neutrality; Barter; Looting |
| Cut Glass Boot | Glass |
| Ring of the Seven Deadly Sins | Pride; Envy; Wrath; Sloth; Greed; Gluttony; Lust |
| Sphere of Self-Sacrifice | Sacrifice |
| Hunting Belt | Arsenal Expansion; Pack |
| Clot of Time | Transgression |
| Rider Flute | Stable |
| Experience Disperser | Experience Dispersion |
| Glitchy Mantle | Surface Tear observed; additional ability/synergy content must be closed before final count |
| Ghostly Mantle | Grave Mist observed; additional ability content must be closed before final count |
| Shield of Retaliation | Retaliation |

This table is deliberately an **observed minimum**, not an exhaustive count.

Springy Boot, Kinetic Belt and Chef's Hat remain in the 20-relic roster but their complete named ability surfaces were not reliably retrievable through the current documentation indexing path during this audit.

## Examples of distinct action semantics

The documented provider powers are not merely tooltip aliases:

- Teleportation performs an active forward/targeted teleport using a regenerating internal buffer;
- Sacrifice consumes player health and establishes a provider recovery/projectile state;
- Transgression actively rewinds the bearer along their recent path;
- Stable stores/releases/recalls tamed mounts;
- Retaliation creates a timed parry window and cooldown;
- Electric Discharge manages charges, target filtering and chained attacks;
- Experience Dispersion redistributes provider XP;
- the Seven Deadly Sins are seven independently named progression/behavior identities.

These are relevant to deduplication against future Black Arcana powers.

## Synergies are not silently counted

Official docs also expose a separate `Synergies` section. Example: Glitchy Mantle + Jellyfish Necklace can expose a named Electric Rift synergy.

A synergy is not automatically treated as:

- a base relic ability;
- a separate spell;
- a new semantic action.

Synergy cardinality requires its own exact inventory and identity rule.

## Rank modifiers and modes are not identities

Examples such as:

- Enabled/Disabled;
- Full Moon/New Moon;
- rank 1/3/5 modifiers;
- quality/stat scaling;
- extra projectiles/bounces/stuns unlocked at rank;

do not independently increase the semantic action count unless the provider explicitly represents them as distinct actions.

## Semantic state

Provider-owned discrete powers: **confirmed**.

Exact final cardinality: **PENDING**.

Reason: exact physical 0.12.8 ability registry/resource identity inventory is not yet independently reconstructed, and the current documentation surface is current/version-correlated rather than immutable build-pinned.

## Runtime state

Still fail-closed:

- actual deployed target toggles;
- FTB Teams target settlement;
- ability enablement and stat configs;
- Curios equip/unequip exactly-once handling;
- cooldown/buffer persistence;
- relic XP persistence and overflow behavior;
- synergies;
- addon coexistence;
- server/restart/migration;
- player death/dimension lifecycle.

## Clean-room result

This audit establishes a provider-owned power system and a 20-relic current roster while refusing to assign an unsupported final ability count.

Status: **⚠️ partial / conditioned**.
