# Blessing Of Life

- **Status no modpack:** PRESENTE — ativo no catálogo atual
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **Spell ID:** `irons_spellbooks:blessing_of_life`
- **JAR/versão:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Holy
- **Níveis:** 1–10
- **Raridade:** Common → Legendary
- **Cast:** Long
- **Cast time auditado:** 30 ticks
- **Mana:** 10–55
- **Cooldown:** 10 s
- **Cura atual:** 6–15
- **Target helper auditado:** até 64 blocos

## O que faz

Seleciona uma criatura e, ao completar o cast, cura o alvo.

## Source audit 3.16.3

- spell power: base 6, +1/level;
- com `TargetEntityCastData` válido: `healAmount = getSpellPower(level, caster)`;
- publica `SpellHealEvent(caster, target, healAmount, HOLY)` antes da cura;
- aplica a cura e envia `HealParticlesPacket`.

## Deduplicação / causalidade

Já cobre cura Holy de alvo único. O `SpellHealEvent` é o hook causal preferível para integrações; não inferir uma segunda cura por diferença de HP nem executar settlement paralelo.

## Fonte / evidência

- Catálogo oficial atual: `https://iron.wiki/spells/`
- Source audit canônico: `wiki/providers/irons-spellbooks/spells/holy/blessing-of-life.md`
- Consulta: 2026-09-06.
