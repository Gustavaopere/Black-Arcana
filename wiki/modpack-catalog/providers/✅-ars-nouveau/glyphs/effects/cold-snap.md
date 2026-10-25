# Ars Nouveau — Cold Snap

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_cold_snap`
- Display name: Cold Snap
- School: Elemental Water
- Default tier: 2
- Default mana cost: 30
- Compatible augments: Amplify, Dampen, Extend Time, Reduce Time (`glyph_duration_down`), AOE, Fortune, Randomize
- Default Amplify limit: 2
- Default AOE limit: 1
- Source default base damage: 6
- Source default Amplify scalar: +2.5 damage
- Source default Snare duration: 5 s
- Source default Extend Time increment: 1 s

## Provider-native behavior

Cold Snap only damages living targets that are wet/rained-on, slowed, or already freezing. Accepted direct damage applies Ars Snare; an eligible target erupts `IceShardEntity` carriers even when the direct damage attempt fails or is canceled. Targets with Ars Freezing are pushed to maximum freeze immediately. Casting on an ice block removes that ice and erupts shards instead. AOE increases shard coverage.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:water_essence` + `minecraft:powder_snow_bucket` + `minecraft:ice`.
- Source-default recipe XP: **55 XP** (Tier II).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / deduplication

Ars Nouveau owns this condition-gated cold burst, its Snare/Freezing interactions and ice-shard entities. Black Arcana cold/death/control concepts must not clone this wet/frozen-triggered pattern.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectColdSnap`).

## Engenharia para perks — caminho causal individual

- **Fonte exata:** [`EffectColdSnap.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectColdSnap.java), `com.hollingsworth.arsnouveau.common.spell.effect.EffectColdSnap` (Ars 5.13.1).
- **Admissão e dano:** entidade precisa de `LivingEntity` no `ServerLevel` e `canDamage(living)` = água/chuva, `MOVEMENT_SLOWDOWN` ou `getPercentFrozen()>0`. Dano nominal `DAMAGE+AMP_VALUE*ampMultiplier` (defaults 6.0 e 2.5), por `IDamageEffect.attemptDamage`; só se este retornar true, aplica Snare com `20*(int)(POTION_TIME+EXTEND_TIME*durationMultiplier)` ticks (defaults 5 e 1).
- **Shards downstream:** `spawnIce` é invocado após `damage` mesmo quando `attemptDamage` não registrou sucesso, desde que `canDamage` tenha admitido o alvo. Seleciona posições substituíveis com loops `1 <= i < 2+AOE`; cada `IceShardEntity` recebe `baseDamage=(DAMAGE+AMP_VALUE*ampMultiplier)*0.5`, vetor para fora do centro, `cancelDrop=true`, `dropItem=false`, `hurtEntities=true`; `ShapersFocus.tryPropagateEntitySpell` pode ser chamado.
- **Ramo gelo:** se hit block pertence a `BlockTags.ICE`, substitui por `AIR` e invoca shards; não foi visto claim gate local neste trecho, exigindo verificar o `SpellResolver` e políticas do provider antes de concluir bypass. Freezing effect preexistente resulta em `setTicksFrozen(ticksRequiredToFreeze+3)`.
- **Perks:** raw damage, aplicação Snare, congelamento completo, shard spawn e dano posterior são fases distintas; impor limites de entidades/positions, evitar proc por cada shard independente.
- **Estado:** ✅ assinatura/fórmula do source pin; ⚠️ config carregada, auxiliar e testes físicos pendentes. Contratos de `EffectResolveEvent.Pre` são existentes, porém o adapter RPG, clamps, causalidade e escrita externa **não** foram validados: ⛔ fail-closed até testes.

## Certificação estática: dano e propagação — 25/10/2026

**✅ Contrato técnico estático documentado; ⛔ `mutating_hook=NOT_VERIFIED`; ⚠️ `physical_qa=NOT_TESTED`.** O ✅ não representa perk implementada, correspondência integral de bytecode ou QA em jogo.

