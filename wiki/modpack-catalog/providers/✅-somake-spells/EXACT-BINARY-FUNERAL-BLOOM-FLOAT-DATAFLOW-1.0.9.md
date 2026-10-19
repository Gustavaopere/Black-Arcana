# Somake Spells 1.0.9 — bounded float JVM dataflow for Funeral Bloom

**Estado:** 🟡 `PENDING_EXACT_FLOAT_PROBE`; nenhuma fórmula nova registrada sem saída do JAR exato.

## Artefato e autoridade

- Minecraft 1.21.1 / NeoForge; Somake Spells 1.0.9, mod ID `somakespells`, JAR da modlist `somakespells-1.0.9-1.21.1.jar`, CurseForge File 8867079, SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0`.
- Sibling `neoforge-rpg-skilltree/main@ed5b65b890767b406ce41127bcb793775263c7bd` é fonte da modlist. A auditoria de métodos/fórmulas anteriores está em [dossiê numérico](EXACT-BINARY-FUNERAL-BLOOM-NUMERIC-1.0.9.md).
- Novo [verificador](../../../../docs/qa/somake_109_float_dataflow.py), [testes](../../../../docs/qa/somake_109_float_dataflow_test.py), [workflow Java21](../../../../.github/workflows/somake-109-float-dataflow.yml). Inspeciona especificamente `FuneralBloomSpell.getImpactDamage(int,LivingEntity)` e `getRadius(int,LivingEntity)`.

## Gate e hipóteses proibidas

O scanner usa interpretação abstrata tipada da pilha JVM; retorna fórmula **apenas** para uma sequência inteira de instruções reconhecidas e um retorno float terminal, sem branches, reconhecendo exclusivamente a dependência externa `getSpellPower` (com descriptor JVM e tipos de argumentos demonstrados). Toda outra API, opcode, branch, tipo ou alias fora do modelo implica `NOT_PROVED`, sem adivinhação. O texto de bytecode, classes, código Java de terceiros e assets não são exportados; a evidência contém somente expressão simbólica ou razão de bloqueio.

| Método | Prova anterior | Novo recorte |
|---|---|---|
| `getImpactDamage` | Literais float `0.75` e `1.5`, uma adição, uma multiplicação e referência a `getSpellPower` | 🟡 Tentar demonstrar composição exata e tipos de parâmetros, condicionada a opcode integral |
| `getRadius` | 2 branches, `SchoolType.getPowerFor`, argumentos de clamp float 10.0/15.0 | ⚠️ Branches impedem certificação por interpretador linear; preservar pendência de CFG completo |

Mesmo uma expressão de retorno demonstrada não é evento de dano, dano sofrido, intervalo, raio real, custo, configuração ativa ou contrato mutador por personagem. `FAIL_CLOSED` para perks. Somake mantém autoridade de efeito; Iron's do host e recursos; RPG Skill Tree fornece atributos/Mastery/perks somente por contratos reais; Black Arcana somente do próprio runtime. Stage 06.05 permanece 🟡, Stage 09 retém validações físicas.
