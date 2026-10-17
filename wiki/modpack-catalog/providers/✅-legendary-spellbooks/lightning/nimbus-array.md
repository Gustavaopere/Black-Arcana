# Nimbus Array

**Prova binária física (2026-10-13):** ✅ `COUNTED_EXACT`, `legendary_spellbooks:nimbus_array` / `dev.higurashi.legendary_spellbooks.common.spells.lightning.NimbusArraySpell`; [Java 21 #38453654179](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38453654179), [dossiê](../EXACT-BINARY-SPELLS-0.3.2.md). Dados numéricos source-pinned; execução/Survival ⚠️; +0.

- ID: `legendary_spellbooks:nimbus_array`
- School: Lightning
- Levels: 1–7
- Min rarity: Rare
- Cooldown: 10 s
- Mana neutral: 80 / 90 / 100 / 110 / 120 / 130 / 140
- Spell power neutral: 2 / 3 / 4 / 5 / 6 / 7 / 8
- Nimbus count: 2 / 4 / 6 / 8 / 10 / 12 / 14
- Lifetime: 25 / 30 / 35 / 40 / 40 / 40 / 40 ticks
- Estado Black Arcana: `JÁ EXISTE / SEM ALTERAÇÃO PLANEJADA`

## Contract

Cria uma array de clouds/nimbus com count `min(2 × spellLevel,15)` e lifetime `min(20 + 5 × spellLevel,40)`. A versão simples permanece craftável no config.

## Acquisition

Pool do Cloud Golem: níveis 1–6, weight 10.

## Regra para o Black Arcana

Não confundir com Triple Nimbus Array; são registros distintos. Não duplicar arrays ou lifespan tracking.

## Source

`NimbusArraySpell.java` @ source pin 0.3.2.

## Engenharia causal para perks — 17/10/2026

**Prova:** `legendary_spellbooks` 0.3.2, JAR `legendary_spellbooks-1.21.1+neo-0.3.2.jar` SHA-1 `bda5b1fbe50ad834a6a76ad36789743c1057ebf5`, registro 30/30 COUNTED_EXACT ([Java21 #38453654179](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38453654179)). Mecânicas a seguir são **SOURCE_CAUSALITY** do pin `Higurashi34m/Legendary-Spellbooks@62ced2f2b2693aa841251473cbbd726fdd928ed3`; igualdade byte-a-byte de código e execução com Iron's 3.16.3/Legendary Monsters 2.2.2 **não verificadas**. Nenhum adapter RPG homologado.

| Eixo | Contrato factual observado | Limite para perks |
|---|---|---|
| Cast/stats | Níveis 1–7; cooldown 10s; mana 80+10×(nível−1), power 2+(nível−1) convertido a int; Lightning school. | Mana/dano do host vs entidade LightningBoltEntity externa. |
| Geometria/fan-out | getNimbusCount=min(level×2,15): **2/4/6/8/10/12/14** strikes nos níveis 1..7. GeometryUtils.getLinePoints(caster.position(),yaw,count,1.5,1.5) e RaycastUtils.findGround(level,point,6,3). | Line placement/range não é esfera de dano; alteração por perk sem hook ⛔. |
| Tempo/dano | Cada LightningBoltEntity do Legendary Monsters recebe warmup=i+1, caster, lifeTick=min(20+level×5,40) =25/30/35/40/40/40/40 ticks, e damage int(power). DamageSource, hitbox e espécie dos alvos pertencem ao dependency jar. | NÃO VERIFICADO no pack 2.2.2; não criar segundo raio/raio elétrico. |

**Âncoras:** [NimbusArraySpell.java](https://github.com/Higurashi34m/Legendary-Spellbooks/blob/62ced2f2b2693aa841251473cbbd726fdd928ed3/src/main/java/dev/higurashi/legendary_spellbooks/common/spells/lightning/NimbusArraySpell.java#L26-L74).

**QA e fail-closed:** QA contagem, ground raycast, duração capped lvl4, servidor/client, attacker credit/friendly/PvP. Não usar simples onCast/trigger como settlement e nunca duplicar custo, objeto mágico ou fonte de dano. **+0 novos spells, +0 adapters.**
