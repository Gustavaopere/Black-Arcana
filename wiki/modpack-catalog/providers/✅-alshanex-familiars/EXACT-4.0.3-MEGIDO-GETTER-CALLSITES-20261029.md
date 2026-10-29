# Alshanex Familiars 4.0.3 — chamadas diretas aos getters de Megido

Estado: `EXACT_BIN_SAME_CLASS_CALLSITES_PROVED / VALUE_FLOW_NOT_VERIFIED / NO_MUTATOR / NO_REAL_MODPACK_QA`.

## Artefato, auditor e escopo

Versão: `alshanex_familiars-1.21.1_v4.0.3.jar`, `modid=alshanex_familiars`, SHA-1 físico/publisher **`e5051c2385a426d05bf203ba8081a23d891f6686`**. Comparação binária obrigatória antes da inspeção. O workflow [run 40938851308](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40938851308) executou o job `megido_consumer_audit` (`123676526680`) com sucesso e seis regressões sintéticas. Evidência em artifact textual **`12925712688`**. Script: `docs/qa/alshanex_403_megido_consumers.py`; workflow: `.github/workflows/alshanex-403-megido-consumers.yml`.

Apenas a classe compilada `net.alshanex.alshanex_familiars.spells.MegidoSpell` foi inspecionada com `javap -p -s -c` **transitório**. O relatório contém **metadados de chamadas**, não bytecode/disassembly ou código do fornecedor (All Rights Reserved). Identifica referências diretas do JVM para `getRange:()F` e `getRadius:()F` **dentro dessa mesma classe**; não é um grafo interclasses.

## Resultado exato e verificado

| Getter | Valor literal de retorno da [PR #949](EXACT-4.0.3-MEGIDO-RANGE-RADIUS-LITERALS-20261029.md) | Chamadas diretas detectadas na própria classe | Dentro de `onCast` | Outros métodos de origem |
|---|---:|---:|---:|---|
| `getRange(): float` | **15.0F** | **2** | **1** | `getUniqueInfo` (**1**) |
| `getRadius(): float` | **10.0F** | **2** | **1** | `getUniqueInfo` (**1**) |

Isso demonstra **que `onCast` faz chamadas diretas aos dois getters na classe MegidoSpell do JAR instalado**, além de `getUniqueInfo`; o método `getUniqueInfo` pode corresponder a metadados informativos, e seu papel efetivo **não** foi decodificado.

**Limite importantíssimo:** uma instrução JVM que invoca um getter prova a **referência de chamada**, mas não prova que o valor retornado define sozinho alcance de alvo, raio de dano, area-of-effect ou geometria de uma entidade. O fluxo de dados após a invocação, branches, fórmulas externas, servidores versus clientes e efeitos/consumidores em outras classes não foram verificados.

## Continuidade para perks e integração segura

1. Auditar o **fluxo consumidor** dos dois retornos dentro de `onCast` (callsites -> validação de alvo -> efeito de dano/entidade), com pesquisa simbólica/factual limitada e sem copiar corpo de método; comparar chamadas indiretas e dependências interclasses.
2. Verificar `getMaxConnections(int, LivingEntity)` e `getDamage(int, LivingEntity)` separadamente, com autoridade de classe/assinatura exata, sem inventar fórmulas e sem assumir `getRadius` como alcance universal.
3. Identificar um contrato provider-native oficial de mutação **antes** de propor perk ativa; nunca substituir o casting/settlement de Alshanex ou Iron's nem adicionar custo, dano ou cooldown pela segunda vez.
4. Verificar a execução física real no pack (multiplayer, cliente/servidor, alvos inválidos, proteções e caps). Até então `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED` e `COMPLETE_PERK_READY=0`.

O inventário global do provider permanece **7 spells + 11 rituais = 18 identidades**. A auditoria não altera o estágio de implementação nem o status alfabético independente de Alex's Caves.

## Primeiro uso do retorno de Megido — continuação 29/10/2026

O [auditor de primeira instrução](EXACT-4.0.3-MEGIDO-ONCAST-FIRST-USE-20261029.md) comprovou, em `onCast`, uma chamada direta a `getDamage` e uma a `getMaxConnections`, além dos getters `getRange/getRadius`. O retorno de `getRadius` é seguido imediatamente de conversão primitiva, enquanto o primeiro passo de `getRange` não prova consumo. Isto **não** é fluxo integral até a área ou dano nem autoriza mutadores; run `40941276448`, artifact `12927531288`.
