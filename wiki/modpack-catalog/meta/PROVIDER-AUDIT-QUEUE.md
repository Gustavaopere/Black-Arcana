# Fila operacional de auditoria dos providers mágicos

## Autoridade atual

O snapshot imediatamente anterior está preservado byte-for-byte em [`PROVIDER-AUDIT-QUEUE-PRE-PHASE2AX.md`](./PROVIDER-AUDIT-QUEUE-PRE-PHASE2AX.md).

- Minecraft 1.21.1
- NeoForge `21.1.248`
- modlist física: **595 entradas top-level**
- SHA-1 da modlist: `7aaece7acbfb07ba4d0c66029042f36c50d046f0`
- estado de evidência Phase 2BO: `main@34a5fd495da744800b32b051e38c6473c6f5ea15`; esse SHA incorpora o source-pinned audit de Farmer's Spell 1.0.5.1 da PR #214 e passou exact-SHA post-merge CI #2565 / run `34724351805`, incluindo unit tests, diff sanity, NeoForge build, built-JAR verification, Foundation GameTests, dedicated-server smoke e canonical QA artifact `10307207453` (`sha256:50b94c3efc207dfd143a10367cf234473ede7dbbc1f36b9acdd3d3ca1ccc67fa`);
- jarjar/internal não conta como provider top-level.

## Métricas separadas

### Cobertura semântica de magias — métrica principal para o usuário

A reconstrução canônica após Phase 2BK fecha **1250 objetos mágicos semânticos**. Phase 2BL fecha Goety Iron 3.1 em **+14** e Goety Cataclysm 1.21.1-1.8.2 em **+52**, portanto o mínimo passa a **1316**. Phase 2BM fecha Ars Polymorphia 1.0.3 com **+0**, Phase 2BN fecha Ars Sable 1.1.2 com **+0**, e Phase 2BO fecha Farmer's Spell 'n Spellbooks 1.0.5.1 em **+6 `COUNTED_SOURCE_PINNED`**. O mínimo estrito corrente passa a **1322**. O denominador global continua incompleto e nenhuma porcentagem semântica é declarada.

A correção de contagem anterior ao fechamento Alshanex continua sendo **Werewolves Leap +1**. GTBC's SpellLib 2.2.0 adiciona **0** magias semânticas independentes. Gaze 1.1.7.1 adiciona **+1** Soulward Shield enquanto os 26 Spirit Rites permanecem `CONDITIONAL` por falta do valor COMMON implantado de `disableGazeRites`.

- delta semântico Farmer's Spell 1.0.5.1 Phase 2BO: **+6** (`COUNTED_SOURCE_PINNED`; seis registrations Gluttony; host-native Scroll Forge focus route fechada em nível de catálogo);
- delta semântico Ars Sable 1.1.2 Phase 2BN: **+0** (`ZERO_SEMANTIC_BRIDGE`);
- delta semântico Ars Polymorphia 1.0.3 Phase 2BM: **+0** (`ZERO_SEMANTIC_BRIDGE`);
- delta semântico Goety Iron 3.1 Phase 2BL: **+14**;
- delta semântico Goety Cataclysm 1.21.1-1.8.2 Phase 2BL: **+52**;
- delta semântico Goety 3.1.4 Phase 2BH: **+361**;
- delta semântico Leyline Spellbooks 1.0.3 Phase 2BG: **+14**;
- delta semântico Somake 1.0.8-fix Phase 2BF: **+0** (`67 exact registry`, reachability/config efetivo ainda `CONDITIONAL`);
- delta semântico Cataclysm: Spellbooks 1.1.13: **+59**;
- delta semântico Alshanex 4.0.3: **+18**;
- delta semântico Gaze 1.1.7.1 Phase 2BJ: **+1**;
- delta semântico Ignis Soulfires: Spellbooks 1.1.0 Phase 2BK: **+0**;
- delta semântico GTBC SpellLib: **+0**;
- delta semântico Werewolves: **+1**;
- mínimo estrito global após Phase 2BO: **1322**;
- denominador global: ainda incompleto;
- nenhuma porcentagem final de spells/magias é declarada enquanto inventories atuais permanecem abertas.

