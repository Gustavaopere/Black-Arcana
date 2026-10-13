# Laceration

**✅ Revalidação SHA-exata 2026-10-13:** spell ID estático `ypfundamentals:laceration` confirmado no JAR físico/publicador 1.1.7.1 (`a2855c253202a8fcc2925fcf5b1bf86d64fbe4da`), escola default Blood, [Java21 #38436717443](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38436717443) SUCCESS. `COUNTED_EXACT` somente registry e classe, +0 novas raízes. [Dossiê](../EXACT-BINARY-SPELLS-1.1.7.1.md). Progressão, mana/config, multiplayer e Survival ⚠️.


- ID: `ypfundamentals:laceration`
- escola: Blood
- rarity: Common
- níveis: 1–5
- cast: LONG, 15 ticks / 0.75 s; não-interrompível
- mana: 40 / 50 / 60 / 70 / 80
- cooldown: 30 s
- neutral power: 5 / 7 / 9 / 11 / 13
- melee area: caixa curta centrada ~2 blocos à frente, com line-of-sight

## Dano

`damage = spellPower + (weaponDamage + SharpnessLevel)/2` quando a arma possui enchantments. Em hit bem-sucedido executa `EnchantmentHelper.doPostAttackEffects` e aplica `Lacerated` amplifier 1.

Duração: `spellPower×15 + additionalDamage×40` ticks.

## Healing reduction — divergência QA

Tooltip informa redução 40. O event handler real faz:

- sem Iron's Blight: heal ×0.6 e depois ×0.8 = **48% da cura original / 52% redução**;
- com Blight: o handler Ypsilon aplica apenas ×0.8; efeito final combinado com o listener do Blight precisa de runtime QA.

## Obtenção

Pipeline padrão permitido; fonte concreta: **NÃO VERIFICADO**.

## Dedup

Não adicionar segundo listener de healing reduction nem repetir enchantment post-hit.