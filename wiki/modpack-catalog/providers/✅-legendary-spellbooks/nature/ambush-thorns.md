# Ambush Thorns

**Prova binária física (2026-10-13):** ✅ `COUNTED_EXACT` — `legendary_spellbooks:ambush_thorns`, classe `dev.higurashi.legendary_spellbooks.common.spells.nature.AmbushThornsSpell` ([Java 21 #38453654179](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38453654179); [dossiê SHA-exato](../EXACT-BINARY-SPELLS-0.3.2.md)). Valores e mecânicas source-pinned; runtime/Survival ⚠️; +0 raízes.

- ID: `legendary_spellbooks:ambush_thorns`
- School: Nature
- Levels: 1–10
- Min rarity: Common
- Cooldown: 120 s
- Cast-time field: 30 ticks
- Mana neutral: 65 / 70 / 75 / 80 / 85 / 90 / 95 / 100 / 105 / 110
- Effect duration: 15 / 20 / 25 / 30 / 35 / 40 / 45 / 50 / 55 / 60 s
- Trigger: victim with Ambush Thorns effect receives damage
- Retaliation chance: 50%
- Retaliation formula: `20% × original incoming damage + (0.25 + 0.25 × amplifier) × entityPowerMultiplier`
- Estado Black Arcana: `JÁ EXISTE / SEM ALTERAÇÃO PLANEJADA`

## Contract

A spell aplica `AMBUSH_THORNS_EFFECT`; o handler escuta `LivingDamageEvent.Pre`. Se houver atacante vivo e o roll `Math.random() < 0.5` passar, o atacante recebe thorns damage calculado pelo provider.

Com amplifier `spellLevel-1`, a parcela base do handler antes do entity-power multiplier é 0.25 / 0.5 / 0.75 / 1.0 / 1.25 / 1.5 / 1.75 / 2.0 / 2.25 / 2.5, além dos 20% do dano original.

## Acquisition

Pool do Ancient Guardian: níveis 3–10, weight 10; global loot modifier usa chance 0.5. Crafting não é desabilitado no config.

## Regra para o Black Arcana

Não instalar segundo thorns listener ou segunda rolagem de 50% para o mesmo dano. Qualquer observação deve deduplicar pelo pipeline provider-native.

## Source

`AmbushThornsSpell.java`, `AmbushThornsEffectHandler.java` @ `Higurashi34m/Legendary-Spellbooks@62ced2f2b2693aa841251473cbbd726fdd928ed3`.

## Engenharia causal para perks — 17/10/2026

**Prova:** `legendary_spellbooks` 0.3.2, JAR `legendary_spellbooks-1.21.1+neo-0.3.2.jar` SHA-1 `bda5b1fbe50ad834a6a76ad36789743c1057ebf5`, registro 30/30 COUNTED_EXACT ([Java21 #38453654179](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38453654179)). Mecânicas a seguir são **SOURCE_CAUSALITY** do pin `Higurashi34m/Legendary-Spellbooks@62ced2f2b2693aa841251473cbbd726fdd928ed3`; igualdade byte-a-byte de código e execução com Iron's 3.16.3/Legendary Monsters 2.2.2 **não verificadas**. Nenhum adapter RPG homologado.

| Eixo | Contrato factual observado | Limite para perks |
|---|---|---|
| Cast/status | Níveis 1–10, cooldown 120s, castTime 30, mana 65+5×(nível−1); aplica AMBUSH_THORNS_EFFECT no próprio caster com amplifier=spellLevel e duration=min((10+5×level)×20,120×20) = **300..1200 ticks**. | Sem spell power base no body; efeitos downstream dependem do handler. |
| Evento/dano real | AmbushThornsEffectHandler escuta `LivingDamageEvent.Pre` da vítima com efeito; identifica atacante por event.source.entity, calcula `0.2×event.originalDamage + 0.5×(0.5+0.5×amplifier)×getEntityPowerMultiplier(victim)`; com chance Math.random()<0.5 tenta `attacker.hurt(victim.damageSources().thorns(victim),amount)`. | Pre-event não é dano liquidado, 50% chance por evento pré-settlement. Não criar procs automáticos nem outro reflected hit. |
| Alvo e tipo | Retalia sobre LivingEntity atacante identificada no DamageSource, não há AOE, raycast ou projectile; DamageSource vanilla thorns e não 'Nature' por inferência. | ⛔ conversão de DamageType/dano per-player sem seam. Não premiar sem dano retornado true. |
| Resolução | A ação de aplicar efeito é um cast, podendo ocorrer múltiplos ataques e retornos de dano enquanto buff ativo. Autocadeia/ordem com buffs de outro mod precisa QA. | Dedup por evento/causa para Mastery e caps anti-recursão. |

**Âncoras:** [AmbushThornsSpell.java](https://github.com/Higurashi34m/Legendary-Spellbooks/blob/62ced2f2b2693aa841251473cbbd726fdd928ed3/src/main/java/dev/higurashi/legendary_spellbooks/common/spells/nature/AmbushThornsSpell.java#L24-L53) · [AmbushThornsEffectHandler.java](https://github.com/Higurashi34m/Legendary-Spellbooks/blob/62ced2f2b2693aa841251473cbbd726fdd928ed3/src/main/java/dev/higurashi/legendary_spellbooks/common/effects/handler/AmbushThornsEffectHandler.java#L16-L41).

**QA e fail-closed:** QA ataque melee/magic/projétil, fonte atacante nula, PvP e reflexo recursivo, thorns cancellation, efeito e nivelamento. Não usar simples onCast/trigger como settlement e nunca duplicar custo, objeto mágico ou fonte de dano. **+0 novos spells, +0 adapters.**