### Cobertura interna de componentes do catálogo

- Phase 2AY / PR #175 foi mergeada como `9a4e1cd6a462a278083ab946b5ed054864c3315e`; post-merge CI #2421 GREEN;
- Gaze / PR #180 foi mergeada como `03054438d1f126f48cb0b11b84c5d6589d677666`; a reconciliação Gaze permanece parcial e não cria novo componente canônico fechado;
- Phase 2BD / PR #186 foi mergeada como `95ec538ff1c34766450393522ce3affe1039d0dd`; post-merge CI #2465 GREEN;
- Phase 2BM / PR #210: HEAD `1b8d5d5761569f8ef1f3a32b7ece84cfb6ce6df6` passou CI #2543; squash merge `f2cdfe7b79d500540c281d70a76e8b6e3a77d311` passou exact-SHA post-merge CI #2544 / run `34713268914`;
- Phase 2BN / PR #212: HEAD `c4facc0286dab0b522bf2b09c5812ffdd935bd5d` passou CI #2553 / run `34720437808`; squash merge `c1c422b5ec72fe4308104f04282732d6c2f2bbc1` passou exact-SHA post-merge CI #2554 / run `34720646567`;
- Phase 2BO / PR #214: corrected HEAD `d3a92c31d7ac5b38183224ef28c6737e721fc758` passou CI #2564 / run `34723967662`; squash merge `34a5fd495da744800b32b051e38c6473c6f5ea15` passou exact-SHA post-merge CI #2565 / run `34724351805` e artifact `10307207453` (`sha256:50b94c3efc207dfd143a10367cf234473ede7dbbc1f36b9acdd3d3ca1ccc67fa`);
- cobertura de componentes após a reconciliação Phase 2BO: **63/100 = 63%**; `farmers_spell` é componente #63 por fechamento source-pinned do inventário de seis spells, sem promover compatibilidade runtime com o host físico atual.

O valor 63/100 nunca substitui a métrica semântica de magias.

## Phase 2BO — Farmer's Spell 'n Spellbooks 1.0.5.1 — componente #63 / semantic +6

| Mod ID | Artefato físico | Estado |
|---|---|---|
| `farmers_spell` | `farmers-spell-n-spellbook-1.0.5.1-1.21.1.jar` | EXACT PHYSICAL IDENTITY + SHA-1 / EXACT OFFICIAL SOURCE PIN `b7cbb403...` / 6 UNCONDITIONAL GLUTTONY SPELL REGISTRATIONS / `COUNTED_SOURCE_PINNED` +6 / HOST-NATIVE SCROLL-FORGE FOCUS ROUTE CLOSED AT CATALOG LEVEL / 4 COMMON + 3 CLIENT REQUIRED MIXINS / 0 PROVIDER PAYLOAD REGISTRATIONS OBSERVED / COMPONENT #63 / CURRENT-HOST RUNTIME QA FAIL-CLOSED |

### Evidence boundary

- physical SHA-1 `f77355e029af39bbaba3854e10cc087a608351ff`; physical CurseForge hash `810347191`;
- exact official source `GLDYM/Farmers-Spell-n-Spellbook@b7cbb40316a9ccbbc2ce2b56b3023647261ce569`, signed version-bump commit `1.0.5.0-1.21.1 -> 1.0.5.1-1.21.1`;
- exact source tree `83f54cd2415b424d1fc209191f6a3f90bd919312`, recursive complete;
- exactly six provider spell IDs: `goodberry`, `phantom_loot`, `seal_coat`, `bad_apple`, `chaos_slash`, `preserve_circle`;
- Gluttony school is support taxonomy, not a seventh semantic action;
- school sets `allowLooting=false`; generic random Iron's scroll loot is not used as reachability proof;
- provider Gluttony focus contains `#minecraft:foods` and `farmers_spell:foodgeist_seasoning`; Iron's 3.16.3 source-line Scroll Forge contract supplies the host-native focus-to-school/spell path;
- no provider override of `allowCrafting`, `isEnabled` or `canBeCraftedBy` was found for the six spell classes;
- required mixin footprint: 4 common + 3 client = 7, default require 1;
- `NetworkHandler.registerPackets()` is empty and no provider-owned payload registration surface was observed at the exact source pin;
- source has no `src/test` subtree; configured gameTest run target is not test-PASS evidence;
- ARR clean-room: no implementation bodies/assets/localization copied or adapted;
- runtime QA remains fail-closed because source build uses NeoForge `21.1.238` and Farmer's Delight `1.3.2` while the physical pack uses NeoForge `21.1.248` and Farmer's Delight `1.3.4`; GeckoLib is `4.9.2` on both sides only by version label; client/server boot, mixin application, Foodgeist progression, Scroll Forge acquisition and representative execution remain direct QA gates.

