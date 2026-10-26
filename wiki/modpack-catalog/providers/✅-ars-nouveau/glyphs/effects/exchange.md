# Ars Nouveau — Exchange

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_exchange`
- Display name: Exchange
- School: Manipulation
- Default tier: 2
- Default mana cost: 50
- Compatible augments: Amplify, Dampen, Pierce, AOE, Randomize

## Provider-native behavior

On entities, Exchange swaps caster and target positions, subject to teleport support/event checks. On blocks, it replaces matching target blocks with block items extracted from the Ars inventory manager while recovering the replaced block through silk-touch-like harvesting semantics. Randomize can select random eligible block items; AOE/Pierce expand the target set.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:manipulation_essence` + `minecraft:emerald_block` + `#c:ender_pearls` ×2.
- Source-default recipe XP: **55 XP** (Tier II).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / deduplication

Ars Nouveau owns both entity-position swapping and this inventory-backed block exchange transaction. Black Arcana should not clone a generic swap spell or double-consume/return blocks when Ars is causal.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectExchange`).

## Dossiê de engenharia para perks — cadeia e interfaces

- **Source pin:** [`EffectExchange.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectExchange.java), Ars Nouveau 5.13.1.
- **Entidades:** `onResolveEntity` rejeita `TELEPORTING_NOT_SUPPORTED` e `FakePlayer`; verifica `EventHooks.onEnderTeleport` separadamente em caster e alvo, de modo que um dos movimentos pode ser cancelado sem cancelar o outro (troca não necessariamente atômica). **Blocos:** `SpellUtil.calcAOEBlocks` com AOE/Pierce, equivalência de `origState.getBlock()`, harvest/protection, extração de `BlockItem` via `InventoryManager` (Randomize altera seleção); `attemptPlace` simula Silk Touch, quebra com `BlockUtil.breakExtraBlock`, coloca state, atualiza tags/components e diminui stack em sucesso. **Perks:** block volume exige budget e inventário consistente; sem segundo loot ou segundo teleporte.
- **Estado:** ✅ classe exata lida; ⚠️ helpers/config real e Survival pendentes; mutabilidade via RPG Skill Tree ⛔ sem interface comprovada que altere esses parâmetros. Ars conserva authority de recursos/efeitos.

## Certificação técnica estática — Exchange (26/10/2026)

**✅ `STATIC_TECHNICAL_CATALOG_ONLY` · ⛔ `mutating_hook=NOT_VERIFIED` · ⚠️ `physical_qa=NOT_TESTED`.** Identidade publicada `ars_nouveau:glyph_exchange` → `EffectExchange` provada na auditoria de registry/classfile do JAR `ars_nouveau-1.21.1-5.13.1.jar` SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`; **não** é equivalência binária dos métodos. Código do commit `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`: [EffectExchange.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectExchange.java), [ExtractedStack.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/item/inv/ExtractedStack.java), [BlockUtil.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/util/BlockUtil.java).

| Campo de engenharia/perk | Contrato verificado na fonte fixada e riscos |
|---|---|
| Entity swap — targeting | `onResolveEntity(EntityHitResult,...)` captura `origLoc=shooter.position`, rejeita `Tags.EntityTypes.TELEPORTING_NOT_SUPPORTED` e `entity instanceof FakePlayer`. Para mover o caster testa `EventHooks.onEnderTeleport(shooter,destino do alvo)` e se não cancelado chama `shooter.teleportTo(ServerLevel,...)`. Para mover o alvo, se for `LivingEntity`, avalia **outra** chamada `EventHooks.onEnderTeleport(living,origLoc)`; para entidades não-vivas essa segunda checagem nem ocorre. Os dois movimentos são independentes e podem ser **parciais**: não há rollback/atomicidade. |
| Geometria de blocos | `onResolveBlock` usa `SpellUtil.calcAOEBlocks(shooter,result.getBlockPos(),result,getAoeMultiplier(),count(AugmentPierce))` (largura derivada de `1+floor(AOE)`, altura de `1+ceil(AOE)`, profundidade de `1+Pierce`); lê `origState` do bloco atingido e só considera candidatos cujo `state.getBlock()` seja o **mesmo Block**, não necessariamente o mesmo BlockState/propriedades. `canBlockBeHarvested`, `IntangibleAirBlock` e `BlockUtil.destroyRespectsClaim` formam gates locais. |
| Inventário e escolha dos candidatos | `InventoryManager.extractItem` exige `BlockItem`; após a primeira extração preenche `firstBlock` e, sem `Randomize`, as demais extrações exigem `blockItem.getBlock()==firstBlock`. `Randomize` usa `extractRandomItem` e ignora essa regra de tipo consistente. **`firstBlock` é definido antes de verificar se `attemptPlace` efetivou a troca**; uma primeira tentativa recusada pode fixar o tipo de item em tentativas seguintes. |
| Settlement / mutation | `attemptPlace` monta `BlockPlaceContext` e `BlockState placeState=item.getBlock().getStateForPlacement(context)`. Aborta se `placeState==null` ou o tipo de bloco já coincide. Constrói ferramenta simulada `LootUtil.getDefaultFakeTool()` com `Enchantments.SILK_TOUCH`; só continua se `BlockUtil.breakExtraBlock((ServerLevel)world,pos1,tool,shooter.getUUID(),true)` retornar true (inclui `CommonHooks.fireBlockBreak`). Depois chama `world.setBlock(pos1,placeState,3)` **sem conferir seu boolean**, e mesmo assim chama `setPlacedBy`, `BlockItemAccessor.invokeUpdateBlockStateFromTag`, `BlockItem.updateCustomBlockEntityTag`, `invokeUpdateBlockEntityComponents`, `stack.shrink(1)` e `ShapersFocus.tryPropagateBlockSpell`. |
| Falhas, perda/duplicação e eventos | Após `attemptPlace`, sempre executa `extractedStack.replaceAndReturnOrDrop(extractedStack.getStack(),world,shooter.getOnPos())`. O método `ExtractedStack.replaceAndReturnOrDrop` é a rotina de devolução aplicada nessa etapa. Segundo [ExtractedStack.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/item/inv/ExtractedStack.java), devolve a stack restante via insert handler/slots; se falha inserção, cria `ItemEntity`. **Isso não prova transação atômica** entre quebra, colocação, componentes, consumo e devolução. `destroyRespectsClaim` é preflight `BlockEvent.BreakEvent`; `breakExtraBlock` tem veto adicional. |
| Custo e autoridade | `getDefaultManaCost()=50`; `Amplify`/`Dampen` afetam harvest threshold, `AOE`/`Pierce` volume, `Randomize` seleção. Sem cooldown específico validado. `WorldEffectPolicy` protege apenas operações próprias Black Arcana; `RPG Skill Tree` fornece progressão/Mastery/perks/gates por adapter real. Não reproduzir swap, loot Silk Touch, item shrink, teleporte ou segundo cast sem hook mutador seguro. |

**QA exigida:** dois vetos de `onEnderTeleport`, jogadores versus entidades não-vivas, teleporte interdimensional, bloqueios de claim, `setBlock=false` depois de `breakExtraBlock=true`, components/BlockEntity, drops Silk Touch, consumo e reinsert/returnOrDrop, efeitos de addons, offsets e multiplayer. `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`. Stage 06.05/09 não promovido.
