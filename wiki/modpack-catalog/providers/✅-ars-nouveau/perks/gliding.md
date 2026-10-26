# Gliding

- Registry ID: `ars_nouveau:thread_gliding`
- Source class: `GlidingPerk`
- Minimum slot: Tier 3 (`PerkSlot.THREE`).
- Core condition: `EffectGlide.canGlide(entity)` returns true when the entity has Ars' Glide effect **or** owns at least one Gliding perk.
- Player tick integration: when Caelus is loaded and `canGlide(player)` is true, Ars calls its `CaelusHandler.setFlying(player)` path.
- Acquisition: Enchanting Apparatus; reagent `ars_nouveau:blank_thread`; 2 `ars_nouveau:air_essence` + 1 `minecraft:elytra`; `sourceCost: 0`.

## Authority / integration

Gliding is Ars-owned mobility capability and depends on the provider's Caelus integration path. Black Arcana must not create a second elytra/glide authority for this perk or charge a second resource for the same movement state.

## Evidence state

`SOURCE-PINNED 5.13.1 @ 112920ff774831f204031da75b4c4e73d3765157`. Runtime modpack QA remains appropriate for Caelus presence/behavior.

## Certificação técnica estática — Thread of Gliding (2026-10-26)

**✅ `STATIC_TECHNICAL_CATALOG_ONLY` · ⛔ `mutating_hook=NOT_VERIFIED` · ⚠️ `physical_qa=NOT_TESTED`.** Ars Nouveau `5.13.1`, JAR SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`; upstream `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`. [GlidingPerk.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/perk/GlidingPerk.java), [EffectGlide.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectGlide.java), [EventHandler.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/event/EventHandler.java), [CaelusHandler.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/compat/CaelusHandler.java), [ElytraPlayerMixin.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/mixin/elytra/ElytraPlayerMixin.java), [PerkUtil.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/util/PerkUtil.java). Os 109 IDs de glyphs/rituais **não constituem prova compilada desta perk**; `evidence_grade=PINNED_SOURCE_WITH_RELEASE_SHA_ONLY`.

| Eixo | Contrato e condicionamento |
|---|---|
| Registry/tier | `GlidingPerk.INSTANCE` usa `ars_nouveau:thread_gliding`, `minimumSlot()=PerkSlot.THREE`. A perk não aplica um atributo de voo próprio em `GlidingPerk`; o consumidor efetivo aparece fora da classe. |
| Gate híbrido | `EffectGlide.canGlide(LivingEntity entity)` retorna `entity.hasEffect(ModPotions.GLIDE_EFFECT) || PerkUtil.countForPerk(GlidingPerk.INSTANCE,entity)>0.0`. `countForPerk` é maior valor de slot Ars, não quantidade de peças somadas; spell Glide e Thread Gliding são duas formas **alternativas** de satisfazer o mesmo predicate. |
| PlayerTick + Caelus | `EventHandler.onGlideTick(PlayerTickEvent.Pre)` (priority `EventPriority.LOWEST`) executa `if(ArsNouveau.caelusLoaded && EffectGlide.canGlide(player)) CaelusHandler.setFlying(player)`. `CaelusHandler.setFlying` recupera `CaelusApi.getInstance().getFallFlyingAttribute()`, checa `attributeInstance!=null` e se ainda não possui `getElytraModifier().id()`, depois chama `addTransientModifier`. **A função inspecionada apenas adiciona e não remove o modifier**: lifetime completo/cancelamento e compatibilidade de outros mods devem ser observados na versão do Caelus/modpack. Isso não transforma o RPG Skill Tree em owner da capability de voo. |
| Mixin de elytra | `ElytraPlayerMixin.elytraOverride(boolean original)` no `Player.class`, injeção `ModifyExpressionValue` de `ItemStack.canElytraFly(LivingEntity)`, devolve `original || EffectGlide.canGlide((LivingEntity)this)`. Não equivale a conceder itens Elytra físicos, stamina Epic Fight, voo criativo nem garantia de queda segura em todos os estados. |
| Mana e integração | O glyph `EffectGlide` tem `getDefaultManaCost()=100` e configuração default potion180/extend120; **a thread em si não executa esse cast e não paga 100 mana por PlayerTick**. Receita do Enchanting Apparatus registrada no inventário-base: 2 Air Essence + 1 Elytra, `sourceCost:0`. `WorldEffectPolicy` Black Arcana não intercepta Caelus/mixin Ars. Sem mutating adapter verificado, Mastery/gates RPG Skill Tree não podem injetar um segundo elytra modifier ou cobrar segundo recurso. |

**QA pendente:** Caelus efetivamente carregado e sua versão física, remoção do modifier após tirar armadura, interação mixin com elytra de outros mods, clientes versus servidor no PlayerTick.Pre, Glide effect expirado, teleporte/dimensão, Fall Flying e stamina Epic Fight. `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`.