Phase 2BO therefore promotes the source-pinned semantic inventory and component closure only. It does not create a Black Arcana Gluttony school, alternate mana/scroll pipeline or certify provider runtime compatibility.

## Phase 2BN — Ars Sable 1.1.2 — componente #62 / semantic +0

| Mod ID | Artefato físico | Estado |
|---|---|---|
| `ars_sable` | `ars_sable-1.21.1-1.1.2.jar` | EXACT PHYSICAL IDENTITY / EXACT OFFICIAL SOURCE PIN `1fd83f3...` / 24 COMMON + 5 CLIENT REQUIRED MIXINS / PROTOCOL 2 + 0 PROVIDER PAYLOAD REGISTRATIONS / NO SPELL-GLYPH-RITUAL-SCHOOL-RESOURCE-ACTION REGISTRY / `ZERO_SEMANTIC_BRIDGE` / +0 / COMPONENT #62 / CURRENT-HOST RUNTIME QA FAIL-CLOSED |

Phase 2BN promotes only provider-component catalog closure; it does not add semantic magic or certify the physical host combination as runtime-compatible.

## Phase 2BM — Ars Polymorphia 1.0.3 — componente #61 / semantic +0

| Mod ID | Artefato físico | Estado |
|---|---|---|
| `ars_polymorphia` | `ars_polymorphia-1.0.3.jar` | EXACT PHYSICAL IDENTITY / EXACT OFFICIAL SOURCE PIN `e09b6c9...` / 5 REQUIRED MIXIN-ACCESSOR BINDINGS / PROTOCOL 1 + 1 PROVIDER SERVERBOUND UNIT PAYLOAD / NO SPELL-GLYPH-RITUAL-SCHOOL-RESOURCE-ACTION REGISTRY / `ZERO_SEMANTIC_BRIDGE` / +0 / COMPONENT #61 / CURRENT-HOST RUNTIME QA FAIL-CLOSED |

Phase 2BM promotes only provider-component catalog closure; it does not add semantic magic or certify runtime compatibility.

## Phase 2BL — Goety Iron 3.1 + Goety Cataclysm 1.21.1-1.8.2 — componentes #59/#60 / semantic +66

| Mod ID | Artefato físico | Estado |
|---|---|---|
| `goetyiron` | `GoetyIron-1.21.1-NeoForge-3.1.jar` | EXACT HASH-MATCHED / 2 FOCUS + 12 DISTINCT NON-FOCUS RITUALS / +14 / COMPONENT #59 |
| `goety_cataclysm` | `goety_cataclysm-1.21.1-1.8.2.jar` | EXACT HASH-MATCHED / 28 FOCUS + 24 DISTINCT NON-FOCUS RITUALS / +52 / COMPONENT #60 |

Evidence: NON-MERGE PR #205 and #206. Runtime mechanics and adapters remain fail-closed.

## Phase 2BK — Ignis Soulfires: Spellbooks 1.1.0 — componente #58 / semantic +0

