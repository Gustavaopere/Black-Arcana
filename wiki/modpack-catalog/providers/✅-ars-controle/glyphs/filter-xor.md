# Filter: XOR

State: `SOURCE-PINNED 1.6.15 / RUNTIME QA PENDING`

- Registry id: `ars_controle:glyph_filter_xor`
- Kind: adaptive binary Filter
- Tier: I
- Base mana: 0
- Scribe XP: 27
- Recipe: `minecraft:comparator` + `minecraft:redstone_torch`

## Behavior

Evaluates the next two valid filters and resolves only when their boolean results differ. Nested Y-level and Random filters receive provider-specific preparation before evaluation.

Malformed nested structure fails closed rather than treating missing filters as true.

## Engenharia para perks — execução pinada à release 1.6.16

- **Source exato 1.6.16:** [FilterBinary.java](https://github.com/Vonr/Ars-Controle/blob/14c5f4770a9ec265491fb9a7ae1a60a2123dfbc0/src/main/java/dev/qther/ars_controle/spell/filter/FilterBinary.java), `Vonr/Ars-Controle@14c5f4770a9ec265491fb9a7ae1a60a2123dfbc0`. Registrado no JAR físico 1.6.16; *identidade binária* comprovada separadamente, execução ainda sem teste de equivalência de método a bytecode.
- **Operação:** `FilterBinary.XOR` resolve só quando `a.get()!=b.get()`. O operador avalia os dois `Supplier<Boolean>` quando a estrutura está válida; apenas o resultado passa ao gate do Ars.
- **Parsing:** `getFilters()` localiza o primeiro filho no cursor e o segundo após seus augments; programa `setCurrentIndex(idx+skip+1)`, erro de estrutura/avaliação retorna false. Validador proíbe `IAdaptiveFilter` como filho para impedir compositions recursivas.
- **Risco:** fonte mutável estática `res` e `FilterRandom.chance`; a preparação de Random no **segundo filho** usa `getAugments(idx,caster)` (índice primeiro), ponto de QA. Nenhum callback RPG para 'um resultado booleano' provado como crédito separado de Mastery.
- **Estado:** ✅ localização do source e IDs físicos; ⚠️ interleaving de contextos, config instalada, erros de validação e Survival/host QA em aberto; ⛔ hooks/adapters RPG não implementados ou testados. O Ars controla gramática, mana e retomadas.
