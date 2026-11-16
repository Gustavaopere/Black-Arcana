# Raygun 1.0.10 — conectividade causal de dano, radiação e mensagem visual

**Estado:** 🟡 descoberta estática em andamento. Esta auditoria não certifica o Raygun, não autoriza perks mutadoras, não muda índices e não altera runtime.

## Autoridade e continuidade

- Artefato publisher: `alexscaves-1.0.10-neoforge+1.21.1.jar`; SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`.
- `RaygunItem.class`: SHA-256 `3fc60cb7ff8be2744becf8ac9e524799349996972708845a124f02650bfb344c`.
- `onUseTick(Level,LivingEntity,ItemStack,int)`: 523 instruções, 57 desvios diretos, SHA-256 do parser `b037276094928625e501d13fddd11829e3fe5540d585f7d8213f37b098c39bc5`.
- Reutiliza o selo integral de 26 métodos da classe, a auditoria de resistência da PR #1019 e o contrato de recarga/munição integrado na [PR #1101](https://github.com/Gustavaopere/Black-Arcana/pull/1101). Não reaudita X-RAY, reservado a trabalho concorrente.

## Questão específica

Os offsets individuais de `ACCompat.hurt @1041`, `ifeq @1044`, `RESISTS_RADIATION @1088`, `LivingEntity.addEffect @1119`, `ifeq @1122` e `AlexsCaves.sendMSGToAll @1154` já estão documentados. Falta verificar **quais destinos são alcançáveis no mesmo ciclo normal do laço**, sem inferir causalidade apenas de sua proximidade textual.

A [sonda de grafo](alexscaves_1010_raygun_hit_outcomes_cfg_probe.py) reconstrói os sucessores de cada instrução do método compilado, verifica todos os 26 fingerprints anteriores, confere os pins conhecidos e calcula caminhos mais curtos limitados à região `[953,1157)`, sem atravessar a volta para `@953`. Para cada guarda `@1044`, `@1088` e `@1122`, compara destino tomado e fallthrough para as chamadas `@1119` e `@1154`. O relatório contém **contagens e posições de decisão**, não o corpo integral do método do provider.

O workflow [SHA-exato](../../.github/workflows/alexscaves-1010-raygun-hit-outcomes-cfg.yml) executa regressões sintéticas positivas/negativas e baixa o JAR publisher. Até produzir o primeiro resultado físico, sua execução será `UNSEALED_DISCOVERY_ONLY`. Após verificar a saída de CI, deve-se fixar o manifesto `EXACT-RAYGUN-HIT-OUTCOMES-CFG-1.0.10.json`, repetir a CI com `--snapshot` e registrar observações concretas aqui e na ficha individual.

## Limites e salvaguardas

Esse grafo contém exclusivamente **arestas normais, estáticas e intramétodo**; não reconstrói exceções, dispatch dinâmico, pilha de operandos, reaching definitions, ownership, autorizações C2S, efeitos realmente aceitos, persistência, sincronização, claims/PvP nem execução em cliente/servidor. Caminho alcançável significa **possibilidade de fluxo normal**, não sucesso de aplicação. A limitação à janela impede que uma iteração posterior seja contada como consequência da mesma tentativa de dano; entradas externas à janela são contabilizadas.

**Política:** `static_perk_contract=NOT_CERTIFIED`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `mutation=NO_MUTATION`, `provider_universe_closed=false`. Não elevar os contadores da catalogação por acrescentar esta prova.

## Resultado reproduzido no publisher JAR — CI #43974401894

A [primeira auditoria física SHA-exata do artefato](https://github.com/Gustavaopere/Black-Arcana/actions/runs/43974401894) executou **12/12 testes sintéticos** e confirmou o JAR publisher, a classe, os **26 métodos SHA-selados**, os 523 comandos JVM e 57 branches de `onUseTick`. O [manifesto observado](../../wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-RAYGUN-HIT-OUTCOMES-CFG-1.0.10.json) foi gerado diretamente do relatório de CI, não preenchido por antecipação. A extração cobriu **82 instruções** em `[953,1157)`; há **duas entradas normais no recorte a partir de fora** e **dez arestas normais de saída**.

| Aresta estrutural, ignorando valores de operandos | `addEffect @1119` alcançável por grafo? | `sendMSGToAll @1154` alcançável por grafo? |
|---|---|---|
| `hurt`/booleano `ifeq @1044`, destino tomado `@1051` | **SIM**, caminho mínimo de 26 arestas | **SIM**, caminho mínimo de 39 arestas |
| `hurt`/booleano `ifeq @1044`, fallthrough `@1047` | **SIM**, caminho mínimo de 27 arestas | **SIM**, caminho mínimo de 40 arestas |
| `RESISTS_RADIATION` `ifne @1088`, destino tomado `@1157` | **NÃO**, encerra a janela do ciclo | **NÃO**, encerra a janela do ciclo |
| `RESISTS_RADIATION` `ifne @1088`, fallthrough `@1091` | **SIM**, 10 arestas | **SIM**, 23 arestas |
| `addEffect`/booleano `ifeq @1122`, destino tomado `@1157` | **NÃO**, não retorna ao pedido na mesma janela | **NÃO**, encerra a janela do ciclo |
| `addEffect`/booleano `ifeq @1122`, fallthrough `@1125` | **NÃO**, pedido já ocorreu antes desse ponto | **SIM**, 11 arestas |

**Retificação causal posterior — PR #1103:** o resultado desta tabela é **somente alcançabilidade de arestas**, não uma trajetória com os valores dos operandos JVM preservados. O branch `ifeq @1044 → 1051` após retorno falso de `ACCompat.hurt` conduz a `iconst_0 @1051`, `istore 26 @1052`, `iload 26 @1054` e `ifeq @1056 → 1157`, encerrando a iteração **antes de `LivingEntity.addEffect @1119`**. Portanto, a interpretação anterior de que a falha de dano poderia prosseguir para a solicitação de irradiação era um falso positivo da busca de caminhos, que não rastreava os valores de stack/slots. O ramo de sucesso grava `1` por `iconst_1 @1047; goto @1048 → 1052` e prossegue apenas se os guards de `LivingEntity @1061–1064` e resistência `@1088` permitirem. O recorte continua sem comprovar execução real, status aceito ou resultado de servidor. Ver [auditoria corretiva](alexscaves-1010-raygun-post-hit-guards-handoff.md) e manifesto SHA-exato complementar.

Para perks, não assumir uma regra inventada `damage_success -> status_success`. Não duplicar `ACCompat.hurt`, `LivingEntity.addEffect` nem recompensas/XP com base em observação visual. Os métodos nativos e os guards continuam com autoridade do provider; **`NO_MUTATION`**.

**Próximo gate:** executar novamente o workflow sobre o commit que contém o snapshot usando `--snapshot`, confirmar CI geral e reconciliar com a `main` antes de merge. QA em mundo real, efeitos aceitos e semântica de `ChargeUsed`/C2S continuam pendentes.
