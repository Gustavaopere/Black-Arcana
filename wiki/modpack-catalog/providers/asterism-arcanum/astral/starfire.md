# Starfire

- ID: `asterismarcanum:starfire`
- escola: Astral
- rarity: Common
- níveis: 1–10
- cast: INSTANT
- mana: 6 / 8 / 10 / 12 / 14 / 16 / 18 / 20 / 22 / 24
- cooldown: 0.3 s nominal
- neutral spell power: 7 / 9 / 11 / 13 / 15 / 17 / 19 / 21 / 23 / 25
- neutral damage: 2.1 / 2.7 / 3.3 / 3.9 / 4.5 / 5.1 / 5.7 / 6.3 / 6.9 / 7.5

## Efeito

Dispara `StarfireProjectile` sem gravidade, speed 2.5, pierce level 2 e ricochet habilitado. Em hit aplica Astral spell damage e então executa o pipeline próprio de pierce/ricochet.

## QA de targeting

O filtro de candidatos ao ricochet contém a condição:

`(owner == null || !Utils.shouldHealEntity(owner, entity)) || entity.getClass() == hit.getClass()`.

A segunda parte pode admitir entidade da mesma classe mesmo quando a primeira a trataria como friendly. Não assumir friendly-fire safety até runtime QA.

## Obtenção

Fonte concreta: Astral Scroll do Astromancer; crafting conforme config do Iron's.

## Authority e dedup

Projectile é authority de piercing/ricochet. Cada hit legítimo pode gerar provenance individual; não duplicar ricochet nem damage.

## QA

Party com dois players, summons da mesma classe, mobs da mesma classe, piercing múltiplo e cooldown sub-segundo no servidor dedicado.