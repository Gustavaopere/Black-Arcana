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

## Certificação técnica estática — Whirlisprig (2026-10-26)

**✅ `STATIC_TECHNICAL_CATALOG_ONLY` · ⛔ `mutating_hook=NOT_VERIFIED` · ⚠️ `physical_qa=NOT_TESTED`.** Ars Nouveau 5.13.1 JAR SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`; source `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`. **Prova binária de 109 IDs não inclui familiares.** [FamiliarWhirlisprig.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/familiar/FamiliarWhirlisprig.java), [WhirlisprigFamiliarHolder.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/familiars/WhirlisprigFamiliarHolder.java), [FamiliarEvents.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/event/FamiliarEvents.java).

| Eixo | Comportamento no source e gate de perk |
|---|---|
| Identidade | `WhirlisprigFamiliarHolder` aceita `Whirlisprig` e instancia `FamiliarWhirlisprig(ModEntities.ENTITY_FAMILIAR_SYLPH.get(),world)`. Na declaração de `ModEntities`, esta constante registra `LibEntityNames.FAMILIAR_WHIRLISPRIG`; não inferir mod ID “sylph” do nome da variável. |
| Earth mana discount | `onCostCalc(SpellCostCalcEvent)` exige `isAlive()` e owner igual a `event.context.getUnwrappedCaster()`; percorre `event.context.getSpell().recipe()`. Para cada part de `SpellSchools.ELEMENTAL_EARTH`, acumula `(int)(part.getCastingCost()*0.5)`, depois executa `event.currentCost -= discount`. **O truncamento ocorre por spell part**, e não há clamp de custo nesta classe. Não equivale a 50% da magia completa. |
| Saturação | `FamiliarEvents.eatEvent(LivingEntityUseItemEvent.Finish)` encaminha ao familiar. Em servidor, se owner consumiu item com `FoodProperties`, calcula `satAmount=nutrition*saturationModifier*2.0f`, soma diretamente `satAmount*0.4f` a `player.getFoodData().saturationLevel` ⇒ acréscimo algébrico `nutrition*saturationModifier*0.8`; **sem clamp explícito no método**. Não atribuir mana/XP ao bônus de comida. |
| Aparência | `interactAt` em servidor/mão principal usa `Whirlisprig.getColorFromStack(stack)`, `setColor(color)` e `stack.shrink(1)` se não infinite. **O método não checa explicitamente se o player é owner no branch de cor**, então comportamento multiplayer exige QA. |
| Autoridade e vida | `FamiliarEntity` mantém owner/holder NBT e termina quando owner ausente em checagem a cada 20 ticks; `FamiliarEvents.maxManaCalc` inclui reserva base 0.15 no primeiro familiar qualificado. Ars controla mana e cost events; RPG Skill Tree/Black Arcana não podem reaplicar desconto/saturação ou consumir casting event outra vez sem adapter comprovado. `WorldEffectPolicy` cobre somente efeitos próprios BA. |

**QA:** custo com addons e floor/zero, saturação real de foods modded, evento concorrente/cliente, color por não-owner, relog e parâmetros de mana; `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`.

## Geometria e atributos de entidade no source

O `EntityType.Builder` do familiar declara `.sized(0.5f,0.5f)` (largura × altura) e `.setTrackingRange(10)`. O tracking declarado não é alcance de habilidade. [Registros e dimensões](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/setup/registry/ModEntities.java#L197-L210).

`FamiliarEntity.attributes()` fornece defaults `MAX_HEALTH=100`, `MOVEMENT_SPEED=0.2` e `FOLLOW_RANGE=16`; a criação dos atributos registra essa base para os seis tipos. Velocidade efetiva e distância de ação dependem dos consumidores/IA. [Base](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/familiar/FamiliarEntity.java#L206-L209) · [registro de atributos](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/setup/registry/ModEntities.java#L369-L375). O [contrato compartilhado](../FAMILIAR-STATIC-SIX-5.13.1.md) distingue esses parâmetros de raios de efeito, reserva de mana e evidência binária.
