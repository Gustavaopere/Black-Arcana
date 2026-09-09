# Fila operacional de auditoria dos providers mágicos

## Autoridade atual

O snapshot imediatamente anterior está preservado byte-for-byte em [`PROVIDER-AUDIT-QUEUE-PRE-PHASE2AV.md`](./PROVIDER-AUDIT-QUEUE-PRE-PHASE2AV.md).

- Minecraft 1.21.1
- NeoForge `21.1.248`
- modlist física: **595 entradas top-level**
- SHA-1 da modlist: `7aaece7acbfb07ba4d0c66029042f36c50d046f0`
- jarjar/internal não conta como provider top-level

## Cobertura

- branch Phase 2AV criada sobre `main@f3a3f95a10cf830b6bf973612d519e53d9168adc`;
- esse `main` já contém Phase 2AU / PR #158;
- cobertura canônica na base: **49/100 = 49%**;
- Phase 2AU: `apothic_enchanting` 1.6.2, componente #49, canônico;
- Phase 2AV: `apotheosis` 8.8.0, **50/100 = 50% somente candidato** até CI GREEN no HEAD reconciliado + gate final de `main` + merge + confirmação pós-merge.

## Phase 2AV — Apotheosis 8.8.0 — candidate #50

| Mod ID | Artefato físico | Estado |
|---|---|---|
| `apotheosis` | `Apotheosis-1.21.1-8.8.0.jar` | EXACT PHYSICAL + EXACT PUBLISHER + EXACT OFFICIAL SOURCE / ADVENTURE-RPG AUTHORITY / DYNAMIC REGISTRIES / WORLD TIER + INVADER STATE / AFFIX+GEM+LOOT / REFORGING+SALVAGING+AUGMENTING / 7 PAYLOAD PROVIDERS / NO STANDALONE CAST SURFACE OBSERVED / APOTHIC SIBLING DEDUP / #50 CANDIDATE |

### Evidence boundary

- physical version 8.8.0, mod id `apotheosis`, SHA-1 `1e4837fcaf24fe73dba1082656736d872690b303`;
- CurseForge project/file `313970 / 8826922`, published 2026-09-07, NeoForge / Minecraft 1.21.1;
- exact source `Shadows-of-Fire/Apotheosis@e825cd9dcb9a6fff5e163659812ff32390e343a6`, message `8.8.0`;
- root tree `98ffba7432210ac6b5d807a83fc8e49e74db31fd`;
- exact Apotheosis Java package tree `a517a5e6ecf47bc1eae07c28206868a4317ffb8b`;
- source baselines/ranges: Minecraft 1.21.1, Java 21, NeoForge 21.1.235+, Placebo 9.9.2+, Apothic Attributes 2.10.0+;
- source metadata orders optional Apothic Enchanting 1.6.2+ and Apothic Spawners 1.4.0+ after Apotheosis and treats Curios as optional;
- physical pack: NeoForge 21.1.248, Placebo 9.9.2, Apothic Attributes 2.10.1, Apothic Enchanting 1.6.2, Apothic Spawners 1.4.0.

`apothic_attributes`, `apothic_enchanting` and `apothic_spawners` retain separate provider authority and previous catalog components. Phase 2AV does not count them again.

### Runtime and authority boundary

Exact bootstrap declares provider registry keys for:

- `rarity`;
- `affix`;
- `gem`;
- `affix_loot_entry`;
- `invader`;
- `rogue_spawner`;
- `elite`;
- `purity_weights`;
- `augment`;
- `tiered_augment`;
- `rarity_override`.

Provider state includes player tier/unlocks, invader cooldown/data, spawn data, bonus loot tables and damage reductions. Provider components own affixed-item, gem, rarity and related item/UI state. Provider recipes/menus own reforging, salvaging, augmenting and gem-cutting workflows.

No standalone provider spell/mana/ritual/casting registration or payload surface was observed in the exact source-tree/bootstrap/network audit. `Spellbreaker` is an affix name in the changelog, not a spell-runtime seam.

### Network boundary

Registered payload providers:

