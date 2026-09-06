# Blood Needles — Iron's Spells 'n Spellbooks

## Estado
`PROVIDER-NATIVE / SOURCE 3.16.3 AUDITADO / ECONOMIA HEMÁTICA FUTURA AINDA NÃO APLICADA`

## Identidade
- **ID:** `irons_spellbooks:blood_needles`
- **Escola:** Blood
- **Raridade:** Uncommon
- **Max level:** 10
- **Função:** volley de cinco projéteis com lifesteal

## Custo atual
- **Mana base:** 25
- **Mana/level:** +5
- **Cooldown:** 10 s
- **Cast:** Instant
- **Spell power base:** 8
- **Spell power/level:** +1

## Efeito
- projectile count fixo: 5;
- `damagePerNeedle = spellPower * 0.25`;
- raycast de referência: 32 blocos;
- damage source: **25% lifesteal**;
- i-frames configurados para `0` no damage source.

## Migração Blood
Substituir apenas a camada de custo por sangue válido. Não duplicar projectile/damage/lifesteal em runtime Black Arcana se o provider puder continuar executando o spell.
