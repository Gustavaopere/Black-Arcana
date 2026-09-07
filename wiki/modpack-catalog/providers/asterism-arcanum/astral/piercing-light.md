# Piercing Light

- ID: `asterismarcanum:piercing_light`
- escola: Astral
- rarity: Rare
- níveis: 1–10
- cast: INSTANT
- mana: 25 / 30 / 35 / 40 / 45 / 50 / 55 / 60 / 65 / 70
- cooldown: 20 s
- neutral spell power: 1 em todos os níveis
- neutral projectile damage: 1.5
- projectiles por cast: `(4 + level) × spellPower × 3` = 15 / 18 / 21 / 24 / 27 / 30 / 33 / 36 / 39 / 42 em neutral

## Efeito

Dispara uma rajada radial em três faixas de velocidade. Para cada índice calculado a spell cria três `PiercingLightProjectile`; cada projectile carrega damage próprio e aplica Astral spell damage em hit.

A classe do projectile não define um segundo damage source nem um ledger paralelo; impacto passa pelo projectile provider-native.

## Obtenção

Fonte concreta: Astral Scroll do Astromancer; crafting conforme config do Iron's.

## Authority e dedup

Cada projectile é uma unidade causal. Um perk que reage a spell-hit deve deduplicar por projectile/hit e nunca multiplicar novamente pela contagem nominal do cast.

## Anti-abuso/QA

A quantidade de entidades cresce até 42 em neutral lvl10. Validar performance, friendly fire e interaction com modifiers que alteram spell power/level.