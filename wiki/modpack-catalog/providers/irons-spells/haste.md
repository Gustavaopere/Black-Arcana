# Haste

- **Status no modpack:** PRESENTE — spell ativo no catálogo atual
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **Spell ID auditado:** `irons_spellbooks:haste`
- **JAR/versão:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Holy
- **Níveis:** 1–4
- **Raridade:** Epic → Legendary
- **Cast:** Long — 30 ticks auditados
- **Mana:** 50–80
- **Cooldown:** 80 s
- **Magical Haste público atual:** 20%
- **Duração pública atual:** 30–45 s

## O que faz

Aplica `Hastened` ao alvo aliado; sem alvo elegível, aplica no próprio caster. O efeito público aumenta movement speed, attack speed, mining speed e cast time reduction.

## Runtime auditado

O source 3.16.3 permite targeting de aliado até 32 blocos e usa self fallback. A duração é `spellPower * 20` ticks; o amplifier base é 7 e a percentagem final passa por `HastenedEffect.getPercentForAmplifier`.

## Deduplicação

Já ocupa buff Holy de haste/cadência. Uma bênção Celestial nova precisa afetar outra grandeza ou depender de uma infraestrutura/gate com função distinta.

## Fonte / evidência

- Catálogo oficial atual: `https://iron.wiki/spells/`.
- Auditoria source 3.16.3: `wiki/providers/irons-spellbooks/spells/holy/haste.md`.