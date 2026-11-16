# Raygun 1.0.10 — guardas pós-dano e causalidade até Irradiated

**Estado:** 🟡 descoberta read-only. Não equivale a certificação de perks, hook mutador ou gameplay; `NO_MUTATION`.

## Fonte e motivação

No [recorte de resultados de dano anterior](alexscaves-1010-raygun-hit-outcomes-cfg-handoff.md), o JAR publisher `alexscaves-1.0.10-neoforge+1.21.1.jar`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`, mostrou que os sucessores de `ACCompat.hurt @1041 / ifeq @1044` podem alcançar `LivingEntity.addEffect @1119`. Os caminhos mínimos passam pelos testes compilados em `@1056` e `@1064`, ainda sem predicados caracterizados.

A versão física permanece **1.0.10** na modlist do sibling; código-fonte upstream de outras versões não substitui os bytes publisher.

## Auditoria delimitada

A [sonda](alexscaves_1010_raygun_post_hit_guard_probe.py) reexecuta os gates SHA-exatos da [PR #1102](https://github.com/Gustavaopere/Black-Arcana/pull/1102) e compara seu [manifesto](../../wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-RAYGUN-HIT-OUTCOMES-CFG-1.0.10.json), antes de examinar o método nativo.

- Janela `[1013,1091)` para invocações e contexto.
- Guards `@1044`, `@1056`, `@1064` e `@1088`: opcode, destino tomado, fallthrough, até cinco instruções anteriores e duas posteriores.
- A partir de cada sucessor, alcançabilidade no mesmo ciclo normal até `@1088`, `addEffect @1119` e `sendMSGToAll @1154`.
- Proíbe alterações não observadas da população de 26 métodos, do hash de `RaygunItem.class`, do digest de `onUseTick` (523 instruções; 57 branches), do relatório anterior ou do JAR físico.
- Os testes negativos rejeitam offsets duplicados, guards ausentes, opcodes incompatíveis, sucessores inválidos e snapshots alterados.

[Workflow de auditoria](../../.github/workflows/alexscaves-1010-raygun-post-hit-guards.yml). A primeira execução é `UNSEALED_DISCOVERY_ONLY` e imprime um relatório candidato, **sem alegar semântica antes da observação JVM**. Depois deve-se fixar `EXACT-RAYGUN-POST-HIT-GUARDS-1.0.10.json`, repetir a CI com `--snapshot`, registrar o que as janelas realmente permitem concluir e executar toda a CI pré-merge.

## Limites

O grafo observa possibilidades de execução normal, sem rastreamento de pilha de operandos, prova de reaching definitions, exceções, side effects reais, C2S, owner, claims/PvP ou semântica dinâmica dos guards. Um caminho alcançável não implica que todos os predicados possam ser satisfeitos simultaneamente. O bloqueio de mutação permanece, e esta entrega não muda os contadores globais nem de Alex's Caves.
