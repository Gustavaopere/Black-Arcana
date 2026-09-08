# Drygmy Familiar

State: `SOURCE-PINNED 5.13.1 / SOURCE-DESCRIPTION DIVERGENCE / RUNTIME QA PENDING`

Registry id: `ars_nouveau:familiar_drygmy`  
Conversion entity: Ars Nouveau `EntityDrygmy`  
Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Aquisição

O holder reconhece `EntityDrygmy`. Binding produz o Bound Script correspondente; o script desbloqueia o familiar no capability Ars.

## Behavior confirmado

### Earth spell modifier

`FamiliarDrygmy` implementa `ISpellCastListener`. Em `SpellModifierEvent`, quando o familiar está vivo, pertence ao caster e a spell part pertence à escola `ELEMENTAL_EARTH`, chama `event.builder.addDamageModifier(2.0f)`.

Há, porém, uma divergência importante no dispatcher comum: `FamiliarEvents` possui dois subscribers para `SpellModifierEvent` (`spellResolveEvent` e `modifierEvent`) e ambos encaminham o mesmo evento para todos os `ISpellCastListener`. O catálogo **não** conclui que o bônus runtime efetivo seja +4 sem QA; registra apenas que o source possui dois paths de dispatch aparentemente duplicados.

### Drygmy's Blessing / Looting

- A cada 60 ticks, o familiar aplica ao owner `ModPotions.LOOTING_EFFECT` por 600 ticks, amplifier 0.
- Esse efeito adiciona `+1.0` ao atributo Ars `PerkAttributes.DRYGMY`.
- O antigo path direto de `LootingLevelEvent` está comentado tanto no familiar quanto em `FamiliarEvents` com TODO para restaurá-lo.

Portanto, a descrição do livro — “chance to increase the amount of looting” — não é tratada como prova de um roll aleatório ativo no 5.13.1; o comportamento confirmado é o efeito/atributo acima.

## Authority e deduplicação

- Modificadores de Earth spell, `LOOTING_EFFECT` e `PerkAttributes.DRYGMY` pertencem ao Ars.
- Black Arcana/RPG Skill Tree não devem conceder um segundo +Earth damage ou Looting apenas porque um Drygmy familiar está ativo.
- Qualquer bridge futura precisa observar o `SpellModifierEvent`/atributo real e deduplicar o root cast.

## QA pendente

1. Medir o damage modifier efetivo em runtime devido aos dois subscribers de `SpellModifierEvent`.
2. Confirmar a semântica efetiva de `PerkAttributes.DRYGMY` no loot pipeline 5.13.1.
3. Confirmar que o antigo roll de Looting não está ativo por outro path não auditado.
