# Cloud Ring

**Prova binária física (2026-10-13):** ✅ `COUNTED_EXACT`, `legendary_spellbooks:cloud_ring` / `dev.higurashi.legendary_spellbooks.common.spells.lightning.CloudRingSpell`; [Java 21 #38453654179](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38453654179), [dossiê](../EXACT-BINARY-SPELLS-0.3.2.md). Dados numéricos source-pinned; execução/Survival ⚠️; +0.

- ID: `legendary_spellbooks:cloud_ring`
- School: Lightning
- Levels: 1–5
- Min rarity: Epic
- Cooldown: 15 s
- Cast-time field: 40 ticks
- Mana neutral: 60 / 70 / 80 / 90 / 100
- Spell power neutral: 2 / 5 / 8 / 11 / 14
- Ring count: 1 / 2 / 3 / 4 / 5
- Estado Black Arcana: `JÁ EXISTE / SEM ALTERAÇÃO PLANEJADA`

## Contract

Gera anéis de cloud entities em torno do caster/área segundo a geometria do provider. O count usa `min(spellLevel,10)`; as clouds e seus efeitos não são uma surface para um segundo pipeline de dano.

## Acquisition

Pool do Cloud Golem: níveis 1–4, weight 10. Crafting não é desabilitado no config.

## Regra para o Black Arcana

Não duplicar rings, clouds ou lightning callbacks.

## Source

`CloudRingSpell.java` @ source pin 0.3.2.

## Engenharia causal para perks — 17/10/2026

**Prova:** `legendary_spellbooks` 0.3.2, JAR `legendary_spellbooks-1.21.1+neo-0.3.2.jar` SHA-1 `bda5b1fbe50ad834a6a76ad36789743c1057ebf5`, registro 30/30 COUNTED_EXACT ([Java21 #38453654179](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38453654179)). Mecânicas a seguir são **SOURCE_CAUSALITY** do pin `Higurashi34m/Legendary-Spellbooks@62ced2f2b2693aa841251473cbbd726fdd928ed3`; igualdade byte-a-byte de código e execução com Iron's 3.16.3/Legendary Monsters 2.2.2 **não verificadas**. Nenhum adapter RPG homologado.

| Eixo | Contrato factual observado | Limite para perks |
|---|---|---|
| Cast/stats | Níveis 1–5, cooldown 15s, castTime 40; mana 60+10×(nível−1), power 2+3×(nível−1), trunca float para int ao configurar as entidades. | Spell power do caster e config efetiva distintos da fórmula neutra. |
| Anéis e quantidades | ringCount=min(level,10)→1..5; raio i =1.5+1.75i, Y=8+i/2 acima do caster; cloudCount por anel=(int)(radius×3) → 4,9,15,20,25, total por spell level **4/13/28/48/73** tentativas, se GeometryUtils retorna todos os pontos. | A contagem é cumulativa por anel; ⛔ alterar geometria/quantidade sem cap e hook. |
| Tempo e dano | Cada SpellCloudEntity tem warmup=(i+1)×4, mesmo atraso para todas as nuvens daquele anel; `onHit` executa AABB inflate(1,1.5,1) e usa **CLOUD_RAIL_SPELL.getDamageSource**, mesmo criada por Cloud Ring. | Possível divergência de atribuição de escola/spell no source, não bug confirmado no JAR. Mastery só pós-hit e dedup. |
| Alvos | Owner e aliados excluídos no applyCloudDamage, mas corpo não comprova LOS, block protection ou DamageType Lightning; tiros filhos são entidades provider-owned. | Sem setter aprovado de tamanho/target. |

**Âncoras:** [CloudRingSpell.java](https://github.com/Higurashi34m/Legendary-Spellbooks/blob/62ced2f2b2693aa841251473cbbd726fdd928ed3/src/main/java/dev/higurashi/legendary_spellbooks/common/spells/lightning/CloudRingSpell.java#L25-L75) · [SpellCloudEntity.java](https://github.com/Higurashi34m/Legendary-Spellbooks/blob/62ced2f2b2693aa841251473cbbd726fdd928ed3/src/main/java/dev/higurashi/legendary_spellbooks/common/entities/spell/projectile/SpellCloudEntity.java#L50-L85).

**QA e fail-closed:** Testar total 73 em lvl5, clouds atingindo blocos/entidades, load/unload e FLAG de attribution Cloud Rail, i-frames e spam PvP. Não usar simples onCast/trigger como settlement e nunca duplicar custo, objeto mágico ou fonte de dano. **+0 novos spells, +0 adapters.**
