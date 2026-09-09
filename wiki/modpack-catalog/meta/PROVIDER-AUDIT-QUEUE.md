# Fila operacional de auditoria dos providers mágicos

## Autoridade atual

O snapshot imediatamente anterior está preservado byte-for-byte em [`PROVIDER-AUDIT-QUEUE-PRE-PHASE2AU.md`](./PROVIDER-AUDIT-QUEUE-PRE-PHASE2AU.md).

- Minecraft 1.21.1
- NeoForge `21.1.248`
- modlist física: **595 entradas top-level**
- SHA-1 da modlist: `7aaece7acbfb07ba4d0c66029042f36c50d046f0`
- jarjar/internal não conta como provider top-level

## Cobertura

- branch inicialmente criada sobre `main@3c9795820f48cbe01a28ed1d4c3f1238cce816a0`
- base de repositório reconciliada: `main@78639998c212e91469e9036484bd5ac2ac9b699b`
- PRs #157 e #159, entre essas bases, são trabalho Stage 05 de keyboard focus, sem delta de catálogo e sem sobreposição com os 8 arquivos da Phase 2AU
- cobertura canônica na base reconciliada: **48/100 = 48%**
- Phase 2AT / PR #156: `apothic_spawners`, componente #48, canônico
- Phase 2AU: `apothic_enchanting` 1.6.2, **49/100 = 49% somente candidato** até CI GREEN no HEAD reconciliado + gate final de `main` + merge + confirmação pós-merge

## Phase 2AU — Apothic Enchanting 1.6.2 — candidate #49

| Mod ID | Artefato físico | Estado |
|---|---|---|
| `apothic_enchanting` | `ApothicEnchanting-1.21.1-1.6.2.jar` | EXACT PHYSICAL + EXACT PUBLISHER + EXACT OFFICIAL SOURCE / ENCHANTING AUTHORITY / 20 ENCHANTMENT KEYS / ETERNA+QUANTA+ARCANA / MAX_ETERNA / INFUSION / RAVEN PERSISTENCE / 4 PLAY PAYLOADS / 20 MIXINS / ENMERCHANTABILITY DISCREPANCY QA / #49 CANDIDATE |

### Evidence boundary

- physical version 1.6.2, SHA-1 `2623af251d3ddeae1d8e710afa76afe753834bab`;
- CurseForge project/file `1063926 / 8797650`, 2026-09-03, NeoForge 1.21.1;
- exact source `Shadows-of-Fire/Apothic-Enchanting@00fbcf00a2f42701645daf8906e54f67ec65a5dc`, message `1.6.2`;
- root tree `cad9b01b8d366e770cb811552884848afb320b30`;
- Java subtree `7f20d16f0d3f0c49caa1c5ae4582f88b22e8bd42`, recursive `truncated=false`;
- source ranges: Minecraft 1.21.1+, NeoForge 21.1.187+, Placebo 9.9.0+, Apothic Attributes 2.4.0+;
- physical pack: NeoForge 21.1.248, Placebo 9.9.2, Apothic Attributes 2.10.1.

No standalone provider spell/glyph/ritual registry and no provider mana/cast resource were observed.

### Runtime and authority boundary

- Eterna, Quanta, Arcana, clues, blacklist, treasure and stability are provider enchanting statistics;
- synced `apothic_enchanting:max_eterna`, default/range 100 / 0..100;
- exactly 20 provider enchantment keys;
- provider extension interfaces `EnchantableItem` and `EnchantmentStatBlock`;
- data-backed `EnchantingStatRegistry`;
- exact IMC method `set_ench_hard_cap`;
- infusion and keep-NBT infusion serializers;
- persistent `RavenTableStats` attachment;
- PLAY payloads version `1`: `clue`, `stats`, `enchantment_info` clientbound; `set_raven_stats` serverbound;
- Raven C2S is menu-gated and server-clamped; it is provider table state, not cast intent;
- generated manifest: 17 common + 3 client mixins.

Provider `Arcana` is an enchanting statistic; naming similarity does not transfer authority to/from Black Arcana. Apothic Enchanting owns its enchanting system and effects. Black Arcana retains canonical casting, targeting, transactional costs, BA cooldowns/charges, hazards, rituals, Corruption, Strain, Arcane Danger, Backlash and world safety. RPG Skill Tree receives no direct provider enchanting-runtime authority.

### Enchantability QA boundary

The exact changelog puts the Enchantability redesign in 1.6.1. Version 1.6.2 fixes star-prefixed display and adds Raven JEI transfer. Exact 1.6.2 source tests `rand.nextFloat() >= chance` on the observed +1-level path; this is not silently normalized to changelog prose. Source/JAR parity and physical runtime reproduction remain fail-closed, and no confirmed runtime bug is asserted.

### License / clean-room

- root source code: MIT;
- generated metadata: `MIT License`;
- exact source assets: All Rights Reserved;
- current CurseForge project surface: All Rights Reserved.

Read-only factual audit only; no code/assets/text copied or adapted.

### Remaining fail-closed QA

- source↔physical-JAR reproducibility;
- physical-vs-publisher hash equality;
- full-pack reload/event ordering;
- runtime Enchantability reproduction;
- complete-pack mixin interactions;
- optional compatibility paths;
- non-API implementation stability.

### Canonicalization gate

Before merge:

1. fetch latest `origin/main`;
2. reconcile if it advanced;
3. review final diff;
4. require CI GREEN on the exact reconciled HEAD;
5. merge;
6. confirm final `main` SHA and applicable post-merge validation.

Phase 3 remains blocked.

## Immediate predecessors

| Component | Phase / PR | Provider | Estado |
|---:|---|---|---|
| 48 | 2AT / #156 | `apothic_spawners` | CANÔNICO em `3c9795820f48cbe01a28ed1d4c3f1238cce816a0` |
| 47 | 2AS / #155 | `apothic_compats` | CANÔNICO |
| 46 | 2AR / #154 | `backportedspellbooks` | CANÔNICO |
| 45 | 2AQ / #152 | `apothic_compat` | CANÔNICO |
| 44 | 2AP / #151 | `create_enchantment_industry_plus` | CANÔNICO |

## Concorrência

Branch: `docs/magic-catalog-phase2au-apothic-enchanting-1.6.2`, criada originalmente sobre `main@3c9795820f48cbe01a28ed1d4c3f1238cce816a0`, reconciliada primeiro com `main@29a0099e899e03d80bf904c2d5ead72f40421fe8` por merge commit `58df873b431c8da91fc6a74d642107a7bcd737cc` e novamente, após a PR #159, com `main@78639998c212e91469e9036484bd5ac2ac9b699b` por merge commit `cdbe48cc268c499306c8c87e37a15a08145fe2db`. Nenhuma reconciliação usou force-push. O gate inicial não encontrou trabalho equivalente. Repetir o gate imediatamente antes do merge; CI anterior à última reconciliação não é evidência final.

## Próxima seleção

Somente após merge + confirmação pós-merge da Phase 2AU. Continuar preferindo providers cujo inventário corrente possa ser fechado sem inferência. `cataclysm_spellbooks`, `gaze`, `leylines` e `somakespells` continuam parciais e sem ponto adicional sob a evidência atual.

## Regras

- presença/versão vêm da modlist/JAR atual;
- source-version pin não implica JAR reproducibility;
- enchanting stat, enchantment, recipe, attachment, payload, mixin ou compat object não vira BA spell por contagem;
- table UI payload não vira cast authority;
- provider-owned stats preservam namespace/semântica;
- integração sem seam seguro e exato permanece fail-closed;
- Phase 3 permanece bloqueada até o catálogo provar lacunas reais.
