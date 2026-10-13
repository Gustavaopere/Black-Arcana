# Pull

**✅ Revalidação SHA-exata 2026-10-13:** spell ID estático `ypfundamentals:pull_spell` confirmado no JAR físico/publicador 1.1.7.1 (`a2855c253202a8fcc2925fcf5b1bf86d64fbe4da`), escola default Ender, [Java21 #38436717443](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38436717443) SUCCESS. `COUNTED_EXACT` somente registry e classe, +0 novas raízes. [Dossiê](../EXACT-BINARY-SPELLS-1.1.7.1.md). Progressão, mana/config, multiplayer e Survival ⚠️.


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