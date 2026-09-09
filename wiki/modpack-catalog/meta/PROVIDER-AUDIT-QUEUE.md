# Fila operacional de auditoria dos providers mágicos

## Autoridade atual

Este arquivo é a fila operacional corrente. O snapshot detalhado de 2026-09-07 permanece preservado em [`PROVIDER-AUDIT-QUEUE-2026-09-07.md`](./PROVIDER-AUDIT-QUEUE-2026-09-07.md).

Autoridade física deste checkpoint:

- Minecraft 1.21.1;
- NeoForge `21.1.248`;
- modlist física mais recente: **595 entradas top-level**;
- SHA-1 da modlist: `7aaece7acbfb07ba4d0c66029042f36c50d046f0`;
- dependências internas/jarjar não contam como providers top-level.

O snapshot histórico de 2026-09-07 usava 612 entradas / 103 candidatos e não é mais autoridade de presença, versão nem denominador.

## Cobertura global

Ver [`CATALOG-COVERAGE-CURRENT.md`](./CATALOG-COVERAGE-CURRENT.md).

- Phase 2AQ / PR #152 está canônica em `main@bdf5271c265b5f40ee5a9e7695c7d71374a4c31c`;
- cobertura canônica atual: **45/100 = 45%**;
- Phase 2AP / PR #151 permanece componente #44 canônico em `main@70a97ec0cf58cecebe4054f43ea5b212e757e365`;
- PR #153 corrige somente a evidência de metadata da Phase 2AP e possui **zero delta de cobertura**;
- provider parcial não recebe ponto inteiro.

### Reconciliação física corrigida do denominador

A lista histórica possui 103 IDs. A comparação direta desses IDs contra a modlist física atual encontra:

- 98 IDs históricos ainda presentes;
- 5 ausentes reais: `ars_morph`, `morerelics`, `reliquary`, `vestis`, `woodwalkers_spellbooks`;
- 2 candidatos magic/cross-domain atuais adicionados depois da lista histórica: `soul_fire_d`, `reliquified_lenders_cataclysm_new_relics_fix`;
- denominador operacional: `103 - 5 + 2 = 100`.

Correção: `backportedspellbooks`, `crystal_chronicles` e `gtbcs_geomancy_plus` estão fisicamente presentes e não devem aparecer como removidos.

## Phase 2AQ — Apothic Compat 2.0.2 — canonical

| Mod ID | Artefato físico | Estado da auditoria |
|---|---|---|
| `apothic_compat` | `apothic_compat-2.0.2.jar` | CANÔNICO VIA PR #152 / EXACT PHYSICAL+PUBLISHER+TAGGED OFFICIAL SOURCE VERSION / APOTHEOSIS LOOT-CATEGORY DATA-MAP + AFFIX-BLACKLIST COMPAT / 0 SPELLS+GLYPHS+RITUALS / 0 MIXINS / 4 JAVA CLASSES / 13 BOW CATEGORY OVERRIDES / 1 CONFIG KEY / 2 COMMAND ROOTS+ALIASES / 3 EVENT HOOKS / COMPONENT #45 / PRIVATE-REFLECTION+BYTE+FULL-PACK QA FAIL-CLOSED |

### Evidence boundary