| Mod ID | Artefato físico | Estado |
|---|---|---|
| `ignissoulfires_spellbooks` | `ignissoulfires_spellbooks-1.1.0.jar` | EXACT HASH-MATCHED ARTIFACT / BRIDGE_COMPAT + GEAR_LOOT_SUPPORT / NO SPELL-RITUAL-ACTION REGISTRY / ZERO_BRIDGE_INFRA / +0 / COMPONENT #58 |

## Phase 2BH — Goety 3.1.4 — componente #57 canônico

Exact evidence closes **123 Focus + 238 non-Focus rituals = +361 semantic objects**. Durable PR #198 clean HEAD passed CI #2523; squash merge passed exact-SHA post-merge CI #2524.

## Phase 2BG — Leyline Spellbooks 1.0.3 — componente #56 canônico

Exact hash-matched evidence closes **14** unconditional registered spells. Durable PR #195 clean HEAD passed CI #2503; squash merge passed exact-SHA post-merge CI #2504.

## Phase 2BF — Somake Spells 1.0.8-fix — exact registry, sem novo componente

| Mod ID | Artefato físico | Estado |
|---|---|---|
| `somakespells` | `somakespells-1.0.8-1.21.1-fix.jar` | EXACT PHYSICAL / EXACT HASH-MATCHED ARTIFACT / 67 CURRENT REGISTERED SPELL IDENTITIES / EFFECTIVE COMMON CONFIG + SURVIVAL REACHABILITY CONDITIONAL / +0 STRICT SEMANTIC DELTA / COMPONENT STILL OPEN |

## Phase 2BE — Cataclysm: Spellbooks 1.1.13 — componente #55 canônico

| Mod ID | Artefato físico | Estado |
|---|---|---|
| `cataclysm_spellbooks` | `cataclysm_spellbooks-1.1.13-1.21.jar` | EXACT HASH-MATCHED ARTIFACT / 59 REGISTERED SPELL IDENTITIES / +59 / #55 CANONICAL |

## Phase 2BD — Alshanex's Familiars 4.0.3 — componente #54

| Mod ID | Artefato físico | Estado |
|---|---|---|
| `alshanex_familiars` | `alshanex_familiars-1.21.1_v4.0.3.jar` | EXACT HASH-MATCHED ARTIFACT / 7 SPELLS + 11 RITUALS / +18 / #54 |

## Phase 2BJ — Gaze 1.1.7.1 — exact artifact, semantic +1, component still open

| Mod ID | Artefato físico | Estado |
|---|---|---|
| `gaze` | `gaze-1.1.7.1.jar` | EXACT HASH-MATCHED / 1 GAZE-OWNED IRON'S SPELL COUNTED / 26 SPIRIT RITES CONFIG-CONDITIONAL / +1 SEMANTIC / COMPONENT OPEN |

## Phase 2AY — GTBC's SpellLib 2.2.0 — canonical #53

| Mod ID | Artefato físico | Estado |
|---|---|---|
| `gtbcs_spell_lib` | `gtbcs_spell_lib-2.2.0-1.21.1.jar` | EXACT PHYSICAL / EXACT PUBLISHER RELEASE / LIBRARY+API INFRASTRUCTURE / 0 INDEPENDENT SEMANTIC SPELLS / #53 CANONICAL |

## Phase 2AX — FamiliarsLib 1.7.1 — canonical #52

| Mod ID | Artefato físico | Estado |
|---|---|---|
| `familiarslib` | `familiarslib-1.21.1-1.7.1.jar` | EXACT PHYSICAL / RELEASE-CORRELATED OFFICIAL SOURCE / FAMILIAR FRAMEWORK / 0 INDEPENDENT SEMANTIC SPELLS / #52 CANONICAL |

## Immediate predecessors

