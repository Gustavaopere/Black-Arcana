# Thread of the Starbuncle

State: `SOURCE-PINNED 5.13.1 / RUNTIME QA PENDING`

Registry id: `ars_nouveau:thread_starbuncle`
Minimum slot: ONE (default)

## Efeito confirmado

`applyAttributeModifiers` adiciona a `Attributes.MOVEMENT_SPEED` um modifier com:

- amount: `0.2 * slotValue`
- operation: `ADD_MULTIPLIED_TOTAL`
- id do modifier: o próprio registry id do perk.

Assim, o source representa +20% por valor do slot onde o perk foi instalado; o catálogo não converte isso em uma regra genérica de “nível do jogador”.

## Receita

Enchanting Apparatus:

- reagent: `ars_nouveau:blank_thread`
- pedestals: 3 × `ars_nouveau:starbuncle_shards`, 3 × `minecraft:sugar`, 2 × `ars_nouveau:manipulation_essence`
- resultado: `ars_nouveau:thread_starbuncle`
- `sourceCost`: 0

## Boundary

O modifier é um armor Thread do Ars. Não deve ser duplicado pelo RPG Skill Tree nem somado novamente por uma bridge ao detectar o mesmo equipamento.

## QA pendente

Validar stacking final com múltiplas peças/slots e outros modifiers de Movement Speed no modpack real.
