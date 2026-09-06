# Blood Slash — Iron's Spells 'n Spellbooks

## Estado
`PROVIDER-NATIVE / SOURCE 3.16.3 AUDITADO / ECONOMIA HEMÁTICA FUTURA AINDA NÃO APLICADA`

## Identidade
- **ID:** `irons_spellbooks:blood_slash`
- **Escola:** Blood
- **Raridade:** Rare
- **Max level:** 5
- **Função:** projectile slash com lifesteal

## Custo atual
- **Mana base:** 25
- **Mana/level:** +5
- **Cooldown:** 10 s
- **Cast:** Instant
- **Spell power base:** 10
- **Spell power/level:** +1

## Efeito
Cria `BloodSlashProjectile` na posição dos olhos, dispara na direção do caster e usa:

`damage = spellPower`

Damage source com **15% lifesteal**.

## VFX/animação
`SLASH_ANIMATION`.

## Migração Blood
Somente o custo deve migrar para sangue mB/corpo/vínculo conforme contrato aprovado; projectile e settlement continuam provider-native quando possível.
