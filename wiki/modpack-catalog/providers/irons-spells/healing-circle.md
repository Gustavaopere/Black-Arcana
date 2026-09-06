# Healing Circle

- **Status no modpack:** PRESENTE — ativo no catálogo atual
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **Spell ID:** `irons_spellbooks:healing_circle`
- **JAR/versão:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Holy
- **Níveis:** 1–10
- **Raridade:** Common → Legendary
- **Cast:** Long
- **Cast time auditado:** 20 ticks
- **Mana:** 40–130
- **Cooldown:** 25 s
- **Cura AOE atual:** 0,5–2,75
- **Raio:** 5 blocos
- **Duração:** 200 ticks / 10 s
- **Targeting auditado:** entidade ou ponto até 32 blocos

## O que faz

Cria uma área circular estacionária de magia Holy no alvo/ponto selecionado, curando aliados dentro dela.

## Source audit 3.16.3

- spell power: base 2, +1/level;
- cria `HealingAoe` circular;
- healing value: `getSpellPower(level, caster) * 0.25` por settlement definido pela entidade do provider;
- previsualização: `TargetedAreaEntity` com fade.

## Deduplicação / área persistente

Já cobre healing AoE Holy estacionário. Uma futura zona consagrada só representa lacuna se tiver semântica adicional real — ward, exorcismo, anti-infernal, julgamento etc. — e não apenas outro campo de cura.

## Fonte / evidência

- Catálogo oficial atual: `https://iron.wiki/spells/`
- Source audit canônico: `wiki/providers/irons-spellbooks/spells/holy/healing-circle.md`
- Consulta: 2026-09-06.
