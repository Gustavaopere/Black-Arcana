# Current Magic Catalog Coverage

## Operational percentage

**Coverage represented by this Phase 2AM revision: 41/100 = 41%.**

Phase 2AM was branched from canonical `main@433233164f61bbf6b6d5cb8aa9625cf286a79a23`, where Phase 2AL / PR #145 made component #40 canonical and coverage reached **40/100 = 40%**. Component #41 becomes canonical only when this revision is reconciled with the latest main, passes CI on that exact reconciled HEAD and is merged. While this revision exists only on the Phase 2AM branch/PR, canonical coverage remains **40/100 = 40%**.

This metric is intentionally conservative. It measures **current magic/cross-domain provider components closed to the strongest evidence presently available**, not a guessed percentage of every individual spell object. A provider with a partial current inventory or unresolved current-version delta contributes zero closed component points.

## Physical anchor

- Minecraft: 1.21.1
- NeoForge: 21.1.248
- latest physical modlist: **595 top-level entries**
- modlist SHA-1: `7aaece7acbfb07ba4d0c66029042f36c50d046f0`
- jarjar/internal dependencies are not counted as top-level providers

The historical 2026-09-07 queue used **612 top-level entries / 103 candidate components**. It is preserved as history and is not the current denominator.

## Current working denominator

The current operational denominator remains **100 magic/cross-domain component units** after direct ID reconciliation of the historical 103-candidate set against the physical modlist:

- **98** of the former 103 candidate mod IDs still survive the current physical modlist;
- the **5 actually absent** former candidates are `ars_morph`, `morerelics`, `reliquary`, `vestis` and `woodwalkers_spellbooks`;
- **2** current magic/cross-domain candidates not represented by the old 103-unit baseline remain under classification: `soul_fire_d` and `reliquified_lenders_cataclysm_new_relics_fix`;
- therefore `103 - 5 + 2 = 100` current operational units.

Correction from the earlier Phase 2AF reconciliation text: `backportedspellbooks`, `crystal_chronicles` and `gtbcs_geomancy_plus` are physically present in the same 595-entry / SHA-1 `7aaece...` modlist and must not be listed as removed.

This denominator is operational, not immutable. Reconcile it whenever the physical provider set changes.

## Closed component count

Phase 2AF / PR #135 is canonical and closed `not_enough_glyphs` as component **35**.

Phase 2AG / PR #137 is canonical and closed `ars_n_spells` as component **36** at the available evidence ceiling:

- exact physical/release identity: Ars 'n' Spells `3.3.2`;
- official NeoForge 1.21.1 source baseline: `3.3.0` at `a9930223c96806e5d748ea69d02f9a32cab62de9`;
- 5 ritual identities under the physical pack condition where Iron's is present;
- 5 provider-owned mana-unification modes;
- Spell Loom/carrier lifecycle;
- cross-cast settlement and finite 8-slot native-wheel proxy pool;
- 8 `ars_cross_*` proxy registry objects explicitly excluded from standalone semantic-spell inflation;
- exact 3.3.2 internal signatures remain unverified/fail-closed rather than guessed.

Phase 2AH / PR #140 is canonical and closed `monstersspellbooks` as component **37**:

- exact physical identity: `monstersspellbooks-0.0.16.3.jar`, SHA-1 `b3aa89fd081bf4bfaf8d0f4380bcdc393c66ab0e`;
- exact CurseForge release: project/file `1428928 / 8788560`, 2026-09-01;
- complete current public-source inventory: **98 explicit `registerSpell(...)` registrations**;
- source-family distribution: blood 5, ender 12, evocation 3, fire 10, holy 4, hydro 8, ice 8, lightning 14, nature 7, necro 25, technomancy 2;
- two SchoolType registrations are observed in the inspected source head (`necro`, `aero`), but source metadata is not an exact 0.0.16.3 build pin;
- Aero contributes zero spell registrations; exact 0.0.16.2 soft-deletes Aero and exact 0.0.16.3 deletes remaining Aero content, so installed `monstersspellbooks:aero` existence is **`NÃO VERIFICADO`**;
- public source head `1ab9b72af2ea44c3c8b816e665d06531ea44ddc2` is contemporaneous with the release but still carries stale `mod_version=0.0.14` metadata;
- `ModSpellRegistry` is unchanged across the public source interval containing the 0.0.16.2/0.0.16.3 work;
- exact 0.0.16.3 binary numerical/API/config/network/save internals and uncertain school parity remain unverified/fail-closed.

The point is awarded for closing the **provider component at its evidence ceiling**, not for pretending the installed JAR was decompiled or that stale source metadata is an exact binary pin.

## Phase 2AI — Somake audit, zero delta

Phase 2AI / PR #141 is canonical on `main@9e2011a46e228fb8e2dd7c9d275c6f43290f6bb8` and re-audits `somakespells-1.0.8-1.21.1-fix.jar` from the already-merged Phase 2O provider tree.

