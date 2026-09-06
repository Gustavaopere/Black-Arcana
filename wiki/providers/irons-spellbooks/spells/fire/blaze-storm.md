# Blaze Storm — Iron's Spells 'n Spellbooks

## Estado
`PROVIDER-NATIVE / SOURCE 3.16.3 AUDITADO`

## Identidade
- **ID:** `irons_spellbooks:blaze_storm`
- **Escola:** Fire
- **Raridade:** Common
- **Max level:** 10
- **Função:** barrage contínua de pequenas fireballs

## Custo e casting
- mana base 5; +1/level;
- cooldown 20 s;
- spell power 5 +1/level;
- cast type Continuous;
- cast duration = `55 + 5*level` ticks.

## Efeito
A cada 5 ticks de janela lança `SmallMagicFireball`.

`damagePerProjectile = spellPower * 0.4`

Damage source: 40 fire ticks e i-frames `0`.

## Deduplicação Infernal
Bloqueia barrage contínua genérica de fire projectiles.