| Component | Phase / PR | Provider | Estado |
|---:|---|---|---|
| 63 | 2BO / #214 | `farmers_spell` | EVIDÊNCIA DURÁVEL em `main@34a5fd49...`; +6 `COUNTED_SOURCE_PINNED`; post-merge CI #2565 GREEN; promovido por esta reconciliação |
| 62 | 2BN / #212 | `ars_sable` | CANÔNICO em `main@c1c422b5...`; `ZERO_SEMANTIC_BRIDGE`; +0; post-merge CI #2554 GREEN |
| 61 | 2BM / #210 | `ars_polymorphia` | CANÔNICO em `main@f2cdfe7b...`; `ZERO_SEMANTIC_BRIDGE`; +0; post-merge CI #2544 GREEN |
| 60 | 2BL / #207 | `goety_cataclysm` | CANÔNICO; +52; exact-artifact |
| 59 | 2BL / #207 | `goetyiron` | CANÔNICO; +14; exact-artifact |
| 58 | 2BK / #204 | `ignissoulfires_spellbooks` | CANÔNICO; `ZERO_BRIDGE_INFRA`; +0 |
| 57 | 2BH / #198 | `goety` | CANÔNICO; +361; post-merge CI #2524 GREEN |
| 56 | 2BG / #195 | `leylines` | CANÔNICO; +14; post-merge CI #2504 GREEN |
| 55 | 2BE / #189 | `cataclysm_spellbooks` | CANÔNICO; +59 |
| 54 | 2BD / #186 | `alshanex_familiars` | CANÔNICO; +18 |
| 53 | 2AY / #175 | `gtbcs_spell_lib` | CANÔNICO; +0 |
| 52 | 2AX / #166 | `familiarslib` | CANÔNICO; +0 |
| 51 | 2AW / #161 | `apotheoticcreation` | CANÔNICO |
| 50 | 2AV / #160 | `apotheosis` | CANÔNICO |
| 49 | 2AU / #158 | `apothic_enchanting` | CANÔNICO |

## Próxima seleção

Phase 2BF / Somake, Phase 2BG / Leylines, Phase 2BH / Goety, Phase 2BL / Goety addons, Phase 2BM / Ars Polymorphia, Phase 2BN / Ars Sable e Phase 2BO / Farmer's Spell já foram reconciliadas no nível de evidência descrito acima. Não reiniciar esses fechamentos a partir de branches antigas.

Blockers atualmente **PARKED até existir input novo**:

- Not Enough Glyphs 4.6.1 — 39 registrations source-enabled permanecem `CONDITIONAL`; cada glyph usa config `SERVER` `not_enough_glyphs/<glyph>.toml` / `[general].enabled`, e nenhum conjunto implantado de world/server overrides está presente;
- Gaze 1.1.7.1 — o registry exato e Soulward Shield já estão fechados; os 26 Spirit Rites permanecem `CONDITIONAL` somente porque o valor COMMON implantado de `disableGazeRites` não está disponível;
- Somake Spells 1.0.8-fix — o registry exato de 67 identidades está fechado, mas config efetiva de `enableSpellLockSystem` e survival acquisition/reachability completa continuam sem autoridade suficiente.

A próxima seleção deve escolher **outro componente ainda aberto** para o qual exista evidência current/exact capaz de reduzir incerteza de inventário ou de classificação. Defaults de provider, publisher prose ou branches preparatórias não substituem estado implantado. Se um candidato só puder avançar com navegação/material externo indisponível, registrar a pendência e passar ao próximo blocker seguro em vez de fabricar fechamento.

Os estados correntes desta reconciliação passam a **1322 objetos semânticos mínimos / 63 de 100 componentes**. A promoção só se torna canônica na `main` após merge desta reconciliação e exact-SHA post-merge CI GREEN.

## Regras

- presença/versão vêm da modlist/JAR atual;
- source-version correlation não implica JAR reproducibility;
- framework/library não vira spell provider;
- tag de spell externo não conta como spell novo;
- componente fechado não altera automaticamente a contagem semântica de magias;
- provider action reachability deve ser provada por registry/tree/input ou mecanismo equivalente, não por aparência de UI;
- cliente envia intenção, nunca ownership authority;
- integração sem seam seguro e exato permanece fail-closed;
- Phase 3 permanece bloqueada até o catálogo provar lacunas reais e a cobertura semântica ser reconstruível.
