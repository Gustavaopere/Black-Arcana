# Thread of High Step

State: `SOURCE-PINNED 5.13.1 / RUNTIME QA PENDING`

Registry id: `ars_nouveau:thread_high_step`  
Minimum slot: ONE (default)

## Efeito confirmado

Adiciona a `Attributes.STEP_HEIGHT`:

- amount: `slotValue`
- operation: `ADD_VALUE`
- modifier id: `ars_nouveau:thread_high_step`

Portanto um slot de valor 1/2/3 adiciona respectivamente +1/+2/+3 ao Step Height através do modifier do item.

## Receita

Enchanting Apparatus:

- reagent: `ars_nouveau:blank_thread`
- pedestals: 3 × `ars_nouveau:air_essence`
- resultado: `ars_nouveau:thread_high_step`
- `sourceCost`: 0

## Boundary

Esse Step Height é um modifier de atributo provider-native do equipamento Ars; não deve gerar um segundo aumento no RPG Skill Tree/Black Arcana.

## QA pendente

Validar stacking com outros providers de Step Height e comportamento em obstáculos/modded blocks do pack.