| Campo | Contrato e limites source-pinned |
|---|---|
| Identidade e versão | `ars_nouveau:glyph_cold_snap`, `com.hollingsworth.arsnouveau.common.spell.effect.EffectColdSnap`, Ars Nouveau **5.13.1**, Elemental Water, tier II; [classe/ID][cold-resolve]. |
| Comportamento e causalidade | `onResolveEntity` exige `LivingEntity` em `ServerLevel`, depois água/chuva, Slowness ou percentual já congelado. A tentativa de dano e o Snare são separados da geração de shards e do congelamento máximo: somente o Snare depende de dano aceito. `onResolveBlock` em `BlockTags.ICE` remove o bloco e gera shards. [Callbacks][cold-resolve], [gate/dano][cold-damage]. |
| Parâmetros, fórmulas e caps | `D=DAMAGE+AMP_VALUE*a`, defaults **6+2,5a**; `snareTicks=20*(int)(POTION_TIME+EXTEND_TIME*t)`, defaults **20*(int)(5+t)**; sem clamp de duração local. Shards recebem `baseDamage=0,5D`. AOE altera posições/quantidade por `i=1; i<2+q; i++`, não um raio universal. Caps default Amplify **2**, AOE **1**, não tetos incondicionais de gameplay. [Config/augments][cold-config], [geração][cold-shards], [config de caps][augment-config]. |
| Targeting, geometria e resultado | Alcance e aquisição são da Form; o glyph não tem raycast, LOS ou projétil de entrega próprio. Entidade usa sua posição real (`safelyGetHitPos`), elevada um bloco se grounded para a origem dos shards. IceShard usa hitbox default **0,98×0,98**; impacto e quebra têm fórmulas/fontes distintas, detalhadas abaixo. Dano direto `DamageTypesRegistry.COLD_SNAP` = `ars_nouveau:frost`; tag gerada `minecraft:is_freezing` não fixa o datapack instalado. [DamageType][damage-types], [registro][shard-size], [tag][freezing-tag]. |
| Custos e aprendizagem | Mana default **30**, tier II, receita `water_essence + powder_snow_bucket + ice`, XP default **55**, starter **não**; [receita][cold-recipe], [XP][recipe-xp], [aquisição](../../ACQUISITION.md). Mana é do jogador Ars, não Source; valor configurado e custo da composição/discounts não são 30 garantidos. Nenhum cooldown autônomo nesta classe; Snare/shard lifetime não são cooldown de cast. |
| Integração e autoridade | Ars Nouveau mantém casting, custo, status e entidades. [SpellModifierEvent via Builder][stats-builder] e [EffectResolveEvent.Pre][resolve-event] são superfícies públicas reais; [SpellResolver][resolve-pipeline] usa o `stats` local e não relê substituições do campo `preEvent.spellStats`. Cancelar Pre pula este Effect, não equivale a reverter efeitos anteriores. API existente não certifica adapter RPG Skill Tree/Black Arcana: `mutating_hook=NOT_VERIFIED`. Black Arcana mantém casting, Corruption, Strain e WorldEffectPolicy próprios; RPG Skill Tree só fornece progressão por contrato comprovado. Para dano direto há ainda [SpellDamageEvent.Pre/Post][damage-event], mas cancelar esse dano **não** impede as etapas posteriores do mesmo callback. Debuff e shards não podem ser contabilizados como novos casts. |
| Evidência e validação | `PINNED_SOURCE_PLUS_SHA_EXACT_BINARY_IDENTITY`, source `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`, publisher `ars_nouveau-1.21.1-5.13.1.jar` SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`; [auditoria compilada](../../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md) prova **ID/classe**, não equivalência integral dos métodos. Config instalada, todos os listeners, cliente/servidor físico e resultado em modpack não foram testados: `physical_qa=NOT_TESTED`. |

### Dois caminhos de dano do IceShard

- **Dano direto do glyph:** [IDamageEffect.attemptDamage][damage-pipeline] rejeita alvo morto/aliado, soma `stats.damageModifier` e `PerkAttributes.SPELL_DAMAGE_BONUS`, aplica Randomize como `count*random[-1,1]`, grava Fortune no SpellDamageSource e publica `SpellDamageEvent.Pre`. Relê `damageSource` e `damage`; retorna false se cancelado, dano não positivo ou `hurt` falhar; Post só ocorre após sucesso. Essa proteção não substitui o gate wet/slowed/frozen do glyph.
- **Shards/freeze independentes do sucesso de dano:** [EffectColdSnap][cold-resolve] chama `spawnIce` depois de `damage(...)` retornar mesmo quando houve veto, resistência ou falha em `hurt`. Se o alvo admitido ainda tiver `FREEZING_EFFECT`, faz `setTicksFrozen(getTicksRequiredToFreeze()+3)`; a mera presença desse efeito sem nenhum critério de `canDamage` não garante admissão. Não presumir que cancelar `SpellDamageEvent.Pre` cancela o pacote inteiro.
- **Construção e movimento:** [spawnIce][cold-shards] percorre quatro colunas laterais e quatro diagonais para cada `i`, mais coluna central de Y −1 a +1, deduplicando cada grupo em `HashSet`; só posições `canBeReplaced` geram entidade. Vetores saem do centro e são multiplicados por `(0,2;0,3;0,2)` nos lados ou `(0,1;0,2;0,1)` nas diagonais/centro. No default `q=0` e ambiente totalmente substituível são **27** shards; com `q=1`, **67**. Contagem real cai com obstáculos. A classe põe AIR na posição usada, seta `cancelDrop=true`, `dropItem=false`, `hurtEntities=true` e atribui `shooter`; não chama `setOwner(shooter)` nesses construtores/spawn.
- **Impacto herdado:** [EnchantedFallingBlock.onHitEntity][falling-hit] calcula `ceil(clamp(min(speed,2,5)*baseDamage+getStateDamageBonus(),0,2147483647))`, marca o ID no conjunto de ignorados **antes** de `hurt`, usa `damageSources().thrown(this,getOwner())` e não chama `IDamageEffect`/`SpellDamageEvent` do Ars. O `shooter` extra do IceShard não é automaticamente seu `getOwner()`. Após hit aceito em LivingEntity, `doPostHurtEffects` aplica Slowness **60 ticks**, amplifier **1**. A filtragem de aliados do dano direto não deve ser presumida no impacto herdado.
- **Quebra após queda:** [IceShard.callOnBrokenAfterFall][ice-shard] consulta LivingEntities na **AABB do bloco da posição inflada 1,25**, não esfera euclidiana; exclui `living==shooter` e `isAlliedTo(shooter)`, chama `hurt(frost,baseDamage)` diretamente e aplica Slowness 60 ticks/amplifier1 sem verificar o boolean de `hurt`. Esse dano também não passa por `SpellDamageEvent`. O caminho de [groundBlock][falling-ground] com `cancelDrop` descarta a entidade e chama esse callback; lifespan herdado descarta após `time>600` ou condição fora da altura após `time>100`, sem garantia de callback em toda remoção. [Tick][falling-tick].
- **Propagação:** [ShapersFocus.tryPropagateEntitySpell][shapers] pode criar contexto filho, cancelar a continuação do pai e resolver/agendar o resto da cadeia sobre cada falling entity. Resolver compartilhado, dano direto, impacto, quebra e criança exigem identidade causal e budget de entidades; alterar tamanho/velocidade não é um setter de range no glyph. Não há claim gate local no `setBlock(AIR)` do ramo gelo/posições; listeners/capabilities do resolver e proteção efetiva do pack continuam a ser validados, sem concluir bypass universal.

**Validade:** mudança de JAR, source, configuração, datapack ou listeners exige reauditoria. Nenhuma mutação executável foi implementada neste lote.

[damage-pipeline]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/IDamageEffect.java#L24-L78
[damage-event]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/event/SpellDamageEvent.java#L11-L43
[resolve-pipeline]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellResolver.java#L214-L270
[resolve-event]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/event/EffectResolveEvent.java#L11-L50
[stats-builder]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellStats.java#L138-L152
[general-defaults]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractSpellPart.java#L128-L150
[augment-config]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractSpellPart.java#L247-L255
[recipe-xp]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/datagen/GlyphRecipeProvider.java#L142-L157
[cold-resolve]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectColdSnap.java#L34-L66
[cold-shards]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectColdSnap.java#L68-L129
[cold-damage]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectColdSnap.java#L131-L147
[cold-config]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectColdSnap.java#L149-L201
[cold-recipe]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/datagen/GlyphRecipeProvider.java#L59-L59
[ice-shard]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/IceShardEntity.java#L24-L58
[shard-size]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/setup/registry/ModEntities.java#L265-L268
[falling-hit]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/EnchantedFallingBlock.java#L322-L391
[falling-ground]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/EnchantedFallingBlock.java#L235-L266
[falling-tick]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/EnchantedFallingBlock.java#L188-L233
[shapers]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/items/curios/ShapersFocus.java#L32-L49
[damage-types]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/setup/registry/DamageTypesRegistry.java#L12-L16
[freezing-tag]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/generated/resources/data/minecraft/tags/damage_type/is_freezing.json#L1-L8
