# Sunbeam

- **Status no modpack:** PRESENTE — ativo no catálogo atual
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **Spell ID:** `irons_spellbooks:sunbeam`
- **JAR/versão:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Holy
- **Níveis:** 1–10
- **Raridade:** Uncommon → Legendary
- **Cast:** Instant
- **Mana:** 40–130
- **Cooldown:** 20 s
- **Dano atual:** 12–25,5
- **Targeting auditado:** até 48 blocos

## O que faz

Canaliza a energia dos céus em um ataque Holy vertical sobre o alvo/ponto resolvido.

## Source audit 3.16.3

- spell power: base 24, +3/level;
- cria `SunbeamEntity` no alvo/ponto resolvido pelo raycast;
- fórmula: `damage = getSpellPower(level, caster) * 0.5`;
- quando não há target entity, procura posição relativa ao chão;
- toca `SUNBEAM_WINDUP` na posição criada.

## Deduplicação

Já cobre “raio de luz do céu” cujo resultado é dano Holy. Uma magia Celestial futura precisa de condição/recurso/semântica distinta — Sanctum, Resonance, julgamento contextual etc. — e não apenas outro beam visual.

## Fonte / evidência

- Catálogo oficial atual: `https://iron.wiki/spells/`
- Source audit canônico: `wiki/providers/irons-spellbooks/spells/holy/sunbeam.md`
- Consulta: 2026-09-06.