Evidence is strong for exact physical/release identity and public feature/release-line behavior, including:

- exact File ID `8417850` and physical SHA-1 `b0ad94c1504709662bee2d08700375ccecbb5ec7`;
- exact 1.0.8-fix Symmetry/Spirit Elemental Charge correction;
- official 1.0.x changelog names and migrations;
- provider-owned Aqua/Symmetry/charge/progression/ritual/equipment capability families.

However, the publisher states `over 50 spells` while the public changelog exposes only a subset, and no exact-current publisher source/registry/API or equivalent complete 1.0.8-fix inventory is available through the inspected evidence. Therefore Somake remains **partial** and receives **0** new component points.

## Phase 2AJ — Ace's Spell Utils component #38, canonical

Phase 2AJ / PR #143 is canonical at merge SHA `83a5cbf95e2e2eeb8c4e5e161aa2eb590b78712b` and closed `aces_spell_utils` at the exact source-version evidence ceiling:

- physical artifact `aces_spell_utils-1.2.7.2-1.21.1.jar`, SHA-1 `8cbcd535a0b19bef49504c0b5ecafcbcd1cb1cca`;
- exact publisher release project/file `1299492 / 8789930`, 2026-09-02;
- exact official source-version pin `AceTheEldritchKing/Aces_Spell_Utils@a0b2f4c2fcfa938c8e47239279c77c2ef82647ac`, whose metadata declares `mod_version=1.2.7.2-1.21.1`;
- **0 standalone provider spell registrations** — no `registerSpell(...)` call / no provider spell-registry registration surface in the exact source;
- 3 Iron's SchoolTypes (`ritual`, `hydro`, `technomancy`);
- 19 attributes, including 13 shared runtime attributes and 6 school power/resistance attributes;
- 3 school damage-type keys;
- 1 serialized copy-on-death attachment;
- 1 custom particle type;
- 14 tag contracts;
- 8 rarity enum extensions;
- 27 unconditional `example_*` item registrations classified as example/support registry objects, not standalone spells;
- 8 optional protocol `4.0.0` S2C visual payloads;
- 2 required mixins and 5 common config values;
- reusable entity/boss/item/summon/domain/VFX API plus provider-owned event runtime for attribute/proc helpers.

Source targets NeoForge 21.1.230 / Iron's 3.11.0 while the pack uses NeoForge 21.1.248 / Iron's 3.16.3. That remains a runtime integration QA boundary, not a reason to invent or withhold semantic registry identities. Source↔physical-JAR byte equality is not asserted.

The point is awarded because this component is an **API/library provider whose complete own registry/runtime surface is closed**, including the exact result that its standalone spell inventory is zero. Consumer-addon spells remain under those addons' namespaces and authority.

## Phase 2AK — EMF Compat: Iron's Spells component #39, canonical

Phase 2AK / PR #144 is canonical at merge SHA `73a425051d242a33af157a3f73ca816498e8eba8` and closed `emf_compat_iron_spells` as a client presentation compatibility component:

- physical artifact `emf_compat_iron_spells_1.21.1_2.0.0.jar`, SHA-1 `515b545870fce128bbf01a0ccacdd19566ed3b22`;
- exact official source revision `victorkozhokin/emf-compat@79d730a9d02275b7d721967c75f5f22dc815d9dc`;
- exact subproject metadata `mod_version=2.0.0`, Java 21, `GNU GPL 3.0`;
- **0 standalone spells and 0 provider gameplay registry surface**;
- complete addon package surface: 5 Java classes;
- exactly 3 required client mixins: `PlayerModelMixin`, `PlayerRendererMixin`, `EMFAnimationPauseHandlerMixin`;
- 2 provider config booleans;
- `iron_spells` pose source priority 10;
- first-person EMF vanilla-model condition while local-player casting under Iron's first-person arm/item settings;
- client-only hard dependency ranges: Core >=2.0.0, Iron's >=3.15.0, EMF >=3.3.2;
- physical pack uses Core 2.0.0, Iron's 3.16.3 and EMF 3.3.5.

The component owns visual pose compatibility only. Iron's remains cast/resource/cooldown authority, and Black Arcana must not interpret these client hooks as cast authority or duplicate the Iron's-specific EMF pose adapter.

Byte-for-byte source/JAR equivalence and full-pack rendering QA remain separate; they do not reopen the semantic inventory closure.

## Phase 2AL — `efiscompat` component #40, canonical

Phase 2AL / PR #145 is canonical at merge SHA `433233164f61bbf6b6d5cb8aa9625cf286a79a23` and closed `efiscompat` at the exact source-version evidence ceiling as an Epic Fight↔Iron's casting-interaction and animation compatibility component:

