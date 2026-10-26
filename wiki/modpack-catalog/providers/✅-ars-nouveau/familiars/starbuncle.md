# Starbuncle Familiar

State: `SOURCE-PINNED 5.13.1 / RUNTIME QA PENDING`

Registry id: `ars_nouveau:familiar_starbuncle`
Conversion entity: Ars Nouveau `Starbuncle`
Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Aquisição

O holder reconhece entidades `Starbuncle`. O Ritual of Binding converte uma entidade elegível em Bound Script; usar o script desbloqueia o familiar no capability Ars do jogador.

## Behavior confirmado

- A cada 60 ticks no servidor, se o owner existir, aplica `MOVEMENT_SPEED` por 600 ticks com amplifier `1` ao owner e ao próprio familiar — equivalente a Speed II enquanto o refresh continuar.
- Interação owner-only com item da tag NeoForge `NUGGETS_GOLD` consome 1 nugget fora de creative/infinite materials.
- Essa interação concede Scrying por `3 * 20 * 60 = 3600` ticks, usando `CompoundScryer` com as tags de gold ore do NeoForge e vanilla.
- Também aceita determinadas dyes/cores próprias do Starbuncle para alterar a variante visual.

## Authority e deduplicação

- O Speed refresh, consumo do nugget, persistent familiar ownership e Scrying são Ars-owned.
- O Scrying concedido reutiliza `RitualScrying.grantScrying`; Black Arcana não deve criar um segundo estado de descoberta/visão para o mesmo efeito.
- O familiar não é equivalente à entidade Starbuncle usada em logística/automação. A entidade base é apenas a entidade de conversão do Binding.

## QA pendente

1. Validar refresh de Speed II e remoção ao unsummon/morte/owner unload.
2. Confirmar coexistência de gold-ore Scrying com outros scryers ativos.
3. Validar o consumo do nugget e persistência após relog/chunk unload.

## Certificação técnica estática — Starbuncle (2026-10-26)

**✅ `STATIC_TECHNICAL_CATALOG_ONLY` · ⛔ `mutating_hook=NOT_VERIFIED` · ⚠️ `physical_qa=NOT_TESTED`.** Mod/JAR físico Ars Nouveau `5.13.1`, SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`; fonte `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`. **Os 109 IDs compilados auditados são glyphs/rituais, não este familiar**. [FamiliarStarbuncle.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/familiar/FamiliarStarbuncle.java), [StarbuncleFamiliarHolder.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/familiars/StarbuncleFamiliarHolder.java), [FamiliarEntity.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/familiar/FamiliarEntity.java), [FamiliarEvents.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/event/FamiliarEvents.java).

| Eixo | Contrato source-pinned |
|---|---|
| Identidade | `StarbuncleFamiliarHolder` converte `Starbuncle` em holder `LibEntityNames.FAMILIAR_STARBUNCLE`; sua invocação cria `FamiliarStarbuncle(ModEntities.ENTITY_FAMILIAR_STARBUNCLE.get(),world)`. A entidade familiar não é o Starbuncle de logística. |
| Buff periódico | `FamiliarStarbuncle.tick()`, no servidor quando `level.getGameTime()%60==0` e owner resolvido, aplica `MobEffects.MOVEMENT_SPEED` durante **600 ticks** com amplifier **1** (Speed II) a owner e familiar; não confundir cadência de refresh com duração total. |
| Reagente | `mobInteract` exige servidor e `player.equals(getOwner())`; `Tags.Items.NUGGETS_GOLD` é consumida em 1 unidade se não houver `hasInfiniteMaterials`; chama `RitualScrying.grantScrying((ServerPlayer)player,3*20*60,new CompoundScryer(TagScryer(Tags.Blocks.ORES_GOLD),TagScryer(BlockTags.GOLD_ORES)))`. O scrying de ouro dura **3600 ticks**; seu estado/visibilidade é Ars-owned. |
| Dye e persistência | `Tags.Items.DYES` com cor em `Starbuncle.carbyColors` chama `setColor`; neste ramo não há `stack.shrink`. `FamiliarEntity` persiste `ownerID`, `holderID`, `terminated` e `PersistentFamiliarData` (`name/color/cosmetic`); owner não resolvido provoca remoção em checagem de 20 ticks servidor. |
| Integração/custo | `FamiliarEvents.maxManaCalc` acrescenta `manaReserveModifier=0.15` para primeiro familiar correspondente e retorna, sem soma por quantidade arbitrária. Não criar segundo Speed/Scrying ou Mastery por refresh. `WorldEffectPolicy` BA aplica-se apenas ao seu runtime; RPG Skill Tree fornece progressão por contrato real. |

**QA:** interações multiplayer, gold-ore tags de outros mods, Scrying combinado, Speed sob unload/relog, contador de ticks, variação de cor, consumo de item e callbacks provider-native. `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`. Sem mudança de Stage.
