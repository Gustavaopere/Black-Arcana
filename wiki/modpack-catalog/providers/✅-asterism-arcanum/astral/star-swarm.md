# Star Swarm

- ID: `asterismarcanum:star_swarm`
- escola: Astral
- rarity: Common
- níveis: 1–10
- cast: CONTINUOUS
- cast base: 100 ticks / 5 s
- mana: 3–12 por nível base (`3 + level - 1`, antes das regras de continuous do Iron's)
- cooldown: 12 s
- neutral spell power: 1–10
- neutral contact damage configurado na gate: 1.75–8.5

## Efeito

Cria uma única `StarSwarmProjectile`/gate e a mantém via `EntityCastData`. A base `AbstractGateProjectile` possui cinco sub-entidades ao redor do caster.

Em ticks divisíveis por 12 ou 20, **cada uma das 5 partes dispara 3 `PiercingLightProjectile`**, ou 15 projectiles por volley elegível. Esse projectile spam é o principal settlement ofensivo continuado.

## Quirk de collision damage

`setDealDamageActive()` da classe base define `dealDamageActive=false`, apesar do nome. Assim, após o primeiro collision pass, os server cast ticks não reativam o contact damage da gate; os volleys de Piercing Light continuam funcionando independentemente.

## Obtenção

Fonte concreta: Astral Scroll do Astromancer; crafting conforme config do Iron's.

## Authority e dedup

Authority = uma gate persistente + projectiles emitidos. Não criar gate por tick e não adicionar tick damage externo para “corrigir” o flag.

## Anti-abuso/QA

Validar quantidade de entities, cleanup em cast cancel, allied collisions, servidor dedicado e interaction com cast-time modifiers.