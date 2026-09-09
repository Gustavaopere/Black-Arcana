# Current Magic Catalog Coverage

## Operational percentage

**Coverage represented by this Phase 2AR revision: 46/100 = 46%.**

The latest canonical `main` before this branch is `67966f99e07890741773f44e920ded20d2bd5666`, where canonical coverage remains **45/100 = 45%**. Phase 2AR represents candidate component #46 and becomes canonical only after latest-main reconciliation, CI GREEN on the reconciled HEAD, merge, and post-merge `main` confirmation.

Phase 2AQ / PR #152 is canonical at merge SHA `bdf5271c265b5f40ee5a9e7695c7d71374a4c31c` and made component #45 canonical. Phase 2AP / PR #151 remains component #44 at merge SHA `70a97ec0cf58cecebe4054f43ea5b212e757e365`. The Phase 2AP metadata correction in PR #153 has **zero coverage delta**.

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
- **2** current magic/cross-domain candidates not represented by the old 103-unit baseline are `soul_fire_d` and `reliquified_lenders_cataclysm_new_relics_fix`;
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

## Phase 2AM — Reliquified L_Ender's Cataclysm New Relics Fix component #41, canonical

Phase 2AM / PR #147 is canonical at merge SHA `192f5d3c109189a9fee5fb3fc247bfbd75a93b68` and closed `reliquified_lenders_cataclysm_new_relics_fix` at the exact physical/publisher evidence ceiling as a bounded Relics 0.10→0.12 compatibility bridge:

- physical artifact `reliquified-lenders-cataclysm-new-relics-fix-1.0.2.jar`, SHA-1 `9d4710e665ec74af917bb9f5f819154ca9f74ca0`;
- exact CurseForge project/file `1665965 / 8778365`, release 2026-08-31;
- publisher environment Client & Server and license All Rights Reserved;
- original target addon explicitly `Reliquified L_Ender's Cataclysm 0.1.1`;
- physical stack includes Relics 0.12.8, Curios 9.5.1, OctoLib 0.6.2, Cataclysm 3.33 and the target addon 0.1.1;
- exactly five existing addon relics are named in the fix scope: Void Cloak, Scouring Eye, Void Vortex in Bottle, Vacuum Glove and Void Bubble;
- eight public repair families cover removed `IRelicItem`, RelicTemplate conversion, Curios/modifiers, progression/cooldowns/XP, active abilities, player-motion networking, order/values and descriptions/tooltips;
- exact 1.0.2 changelog narrows the bridge to the addon's base class and prevents global `RelicItem` modifications;
- **0 new semantic relic identities** and **0 standalone spell identities** are published as fix-owned content.

No exact public source for fix 1.0.2 was located. Exact mixin classes/counts/targets, transform signatures, packet schema and persistence keys remain fail-closed and are not invented. The original addon's current public `1.21.1` branch already declares `mod_version=0.2`, so it is not substituted for the physical target addon `0.1.1` or for missing fix source.

This point is awarded for closing the **compatibility component's identity/authority/deduplication surface at the publisher evidence ceiling**, not for claiming source-internal implementation closure.

## Phase 2AN — Apothic Attributes component #42, canonical

Phase 2AN / PR #149 is canonical at merge SHA `994d2983f0ec54fd54455a14abad473ebaea86bc` and closed `apothic_attributes` at the exact source-version evidence ceiling as a combat/attribute/effect support provider:

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

## Phase 2AO — Soul Fire'd component #43, canonical

Phase 2AO / PR #150 is canonical at merge SHA `068ca67e786d95255ccecb70433dd66d26a4b3e4` and closed `soul_fire_d` 6.1.0 at the exact physical/publisher/source evidence ceiling as a Prometheus-backed Soul Fire content provider:

