# Burrowing

Status: `SOURCE-PINNED 5.13.1 / RITUAL`

- Registry id: `ars_nouveau:ritual_burrowing`
- Class: `RitualDig`
- Exact release checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Provider-native behavior

On start, the ritual creates an `EntityRitualProjectile` linked to the ritual tile. Server-side, once per 20 game ticks, it advances one layer downward from the ritual position and attempts to break four positions in its configured cross/column pattern.

A block is eligible only when:

- its destroy speed is non-negative;
- Ars Nouveau's `SpellUtil.isCorrectHarvestLevel(5, ...)` passes;
- `BlockUtil.destroyRespectsClaim(...)` passes.

Eligible blocks are settled through a provider fake player using a diamond pickaxe context and Ars Nouveau's safe-destroy utility. The ritual ends when its next position is outside build height.

Provider description: digs four adjacent holes to bedrock and drops the affected blocks.

## Authority / Black Arcana boundary

Burrowing is an Ars-owned destructive world ritual. Black Arcana must not replay its block breaks, drops or claim checks and must not treat each broken block as a separate cast/ritual completion.

Any independent Black Arcana terrain destruction remains subject to `WorldEffectPolicy`; Ars' own claim-aware destruction does not grant Black Arcana permission to bypass its policy.

## QA

Source semantics are pinned to 5.13.1. Full-pack claim-provider, drop and performance behavior remains runtime QA.

## Engenharia para perks — execução do ritual

- **Source pin:** [`RitualDig.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/ritual/RitualDig.java), versão Ars Nouveau 5.13.1.
- **Ativação:** `RitualDig.onStart` cria `EntityRitualProjectile` ligado à posição do ritual. `tick()` no servidor trabalha a cada `20` game ticks.
- **Geometria:** começa em `tile.getBlockPos().north().below(context.progress)`, tenta **quatro** `BlockPos`: posição original, `south().south()`, `south().east()`, `south().west()`; depois `progress++` produz próxima camada. Sai quando o próximo anchor está fora de build height.
- **World/admission:** `canBlockBeHarvested` exige destroy speed >=0 e `SpellUtil.isCorrectHarvestLevel(5,...) `; cada bloco exige `BlockUtil.destroyRespectsClaim`. O provider usa fake player e `Items.DIAMOND_PICKAXE` com `destroyBlockSafely`. **Perks:** não converter em mineração instantânea infinita nem bypass de claims. Black Arcana world effects sempre WorldEffectPolicy.
- **Status:** ✅ código fonte exato; ⚠️ configurações e comportamento físico dos providers adicionais pendentes; ⛔ mutabilidade em ritual ou integração com Mastery não é provada pelos eventos de glyph. Ritual runtime permanece Ars Nouveau.
