# Lapsus

**✅ Revalidação SHA-exata 2026-10-13:** spell ID estático `ypfundamentals:lapsus` confirmado no JAR físico/publicador 1.1.7.1 (`a2855c253202a8fcc2925fcf5b1bf86d64fbe4da`), escola default Ender, [Java21 #38436717443](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38436717443) SUCCESS. `COUNTED_EXACT` somente registry e classe, +0 novas raízes. [Dossiê](../EXACT-BINARY-SPELLS-1.1.7.1.md). Progressão, mana/config, multiplayer e Survival ⚠️.


- ID: `ypfundamentals:lapsus`
- escola: Ender
- rarity: Rare
- níveis: 1–3
- cast: INSTANT
- mana: 50 / 60 / 70
- cooldown: 45 s
- recast count: 2
- janela: 3 / 6 / 9 s
- dano: nenhum

## Efeito

Primeira execução salva `caster.blockPosition().below()`. Nova execução enquanto a location existe teleporta o caster para `location + 1` via `Utils.handleSpellTeleport`, zera fall distance e limpa location.

## QA BLOCKER — estado singleton

`location` é um campo `private BlockPos` na instância registrada de `LapsusSpell`, não cast data por jogador. Como spells são singletons de registry, dois players/casts concorrentes podem compartilhar ou limpar o mesmo estado. **Não considerar multiplayer-safe sem GameTest/dedicated-server QA.**

## Obtenção

Pipeline padrão permitido; fonte concreta: **NÃO VERIFICADO**.

## Dedup

Black Arcana não deve tentar remediar o estado criando uma segunda location silenciosa; qualquer fix exige patch explícito/provider contract.