- Physical SHA-1: `868506b8367be2c155acde0ef186b5a3e6ba8db9`.
- CurseForge project/file: `1516278 / 8219980`, exact NeoForge 1.21.1 release dated 2026-06-09.
- Exact official GitHub release tag: `v2.0.2-neoforge-1.21.1`; published release asset `apothic_compat-2.0.2.jar` has SHA-256 `eaee4ee2be65b95fe10ee749dc2d023b90fb63338825f5ba0b697124f42295de`.
- Exact tagged source revision: `Nightwielder23/apothic-category-compat@cebf69a37f8c6573fc0c0295e627f4636e7bd026`.
- Exact metadata declares `mod_version=2.0.2`, Minecraft 1.21.1, NeoForge baseline 21.1.230, Apotheosis baseline 8.5.4 and runtime Apotheosis range `[8.5,9)`.
- Physical pack uses Apotheosis `8.8.0`, Placebo `9.9.2` and Apothic Attributes `2.10.1`; the declared Apotheosis range is satisfied, but private-reflection parity is not inferred from semver.
- Exact source tree exposes 4 Java classes, 0 mixins, 0 standalone spells, 0 glyphs, 0 rituals, 0 provider mana/cast resource and no provider packet/persistence surface observed.
- Exact `data/apotheosis/data_maps/item/loot_category_overrides.json` contains 13 explicit item mappings, all to `apotheosis:bow`.
- Exact config has one semantic key, `affix_blacklist`, in `apothic_compat-common.toml`.
- Exact commands are `/apothiccompat reload` and `/ac reload`, permission level 2. Later/editorial `/apothiccategorycompat` or `/acc` naming is not projected onto installed 2.0.2.
- Exact runtime hooks are command registration, `ServerStartedEvent` blacklist application and full `OnDatapackSyncEvent` blacklist reapplication.
- `AffixBlacklist` filters the host affix-by-type pool by reflectively writing private `AffixRegistry.byType`; reflection failure is caught/logged and is not a supported Black Arcana integration seam.
- Static QA edge: changing an already-applied non-empty blacklist to empty and running only `/ac reload` returns before reconstructing the filtered host pool. A host pool rebuild lifecycle is distinct; live unblacklist semantics remain runtime-QA pending.
- Continued-port item registry parity and data-map priority across the physical pack remain fail-closed until runtime verification.
- Root tagged source and exact NeoForge metadata are MIT. Inspection is factual/read-only; no code/assets are copied.
- Exact tagged source/release asset are not promoted to byte-for-byte physical-JAR identity without direct reproducibility comparison.
- Final PR-head CI #2228 (`34358226123`) passed on `7c69cee76d3bb866e4cdd3ff8a2748bef43df639`.
- Exact post-merge `main@bdf5271c265b5f40ee5a9e7695c7d71374a4c31c` CI #2230 (`34358659906`) passed the full pipeline.

### Provider authority

- Apotheosis owns loot-category semantics/data-map interpretation, affix identities/registry/pools, affix rolling and synchronization.
- Apothic Compat owns only its 13 contributed data-map values, affix-blacklist policy/reapplication and command UX.
- Black Arcana retains canonical casting, transactional costs, BA cooldowns/charges, targeting, hazards, Corruption, Strain, Arcane Danger, Backlash causality and `WorldEffectPolicy`.
- `apotheosis:bow`, the blacklist and provider affix pool are not Black Arcana spell-domain/cast/proc authority.
- BA must not duplicate the same category mappings or copy the provider's private reflection seam as a generic proc-suppression mechanism.
- RPG Skill Tree receives no affix/category or magic runtime authority.

## Phase 2AP — Create Enchantment Industry Plus 1.1.1 — canonical predecessor

| Mod ID | Artefato físico | Estado da auditoria |
|---|---|---|
| `create_enchantment_industry_plus` | `create_enchantment_industry_plus-1.1.1-1.21.1.jar` | CANÔNICO VIA PR #151 / EXACT PHYSICAL+OFFICIAL SOURCE VERSION / CREATE+CEI RECIPE EXTENSION / 0 SPELLS+GLYPHS+RITUALS / 1 ITEM / 6 ADDON RECIPES + 1 HOST-RECIPE DISABLE / CREATE METADATA TABLE MIS-KEYED / UNDECLARED CREATE DRAGONS PLUS DATA DEPENDENCY / COMPONENT #44 / LICENSE-METADATA + BYTE+FULL-PACK QA FAIL-CLOSED |

### Evidence boundary

- Physical SHA-1: `c7e87eb00e10cb347f6372e17d38da51ce6f1975`.
- Exact official source: `TiesToetToet/create_enchantment_industry_plus@fb97ed35288f7ff2c80d43ef33f051db93d281d5`.
- Exact source metadata declares version `1.1.1`, Minecraft 1.21.1 and NeoForge baseline 21.1.159.
- Exact source package contains 2 addon Java files and exactly one registered addon item: `create_enchantment_industry_plus:sac`.
- Exact source data contains 6 addon recipe JSONs: 2 filling, 1 grinding, 2 mixing and 1 pressing route.
- Exact source also overlays `create_enchantment_industry:recipes/mixing/ink` with `neoforge:never`, disabling that host recipe rather than adding a seventh processing route.
- Exact source tree exposes 0 standalone spells, 0 glyphs, 0 rituals, 0 provider mana/cast resource, 0 mixin configs and no provider network/persistence surface observed.
- Addon-keyed metadata declares NeoForge `[21.1.0,)`, Minecraft `[1.21.1,1.22)` and Create: Enchantment Industry `[2.0.0,)`.
- The source also contains Create range `[6.0.4,6.1.0)` under mis-keyed table `[[dependencies.create_enchantment_industry]]`, not `[[dependencies.create_enchantment_industry_plus]]`; physical Create `6.0.10` satisfies the numeric range, while physical-JAR metadata parity and loader interpretation remain **NÃO VERIFICADO**.
- Four exact recipe routes reference `create_dragons_plus:black_dye` or `create_dragons_plus:grinding`, but Create: Dragons Plus is not declared in metadata. The current pack contains Create: Dragons Plus `1.11.8b`; this is recorded as an undeclared data-level dependency, not converted into a fabricated formal dependency.
- Publisher-facing documentation describes an Ink Sac drain/recovery path, but the exact 1.1.1 source tree contains no `emptying`/drain recipe. That route remains fail-closed until physical provider/recipe identity is proven.
- Exact source metadata and Modrinth indicate MIT, CurseForge labels LGPLv3 and repository `LICENSE.txt` is Forge-origin LGPL boilerplate. Reuse remains review-required; inspection is factual/read-only.
- Exact source-version pin is not promoted to byte-for-byte source/JAR identity without reproducibility evidence.

