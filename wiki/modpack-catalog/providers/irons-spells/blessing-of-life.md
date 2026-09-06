# Blessing Of Life

- **Status no modpack:** PRESENTE — spell ativo no catálogo atual
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **Spell ID auditado:** `irons_spellbooks:blessing_of_life`
- **JAR/versão:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Holy
- **Níveis:** 1–10
- **Raridade:** Common → Legendary
- **Cast:** Long — 30 ticks auditados
- **Mana:** 10–55
- **Cooldown:** 10 s
- **Cura pública atual:** 6–15
- **Target helper auditado:** até 64 blocos

## O que faz

Seleciona uma criatura-alvo e, ao completar a conjuração, aplica cura Holy a ela.

## Runtime e causalidade auditados

O source 3.16.3 resolve `healAmount = getSpellPower(level, caster)`, publica `SpellHealEvent(caster, target, healAmount, HOLY)` antes da cura e então cura o alvo. Esse evento é o hook preferencial para qualquer integração Black Arcana/RPG que precise provar qual cast/provider gerou a cura.

## VFX

O runtime auditado distribui `HealParticlesPacket`. Aparência final no cliente real do pack permanece sujeita à matriz visual.

## Deduplicação

Já cobre cura Holy direcionada de alvo único. Uma nova magia Celestial não ganha delta por apenas curar mais ou trocar VFX.

## Fonte / evidência

- Catálogo oficial atual: `https://iron.wiki/spells/`.
- Auditoria source 3.16.3: `wiki/providers/irons-spellbooks/spells/holy/blessing-of-life.md`.