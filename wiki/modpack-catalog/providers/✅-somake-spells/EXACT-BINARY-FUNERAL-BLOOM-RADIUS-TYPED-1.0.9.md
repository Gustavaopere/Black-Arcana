# Somake Spells 1.0.9 — Funeral Bloom, auditoria tipada dos dois caminhos de raio

**Estado inicial:** 🟡 `PENDING_SHA_EXACT_TWO_PATH_JVM_PROOF`. A fórmula integral do raio não deve ser promovida até a inspeção de ambos os caminhos no artefato do publisher.

## Escopo e identidade

- Modlist sibling `neoforge-rpg-skilltree/main@ed5b65b890767b406ce41127bcb793775263c7bd`, release Somake `somakespells-1.0.9-1.21.1.jar`, CurseForge File 8867079, SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0`; Minecraft 1.21.1, NeoForge, Java 21.
- Última base integrada [PR #834](https://github.com/Gustavaopere/Black-Arcana/pull/834): `getRadius(int,LivingEntity):float`, grafo compilado de 28 instruções com um `ifnonnull`, um `goto`, junção e retorno; `SchoolType.getPowerFor`, `Math.max(FF)F`, `Mth.clamp(FFF)F` com operandos finais 10.0f/15.0f. A correspondência do `getSpellPower(int,Entity)` com a API oficial Iron's 3.16.3 já foi demonstrada.
- [Scanner de pilha](../../../../docs/qa/somake_109_radius_typed_paths.py), [fixtures](../../../../docs/qa/somake_109_radius_typed_paths_test.py), [workflow Java21](../../../../.github/workflows/somake-109-radius-typed-paths.yml).

## Critério de prova e clean-room

O interpretador abstrato usa valores simbólicos tipados nas posições da pilha e slots locais, preserva ordem dos operadores float32 e double, bifurca por `ifnonnull` e exige um retorno `freturn` íntegro por caminho. Só aceita invocações de um conjunto delimitado e descritores JVM exatos; falha se houver instrução desconhecida, consumidor incompatível, stack underflow, branch irreconciliável ou argumento de clamp inesperado.

**Não exportar** implementação, sequência compilada de opcodes, offsets do classfile, código de terceiro, JAR ou assets. A saída contém no máximo a condição de ramo demonstrada, expressões numéricas *abstratas* e nomes de métodos de fronteira; não prova comportamento durante casts reais.

| Pergunta | Antes do gate |
|---|---|
| Qual referência alimenta o `ifnonnull`? | ⚠️ Ainda sem prova tipada de origem |
| Os caminhos completo nulo e não nulo chegam ao clamp e retorno? | 🟡 Sob auditoria exata |
| Expressão matemática de `getRadius` | ⛔ Sem equação até prova de todos os opcodes e conversões |
| Tipo/unidades/efeito em entidades | ⚠️ Aguardar leitura de consumers, runtime e config |
| Perks de raio, área e targeting | ⛔ `FAIL_CLOSED`: não existe contrato seguro per-player comprovado |

**Autoridades:** execução nativa Somake, host e recursos do Iron's, progresso do RPG Skill Tree somente por interface real, runtime próprio do Black Arcana. Stage 06.05 🟡; Stage 09 condicionada sob D035. Nenhum ID novo de magia está sendo contado.