### Provider authority

- Create owns machine/process execution and Create recipe semantics.
- Create: Enchantment Industry owns its experience/enchantment-processing domain.
- Create: Dragons Plus owns the `black_dye` fluid and `grinding` recipe type referenced by CEI Plus data.
- Create Enchantment Industry Plus owns only its `sac` item and recipe/data overlays.
- Black Arcana retains canonical casting, costs, BA cooldowns/charges, targeting, hazards, Corruption, Strain, Arcane Danger, Backlash causality and `WorldEffectPolicy`.
- Recipe objects are not spells and do not create a second Black Arcana magic pipeline.
- RPG Skill Tree receives no processing or magic runtime authority.

## Phase 2AO — Soul Fire'd 6.1.0 — canonical predecessor

| Mod ID | Artefato físico | Estado da auditoria |
|---|---|---|
| `soul_fire_d` | `soul-fire-d-neoforge-1.21-6.1.0.jar` | CANÔNICO VIA PR #150 / EXACT PHYSICAL+PUBLISHER+OFFICIAL SOURCE VERSION / PROMETHEUS-BACKED SOUL-FIRE CONTENT PROVIDER / 0 SPELLS+GLYPHS+RITUALS / 0 MIXINS / 1 SOUL FIRE TYPE + 1 ASSOCIATED FIRE CHARGE / 2 ENCHANTMENTS / STATIC DATAPACK / 1 NEOFORGE GLM SERIALIZER + BASTION ACQUISITION / COMPONENT #43 / LICENSE-METADATA CONFLICT + BYTE+FULL-PACK QA FAIL-CLOSED |

### Evidence boundary

- Physical SHA-1: `877002a5aa386f9011ebc4eb3360a7647ac359d9`.
- CurseForge project/file: `662413 / 7364962`, exact NeoForge 1.21/1.21.1 release dated 2025-12-22.
- Official exact source branch: `Crystal-Nest/soul-fire-d:1.21@0cc7a03b950e74742eb75f51642cc7a0190c7127`.
- Exact source metadata: version 6.1.0, Java 21, NeoForge baseline 21.0.143/range `[21.0,)`, Cobweb 1.4.0, Prometheus 1.2.5.
- Physical pack uses Cobweb 1.4.0 and Prometheus 1.2.5 exactly and NeoForge 21.1.248 satisfies the loader range.
- Since Soul Fire'd 6.0.0 the generic fire API moved to Prometheus. Exact physical Prometheus 1.2.5 source is pinned at `Crystal-Nest/prometheus:1.21@3edbe979b3a383b526f38daeba4eb35d18283a9d` only to establish the consumed provider boundary.
- Exact Prometheus defines Soul Fire type `minecraft:soul`; Soul Fire'd supplies its definition through Prometheus with light 10, damage value 2 and the vanilla Soul Fire flame particle.
- Soul Fire'd requests associated fire-charge registration through Prometheus; exact resources/recipe identify `minecraft:soul_fire_charge`, recipe output 16.
- Exact `CommonModLoader` registers only the fire definition plus Cobweb static enchantment datapack at top position; NeoForge loader additionally registers the loot serializer.
- Exact common and NeoForge mixin manifests both contain empty common/client/server arrays: active mixin count **0**.
- Static datapack contains exactly `minecraft:soul_fire_aspect` and `minecraft:soul_flame`, both using `prometheus:ignite` with fire type `soul`.
- NeoForge registers one global-loot-modifier serializer: `soul_fire_d:chest_loot_modifier`.
- Bundled Bastion modifier independently rolls 5% for a level-1 Soul Fire Aspect book and 5% for a level-1 Soul Flame book in `minecraft:chests/bastion_other`.
- Exact source tree exposes no standalone spell/glyph/ritual or provider mana/cast-resource surface.
- Exact source/root metadata is GPL-3.0-or-later/GPLv3 while publisher surfaces label the release Custom License / Crystal Nest Community License v1. Reuse/derivation remains blocked pending independent reconciliation.
- Exact source-version pin is not promoted to byte-for-byte source/JAR identity without reproducibility evidence.

