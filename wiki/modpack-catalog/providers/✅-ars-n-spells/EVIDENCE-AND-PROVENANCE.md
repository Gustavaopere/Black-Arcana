# Evidence and Provenance — Ars 'n' Spells 3.3.4

## Physical pack authority

Current physical Project Library authority (`modlist(1).txt`, 2026-09-22 checkpoint):

- JAR `ars_n_spells-3.3.4.jar`;
- mod id `ars_n_spells`;
- display name `Ars 'n' Spells`;
- runtime `3.3.4`;
- SHA-1 `53966330a468e626cd6469259af6778a5a7d9305`.

Relevant physical companion engines:

- Ars Nouveau `5.13.1`;
- Iron's Spells 'n Spellbooks `1.21.1-3.16.3`;
- Ars Elemental `0.7.10.1`;
- Ars Zero `2.0.2`.

The physical modlist is authority for installed presence/version/hash. It does not by itself expose Java internals.

## Exact 3.3.4 release evidence

Official CurseForge project: project `1447914`, GPLv3, client & server.

Exact current file:

- file id `8881108`;
- `ars_n_spells-3.3.4.jar`;
- NeoForge / Minecraft 1.21.1;
- uploaded 2026-09-14;
- Release;
- publisher changelog version `[3.3.4] - 2026-09-14`.

Publisher-declared 3.3.4 changes relevant to Black Arcana boundaries:

- native cast payment ownership moved to the final host cast lifecycle;
- final cost listeners run once and the replaced native debit is suppressed;
- effects, channel cancellation, scroll consumption and native/category cooldowns share one lifecycle;
- measured debit/refund recovery and persistent unresolved obligations were added;
- Curios attribute mirroring toggle and cross-loader defaults/parity were updated;
- carrier revisions now cover every native item component;
- client/server protocol advances to **7**;
- selected blank-scroll loot was restored in Iron's structure loot tables;
- MixinExtras 0.5.3 and payment/ticker mixin gates were restored.

These release notes are authoritative for those declared changes. They do not expose exact 3.3.4 class signatures or prove registry byte parity.

## Historical exact release deltas retained

- 3.3.1 removes the transaction receipt HUD/panel;
- 3.3.2 fixes contextual Iron's mana-bar visibility and explicitly reports no config/network/save-format delta from 3.3.1;
- 3.3.3 moves the public NeoForge source line to the ornate Spell Loom/carrier revision architecture and protocol 6.

## Official NeoForge 1.21.1 source evidence

Repository: `otectus/ars-n-spells`.

Public branch: `port/neoforge-1.21.1`.

Latest public source checkpoint currently on that branch:

- commit `41fac17065c381104b17fdaab307d89ba21b49ab`;
- commit title `release: 3.3.3 - Spell Loom workstation, mana-bar visibility fix and receipt HUD removal`;
- `gradle.properties` declares `mod_version=3.3.3`, Minecraft `1.21.1`, NeoForge `21.1.248`, Ars Nouveau `5.13.1.1400` and Iron's `1.21.1-3.16.3`.

The earlier detailed semantic/source audit remains pinned to:

- commit `a9930223c96806e5d748ea69d02f9a32cab62de9`;
- declared `mod_version=3.3.0`.

That 3.3.0 pin remains the baseline for subdocuments that were inspected line-by-line there. Public 3.3.3 is used only for facts independently verified on that source line, including current source version, protocol 6, current Spell Loom/carrier architecture and continued proxy-pool size 8.

There is **no public NeoForge 3.3.4 source pin in the branch used here**. Exact 3.3.4 internals therefore remain release-bounded / fail-closed.

## Semantic registry boundary

The provider catalog retains **five ritual identities**:

1. `ars_n_spells:spell_uninscription`;
2. `ars_n_spells:spell_transcription`;
3. `ars_n_spells:spellbook_binding`;
4. `ars_n_spells:mana_infusion`;
5. `ars_n_spells:mana_well`.

The public source line also retains an eight-slot Iron's proxy pool, `ars_cross_1..8`. These are transport registry objects, not eight standalone semantic spells.

Current semantic disposition:

- provider ritual identities: **5**;
- proxy registry objects: **8 infrastructure objects**;
- standalone semantic spell contribution from proxies: **0**;
- semantic delta from the previously cataloged 3.3.2 line: **+0**.

Because 3.3.4 changes payment/carrier internals without publishing a source pin, this semantic continuity is `RELEASE_BOUNDED`, not a claim of exact binary registry equivalence.

## Confidence labels

- physical presence/version/hash: **HIGH / exact physical row**;
- 3.3.4 publisher delta: **HIGH / exact official release page**;
- public 3.3.3 source facts: **HIGH / official source pin**;
- detailed 3.3.0 implementation facts retained in legacy subcatalogs: **HIGH for that pin**;
- five-ritual / eight-proxy continuity into 3.3.4: **RELEASE-BOUNDED / not binary-proven**;
- exact 3.3.4 classes, signatures, packet codecs, mixin targets and ordering: **UNVERIFIED unless exposed by release evidence**.

## Clean-room rule

This catalog records only factual provider behavior and interoperability boundaries. It does not authorize copying Ars 'n' Spells source, assets, text or implementation into Black Arcana.

## Pending exact-runtime evidence

- physical 3.3.4 JAR structural extraction / registry comparison if an exact hook is ever required;
- assembled-pack validation of provider payment ownership and cross-cast settlement;
- Spell Loom/carrier revision compatibility against the physical pack;
- protocol 7 client/server behavior;
- restored blank-scroll loot in the assembled datapack stack;
- any exact 3.3.4 internal hook Black Arcana may eventually consume.

Until those are closed, provider-specific exact-internal adapters remain fail-closed.