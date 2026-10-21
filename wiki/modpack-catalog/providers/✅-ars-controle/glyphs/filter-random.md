# Filter: Random

State: `SOURCE-PINNED 1.6.15 / RUNTIME QA PENDING`

- Registry id: `ars_controle:glyph_filter_random`
- Kind: Filter
- Tier: I
- Base mana: 0
- Scribe XP: 27
- Recipe: `ars_nouveau:allow_scroll` + `ars_nouveau:glyph_randomize`

## Behavior

Base resolution probability is 50%.

For positive amplification `a`:

`chance = 1 - 0.5 / 2^a`

For dampening magnitude `d`:

`chance = 0.5 / 2^d`

The compatible augments are Amplify and Dampen, and Ars Controle overrides their mana contribution on this filter to 0.

The actual roll uses `ThreadLocalRandom.nextDouble() <= chance`. Randomness is provider-owned spell filtering; Black Arcana must not perform a second independent roll for the same Ars filter.

## Engenharia para perks — execução pinada à release 1.6.16

- **Source exato 1.6.16:** [FilterRandom.java](https://github.com/Vonr/Ars-Controle/blob/14c5f4770a9ec265491fb9a7ae1a60a2123dfbc0/src/main/java/dev/qther/ars_controle/spell/filter/FilterRandom.java), `Vonr/Ars-Controle@14c5f4770a9ec265491fb9a7ae1a60a2123dfbc0`. Registrado no JAR físico 1.6.16; *identidade binária* comprovada separadamente, execução ainda sem teste de equivalência de método a bytecode.
- **Fórmula:** `BASE_CHANCE=0.5`; `calculateChance(amps)` devolve `1-0.5/2^amps` para `amps>0`, `0.5/2^(-amps)` para `amps<0`, `0.5` para zero. Roll efetivo `ThreadLocalRandom.current().nextDouble()<=chance`; base 50%.
- **Lifecycle:** `onResolveBlock/Entity` chama `this.chance=calculateChance(stats.getAmpMultiplier())` antes do `super`. `chance` é campo mutável na instância única. Quando usado como filho de NOT/OR/XOR/XNOR, a preparação de chance vem das respectivas funções de parser e pode usar stats/augments de outra posição.
- **Recursos:** Amplify e Dampen compatíveis e com override de custo augment=0. Probabilidade não é alteração de damage/mana, e não se deve fazer novo roll para conceder Mastery/perk RPG. Reentrância e aleatoriedade requerem teste dirigido antes de permitir gating externo.
- **Estado:** ✅ localização do source e IDs físicos; ⚠️ interleaving de contextos, config instalada, erros de validação e Survival/host QA em aberto; ⛔ hooks/adapters RPG não implementados ou testados. O Ars controla gramática, mana e retomadas.
