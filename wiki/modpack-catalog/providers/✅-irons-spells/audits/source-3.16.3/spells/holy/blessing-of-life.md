# Blessing of Life — Iron's Spells 'n Spellbooks

## Estado
`PROVIDER-NATIVE / SOURCE 3.16.3 AUDITADO`

## Identidade
- **ID:** `irons_spellbooks:blessing_of_life`
- **Escola:** Holy
- **Raridade:** Common
- **Max level:** 10
- **Função:** cura direcionada de aliado/alvo

## Custo e casting
- **Mana base:** 10
- **Mana/level:** +5
- **Cooldown:** 10 s
- **Cast time:** 30 ticks
- **Cast type:** Long
- **Spell power base:** 6
- **Spell power/level:** +1
- **Target helper:** até 64 blocos

## Efeito
Com `TargetEntityCastData` válido:

`healAmount = getSpellPower(level, caster)`

Publica `SpellHealEvent(caster, target, healAmount, HOLY)`, cura o alvo e distribui `HealParticlesPacket`.

## Deduplicação
Bloqueia nova cura Divine de alvo único sem delta. Também fornece hook canônico para perks de cura Holy quando a causalidade do cast for necessária.
