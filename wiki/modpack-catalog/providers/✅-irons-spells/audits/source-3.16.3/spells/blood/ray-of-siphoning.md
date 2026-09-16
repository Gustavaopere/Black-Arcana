# Ray of Siphoning — Iron's Spells 'n Spellbooks

## Estado
`PROVIDER-NATIVE / SOURCE 3.16.3 AUDITADO / ECONOMIA HEMÁTICA FUTURA AINDA NÃO APLICADA`

## Identidade
- **ID:** `irons_spellbooks:ray_of_siphoning`
- **Escola:** Blood
- **Raridade:** Common
- **Max level:** 10
- **Função:** ray contínuo de dano + lifesteal integral

## Custo atual
- **Mana base:** 8
- **Mana/level:** +1
- **Cooldown:** 15 s
- **Cast time:** 100 ticks
- **Cast type:** Continuous
- **Spell power base:** 4
- **Spell power/level:** +1
- **Range:** 12 blocos

## Efeito
A cada settlement do cast:

`tickDamage = spellPower * 0.25`

O raycast respeita blocos e `Utils.canHitWithRaycast`. Em hit confirmado, usa damage source:

- **lifestealPercent = 1.0 (100%)**;
- `indirect()`.

Em dano confirmado envia `BloodSiphonParticlesPacket(target → caster)`.

## Deduplicação
Já ocupa o nicho de siphon/drain contínuo no provider. Sanguine Harvest do Black Arcana continua distinto pelo contrato de pulse bounded/anti-farm/settlement, mas qualquer novo beam de dreno deve ser comparado contra ambos.

## Migração Blood
O custo atual é mana. A futura economia substitui por sangue real/reservatório/vínculo; lifesteal recebido não deve automaticamente virar mB sem uma regra explícita de conversão, para evitar geração circular/infinita.
