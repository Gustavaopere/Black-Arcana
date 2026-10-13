# Thorn

**✅ Revalidação SHA-exata 2026-10-13:** spell ID estático `ypfundamentals:thorn` confirmado no JAR físico/publicador 1.1.7.1 (`a2855c253202a8fcc2925fcf5b1bf86d64fbe4da`), escola default Blood, [Java21 #38436717443](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38436717443) SUCCESS. `COUNTED_EXACT` somente registry e classe, +0 novas raízes. [Dossiê](../EXACT-BINARY-SPELLS-1.1.7.1.md). Progressão, mana/config, multiplayer e Survival ⚠️.


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