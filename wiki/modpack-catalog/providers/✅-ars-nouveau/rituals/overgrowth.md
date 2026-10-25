# Overgrowth

Status: `SOURCE-PINNED 5.13.1 / GROWTH RITUAL`

- Registry id: `ars_nouveau:ritual_overgrowth`
- Class: `RitualOvergrowth`
- Source cost declaration: `500`
- Processing cadence: every `200` game ticks
- Working radius: `5` blocks
- Exact release checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Provider-native behavior

Without a modifier, Overgrowth scans a bounded 11×3×11 block volume around the ritual every 200 ticks. Candidate farm/bonemealable positions are adjusted to their crop position; each candidate has a `1/25` random chance to receive vanilla bonemeal through an Ars fake player. If at least one bonemeal application succeeds, the ritual marks that work cycle as needing Source.

With exactly one consumed Bone Block, the ritual switches modes: it scans `AgeableMob` entities inside radius 5, skips the provider blacklist, and advances baby animals by `500` age ticks. A successful cycle requests Source.

## Authority / Black Arcana boundary

Crop growth, animal age advancement, random selection and Source settlement are Ars Nouveau authority. Black Arcana must not replay successful growth operations or duplicate Source costs.

The Bone Block modifier selects a provider-native mode; it is not a Black Arcana progression gate.

## QA

Source is pinned to 5.13.1. Effective Source debit timing and compatibility with modded bonemeal/growth hooks remain runtime QA.

## Engenharia para perks — contrato de ritual

- **Fonte exata:** [`RitualOvergrowth.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/ritual/RitualOvergrowth.java) no Ars 5.13.1.
- **Cadência:** a cada `200` game ticks no servidor, modo baseline percorre posições em `brazier.offset(±5,-1..1,±5)` (11×3×11 candidatos) e, para cada posição ajustada quando FarmBlock/Bonemealable acima, faz tentativa de bone meal apenas se `rand.nextInt(25)==0`; sucesso de `BoneMealItem.applyBonemeal` marca `didWorkOnce`.
- **Modo Bone Block:** `canConsumeItem` só aceita **um** `Items.BONE_BLOCK` com lista vazia. `isAnimalGrowth` muda para `AgeableMob` na AABB `inflate(5)`, exclui `OVERGROWTH_BLACKLIST` e chama `ageUp(500,true)` apenas em bebês.
- **Custos e causalidade:** ao menos um sucesso por ciclo chama `setNeedsSource(true)`; `getSourceCost=500` não prova 500 por planta ou baby. Ampliação de RNG/biome/per-tick por perk exige budget; observer não deve duplicar bonemeal nem contabilizar cada iteração como novo cast.
- **Estado:** ✅ identidade/métodos/source pin; ⚠️ valores no modpack, proteções, Save/Restart e multiplayer não testados nesta branch. ⛔ adapter RPG para mutation, bônus de recursos ou acompanhamento de um cast por ritual não implementado; Ars conserva Source e world authority.

## Certificação técnica estática — crop/animal growth (25/10/2026)

**✅ `STATIC_TECHNICAL_CATALOG_ONLY` · ⛔ `mutating_hook=NOT_VERIFIED` · ⚠️ `physical_qa=NOT_TESTED`.** ID `ars_nouveau:ritual_overgrowth` ↔ `RitualOvergrowth` está na auditoria de identidades do JAR `ars_nouveau-1.21.1-5.13.1.jar`, SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`. Fluxo inspecionado em [RitualOvergrowth.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/ritual/RitualOvergrowth.java) do upstream `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`; sem equivalência integral dos métodos no binário.

| Campo para perks | Evidência e limitação |
|---|---|
| Lado/cadência | `tick()` em cliente produz somente `spawnRitualAreaEffect` (raio visual 5). No servidor executa a lógica funcional apenas a cada `world.getGameTime()%200==0`, e `setNeedsSource(true)` somente se `didWorkOnce`. O evento visual não é cast extra. |
| Área do modo cultivo | Sem `Items.BONE_BLOCK`, percorre `BlockPos.betweenClosed(pos.offset(5,-1,5),pos.offset(-5,1,-5))`: **11×3×11 = 363 posições candidatas**, antes de ajustes e filtros. Se `state.getBlock() instanceof FarmBlock` **ou** o bloco em `b.above()` é `BonemealableBlock`, muda o alvo local para `b.above()`. Cada posição candidata pode tentar `BoneMealItem.applyBonemeal(new ItemStack(Items.BONE_MEAL),...,ANFakePlayer)` quando `rand.nextInt(25)==0`. Posições podem se sobrepor após ajuste; não é 363 plantas distintas. |
| Modo animal | `canConsumeItem` admite um `Items.BONE_BLOCK` com lista consumida vazia. `isAnimalGrowth()` seleciona `AgeableMob` em `new AABB(getPos()).inflate(5)` (não esfera), exclui `EntityTags.OVERGROWTH_BLACKLIST`, somente para `a.isBaby()` chama `a.ageUp(500,true)`. `didWorkOnce=true` significa **chamada de avanço de idade**, não prova de nascimento, morte ou crescimento completo de um mob específico. |
| Source e falhas | `getSourceCost()=500`, mas `setNeedsSource(true)` ocorre uma vez no ciclo com qualquer aplicação de bonemeal que retornou true ou ao menos um baby processado. Não significa 500 Source por planta/animal, nem comprova debit no mesmo tick; `RitualBrazierTile` controla a transação. Mudanças por perk exigem interdição de duplicação e custo justo. |
| Efeito e world-safety | Não existe `DamageType`/projetil ofensivo. `BoneMealItem.applyBonemeal` e `AgeableMob.ageUp` são consumidores vanilla/provider; a classe não chama diretamente `destroyRespectsClaim`. Isso não comprova respeito uniforme a claims no pack. `WorldEffectPolicy` do Black Arcana vale para efeitos próprios, não sobreposição de growth Ars. |
| QA e integração | Ampliar área, frequência, probabilidade e `ageUp` por perks pode produzir multiplicações de trabalho e desbalanceamento. `RitualOvergrowth` mantém Source/ciclo/mundo; RPG Skill Tree só poderia modificar por adapter verificado e Mastery deduplicada por execução. Config, tags, entidades modded, save/restart, claims e multiplayer permanecem pendentes. |

**Limite da prova:** `STATIC_TECHNICAL_CATALOG_ONLY`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`; sem Stage 06.05/09 promovido.
