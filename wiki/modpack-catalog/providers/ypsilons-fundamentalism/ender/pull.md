# Pull

- ID: `ypfundamentals:pull_spell`
- escola: Ender
- rarity: Rare
- níveis: 1–4
- cast: INSTANT
- mana: 40 / 50 / 60 / 70
- cooldown: 40 s
- neutral damage: 1 / 3 / 5 / 7
- radius: ~1.125 / 1.789 / 2.357 / 2.875
- projectile speed: 0.30
- lifetime: 5 s

## Efeito

`PullProjectile` rastreia entities dentro do volume, exclui owner, friendly fire e spectators; aplica força em direção ao centro escalada por distância, knockback resistance e resistência de boss. A cada 5 ticks, se a entidade está a menos de 9 blocos e `canHitEntity`, aplica o damage configurado. Zera fallDistance. É `AntiMagicSusceptible`.

## Obtenção

Pipeline padrão permitido; fonte concreta: **NÃO VERIFICADO**.

## Dedup

Não adicionar segundo pull/damage ticker. Entity do provider é a única authority.