- physical artifact `soul-fire-d-neoforge-1.21-6.1.0.jar`, SHA-1 `877002a5aa386f9011ebc4eb3360a7647ac359d9`;
- exact CurseForge project/file `662413 / 7364962`, release 2025-12-22 for NeoForge 1.21/1.21.1;
- exact official source branch `Crystal-Nest/soul-fire-d:1.21@0cc7a03b950e74742eb75f51642cc7a0190c7127` declares version 6.1.0, Java 21, Cobweb 1.4.0 and Prometheus 1.2.5;
- physical pack matches Cobweb 1.4.0 and Prometheus 1.2.5 exactly;
- since 6.0.0 the generic Fire API moved to Prometheus; exact physical Prometheus 1.2.5 source pin `Crystal-Nest/prometheus:1.21@3edbe979b3a383b526f38daeba4eb35d18283a9d` confirms the consumed framework boundary;
- **0 standalone spells, 0 glyphs, 0 rituals and 0 provider mana/cast resource**;
- both exact common and NeoForge mixin manifests contain zero mixins;
- one Soul Fire definition supplied through Prometheus: `minecraft:soul`, light 10, damage value 2, vanilla Soul Fire flame particle;
- one associated `minecraft:soul_fire_charge` resource/item/recipe family, with exact recipe output 16;
- two exact enchantments: `minecraft:soul_fire_aspect` and `minecraft:soul_flame`, both delegating ignition to `prometheus:ignite` with fire type `soul`;
- one provider-owned NeoForge GLM serializer, `soul_fire_d:chest_loot_modifier`;
- one bundled Bastion modifier with independent 5% level-1 enchanted-book additions for each enchantment.

Prometheus owns the generic fire framework/API; Soul Fire'd owns Soul-specific definitions/content/enchantments/acquisition. Black Arcana retains its canonical magic/hazard/world-safety runtime and must not treat provider fire/enchantment causality as a second cast pipeline or bypass `WorldEffectPolicy`.

License metadata is intentionally unresolved for reuse: exact source metadata/root text are GPL-3.0-or-later/GPLv3, while publisher surfaces label the distributed project Custom License / Crystal Nest Community License v1. Source inspection is read-only and no code/assets are copied.

The point is awarded because the exact 6.1.0 component identity, content surface, authority migration and deduplication boundary are closed without claiming source/JAR byte reproducibility or full-pack runtime interoperability.

## Phase 2AP — Create Enchantment Industry Plus component #44, canonical

Phase 2AP / PR #151 is canonical at merge SHA `70a97ec0cf58cecebe4054f43ea5b212e757e365` and closed `create_enchantment_industry_plus` 1.1.1 at the exact physical/source evidence ceiling as a small Create / Create: Enchantment Industry recipe-and-content extension:

- physical artifact `create_enchantment_industry_plus-1.1.1-1.21.1.jar`, SHA-1 `c7e87eb00e10cb347f6372e17d38da51ce6f1975`;
- exact official source pin `TiesToetToet/create_enchantment_industry_plus@fb97ed35288f7ff2c80d43ef33f051db93d281d5`, whose metadata declares version 1.1.1 for Minecraft 1.21.1;
- **0 standalone spells, 0 glyphs, 0 rituals and 0 provider mana/cast resource**;
- exactly 2 addon Java files and **1 registered addon item**, `create_enchantment_industry_plus:sac`;
- exactly **6 addon recipe JSONs**: two filling, one grinding, two mixing and one pressing route;
- exactly **1 host-recipe disable overlay** under `create_enchantment_industry:recipes/mixing/ink` using `neoforge:never`;
- no mixin configuration, provider packet or persistence surface observed in the exact source tree;
- addon-keyed metadata declares NeoForge `[21.1.0,)`, Minecraft `[1.21.1,1.22)` and Create: Enchantment Industry `[2.0.0,)`; the source also contains Create range `[6.0.4,6.1.0)` under the mis-keyed table `[[dependencies.create_enchantment_industry]]`, so physical-JAR parity and loader interpretation of that Create block remain fail-closed;
- four recipe routes directly reference `create_dragons_plus:black_dye` or `create_dragons_plus:grinding`, but Create: Dragons Plus is not declared in metadata; the current physical pack contains Create: Dragons Plus 1.11.8b, so this is recorded as an undeclared data-level dependency rather than hidden or replaced;
- publisher-facing documentation describes an Ink Sac drain/recovery route, but the exact 1.1.1 source tree contains no `emptying`/drain recipe. That path remains fail-closed until its physical provider/recipe identity is proven.

