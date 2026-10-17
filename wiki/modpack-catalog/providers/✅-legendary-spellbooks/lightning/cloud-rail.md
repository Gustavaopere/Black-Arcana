# Cloud Rail

**Prova binária física (2026-10-13):** ✅ `COUNTED_EXACT`, `legendary_spellbooks:cloud_rail` / `dev.higurashi.legendary_spellbooks.common.spells.lightning.CloudRailSpell`; [Java 21 #38453654179](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38453654179), [dossiê](../EXACT-BINARY-SPELLS-0.3.2.md). Dados numéricos source-pinned; execução/Survival ⚠️; +0.

- ID: `legendary_spellbooks:cloud_rail`
- School: Lightning
- Levels: 1–10
- Min rarity: Common
- Cooldown: 6 s
- Mana neutral: 20 / 25 / 30 / 35 / 40 / 45 / 50 / 55 / 60 / 65
- Spell power neutral: 2 / 3 / 4 / 5 / 6 / 7 / 8 / 9 / 10 / 11
- Cloud count: 3 / 4 / 5 / 6 / 7 / 8 / 9 / 10 / 11 / 12
- Estado Black Arcana: `JÁ EXISTE / SEM ALTERAÇÃO PLANEJADA`

## Contract

Cria uma linha/rail de clouds sob a resolução do provider. O count usa `min(2 + spellLevel, 15)`; posicionamento, lightning interactions e damage/effects permanecem do addon/Iron's.

## Acquisition

Pool do Cloud Golem: níveis 4–10, weight 10. Crafting não é desabilitado no config.

## Regra para o Black Arcana

Não criar segunda linha de clouds nem reprocessar cada cloud como cast independente.

## Source

`CloudRailSpell.java` @ `Higurashi34m/Legendary-Spellbooks@62ced2f2b2693aa841251473cbbd726fdd928ed3`.

## Engenharia causal para perks — 17/10/2026

**Prova:** `legendary_spellbooks` 0.3.2, JAR `legendary_spellbooks-1.21.1+neo-0.3.2.jar` SHA-1 `bda5b1fbe50ad834a6a76ad36789743c1057ebf5`, registro 30/30 COUNTED_EXACT ([Java21 #38453654179](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38453654179)). Mecânicas a seguir são **SOURCE_CAUSALITY** do pin `Higurashi34m/Legendary-Spellbooks@62ced2f2b2693aa841251473cbbd726fdd928ed3`; igualdade byte-a-byte de código e execução com Iron's 3.16.3/Legendary Monsters 2.2.2 **não verificadas**. Nenhum adapter RPG homologado.

| Eixo | Contrato factual observado | Limite para perks |
|---|---|---|
| Cast/stats | Rarity COMMON, nível 1–10, cooldown 6s, mana neutra 20+5×(nível−1), spell power=2+(nível−1), convertido a int no cast. | Mana/cooldown host; dano pós-settlement condicionado. |
| Posição/fan-out | getCloudCount=min(2+level,15) → 3..12 nuvens para níveis 1..10; GeometryUtils.getLinePoints de caster.position()+Y6, yaw, espaçamento 1.5, offset 1.75. Cada SpellCloudEntity recebe caster, damage e warmup=i+1, invisível inicialmente. | A formação aérea não é projectile ao longo de raycast de 12 blocos; sem geometria mutável per-caster. |
| AOE/target real | SpellCloudEntity.onHit pega LivingEntity na AABB inflate(1,1.5,1), exceto owner e aliados (checagem caster.isAlliedTo), damage = int(power)/max(distanceTo(target)/2,1), DamageSource obtida de CLOUD_RAIL_SPELL. Deflect de projectiles redirecionáveis também pertence à entidade. | A consulta ao DamageSource é compartilhada com Cloud Ring; não creditar outra spell por child. Não há validação de retorno de DamageSources.applyDamage. |
| Lifetime | Warmup tick zera velocidade; onHit cria dano/external game event e discard. Tempo máximo de vida sem impacto exige análise upstream do pai/base host. | ⛔ sem hook de atraso/fly speed/dano. |

**Âncoras:** [CloudRailSpell.java](https://github.com/Higurashi34m/Legendary-Spellbooks/blob/62ced2f2b2693aa841251473cbbd726fdd928ed3/src/main/java/dev/higurashi/legendary_spellbooks/common/spells/lightning/CloudRailSpell.java#L24-L66) · [SpellCloudEntity.java](https://github.com/Higurashi34m/Legendary-Spellbooks/blob/62ced2f2b2693aa841251473cbbd726fdd928ed3/src/main/java/dev/higurashi/legendary_spellbooks/common/entities/spell/projectile/SpellCloudEntity.java#L40-L110).

**QA e fail-closed:** Testar clouds no teto, friendly fire, cast em chuva, deflect, efeitos de bloco, 12 entidades, unload, cooldown e dano por distância. Não usar simples onCast/trigger como settlement e nunca duplicar custo, objeto mágico ou fonte de dano. **+0 novos spells, +0 adapters.**
