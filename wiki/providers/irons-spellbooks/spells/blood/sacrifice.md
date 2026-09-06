# Sacrifice — Iron's Spells 'n Spellbooks

## Estado
`PROVIDER-NATIVE / SOURCE 3.16.3 AUDITADO / ECONOMIA HEMÁTICA FUTURA AINDA NÃO APLICADA`

## Identidade
- **ID:** `irons_spellbooks:sacrifice`
- **Escola:** Blood
- **Raridade:** Rare
- **Max level:** 5
- **Função:** sacrifica summon mágico próprio para explosão

## Custo atual
- **Mana base:** 25
- **Mana/level:** +5
- **Cooldown:** 1 s
- **Cast:** Instant
- **Spell power base:** 2
- **Spell power/level:** +1
- **Target range:** 25 blocos

## Gate de alvo
O pre-cast só aceita entidade que:
- implemente `IMagicSummon`;
- tenha `summon.getSummoner() == caster`.

## Efeito
No cast revalida ownership e então:

`explosionDamage = getDamage(level,caster) + summon.currentHealth * 0.5`

onde:

`getDamage = (10 + spellPower) * SUMMON_DAMAGE_attribute`

Raio:

`radius = 3 * (1 + 0.5 * summonHealth/summonMaxHealth)`

A explosão aplica falloff cúbico e exige line of sight. Depois o summon é removido com `RemovalReason.KILLED`.

## Deduplicação
Já ocupa o arquétipo de “sacrificar servo para poder explosivo”. Constantine/Infernal/Witchcraft não devem adicionar outra versão igual por estética.

## Migração Blood
O próprio **summon sacrificado não é automaticamente uma fonte de sangue**. O custo de lançamento futuro deve ser resolvido pela economia hemática separadamente; sacrificar um Iron Golem/construct summon não o transforma em `HEMATIC_BLOOD`.