- `apotheosis:config` — CLIENTBOUND v4;
- `apotheosis:boss_spawn` — CLIENTBOUND v1;
- `apotheosis:link_item` — SERVERBOUND v1;
- `apotheosis:radial_state` — BIDIRECTIONAL v1;
- `apotheosis:gem_case_select` — BIDIRECTIONAL v1;
- `apotheosis:world_tier` — BIDIRECTIONAL v1;
- `apotheosis:reroll_result` — CLIENTBOUND v1.

Serverbound/bidirectional paths retain provider validation: menu/slot context for item links, held item + registry gem for gem-case selection, and config/unlock checks for world-tier changes. These are provider interaction/state packets and must not enter Black Arcana's cast-intent pipeline.

### Black Arcana boundary

Apotheosis owns its Adventure/RPG gear, affix, gem, loot, encounter, world-tier and workstation runtime. Black Arcana retains canonical server-authoritative casting, targeting, transactional costs, BA cooldowns/charges, hazards, rituals, Corruption, Strain, Arcane Danger, Backlash and world safety.

No second mana/resource, no duplicate registry authority and no second cast pipeline are introduced. Future integration must use a proven provider-native exact-version seam behind an adapter; absent a safe seam, fail closed.

### Reload / clean-room

Provider registries are data-driven/synchronized. Do not build a stale mirrored registry or unbounded polling path. Reload-sensitive integration requires explicit invalidation/lifecycle handling.

License layers:

- root source code: MIT;
- generated source metadata: MIT;
- exact source assets: All Rights Reserved;
- current CurseForge project surface: All Rights Reserved.

Read-only factual audit only; no code/assets/text copied or adapted.

### Remaining fail-closed QA

- source↔physical-JAR reproducibility;
- physical-vs-publisher exact hash equality;
- complete-pack reload/event ordering;
- complete-pack mixin/runtime interactions;
- dedicated/client smoke for provider paths;
- optional Curios/Apothic compatibility behavior;
- non-API implementation-class stability;
- future-version parity.

### Canonicalization gate

Before merge:

1. fetch latest `origin/main`;
2. reconcile if it advanced;
3. review final diff;
4. require CI GREEN on the exact reconciled HEAD;
5. merge without discarding concurrent work;
6. confirm final `main` SHA and applicable post-merge validation.

Phase 3 remains blocked.

## Immediate predecessors

| Component | Phase / PR | Provider | Estado |
|---:|---|---|---|
| 49 | 2AU / #158 | `apothic_enchanting` | CANÔNICO em `f3a3f95a10cf830b6bf973612d519e53d9168adc` |
| 48 | 2AT / #156 | `apothic_spawners` | CANÔNICO |
| 47 | 2AS / #155 | `apothic_compats` | CANÔNICO |
| 46 | 2AR / #154 | `backportedspellbooks` | CANÔNICO |
| 45 | 2AQ / #152 | `apothic_compat` | CANÔNICO |

## Concorrência

Branch: `docs/magic-catalog-phase2av-apotheosis-8.8.0`, criada sobre `main@f3a3f95a10cf830b6bf973612d519e53d9168adc` após gate sem branch/PR Phase 2AV equivalente. Repetir o gate imediatamente antes do merge. CI anterior à última reconciliação não vale como evidência final.

## Próxima seleção

Somente após merge + confirmação pós-merge da Phase 2AV. Continuar preferindo providers cujo inventário corrente possa ser fechado sem inferência. `cataclysm_spellbooks`, `gaze`, `leylines` e `somakespells` continuam parciais e sem ponto adicional sob a evidência atual.

## Regras

- presença/versão vêm da modlist/JAR atual;
- source-version pin não implica JAR reproducibility;
- affix, gem, rarity, world tier, invader, recipe, attachment, payload ou compat object não vira BA spell por contagem;
- provider UI/state C2S não vira cast authority;
- sibling mod não é absorvido por dependência temática;
- integração sem seam seguro e exato permanece fail-closed;
- Phase 3 permanece bloqueada até o catálogo provar lacunas reais.
