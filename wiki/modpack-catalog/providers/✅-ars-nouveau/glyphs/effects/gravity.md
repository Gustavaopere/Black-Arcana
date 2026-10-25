# Ars Nouveau — Gravity

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_gravity`
- Display name: Gravity
- School: Elemental Air
- Default tier: 2
- Default mana cost: 15
- Compatible augments: Amplify, Dampen, AOE, Pierce, Extend Time, Reduce Time (`glyph_duration_down`)
- Source default potion duration: 30 s
- Source default Extend Time increment: 8 s

## Provider-native behavior

On blocks, Gravity converts eligible targets into Ars `EnchantedFallingBlock` entities. On living entities without Extend Time it applies immediate downward velocity of `-1.0 - amplification`. With Extend Time it applies Ars' Gravity effect instead; provider documentation states this disables player flight while active and causes rapid falling with doubled fall damage.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:air_essence` + `minecraft:anvil` ×2 + `#c:feathers` ×3.
- Source-default recipe XP: **55 XP** (Tier II).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / deduplication

Ars Nouveau owns this gravity/falling control primitive and its falling-block interaction. Black Arcana Space/Displacement or forbidden-control spells must be mechanically distinct and must not replay provider motion/block conversion.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectGravity`).

## Dossiê de engenharia para perks — cadeia e interfaces

- **Source pin:** [`EffectGravity.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectGravity.java), Ars Nouveau 5.13.1.
- **Blocos:** `SpellUtil.calcAOEBlocks` com AOE/Pierce; cada candidato tenta `EnchantedFallingBlock.fall(...)`, seguido de `ShapersFocus.tryPropagateEntitySpell` quando não nulo. **Entidades:** com Extend Time aplica `ModPotions.GRAVITY_EFFECT` por `IPotionEffect`; sem ele muda movimento por `deltaMovement.add(0,-1.0-getAmpMultiplier(),0)`. **Defaults status:** potion 30 segundos, extend 8, com ticks resolvidos pelo helper. **Perks:** transformação de bloco, impulso vertical e buff/debuff são casos diferentes, com decisões do executor e world/claim owner em Ars. Não repetir efeitos via Black Arcana.
- **Estado:** ✅ classe exata lida; ⚠️ config real e Survival pendentes; mutabilidade via RPG Skill Tree ⛔ adapter seguro não validado, embora APIs provider-native existam. Ars conserva authority de recursos/efeitos.

## Certificação estática: entidades, gravidade e runa — 25/10/2026

**✅ `COMPLETE_PERK_READY` no escopo `STATIC_TECHNICAL_CATALOG_ONLY`; ⛔ `mutating_hook=NOT_VERIFIED`; ⚠️ `physical_qa=NOT_TESTED`.** A certificação é da documentação estática. A identidade de ID/classe no publisher JAR foi auditada separadamente da lógica lida no source pin.

