# Greater Heal

- **Status no modpack:** PRESENTE — spell ativo no catálogo atual
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **Spell ID auditado:** `irons_spellbooks:greater_heal`
- **JAR/versão:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Holy
- **Nível:** 1
- **Raridade:** Rare
- **Cast:** Long — 120 ticks auditados
- **Mana:** 100
- **Cooldown:** 45 s
- **Cura pública:** Max Healing

## O que faz

É uma cura própria preparada e lenta que tenta restaurar completamente o caster.

## Runtime e causalidade auditados

O source 3.16.3 calcula `healAmount = caster.getMaxHealth()` e executa `caster.heal(healAmount)`. Antes da cura publica `SpellHealEvent(caster, caster, healAmount, HOLY)` e envia `HealParticlesPacket`.

## Deduplicação

Já ocupa o resultado “full self-heal”. Um Miracle-tier Holy não deve existir apenas como Greater Heal mais forte; precisa de custo, gate, condição e consequência realmente diferentes.

## Fonte / evidência

- Catálogo oficial atual: `https://iron.wiki/spells/`.
- Auditoria source 3.16.3: `wiki/providers/irons-spellbooks/spells/holy/greater-heal.md`.