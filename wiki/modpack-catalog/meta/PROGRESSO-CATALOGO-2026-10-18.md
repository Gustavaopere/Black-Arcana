# Black Arcana — progresso de catalogação, cohort 2026-10-18

**Checkpoint documental com base em `Black-Arcana/main@511ec03f0da62ebfc1722825def50354594976c3` e modlist física indexada no `neoforge-rpg-skilltree/main@ed5b65b890767b406ce41127bcb793775263c7bd`.** Este arquivo distingue a cobertura dos objetos mágicos, a dos registros binários, o aprofundamento por campo e a habilitação real de perks.

## Barra 1 — universo de magias/rituais/ações sobrenaturais de todos os mods

**Total desconhecido — percentual global indeterminado.** O catálogo registra pelo menos **1.857 objetos semânticos na baseline de 13/10** (**1.855** no escopo mencionado naquele checkpoint), mas o universo final de objetos de todos os mods continua **sem denominador verificável**. Isto é um **piso**, não uma fração; não representar como `1857 / 1857 = 100%`. A PR draft #825 tem uma baseline operacional diferente, **mínimo 1.856 / 1.854**; reconciliar denominador e cortes antes de substituir uma baseline por outra.

Campanha de evidência física do recorte histórico **39 providers** na `main`: **25/39 = 64,1%** com prova binária exata no último checkpoint consolidado de 13/10; é uma **submétrica delimitada**, não a conclusão do catálogo global, não é cobertura de perks nem QA em cliente. PRs draft posteriores podem ter avançado a campanha mas não contam como `main`.

## Barra 2 — Somake Spells 1.0.9, provider trabalhado nesta tranche

**83/83 (100%)** — fichas de identidade de spells do release verificadas no registry exato e já presentes em `registry-1.0.9/`. **7/83 (8,43%)** — fichas que receberam **nesta tranche** um novo dossiê de gate de aquisição/perk por terem `allowCrafting()` próprio (3 retornos `false` constantes, 4 não constantes). **7/7 (100%)** — classes com overrides `allowCrafting()` cobertas por esse recorte de documentação. Isto não representa percentual de todas as fichas com hooks/perks implementáveis: a auditoria de causalidade dos efeitos e mecanismos para os outros 76 não foi aferida aqui.

`Somake 1.0.9` = ✅ catalogado estruturalmente, ⚠️ condicionado em configuração/reachability, ⛔ sem hook mutador homologado para a mudança destas skills. Nenhuma nova identidade estrita; nenhuma migração de runtime; Stage 06.05 continua 🟡 e Stage 09 depende da campanha física sob D035.

### Critérios de avanço, por mod

Para cada provider o acompanhamento deve sempre expor: `registrados confirmados / identificados`, `fichas com campos técnicos comprovados / objetos elegíveis`, `hooks mutadores validados / demandas de mutação` (quando houver denominador) e `QA físico`. Se qualquer denominador estiver aberto, usar **—%** e declarar explicitamente o escopo, sem completar com estimativas.

Fonte da tranche: [Somake — matriz de sete gates](../providers/✅-somake-spells/PERK-REACHABILITY-GATES-1.0.9.md). Fonte global: [catálogo canônico](CATALOGO-GLOBAL-MAGIAS.md), [pendências](PENDENCIAS-MAGICAS-ATUAIS.md) e [regras técnicas](PERK-READY-TECHNICAL-STANDARD.md).

## Continuação Somake — prova de métodos de crafting no JAR (18/10/2026)

[CI SHA-exata #39186593493](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39186593493): **7/7 métodos de `allowCrafting()` com classe/descritor comprovados, 7/7 testes sintéticos**, incluindo quatro dependentes de três campos `Config.DISABLE_*` identificados no bytecode e três constantes `false`. Evidência estritamente estática/clean-room; [matriz compilada](../providers/✅-somake-spells/EXACT-BINARY-CRAFTING-METHOD-SEAMS-1.0.9.md). Barras inalteradas em seu escopo: global —% (denominador aberto), Somake identidades 83/83 (100%), aprofundamento **7/83 = 8,43% no recorte de métodos de aquisição**. Nenhuma QA física Survival, API de perk ou implementação nova inferida.

## Somake 1.0.9 — segundo eixo: descobertas compiladas de execução

[Java21 #39192999780](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39192999780) **SUCCESS**, SHA-1 físico/publisher verificado. O novo probe compilado cobriu as **7/7 classes desta campanha**, encontrou 116 declarações de métodos (101 com nomes de interesse para inspeção), incluindo onCast, onServerCastTick, pre-cast, getters de dano/cura/raio/duração e referências a entidades downstream. A [matriz causal estática](../providers/✅-somake-spells/EXACT-BINARY-CAST-CALLSITES-1.0.9.md) e as sete fichas foram atualizadas. O primeiro run #39192927218 falhou pelo teto de 250 caracteres para uma referência JVM, corrigido para 2048 com teste negativo; a execução seguinte passou.

**Barras invariantes:** global **—%** (universo ainda sem denominador); Somake **83/83 = 100% identidades**. A campanha limitada de **métodos de cast/efeito cobre 7/83 = 8,43%** das fichas atuais, sem equivaler a profundidade causal de runtime, fórmula completa ou perks homologadas. Identidades novas +0; adapters +0; Stage 06.05 🟡; validações físicas/Survival ainda pendentes.
