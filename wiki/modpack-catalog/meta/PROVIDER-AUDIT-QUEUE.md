# Fila operacional de auditoria dos providers mágicos

## Autoridade atual

O snapshot imediatamente anterior está preservado byte-for-byte em [`PROVIDER-AUDIT-QUEUE-PRE-PHASE2AX.md`](./PROVIDER-AUDIT-QUEUE-PRE-PHASE2AX.md).

- Minecraft 1.21.1
- NeoForge `21.1.248`
- modlist física: **595 entradas top-level**
- SHA-1 da modlist: `7aaece7acbfb07ba4d0c66029042f36c50d046f0`
- jarjar/internal não conta como provider top-level

## Métricas separadas

### Cobertura semântica de magias — métrica principal para o usuário

FamiliarsLib 1.7.x adiciona **0 magias semânticas independentes** neste fechamento. Seus spellcasting familiar abstractions e tags de Iron's consomem/classificam spells externos; o conteúdo histórico de Sound foi removido na linha 1.7 e movido para Tunes 'n Tomes.

- delta de numerador semântico da Phase 2AX: **+0**;
- delta de denominador semântico atribuível a FamiliarsLib: **+0**;
- denominador global: ainda incompleto;
- nenhuma porcentagem final de spells/magias é declarada por esta phase.

### Cobertura interna de componentes do catálogo

- base reconciliada: `main@9cc91f1bf9b7f41708ea70635d5b36b282947866`;
- Phase 2AW / PR #161 está integrada e o estado corrente dessa main possui CI completa GREEN no run `34428143443` / #2334;
- cobertura canônica de componentes na base: **51/100 = 51%**;
- Phase 2AX: `familiarslib` 1.7.1, **52/100 = 52% somente candidato** até CI GREEN no HEAD reconciliado + gate final de `main` + merge + confirmação pós-merge.

O valor 52/100 nunca substitui a métrica semântica de magias.

## Phase 2AX — FamiliarsLib 1.7.1 — candidate #52

| Mod ID | Artefato físico | Estado |
|---|---|---|
| `familiarslib` | `familiarslib-1.21.1-1.7.1.jar` | EXACT PHYSICAL / EXACT PUBLISHER FILE / RELEASE-CORRELATED OFFICIAL SOURCE / FAMILIAR FRAMEWORK + ATTACHMENT + NETWORK AUTHORITY / IRON'S SPELL CLASSIFICATION CONSUMER / SOUND CONTENT REMOVED IN 1.7 / 0 INDEPENDENT SEMANTIC SPELLS / #52 CANDIDATE |

### Evidence boundary

- physical runtime `1.21.1-1.7`, mod id `familiarslib`, SHA-1 `7fa3f3116e35c12456425ae195924ced33fcc2eb`;
- CurseForge project/file `1316458 / 8059464`, 2026-05-08, release, NeoForge / Minecraft 1.21.1;
- official source repository `Alshanex/FamiliarsLib`;
- strongest release-correlated source commit `56561e7fd474fbd5c5166c1ac96f235faae156ab`, same date and matching familiar-bed bug-fix intent;
- correlated source tree `9d39b4751b9e52874f66cf2187afab239d00b251`, recursive `truncated=false`;
- source metadata: MC 1.21.1, NeoForge development baseline 21.1.90, Iron's `1.21.1-3.15.5`, Curios 9.2.2, mod version `1.21.1-1.7`;
- no release tag or reproducible-build proof was established, so source↔installed-JAR exactness remains unproven.

### Runtime and authority boundary

FamiliarsLib demonstrably owns framework surfaces for familiars rather than a standalone player spell catalog:

- serializable `player_familiar_data` attachment;
- familiar data/lifecycle, beds and storage;
- familiar summon/selection/release/movement/storage/sync networking;
- `PayloadHandler` registers 17 optional handlers: 9 play-to-server and 8 play-to-client;
- spellcasting familiar base classes and familiar-spellbook/school interoperability;
- Iron's spell classification tags under `data/familiarslib/tags/irons_spellbooks/spells/**`.

The complete release-correlated tree has no provider-owned spell registry and no `data/familiarslib/spells/**` content. The Iron's tag files reference/classify spells owned by the external spell provider and count as **zero new semantic magics**.

The Modrinth 1.7 changelog explicitly says Sound-school content was removed and moved to Tunes 'n Tomes. Do not count older FamiliarsLib Sound-school prose as current 1.7.x content.

### Black Arcana / Stage 07.07 boundary

No automatic FamiliarsLib bridge is created. The BA noetic runtime remains server-authoritative and revalidates through its canonical familiar-ownership boundary. A FamiliarsLib entity cannot be admitted merely because it is a familiar, tameable, spellcasting pet or nearby entity.

Provider-specific ownership integration remains **fail-closed** until a current exact-version seam is proven and deliberately adapted. The catalog evidence identifies promising provider-owned familiar state, but source↔physical exactness and the intended stable public ownership contract are not closed strongly enough to promote a runtime adapter here.

### License / clean-room

License evidence conflicts:

- release-correlated source property: `All Rights Reserved`;
- current CurseForge surface: GPLv3;
- current Modrinth surface: MIT.

No reuse conclusion is inferred. Read-only factual audit only; no code/assets/text copied or adapted.

### Remaining fail-closed QA

- source↔physical-JAR reproducibility / exact source pin;
- exact stable provider-native ownership query suitable for Stage 07.07;
- runtime behavior against the physically installed Iron's/Familiars stack;
- save/load and attachment migration compatibility under the exact pack;
- optional-network compatibility under the exact pack;
- resolution of publisher/source license disagreement if reuse were ever contemplated.

None of these open QA items creates semantic spells or justifies an automatic Black Arcana integration.

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
| 51 | 2AW / #161 | `apotheoticcreation` | CANÔNICO no estado integrado corrente de `main@9cc91f1...`; ver nota histórica de GameTest no coverage/checkpoint |
| 50 | 2AV / #160 | `apotheosis` | CANÔNICO |
| 49 | 2AU / #158 | `apothic_enchanting` | CANÔNICO |
| 48 | 2AT / #156 | `apothic_spawners` | CANÔNICO |
| 47 | 2AS / #155 | `apothic_compats` | CANÔNICO |

## Concorrência

Branch: `docs/magic-catalog-phase2ax-familiarslib-1.7.1`. A branch foi originalmente criada em `40fedc5...` e, antes da edição, fast-forwarded sem force para `main@9cc91f1bf9b7f41708ea70635d5b36b282947866`. Repetir o gate imediatamente antes do merge. CI anterior à última reconciliação não vale como evidência final.

## Próxima seleção

Somente após merge + confirmação pós-merge da Phase 2AX. Continuar preferindo providers cuja superfície corrente possa ser fechada sem inferência. Em paralelo, a reconstrução da métrica semântica deve priorizar os providers que ainda impedem um denominador completo, incluindo `cataclysm_spellbooks`, `gaze`, `leylines` e `somakespells`.

## Regras

- presença/versão vêm da modlist/JAR atual;
- source-version correlation não implica JAR reproducibility;
- familiar framework não vira spell provider;
- tag de spell externo não conta como spell novo;
- histórico Sound anterior à 1.7 não conta para FamiliarsLib atual;
- componente fechado não altera automaticamente a contagem semântica de magias;
- familiar ownership precisa de seam provider-native comprovado;
- cliente envia intenção, nunca ownership authority;
- integração sem seam seguro e exato permanece fail-closed;
- Phase 3 permanece bloqueada até o catálogo provar lacunas reais.