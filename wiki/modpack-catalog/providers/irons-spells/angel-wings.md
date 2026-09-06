# Angel Wings

- **Status no modpack:** PRESENTE — ativo no catálogo atual
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **Spell ID:** `irons_spellbooks:angel_wing`
- **JAR/versão:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Holy
- **Níveis:** 1–5
- **Raridade atual:** Legendary
- **Cast:** Instant
- **Mana atual:** 80–160
- **Cooldown:** 120 s
- **Duração atual:** 10–50 s

## O que faz

Aplica asas de energia sagrada ao caster, funcionando como uma elytra temporária.

## Source audit 3.16.3

- classe: `AngelWingsSpell`;
- spell power: base 10, +10/level;
- duração: `getSpellPower * 20` ticks;
- aplica `MobEffectRegistry.ANGEL_WINGS` ao caster;
- VFX auditado: 35 partículas `WISP` em padrão swirling.

A duração derivada do source corresponde ao balance atual 10–50 s. O changelog atual também registra cast effects adicionados em 3.16.2.

## Deduplicação

Já cobre voo/asas Holy temporários. Uma futura mobilidade Celestial/Divine precisa de diferença mecânica real — por exemplo resgate de aliados, ascensão contextual ou traversal ligado a Sanctum — e não apenas novas asas/VFX.

## Fonte / evidência

- Catálogo oficial atual: `https://iron.wiki/spells/`
- Changelog oficial: `https://iron.wiki/changelog/`
- Source audit canônico: `wiki/providers/irons-spellbooks/spells/holy/angel-wing.md`
- Consulta: 2026-09-06.
