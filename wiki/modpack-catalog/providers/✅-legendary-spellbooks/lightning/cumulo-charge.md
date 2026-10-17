# Cumulo Charge

**Prova binária física (2026-10-13):** ✅ `COUNTED_EXACT` — `legendary_spellbooks:cumulo_charge`, classe `dev.higurashi.legendary_spellbooks.common.spells.lightning.CumuloChargeSpell` ([Java 21 #38453654179](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38453654179); [dossiê SHA-exato](../EXACT-BINARY-SPELLS-0.3.2.md)). Valores e mecânicas source-pinned; runtime/Survival ⚠️; +0 raízes.

- ID: `legendary_spellbooks:cumulo_charge`
- School: Lightning
- Levels: 1–3
- Min rarity: Legendary
- Cooldown: 15 s
- Cast-time field: 40 ticks
- Mana neutral: 200 / 250 / 300
- Spell power neutral: 10 / 18 / 26
- Target helper range: 48 blocks
- Entity duration: 120 / 140 / 160 ticks
- Crafting: desabilitado
- Estado Black Arcana: `JÁ EXISTE / SEM ALTERAÇÃO PLANEJADA`

## Contract

Spawna `CumuloChargeEntity` com target opcional e duração `min(100 + 20 × spellLevel,300)`. Projectile/entity logic, chain/effect resolution and damage source remain provider-native.

## Acquisition

Pool do Cloud Golem: níveis 1–3, weight 12. O Stormbound Grimoire possui afinidades para Cumulo Charge em SUNNY e THUNDER.

## Regra para o Black Arcana

Não criar segundo projectile, chain callback ou target resolver para o mesmo cast.

## Source

`CumuloChargeSpell.java`, `CumuloChargeEntity.java`, `StormboundSpellbookItem.java` @ source pin 0.3.2.

## Engenharia causal para perks — 17/10/2026

**Proveniência:** identificação física `legendary_spellbooks-1.21.1+neo-0.3.2.jar`, SHA-1 `bda5b1fbe50ad834a6a76ad36789743c1057ebf5` (30/30 registros). Corpo de método proveniente de `Higurashi34m/Legendary-Spellbooks@62ced2f2b2693aa841251473cbbd726fdd928ed3` com nível de evidência **SOURCE_CAUSALITY**. Não equivale a QA do pack Iron's 3.16.3/Legendary Monsters 2.2.2 nem a assinatura de adapter RPG homologada.

| Eixo | Mecanismo verificado | Status de mutação |
|---|---|---|
| Admissão e targeting | `checkPreCastConditions` chama `Utils.preCastTargetHelper(level, caster, magicData, spell, 48, 1.0f, false)` e retorna true. `onCast` tenta `TargetEntityCastData.getTarget(ServerLevel)`; target pode ser null. Não há `canBeCastedBy` custom nesta classe. | Targeting **host owned**, range de aquisição **48 blocos** (parâmetro ao helper), não alcance de explosão. ⛔ retarget per-player sem seam. |
| Custo/stats | Níveis 1–3, cooldown 15s, castTime 40 ticks; mana `200+50×(level−1)`, power `10+8×(level−1)`. Cria `CumuloChargeEntity` com caster, target, damage=power e duration `min(100+20×level,300)` → **120/140/160 ticks**. | Config/custo no Iron's; nenhum gasto secundário. |
| Posição e movimento | Spawn usa `GeometryUtils.getRelativePos(caster,-1.0,0.5,0)`; entidade possui `HORIZONTAL_SPEED=0.8`, `FALL_SPEED=-0.1`, `HOMING_STRENGTH=0.1` (lerp horizontal para target válido). Sem alvo, move segundo yaw existente; não é teleporte ou projectile direct magic padrão. | `SEM_HOOK_SEGURO` para turn rate, velocidade, range ou capacidade de mudar target. |
| Colisão / AOE | A cada tick server consulta `getBoundingBox().inflate(0.8)` para primeiro alvo válido. Ao hit, marca `DATA_HAS_HIT=true`, redefine duração para **15 ticks**, pára movimento e busca vítimas numa AABB `inflate(4)`, aplicando filtro adicional `distanceTo(charge)<=4` (raio real da seleção final). | Efeitos podem alcançar N vítimas num impacto; sem hook seguro para raio, hitbox ou alvo. |
| DamageType/status | `performHit` usa `damageSources().mobAttack(summoner != null ? summoner : this)`, **não** `spell.getDamageSource`; chama `hurt(damage)`, aplica `STUN` **20 ticks mesmo sem testar retorno de hurt**, e modifica velocidade. É relevante para perks por tipo e Mastery: a escola Lightning da spell **não prova** `DamageType` Lightning. | **⛔** não atribuir procs de spell damage por inferência de school; conferir o evento de dano no runtime. |
| Knockback source | Em `performHit`, velocity é zerada antes do cálculo `this.getDeltaMovement().multiply(1.5,1,1.5).add(0,0.4,0)`; portanto no source a componente calculada a partir da velocidade é **zero**, restando `+0.4 Y` quando se aplica à vítima. Não declarar empurrão horizontal pretendido sem teste. | Diferença entre implementação observada e efeito desejado; adaptar gravity/knockback exige contrato. |
| Lifetime/custo de jogo | Após hit, permanece estacionária por até 15 ticks pós-impacto e encerra no timeout; anti-magic chama `discard()`. Cada cast cria uma única charge raiz. | Não creditar STUN/knockback como cast novo; proteção, damage per victim e cleanup precisam QA. |

**Âncoras:** [CumuloChargeSpell — casting e helpers](https://github.com/Higurashi34m/Legendary-Spellbooks/blob/62ced2f2b2693aa841251473cbbd726fdd928ed3/src/main/java/dev/higurashi/legendary_spellbooks/common/spells/lightning/CumuloChargeSpell.java#L26-L88); [CumuloChargeEntity — física, hit e dano](https://github.com/Higurashi34m/Legendary-Spellbooks/blob/62ced2f2b2693aa841251473cbbd726fdd928ed3/src/main/java/dev/higurashi/legendary_spellbooks/common/entities/spell/projectile/CumuloChargeEntity.java#L24-L145); [anti-magic e ownership](https://github.com/Higurashi34m/Legendary-Spellbooks/blob/62ced2f2b2693aa841251473cbbd726fdd928ed3/src/main/java/dev/higurashi/legendary_spellbooks/common/entities/spell/projectile/CumuloChargeEntity.java#L211-L237).

**QA:** source `mobAttack` vs magia Lightning no JAR real, status STUN em dano cancelado, target null, owner/friendly-fire, knockback vertical only, PvP, entity lifetime 120–160 vs 15 pós-hit, unload e multiplicidade de hits. **+0 novas raízes.**
