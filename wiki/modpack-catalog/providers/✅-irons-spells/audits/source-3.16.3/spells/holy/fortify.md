# Fortify — Iron's Spells 'n Spellbooks

## Estado
`PROVIDER-NATIVE / SOURCE 3.16.3 AUDITADO`

## Identidade
- **ID:** `irons_spellbooks:fortify`
- **Escola:** Holy
- **Raridade:** Common
- **Max level:** 10
- **Função:** defesa/absorção de grupo

## Custo e casting
- **Mana base:** 80
- **Mana/level:** +10
- **Cooldown:** 180 s
- **Cast time:** 60 ticks
- **Cast type:** Long
- **Spell power base:** 6
- **Spell power/level:** +1
- **Raio:** 8 blocos

## Efeito
Para living entities elegíveis via `Utils.shouldHealEntity` dentro de 8 blocos:

- aplica `MobEffectRegistry.FORTIFY` por `20*120 = 2400 ticks` (120 s);
- amplifier = `(int)getSpellPower - 1`;
- o efeito representa a quantidade de absorção indicada pelo tooltip do provider.

O pre-cast mostra `TargetedAreaEntity` de raio 8.

## VFX
`AbsorptionParticlesPacket` por alvo + `FortifyAreaParticlesPacket` na área.

## Deduplicação
Bloqueia outra bênção Divine cujo único efeito seja absorção/fortificação de aliados em área.
