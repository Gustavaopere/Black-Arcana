# Spell Transcription

Registry identity at the official NeoForge 1.21.1 source baseline: `ars_n_spells:spell_transcription`.

## Evidence status

- Physical provider: Ars 'n' Spells `3.3.2`.
- Implementation evidence: official NeoForge `3.3.0` source pin `a9930223c96806e5d748ea69d02f9a32cab62de9`.
- Exact 3.3.2 binary registry parity: `NÃO VERIFICADO`.

This ritual is registered by the 3.3.0 NeoForge baseline only when `irons_spellbooks` is loaded. Iron's is physically present in the current pack.

## Semantics

The ritual transcribes one supported spell-bearing source onto one supported blank carrier target through the provider's cross-cast serialization path.

The audited NeoForge baseline performs validation before mutation and distinguishes:

- existing ANS-inscribed items;
- exactly one source;
- exactly one blank target;
- targets already carrying a rooted Ars spell;
- provider-defined inscription-plan rejection;
- source parse failure;
- Ars payloads containing provider-blacklisted/caster-bound glyphs.

The 3.3.0 NeoForge hardening also prevents a dropped stack of blank targets from being duplicated into a fully inscribed stack: the provider plan authorizes the output count and preserves the remainder. Reusable books/foci can be read without being consumed when the provider plan marks them reusable; disposable sources are consumed only by the authorized amount.

Baseline search radius: **3 blocks** around the brazier.

This is a one-shot `AnsRitual` at the source baseline, using the default **60 server-tick** completion lifecycle.

## Deduplication boundary

Black Arcana must not serialize arbitrary Ars spell graphs into foreign carriers itself, guess whether a source is disposable, bypass the provider blacklist, or mutate carrier state before provider validation completes.

A transcribed payload remains Ars 'n' Spells/host-owned data. Black Arcana may observe an approved provider outcome through a real adapter, but must not become a second inscription authority.