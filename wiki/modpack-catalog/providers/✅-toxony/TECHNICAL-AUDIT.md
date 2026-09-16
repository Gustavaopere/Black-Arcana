# Toxony 0.10.7 — technical audit and provenance

## Installed artifact

Current modlist authority:

- JAR: `toxony-0.10.7.jar`;
- mod id: `toxony`;
- runtime: `0.10.7`;
- mixin config: `toxony.mixins.json`;
- SHA-1: `d92e0d0ae2ece85c353f22463fbc7c61595fca20`;
- CurseForge/package fingerprint: `1401862999`.

No claim in this audit overrides the physical modlist for installed identity.

## Exact public source version checkpoint

Repository: `MrFrostyDev/Toxony_Mod`

Commit:

`881bf7fe632659e748c279966a2bf49b99f7503f`

At that commit `gradle.properties` declares:

- Minecraft `1.21.1`;
- NeoForge `21.1.221`;
- mod id `toxony`;
- mod version `0.10.7`;
- Curios `9.5.1+1.21.1`;
- Iron's Spells `1.21.1-3.16.0`;
- `mod_license=GNU LGPL 3.0`.

The commit changes the mod version from `0.10.6` to `0.10.7` and includes the release-line fixes/updates.

## License conflict

The exact source checkpoint is internally inconsistent about licensing:

- `gradle.properties`: `GNU LGPL 3.0`;
- public distribution metadata: LGPLv3;
- root `LICENSE`: GNU GPL v3 text.

This is not silently interpreted in Black Arcana's favor.

Current posture:

`READ-ONLY FACTUAL SOURCE AUDIT ALLOWED FOR CATALOGING / SOURCE-DERIVED IMPLEMENTATION CONTRACT BLOCKED / NO CODE OR ASSET COPYING / REVIEW_REQUIRED`

A future derivation or tight source-coupled adapter requires explicit license reconciliation first.

## Exact registry evidence

At the pinned version checkpoint the source registers:

- 5 harmful MobEffects;
- 7 Mutagen MobEffects;
- 9 Oils in Toxony's custom Oil registry;
- 11 Affinities in Toxony's custom Affinity registry.

These counts are factual source observations and are documented in provider subcatalogs.

## Player state model — source-observed

`ToxData` contains synchronized provider state for:

- tox;
- tolerance;
- threshold;
- affinity map;
- mutagen list;
- known ingredient map;
- deathState.

Constants observed at the exact pin:

- `MAX_TOLERANCE = 999`;
- `MAX_MUTAGENS = 3`;
- `MIN_TOLERANCE = 10`;
- `DEFAULT_TOLERANCE = 30`;
- `THRESHOLD_MULTIPLIER = 100`.

Threshold advancement posts provider `ChangeThresholdEvent` and uses the triangular-number goal documented in the Mutagen catalog.

## Source-visible event surface

The exact source contains an `xyz.yfrostyf.toxony.api.events` package with:

- `ChangeToxEvent`;
- `ChangeToleranceEvent`;
- `ChangeThresholdEvent`.

`ToxData` posts those events on NeoForge's event bus before corresponding provider mutations. `ChangeThresholdEvent` is cancellable and exposes old/new threshold plus the `ToxData` reference.

### API caution

This is evidence that the upstream project intentionally uses an `api` namespace. It does **not** yet prove:

- a separately published/stable API artifact;
- binary compatibility policy;
- semantic compatibility with the exact installed JAR;
- permission to derive Black Arcana implementation against internals while the license conflict is unresolved.

Therefore these events are `CANDIDATE BOUNDARIES / NOT YET APPROVED ADAPTER CONTRACTS`.

## Iron's version drift

Toxony 0.10.7 source builds against Iron's `1.21.1-3.16.0`.

The modpack currently installs Iron's `1.21.1-3.16.3`.

The source resolves Iron's School Spell Power attributes dynamically by registry id and adds five Mutagen modifiers. This is promising compatibility evidence, but exact 3.16.3 runtime behavior remains unverified.

Black Arcana must fail closed rather than infer that a 3.16.0 source observation is a guaranteed 3.16.3 integration contract.

## Vampirism / Werewolves compatibility

The source compatibility helper defines EntityType tags:

- `vampirism:vampire`;
- `werewolves:werewolf`.

Its silver helper multiplies damage by `1.5` for matching targets. Direct source usages located at this pin include Flintlock Ball and Flail Ball damage settlement.

This does not prove a universal +50% modifier for every silver-themed item in the pack.

## High-risk static observations

### Necrotic resurrection cooldown

Executable 0.10.7 source:

`DEFAULT_RESURRECTION_COOLDOWN = 200`

The neighboring `48000` is commented. The active source value equals 10 seconds at 20 ticks/s. Runtime QA is required because older descriptive material may still imply a much longer cooldown.

### Mutagen equal-score selection

Threshold selection aggregates candidate weights in a `HashMap` and changes the current winner only on a strictly larger score. Equal-score order has no explicit stable tie-break contract. Runtime/behavior tests must not assume a deterministic winner without evidence.

### Multi-threshold promotion

When one change skips multiple thresholds, the selection loop runs repeatedly against the same Affinity map; Affinities are cleared only after that loop. This can legitimately produce repeated Mutagen entries, which then stack amplifier when the provider reapplies its Mutagen list.

## Installed-runtime QA matrix

Before any provider-specific integration can be promoted:

1. verify installed artifact behavior against the exact 0.10.7 public source checkpoint;
2. verify the three player threshold crossings and max-three list behavior;
3. verify equal-score Affinity selection behavior;
4. verify repeated-threshold/duplicate Mutagen stacking;
5. verify Necrotic resurrection and 200-tick cooldown;
6. verify five Iron's School Spell Power modifiers against installed 3.16.3;
7. verify Vampirism/Werewolves tag matching against installed versions;
8. verify Curios Toxicity Gauge behavior if Black Arcana needs equipment observation;
9. determine whether upstream documents the `api` namespace as a supported external contract;
10. reconcile GPLv3/LGPLv3 license evidence before any source-derived implementation or redistribution decision.

## Black Arcana gate

Current technical integration state:

`FAIL-CLOSED FOR PROVIDER-SPECIFIC ADAPTER IMPLEMENTATION`.

Factual source cataloging is stronger than before, but it is not runtime validation, API stability evidence or source-reuse authorization.
