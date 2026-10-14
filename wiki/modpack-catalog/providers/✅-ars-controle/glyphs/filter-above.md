# Filter: Above

State: `SOURCE-PINNED 1.6.15 / RUNTIME QA PENDING`

- Registry id: `ars_controle:glyph_filter_above`
- Kind: Filter
- Tier: I
- Base mana: 0
- Scribe XP: 27
- Recipe: `ars_nouveau:allow_scroll` + `minecraft:feather`

## Behavior

The filter snapshots its comparison Y from `caster position Y - 1`, cast to integer, then permits block/entity resolution only when the target's integer Y compares as greater than that stored value.

This is provider spell-grammar filtering, not a Black Arcana targeting authorization. A target rejected or admitted by this glyph does not bypass Black Arcana's own server-side target rules for Black Arcana spells.

## Engenharia para perks — execução pinada à release 1.6.16

- **Source exato 1.6.16:** [FilterYLevel.java](https://github.com/Vonr/Ars-Controle/blob/14c5f4770a9ec265491fb9a7ae1a60a2123dfbc0/src/main/java/dev/qther/ars_controle/spell/filter/FilterYLevel.java), `Vonr/Ars-Controle@14c5f4770a9ec265491fb9a7ae1a60a2123dfbc0`. Registrado no JAR físico 1.6.16; *identidade binária* comprovada separadamente, execução ainda sem teste de equivalência de método a bytecode.
- **Predicado:** `FilterYLevel.ABOVE` tem `comparison=+1`; `shouldResolveOnBlock` compara `Integer.compare(targetBlockY,this.y)==+1`; entidades usam `(int)entity.position().y`. Em `onResolveEntity/Block` define `y=(int)(spellContext.getCaster().getPosition().y-1)` antes de `super`.
- **Geometria:** Above é **qualquer** Y inteiro maior que o limiar configurado, não `+1 bloco` exato; conversão `(int)` de valor negativo trunca em direção a zero. Tipo index 15, Tier I, 0 mana da ficha anterior.
- **Risco:** `y` é campo de instância static singleton compartilhada pela registry; não provar simultaneidade/corrupção sem ensaio e rastreio do host. Nenhum perk de mobilidade muda esse filtro sem hook real.
- **Estado:** ✅ localização do source e IDs físicos; ⚠️ interleaving de contextos, config instalada, erros de validação e Survival/host QA em aberto; ⛔ hooks/adapters RPG não implementados ou testados. O Ars controla gramática, mana e retomadas.
