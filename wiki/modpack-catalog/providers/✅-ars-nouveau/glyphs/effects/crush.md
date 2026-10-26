# Ars Nouveau — Crush

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_crush`
- Display name: Crush
- School: Elemental Earth
- Default tier: 2
- Default mana cost: 30
- Compatible augments: Amplify, Dampen, AOE, Pierce, Fortune, Sensitive
- Default Amplify limit: 2
- Default Sensitive limit: 1
- Source default base damage: 3
- Source default Amplify scalar: +1 damage

## Provider-native behavior

Crush uses Ars `CrushRecipe` data to transform eligible blocks into recipe outputs, optionally placing a block result and spawning remaining outputs. Sensitive enables processing nearby dropped items, with a source cap of `4 + 4*AOE + 4*Pierce` items per resolution. Against entities it deals provider Crush damage; underwater targets take triple the base component before amplification.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:earth_essence` + `minecraft:grindstone` + `minecraft:piston`.
- Source-default recipe XP: **55 XP** (Tier II).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / deduplication

Ars Nouveau owns this recipe-driven magical crushing/processing path and its outputs. Black Arcana should not clone generic ore/block crushing or double-generate recipe outputs; any forbidden transmutation must define a distinct cost/hazard/progression contract.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectCrush`).

## Engenharia para perks — caminho causal individual

- **Fonte exata:** [`EffectCrush.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectCrush.java), `com.hollingsworth.arsnouveau.common.spell.effect.EffectCrush` (Ars 5.13.1).
- **Entidades:** `onResolveEntity` chama `IDamageEffect.attemptDamage` com `(isUnderWater()? DAMAGE*3.0 : DAMAGE)+AMP_VALUE*getAmpMultiplier()`, defaults DAMAGE 3.0 e AMP 1.0. O triplo afeta **apenas o termo base**, não o termo Amplify.
- **Sensitive/item pipeline:** `onResolve` com `isSensitive()` prioriza `ItemEntity` em AABB `inflate(AOE+1)`, com cap de unidades `maxItemCrush=(int)(4+4*AOE+4*count(Pierce))`. `crushItems` consulta `CrushRecipe` e, para cada unidade, reduz o ItemStack em 1 e cria itens dos outputs rolados pelo RNG do mundo; não confundir quantidade de item entities com número de unidades.
- **Blocos:** `onResolveBlock` percorre `SpellUtil.calcAOEBlocks`, consulta `RecipeRegistry.CRUSH_TYPE`, rola outputs, pode colocar primeiro BlockItem e soltar sobras ou substituir posição por `AIR`, propagando `ShapersFocus`. A implementação local exibida **não chama** `BlockUtil.destroyRespectsClaim` nem harvest gate neste método; isso é lacuna de verificação da admissão global, não prova de vulnerabilidade ou licença para bypass.
- **Perks:** scaling de dano, transformação de bloco, recipe RNG e multiplicação de outputs requerem handlers distintos. Nenhuma modificação direta externa de drops declarada como segura.
- **Estado:** ✅ assinatura/fórmula do source pin; ⚠️ config carregada, auxiliar e testes físicos pendentes. Contratos de `EffectResolveEvent.Pre` são existentes, porém o adapter RPG, clamps, causalidade e escrita externa **não** foram validados: ⛔ fail-closed até testes.

## Certificação técnica estática — Crush (26/10/2026)

**✅ `STATIC_TECHNICAL_CATALOG_ONLY` · ⛔ `mutating_hook=NOT_VERIFIED` · ⚠️ `physical_qa=NOT_TESTED`.** `ars_nouveau:glyph_crush` → `EffectCrush`: identidade classe/ID verificada na auditoria compilada do publisher 5.13.1 (SHA-1 JAR `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`), **não** equivalência dos métodos. Fonte commit `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`: [EffectCrush.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectCrush.java), [CrushRecipe.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/crafting/recipes/CrushRecipe.java).