### Provider authority

- Prometheus 1.2.5 owns the generic Fire API/runtime/component registration framework.
- Soul Fire'd 6.1.0 owns Soul-specific definition/content, two enchantments, static data and loot acquisition.
- Cobweb owns the static/dynamic registration support it provides.
- Black Arcana retains canonical casting, costs, BA cooldowns/charges, targeting, hazards, Corruption, Strain, Arcane Danger, Backlash causality and `WorldEffectPolicy`.
- A provider Soul Fire type never authorizes bypassing BA world-effect policy or treating generic fire/enchantment callbacks as a second BA cast pipeline.
- RPG Skill Tree receives no fire or magic runtime authority.

## Phase 2AN — Apothic Attributes 2.10.1 — canonical predecessor

| Mod ID | Artefato físico | Estado da auditoria |
|---|---|---|
| `apothic_attributes` | `ApothicAttributes-1.21.1-2.10.1.jar` | CANÔNICO VIA PR #149 / EXACT PHYSICAL VERSION + EXACT OFFICIAL SOURCE VERSION PIN / COMBAT+ATTRIBUTE+EFFECT SUPPORT PROVIDER / 0 STANDALONE SPELLS+GLYPHS+RITUALS OBSERVED / 22 ATTRIBUTES / 7 EFFECTS / 31 POTIONS / 37 BREWING MIXES / 5 DAMAGE TYPES / COMPONENT+ATTACHMENT+SLOT REGISTRIES / 2 CLIENTBOUND PAYLOADS / 8 MIXINS / SERVER ABILITY COOLDOWNS / CONDITIONAL CURIOS BRIDGE / COMPONENT #42 / BYTE+FULL-PACK QA FAIL-CLOSED |

### Evidence boundary

- Physical SHA-1: `6a6b84d09801621df5cc2c8a68f35bd93a6cda0f`.
- Official exact-version source: `Shadows-of-Fire/Apothic-Attributes@686361b2c7b0e76bf4158890bb8a2e42ef805622`.
- Source metadata declares exactly version `2.10.1`, Minecraft 1.21.1, Java 21, NeoForge baseline 21.1.235 and Placebo 9.9.0; Curios is optional.
- Physical pack uses NeoForge 21.1.248, Placebo 9.9.2 and Curios 9.5.1+1.21.1.
- Exact source tree exposes no standalone spell/glyph/ritual registration surface; path-level recheck found no `spell`, `glyph` or `ritual` paths.
- Closed central content surface: 2 synchronized custom registries, 22 attributes, 7 effects, 31 potions, 37 generated brewing mixes, 5 damage types, 2 data components, 3 attachments, 7 equipment-slot objects, 11 slot groups, 3 provider tag contracts, 1 particle and 1 sound.
- Networking surface observed: exactly 2 clientbound PLAY payloads; no provider C2S cast-intent path was found.
- Runtime surface includes 7 common + 1 client mixin, combat/attribute handlers and the public server-side `AbilityCooldowns` subsystem.
- Curios compat is conditional and bridges modifier-source/stack-attribute composition; Curios remains slot/inventory authority.
- Exact source discrepancy retained: `DetonationEffect` consumes fire ticks but its damage call uses `ALObjects.DamageTypes.BLEEDING` even though `DETONATION` is separately registered/tagged.
- `current_hp_damage` is tagged physical and cannot critically strike; `detonation`, `fire_damage` and `cold_damage` enter the NeoForge magic tag; bleeding/detonation/fire/cold bypass armor.
- Root upstream source code license is MIT, assets are All Rights Reserved; `StackAttributeModifiersEvent.java` has a file-level Forge Development LLC / SPDX LGPL-2.1-only header.
- Exact source-version pin is not promoted to byte-for-byte source/JAR identity without reproducibility evidence.

### Provider authority

- Apothic Attributes owns its armor/protection replacement formulas, penetration/shred, crit, auxiliary damage, dodge, life steal/overheal, projectile modifiers, healing/XP/mining modifiers, potion/effect behavior and `AbilityCooldowns` runtime.
- Curios owns Curios inventory and slot state; Apothic only owns its conditional modifier bridge.
- Black Arcana retains canonical casting, transactional costs, BA cooldowns/charges, targeting, Corruption, Strain, Arcane Danger, Backlash and WorldEffectPolicy.
- `apothic_attributes:cooldown_reduction` does not automatically apply to Black Arcana cooldowns.
- BA Backlash must not be deliberately routed through Apothic crit/life-steal/auxiliary-damage proc chains.
- RPG Skill Tree remains progression/Mastery/perk authority only through real contracts.

