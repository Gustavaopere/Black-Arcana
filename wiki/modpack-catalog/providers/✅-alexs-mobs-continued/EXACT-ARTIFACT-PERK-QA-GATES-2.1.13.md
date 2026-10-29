# Alex's Mobs Continued 2.1.13 — contratos de QA, progressão e gating

Status: `EXACT_ARTIFACT_SCOPED / 3 ROOTS / 1 COUNTED_EXACT / 2 CONDITIONAL / NO_MUTATING_HOOK / PACK_QA_PENDING`.

**Autoridade:** JAR físico `alexsmobs-2.1.13-neoforge+1.21.1.jar`, mod id `alexsmobs`, SHA-1 `50ddafdf3d12b33331e4eecb4ab514ae451baadd`; [auditoria exata](EXACT-2.1.13-ARTIFACT-AUDIT.md), PR #511, workflow `36949047824`. Este documento é um **plano de aceitação derivado da evidência**, não relatório de execução. Metodologia de status em [`PUBLIC-SOURCE-VERSION-DRIFT-2026-10-29.md`](PUBLIC-SOURCE-VERSION-DRIFT-2026-10-29.md). Manifesto computável em [`SEMANTIC-REACHABILITY-GATES-2.1.13.json`](SEMANTIC-REACHABILITY-GATES-2.1.13.json).

## Dependência real: identidade, obtenção, elegibilidade e execução não são a mesma coisa

| Raiz única / dono | Identidade exata | Aquisição em dados do JAR | Bloqueio de elegibilidade/uso real | Contagem estrita | Integração de perks |
|---|---|---|---|---|---|
| [Transmutation Table](actions/item-transmutation.md) — `alexsmobs:transmutation_table` | confirmada | recipe exata presente | custo XP, pools, UI/servidor e datapacks requerem verificação de valores e segurança | +1 | ⛔ sem hook mutador |
| [Mysterious Worm](actions/void-worm-summoning.md) — `alexsmobs:mysterious_worm` | confirmada | Capsid/Mosquito Larva presentes | `voidWormSummonable`, `voidWormSpawnDimensions` e profundidade efetiva não capturados | +0 condicional | ⛔ sem hook mutador |
| [Dimensional Carver](actions/dimensional-carver-passage.md) — `alexsmobs:dimensional_carver` | confirmada | recipe usa Eye + Mandible do Void Worm | obtenção normal depende da raiz condicional Void Worm; overrides podem alterar a cadeia | +0 condicional | ⛔ sem hook mutador |

**Grafo de obtenção (não um segundo pipeline):** Mosquito Larva → receita Capsid → Mysterious Worm → gates efetivos de dimensão/depth/config → Void Worm → Eye/Mandible → recipe do Carver → portal. O grafo de obtenção **não** cria sete spells; ele descreve dependências de duas das três ações.

## Casos de teste propostos — NÃO executados

| ID | Cenário / pré-condição | Aceitação exigida | Dependência |
|---|---|---|---|
| AMC-T01 | Transmutation Table, escolha válida, XP suficiente, candidato válido | somente um input consumido/convertido, um resultado e um desconto XP pelo provider; estado reroll consistente | servidor dedicado + client |
| AMC-T02 | Menu aberto com candidato inválido, falta de XP, inventário alterado ou pacote repetido | falha segura, sem ganho de item, sem débito duplo; não inferir proteção antes do teste | segurança de menu e sessão |
| AMC-T03 | Reload/datapack/restore com opções de transmutação | tabela restaura dados e não reutiliza saída inválida | JAR 2.1.13 + save/restart |
| AMC-V01 | `voidWormSummonable=false` ou dimensão fora da lista permitida | não criar boss; consumo do Mysterious Worm seguir estritamente o provider | captura de config efetiva |
| AMC-V02 | dimensões permitidas e limiar de profundidade atendido, item válido | uma única transição de item → spawn, com owner/advancement coerentes | client + server |
| AMC-V03 | drop em ticks múltiplos, logout e multiplayer | nenhum segundo Void Worm para o mesmo evento; sem replay/cadeia duplicada | dedicado |
| AMC-D01 | Carver obtido pela recipe normal no pack e usado em superfície válida | exatamente um `EntityVoidPortal`, destino e durabilidade geridos pelo provider | gate do boss + recipes/loot efetivos |
| AMC-D02 | alvo inválido/protegido, destino fora de dimensão, logout ou reload com portal ativo | abortar ou encerrar conforme provider, sem bypass de WorldEffectPolicy para efeitos próprios do BA, sem portal órfão ou duplicação de custo | servidor + proteção + persistência |

Nenhum desses casos tem resultado registrado como `PASS`. O antigo CI de auditoria prova **identidade/estrutura** do artefato, não valida o comportamento do modpack montado.

## Mutadores e boundary segura

- **Transmutation:** hooks pré-custo/pré-settlement e validação server-side devem ser confirmados no **bytecode 2.1.13** e, idealmente, em API pública provider-native. Black Arcana não remete um segundo pacote nem remunera XP/result.
- **Summon:** progressão/Mastery do RPG Skill Tree não autoriza bypass de `AMConfig` ou spawn client-side. Se não houver seam segura, perk permanece inativa.
- **Carver:** expansão de range, duração, área ou dimensões necessita seam real no owner do `EntityVoidPortal`, segurança de destino, orçamento de entidades e política de proteção; não duplicar teleporte/durabilidade.

Black Arcana mantém casting, hazards e WorldEffectPolicy para seu próprio runtime; Alex's Mobs mantém seus efeitos nativos. O sibling RPG Skill Tree fornece somente progressão/perks/gates mediante contrato verificável. **Fail-closed para todos os três mutadores neste checkpoint.**

## Limite da etapa

- Alteração documental não promove o estado da fila alfabética: Alex's Caves Continued está sendo investigado em paralelo.
- Contagem preservada: **3** raízes, **1** `COUNTED_EXACT`, **2** `CONDITIONAL` e **0** fichas `COMPLETE_PERK_READY`.
- Nenhum teste físico, alteração em config de produção, permissão, mod JAR ou registro de eventos foi efetuado.
