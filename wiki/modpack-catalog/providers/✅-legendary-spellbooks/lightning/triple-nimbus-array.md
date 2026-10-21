# Triple Nimbus Array

**Prova binária física (2026-10-13):** ✅ `COUNTED_EXACT`, `legendary_spellbooks:triple_nimbus_array` / `dev.higurashi.legendary_spellbooks.common.spells.lightning.TripleNimbusArraySpell`; [Java 21 #38453654179](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38453654179), [dossiê](../EXACT-BINARY-SPELLS-0.3.2.md). Dados numéricos source-pinned; execução/Survival ⚠️; +0.

- ID: `legendary_spellbooks:triple_nimbus_array`
- School: Lightning
- Levels: 1–5
- Min rarity: Rare
- Cooldown: 15 s
- Mana neutral: 140 / 160 / 180 / 200 / 220
- Spell power neutral: 3 / 5 / 7 / 9 / 11
- Anchor iterations: 2 / 4 / 6 / 8 / 10
- Pattern: cada anchor gera três pontos/linhas em leque segundo a geometria do provider
- Lifetime: 25 / 30 / 35 / 40 / 40 ticks
- Crafting: desabilitado
- Estado Black Arcana: `JÁ EXISTE / SEM ALTERAÇÃO PLANEJADA`

## Contract

É a variante tripla provider-native de Nimbus Array, com geometria em três linhas e custo/power próprios. A spell desabilita looting e crafting.

## Acquisition

Pool do Cloud Golem: níveis 1–4, weight 12.

## Regra para o Black Arcana

Não modelar a variante tripla como três casts de Nimbus Array nem gerar três cobranças/recompensas/procs separados por integração.

## Source

`TripleNimbusArraySpell.java` @ source pin 0.3.2.

## Engenharia causal para perks — 17/10/2026

**Prova:** `legendary_spellbooks` 0.3.2, JAR `legendary_spellbooks-1.21.1+neo-0.3.2.jar` SHA-1 `bda5b1fbe50ad834a6a76ad36789743c1057ebf5`, registro 30/30 COUNTED_EXACT ([Java21 #38453654179](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38453654179)). Mecânicas a seguir são **SOURCE_CAUSALITY** do pin `Higurashi34m/Legendary-Spellbooks@62ced2f2b2693aa841251473cbbd726fdd928ed3`; igualdade byte-a-byte de código e execução com Iron's 3.16.3/Legendary Monsters 2.2.2 **não verificadas**. Nenhum adapter RPG homologado.

| Eixo | Contrato factual observado | Limite para perks |
|---|---|---|
| Cast/custo | Níveis 1–5, cooldown 15s, mana 140+20×(nível−1), power neutro 3+2×(nível−1), int ao spawn; classe sem castTime específico nesse corpo. | Timing efetivo depende da base host; não inventar ticks de cast. |
| Geometria/quantidade | getNimbusCount=min(2×level,15)→2/4/6/8/10 **fileiras**, cada uma GeometryUtils.getFanPoints(center,yaw,70°,distance=(i+1)×1.5,**3**) = até **6/12/18/24/30** LightningBoltEntity, não 2/4/6/8/10 strikes totais. | A UI `nimbus_count` expõe fileiras; 3 por iteração são filhos. Alteração de fanout ⛔. |
| Warmup/duração | Warmup i+1 em cada subfileira, lifeTick=min(20+5×level,40)=25/30/35/40/40. findGround(...,6,3) pode impedir parte dos spawns. | DamageType/physics da entidade externa e side não homologados. |

**Âncoras:** [TripleNimbusArraySpell.java](https://github.com/Higurashi34m/Legendary-Spellbooks/blob/62ced2f2b2693aa841251473cbbd726fdd928ed3/src/main/java/dev/higurashi/legendary_spellbooks/common/spells/lightning/TripleNimbusArraySpell.java#L26-L81).

**QA e fail-closed:** QA 30 bolt case, performance, hit overlap, line-of-sight, friendly fire, instância LightningBoltEntity 2.2.2, per-hit Mastery. Não usar simples onCast/trigger como settlement e nunca duplicar custo, objeto mágico ou fonte de dano. **+0 novos spells, +0 adapters.**
