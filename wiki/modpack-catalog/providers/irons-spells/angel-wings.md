# Angel Wings

- **Status no modpack:** PRESENTE — spell ativo no catálogo atual
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **Spell ID auditado:** `irons_spellbooks:angel_wing`
- **JAR/versão:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Holy
- **Níveis:** 1–5
- **Raridade:** Legendary
- **Cast:** Instant
- **Mana:** 80–160
- **Cooldown:** 120 s
- **Duração pública atual:** 10–50 s

## O que faz

Aplica asas de energia Holy ao caster; o efeito funciona como uma elytra temporária.

## Runtime auditado

A auditoria source 3.16.3 confirma `AngelWingsSpell`, spell power base 10 com +10/level e duração `getSpellPower * 20` ticks. O cast aplica `MobEffectRegistry.ANGEL_WINGS` ao próprio caster.

## VFX

O source auditado cria 35 partículas `WISP` em padrão swirling ao redor do caster. A aparência final em conjunto com resource packs/EFIS no modpack real permanece sujeita à validação visual.

## Deduplicação

Já ocupa o nicho de asas/voo Holy temporário. Uma futura expansão Celestial/Holy não deve criar outro voo genérico; qualquer mobilidade nova precisa de delta real, como condição de Sanctum, resgate de aliado ou traversal contextual.

## Fonte / evidência

- Catálogo oficial atual: `https://iron.wiki/spells/` — consulta em 2026-09-06.
- Auditoria source 3.16.3: `wiki/providers/irons-spellbooks/spells/holy/angel-wing.md`.