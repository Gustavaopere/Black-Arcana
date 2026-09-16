# Wither Skull — Iron's Spells 'n Spellbooks

## Estado
`PROVIDER-NATIVE / SOURCE 3.16.3 AUDITADO / ECONOMIA HEMÁTICA FUTURA AINDA NÃO APLICADA`

## Identidade
- **ID:** `irons_spellbooks:wither_skull`
- **Escola:** Blood
- **Raridade:** Uncommon
- **Max level:** 10
- **Função:** projectile ofensivo

## Custo atual
- **Mana base:** 20
- **Mana/level:** +2
- **Cooldown:** 1 s
- **Cast:** Instant
- **Spell power base:** 12
- **Spell power/level:** +1

## Efeito
Cria `WitherSkullProjectile` à frente do caster.

- `damage = spellPower * 0.5`;
- projectile speed = `(6 + spellLevel) * 0.08`;
- usa som vanilla `WITHER_SHOOT`.

A semântica adicional de impacto/wither pertence ao projectile e deve ser auditada antes de afirmar debuffs.

## Deduplicação
O fato de estar na escola Blood não torna o projétil fisiologicamente hemático. O catálogo separa **escola/provider** de **tipo real de recurso/efeito**.
