# Filter: Level

State: `SOURCE-PINNED 1.6.15 / RUNTIME QA PENDING`

- Registry id: `ars_controle:glyph_filter_level`
- Kind: Filter
- Tier: I
- Base mana: 0
- Scribe XP: 27
- Recipe: `ars_nouveau:allow_scroll` + `minecraft:short_grass`

## Behavior

The filter snapshots its comparison Y from `caster position Y - 1`, cast to integer, then permits resolution only when the target's integer Y is equal to that stored value.

This is discrete integer-Y comparison rather than an arbitrary vertical tolerance band.

## Engenharia para perks — execução pinada à release 1.6.16

- **Source exato 1.6.16:** [FilterYLevel.java](https://github.com/Vonr/Ars-Controle/blob/14c5f4770a9ec265491fb9a7ae1a60a2123dfbc0/src/main/java/dev/qther/ars_controle/spell/filter/FilterYLevel.java), `Vonr/Ars-Controle@14c5f4770a9ec265491fb9a7ae1a60a2123dfbc0`. Registrado no JAR físico 1.6.16; *identidade binária* comprovada separadamente, execução ainda sem teste de equivalência de método a bytecode.
- **Predicado:** `FilterYLevel.LEVEL`, `comparison=0`; passes se `Integer.compare(targetY,(int)(casterPosition.y-1))==0`; em `onResolveBlock/Entity`, a classe atualiza `y` antes de deferir ao AbstractFilter.
- **Causalidade:** casterPosition usa `spellContext.getCaster().getPosition()`; são coordenadas da entidade/contexto do caster, não necessariamente a altura de olhos de um player real. Entidades usam cast int da coordenada Y.
- **Perks:** não substituir o limiar por um range arbitrário de tolerância; com filtro `NOT` ou composto, predicado pode ser consumido dentro de parser e cursor avançar.
- **Estado:** ✅ localização do source e IDs físicos; ⚠️ interleaving de contextos, config instalada, erros de validação e Survival/host QA em aberto; ⛔ hooks/adapters RPG não implementados ou testados. O Ars controla gramática, mana e retomadas.
