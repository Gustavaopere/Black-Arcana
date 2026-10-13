# Filter: OR

State: `SOURCE-PINNED 1.6.15 / RUNTIME QA PENDING`

- Registry id: `ars_controle:glyph_filter_or`
- Kind: adaptive binary Filter
- Tier: I
- Base mana: 0
- Scribe XP: 27
- Recipe: `minecraft:comparator` + `minecraft:redstone`

## Behavior

Consumes/interprets the next two valid filters in the spell grammar and resolves when either one is true. It accounts for augments attached to the first nested filter when locating the second filter and advances the spell context past the consumed nested filter sequence.

Malformed or failing nested-filter evaluation fails closed and can emit a provider error to the casting player.

## Engenharia para perks — execução pinada à release 1.6.16

- **Source exato 1.6.16:** [FilterBinary.java](https://github.com/Vonr/Ars-Controle/blob/14c5f4770a9ec265491fb9a7ae1a60a2123dfbc0/src/main/java/dev/qther/ars_controle/spell/filter/FilterBinary.java), `Vonr/Ars-Controle@14c5f4770a9ec265491fb9a7ae1a60a2123dfbc0`. Registrado no JAR físico 1.6.16; *identidade binária* comprovada separadamente, execução ainda sem teste de equivalência de método a bytecode.
- **Operação:** `FilterBinary.OR` combina duas `Supplier<Boolean>` com `a.get() || b.get()`, preservando short-circuit lógico; os dois filtros são encontrados via `getFilters()` a partir de `spellContext.getCurrentIndex`, pulando augments do primeiro.
- **Estado/cursor:** se `res==null`, client ou child inválido falha; após obter filtros válidos, `setCurrentIndex(idx+skip+1)` antes de avaliar. Prepara Y/Random dos filhos; erro gera mensagem sem spam e retorno false. `BinaryFilterValidator` exige dois filtros não-adaptativos, permitindo augments do primeiro.
- **Divergência para QA:** quando segundo filho é `FilterRandom`, código usa `spell.getAugments(idx,caster)` em vez do índice do segundo; não assumir chance correta com augments distintos. O campo `res` pertence ao singleton `FilterBinary` e requer teste de interleaving. **Perks:** OR não é duplicação de cast por cada operand.
- **Estado:** ✅ localização do source e IDs físicos; ⚠️ interleaving de contextos, config instalada, erros de validação e Survival/host QA em aberto; ⛔ hooks/adapters RPG não implementados ou testados. O Ars controla gramática, mana e retomadas.
