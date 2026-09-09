# Phase 2AG — Ars 'n' Spells 3.3.2 Checkpoint

## Scope

Close the current Ars 'n' Spells magic/cross-domain catalog to the strongest evidence presently available without treating a 3.3.0 source tree as exact 3.3.2 binary authority.

Branch: `docs/magic-catalog-phase2ag-ars-n-spells-3.3.2`

Initial base: `main@6ef2fb6fee567dc4fbe3d340166829d042132bfb`

## Physical anchor

- `ars_n_spells-3.3.2.jar`
- mod id `ars_n_spells`
- version `3.3.2`
- SHA-1 `2d2274ff786c42ea46c53fec866116f83d98fe5a`
- Minecraft `1.21.1`
- NeoForge `21.1.248`
- physical pack contains Ars Nouveau `5.13.1` and Iron's Spellbooks `1.21.1-3.16.3`.

## Evidence ceiling

Exact release evidence:

- 3.3.1 NeoForge file `8827129`: transaction receipt HUD removed;
- 3.3.2 NeoForge file `8832580`: contextual Iron's mana-HUD visibility fixes; no config, network-protocol or save-format changes from 3.3.1.

Official same-loader/game source baseline:

- repository `otectus/ars-n-spells`;
- branch `port/neoforge-1.21.1`;
- commit `a9930223c96806e5d748ea69d02f9a32cab62de9`;
- source version `3.3.0`;
- build pins Minecraft 1.21.1, NeoForge 21.1.248, Ars 5.13.1.1400 and Iron's 1.21.1-3.16.3.

Exact 3.3.2 Java binary/source parity is **not claimed**.

## Catalog result

Current semantic provider surface closed in this pass:

- **5 ritual identities** under current pack conditions on the NeoForge 3.3.0 source baseline:
  - Spell Uninscription;
  - Spell Transcription;
  - Spellbook Binding;
  - Mana Infusion;
  - Mana Well;
- **5 mana-unification modes**;
- Spell Loom / carrier serialization and cleanup lifecycle;
- cross-engine cast/payment routing;
- finite **8-slot** Iron's proxy transport registry;
- provider-owned cross-system school/progression/equipment bridge boundary;
- current HUD delta: receipt panel removed, contextual mana visibility fixed.

Semantic standalone-spell count contributed by the eight fixed `ars_cross_*` proxy identities: **0**. They are real registry objects but represent transport slots for serialized Ars spells rather than eight fixed magical effects.

No Ars Nouveau glyph registration owned by Ars 'n' Spells was proven in this pass.

## Architecture result

Black Arcana must not add a second generic Ars↔Iron's mana ledger, carrier serializer, native-wheel proxy pool, inscription engine, provider cooldown/progression mirror or duplicate cross-cast settlement.

One routed action must retain one causal identity even when an Iron's proxy and delegated Ars payload are both observable.

Black Arcana retains authority over its own casting, Corruption, Strain, Arcane Danger and world-safety runtime. The provider bridge does not gain authority over those channels.

## Deferred evidence

Still explicitly pending:

- exact installed 3.3.2 JAR extraction/registry comparison;
- real full-modpack runtime validation of the five ritual paths;
- real full-modpack cross-cast/proxy interoperability validation;
- exact 3.3.2 internal hook verification for any future adapter.

These pending items do not justify inventing internals. Any hook-dependent integration remains fail-closed.

## Coverage

The canonical catalog before this phase is **35/100**. This revision represents component **36/100** once it is canonical on `main`. While it exists only on the branch/PR, `main` remains 35/100.

## Merge gates

Before merge:

1. fetch latest `main` again;
2. reconcile if it advanced;
3. review exact diff and review threads;
4. run Black Arcana CI on the final reconciled HEAD;
5. require GREEN on that exact HEAD;
6. fetch `main` immediately before merge;
7. merge with expected-head protection;
8. confirm final `main` SHA.

Phase 3 remains blocked.