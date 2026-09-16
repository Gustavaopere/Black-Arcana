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
