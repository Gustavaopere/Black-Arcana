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
