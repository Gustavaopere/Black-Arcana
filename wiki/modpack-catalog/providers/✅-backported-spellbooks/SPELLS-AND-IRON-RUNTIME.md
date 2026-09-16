# Backported Spellbooks — spells and Iron's runtime boundary

## Canonical semantic spell inventory at the source ceiling

The May 28 official source registers exactly six provider spells in Iron's spell registry:

| Registry ID | School | Rarity | Max level | Cooldown | Cast type | Base mana / per level |
|---|---|---:|---:|---:|---|---|
| `backportedspellbooks:slime_aspect` | Iron's Nature | Rare | 5 | 90s | instant | 35 / +5 |
| `backportedspellbooks:sulfur_bomb` | Iron's Nature | Uncommon | 8 | 12s | long | 30 / +5 |
| `backportedspellbooks:sulfur_clouds` | Iron's Nature | Rare | 10 | 16s | long | 50 / +5 |
| `backportedspellbooks:sulfur_release` | Iron's Nature | Common | 5 | 60s | long | 90 / +22 |
| `backportedspellbooks:pale_thorn` | `backportedspellbooks:pale_flora` | Common | 5 | 10s | instant | 25 / +15 |
| `backportedspellbooks:resin_spray` | `backportedspellbooks:pale_flora` | Common | 10 | 12s | continuous | 5 / +1 |

The first four are the publisher's exact 0.1.2 spell delta. Pale Thorn and Resin Spray already exist in the earlier May 18 source point.

## School surface

The provider registers one `SchoolType`:

- `backportedspellbooks:pale_flora`.

The inspected source binds this school to provider focus-tag/data and Iron's/Ace's-compatible damage/power surfaces. Java symbol names are not substituted for registry IDs.

## Behavioral summaries from release-day source

### Slime Aspect

- uses Iron's Nature school;
- applies provider `slime_aspect` effect;
- provider effect interacts with Vanilla Backport movement/bounce/air-drag attributes and vanilla jump-strength behavior.

Authority: Iron's cast/mana/cooldown; Backported owns the effect definition and effect behavior; Vanilla Backport owns the imported host attributes.

### Sulfur Bomb

- Nature spell;
- spawns provider sulfur-bomb projectile/entity;
- provider projectile owns its local hit/AOE behavior.

Authority: Iron's cast settlement; Backported projectile/effect semantics. BA must not wrap the same hit in a second cast or damage settlement.

### Sulfur Clouds

- Nature spell;
- server-side source emits three provider sulfur-cloud projectiles/entities;
- resulting cloud/effect behavior remains provider-owned.

Authority remains split between Iron's casting pipeline and Backported effect entities.

### Sulfur Release

- Nature spell;
- radial provider effect/damage behavior;
- applies provider Sulfuric Poison and confusion-related effects;
- references Vanilla Backport sulfur presentation/content.

Black Arcana must not infer Corruption, Strain or Arcane Danger merely from this provider spell firing. Any BA reaction requires a separate explicit BA contract.

### Pale Thorn

- Pale Flora school;
- source raycasts to a bounded range and creates provider pale-thorn visual/entity behavior;
- applies provider Paranoia;
- uses a damage calculation involving Iron's Nature/Eldritch power surfaces and provider school semantics.

This is a provider spell identity. Similar visual or control themes do not create a BA duplicate.

### Resin Spray

- Pale Flora school;
- continuous Iron's spell;
- uses Iron's `MagicData` additional-cast-data path;
- emits provider cone/projectile behavior and provider damage semantics.

The use of Iron's cast data is host-native settlement, not evidence for a second addon cast state.

## Iron's authority

All six spell objects extend/register through Iron's spell infrastructure. Consequently Iron's remains authority for:

- host cast state and cast progression;
- mana accounting;
- spell cooldown accounting;
- Iron's spell configuration plumbing;
- host casting/network synchronization;
- host spellbook/cast UX where applicable.

Backported Spellbooks owns:

- the six spell identities;
- one Pale Flora school identity;
- spell-specific projectiles/entities/effects/content;
- addon-specific numerical defaults and behavior observed in its source.

Black Arcana owns none of the above provider settlement simply because a theme overlaps BA.

## No duplicate-resource rule

No Backported-specific mana resource was observed. The spells consume Iron's mana through Iron's spell classes/configuration.

Therefore BA must not:

- create a second mana debit for these spells;
- mirror their cooldown into BA cooldown/charge state;
- replay their projectiles/effects through BA's canonical cast pipeline;
- translate Iron's client state into BA server authority;
- award RPG Skill Tree authority over provider spell execution.

A future progression bridge may gate or observe through a real contract, but runtime ownership remains with Iron's + Backported.

## Causality / Backlash boundary

Backported spell damage/effects are provider causality. BA Backlash is a distinct BA channel and must not be routed deliberately through Backported equipment/spell offensive proc paths.

Conversely, a provider spell event must not be treated as a BA cast unless a future adapter explicitly maps it with replay protection, deduplication and one settlement authority.

## Networking/persistence evidence ceiling

The inspected provider source did not expose a custom `CustomPacketPayload`/payload-registrar surface. No provider-owned player/world SavedData/attachment/data-component subsystem was observed.

That does not prove the physical JAR contains no generated/inherited serialization and does not authorize assumptions about Iron's networking. Iron's host runtime remains the network/cast authority for these spell objects.

## Runtime QA still required

- physical Iron's 3.16.3 compatibility versus source development baseline 3.15.4;
- exact physical spell registry parity;
- multiplayer cast lifecycle for all six spells;
- continuous Resin Spray start/continue/stop synchronization;
- repeated Sulfur projectile/AOE deduplication;
- spell cooldown/mana conservation under interruption/reconnect;
- provider interaction with BA damage/proc suppression only if a real bridge is later proposed.