# 07A.03 — Bounded Spell Fusion

## State

`PLANNED / NOT IMPLEMENTED`

## Objective

Allow approved cross-domain combinations such as control/tendrils + fire, frost or blood without constructing a second Ars-like spell grammar or nesting independent casts.

## Core invariant

Fusion resolves before ordinary resource commit into **one canonical Black Arcana cast transaction**.

One fusion operation has exactly one:

- cast identity/replay claim;
- progression admission;
- target resolution;
- resource transaction;
- cooldown decision;
- Arcane Danger transaction;
- world-effect admission;
- success/reward causality identity.

Fusion components are semantic ingredients, not child casts.

## Planned data contract

A bounded fusion definition should contain, at minimum:

- stable fusion id;
- admitted base capability/spell tag or exact allowlist;
- admitted infusion/aspect;
- explicit incompatible spell/aspect list;
- target-shape compatibility rule;
- bounded potency/duration/area/target transformation;
- cost transformation or added provider-native component;
- cooldown transformation;
- hazard transformation;
- world-effect policy requirement;
- progression gate;
- presentation host/visual key;
- hard caps and schema version.

Datapacks remain declarative under D021. Definitions may select from registered bounded strategies; they must never name arbitrary Java classes, commands or scripts.

## Resolution pipeline

Planned flow:

1. canonical cast ingress resolves caster/spell/loadout and replay identity;
2. server resolves requested/selected fusion from server-owned loadout/progression state;
3. fusion registry validates base+aspect compatibility;
4. fusion planner produces an immutable resolved cast specification;
5. canonical targeting validates the transformed target geometry;
6. canonical world/hazard preflights evaluate the transformed specification;
7. one composite cost transaction reserves provider resources;
8. one effect path executes the fused semantics;
9. ordinary canonical commit/cooldown/hazard success handling runs once.

The implementation must integrate with the then-current `ArcanaCastIngressService`, canonical runtime and D024 channel path rather than bypassing them.

## Provider-native-first rules

### Ars Nouveau

Ars owns glyph/augment composition. If the desired result is already safely expressible as an Ars spell with native augments, do not clone that grammar into Black Arcana.

Black Arcana fusion may use Ars only when an exact-version adapter can prove the composed spell identity/parameters needed for Black Arcana safety and causality. Otherwise the combination is provider-native Ars behavior outside this stage or is implemented as a bounded Black Arcana-native semantic combination.

### Iron's Spells

Iron's is preferred for fixed active combat spell presentation where the existing adapter can preserve one canonical Black Arcana transaction. Do not fire an Iron's spell and then separately fire a Black Arcana child cast.

### Blood aspect

Blood infusion must reuse Blood & Curses/07.08 contracts. It must not invent a second blood meter or silently turn a spell Umbral unless the resolved source actually steals non-consensual blood/life.

## Initial fusion candidates

The first implementation should be deliberately small and prove the architecture before broad content expansion.

Candidate family:

- **Tendrils + Fire** — control/entanglement plus bounded burn/heat component;
- **Tendrils + Frost** — control plus bounded slow/freeze-compatible component;
- **Tendrils + Blood** — control plus bounded blood-domain interaction; non-consensual extraction is Umbral.

Before implementation, provider catalogs must identify the exact existing tendril/control host and fire/frost capabilities. If no safe provider boundary exists, implement only the Black Arcana-native portion or leave the candidate blocked; do not invent API calls.

## Safety and anti-abuse

- transformed area/range/targets never exceed absolute canonical ceilings;
- destructive secondary effects route through `WorldEffectPolicy`;
- multi-tick secondary work is admitted to `BoundedWorkScheduler` before cost commit under D026;
- a fusion cannot recursively fuse or recursively echo itself;
- a fusion cannot convert one paid hit into unbounded chain damage;
- child semantics cannot emit independent ordinary offensive proc chains or independent Mastery/XP rewards;
- no duplicate kill attribution;
- failure of an optional provider component fails the fusion closed before resource commit unless the definition explicitly has a safe identity-preserving fallback.

## Tests first

RED tests must cover:

- one fusion produces one resource reservation and one cooldown;
- base+aspect incompatibility is denied before mutation;
- transformed targeting is server-owned and capped;
- world-destructive infusion cannot bypass policy;
- scheduler saturation denies before cost commit;
- provider adapter failure does not execute base spell as a misleading partial success unless an explicit safe fallback exists;
- blood fusion polarity changes only when resolved sourcing is extractive;
- duplicate/replayed cast id cannot replay fusion effects;
- fusion does not double-award progression/rewards;
- no fusion recursion.

## Acceptance

- small explicit fusion matrix, not arbitrary combinatorial explosion;
- single canonical transaction;
- provider-native composition preferred where it already exists;
- deterministic caps and config surfaces ready for Stage 08 tuning.