Create owns machine/process execution, Create: Enchantment Industry owns its experience/enchantment-processing domain, Create: Dragons Plus owns the black-dye fluid and grinding type referenced by the data, and CEI Plus owns only its item/recipe overlays. Black Arcana retains its canonical magic runtime and must not duplicate processing/resource settlement or count these recipes as spells.

License metadata remains a reuse-review boundary: exact source metadata and Modrinth indicate MIT, CurseForge labels LGPLv3, and the repository `LICENSE.txt` is Forge-origin LGPL boilerplate. Source/data inspection is read-only and no code/assets are copied.

The point was awarded because the exact 1.1.1 semantic component was closed without pretending source/JAR byte reproducibility or full-pack recipe interoperability had been proven.

## Phase 2AQ — Apothic Compat component #45, canonical

Phase 2AQ / PR #152 is canonical at merge SHA `bdf5271c265b5f40ee5a9e7695c7d71374a4c31c` and closed `apothic_compat` 2.0.2 at the exact physical/publisher/tagged-source evidence ceiling as an Apotheosis loot-category data-map and affix-blacklist compatibility provider:

- physical artifact `apothic_compat-2.0.2.jar`, SHA-1 `868506b8367be2c155acde0ef186b5a3e6ba8db9`;
- exact CurseForge project/file `1516278 / 8219980`, NeoForge 1.21.1 release dated 2026-06-09;
- exact official GitHub release tag `v2.0.2-neoforge-1.21.1`, with published asset SHA-256 `eaee4ee2be65b95fe10ee749dc2d023b90fb63338825f5ba0b697124f42295de`;
- exact tagged source revision `Nightwielder23/apothic-category-compat@cebf69a37f8c6573fc0c0295e627f4636e7bd026`, whose metadata declares `mod_version=2.0.2`, Minecraft 1.21.1 and NeoForge baseline 21.1.230;
- runtime metadata requires Apotheosis `[8.5,9)`; physical Apotheosis 8.8.0 satisfies that declared range;
- **0 standalone spells, 0 glyphs, 0 rituals and 0 provider mana/cast resource**;
- **0 mixins**, **4 Java classes**, one provider data-map resource and no provider packet/persistence surface observed;
- exactly **13 loot-category data-map overrides**, all mapping explicit third-party item IDs to `apotheosis:bow`;
- one config key, `affix_blacklist`, stored in `apothic_compat-common.toml`;
- exact command identities `/apothiccompat reload` and `/ac reload`, permission level 2;
- three NeoForge lifecycle/event hooks: command registration, server-start blacklist application and full datapack-sync blacklist reapplication;
- affix-blacklist runtime rebuilds the host affix-by-type selection pool while leaving the backing affix registry intact, and catches private-reflection failure rather than propagating it.

Apotheosis owns loot-category semantics/data-map interpretation, affix identities/registry/pools, rolling and synchronization. Apothic Compat owns only its contributed mappings, blacklist policy/reapplication and command UX. Black Arcana retains all canonical spell/cast/hazard/world-safety authority and must not use this provider's reflection into private `AffixRegistry.byType` as a BA extension seam.

The exact source also exposes a static QA edge case: after a non-empty blacklist has filtered the host pool, changing the blacklist to empty and running only `/ac reload` returns before reconstructing the already-filtered `byType` map. A normal Apotheosis pool rebuild lifecycle is distinct. Live removal semantics therefore remain runtime-QA pending.

