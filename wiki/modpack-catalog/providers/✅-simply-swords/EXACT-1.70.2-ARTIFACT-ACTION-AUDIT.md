# Simply Swords 1.70.2 — exact artifact action audit

Checkpoint: 2026-09-29

## Evidence class

`EXACT HASH-MATCHED ARTIFACT / RELEASE-CORRELATED SOURCE CLASSIFICATION / EXACT ACTION DENOMINATOR 66 / DEPLOYED REACHABILITY OPEN / +0 STRICT`

## Purpose

Close the prior uncertainty around legacy/non-opted `UniqueWeaponActiveAbility` and Secondary player-action paths without reconstructing or retaining provider implementation bodies.

This audit answers one bounded catalog question:

> Does the exact physically installed 1.70.2 artifact expose any additional player-invoked Simply Swords action root beyond the 62 source-classified ACTIVE Unique roots and four source-classified player-use Runic action families?

Result: **no**.

## Physical artifact identity

Current sibling authority at
`neoforge-rpg-skilltree@51751e6c77530a7d8825ec42493ffccedf978d1a`
records row #503:

- JAR: `simplyswords-neoforge-1.70.2-1.21.1.jar`;
- runtime: `1.70.2-1.21.1`;
- category includes `Magic`.

Canonical physical SHA-1:

`05b074ff774467f1fe9fb5592151b7845c321cbc`

Publisher anchor:

- CurseForge project: Simply Swords;
- File: `8746001`.

## Non-merge exact-artifact audit

Evidence PR:

- PR: `#448`;
- branch: `audit/simply-swords-1702-exact-artifact-2026-09-29`;
- final audited SHA: `dd7f5450b93f4f6004a3f73b53b121898349d459`;
- exact-artifact workflow: `Simply Swords 1.70.2 exact artifact audit`;
- final audit run: `36524073819`;
- final audit result: **SUCCESS**.

The workflow materializes exact CurseForge File `8746001` via Curse Maven and refuses inspection unless the downloaded SHA-1 equals the physical catalog hash.

The successful final run recorded:

- SHA-1: `05b074ff774467f1fe9fb5592151b7845c321cbc`;
- metadata mod id: `simplyswords`;
- metadata version: `1.70.2-1.21.1`;
- provider top-level classes: **666**;
- exact `UniqueAbilityDefinition` fields across built-in/Phase2–Phase10 registries: **121**;
- `ItemsRegistry` custom class references: **54**;
- registered concrete custom classes: **54**.

The audit retains bounded factual archive/class/interface/member/call-target facts only. Full disassembly is not persisted or published.

## Exact Active and Secondary surface

The exact artifact contains **51 registered concrete custom classes** whose provider inheritance chain implements
`UniqueWeaponActiveAbility`.

The final gate asserts the entire 51-class set, not only its cardinality, against the version-declared 1.70.2 source line. The gate passed:

`registered_active_class_set_matches_version_declared_source = true`

No concrete Active class exists in the provider archive outside the registered set:

`unregistered_concrete_active_classes = []`

Exactly **2** registered classes implement the Secondary contract:

1. `StormscaleSwordItem`;
2. `WraithmawSwordItem`.

The exact Secondary set gate passed:

`registered_secondary_class_set_matches_version_declared_source = true`

No unregistered concrete Secondary class exists:

`unregistered_concrete_secondary_classes = []`

## Residual non-Active direct-use surface

Exactly two registered custom classes expose a player `use` method while not implementing the Active interface:

1. `RighteousRelicSwordItem`;
2. `TaintedRelicSwordItem`.

The exact set gate passed:

`registered_non_active_use_class_set_matches_version_declared_source = true`

The same two classes are the only registered custom classes with action-shaped methods but neither Active nor Secondary membership.

## Bounded exact call-target reconciliation

The final audit uses `javap -c` only inside four specifically selected methods and retains only their invoked method targets.

All four semantic reconciliation gates passed:

`bounded_residual_action_targets_match_version_declared_source = true`

### Righteous Relic

