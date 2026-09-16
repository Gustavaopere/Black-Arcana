# Luminous Beam

- ID: `asterismarcanum:luminous_beam`
- escola: Astral
- rarity: Common
- níveis: 1–10
- cast: CONTINUOUS
- cast base: 100 ticks / 5 s
- mana: 3–12 por nível base do cast (`3 + level - 1`, antes das regras de continuous do Iron's)
- cooldown: 12 s
- neutral spell power: 1–10
- neutral damage por settlement: 1.75–8.5 (`1 + 0.75×spellPower`)

## Efeito

No primeiro tick cria **uma única** `LuminousBeamProjectile` e a guarda em `EntityCastData`. Durante o cast, o provider reativa o damage settlement da mesma entidade em vez de criar um novo beam a cada tick.

A beam acompanha eye position/rotation do owner, possui 18 collision parts e corta o comprimento na colisão com blocos. `LuminousBeamProjectile.onHitEntity` aplica Astral spell damage.

## Obtenção

Fonte concreta: Astral Scroll do Astromancer; crafting conforme config do Iron's.

## Authority e dedup

A entidade persistente é authority. É proibido transformar cada cast tick em novo projectile/beam ou reaplicar dano por observer.

## QA

O collision filter exclui owner e exige LOS, mas não possui allied filter explícito antes de `DamageSources.applyDamage`. Validar party/PvP/summons e taxa real de damage ticks.