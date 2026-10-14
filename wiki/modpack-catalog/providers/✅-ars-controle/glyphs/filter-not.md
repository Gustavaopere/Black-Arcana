# Filter: NOT

State: `SOURCE-PINNED 1.6.15 / RUNTIME QA PENDING`

- Registry id: `ars_controle:glyph_filter_not`
- Kind: adaptive unary Filter
- Tier: I
- Base mana: 0
- Scribe XP: 27
- Recipe: `ars_nouveau:allow_scroll` + `minecraft:redstone_torch`

## Behavior

Evaluates the next valid filter and negates its result. Augments belonging to that nested filter are accounted for when advancing the spell context.

Missing/non-filter nested parts fail closed. Nested Y-level/Random filters receive provider-specific setup before evaluation.

## Engenharia para perks — execução pinada à release 1.6.16

- **Source exato 1.6.16:** [FilterUnary.java](https://github.com/Vonr/Ars-Controle/blob/14c5f4770a9ec265491fb9a7ae1a60a2123dfbc0/src/main/java/dev/qther/ars_controle/spell/filter/FilterUnary.java), `Vonr/Ars-Controle@14c5f4770a9ec265491fb9a7ae1a60a2123dfbc0`. Registrado no JAR físico 1.6.16; *identidade binária* comprovada separadamente, execução ainda sem teste de equivalência de método a bytecode.
- **Parser:** `FilterUnary.NOT` representa negação de um único `IFilter` que vem depois. `getFilter()` lê `spell.get(currentIndex)`, rejeita não-`IFilter` (retorna null) e considera `spell.getAugments(idx,caster).size()` para pular o filtro e seus augments ao atualizar o cursor.
- **Avaliação:** em bloco/entidade, quando `res==null`, client side ou child ausente, devolve false; caso contrário `spellContext.setCurrentIndex(idx+skip)` e aplica `!filter.shouldResolve...` em try/catch que devolve false em exceção. Prepara `FilterYLevel.y` e `FilterRandom.chance` do child antes de avaliar.
- **Gramática:** `UnaryFilterValidator` rejeita filho não-AbstractFilter e encadeamento de `IAdaptiveFilter` (inclusive outro NOT) no source. **Perks:** não tratar a negação como efeito próprio nem desativar validação para encadear filtros de composição sem segurança.
- **Estado:** ✅ localização do source e IDs físicos; ⚠️ interleaving de contextos, config instalada, erros de validação e Survival/host QA em aberto; ⛔ hooks/adapters RPG não implementados ou testados. O Ars controla gramática, mana e retomadas.