## Phase 2AM — Reliquified L_Ender's Cataclysm New Relics Fix 1.0.2 — canonical predecessor

| Mod ID | Artefato físico | Estado da auditoria |
|---|---|---|
| `reliquified_lenders_cataclysm_new_relics_fix` | `reliquified-lenders-cataclysm-new-relics-fix-1.0.2.jar` | CANÔNICO VIA PR #147 / EXACT PHYSICAL+PUBLISHER 1.0.2 / RELICS 0.10→0.12 COMPATIBILITY BRIDGE / 5 EXISTING RELICS IN PUBLISHED SCOPE / 8 PUBLISHED REPAIR FAMILIES / 0 NEW SEMANTIC RELIC IDS / 0 PUBLISHED STANDALONE SPELL IDS / 1.0.2 BASE-CLASS-ONLY TRANSFORM SCOPE / COMPONENT #41 / EXACT SOURCE+MIXIN+PACKET+PERSISTENCE INTERNALS FAIL-CLOSED |

### Evidence boundary

- Physical SHA-1: `9d4710e665ec74af917bbf5f819154ca9f74ca0`.
- CurseForge project/file: `1665965 / 8778365`, exact 1.0.2 release dated 2026-08-31.
- Publisher: NeoForge 1.21.1, Client & Server, All Rights Reserved.
- Publisher defines the component as a bridge allowing Reliquified L_Ender's Cataclysm `0.1.1` to work with newer Relics `0.12` after old Relics `0.10` classes/methods changed or disappeared.
- Exact physical required stack includes Relics `0.12.8`, Curios `9.5.1+1.21.1`, OctoLib `0.6.2`, L_Ender's Cataclysm `3.33` and Reliquified L_Ender's Cataclysm `0.1.1`.
- Publisher names exactly five fixed existing relics: Void Cloak, Scouring Eye, Void Vortex in Bottle, Vacuum Glove and Void Bubble.
- Publisher lists repair of `IRelicItem` startup/API breakage, RelicTemplate conversion, Curios/modifiers, stats/levels/ranks/cooldowns/XP, legacy active abilities, player-motion networking, ability order/progression values and descriptions/tooltips.
- Exact file 1.0.2 changelog narrows the bridge to the addon's base class and prevents global `RelicItem` modification.
- No exact public source for the fix was located; exact mixin classes/counts/targets, bytecode transforms, packet schema and persistence keys remain fail-closed.
- Original addon's current public `1.21.1` branch declares `mod_version=0.2`, so it is not substituted for the physical target addon `0.1.1` or for missing fix source.

### Provider authority

- Relics owns current framework/rank/level/XP/cooldown infrastructure.
- Reliquified L_Ender's Cataclysm owns the five relic identities and content behavior.
- Curios owns equip-slot infrastructure.
- this fix owns only old-addon→new-Relics compatibility translation.
- Black Arcana does not duplicate template/modifier/progression/cooldown/ability/network adaptation and retains its own canonical magic runtime.
- RPG Skill Tree receives no relic or magic runtime authority from this compatibility component.

## Phase 2AL — `efiscompat` 3.1.0 — canonical predecessor

| Mod ID | Artefato físico | Estado da auditoria |
|---|---|---|
| `efiscompat` | `efiscompat-3.1.0.jar` | CANÔNICO VIA PR #145 / EXACT PHYSICAL VERSION + EXACT OFFICIAL SOURCE VERSION PIN / EPIC FIGHT↔IRON'S CASTING-INTERACTION+ANIMATION COMPAT / 0 SPELLS / 28 JAVA FILES / 35 ANIMATION ACCESSORS / 12 REQUIRED MIXINS (6 CLIENT + 6 COMMON) / 6 CONFIG KEYS / DATA-DRIVEN SPELL-ANIMATION MAP / IRON'S PRECAST+CANCEL RECONCILIATION / COMPONENT #40 / LICENSE-CONFLICT + BYTE/HOST/FULL-PACK QA FAIL-CLOSED |

### Evidence boundary

