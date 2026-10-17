# Glacier Eruption

**Prova binária física (2026-10-13):** ✅ `COUNTED_EXACT`, `legendary_spellbooks:glacier_eruption` / `dev.higurashi.legendary_spellbooks.common.spells.ice.GlacierEruptionSpell`; [Java 21 #38453654179](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38453654179), [dossiê SHA-exato](../EXACT-BINARY-SPELLS-0.3.2.md). Números/comportamentos source-pinned; execução/Survival ⚠️; +0 magias.

- ID: `legendary_spellbooks:glacier_eruption`
- School: Ice
- Levels: 1–7
- Min rarity: Rare
- Cooldown: 6 s
- Mana neutral: 30 / 35 / 40 / 45 / 50 / 55 / 60
- Spell power neutral: 3 / 4 / 5 / 6 / 7 / 8 / 9
- Spike count: 4 / 5 / 6 / 7 / 8 / 9 / 10 from `min(3 + level, 15)`
- Estado Black Arcana: `JÁ EXISTE / SEM ALTERAÇÃO PLANEJADA`

## Contract

Erupção de ice spikes provider-native. O addon possui mixins próprios para entidades de Ice Spike e é a authority de posicionamento/impacto; Black Arcana não deve instalar uma segunda conversão sobre as mesmas spikes.

## Acquisition

Pool do Frostbitten Golem: níveis 2–7, weight 10. Crafting não é desabilitado no config.

## Regra para o Black Arcana

Não duplicar spike count, dano, freeze/frost riders ou callbacks já tratados pelo addon.

## Source

`GlacierEruptionSpell.java`, Ice Spike mixins @ source pin 0.3.2.

## Engenharia causal para perks — 17/10/2026

**Prova:** `legendary_spellbooks` 0.3.2, JAR `legendary_spellbooks-1.21.1+neo-0.3.2.jar` SHA-1 `bda5b1fbe50ad834a6a76ad36789743c1057ebf5`, registro 30/30 COUNTED_EXACT ([Java21 #38453654179](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38453654179)). Mecânicas a seguir são **SOURCE_CAUSALITY** do pin `Higurashi34m/Legendary-Spellbooks@62ced2f2b2693aa841251473cbbd726fdd928ed3`; igualdade byte-a-byte de código e execução com Iron's 3.16.3/Legendary Monsters 2.2.2 **não verificadas**. Nenhum adapter RPG homologado.

| Eixo | Contrato factual observado | Limite para perks |
|---|---|---|
| Cast / scaling | Níveis 1–7; cooldown 6s; mana neutra 30+5×(nível−1), power 3+(nível−1). onCast faz (int)getSpellPower, truncando o dano recebido pela entidade. | Stats/cast Iron's; source de dano final em IceSpikeEntity externa ⚠️. |
| Geometria | getSpikesCount=min(3+level,15) → **4..10** pontos nos níveis 1..7 em GeometryUtils.getLinePoints(caster.position(),yaw,spikeCount,1.5,1.5). Cada ponto usa RaycastUtils.findGround(...,6,3); se null, pula só aquele ponto. | Linha no solo não é raio de hitbox/target. Range exato de helper precisa QA. |
| Tempo/fan-out | Cada SpellIceSpikeEntity é construída com warmup=i+1, yaw radians, caster e dano. Espículas são entidades filhas do mesmo cast, sem comprovação de dano/Freeze da build Legendary Monsters 2.2.2. | ⛔ não ampliar contagem ou alterar tick/hitbox sem hook real. |

**Âncoras:** [GlacierEruptionSpell.java](https://github.com/Higurashi34m/Legendary-Spellbooks/blob/62ced2f2b2693aa841251473cbbd726fdd928ed3/src/main/java/dev/higurashi/legendary_spellbooks/common/spells/ice/GlacierEruptionSpell.java#L25-L66) · [SpellIceSpikeEntity.java](https://github.com/Higurashi34m/Legendary-Spellbooks/blob/62ced2f2b2693aa841251473cbbd726fdd928ed3/src/main/java/dev/higurashi/legendary_spellbooks/common/entities/spell/projectile/SpellIceSpikeEntity.java#L9-L23).

**QA e fail-closed:** QA em terreno desigual, níveis 1 e 7, delay crescente, 10 spawns, dano efetivo, cliente/servidor e type. Não usar simples onCast/trigger como settlement e nunca duplicar custo, objeto mágico ou fonte de dano. **+0 novos spells, +0 adapters.**
