# Conjure Magelight

- Registry ID: `ars_nouveau:glyph_light`
- Source class: `EffectLight`
- School: Conjuration
- Default tier: **1**
- Default mana: **25**
- Exact source: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Source-pinned behavior

On blocks, creates provider light blocks after claim/bounds/collision checks; without a duration modifier the light is persistent, while time modification selects the temporary-light block path. Amplify/Dampen adjust provider light level. On living entities it applies Night Vision and, subject to caster/Sensitive conditions, Glowing. Sensitive can apply the spell color to Glowing.

Compatible augments: Amplify, Reduce Time, Dampen, Extend Time, Sensitive. Amplify and Sensitive are limited to 1 by default.

## Acquisition / learning

- Provider-generated Glyph recipe: `minecraft:lantern` + `minecraft:torch`.
- Source-default recipe XP: **27 XP** (Tier I).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Boundary

Ars Nouveau owns Magelight blocks, potion effects, color presentation and provider config. Black Arcana lighting/world placement must remain policy-controlled and must not duplicate persistent provider lights without a distinct requirement.

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME+CONFIG QA PENDING`.

## Engenharia para perks — caminho causal individual

- **Fonte versionada:** [`EffectLight.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectLight.java), Ars Nouveau 5.13.1.
- **Ramo entidade:** se alvo implementa `ILightable`, chama `onLight` independentemente de ser LivingEntity. Para alvo vivo aplica `NIGHT_VISION` sempre; aplica `GLOWING` quando alvo != shooter ou Sensitive, e com Sensitive+Glowing confirmado envia `PacketUpdateGlowColor` baseado nas cores do spell.
- **Ramo bloco:** calcula posição adjacente à face e exige `BlockUtil.destroyRespectsClaim` nessa posição. Pode acionar `ILightable` no bloco original/BlockEntity, ou mudar o texto luminoso de um `SignBlockEntity`. Quando posição é replaceable, unobstructed e in-bounds, cria `LIGHT_BLOCK` permanente se `durationMultiplier==0`, senão `T_LIGHT_BLOCK` temporário com `TempLightTile.lengthModifier`.
- **Luminosidade:** valor clamped por `Math.max(0,Math.min(15,14+(int)ampMultiplier))`; config default potion 30s, ExtendTime 8s, Amplify e Sensitive max 1. **Perks:** luz bloco, Night Vision, Glowing e packet de cor são ramos independentes; uma perk não pode inferir Glow quando caster sem Sensitive.
- **Estado:** ✅ source pin com métodos/fórmulas; ⚠️ auxiliaries, config real e Survival QA pendentes. API de `EffectResolveEvent.Pre` existe, mas adapter RPG para este glyph não foi implementado/testado; sem duplicação de custo/efeito/WorldEffectPolicy.

## Certificação técnica estática — Conjure Magelight (25/10/2026)

**✅ `STATIC_TECHNICAL_CATALOG_ONLY` · ⛔ `mutating_hook=NOT_VERIFIED` · ⚠️ `physical_qa=NOT_TESTED`.** Registry `ars_nouveau:glyph_light` ↔ `EffectLight` em publisher `ars_nouveau-1.21.1-5.13.1.jar`, SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`, **identidade classe/ID apenas**. Fontes `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`: [EffectLight.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectLight.java), [TempLightTile.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/block/tile/TempLightTile.java).

| Eixo de integração | Condição no source fixado |
|---|---|
| Entidades e potions | `onResolveEntity` chama `ILightable.onLight` se a interface existir mesmo quando alvo não é `LivingEntity`. Para alvo vivo aplica `MobEffects.NIGHT_VISION`; aplica `MobEffects.GLOWING` se `!shooter.equals(living)||spellStats.isSensitive()`. Só quando Glowing está presente **e** Sensitive, envia `PacketUpdateGlowColor` via `Networking.sendToNearbyClient`, com cor padrão ou `RainbowParticleColor ? -1`. Portanto Night Vision, Glowing e pacote de cor são três resultados condicionais distintos; default `addPotionConfig(builder,30)` e `addExtendTimeConfig(builder,8)`, segundos apenas mediante contrato da configuração de potion. |
| Mutação de bloco e claims | `onResolveBlock` calcula `pos=hitPos.relative(direction)` e chama `BlockUtil.destroyRespectsClaim(player,world,pos)` **antes** de lidar com `ILightable` do bloco original, ou `SignBlockEntity` na posição adjacente. A verificação é na posição de destino, não necessariamente no `BlockEntity` de origem. Se `ILightable` do bloco/BE original atua, retorna sem colocar luz. Se é `SignBlockEntity` na posição adjacente, executa `sign.updateText` e `GameEvent.BLOCK_CHANGE`, mas **continua** para o branch opcional de colocação. |
| Bloco permanente/temporário | Se `world.getBlockState(pos).canBeReplaced()`, `world.isUnobstructed(LIGHT_BLOCK,...CollisionContext.of(ANFakePlayer))` e `world.isInWorldBounds(pos)`, coloca `LIGHT_BLOCK` se `getDurationMultiplier()==0`; caso contrário `T_LIGHT_BLOCK`. Define `WATERLOGGED` por `world.getFluidState(pos).getType()==Fluids.WATER`, intensidade `SconceBlock.LIGHT_LEVEL=Math.max(0,Math.min(15,14+(int)getAmpMultiplier()))`. O `setBlockAndUpdate` **não tem retorno conferido**, embora faça `LightTile.setTimeline` quando BE encontrada e `sendBlockUpdated`. |
| Timer / NBT de luz | `TempLightTile.tick` usa lado servidor, incrementa `age` e, se `age>(20*15+20*5*lengthModifier)`, destrói/remove bloco; `age` e `modifier` persistem por NBT. A escolha temporária depende de `durationMultiplier !=0`, mas o campo não é `Age` de um status de entidade. Não assumir wall-clock em chunks descarregados, persistência de packet color nem coexistência com provider light permanente. |
| Custos e ownership | `getDefaultManaCost()=25`; compatíveis `Amplify`, `AugmentDurationDown`, `Dampen`, `ExtendTime`, `Sensitive`. `getBaseDuration` fallback30, `getExtendTimeDuration` fallback8 sob config nula; valores carregados não inspecionados. Nenhum hook de reescrever luz/status/pacotes externamente é comprovado. `WorldEffectPolicy` governa world effects BA, não callbacks Ars; RPG Skill Tree somente progression/Mastery/perks/gates por contrato real. |

**QA pendente:** flags waterlogged, duração negativa/config, claims em Sign/ILightable versus destino, sucesso do retorno de `setBlockAndUpdate`, formação de Tile, packets Glowing cor, clientes distantes, reload NBT/chunk, timers e custo real. `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`.
