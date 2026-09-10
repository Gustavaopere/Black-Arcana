# Fila operacional de auditoria dos providers mágicos

## Autoridade atual

O snapshot imediatamente anterior está preservado byte-for-byte em [`PROVIDER-AUDIT-QUEUE-PRE-PHASE2AX.md`](./PROVIDER-AUDIT-QUEUE-PRE-PHASE2AX.md).

- Minecraft 1.21.1
- NeoForge `21.1.248`
- modlist física: **595 entradas top-level**
- SHA-1 da modlist: `7aaece7acbfb07ba4d0c66029042f36c50d046f0`
- `main` canônica após Phase 2AX: `4238275d2086a00c6f31960114733d74b8cdb1d8`
- jarjar/internal não conta como provider top-level

## Métricas separadas

### Cobertura semântica de magias — métrica principal para o usuário

FamiliarsLib 1.7.x adiciona **0 magias semânticas independentes**. Seus spellcasting familiar abstractions e tags de Iron's consomem/classificam spells externos; o conteúdo histórico de Sound foi removido na linha 1.7 e movido para Tunes 'n Tomes.

- delta de numerador semântico da Phase 2AX: **+0**;
- delta de denominador semântico atribuível a FamiliarsLib: **+0**;
- denominador global: ainda incompleto;
- nenhuma porcentagem final de spells/magias é declarada pela Phase 2AX.

### Cobertura interna de componentes do catálogo

- Phase 2AX / PR #166 foi mergeada como `4238275d2086a00c6f31960114733d74b8cdb1d8`;
- HEAD pré-merge `b5b36a6fa3b1a5bf3b2add56ec3c604592f5ca71` passou Black Arcana CI #2336;
- o merge SHA exato passou Black Arcana CI #2337 / workflow run `34430446827` com unit tests, diff sanity, NeoForge build, built-JAR verification, Foundation GameTest server, dedicated-server smoke e publicação do canonical QA JAR;
- cobertura canônica de componentes atual: **52/100 = 52%**.

O valor 52/100 nunca substitui a métrica semântica de magias.

## Phase 2AX — FamiliarsLib 1.7.1 — canonical #52

| Mod ID | Artefato físico | Estado |
|---|---|---|
| `familiarslib` | `familiarslib-1.21.1-1.7.1.jar` | EXACT PHYSICAL / EXACT PUBLISHER FILE / RELEASE-CORRELATED OFFICIAL SOURCE / FAMILIAR FRAMEWORK + ATTACHMENT + NETWORK AUTHORITY / IRON'S SPELL CLASSIFICATION CONSUMER / SOUND CONTENT REMOVED IN 1.7 / 0 INDEPENDENT SEMANTIC SPELLS / #52 CANONICAL / POST-MERGE CI GREEN |

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

Provider-specific ownership integration remains **fail-closed** until a current exact-version seam is proven and deliberately adapted. The catalog evidence identifies provider-owned familiar state, but source↔physical exactness and a stable ownership contract are not closed strongly enough to promote a runtime adapter.

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

None of these open QA items creates semantic spells or invalidates the provider-component closure already merged and post-merge validated.

## Immediate predecessors

| Component | Phase / PR | Provider | Estado |
|---:|---|---|---|
| 52 | 2AX / #166 | `familiarslib` | CANÔNICO em `main@4238275...`; CI pós-merge #2337 GREEN |
| 51 | 2AW / #161 | `apotheoticcreation` | CANÔNICO; ver nota histórica de GameTest no coverage/checkpoint |
| 50 | 2AV / #160 | `apotheosis` | CANÔNICO |
| 49 | 2AU / #158 | `apothic_enchanting` | CANÔNICO |
| 48 | 2AT / #156 | `apothic_spawners` | CANÔNICO |

## Próxima seleção

A Phase 2AX está encerrada e não bloqueia mais a escolha do próximo provider. A próxima auditoria deve continuar preferindo superfícies atuais que possam ser fechadas sem inferência.

Em paralelo, a reconstrução da métrica semântica deve priorizar os providers que ainda impedem um denominador completo, incluindo:

- `cataclysm_spellbooks` — publisher atual informa 65 spells, mas registry exato 1.1.13 permanece aberto;
- `gaze` — Rites/Geas atuais ainda não têm inventário granular completo;
- `leylines` — nove nomes públicos são apenas lower bound;
- `somakespells` — publisher informa `over 50 spells`, sem registry atual completo.

Alshanex's Familiars também exige reconciliação própria antes de qualquer contagem: a linha 4.0 removeu a Sound School do provider e a moveu para Tunes 'n Tomes, enquanto documentação histórica ainda pode listar esses spells sob Alshanex. Não promover histórico a ownership atual.

## Regras

- presença/versão vêm da modlist/JAR atual;
- source-version correlation não implica JAR reproducibility;
- familiar framework não vira spell provider;
- tag de spell externo não conta como spell novo;
- histórico Sound anterior à linha atual não conta no provider que deixou de possuí-lo;
- componente fechado não altera automaticamente a contagem semântica de magias;
- familiar ownership precisa de seam provider-native comprovado;
- cliente envia intenção, nunca ownership authority;
- integração sem seam seguro e exato permanece fail-closed;
- Phase 3 permanece bloqueada até o catálogo provar lacunas reais e a cobertura semântica ser reconstruível.