| Campo de perk | Comportamento do código e restrição |
|---|---|
| Entity damage | `onResolveEntity` implementa `IDamageEffect`; o `DamageSource` usa `DamageTypesRegistry.CRUSH` via `DamageUtil.source(world,...,shooter)`. Fórmula exata pré-receptor: `damage=(isUnderWater()?DAMAGE.get()*3.0:DAMAGE.get())+AMP_VALUE.get()*getAmpMultiplier()`, com defaults `DAMAGE=3.0` e `AMP_VALUE=1.0`. O multiplicador submerso atinge **somente base**, não AMP. `attemptDamage` pode passar por gates próprios; essa fórmula não certifica HP efetivamente perdido. |
| Sensitive e área de itens | `onResolve(HitResult,...)` quando `isSensitive()` consulta `ItemEntity` numa `AABB(BlockPos.containing(hitLocation)).inflate(aoeBuff+1.0)` e limita unidades a `maxItemCrush=(int)(4+4*aoeBuff+4*count(AugmentPierce))`. **Sem Sensitive** chama `super.onResolve` e segue o branch de alvo block/entity. AABB não significa raio esférico; count é **unidades**, não número de ItemEntity. |
| Receitas e RNG | `RecipeRegistry.CRUSH_TYPE` é consultado por `world.getRecipeManager().getAllRecipesFor`. `CrushRecipe` usa `Ingredient`, `outputs` e `skip_block_place`; `getRolledOutputs(world.random)` sorteia `chance`, e com `maxRange>1` escolhe `random.nextInt(maxRange)+1` stacks cópia, senão um. `lastHit` é cache revalidado por `matches(item.getDefaultInstance(),world)`; não assume que todos os outputs são determinísticos ou que a receita antiga vale após datapack reload. |
| Mutação de bloco | `onResolveBlock` percorre `SpellUtil.calcAOEBlocks` com AOE/Pierce, procura o primeiro `CrushRecipe` válido, rola outputs **antes** de qualquer validação local de mudança de bloco. Primeiro `BlockItem` quando `!shouldSkipBlockPlace()` vira `world.setBlockAndUpdate(p,defaultState)`, `i.shrink(1)` e `ShapersFocus.tryPropagateBlockSpell`; demais stacks são gerados por `world.addFreshEntity(new ItemEntity(...))`. Sem saída colocável, `world.setBlockAndUpdate(p,Blocks.AIR.defaultBlockState())` e propaga. **Nenhum retorno de `setBlockAndUpdate` é conferido** antes de alterar a stack/gerar outputs. O método não chama `destroyRespectsClaim` nem `canBlockBeHarvested` diretamente; requer QA de proteções externas, não é bypass comprovado. |
| Modo itens e conta causal | `crushItems` reusa cache de receita, percorre cada `ItemEntity`, enquanto `itemsCrushed<maxItemCrush` e stack não vazia: `stack.shrink(1)` e `world.addFreshEntity` para cada output de `getRolledOutputs`. Retorno do spawn do output não é testado. Não conceder Mastery por cada output gerado nem multiplicar rolls/drops; diferenciar item unit, item stack e entidade gerada. |
| Custo e autoridade | `getDefaultManaCost()=30`; `Amplify`, `Dampen`, `AOE`, `Pierce`, `Fortune`, `Sensitive` são augments declarados. Seus efeitos downstream **não são todos consumidos em cada branch**; por exemplo o código de `onResolveBlock` não acessa diretamente `AugmentFortune`, apesar de estar na lista compatível. `WorldEffectPolicy` governa as mutações próprias Black Arcana, não é hook de `EffectCrush`; `RPG Skill Tree` não pode emitir processamento duplicado. |

**Fail-closed:** auditar receitas carregadas e probabilidades, `getRolledOutputs`, Fortune efetivo, veto de claims para alterações, callbacks de BlockItem, perdas no `setBlockAndUpdate`, ausência de retorno checado de `addFreshEntity`, custos reais, dobras de AOE, recarga do datapack e QA multiplayer. `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`.
