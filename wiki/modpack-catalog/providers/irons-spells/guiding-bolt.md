# Guiding Bolt

- **Status no modpack:** PRESENTE — spell ativo no catálogo atual
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **Spell ID auditado:** `irons_spellbooks:guiding_bolt`
- **JAR/versão:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Holy
- **Níveis:** 1–10
- **Raridade:** Common → Legendary
- **Cast:** Instant
- **Mana:** 20–65
- **Cooldown:** 8 s
- **Dano público atual:** 3–7,5
- **Guided effect:** 25 s

## O que faz

Dispara um bolt lento de energia Holy. O catálogo atual confirma que criaturas atingidas recebem `Guided`, fazendo projéteis próximos tenderem/homing em direção a elas.

## Runtime auditado

O source 3.16.3 cria `GuidingBoltProjectile` na altura dos olhos do caster e registra `damage = getSpellPower(level, caster) * 0.5`. O detalhe de aquisição, resistência e comportamento fino do efeito `Guided` além da semântica pública permanece sob authority do provider.

## Deduplicação

Já cobre projétil ofensivo Holy com marca de orientação/homing. Nova magia não é gap apenas por usar outro bolt luminoso ou outra marca de target attraction equivalente.

## Fonte / evidência

- Catálogo oficial atual: `https://iron.wiki/spells/`.
- Auditoria source 3.16.3: `wiki/providers/irons-spellbooks/spells/holy/guiding-bolt.md`.