# Fila operacional de auditoria dos providers mágicos

## Autoridade atual

O snapshot imediatamente anterior está preservado byte-for-byte em [`PROVIDER-AUDIT-QUEUE-PRE-PHASE2AW.md`](./PROVIDER-AUDIT-QUEUE-PRE-PHASE2AW.md).

- Minecraft 1.21.1
- NeoForge `21.1.248`
- modlist física: **595 entradas top-level**
- SHA-1 da modlist: `7aaece7acbfb07ba4d0c66029042f36c50d046f0`
- jarjar/internal não conta como provider top-level

## Cobertura

- branch Phase 2AW criada sobre `main@517b3e9c6da648c1470c227a11f571d951fbee47`;
- esse `main` contém Phase 2AV / PR #160 e seu pós-merge #2295 GREEN;
- cobertura canônica na base: **50/100 = 50%**;
- Phase 2AV: `apotheosis` 8.8.0, componente #50, canônico;
- Phase 2AW: `apotheoticcreation` 2.0.0, **51/100 = 51% somente candidato** até CI GREEN no HEAD reconciliado + gate final de `main` + merge + confirmação pós-merge.

## Phase 2AW — Apotheotic Creation 2.0.0 — candidate #51

| Mod ID | Artefato físico | Estado |
|---|---|---|
| `apotheoticcreation` | `apotheoticcreation-2.0.0.jar` | EXACT PHYSICAL + EXACT PUBLISHER + EXACT OFFICIAL SOURCE / CREATE ITEM ATTRIBUTE BRIDGE / `rarity` + `affix` TYPES / APOTHEOSIS DATA CONSUMER / NO OWN MAGIC RESOURCE / NO OWN NETWORK OR PERSISTENCE / #51 CANDIDATE |

### Evidence boundary

- physical version 2.0.0, mod id `apotheoticcreation`, SHA-1 `6bbb91aea834941b47a6af3318b091f64e4375ab`;
- physical Create 6.0.10 and Apotheosis 8.8.0;
- CurseForge project/file `956637 / 8391265`, 2026-07-08, release, NeoForge / Minecraft 1.21.1;
- publisher Source link → `maxpowa/ApotheoticCreation`;
- exact source `maxpowa/ApotheoticCreation@ed56ccf54e1be132c983c524597300e852098840`;
- exact tree `5c5d51ef69b5f0f50d398d7f0479b8ca83894f7d`, recursive `truncated=false`;
- source metadata: MC 1.21.1, mod version 2.0.0, NeoForge development baseline 21.1.235, Create `[6,)`, Apotheosis `[8,)`, MIT;
- exact tree contains one Java source file.

### Runtime and authority boundary

The addon registers exactly two Create `ITEM_ATTRIBUTE_TYPE` entries:

- `apotheoticcreation:rarity`;
- `apotheoticcreation:affix`.

`RarityAttribute` reads provider-owned `LootRarity` through `AffixHelper` and provider codecs/registry. `AffixAttribute` reads provider-owned affix holders through `AffixHelper` / `AffixRegistry`.

Visible affix enumeration excludes paths `socket` and `durable`. Do not summarize the addon as exposing every affix without this caveat.

No addon-owned spell/mana/ritual/casting registry, payload/network class, persistence/attachment or parallel provider state is observed in the complete exact source tree.

### Create / Apotheosis boundary

- Apotheosis owns rarity/affix identity and item metadata.
- Create owns Attribute Filter semantics and downstream logistics.
- Apotheotic Creation owns the narrow registration/translation bridge only.
- Smart Observers, Brass Tunnels, funnels and other filter consumers are downstream Create behavior, not separate addon hooks unless independently proven.
- Apokinetics machine-gem/socket semantics remain a separate addon/provider concern.

Black Arcana must not copy this bridge, mirror affix/rarity registries or route its outputs into the canonical cast pipeline. If BA ever needs to observe the same classification, use a proven exact-version provider-native seam behind a dedicated adapter; otherwise fail closed.

### License / clean-room

- exact metadata: MIT;
- exact root `LICENSE.md`: MIT, copyright 2023 maxpowa;
- current CurseForge project: MIT;
- no separate asset-license file observed in the exact tree.

Read-only factual audit only; no code/assets/text copied or adapted.

### Remaining fail-closed QA

- source↔physical-JAR reproducibility;
- physical-vs-publisher exact hash equality;
- custom datapack rarity/affix handling;
- multiple-affix / whitelist / blacklist / combination semantics;
- downstream Create-consumer behavior;
- saved filter behavior after reload/restart;
- full-pack runtime compatibility;
- future Create/Apotheosis parity.

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
| 50 | 2AV / #160 | `apotheosis` | CANÔNICO em `517b3e9c6da648c1470c227a11f571d951fbee47` |
| 49 | 2AU / #158 | `apothic_enchanting` | CANÔNICO |
| 48 | 2AT / #156 | `apothic_spawners` | CANÔNICO |
| 47 | 2AS / #155 | `apothic_compats` | CANÔNICO |
| 46 | 2AR / #154 | `backportedspellbooks` | CANÔNICO |

## Concorrência

Branch: `docs/magic-catalog-phase2aw-apotheotic-creation-2.0.0`, criada sobre `main@517b3e9c6da648c1470c227a11f571d951fbee47` após gate sem branch/PR Phase 2AW equivalente. Repetir o gate imediatamente antes do merge. CI anterior à última reconciliação não vale como evidência final.

## Próxima seleção

Somente após merge + confirmação pós-merge da Phase 2AW. Continuar preferindo providers cujo inventário corrente possa ser fechado sem inferência. `cataclysm_spellbooks`, `gaze`, `leylines` e `somakespells` continuam parciais e sem ponto adicional sob a evidência atual.

## Regras

- presença/versão vêm da modlist/JAR atual;
- source-version pin não implica JAR reproducibility;
- metadata bridge não vira authority dos dados traduzidos;
- Create Attribute Filter não vira BA cast target/filter pipeline;
- downstream Create logistics não vira hook próprio do addon por inferência;
- integração sem seam seguro e exato permanece fail-closed;
- Phase 3 permanece bloqueada até o catálogo provar lacunas reais.