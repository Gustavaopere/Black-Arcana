# Black Arcana — cinco pendências mágicas (acompanhamento)

**Atualizado: 2026-10-09.** Base técnica inicial: `Black-Arcana/main@9141a8ed1c345db4e995e5f2aa849df2c24769b9`; modlist física sibling `de80b186357cad20ba5b81892a8682777e96e35a`. Este arquivo é o quadro de execução; atualizar status somente após evidência concreta no HEAD/PR correspondente. **Nenhuma tarefa em andamento executa em segundo plano.**

| Pendência | Estado |
|---|---|
| Identificar eventuais magias ainda não descobertas em mods de outras categorias | 🟡 **Em auditoria** — 489 JARs inventariados; 142 candidatos priorizados (46 por nome + 96 por categoria), 139 dossiês individuais revisados (incluindo 32/347 OTHER); 315 OTHER ainda sem leitura; auditoria binária não executada |
| Comprovar registries binários de 39 providers atualmente documentados por fonte ou release | ⚠️ **Parcial** — 39 catalogados, 0 novas provas binary-exact |
| Verificar configurações, desbloqueios e aquisição de magias em Survival | ⚠️ **Condicionado** — 14 rotas de evidência, nenhuma aprovação física inferida |
| Atualizar algumas referências antigas que ainda indicam pastas ⚠️ já promovidas a ✅ | ✅ **Referências operacionais atuais corrigidas** |
| Concluir a ativação canônica do grande ritual `black_arcana:veil_anchor_consecration` | ⛔ **Bloqueado na Stage 06.05** — sem ingresso legítimo de jogador |

## Evidências por pendência

**1 — Modlist cross-domain:** [auditoria](AUDITORIA-CROSS-DOMAIN-2026-10-08.md) e [procedimento de inspeção](../../../docs/qa/nonmagic_physical_jar_triage.md). O índice físico contém **587 = 97 linhas Magic + 489 JARs fora de Magic + 1 NeoForge loader**, este último indevidamente contado como mod no checkpoint anterior. **489/489 nomes físicos** estão agora num manifesto determinístico; a triagem prioriza **46** por nome e **96** adicionais por categoria (142 prioritários; outros 347 JARs também incluídos na ferramenta). **139 dossiês** tiveram revisão textual individual (11 candidatos lexicais + 96/96 por categoria + [32/347 dossiês `OTHER`](AUDITORIA-OTHER-2026-10-09.md) conferidos na primeira passada, deixando 315/347 sem leitura individual). As outras 35 entradas do grupo lexical estão vinculadas a catálogos canônicos existentes, sem nova inspeção binária. Os **142/142 candidatos priorizados** têm rota documental, mas os **315 OTHER restantes** ainda exigem leitura semântica individual; os 347/347 continuam sem auditoria binária da instância. Fechamento de leitura documental por categoria **não** encerra cobertura de registries ou confirma ausência de feitiços. O índice sibling registra mudanças pós-snapshot que não alteram retroativamente a base física certificada de 587 posições sem novo dump. O scanner de ZIP/sha de 489 JARs foi implementado e testado em ZIPs sintéticos, **não executado na instância real**. Não há prova de ausência de feitiços nas outras linhas nem novo ID certificado.

**2 — Registries:** [matriz nominal dos 39](REVALIDACAO-BINARIA-39-PROVIDERS-2026-10-08.md) e [crosswalk 69](PHYSICAL-LEDGER-VERSION-RECONCILIATION-2026-10-08.md). O coletor [physical_provider_fingerprint_collector.py](../../../docs/qa/physical_provider_fingerprint_collector.py) produz SHA-1/SHA-256 read-only sobre os 69 JARs esperados, **mas ainda não foi executado contra a instância real**. Não transforma nome de JAR em prova de registry.

**3 — Configuração/Survival:** [14 checklists atuais](CONDITIONAL-PROVIDER-CLOSURE.md) e [coletor deployed](../../../docs/qa/provider-catalog-deployed-evidence.md). Faltam os valores `config/`, `defaultconfigs/`, `serverconfig/`, scripts/dados efetivamente carregados, possíveis desbloqueios, testes de cliente e obtenção em Survival. Nenhum desses dados foi simulado.

**4 — Links e status:** [roteamento atualizado](CONDITIONAL-PROVIDER-CLOSURE.md) aponta para pastas ✅ de Traveloptics e Deeper and Darker e usa os audits físicos de 08/10. Os checkpoints datados antigos foram preservados intencionalmente como históricos.

**5 — Grand ritual:** [gate de desenho e aceite](../../../docs/qa/ritual-veil-anchor-activation-design-gate-2026-10-08.md) e [plano 06.05](../../../plans/06-rituals/05-final-validation-handoff.md). `RitualEngine` existe, mas sem entrada player-facing de produção o ritual não é executável por caminho legítimo; não criar comando ou item de debug para fabricar PASS.
## Legenda

- ✅ catalogado/concluído no escopo evidenciado · ❌ não catalogado · 🟡 em implementação/triagem · ⚠️ parcial ou condicionado · ⛔ bloqueado por contrato/superfície ausente.
- Os 164 diretórios de providers estão ✅ na **catalogação estrutural**. Os 97 dossiês da categoria física `Magic` estão reconciliados. Isso **não** prova a ausência de magias em todas as outras categorias nem disponibilidade em Survival.
- O mínimo estrito global continua **1851** (1849 no escopo do usuário, sem Traveloptics e Deeper and Darker base); nenhuma das cinco linhas altera esse mínimo por presunção.

## Regra operacional de atualização

Quando uma pendência avançar: anexar SHA/artefato/fonte, registrar quantidade restante, atualizar o checklist e o teste aplicável, depois reconciliar esta tabela. Não converter `⚠️` ou `⛔` em ✅ por documentação de intenção.
