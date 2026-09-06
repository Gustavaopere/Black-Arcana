# Planar Sight — Iron's Spells 'n Spellbooks

## Estado

`PROVIDER-NATIVE / SOURCE AUDITADO`

## Identidade

- **ID:** `irons_spellbooks:planar_sight`
- **Escola:** Eldritch
- **Raridade mínima:** Legendary
- **Max level:** 3
- **Função:** perception / planar vision

## Custo e casting

- **Mana base:** 150
- **Mana por nível:** +50
- **Cooldown:** 200 s
- **Cast:** Instant
- **Spell power base:** 40
- **Spell power/level:** +20
- **Duração:** `spellPower * 20` ticks

## Efeito

Aplica `MobEffectRegistry.PLANAR_SIGHT` ao caster pelo tempo derivado de spell power.

## Deduplicação

Qualquer Divination de Ordem/Divina/Witchcraft precisa demonstrar delta contra Planar Sight.

`Olho da Convergência` continua válido apenas se sua saída for **fate/probability/trajectory/prediction telemetry** e não simplesmente “ver entidades/coisas ocultas em outro plano”.

`Busca por Vestígio` de Witchcraft também permanece distinta se usar objeto-foco e rastreamento causal de uma identidade, em vez de percepção planar genérica.

## Fonte técnica

`PlanarSightSpell.java`, Iron's branch 1.21 / 3.16.3.
