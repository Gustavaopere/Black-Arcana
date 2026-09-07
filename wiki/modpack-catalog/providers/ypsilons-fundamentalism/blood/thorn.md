# Thorn

- ID: `ypfundamentals:thorn`
- escola: Blood
- rarity: Common
- níveis: 1–5
- cast: INSTANT
- mana: 20 / 25 / 30 / 35 / 40
- cooldown: 12 s
- neutral power: 10 / 15 / 20 / 25 / 30
- projectile speed: 2

## Dano e mark

Projectile base damage = `0.5×spellPower`: 5 / 7.5 / 10 / 12.5 / 15.

Primeiro hit em LivingEntity sem Marked: aplica `Marked` por 15 s e causa base damage. Hit posterior enquanto Marked está ativo remove Marked e causa `3× projectile damage`: 15 / 22.5 / 30 / 37.5 / 45, além de blastwave/camera shake visuais.

## Obtenção

Pipeline padrão permitido; fonte concreta: **NÃO VERIFICADO**.

## Authority / dedup

`Marked` é o ledger provider-native. Não criar mark paralelo nem executar o bônus duas vezes.