| Campo | Contrato técnico e limite de evidência |
|---|---|
| Identidade e versão | `ars_nouveau:glyph_gravity`; `com.hollingsworth.arsnouveau.common.spell.effect.EffectGravity`; Ars Nouveau **5.13.1**, Elemental Air, tier II. Consumidores: `GravityEffect`, `IPotionEffect`, `EnchantedFallingBlock`, `ShapersFocus` [gravity-identity][gravity-identity] [gravity-duration][gravity-duration]. |
| Comportamento e causalidade | Em bloco, calcula candidatos e tenta `EnchantedFallingBlock.fall`; somente retorno não nulo passa a `ShapersFocus.tryPropagateEntitySpell`. Em `LivingEntity`, **presença de Extend Time** seleciona `GRAVITY_EFFECT`; sem essa presença soma `(0,-1-ampMultiplier,0)` à velocidade atual e marca `hurtMarked`. Reduce Time sozinho não seleciona status; Extend+Reduce com saldo zero ainda o selecionam [gravity-effect][gravity-effect]. |
| Parâmetros, escala e caps | Status por `IPotionEffect`: `ticks=base*20+extend*stats.getDurationInTicks()`, com `getDurationInTicks()=(int)(20*durationMultiplier)` [stats-duration][stats-duration] e amplifier `(int)ampMultiplier`; config default e fallback **30/8**, logo `600+8*(int)(20*durationMultiplier)` com defaults [gravity-duration][gravity-duration] [potion-helper][potion-helper]. Não há clamp local de duração/impulso. Compatíveis Amplify, Dampen, AOE, Pierce, Extend Time, Reduce Time. O downstream `GravityEffect.applyEffectTick` **não usa amplifier**: soma **−0,5 Y** por tick quando fora do chão e elegível, não `-0,5×amp` [gravity-potion][gravity-potion]. |
| Targeting, geometria, dano e duração | Blocos: grade `width=(int)(1+floor(AOE))`, `height=(int)(1+ceil(AOE))`, `depth=1+count(Pierce)`, orientada por face/direção; não é raio universal [block-grid][block-grid]. Exclui ar, fluidos, `RELOCATION_NOT_SUPPORTED`, block entities exceto mageblock/skull; exige harvest level e `destroyRespectsClaim` [fall-admission][fall-admission]. Entidade: LivingEntity já atingida, sem alcance extra. `GravityEffect` aplica a queda em todo mob no ar; para Player exige que os dois blocos abaixo sejam ar. `PlayerTickEvent.Post` desliga flight fora do chão em não-creative; `LivingDamageEvent.Pre` dobra `DamageTypes.FALL` enquanto status presente, independentemente do amplifier [gravity-potion][gravity-potion]. Dano por queda não é dano mágico direto do glyph. |
| Custos e aprendizagem | Mana default **15**, tier II, receita **55 XP**, starter default não. Receita: `ars_nouveau:air_essence` + `minecraft:anvil` ×2 + `#c:feathers` ×3 [gravity-recipe][gravity-recipe] [recipe-xp][recipe-xp]. Duração de status não é cooldown; custo/casting da composição pertencem a Ars e sua config. Source e mana de jogador não são sinônimos. |
| Integração, authority e deduplicação | A API nativa **existe**: `SpellStats.Builder.build` publica `SpellModifierEvent` com o builder original mutável [stat-build][stat-build] [modifier-event][modifier-event]; depois `EffectResolveEvent.Pre` é cancelável [resolve-event][resolve-event]. O resolver consome `stats` local e `this.hitResult`, não qualquer campo público substituído no objeto de evento [resolve-consumer][resolve-consumer]. Isso identifica superfícies para auditoria, sem provar adapter RPG Skill Tree, caps, pagamento, autoridade, target replacement ou deduplicação seguros. Black Arcana mantém sua própria `WorldEffectPolicy`, casting, Corruption e Strain. Amplifier escrito no status não prova escala de aceleração/dano no consumidor. Não repetir impulso em paralelo ao tick nativo nem duplicar FALL damage por suposta perk de gravidade. Shapers Focus pode criar child context/cancelar o atual e continuar o remainder na entidade-bloco, com reaproveitamento do delay quando presente [shapers-focus][shapers-focus]; isso exige rastrear origem, contexto e cada hit sem novo pagamento/Mastery automático. |
| Evidência e validação | Source `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`; publisher `ars_nouveau-1.21.1-5.13.1.jar`, SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`. A [auditoria binária de identidades](../../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md) prova registro ID/classe, não equivalência de todos os métodos, config instalada ou gameplay. Integração RPG/Black Arcana, ordem dos listeners, cliente/servidor e Survival: não testados. |

**Entidade-bloco e dano separado:** `fall` cria a variante apropriada (mageblock/skull/comum), guarda dados, owner/context/stats, define `baseDamage=9+damageModifier`, habilita `hurtEntities` quando há Shapers Focus e substitui o bloco pelo estado de fluido [fall-admission][fall-admission]. O construtor inicia velocidade zero; o tick normal soma **−0,04 Y** e depois aplica drag **0,98**, com descarte por tempo/limites de altura [fall-tick][fall-tick]. A fórmula local do glyph não aplica `ampMultiplier` à velocidade desse bloco, apesar da descrição genérica de Amplify/Dampen.

Quando `hurtEntities` está ativo, `onHitEntity` calcula `ceil(clamp(min(|velocity|,2.5)*baseDamage + getStateDamageBonus(),0,2.147483647E9))`, registra ID no conjunto de entidades já atingidas e usa `damageSources().thrown(this,owner)`; `getStateDamageBonus` tenta hardness e tem fallback **1** [fall-damage][fall-damage]. Não confundir esse hit com `LivingDamageEvent` de queda, nem assumir alvo/friendly-fire equivalentes aos de outros Effects. Defesa e listeners ainda determinam dano final.

**Localizadores imutáveis adicionais:**

[gravity-identity]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectGravity.java#L23-L27
[gravity-effect]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectGravity.java#L30-L81
[gravity-duration]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectGravity.java#L103-L111
[gravity-potion]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/potions/GravityEffect.java#L23-L66
[fall-admission]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/EnchantedFallingBlock.java#L130-L170
[fall-tick]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/EnchantedFallingBlock.java#L188-L233
[fall-damage]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/EnchantedFallingBlock.java#L322-L387
[block-grid]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/util/SpellUtil.java#L66-L139
[shapers-focus]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/items/curios/ShapersFocus.java#L32-L49
[potion-helper]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/IPotionEffect.java#L10-L23
[gravity-recipe]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/datagen/GlyphRecipeProvider.java#L74-L80
[stats-duration]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellStats.java#L48-L58
[stat-build]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellStats.java#L138-L152
[modifier-event]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/event/SpellModifierEvent.java#L13-L32
[resolve-event]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/event/EffectResolveEvent.java#L11-L49
[resolve-consumer]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellResolver.java#L220-L279
[cost-config]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractSpellPart.java#L127-L149
[recipe-xp]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/datagen/GlyphRecipeProvider.java#L142-L156