- physical artifact `efiscompat-3.1.0.jar`, SHA-1 `4250e1c65732d70d1091cc50b84a91b6ed5b2b3f`;
- exact CurseForge project/file `1109064 / 8372294`, release 2026-07-05;
- exact official source pin `domanhthang2110/efiscompat@b4b58aff86e707420fac8a7c29fe647d7f5aaac4` on the dedicated `1.21.1` branch;
- the pinned commit is itself the 3.1.0 `Fixed dedicated server crash` commit and changes source `mod_version` from 3.0.0 to 3.1.0;
- **0 standalone provider spells** and no provider-owned mana/resource system;
- 28 Java source files;
- 35 provider Epic Fight animation accessors;
- 12 required mixins: 6 client + 6 common;
- 6 common config keys;
- data-driven `spell_animations` reload with 9 chant/cast/continuous + staff-side roles and default fallback;
- real server-side casting interaction: Iron's pre-cast veto from Epic Fight state plus Iron's cast cancellation on skill/guard/dodge paths;
- exact runtime metadata requires BOTH-side Epic Fight `[21,)` and Iron's `[1.21.1-3.15.0,)`;
- physical pack uses Epic Fight 21.17.3.1 and Iron's 3.16.3.

One common mixin targets `com.p1nero.invincible.skill.ComboBasicAttack`; exact target ownership/presence is not proven from the top-level physical inventory and remains runtime QA/fail-closed.

License metadata is also intentionally unresolved: CurseForge labels MIT while exact source metadata declares `GNU GPLv3`, with no root `LICENSE` file observed at the pin. Source inspection is read-only and no code/assets are copied.

The provider owns reconciliation around Iron's casts, not a second spell runtime. Black Arcana therefore must not duplicate Iron's↔Epic Fight interruption/animation handling or route BA-native spells through Iron's just to inherit this compatibility.

## Phase 2AM — Apothic Attributes component #41 candidate

Phase 2AM closes `apothic_attributes` at the exact source-version evidence ceiling as a combat/attribute/effect support provider:

- physical artifact `ApothicAttributes-1.21.1-2.10.1.jar`, SHA-1 `6a6b84d09801621df5cc2c8a68f35bd93a6cda0f`;
- exact official source pin `Shadows-of-Fire/Apothic-Attributes@686361b2c7b0e76bf4158890bb8a2e42ef805622`;
- exact source metadata declares version 2.10.1, Minecraft 1.21.1, Java 21, NeoForge baseline 21.1.235 and Placebo 9.9.0, with Curios optional;
- **0 standalone spell/glyph/ritual registrations observed** in the exact source tree;
- 2 synchronized custom registries, 22 attributes, 7 effects, 31 potions, 37 brewing mixes and 5 damage types;
- 2 data components, 3 attachments, 7 built-in equipment-slot objects, 11 slot groups, 3 provider tag contracts, 1 particle and 1 sound;
- 2 clientbound PLAY payloads, 7 common + 1 client mixin;
- provider-owned combat formula/proc runtime and server-side `AbilityCooldowns` API;
- conditional Curios attribute/modifier bridge under the physical pack's Curios 9.5.1 path;
- exact `DetonationEffect` discrepancy is preserved literally: its damage call uses `DamageTypes.BLEEDING` despite a separately registered/tagged `DETONATION` damage type.

Apothic owns its generic combat math, cooldown subsystem and modifier bridge. Black Arcana retains canonical cast/cost/target/effect/cooldown authority, Corruption, Strain, Arcane Danger, Backlash no-proc semantics and WorldEffectPolicy. `apothic_attributes:cooldown_reduction` does not automatically become a BA cooldown modifier, and BA must not route Backlash into Apothic offensive proc chains.

Source↔physical-JAR byte reproducibility and full-modpack combat-provider interaction remain QA/fail-closed rather than guessed. Root source code is MIT, assets are All Rights Reserved, and `StackAttributeModifiersEvent.java` carries a file-level Forge Development LLC / SPDX LGPL-2.1-only header; this catalog performs read-only inspection only.

## Partial providers still receive zero points

Examples include:

- `leylines` — public signature names known, total current inventory not verified;
- `somakespells` — exact physical/release surface is audited, but current granular spell inventory is not closed;
- `cataclysm_spellbooks` — installed 1.1.13 remains ahead of the exact public source inventory already audited;
- `gaze` — public surface audited, exact current registry/source-JAR closure still pending.

## Update rule

After each provider closure:

1. re-read the physical modlist and current `main`;
2. reconcile concurrent PR ownership;
3. close the provider to the strongest exact evidence available;
4. preserve explicit evidence layers when release/source/JAR versions differ;
5. merge only after latest-main reconciliation and CI GREEN on the reconciled HEAD;
6. increment the numerator only once the closure revision is canonical on `main`;
7. change the denominator whenever physical reconciliation changes the provider set.

Phase 3 remains blocked until the provider catalog/deduplication pass establishes real Black Arcana gaps.