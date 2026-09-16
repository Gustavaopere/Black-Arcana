# Acupuncture — Iron's Spells 'n Spellbooks

## Estado
`PROVIDER-NATIVE / SOURCE 3.16.3 AUDITADO / ECONOMIA HEMÁTICA FUTURA AINDA NÃO APLICADA`

## Identidade
- **ID:** `irons_spellbooks:acupuncture`
- **Escola:** Blood
- **Raridade:** Rare
- **Max level:** 10
- **Função:** barrage circular de blood needles sobre alvo

## Custo atual do provider
- **Mana base:** 25
- **Mana/level:** +5
- **Cooldown:** 20 s
- **Cast:** Instant
- **Target:** até 32 blocos
- **Spell power base:** 1
- **Spell power/level:** 0

## Efeito
`count = (int)((4 + level) * spellPower)`

`damagePerNeedle = 1 + spellPower`

Cria BloodNeedles ao redor do alvo e dispara radialmente para o centro.

## Migração Blood
O custo acima é mana nativa. A política futura do pack exige **zero mana normal** para Blood; portanto este spell precisa de adapter/cost override explícito para sangue mB/linked blood, mantendo o efeito provider-native.
