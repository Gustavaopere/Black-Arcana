# Thread of Depths

State: `SOURCE-PINNED 5.13.1 / RUNTIME QA PENDING`

Registry id: `ars_nouveau:thread_depths`  
Minimum slot: ONE (default)

## Respiração submersa

O behavior principal fica em mixin de `LivingEntity.decreaseAirSupply` e usa a **contagem total do perk no entity**, não apenas `slotValue` de uma peça.

`numDepths = PerkUtil.countForPerk(DepthsPerk.INSTANCE, entity)`

O decremento de ar é cancelado quando:

- `numDepths >= 3`; ou
- `random.nextDouble() <= numDepths * 0.33`.

Portanto, para contagens 1 e 2, o source implementa aproximadamente 33% e 66% de chance por chamada de preservar o ar; com 3+ preserva sempre. O catálogo não transforma essas probabilidades em duração média garantida.

## Swim Speed

`DepthsPerk.applyAttributeModifiers` usa o **valor do slot**. Se `slotValue >= 3`, adiciona a `NeoForgeMod.SWIM_SPEED`:

- amount: `2.0`
- operation: `ADD_VALUE`
- modifier id: `ars_nouveau:thread_depths`

Slots abaixo de 3 não adicionam esse modifier.

## Receita

Enchanting Apparatus:

- reagent: `ars_nouveau:blank_thread`
- pedestals: 3 × tag `minecraft:fishes`, 2 × `ars_nouveau:water_essence`, 1 × `minecraft:pufferfish`
- resultado: `ars_nouveau:thread_depths`
- `sourceCost`: 0

## Boundary

- Respiração e Swim Speed são Ars-owned.
- Não duplicar a proteção de ar como atributo/perk do RPG Skill Tree sem contrato explícito.
- Como a respiração usa contagem total enquanto Swim Speed usa slot value local, bridges não devem assumir que as duas escalas são equivalentes.

## QA pendente

1. Medir interação com Respiration e outros mixins/mods que alterem `decreaseAirSupply`.
2. Validar stacking do `SWIM_SPEED +2.0` quando múltiplas peças puderem carregar slot 3.
3. Confirmar comportamento com entidades/jogadores modificados por outros providers do pack.
