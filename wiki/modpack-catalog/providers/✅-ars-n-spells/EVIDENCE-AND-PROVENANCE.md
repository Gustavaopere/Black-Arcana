# Evidence and Provenance — Ars 'n' Spells 3.3.2

## Physical pack authority

Source of presence/version: latest physical `/mnt/data/modlist.txt` used by the Black Arcana project checkpoint.

Verified physical row:

- `ars_n_spells-3.3.2.jar`
- mod id `ars_n_spells`
- display name `Ars 'n' Spells`
- runtime version `3.3.2`
- SHA-1 `2d2274ff786c42ea46c53fec866116f83d98fe5a`

Relevant current pack anchors:

- NeoForge `21.1.248`
- Ars Nouveau `5.13.1`
- Iron's Spells 'n Spellbooks `1.21.1-3.16.3`
- Ars Elemental `0.7.10.1`
- Ars Zero `2.0.2`

The physical modlist is authority for installed presence and version. It does not by itself expose Java registry internals.

## Exact 3.3.2 release evidence

Official CurseForge project: project `1447914`, license GPLv3, client & server.

Exact current file:

- file id `8832580`
- `ars_n_spells-3.3.2.jar`
- NeoForge / Minecraft 1.21.1
- uploaded 2026-09-07
- release page: `https://www.curseforge.com/minecraft/mc-mods/ars-n-spells/files/8832580`

Published 3.3.2 delta:

- fixes contextual Iron's mana-bar visibility when displayed mana is full but maximum values are fractional;
- restores XP-bar visibility at the XP anchor when the contextual mana bar hides;
- aligns Forge/NeoForge mana-visibility rules/regressions;
- explicitly states no config, network-protocol or save-format changes from 3.3.1.

Exact 3.3.1 NeoForge file:

- file id `8827129`
- release page: `https://www.curseforge.com/minecraft/mc-mods/ars-n-spells/files/8827129`
- published delta: removal of the transaction receipt HUD/panel.

These releases are authoritative for those declared deltas. They are not a substitute for exact 3.3.2 binary registry inspection.

## Official NeoForge 1.21.1 source baseline

Repository: `https://github.com/otectus/ars-n-spells`

Branch: `port/neoforge-1.21.1`

Pinned commit: `a9930223c96806e5d748ea69d02f9a32cab62de9`

Commit title identifies it as the 3.3.0 release/parity checkpoint for the NeoForge 1.21.1 line.

`gradle.properties` at that pin declares:

- Minecraft `1.21.1`;
- NeoForge `21.1.248`;
- Java 21 compile/run toolchain;
- `mod_id=ars_n_spells`;
- `mod_version=3.3.0`;
- Ars Nouveau `5.13.1.1400`, runtime range `[5.13,6.0)`;
- Iron's `1.21.1-3.16.3`, runtime range `[1.21.1-3.16.3,1.21.1-4.0.0)`;
- optional Ars Elemental `0.7.10.1` test profile;
- optional Ars Zero `2.0.2` test profile.

This is strong same-loader/game source evidence, but it is still **3.3.0**, not 3.3.2.

## Source surfaces audited

At the pinned NeoForge baseline the Phase 2AG pass inspected the provider's public source surfaces for:

- ritual registration and tablet splice;
- Spell Uninscription;
- Spell Transcription;
- Spellbook Binding;
- Mana Infusion;
- Mana Well;
- shared one-shot ritual lifecycle;
- mana-unification enum;
- cross-mod data components;
- finite `ars_cross_*` Iron's proxy registry.

The baseline proves five ritual registrations under the current pack condition (Iron's present) and eight proxy transport registry objects.

## Upstream test evidence

The official 3.3.0 NeoForge release commit reports upstream green checks including 920 unit tests / 68 suites and 86/86 GameTest scenarios in both absent/loaded dependency profiles, plus zero contract-parity drift.

This is provider-project evidence only. It is **not** Black Arcana full-modpack runtime QA and is not reported as a local PASS for the installed 3.3.2 JAR.

## Confidence labels

- Physical presence/version/hash: **HIGH / exact physical artifact row**.
- 3.3.1/3.3.2 published deltas: **HIGH / exact official release pages**.
- NeoForge 1.21.1 3.3.0 source semantics: **HIGH / official source pin**.
- Continuity of five ritual identities and eight proxies into 3.3.2: **MEDIUM-HIGH at semantic release-line level**, because later published deltas are HUD-only; **NOT binary-proven**.
- Exact 3.3.2 classes, signatures, registry implementation, packet codecs and internal ordering: **NÃO VERIFICADO** unless independently exposed by exact release evidence.

## Clean-room rule

This catalog paraphrases publicly inspectable provider behavior for compatibility/deduplication analysis. Black Arcana must not copy Ars 'n' Spells source code, assets, text, models, sounds or implementation structures into its own runtime merely because the provider is GPLv3.

Any future code reuse would require an explicit licensing/provenance decision consistent with Black Arcana's own publication plan. Interoperability inspection does not automatically authorize implementation copying.

## Pending exact-runtime evidence

- exact installed 3.3.2 JAR binary extraction/registry comparison;
- full physical-modpack runtime validation of the five ritual paths;
- full physical-modpack runtime validation of cross-casting/proxy settlement;
- any exact 3.3.2 internal hook Black Arcana may eventually want to consume.

Until those are available, exact-internal adapters remain fail-closed.