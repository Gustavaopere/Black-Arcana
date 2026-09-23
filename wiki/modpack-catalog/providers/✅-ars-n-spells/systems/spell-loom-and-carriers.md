# Spell Loom and Carriers

## Evidence boundary

Physical provider: Ars 'n' Spells `3.3.4`.

Historical implementation details below remain pinned to the official NeoForge 1.21.1 `3.3.0` source line at `a9930223c96806e5d748ea69d02f9a32cab62de9`. Public NeoForge source reaches exact 3.3.3 at `41fac17065c381104b17fdaab307d89ba21b49ab`, while exact 3.3.4 publisher evidence covers the current carrier-revision/protocol delta. Exact 3.3.4 carrier bytecode parity remains `NÃO VERIFICADO`.

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

## Current 3.3.3 / 3.3.4 carrier delta

Exact 3.3.3 source/release evidence adds the provider Blank Scroll, direct binding through Iron's Inscription Table, Spell Loom redesign and carrier validation/repair hardening. Exact 3.3.4 publisher evidence expands carrier revisions to every native item component, advances client/server protocol to 7 and restores Blank Scroll drops in Iron's Catacombs armory/Citadel tomes.

These changes remain provider-owned. They do not authorize Black Arcana to serialize, revise, repair or settle Ars 'n' Spells carriers independently.

## Black Arcana boundary

Black Arcana must not invent a parallel universal spellbook format over these same Ars↔Iron's carriers. It may have its own canonical loadout/casting representation for Black Arcana spells, but external Ars spell graphs stored by Ars 'n' Spells remain provider-owned.

If a future Black Arcana feature needs to reference a provider-bound Ars spell, the safe design is an opaque/provider-native identity or verified adapter—not copying the serialized implementation format into Black Arcana persistence.