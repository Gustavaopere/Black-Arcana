# Wisp — Iron's Spells 'n Spellbooks

## Estado
`PROVIDER-NATIVE / SOURCE 3.16.3 AUDITADO`

## Identidade
- **ID:** `irons_spellbooks:wisp`
- **Escola:** Holy
- **Raridade:** Common
- **Max level:** 10
- **Função:** entidade/projétil Holy orientado a target

## Custo e casting
- **Mana base:** 15
- **Mana/level:** +2
- **Cooldown:** 3 s
- **Cast time:** 20 ticks
- **Cast type:** Long
- **Spell power base:** 5
- **Spell power/level:** +1
- **Target helper:** 48 blocos

## Efeito
Com target válido, cria `WispEntity(world, caster, spellPower)`, associa o alvo e posiciona o wisp à frente do caster.

O tooltip expõe o spell power como dano. A liquidação exata de impacto/perseguição pertence à `WispEntity` e deve ser auditada separadamente antes de afirmar fórmulas adicionais.

## Deduplicação
Bloqueia outro orbe/wisp Holy teleguiado sem diferença mecânica.
