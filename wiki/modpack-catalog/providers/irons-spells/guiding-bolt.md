# Guiding Bolt

- **Status no modpack:** PRESENTE — ativo no catálogo atual
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **Spell ID:** `irons_spellbooks:guiding_bolt`
- **JAR/versão:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Holy
- **Níveis:** 1–10
- **Raridade:** Common → Legendary
- **Cast:** Instant
- **Mana:** 20–65
- **Cooldown:** 8 s
- **Dano atual:** 3–7,5
- **Guided atual:** 25 s

## O que faz

Dispara um projétil lento Holy. A documentação pública atual registra que criaturas atingidas recebem Guided, fazendo projéteis próximos tenderem ao alvo durante 25 s.

## Source audit 3.16.3

- spell power: base 6, +1/level;
- cria `GuidingBoltProjectile` na altura dos olhos do caster e o dispara na direção de visão;
- fórmula de dano: `getSpellPower(level, caster) * 0.5`.

A mecânica pública de Guided é confirmada pelo catálogo atual; raio/algoritmo fino de homing permanece propriedade do projectile/effect do provider e não é reimplementado aqui.

## Deduplicação / causalidade

Já cobre bolt Holy + marca de homing. Não criar um segundo homing genérico nem atribuir hits posteriores ao cast raiz sem causalidade comprovada pelo provider.

## Fonte / evidência

- Catálogo oficial atual: `https://iron.wiki/spells/`
- Source audit canônico: `wiki/providers/irons-spellbooks/spells/holy/guiding-bolt.md`
- Consulta: 2026-09-06.
