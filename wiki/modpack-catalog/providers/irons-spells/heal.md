# Heal

- **Status no modpack:** PRESENTE — spell ativo no catálogo atual
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **Spell ID auditado:** `irons_spellbooks:heal`
- **JAR/versão:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Holy
- **Níveis:** 1–8
- **Raridade:** Uncommon → Legendary
- **Cast:** Instant
- **Mana:** 30–135
- **Cooldown:** 30 s
- **Cura pública atual:** 5–12

## O que faz

Infunde o próprio caster com energia Holy e recupera vida imediatamente.

## Runtime e causalidade auditados

O source 3.16.3 usa `healAmount = getSpellPower(level, caster)` e publica `SpellHealEvent(caster, caster, healAmount, HOLY)` antes de chamar `entity.heal`. Para perks/telemetria causais, esse evento deve ser preferido a inferir cura por delta de HP.

## VFX / animação

A auditoria registra círculo de 16 partículas `HEART` e `SELF_CAST_ANIMATION`.

## Deduplicação

Já ocupa self-heal Holy instantâneo. Uma nova cura não é gap por alterar apenas magnitude, cor ou nome.

## Fonte / evidência

- Catálogo oficial atual: `https://iron.wiki/spells/`.
- Auditoria source 3.16.3: `wiki/providers/irons-spellbooks/spells/holy/heal.md`.