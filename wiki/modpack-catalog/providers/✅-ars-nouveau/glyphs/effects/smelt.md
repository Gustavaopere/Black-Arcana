# Ars Nouveau — Smelt

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_smelt`
- Display name: Smelt
- School: Elemental Fire
- Default tier: 2
- Default mana cost: 100
- Compatible augments: Amplify, Dampen, AOE, Pierce, Sensitive

## Provider-native behavior

Smelt processes blocks through normal smelting recipes and world items through recipe lookup. Source caps item processing at `round(4 * (1 + AOE multiplier + Pierce count))`. Sensitive limits the effect to item entities. Dampen switches item processing to Smoking recipes; Amplify switches item processing to Blasting recipes and also raises harvest capability for block targets. Claim/harvest checks precede block conversion.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:fire_essence` + `minecraft:blast_furnace` ×4 + `#c:rods/blaze`.
- Source-default recipe XP: **55 XP** (Tier II).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / deduplication

Ars Nouveau owns this remote magical processing path. Black Arcana must not double-convert blocks/items or duplicate output generation when Ars is causal. A separate Black Arcana transmutation effect would require a materially different forbidden-magic contract, not a cosmetic furnace replacement.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectSmelt`).

## Dossiê de engenharia para perks — classe de efeito

- **Source pin:** [`EffectSmelt.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectSmelt.java), Ars Nouveau 5.13.1.
- **Geometria e volume:** `maxItemSmelt=(int)Math.round(4*(1+aoeMultiplier+count(Pierce)))`; percorre `ItemEntity` em AABB `inflate(aoeMultiplier+1)`, limitando por *unidades processadas*, não por entidades. Sensitive em bloco força caminho de itens; sem Sensitive percorre `SpellUtil.calcAOEBlocks` e `smeltBlock`.
- **Receitas:** blocos usam `RecipeType.SMELTING` e `canBlockBeHarvested` + `destroyRespectsClaim`; resultado BlockItem muda estado, resultado não-bloco remove e solta item. Em itens: Dampen prioriza `SMOKING`; senão Amplify `BLASTING`; senão `SMELTING`. A cada unidade processada reduz stack original em 1 e emite `ItemEntity` do resultado.
- **Perks:** aumentar AOE/Pierce altera tanto cap de itens quanto geometria; receitas/outputs e claim checks pertencem ao provider. Não usar esse caminho para duplicação de item, nem confundir item-per-second com magic damage.
- **Status:** ✅ source exato lido; ⚠️ entidade auxiliar, caps runtime e Survival requerem testes; API por efeito não foi validada contra RPG/Black Arcana. Sem autorização para segunda liquidação de dano/recurso/target.

## Certificação técnica estática — Smelt (26/10/2026)

**✅ `STATIC_TECHNICAL_CATALOG_ONLY` · ⛔ `mutating_hook=NOT_VERIFIED` · ⚠️ `physical_qa=NOT_TESTED`.** `ars_nouveau:glyph_smelt` → `EffectSmelt` provado somente quanto à associação classe/ID no publisher JAR `ars_nouveau-1.21.1-5.13.1.jar` SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`, não equivalência do bytecode do método. Código upstream fixado `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`: [EffectSmelt.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectSmelt.java), [BlockUtil.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/util/BlockUtil.java).

| Campo de engenharia | Semântica executável observada na fonte e limites |
|---|---|
| Seleção de destino e volume | `onResolveEntity` consulta `ItemEntity` em `new AABB(entity.blockPosition()).inflate(aoeBuff+1.0)`. `onResolveBlock` consulta itens próximos ao bloco quando `spellStats.isSensitive()`, senão `SpellUtil.calcAOEBlocks(shooter,pos,hit,spellStats)` e `smeltBlock`. Para os dois ramos de itens: `maxItemSmelt=(int)Math.round(4*(1+aoeBuff+count(AugmentPierce)))` — limite em **unidades processadas** de ItemStack, não entidades. |
| Admissão de bloco | `smeltBlock` exige `canBlockBeHarvested(spellStats,world,pos)` e `BlockUtil.destroyRespectsClaim(getPlayer(shooter,(ServerLevel)world),world,pos)`. `destroyRespectsClaim` publica `BlockEvent.BreakEvent` com fake player, não é uma transação. Busca receita `RecipeType.SMELTING` via `getRecipeFor(...,new SingleRecipeInput(new ItemStack(state.getBlock().asItem(),1)),world)`, mesmo com Amplify/Dampen; esses augments **não** trocam recipe type do bloco. |
| Resultado BlockItem | `RecipeHolder<SmeltingRecipe>` com resultado não-vazio do tipo `BlockItem` executa `world.setBlockAndUpdate(pos,block.defaultBlockState())` e depois `ShapersFocus.tryPropagateBlockSpell`. O método **ignora o boolean de setBlockAndUpdate**, portanto não garante mutação persistida nem autoriza Mastery por “bloco convertido” sem observação real. |
| Resultado item e risco crítico | Quando o resultado **não** é BlockItem, chama `BlockUtil.destroyBlockSafely(world,pos,false,shooter)` e **não verifica o boolean de retorno**. Independentemente de o segundo `BlockEvent.BreakEvent` impedir a remoção, executa `world.addFreshEntity(new ItemEntity(...,itemstack.copy()))`, `BlockUtil.safelyUpdateState` e `ShapersFocus.tryPropagateBlockSpell`. Assim, há **possibilidade condicionada** de geração de output sem destruição confirmada; não é exploit comprovado do pack, mas bloqueia qualquer perk mutadora de duplicação/reciclagem sem integração transacional e QA. |
| Receitas de itens | `smeltItems` escolhe `RecipeType.SMOKING` primeiro se `spellStats.hasBuff(AugmentDampen.INSTANCE)`, senão `RecipeType.BLASTING` se Amplify, senão `RecipeType.SMELTING`; prioridade Dampen sobre Amplify (`AugmentAmplify`). Obtém `result.copy()` e, para cada unidade com limite, chama `itemEntity.getItem().shrink(1)`, `world.addFreshEntity(new ItemEntity(...,result.copy()))`, `numSmelted++`. **Não verifica retorno de addFreshEntity** e não concede XP explícita de furnace. Receita selecionada por ItemStack e resultado podem depender de datapack. |
| Custos e mutação externa | `getDefaultManaCost()=100`, Tier TWO, augments `Amplify,Dampen,AOE,Pierce,Sensitive` (Sensitive default max1). Sem cooldown individual ou DamageType. AOE/Pierce podem alterar simultaneamente **cap de itens** e geometria de blocos, não concedem segundo craft/smelt. `WorldEffectPolicy` do Black Arcana vale para world effects próprios; `RPG Skill Tree` provê perks/Mastery via contratos reais, sem alterar o provider resolver nem repetir receitas. |

**QA pendente:** veto do segundo `BlockEvent.BreakEvent` depois do preflight, `destroyBlockSafely=false`, `setBlockAndUpdate=false`, relação input/output, receita por datapack, reentrância/claim, XP, inventário de ItemEntity, carregamento de chunks, limitações de AOE, multiplayer e configs. `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`. Sem promover Stage 06.05 ou Stage 09.
