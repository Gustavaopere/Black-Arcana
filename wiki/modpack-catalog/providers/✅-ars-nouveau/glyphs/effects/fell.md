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

## Certificação técnica estática — Fell (25/10/2026)

**✅ `STATIC_TECHNICAL_CATALOG_ONLY` · ⛔ `mutating_hook=NOT_VERIFIED` · ⚠️ `physical_qa=NOT_TESTED`.** ID `ars_nouveau:glyph_fell` ↔ classe `EffectFell` comprovados no manifesto binário do publisher JAR 5.13.1 SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd` (identidade, **não equivalência de método**). Fontes upstream pinadas `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`: [EffectFell.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectFell.java), [SpellUtil.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/util/SpellUtil.java), [BlockUtil.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/util/BlockUtil.java), [LootUtil.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/util/LootUtil.java).

| Eixo | Contrato técnico e limitações |
|---|---|
| Identificação e varredura | `onResolveBlock` só entra se `state.is(BlockTagProvider.FELLABLE)`. `getTree` encaminha `SpellUtil.DFSBlockstates(world,start,maxBlocks,this::isTree)`. `maxBlocks=(int)(GENERIC_INT.get()+Math.round(AOE_BONUS.get()*spellStats.getAoeMultiplier()))`, com defaults `GENERIC_INT=50` e `AOE_BONUS=50`. AOE aqui aumenta **orçamento do DFS**, não um cubo geométrico arbitrário ou drop confirmado; método retorna `Set<BlockPos>`, sem ordem estável garantida. |
| Admissão e world safety | Para cada `listPos`, exige simultaneamente `BlockUtil.destroyRespectsClaim(shooter,world,listPos)` e `BlockUtil.canBlockBeHarvested(spellStats,world,listPos)`. O primeiro é preflight `BlockEvent.BreakEvent`; `BlockUtil.destroyBlockSafelyWithoutSound` é uma **segunda** etapa que publica `BlockEvent.BreakEvent` e pode recusar a quebra por novo veto. Não prometer que um preflight aprovado equivale a bloco destruído. |
| Extract/Silk | Se `spellStats.hasBuff(AugmentExtract.INSTANCE)`, coleta `BlockState.getDrops(LootUtil.getSilkContext((ServerLevel)world,listPos,shooter))` e **gera `ItemEntity` antes** de `BlockUtil.destroyBlockSafelyWithoutSound(world,listPos,false,shooter)`. A classe **não verifica o retorno da destruição**; se for vetada no segundo evento, drops já podem ter sido gerados. Isso exige QA de claims e callbacks; não comprova duplicação in-game. |
| Fortune | Se não entrou em Extract e existe `AugmentFortune`, calcula `getFortuneContext(...,spellStats.getBuffCount(AugmentFortune.INSTANCE))`, igualmente emite drops **antes da destruição**, sem conferir `destroyBlockSafelyWithoutSound`. **Extract tem precedência sobre Fortune** por `if/else if`, independentemente de ambos estarem presentes. |
| Sem augment de loot | Caso contrário usa `destroyBlockSafelyWithoutSound(world,listPos,true,shooter)`, delegando drops à rotina de quebra. Retorno também é ignorado; não contabilizar `list.size()` como quebras/drops confirmados. `world.levelEvent(2001,...)` é VFX por posição inicial, não prova de êxito por bloco. |
| Custo/integração | `getDefaultManaCost()=150`, Tier ONE; compatíveis `AOE`, `Extract`, `Fortune`, `Amplify` e `Dampen`. `Amplify/Dampen` alteram harvest admissível, não produzem segunda ação de mineração. Budget de DFS/árvores modded pode crescer com config; usar limite server-authoritative e `WorldEffectPolicy` só para **mutações próprias** do Black Arcana. RPG Skill Tree não deve conceder Mastery por posição varrida nem duplicar loot do Ars. |

**QA física necessária:** blocktag FELLABLE real, teto do DFS e chunks, world claims e eventos duplicados, veto após loot manual, Fortune/Silk com blocos modded, drops e reinício, perf/CPU do DFS em árvores grandes, custo de mana e multiplayer. `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`. Stage não promovido.
