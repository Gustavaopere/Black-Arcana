# Haste — Iron's Spells 'n Spellbooks

## Estado
`PROVIDER-NATIVE / SOURCE 3.16.3 AUDITADO`

## Identidade
- **ID:** `irons_spellbooks:haste`
- **Escola:** Holy
- **Raridade:** Epic
- **Max level:** 4
- **Função:** buff de velocidade/cadência via `HASTENED`

## Custo e casting
- **Mana base:** 50
- **Mana/level:** +10
- **Cooldown:** 80 s
- **Cast time:** 30 ticks
- **Cast type:** Long
- **Spell power base:** 30
- **Spell power/level:** +5
- **Targeting:** aliado até 32 blocos; se nenhum alvo elegível for encontrado, seleciona o próprio caster.

## Efeito
Aplica `MobEffectRegistry.HASTENED`.

- **duração:** `spellPower * 20` ticks;
- **amplifier base:** 7, escalado pelo entity power multiplier;
- a percentagem final é resolvida por `HastenedEffect.getPercentForAmplifier`.

## Deduplicação
Bloqueia outro buff Divine genérico de haste. Uma bênção celestial futura precisa afetar outra grandeza ou depender de Sanctum/Ressonância com função distinta.
