# Annihilation Shockwave

**Prova binária física (2026-10-13):** ✅ `COUNTED_EXACT`, identidade estática `legendary_spellbooks:annihilation_shockwave` / classe `dev.higurashi.legendary_spellbooks.common.spells.annihilation.AnnihilationShockwaveSpell` — [Java 21 #38453654179](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38453654179), [dossiê SHA-exato](../EXACT-BINARY-SPELLS-0.3.2.md). Valores/custos descritos da fonte continuam **⚠️ sem validação runtime/Survival**; +0 raízes.

- ID: `legendary_spellbooks:annihilation_shockwave`
- School: `legendary_spellbooks:annihilation`
- Levels: 1–6
- Min rarity: Rare
- Cooldown: 16 s
- Cast: Long, 10 ticks; cast-time reduction desabilitada
- Mana neutral: 120 / 130 / 140 / 150 / 160 / 170
- Spell power neutral: 6 / 8 / 10 / 12 / 14 / 16
- Max-HP component: 0.5% / 1% / 1.5% / 2% / 2.5% / 3%
- Wave count: 3 / 4 / 5 / 6 / 7 / 8
- Outer distance: 6 / 7.5 / 9 / 10.5 / 12 / 13.5 blocks
- Looting: desabilitado
- Estado Black Arcana: `JÁ EXISTE / SEM ALTERAÇÃO PLANEJADA`

## Contract

Stomp que gera ondas em leque de `AnnihilationFlameStrike`. Cada strike recebe spell power e o componente de vida máxima; o provider marca as entidades como source de spell.

## Acquisition

Pool do The Obliterator: níveis 1–5, weight 18. Crafting não é desabilitado no config da spell.

## Regra para o Black Arcana

Não processar as FlameStrikes novamente como spell nova nem duplicar o HP damage.

## Source

`AnnihilationShockwaveSpell.java` @ source pin 0.3.2.

## Engenharia causal para perks — 17/10/2026

**Proveniência:** identificação física `legendary_spellbooks-1.21.1+neo-0.3.2.jar`, SHA-1 `bda5b1fbe50ad834a6a76ad36789743c1057ebf5` (30/30 registros). Corpo de método proveniente de `Higurashi34m/Legendary-Spellbooks@62ced2f2b2693aa841251473cbbd726fdd928ed3` com nível de evidência **SOURCE_CAUSALITY**. Não equivale a QA do pack Iron's 3.16.3/Legendary Monsters 2.2.2 nem a assinatura de adapter RPG homologada.

| Eixo | Causalidade source-pinned | Limite de integração |
|---|---|---|
| Cast/custo | DefaultConfig nível 1–6, cooldown 16s, rarity RARE, castTime=10 ticks, mana `120+10×(level−1)`, spell power `6+2×(level−1)` neutros. O addon usa `SpellAnimations.STOMP`, nenhum cast extra para as waves. | Mana, casting e config sob host Iron's, ⛔ hook para alterar quantidade de waves não demonstrado. |
| Geometria | `waveCount=min(2+level,10)` = 3,4,5,6,7,8. O loop i=0..waveCount−1 chama `getBlockDistance(i)=(i+1)×1.5`: distância máxima **4.5/6/7.5/9/10.5/12 blocos** no spawn. Já o UI usa `getBlockDistance(getWaveCount(level))`, ou **6/7.5/9/10.5/12/13.5**. **Distância exibida ≠ última onda posicionada**. | `SEM_HOOK_SEGURO` para range, cone ou alvos; não empregar número de UI como limite do efeito físico. |
| Cones / contagem | `GeometryUtils.getFanPoints(caster.position(),yaw,50°,distance,1+i)`; com waveCount 3..8, até `sum(1..waves)` = **6/10/15/21/28/36** tentativas de `AnnihilationFlameStrike`, antes de `RaycastUtils.findGround(level,point,4,2)` e limites de entidade/chunk. | Multiplicar strikes por perk expande custo por ~quadrado das waves; carece caps, teste e hook. |
| Tempo / alvos | Cada strike recebe warmup `i×2 ticks`, lifetime/arg `20`, yaw para origem; a lógica de colisão e atingimento pertence à `AnnihilationFlameStrike` de Legendary Monsters. | **NÃO VERIFICADO** hitbox, target eligibility, time-to-hit e runtime 2.2.2. |
| Tipo e dano | Spawn passa `damage=getSpellPower(level,caster)` mais `healthDamageMultiplier=0.005×level` via `ISpellSourceFlag.legendarySpellbooks$setDamage`. A classe do addon marca o strike como `markSpell`, mas dano executado pertence ao handler/entidade externa. | `⛔` não duplicar base+HP damage nem inferir aceitação de `DamageType` em driver externo. |
| Causalidade/Mastery | Uma ativação gera várias entidades filhas com buffs/debuffs desconhecidos; sons/partículas são componentes visuais. | Mastery exige token do cast pai e settlement por dano, não por 36 instâncias. |

**Âncora:** [AnnihilationShockwaveSpell, loops, UI e multiplicadores](https://github.com/Higurashi34m/Legendary-Spellbooks/blob/62ced2f2b2693aa841251473cbbd726fdd928ed3/src/main/java/dev/higurashi/legendary_spellbooks/common/spells/annihilation/AnnihilationShockwaveSpell.java#L31-L123).

**QA:** medir distância da última onda versus tooltip, line-of-sight e `findGround`, cancelamento, fonte `ISpellSourceFlag` no JAR 2.2.2, AoE, friendly-fire, cap de 36 entidades, lag/cleanup e dano de HP real. **+0 raízes.**
