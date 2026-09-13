# 07A.07 — Provider Contract Verification & Fail-Closed Adapters

## State

`PLANNED / NOT IMPLEMENTED`

## Objective

Prove every provider hook required by 07A against the exact physically installed version before implementation depends on it.

## Physical baseline at planning time

The supplied physical modlist is authority for presence/version. Relevant entries include:

- NeoForge `21.1.248`;
- Iron's Spells 'n Spellbooks `3.16.3`;
- Ars Nouveau `5.13.1`;
- Eidolon: Repraised `0.5.0.2`;
- Malum `1.8.2`;
- Goety `3.1.4`;
- Vampirism `1.10.13`;
- Ars 'n' Spells `3.3.2`.

Mahou Tsukai is not physically installed and must not become a dependency.

Implementation must re-read the then-current physical modlist because these pins may drift.

## Verification matrix

### Iron's

Prove, for the exact installed version:

- supported spell invocation/registration or host boundary actually used by current Black Arcana adapter;
- mana quote/reservation/mutation semantics sufficient for D017;
- caster/target/cast causality;
- channel/cooldown interaction;
- whether presentation can be used without executing a second provider-owned gameplay effect;
- whether transformed/fused/metamagic parameters can be represented safely or must remain Black Arcana-native.

If the adapter cannot preserve one canonical transaction, do not use Iron's as host for that mechanic.

### Ars Nouveau

Prove only the hooks needed for approved integration. Do not introspect/replace Ars glyph semantics unnecessarily.

Required questions:

- can the exact spell/glyph identity needed for an approved fusion be observed/resolved causally?
- can Black Arcana add a cross-domain semantic without double spending Ars mana or duplicating native augments?
- does the provider expose a stable public integration seam for the intended use?

If not, keep the feature provider-native Ars or Black Arcana-native; do not use mixins/reflection as an assumed bridge.

### Eidolon

Re-verify the current callback/session identity problem before any Ankh, contract or grand-ritual player reward relies on Eidolon presentation.

Required proof:

- exact ritual/caster identity;
- cancellation/failure semantics;
- exactly-once completion causality;
- resource/material consumption relationship;
- server-thread/lifecycle behavior.

If caster identity is insufficient, player-specific Black Arcana completion remains fail-closed and the Stage 06 native ritual engine is used.

### Malum

Prove exact spirit query/reservation/commit behavior for any selected spirit-backed ritual/metamagic cost. A thematic spirit concept is not enough.

No direct undocumented storage mutation. No duplicate spirit drops/rewards.

### Goety

Only verify if a concrete 07A mechanic actually selects Goety for summon/minion hosting. Required proof includes ownership, despawn/death, dimension/lifecycle and cost causality. Otherwise no new Goety dependency is added by this stage.

### Vampirism

07.08 owns the full exact-version gate for thirst/feeding. 07A consumes that canonical adapter if/when implemented and must not create a parallel Vampirism bridge.

### RPG Skill Tree

Verify the then-current public/read-only progression contract used for gates. 07A must not write internal attachments or move cast/hazard/resource authority into RPG Skill Tree.

## Evidence standard

Acceptable evidence:

- exact installed API/source artifact documentation;
- exact JAR public signatures/metadata where API/source is insufficient;
- existing Black Arcana integration tests against the exact dependency;
- real-modpack validation where the task explicitly requires it.

Not acceptable as proof:

- old plans;
- thematic similarity;
- class/method names from another version;
- UI observation for server state;
- generic NeoForge events that cannot preserve causal identity;
- reflection/mixin assumptions without a separate reviewed decision.

## Adapter behavior

Every optional adapter must expose explicit capability/support status. Unsupported/incompatible state fails only the dependent feature, not the entire Black Arcana runtime.

Fallback is allowed only when it preserves the mechanic's identity and accounting. A visual-only fallback cannot silently replace a provider-native resource or causal hook.

## Tests first

For each selected adapter add deterministic tests for:

- provider absent;
- provider present/supported;
- provider present but incompatible/unknown;
- duplicate event/replay;
- resource quote failure;
- provider mutation failure where recoverable;
- lifecycle invalidation/reload;
- no double processing through generic NeoForge + provider-specific hooks.

Real-modpack/manual validation remains explicit where automated fixtures cannot prove renderer/provider behavior.

## Acceptance

- exact-version evidence recorded for every 07A provider dependency;
- no guessed API/hook;
- unsupported combinations fail closed;
- one causal action -> one Black Arcana transaction/reward path;
- provider versions and mod ids reconciled against the physical modlist at implementation time.
