# Ars Nouveau — Toss

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_toss`
- Display name: Toss
- School: Manipulation
- Default tier: 1
- Default mana cost: 10
- Compatible augments: Extract, Randomize, Dampen, Amplify

## Provider-native behavior

Toss routes items out of the Ars caster inventory. Extract constrains the amount to 1; otherwise source stack size is `64 * 2^amplification`, so Dampen halves and Amplify doubles per step. Randomize changes stack selection. A block target with an item-handler capability receives insertion directly; otherwise the spell spawns item entities at the target.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:manipulation_essence` + `minecraft:dropper`.
- Source-default recipe XP: **27 XP** (Tier I).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / deduplication

Ars Nouveau owns this inventory extraction/transfer path. Black Arcana must not double-remove, double-insert or duplicate dropped stacks when Ars is causal.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectToss`).

## Engenharia para perks — caminho causal individual

- **Source pin:** [`EffectToss.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectToss.java) do Ars 5.13.1.
- **Volume nominal:** `getStackSize` devolve 1 com `AugmentExtract` ou `(int)(64*Math.pow(2,ampMultiplier))`. O método **não** apresenta clamp próprio para overflow, negativos ou máximos de pack; qualquer perk que aumente amp precisa de validação/cap real no pipeline.
- **Extrator:** `processStacks` parcela o total em requisições `size=min(amount,64)` e chama `InventoryManager.extractRandomItem` (Randomize) ou `extractItem`. Para caster não-tile, filtra itens iguais a `shooter.getMainHandItem()` usando `ItemStack.matches`; para TileCaster aceita qualquer stack não vazia.
- **Destino:** entity hit gera stacks como ItemEntity próximo do alvo; block hit tenta obter `Capabilities.ItemHandler.BLOCK` no **bloco acertado**. Se existir, insere via `ItemHandlerHelper.insertItemStacked`, devolve/dropa sobras por `ExtractedStack.returnOrDrop`; sem handler, cria ItemEntity adjacente ao hit. **Perks:** manter contabilidade exata e não transformar extração/retorno em duplicação ou XP por item.
- **Estado:** ✅ classe/método do source pin; ⚠️ scripts de addons, config física e QA Survival pendentes; ⛔ bridge de perks RPG e mutação de `SpellStats` sem validação de causalidade e limites.
