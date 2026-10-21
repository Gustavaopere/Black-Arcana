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