Exact command names from the tagged 2.0.2 source supersede later/editorial renamed forms such as `/apothiccategorycompat` or `/acc`. Continued-port target registry parity and physical Apotheosis 8.8.0 private-field compatibility likewise remain fail-closed until runtime verification.

The point was awarded after exact-head CI GREEN and merge. Source/release-asset/physical-JAR byte reproducibility is not asserted without a direct byte comparison.

## Phase 2AR — Backported Spellbooks component #46, candidate

Phase 2AR closes `backportedspellbooks` at a layered physical/publisher/release-day-source evidence ceiling while preserving the version discrepancy instead of normalizing it:

- physical artifact `backportedspellbooks-0.1.2.jar`, SHA-1 `747847c1f38c73250ebac05ea06b41a381187850`, is present in the current 595-entry modlist;
- physical runtime metadata reports mod ID `backportedspellbooks`, version `0.1.0`;
- exact publisher release is CurseForge project/file `1543731 / 8158731`, released 2026-05-28 for NeoForge Minecraft 1.21.1, filename `backportedspellbooks-0.1.2.jar`;
- official release-day source pin is `RedReaper28/BackportedSpellbooks-1.21.1@07cb65efca0c264762a21c2d6bce0f83e3947226`;
- that source still declares `mod_version=0.1.0`, matching the physical runtime metadata while differing from the public file/release label;
- release-day `ModSpellRegistry` closes exactly **6 provider spells**: `slime_aspect`, `sulfur_bomb`, `sulfur_clouds`, `sulfur_release`, `pale_thorn`, `resin_spray`;
- the exact 0.1.2 publisher changelog names the first four as the release delta; Pale Thorn and Resin Spray predate it;
- one Pale Flora school/sub-school surface is registered;
- supporting source inventory includes 19 item registry objects including block-items, 4 blocks, 5 entity types, 4 effects, 2 particle types, 1 fluid + 1 fluid type and 19 recipe JSONs;
- two exact NeoForge biome modifiers place Corroded Fossil and Quicksilver ore features in `minecraft:sulfur_caves` at `underground_ores`;
- server-side equipment hooks cover Miasma Staff and Garden Rapier post-damage procs plus Slime Boots fall cancellation;
- no provider custom payload registration, provider SavedData/attachment/data-component persistence subsystem or mixin configuration was observed in the inspected release-day source tree; these remain source observations, not physical-bytecode claims.

Iron's owns host casting/mana/cooldown/container semantics. Backported Spellbooks owns its six spell identities, Pale Flora content, effects/entities/equipment/worldgen and provider procs. Vanilla Backport and Ace's retain authority over the consumed surfaces they provide. Black Arcana does not clone these spells, duplicate the equipment proc/fall pipeline, introduce a second mana/cooldown settlement path or reinterpret provider worldgen as BA `WorldEffectPolicy` authority.

Static/runtime QA remains explicit: physical SHA-1 is known but source↔JAR byte equivalence is not proven; source targets NeoForge 21.1.216 / Iron's 3.15.4 while the pack uses NeoForge 21.1.248 / Iron's 3.16.3; source imports Iron's, Vanilla Backport and Ace's although the inspected generated metadata template formally lists only NeoForge/Minecraft; Slime Boots exposes cooldown presentation/constants while the inspected fall hook does not show a cooldown gate; full-pack event ordering, network sync, provider config values, duplicate-proc behavior and dedicated-server operation remain unverified.

License evidence is also intentionally unresolved for reuse: CurseForge labels MIT while release-day source metadata declares All Rights Reserved. Inspection is factual/read-only and no third-party code/assets are copied.

The represented numerator is 46 only for this Phase 2AR revision. Component #46 becomes canonical only after latest-main reconciliation, CI GREEN, merge and post-merge `main` confirmation.

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