- Physical SHA-1: `4250e1c65732d70d1091cc50b84a91b6ed5b2b3f`.
- CurseForge project/file: `1109064 / 8372294`, release `3.1.0` dated 2026-07-05.
- Official exact-version source: `domanhthang2110/efiscompat@b4b58aff86e707420fac8a7c29fe647d7f5aaac4` on branch `1.21.1`.
- The pinned commit is titled `Fixed dedicated server crash` and changes `mod_version=3.0.0` to `3.1.0`.
- Exact source metadata: Minecraft 1.21.1, Java 21, NeoForge baseline 21.1.219, Iron's baseline 3.15.6.
- Generated runtime metadata requires BOTH-side Epic Fight `[21,)` and Iron's `[1.21.1-3.15.0,)`.
- Physical pack uses Epic Fight `21.17.3.1` and Iron's `1.21.1-3.16.3`; declared ranges are satisfied, but exact mixin/API/event-order parity remains runtime QA.
- Standalone provider spell count is **0**; Iron's `SpellRegistry` is queried only to resolve host spells for animation selection.
- Exact source surface contains 28 Java files, 35 provider animation accessors, 12 required mixins and 6 common config keys.
- `SpellAnimationLoader` provides a reloadable 9-role chant/cast/continuous + staff-side mapping with default fallback.
- Server-relevant compatibility includes an Iron's pre-cast veto from Epic Fight stun/recent-action state and cancellation of active Iron's casts from Epic Fight skill/guard/dodge paths.
- `MixinComboBasicAttack` targets `com.p1nero.invincible.skill.ComboBasicAttack`; physical target owner/presence is not established from the top-level modlist and remains fail-closed QA.
- License metadata conflict is preserved: CurseForge labels MIT, exact source metadata declares `GNU GPLv3`, and no root `LICENSE` file was observed at the source pin.
- Exact source-version pin is not promoted to byte-for-byte source/JAR identity without reproducibility evidence.

### Provider authority

- Iron's owns spells, cast state, mana, spell effects and cooldown semantics.
- Epic Fight owns combat action/stun/skill/animation state.
- `efiscompat` owns only the reconciliation policy and animation compatibility around those providers.
- Black Arcana must not duplicate the same Iron's↔Epic Fight interruption/animation layer or route BA-native spells through Iron's to inherit it.
- Black Arcana retains canonical casting/cost/target/effect/cooldown, Corruption, Strain, Arcane Danger, ritual/hazard and `WorldEffectPolicy` authority.
- RPG Skill Tree receives no magic runtime authority from this compat.

## Phase 2AK — EMF Compat: Iron's Spells 2.0.0 — canonical predecessor

| Mod ID | Artefato físico | Estado da auditoria |
|---|---|---|
| `emf_compat_iron_spells` | `emf_compat_iron_spells_1.21.1_2.0.0.jar` | CANÔNICO VIA PR #144 / EXACT PHYSICAL VERSION + EXACT OFFICIAL SOURCE VERSION / CLIENT PRESENTATION COMPAT / 0 SPELLS / 0 GAMEPLAY REGISTRY / 5 JAVA CLASSES / 3 REQUIRED CLIENT MIXINS / 2 CONFIG KEYS / POSE SOURCE PRIORITY 10 / FIRST-PERSON EMF CONDITION / COMPONENT #39 / BYTE-EQUIVALENCE + FULL-PACK RENDER QA FAIL-CLOSED |

### Evidence boundary

- Physical SHA-1: `515b545870fce128bbf01a0ccacdd19566ed3b22`.
- Official source revision: `victorkozhokin/emf-compat@79d730a9d02275b7d721967c75f5f22dc815d9dc`.
- Exact NeoForge 1.21.1 subproject metadata declares `mod_version=2.0.0`, Java 21 and `mod_license=GNU GPL 3.0`.
- Complete addon Java surface: `EMFCompatIronSpellsMod`, `IronSpellsCompat`, `PlayerModelMixin`, `PlayerRendererMixin`, `EMFAnimationPauseHandlerMixin`.
- Required mixin manifest contains exactly the three client mixins above and no common/server mixins.
- Config keys: `ironspells.enabled` and `ironspells.bodyFollowArms`, both default true.
- Casting state is consumed from Iron's client data only; the compat does not originate or authorize a cast.
- Source build baseline: NeoForge 21.1.230, Iron's 3.15.6, EMF 3.3.2.
- Runtime metadata requires Core >=2.0.0, Iron's >=3.15.0 and EMF >=3.3.2, client-side. Physical pack uses Core 2.0.0, Iron's 3.16.3 and EMF 3.3.5.
- Some public web file indices remain stale at 1.0.0; physical artifact + exact publisher source metadata are used as stronger version evidence.
- Exact source version is not promoted to byte-for-byte source/JAR identity without reproducibility evidence.

### Provider authority

- Iron's owns casting state, spells, mana, cooldowns and remote synced cast state.
- EMF Compat: Iron's owns only the client pose compatibility adapter.
- EMF Compat Core / EMF own their shared presentation APIs/runtime.
- Black Arcana must not treat EMF pose state or client casting state as server authority and must not duplicate this Iron's-specific pose adapter.
- RPG Skill Tree receives no progression authority from this visual layer.

