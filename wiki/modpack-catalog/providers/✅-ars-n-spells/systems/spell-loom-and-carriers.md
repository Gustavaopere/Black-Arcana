# Spell Loom and Carriers

## Evidence boundary

Physical provider: Ars 'n' Spells `3.3.2`.

Implementation details here are pinned to the official NeoForge 1.21.1 `3.3.0` source line at `a9930223c96806e5d748ea69d02f9a32cab62de9`. The exact 3.3.1/3.3.2 public deltas are HUD-only; exact 3.3.2 carrier bytecode parity is still `NÃO VERIFICADO`.

## Provider role

The Spell Loom/carrier subsystem is how Ars 'n' Spells turns an arbitrary Ars spell graph into provider-owned serialized carrier state that can cross into supported Iron's workflows.

The provider—not Black Arcana—owns:

- reading supported source spell data;
- deciding whether a target is blank/eligible;
- deciding whether a source is reusable or disposable;
- serializing the cross-spell payload;
- exporting Ars payloads onto supported carrier scrolls;
- allocating/removing native-wheel proxy slots when an Iron's spellbook is involved;
- preserving native/unrelated item state while cleaning ANS-owned state;
- validating provider-defined blacklists and malformed/stale payloads.

## 3.3.0 NeoForge hardening relevant to dedup

The source-release baseline records several correctness fixes:

- preview must not mutate the input;
- reusable books/foci used as sources are returned rather than consumed;
- a filled scroll is not treated as a blank target;
- transcription produces the intended output count and preserves the remainder of stacked blank targets;
- player-triggered cleanup removes all ANS-owned cross-cast state atomically while preserving genuine native spells/unrelated components;
- carrier-aware billing distinguishes reusable books from consumable scrolls.

These behaviors matter because a second serializer/settler in Black Arcana could reintroduce item loss, duplicate spell entries or double payment even if its UI looked equivalent.

## Black Arcana boundary

Black Arcana must not invent a parallel universal spellbook format over these same Ars↔Iron's carriers. It may have its own canonical loadout/casting representation for Black Arcana spells, but external Ars spell graphs stored by Ars 'n' Spells remain provider-owned.

If a future Black Arcana feature needs to reference a provider-bound Ars spell, the safe design is an opaque/provider-native identity or verified adapter—not copying the serialized implementation format into Black Arcana persistence.