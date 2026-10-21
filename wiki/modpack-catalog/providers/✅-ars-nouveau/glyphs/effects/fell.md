# Ars Nouveau — Fell

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_fell`
- Display name: Fell
- School: Elemental Earth
- Default tier: 1
- Default mana cost: 150
- Compatible augments: AOE, Extract, Fortune, Amplify, Dampen

## Provider-native behavior

Fell performs a bounded depth-first traversal over provider-tagged fellable vegetation. Source defaults cap the harvested set at 50 blocks, with an additional configured 50-block allowance per AOE multiplier. Claim/harvest checks are applied per block. Extract uses a silk-touch loot context; Fortune uses a fortune loot context.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:earth_essence` + `minecraft:diamond_axe`.
- Source-default recipe XP: **27 XP** (Tier I).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / deduplication

Ars Nouveau owns this whole-tree/vegetation harvesting primitive. Black Arcana must not introduce a generic duplicate mass-felling spell or duplicate provider loot settlement. Independent destructive vegetation magic remains subject to Black Arcana `WorldEffectPolicy` and bounded-work rules.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectFell`).

## Engenharia para perks — caminho causal individual

- **Fonte versionada:** [`EffectFell.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectFell.java), Ars Nouveau 5.13.1.
- **Limite do algoritmo:** verifica `state.is(FELLABLE)`, então `SpellUtil.DFSBlockstates(world,start,maxBlocks,isTree)` com `maxBlocks=(int)(GENERIC_INT.get()+Math.round(AOE_BONUS.get()*AOE))`; defaults 50 e +50 por unidade AOE. É teto de blocos *encontrados*, não total garantido de drops.
- **Proteção e loot:** por posição exige `BlockUtil.destroyRespectsClaim` e `BlockUtil.canBlockBeHarvested`. Com Extract usa `LootUtil.getSilkContext` e quebra sem drops internos; com Fortune usa `getFortuneContext(...,count(Fortune))`; sem os dois, usa `destroyBlockSafelyWithoutSound(world,pos,true,shooter)`. **Perks:** a ordem por Set não garante ordenação da árvore, e bônus de loot do RPG não deve rodar uma segunda vez.
- **Contenção:** AOE altera limite do DFS, não apenas raio; limites configuráveis e escala exigem work budget e perf test, sobretudo com árvore enorme ou addons de vegetação.
- **Estado:** ✅ source pin com métodos/fórmulas; ⚠️ auxiliaries, config real e Survival QA pendentes. API de `EffectResolveEvent.Pre` existe, mas adapter RPG para este glyph não foi implementado/testado; sem duplicação de custo/efeito/WorldEffectPolicy.