## Phase 2AJ — Ace's Spell Utils 1.2.7.2 — canonical predecessor

| Mod ID | Artefato físico | Estado da auditoria |
|---|---|---|
| `aces_spell_utils` | `aces_spell_utils-1.2.7.2-1.21.1.jar` | CANÔNICO VIA PR #143 / EXACT PHYSICAL VERSION + EXACT OFFICIAL SOURCE VERSION PIN / API+LIBRARY PROVIDER / 0 STANDALONE SPELL REGISTRATIONS / 3 SCHOOLS / 19 ATTRIBUTES / 3 DAMAGE TYPES / 14 TAGS / 8 RARITIES / 27 EXAMPLE ITEM REGISTRATIONS / 8 S2C VFX PAYLOADS / 2 REQUIRED MIXINS / 5 CONFIG VALUES / COMPONENT #38 / HOST-VERSION+BYTE-EQUIVALENCE QA FAIL-CLOSED |

### Evidence boundary

- Physical SHA-1: `8cbcd535a0b19bef49504c0b5ecafcbcd1cb1cca`.
- CurseForge project/file: `1299492 / 8789930`, exact 1.2.7.2 release dated 2026-09-02.
- Official exact-version source: `AceTheEldritchKing/Aces_Spell_Utils@a0b2f4c2fcfa938c8e47239279c77c2ef82647ac`.
- Source `gradle.properties` declares exactly `mod_version=1.2.7.2-1.21.1`.
- No `registerSpell(...)` call and no provider standalone spell-registry registration surface were found: exact provider spell count is **0**.
- School registry IDs are `aces_spell_utils:ritual`, `aces_spell_utils:hydro`, `aces_spell_utils:technomancy`.
- Publisher display language may call Ritual `Occult`; exact registry remains `ritual`.
- Source Java supplier `ABYSSAL` actually registers `hydro`; do not fabricate an Abyssal school.
- Source targets NeoForge 21.1.230 / Iron's 3.11.0 while pack uses NeoForge 21.1.248 / Iron's 3.16.3. Exact host-runtime parity remains QA/fail-closed.
- Exact source-version pin is not promoted to byte-for-byte source/JAR identity without reproducibility evidence.

### Provider authority

- Iron's owns underlying spell casting, mana and cooldown authority.
- Ace's owns shared attributes/proc helpers, API classes, mixins, attachment, VFX transport and example runtime it registers.
- consuming addons own concrete spells/entities/items built on the Ace's API.
- Black Arcana does not duplicate these pipelines and retains its own canonical casting, Corruption, Strain, Arcane Danger and WorldEffectPolicy.
- RPG Skill Tree remains progression/mastery only through real contracts.

## Phase 2AI — canonical predecessor, zero delta

| Mod ID | Artefato físico | Estado |
|---|---|---|
| `somakespells` | `somakespells-1.0.8-1.21.1-fix.jar` | CANÔNICO VIA PR #141 / EXACT PHYSICAL+RELEASE IDENTITY / OFFICIAL 1.0.x RELEASE SURFACE AUDITED / PUBLISHER `OVER 50` SCALE / COMPLETE CURRENT SPELL REGISTRY NOT AVAILABLE / EXACT SOURCE+API NOT LOCATED / AQUA↔T.O RUNTIME QA BLOCKED / ZERO COVERAGE DELTA / FAIL-CLOSED |

## Phase 2AH — canonical predecessor

| Mod ID | Artefato físico | Estado |
|---|---|---|
| `monstersspellbooks` | `monstersspellbooks-0.0.16.3.jar` | CANÔNICO VIA PR #140 / EXACT PHYSICAL+RELEASE 0.0.16.3 / 98 SPELL REGISTRATIONS CLOSED SEMANTICALLY / NECRO+AERO SCHOOLTYPES OBSERVED IN SOURCE ONLY / AERO 0 SPELL REGISTRATIONS + INSTALLED AERO STATE UNVERIFIED AFTER 0.0.16.3 CLEANUP / EXACT BINARY NUMERICAL/API INTERNALS FAIL-CLOSED |

## Phase 2AG — canonical predecessor

| Mod ID | Artefato físico | Estado |
|---|---|---|
| `ars_n_spells` | `ars_n_spells-3.3.2.jar` | CANÔNICO VIA PR #137 / EXACT PHYSICAL+RELEASE 3.3.2 / OFFICIAL NEOFORGE SOURCE BASELINE 3.3.0 / 5 RITUAIS / 5 MANA MODES / SPELL LOOM+CARRIERS / 8 TRANSPORT PROXIES, 0 SPELLS SEMÂNTICOS INDEPENDENTES |

