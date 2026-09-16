# Greater Heal — Iron's Spells 'n Spellbooks

## Estado
`PROVIDER-NATIVE / SOURCE 3.16.3 AUDITADO`

## Identidade
- **ID:** `irons_spellbooks:greater_heal`
- **Escola:** Holy
- **Raridade:** Rare
- **Max level:** 1
- **Função:** self-heal total preparado

## Custo e casting
- **Mana:** 100
- **Cooldown:** 45 s
- **Cast time:** 120 ticks
- **Cast type:** Long

## Efeito
`healAmount = caster.getMaxHealth()` e então `caster.heal(healAmount)`. Na prática tenta restaurar até a vida máxima, respeitando o comportamento de heal da entidade.

Publica `SpellHealEvent(caster, caster, healAmount, HOLY)` antes da cura e envia `HealParticlesPacket`.

## Deduplicação
Bloqueia um novo milagre cuja única função seja “full heal do caster”. Um Miracle-tier Divine precisa adicionar custo/fonte/gate/efeito contextual realmente diferente, sem replicar este resultado.
