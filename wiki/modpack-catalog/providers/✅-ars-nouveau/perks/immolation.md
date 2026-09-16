# Thread of Immolation

State: `SOURCE-PINNED 5.13.1 / DESCRIPTION-PATH DIVERGENCE / RUNTIME QA PENDING`

Registry id: `ars_nouveau:thread_immolation`
Minimum slot: ONE (default)

## Efeito confirmado

`ImmolatePerk` participa de `SpellCastEvent` via `IEffectResolvePerk`.

Quando o caster está pegando fogo:

1. extingue o fogo;
2. aplica `ModPotions.IMMOLATE_EFFECT` por `20 * 5 = 100` ticks;
3. amplifier = `PerkUtil.countForPerk(thread_immolation, caster) - 1`.

Se o bloco no `blockPosition()` do caster está na tag vanilla `BlockTags.FIRE`, o código remove esse bloco sem drops e aplica o mesmo efeito de 5 segundos.

No `SpellDamageEvent.Pre`, Ars verifica se o damage source está em `DamageTypeTags.IS_FIRE` e o caster possui `IMMOLATE_EFFECT`; nesse caso adiciona:

`2 * (amplifier + 1)`

ao spell damage do evento.

## Divergência editorial

O texto provider-native diz que fire spells causam dano adicional **e duram mais** por nível de Immolation. No source checkpoint auditado, a busca pelo uso de `IMMOLATE_EFFECT` encontrou o bônus de dano em `ArsEvents`, mas não um path confirmado de extensão de duração. O catálogo não assume a segunda parte sem evidência/runtime QA.

## Receita

Enchanting Apparatus:

- reagent: `ars_nouveau:blank_thread`
- pedestals: 3 × `ars_nouveau:fire_essence`
- resultado: `ars_nouveau:thread_immolation`
- `sourceCost`: 0

## Boundary

- Ars é authority do perk count, `IMMOLATE_EFFECT` e `SpellDamageEvent`.
- Black Arcana não deve conceder dano adicional paralelo quando o mesmo fire spell já foi modificado pelo Ars.
- A remoção de fire block pertence ao provider e não deve ser tratada como precedente para ignorar `WorldEffectPolicy` em efeitos próprios.

## QA pendente

1. Verificar se algum path runtime não indexado aumenta duração de fire spells.
2. Validar comportamento quando caster está simultaneamente `isOnFire()` e sobre um bloco da tag FIRE.
3. Confirmar stacking de múltiplos threads e ordem com outros `SpellDamageEvent.Pre` modifiers.
