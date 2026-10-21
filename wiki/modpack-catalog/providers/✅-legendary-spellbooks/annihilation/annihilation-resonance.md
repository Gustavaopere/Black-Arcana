# Annihilation Resonance

**Prova binária física (2026-10-13):** ✅ `COUNTED_EXACT`, identidade estática `legendary_spellbooks:annihilation_resonance` / classe `dev.higurashi.legendary_spellbooks.common.spells.annihilation.AnnihilationResonanceSpell` — [Java 21 #38453654179](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38453654179), [dossiê SHA-exato](../EXACT-BINARY-SPELLS-0.3.2.md). Valores/custos descritos da fonte continuam **⚠️ sem validação runtime/Survival**; +0 raízes.

- ID: `legendary_spellbooks:annihilation_resonance`
- School: `legendary_spellbooks:annihilation`
- Levels: 1–6
- Min rarity: Rare
- Cooldown: 180 s
- Long cast field: 35 ticks
- Mana neutral: 120 / 140 / 160 / 180 / 200 / 220
- Effect duration: 25 / 30 / 35 / 40 / 45 / 50 s (`min(20 + 5×level,100)`)
- Tradeoff effect: -25% Attack Damage e -25% Armor via `ADD_MULTIPLIED_TOTAL`
- Trigger: critical hit while effect is active
- Blast radius: 3 blocks around the struck target
- Blast base formula: `4 × (1 + 0.75 × effectAmplifier) × entityPowerMultiplier`
- Looting: desabilitado
- Estado Black Arcana: `JÁ EXISTE / SEM ALTERAÇÃO PLANEJADA`

## Contract

Aplica ao caster um estado de Resonance com tradeoff ofensivo/defensivo. Critical hits disparam a explosão provider-native; o handler usa o damage source da própria spell.

## Acquisition

Pool do The Obliterator: níveis 1–4, weight 14. Crafting não é desabilitado no config.

## QA

O predicado do handler usa `!attacker.isAlliedTo(target)` como condição constante ao iterar entidades próximas, em vez de verificar aliança com cada candidata. Friendly-fire real precisa de runtime QA.

## Regra para o Black Arcana

Não criar segunda detecção de crítico ou segunda explosão para a mesma ação.

## Source

`AnnihilationResonanceSpell.java`, `AnnihilationResonanceHandler.java`, `AnnihilationResonanceEffect.java` @ source pin 0.3.2.

## Engenharia causal para perks — 17/10/2026

**Proveniência:** JAR físico `legendary_spellbooks-1.21.1+neo-0.3.2.jar`, SHA-1 `bda5b1fbe50ad834a6a76ad36789743c1057ebf5`, registro 30/30 COUNTED_EXACT ([Java 21 #38453654179](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38453654179)). Detalhes **SOURCE_CAUSALITY** em `Higurashi34m/Legendary-Spellbooks@62ced2f2b2693aa841251473cbbd726fdd928ed3`, não ABI de todos os helpers nem QA com Iron's 3.16.3/Legendary Monsters 2.2.2.

| Eixo | Contrato causal lido na fonte | Situação de perks |
|---|---|---|
| Ativação, mana e cast | `AnnihilationResonanceSpell`, `DefaultConfig` cooldown **180 segundos**, níveis **1–6**, rarity RARE, `castTime=35 ticks`, mana neutra `120+20×(level−1)`. No `onCast`, `MobEffectInstance` no caster com amplifier **igual a spellLevel**, duração `min(20+5×level,100)×20 ticks`. | Iron's controla custos/cast e início de cooldown. `⛔` alterar cast/tempo per-player sem seam do host validado. |
| Atributos | `AnnihilationResonanceEffect` atribui **−0.25 ADD_MULTIPLIED_TOTAL** tanto a `ATTACK_DAMAGE` quanto `ARMOR`. Mesmo que o efeito escale o amplifier, essas duas lambdas retornam −0.25 constante. | `NATIVE_ATTRIBUTE` de efeito pertencente ao addon; modificação per-player por RPG não comprovada. |
| Trigger | `AnnihilationResonanceHandler.onCriticalHit(CriticalHitEvent)` roda somente no servidor se `event.getTarget()` é LivingEntity e `event.isCriticalHit()`, com efeito ativo no atacante. O evento de crítico pode ocorrer antes do dano final do golpe: **não** equivale automaticamente a hit/dano confirmado. | `VERIFIED_EVENT_OR_API` apenas evento NeoForge observado em source; integração Mastery exige settle/dedup por crítico e vítima. |
| Targeting / AOE | Busca LivingEntities na **AABB do alvo atingido, inflada em 3 blocos em X/Y/Z**; exclui atacante e alvo primário. O UI exibe `radius=4`, mas o callsite causal examinado usa **inflate(3.0)**; **divergência UI vs scan**, sem interpretar como esfera 4. | `SEM_HOOK_SEGURO` para multiplicar a AABB por perk; não usar UI como authority espacial. |
| Friendly fire | Predicado no loop é `entity != attacker && entity != target && !attacker.isAlliedTo(target)`; a condição de aliança é **constante sobre target primário**, não sobre cada candidato `entity`. Consequência potencial de friendly fire precisa teste com facções/party. | `⛔` não reaplicar dano em área num adaptador; preservar claims/PvP e filtros provider. |
| Dano/tipo | Chama `DamageSources.applyDamage(enemy, 4×(1+0.75×effectAmplifier)×getEntityPowerMultiplier(attacker), spell.getDamageSource(attacker))`. O método não verifica retorno do applyDamage para creditar uma vítima nem inclui o alvo primário no blast. | Dano é **provider spell DamageSource**, não conversão elemental livre. Perks on-hit dependem de dano efetivo/correlation. |
| Área visual e vida | VFX círculo raio 3 e som após varredura; ausência de projectile de dano dedicado nesse handler. Lançar a spell uma vez pode produzir **muitos CriticalHitEvents** enquanto efeito durar. | `N/A` projectile hitbox/velocidade. 1 spell cast ≠ 1 blast ≠ 1 damage application. |

**Âncoras:** [spell default/effect](https://github.com/Higurashi34m/Legendary-Spellbooks/blob/62ced2f2b2693aa841251473cbbd726fdd928ed3/src/main/java/dev/higurashi/legendary_spellbooks/common/spells/annihilation/AnnihilationResonanceSpell.java#L22-L57); [CriticalHitEvent, targeting, dano e fórmula](https://github.com/Higurashi34m/Legendary-Spellbooks/blob/62ced2f2b2693aa841251473cbbd726fdd928ed3/src/main/java/dev/higurashi/legendary_spellbooks/common/effects/handler/AnnihilationResonanceHandler.java#L23-L65); [efeito de atributos](https://github.com/Higurashi34m/Legendary-Spellbooks/blob/62ced2f2b2693aa841251473cbbd726fdd928ed3/src/main/java/dev/higurashi/legendary_spellbooks/common/effects/AnnihilationResonanceEffect.java#L9-L14).

**QA condicionado:** teste em servidor com crítico cancelado, damage post-event, equipe A/B, PvP, mobs aliados ao alvo vs caster, 0/1/N candidatos, i-frames, redução de armadura, spell power e UI radius 4 vs AABB 3. Nenhum hook para mudar DamageType/range/performance foi homologado. **+0 raízes / +0 adapters.**
