# Cloud of Regeneration — Iron's Spells 'n Spellbooks

## Estado
`PROVIDER-NATIVE / DEPRECATED NO DEFAULT CONFIG / SOURCE 3.16.3 AUDITADO`

## Identidade
- **ID:** `irons_spellbooks:cloud_of_regeneration`
- **Escola:** Holy
- **Raridade:** Common
- **Max level:** 5
- **Função:** cura contínua de aliados próximos
- **Deprecated:** `true` no `DefaultConfig`

## Custo e casting
- **Mana base:** 10
- **Mana/level:** +3
- **Cooldown:** 35 s
- **Cast time:** 200 ticks
- **Cast type:** Continuous
- **Spell power base:** 2
- **Spell power/level:** +1
- **Raio:** 5 blocos

## Efeito
Durante o cast, percorre living entities no raio e, para targets elegíveis via `Utils.shouldHealEntity`:

`healAmount = getSpellPower(level, caster) * 0.5`

Publica `SpellHealEvent` por cura e então aplica heal + partículas.

## Deduplicação
Mesmo deprecated, deve permanecer no catálogo histórico/semântico para não recriarmos a mesma mecânica por acidente. Uma nova habilidade só pode substituir este nicho deliberadamente, não por desconhecimento de que ele já existiu.
