# Whirlisprig Familiar

State: `SOURCE-PINNED 5.13.1 / RUNTIME QA PENDING`

Registry id: `ars_nouveau:familiar_whirlisprig`
Conversion entity: Ars Nouveau `Whirlisprig`
Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Aquisição

O holder reconhece `Whirlisprig`. Binding converte uma entidade elegível em Bound Script; usar o script desbloqueia o familiar no capability Ars.

## Behavior confirmado

### Redução de custo de Earth parts

`FamiliarWhirlisprig` escuta `SpellCostCalcEvent`. Para spells do owner, percorre cada spell part; quando a part pertence à escola `ELEMENTAL_EARTH`, soma `int(part.getCastingCost() * 0.5)` ao desconto e subtrai o total de `event.currentCost`.

Isto é mais preciso do que dizer genericamente “metade do custo da magia”: o desconto é calculado **por part Earth**, usando o casting cost de cada part e truncamento para `int`.

### Saturation

No `LivingEntityUseItemEvent.Finish` do owner, se o item possuir `FoodProperties`:

- lê `nutrition` e `saturation()`;
- calcula `satAmount = nutrition * saturationModifier * 2.0`;
- adiciona `satAmount * 0.4` ao `FoodData.saturationLevel`.

Equivalentemente, a adição observada no source é `nutrition * saturationModifier * 0.8`.

### Variante visual

Interação com stacks reconhecidos por `Whirlisprig.getColorFromStack` pode alterar a cor e consumir o item fora de creative/infinite materials.

## Authority e deduplicação

- Ars Nouveau é authority do `SpellCostCalcEvent`, mana cost e classificação `ELEMENTAL_EARTH`.
- Black Arcana não deve aplicar um segundo desconto de mana com base apenas no familiar ativo.
- O bônus de saturation deve permanecer ligado ao evento real de consumo do owner; não duplicar por tick ou por leitura posterior do FoodData.

## QA pendente

1. Confirmar custo final quando outros addons também alteram `SpellCostCalcEvent`.
2. Validar floor/zero behavior se descontos concorrentes reduzirem `currentCost` agressivamente.
3. Confirmar saturation resultante com foods de outros mods do pack.
