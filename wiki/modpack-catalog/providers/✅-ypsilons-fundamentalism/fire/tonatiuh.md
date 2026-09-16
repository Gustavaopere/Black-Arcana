# Tonatiuh

- ID: `ypfundamentals:sol`
- classe: `SolSpell`
- escola: Fire
- rarity: Legendary
- nível: 1
- cast: LONG, 200 ticks / 10 s
- mana: 450
- cooldown: 300 s
- neutral spell power: 30
- `requiresLearning=true`

## Escala solar

`damage = spellPower × timeBoost`.

Time boost: 0.25× na faixa 15000–21000; 0.75× em 12000–15000 e 21000–24000; 1× em 0–3000 e 9000–12000; 1.5× em 3000–9000; 2.5× em 4500–7500. As condições se sobrepõem parcialmente no código; a ordem dos `if/else if` acima é a authority.

Neutral damage: 7.5 / 22.5 / 30 / 45 / 75 conforme boost. `radius = 1 + 4.5×boost`; projectile recebe explosion radius `radius×4`.

## Aprendizado

O event layer aprende Tonatiuh ao jogador que mata o `FireBossEntity` do Iron's. Não conceder por fallback genérico.

## Dedup

Authority de dano/explosão/world-griefing = `SolProjectile`. Respeitar event de explosão/provider configs; não criar segunda explosão.