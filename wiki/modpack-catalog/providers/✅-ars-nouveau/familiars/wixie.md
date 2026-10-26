# Wixie Familiar

State: `SOURCE-PINNED 5.13.1 / RUNTIME QA PENDING`

Registry id: `ars_nouveau:familiar_wixie`
Conversion entity: Ars Nouveau `EntityWixie`
Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Aquisição

O holder reconhece `EntityWixie`. Binding converte a entidade em Bound Script e o uso do script desbloqueia o familiar no capability Ars.

## Behavior confirmado

### Extensão de duração de efeitos

`FamiliarWixie` recebe `MobEffectEvent.Added` via `FamiliarEvents`. Quando o familiar está vivo:

- se o alvo é o owner e o efeito adicionado é beneficial; **ou**
- se o applier do efeito é o owner,

então o código aumenta a duração do `MobEffectInstance` em `duration / 5`, isto é, +20% usando divisão inteira.

A condição “applier is owner” não restringe o efeito a beneficial, então o path pode aumentar também efeitos prejudiciais aplicados pelo owner.

### Reagentes de poção

Ao interagir com o familiar usando um item que seja ingrediente de uma `BrewingRecipe` cujo input aceite Water Potion ou Awkward Potion, o familiar:

- obtém o output da receita;
- aplica o `PotionContents` diretamente ao owner;
- consome 1 ingrediente fora de creative/infinite materials;
- emite mensagem/efeito visual provider-native.

Isto corresponde a aplicar o resultado básico/tier-1 da receita encontrada; o catálogo não presume ordem quando múltiplas receitas aceitarem o mesmo ingrediente sem QA.

### Debuff de combate

`DebuffTargetGoal` pode atuar quando há target e `debuffCooldown <= 0`:

- escolhe aleatoriamente entre Slowness, Weakness, Levitation e Poison;
- se escolher Poison contra alvo com `isInvertedHealAndHarm()`, troca para Regeneration;
- duração: `7 * 20 = 140` ticks;
- amplifier aleatório 0 ou 1;
- após aplicar, define cooldown `150` ticks.

## Authority e deduplicação

- Potion recipe enumeration, effect duration mutation e debuff AI pertencem ao Ars.
- Black Arcana não deve reaplicar +20% de duração nem duplicar o debuff porque detectou o familiar por proximidade.
- Qualquer integração deve observar o evento real e preservar o applier/origin do efeito.

## QA pendente

1. Validar interação com receitas de brewing adicionadas por outros mods.
2. Confirmar comportamento quando múltiplas recipes aceitam o mesmo ingrediente.
3. Validar stacking/order do +20% com outros duration modifiers do pack.

## Certificação técnica estática — Wixie (2026-10-26)

**✅ `STATIC_TECHNICAL_CATALOG_ONLY` · ⛔ `mutating_hook=NOT_VERIFIED` · ⚠️ `physical_qa=NOT_TESTED`.** Ars Nouveau 5.13.1 JAR SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`; upstream `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`. **Os 109 IDs binários auditados não abrangem familiars.** [FamiliarWixie.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/familiar/FamiliarWixie.java), [WixieFamiliarHolder.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/familiars/WixieFamiliarHolder.java), [FamiliarEvents.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/event/FamiliarEvents.java), [FamiliarEntity.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/familiar/FamiliarEntity.java).

| Campo | Consumidor real e limite |
|---|---|
| Registry/holder | `WixieFamiliarHolder` converte `EntityWixie`, instancia `FamiliarWixie(ModEntities.ENTITY_FAMILIAR_WIXIE.get(),world)`, e configura dados de owner/holder no ciclo de invocação. |
| Brewing reagents | `mobInteract` requer servidor/mão principal; se não dye, itera `ArsNouveauAPI.getInstance().getAllPotionRecipes(level())`. Para `BrewingRecipe` com `r.isIngredient(stack)` e `r.getInput().test(Potions.AWKWARD)` ou `Potions.WATER`, lê `PotionContents`, aplica `PotionUtil.applyContents(contents,player,player,player)`, envia mensagem/partículas/animação e consome 1 stack quando não infinite. **O resultado é aplicado ao player que interagiu; o método não checa owner explicitamente e não há check `player.equals(getOwner())`**; ordem quando receitas conflitam e autorização multiplayer exigem QA. |
| Added duration | `FamiliarEvents.potionEvent` encaminha `MobEffectEvent.Added` a `potionEvent`. Se alvo é owner e o efeito é beneficial, **ou** applier é owner, executa `effect.duration += effect.duration/5`. O segundo branch não exige beneficial; pode incluir harmful. Percentual é acréscimo inteiro, **não garantia de 1.2x ao final da cadeia de outros modifiers**. |
| Debuffs em combate | `DebuffTargetGoal.canUse` exige `debuffCooldown<=0` e alvo existente; tick escolhe dentre `MOVEMENT_SLOWDOWN`, `WEAKNESS`, `LEVITATION`, `POISON`, trocando Poison por `REGENERATION` quando alvo `isInvertedHealAndHarm()`. Duração `7*20=140` ticks, amplifier 0/1, depois `debuffCooldown=150` ticks; contador decrementado a cada tick servidor em `FamiliarWixie.tick`. Return de `target.addEffect` não verificado antes de cooldown/packet. |
| Persistência e gates | `debuffCooldown` não é serializado explicitamente por `FamiliarWixie` nem no `FamiliarEntity.addAdditionalSaveData` inspecionado; **não presumir cooldown preservado entre unload/recreate**. Dados `ownerID/holderID/terminated/name/color/cosmetic` pertencem ao Ars. `WorldEffectPolicy` BA não intercepta `MobEffectEvent.Added` nem a IA Wixie; RPG Skill Tree só atributos/perks/Mastery por boundary real. |

**QA:** bytecode dos métodos, não-owner potion, recipes modded, duração duplicada por listeners e addons, troca Poison→Regeneration, spawn/target e save/reload de cooldown, multiplayer. `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`. Sem Stage alterado.