`RighteousRelicSwordItem#use` invokes:

`UniqueSwordItem.use(...)`

No independent provider action implementation is selected by this override.

Disposition: **alias/pass-through / +0 roots**.

### Tainted Relic

`TaintedRelicSwordItem#use` invokes:

`UniqueSwordItem.use(...)`

Disposition: **alias/pass-through / +0 roots**.

### Stormscale Secondary

`StormscaleSwordItem#startPlayerSecondaryAbility` invokes:

`StormscaleLightningRodManager.tryReactivate(...)`

The version-declared source independently identifies this as reactivation of the already initiated Stormscale lightning-rod ability.

Disposition: **continuation/reactivation of existing Stormscale root / +0 roots**.

### Wraithmaw Secondary

`WraithmawSwordItem#startPlayerSecondaryAbility` invokes:

`WraithmawAbilityManager.tryDetonate(...)`

The version-declared source independently identifies this as detonation/continuation of the already initiated Wraithmaw ability.

Disposition: **continuation of existing Wraithmaw root / +0 roots**.

## Source classification retained

The exact artifact audit intentionally does not infer ACTIVE/PASSIVE kind from bytecode.

Semantic kind/root classification remains grounded in:

- primary release-correlated source:
  `Sweenus/SimplySwords@c82eeaf4479543a728340b9763ab445c9c9d4c0d`;
- version-declared cross-check:
  `Sweenus/SimplySwords@359a8031b1a3243d1a3b013dbaa0cbba70ea8278`.

Those checkpoints close:

- **62 ACTIVE Unique roots**;
- **59 PASSIVE** roots at the primary checkpoint;
- same **62 ACTIVE** + **60 PASSIVE** at the later cross-check;
- **4** causal player-use Runic families;
- **17** Weapon Implicits excluded as proc/passive behavior.

The exact JAR independently exposes **121 `UniqueAbilityDefinition` fields**, consistent with the primary source registry cardinality while leaving semantic kind classification to source evidence.

## Special source-line reconciliation

Several class/owner relationships are not simple name equality but do not add roots:

- `DormantRelicSwordItem` dispatches by Awakening form to the already-counted Sunfire/Harbinger action families;
- Watcher concrete items share the provider Watcher active substrate while source root definitions distinguish their relevant action identities;
- source-defined compatibility roots such as Dreadtide remain subject to deployed compat/reachability state and are not multiplied by item/class plumbing.

The audit found no hidden registered concrete Active or Secondary class outside the exact bounded inventory.

## Exact denominator

Source-classified causal roots:

- 62 ACTIVE Unique roots;
- 4 player-use Runic roots.

Exact residual artifact surface:

- 2 Secondary continuations: +0;
- 2 direct-use pass-through overrides: +0;
- hidden/unregistered concrete Active classes: 0;
- hidden/unregistered concrete Secondary classes: 0.

Arithmetic:

`62 + 4 + 0 = 66`

Therefore the **current Simply Swords 1.70.2 player-action denominator is exactly 66** for the Black Arcana semantic metric.

The previous `LOWER_BOUND 66` state is superseded.

## What remains open

This audit closes identity/action cardinality only. It does not establish the active subset in the deployed modpack.

Still fail-closed:

- deployed Awakening/unlock state;
- current acquisition/reformation paths;
- config/datapack/script suppression;
- compatibility-dependent materialization/reachability;
- assembled-pack runtime behavior;
- persistence/migration;
- Epic Fight/Lootr coexistence;
- addon operational ownership where current deployed paths overlap.

Until those are captured, Simply Swords remains:

`⚠️ EXACT DENOMINATOR 66 / +0 STRICT`

## Clean-room boundary

The provider source line uses the Timefall Development License 1.2.

Black Arcana retains only factual interoperability/catalog evidence:

- artifact cryptographic identity;
- metadata;
- class/interface/member identities;
- registry cardinalities;
- bounded selected-method call targets;
- release-correlated root identifiers/classification.

No upstream implementation body, asset, model, sound, localization prose or full disassembly is copied into Black Arcana.