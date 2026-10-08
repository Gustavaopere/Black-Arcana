# Black Arcana — cinco pendências mágicas (acompanhamento)

**Atualizado: 2026-10-08.** Base técnica inicial: `Black-Arcana/main@9141a8ed1c345db4e995e5f2aa849df2c24769b9`; modlist física sibling `de80b186357cad20ba5b81892a8682777e96e35a`. Este arquivo é o quadro de execução; atualizar status somente após evidência concreta no HEAD/PR correspondente. **Nenhuma tarefa em andamento executa em segundo plano.**

| Pendência | Estado | Evidência / próximo bloqueio |
|---|---|---|
| Identificar eventuais magias ainda não descobertas em mods de outras categorias | 🟡 **Triagem avançada, auditoria exaustiva ainda aberta** | [Auditoria cross-domain](AUDITORIA-CROSS-DOMAIN-2026-10-08.md): 490 entradas físicas fora de `Magic`, 46 candidatos lexicais, 35 catálogos existentes e 11 dossiês individuais revisados. **444 outras entradas não receberam varredura exaustiva de registries**, portanto não há prova global de zero novas magias. |
| Comprovar registries binários de 39 providers atualmente documentados por fonte ou release | ⚠️ **39/39 identificados; 0/39 promovidos a binary-exact nesta rodada** | [Matriz nominativa dos 39](REVALIDACAO-BINARIA-39-PROVIDERS-2026-10-08.md) e [crosswalk físico 69](PHYSICAL-LEDGER-VERSION-RECONCILIATION-2026-10-08.md). Faltam bytes/registries dos JARs físicos e comparação das identidades na versão exata. |
| Verificar configurações, desbloqueios e aquisição de magias em Survival | ⚠️ **14 rotas específicas de evidência; deployed QA não observada nesta rodada** | [Rotas e checklists atuais](CONDITIONAL-PROVIDER-CLOSURE.md); conferir `config/`, `defaultconfigs/`, `world/serverconfig`, KubeJS/datapacks, runtime e Survival na instância exata. Config de publisher ou CI não substitui estado carregado. |
| Atualizar algumas referências antigas que ainda indicam pastas ⚠️ já promovidas a ✅ | ✅ **Rotas operacionais atuais corrigidas** | [CONDITIONAL-PROVIDER-CLOSURE.md](CONDITIONAL-PROVIDER-CLOSURE.md) utiliza ✅ para Deeper and Darker/Traveloptics e descreve os audits de JAR 2026-10-08. Os checkpoints antigos continuam arquivados intencionalmente e não devem ser reescritos como se fossem contemporâneos. |
| Concluir a ativação canônica do grande ritual `black_arcana:veil_anchor_consecration` | ⛔ **Bloqueado — falta superfície legítima de jogador em produção** | [Gate de desenho/aceitação](../../../docs/qa/ritual-veil-anchor-activation-design-gate-2026-10-08.md), [plano 06.05](../../../plans/06-rituals/05-final-validation-handoff.md). O `RitualEngine` existe, mas ainda falta ingresso player-facing autorizado; não criar item/comando debug só para marcar PASS. |

## Legenda

- ✅ catalogado/concluído no escopo evidenciado · ❌ não catalogado · 🟡 em implementação/triagem · ⚠️ parcial ou condicionado · ⛔ bloqueado por contrato/superfície ausente.
- Os 164 diretórios de providers estão ✅ na **catalogação estrutural**. Os 97 dossiês da categoria física `Magic` estão reconciliados. Isso **não** prova a ausência de magias em todas as outras categorias nem disponibilidade em Survival.
- O mínimo estrito global continua **1851** (1849 no escopo do usuário, sem Traveloptics e Deeper and Darker base); nenhuma das cinco linhas altera esse mínimo por presunção.

## Regra operacional de atualização

Quando uma pendência avançar: anexar SHA/artefato/fonte, registrar quantidade restante, atualizar o checklist e o teste aplicável, depois reconciliar esta tabela. Não converter `⚠️` ou `⛔` em ✅ por documentação de intenção.
