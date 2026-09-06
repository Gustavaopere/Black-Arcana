# Wisp

- **Status no modpack:** PRESENTE — spell ativo no catálogo atual
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **Spell ID auditado:** `irons_spellbooks:wisp`
- **JAR/versão:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Holy
- **Níveis:** 1–10
- **Raridade:** Common → Legendary
- **Cast:** Long — 20 ticks auditados
- **Mana:** 15–33
- **Cooldown:** 3 s
- **Dano público atual:** 5–14
- **Target helper auditado:** 48 blocos

## O que faz

Conjura um wisp/projétil de energia Holy que flutua em direção a um alvo próximo e causa dano no impacto.

## Runtime auditado

Com alvo válido, o source 3.16.3 cria `WispEntity(world, caster, spellPower)`, associa o target e posiciona o wisp à frente do caster. O tooltip expõe spell power como dano; detalhes finos de perseguição/impacto pertencem à `WispEntity` e não são reimplementados por Black Arcana.

## Deduplicação

Já ocupa projétil/orbe Holy teleguiado. Outro wisp de luz sem semântica adicional não é gap.

## Fonte / evidência

- Catálogo oficial atual: `https://iron.wiki/spells/`.
- Auditoria source 3.16.3: `wiki/providers/irons-spellbooks/spells/holy/wisp.md`.