## Phase 2AF — canonical predecessor

| Mod ID | Artefato físico | Estado |
|---|---|---|
| `not_enough_glyphs` | `not_enough_glyphs-1.21.1-4.6.1.jar` | CANÔNICO VIA PR #135 / SOURCE-PINNED 4.6.1 / 40 REGISTROS CONDICIONAIS / 39 SOURCE-ENABLED / 4 FORMS + 36 EFFECTS / BINDER 25 STORAGE + 10 CASTER / 13 PERKS |

## Concorrência — não colidir

Phase 2AQ / PR #152 já está canônica em `main@bdf5271c265b5f40ee5a9e7695c7d71374a4c31c`. O PR #153 é o follow-up ativo de correção factual da Phase 2AP e deve preservar integralmente os arquivos adicionados pela 2AQ.

A CI #2229 do antigo HEAD do PR #153 foi invalidada como evidência final quando a main avançou com a Phase 2AQ. A correção precisa ser reconciliada com `main@bdf5271c...` e revalidada em um novo HEAD antes do merge.

PRs antigos de Ars permanecem concorrência separada e não são usados como autoridade contra a main mais recente.

Antes do merge, buscar `main` novamente e reconciliar qualquer avanço. CI anterior à última reconciliação não vale como evidência final.

## Próxima seleção após a correção Phase 2AP / PR #153

Selecionar somente depois de:

1. reconciliação e CI GREEN do PR #153 no HEAD exato;
2. latest-main gate imediatamente pré-merge;
3. merge e confirmação do `main` final;
4. CI pós-merge no SHA exato da main;
5. verificação da modlist física atual;
6. pesquisa de PR/branch equivalente;
7. leitura do catálogo já canônico;
8. confirmação da versão exata e do melhor source/API/release aplicável.

Continuar preferindo componentes cuja superfície atual possa ser fechada sem inferência. `cataclysm_spellbooks`, `gaze`, `leylines` e `somakespells` continuam parciais sob a evidência atual.

## Providers parcialmente fechados — não contam como concluídos

Exemplos atuais:

- `leylines` — nomes públicos parciais; inventário total atual não verificado;
- `somakespells` — exact artifact/release e release-line auditados, mas inventário granular atual ainda não fechado;
- `cataclysm_spellbooks` — artefato instalado 1.1.13 sem source público exato equivalente já fechado;
- `gaze` — superfície pública auditada, mas registry/source-JAR exato ainda não fechado.

## Regras de fila

- presença/versão vêm da modlist/JAR atual, não do snapshot histórico;
- README preparatório, guia lido ou branch antiga não equivale a catálogo canônico;
- source público de versão diferente não autoriza promover internals da versão instalada;
- exact source-version pin não equivale automaticamente a byte-for-byte JAR reproducibility;
- library/API ou compat provider pode fechar com zero spells se zero registro próprio for demonstrado e suas superfícies reais estiverem inventariadas;
- compatibility bridge pode fechar semanticamente no publisher evidence ceiling quando o escopo público atual é explicitamente bounded e nenhuma identidade nova é atribuída, mantendo internals não publicados fail-closed;
- API/framework que migrou para sibling provider deve manter a authority no provider atual; não atribuir API histórica ao consumer instalado;
- client presentation hook não é cast authority;
- cross-provider cast cancellation/reconciliation não vira segundo cast authority;
- registry/example/animation/compatibility/fire/recipe/data-map/affix object não vira spell por contagem;
- capabilities repacked mantêm provenance/namespace e não criam duplicata semântica automaticamente;
- integração sem hook seguro permanece fail-closed;
- Black Arcana não duplica mana, casting, cooldown, targeting, summon lifecycle, proc pipeline, relic migration/settlement, fire-framework settlement, recipe/resource settlement, loot-category/affix settlement, presentation adapter ou world mutation de provider;
- private reflection usada internamente por provider não é automaticamente API de integração segura para Black Arcana;
- source-family label ou Java symbol não deve ser confundido com registry ID sem evidência;
- provider parcial continua zero até inventário atual fechar ao teto de evidência aceito;
- Phase 3 continua bloqueada até o catálogo/deduplicação provar lacunas reais.

## Histórico

Para os 103 candidatos e respectivos estados do checkpoint de 2026-09-07, consultar `PROVIDER-AUDIT-QUEUE-2026-09-07.md`. Antes de retomar qualquer linha daquele snapshot, reconciliar presença e versão contra a modlist física atual.