# Filter: Below

State: `SOURCE-PINNED 1.6.15 / RUNTIME QA PENDING`

- Registry id: `ars_controle:glyph_filter_below`
- Kind: Filter
- Tier: I
- Base mana: 0
- Scribe XP: 27
- Recipe: `ars_nouveau:allow_scroll` + `minecraft:cobbled_deepslate`

## Behavior

The filter snapshots its comparison Y from `caster position Y - 1`, cast to integer, then permits resolution only when the target's integer Y compares below that value.

The exact integer conversion and `-1` offset are source facts; the catalog does not normalize them to a looser geometric interpretation.

## Engenharia para perks — execução pinada à release 1.6.16

- **Source exato 1.6.16:** [FilterYLevel.java](https://github.com/Vonr/Ars-Controle/blob/14c5f4770a9ec265491fb9a7ae1a60a2123dfbc0/src/main/java/dev/qther/ars_controle/spell/filter/FilterYLevel.java), `Vonr/Ars-Controle@14c5f4770a9ec265491fb9a7ae1a60a2123dfbc0`. Registrado no JAR físico 1.6.16; *identidade binária* comprovada separadamente, execução ainda sem teste de equivalência de método a bytecode.
- **Predicado:** `FilterYLevel.BELOW`, `comparison=-1`; só passa quando `Integer.compare(targetY,(int)(casterPositionY-1))==-1`. Bloco usa `getBlockPos().getY()`; entidade `(int)position().y`.
- **Referencial:** compara nível inteiro com `(int)(casterPosition.y-1)`, não Y absoluto 0 ou distância vertical. O getter depende do contexto de resolução atual; `y` é mantido em instância singleton e sobrescrito por chamadas.
- **Perks:** mirar abaixo não concede licença para chunk scan/teleporte; ❌ sem API de offset vertical personalizada, não alterar predicado.
- **Estado:** ✅ localização do source e IDs físicos; ⚠️ interleaving de contextos, config instalada, erros de validação e Survival/host QA em aberto; ⛔ hooks/adapters RPG não implementados ou testados. O Ars controla gramática, mana e retomadas.
