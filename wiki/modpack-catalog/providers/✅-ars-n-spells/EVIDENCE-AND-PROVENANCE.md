# Evidence and Provenance — Ars 'n' Spells 3.3.4

## Physical pack authority

Current provider-specific authority: sibling `neoforge-rpg-skilltree@12a99071f241a3d61b4a48f5da15c67fd61c88b0`.

Certified physical row **#46**:

- `ars_n_spells-3.3.4.jar`
- mod id `ars_n_spells`
- display name `Ars 'n' Spells`
- runtime version `3.3.4`
- SHA-1 `53966330a468e626cd6469259af6778a5a7d9305`

Relevant current pack anchors:

- NeoForge `21.1.248`
- Ars Nouveau `5.13.1`
- Iron's Spells 'n Spellbooks `1.21.1-3.16.3`
- Ars Elemental `0.7.10.1`
- Ars Zero `2.0.2`

The physical modlist is authority for installed presence and version. It does not by itself expose Java registry internals.

## Exact 3.3.4 publisher release

Official CurseForge project: project `1447914`, license GPLv3, client & server.

Exact current file:

- file id `8881108`;
- `ars_n_spells-3.3.4.jar`;
- NeoForge / Minecraft `1.21.1`;
- uploaded `2026-09-14`;
- release type.

Published 3.3.4 delta:

- native cast payment ownership/final-cost lifecycle consolidation;
- measured debit/refund recovery and persistent unresolved obligations;
- restored optional Iron's payment/ticker mixin gates and bundled MixinExtras 0.5.3;
- Curios mirroring toggle and fresh-config/default alignment;
- carrier revisions expanded to every native item component;
- client/server protocol advanced to `7`;
- restored Blank Scroll drops in Iron's Catacombs armory and Citadel tomes;
- regression/config/resource/contract fixtures.

The publisher delta does not announce a new ritual or standalone spell registry identity. That is supporting continuity evidence, not exact 3.3.4 binary-registry proof.

## Official NeoForge 1.21.1 source evidence

Repository: `https://github.com/otectus/ars-n-spells`

Branch: `port/neoforge-1.21.1`

Exact 3.3.3 checkpoint: `41fac17065c381104b17fdaab307d89ba21b49ab`.

`gradle.properties` at that checkpoint declares Minecraft `1.21.1`, NeoForge `21.1.248`, `mod_id=ars_n_spells`, `mod_version=3.3.3`, Ars Nouveau `5.13.1.1400` and Iron's `1.21.1-3.16.3`.

Historical 3.3.0 baseline: `a9930223c96806e5d748ea69d02f9a32cab62de9`.

Two registration-critical files prove exact continuity from 3.3.0 through 3.3.3:

- `RitualRegistryHandler.java` -> Git blob `b25378e8a67ea084c77116bfe936f10512d3f691` at both checkpoints;
- `ArsCrossProxyRegistry.java` -> Git blob `f4e35f708aa41f7c4bf2599f2517429a4871f82b` at both checkpoints;
- `CrossModSpellComponents.PROXY_POOL_SIZE` remains exactly `8` in 3.3.3.

No exact public NeoForge 3.3.4 source checkpoint is promoted by this audit.

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

The exact 3.3.3 source proves five ritual registrations under the current pack condition (Iron's present) and eight proxy transport registry objects. The five ritual registrations are `spell_uninscription`, `mana_infusion`, `spell_transcription`, `mana_well` and `spellbook_binding`.

## Upstream test evidence

The official 3.3.0 NeoForge release commit reports upstream green checks including 920 unit tests / 68 suites and 86/86 GameTest scenarios in both absent/loaded dependency profiles, plus zero contract-parity drift.

This is provider-project evidence only. It is **not** Black Arcana full-modpack runtime QA and is not reported as a local PASS for the installed 3.3.4 JAR.

## Confidence labels

- Physical 3.3.4 presence/version/hash: **HIGH / current provider-specific physical dossier**.
- 3.3.4 publisher identity and declared delta: **HIGH / exact official release**.
- Five rituals and eight-proxy topology through NeoForge 3.3.3: **HIGH / exact official source**.
- Continuity of those identities into 3.3.4: **RELEASE-BOUNDED / not binary-proven**.
- Exact 3.3.4 classes, signatures, registry implementation, packet codecs and internal ordering: **NÃO VERIFICADO**.

## Clean-room rule

This catalog paraphrases publicly inspectable provider behavior for compatibility/deduplication analysis. Black Arcana must not copy Ars 'n' Spells source code, assets, text, models, sounds or implementation structures into its own runtime merely because the provider is GPLv3.

Any future code reuse would require an explicit licensing/provenance decision consistent with Black Arcana's own publication plan. Interoperability inspection does not automatically authorize implementation copying.

## Pending exact-runtime evidence

- exact installed 3.3.4 JAR binary extraction/registry comparison if a future adapter requires it;
- full physical-modpack runtime validation of the five ritual paths;
- full physical-modpack validation of payment/refund/cooldown exactly-once behavior;
- protocol-7 and carrier-revision behavior;
- Inscription Table / Spell Loom binding and repair;
- deployed server config reconciliation;
- any exact 3.3.4 internal hook Black Arcana may eventually want to consume.

Until those are available, exact-internal adapters remain fail-closed.