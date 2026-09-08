# Phase 2P — Ars Nouveau 5.13.1 checkpoint

## Base and concurrency

The long-running Ars Nouveau branch was reconciled with `main@65e3a24d566cb0e424262168c8572ee4d70a4fff` before this closure pass. The semantic merge is `65e58363efe84e75cf55a7eb0d18a5536c5cb132` and preserves the Stage 06 final-validation handoff already integrated in main.

Phase labels were reconciled against newer parallel catalog work before naming this checkpoint: Phase 2M is Cataclysm: Spellbooks, Phase 2N is Leyline Spellbooks and Phase 2O is Somake Spells. The historical branch name still contains `phase2m`; this checkpoint is canonically **Phase 2P** and does not rewrite earlier history.

## Exact current provider

- provider: Ars Nouveau;
- mod id: `ars_nouveau`;
- JAR: `ars_nouveau-1.21.1-5.13.1.jar`;
- runtime version: `5.13.1`;
- exact source pin: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`.

The exact source `license.txt` places code under **GNU LGPL v3** and states that assets including textures/models are **All Rights Reserved** unless otherwise stated or permission is granted. Source inspection in this checkpoint is read-only factual cataloging; no upstream code/assets are copied or adapted into Black Arcana.

## Source-catalog scope closed

- core spell grammar primitives: **85/85** = **5 Forms + 67 Effects + 13 Augments**;
- individual acquisition for those 85 spell parts: **85/85**, with provider-generated recipe, source-default recipe XP and starter/learning boundary tied to the same 5.13.1 pin;
- Rituals: **24/24** source classes/pages;
- Familiars: **6/6** source-cataloged mechanics/pages;
- Perks/Threads: **20/20** source registry/pages;
- armor perk-slot providers: **12/12** source-pinned provider entries across Tier I/II/III layouts;
- provider-wide systems inventory: spell composition/execution, glyph learning, player mana/equipment economy, Source and perk-slot providers.

The catalog preserves the provider split between **player mana** and **Source**; one is not silently converted into the other. Glyph learning, spell context/child resolvers, provider costs, ritual execution, familiar ownership and Thread/perk semantics remain Ars authority.

## Key authority and deduplication findings

1. Ars spell chains remain one provider-owned causal cast. `Linger`, `Wall`, `Orbit`, `Reset`, delayed continuations and similar child contexts do not create new Black Arcana casts, costs, cooldowns or mastery events merely because provider execution fans out.
2. Ars-owned world mutation is observed, not replayed. Independent Black Arcana destructive effects still require `WorldEffectPolicy`.
3. `Randomize` means generic randomness is already occupied; a future Chaos identity must prove materially distinct entropy/instability semantics.
4. Rune/Wall/Snare/Gravity/Reset and other control/constraint primitives mean future Order content must prove authoritative-law/seal mechanics rather than generic geometry or immobilization.
5. Blink/Exchange/Rewind occupy substantial space/time capability territory; future Black Arcana time/space work must deduplicate against them.
6. Sense Magic, Heal, Hex/Wither, Ignite/Flare and multiple summon/world-control primitives create direct overlap pressure on Divination, healing/divine, curse/death, infernal and summoning concepts.
7. Ars addons remain separate providers. Core closure does not promote Ars Elemental, Ars Zero, Ars Controle, Ars Technica or any other addon to audited-complete status.

## Explicitly not closed

- effective runtime/config values in the full pack;
- claim/protected-area behavior where the exact Effect execution path does not prove an equivalent provider guard;
- client rendering, accessibility and VFX interactions;
- event ordering with other perk/damage/loot/potion systems;
- optional-addon activation and inter-provider behavior;
- any future supported API seam used by a Black Arcana runtime adapter must still be verified against the exact integration target;
- dedicated-server/full **612-entry** modpack runtime QA.

## Runtime status

This checkpoint is documentation/provenance/authority/deduplication work. It does **not** promote Black Arcana runtime Stages, does not implement an Ars adapter and is not evidence that runtime/config/client QA passed.
