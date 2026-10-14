# Warping

Status: `SOURCE-PINNED 5.13.1 / TELEPORT RITUAL`

- Registry id: `ars_nouveau:ritual_warping`
- Class: `RitualWarp`
- Activation radius: `5` blocks
- Completion threshold: `3` progress steps, advanced once per 20 server ticks
- Exact release checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Provider-native admission

The ritual accepts exactly one `WarpScroll` only when its provider `WARP_SCROLL` data component is valid and `canTeleportWithDim(tile.getLevel())` passes. `canStart` is false until such an item has been consumed.

## Provider-native settlement

At progress 3, the ritual reads the stored `BlockPos` from the consumed Warp Scroll and teleports every `Entity` inside a radius-5 AABB to that position. If a position exists, it also plays the portal-travel sound at the destination and marks the ritual finished.

The destination validation encoded by `WarpScrollData` remains provider authority. This exact path calls entity `teleportTo(x,y,z)` using the stored position; Black Arcana must not substitute its own destination or replay settlement.

## Black Arcana boundary

Warping materially overlaps Space & Displacement but remains an Ars ritual. Black Arcana must not double-teleport, double-consume the scroll or reinterpret this provider destination as a Black Arcana Gate/Recall target.

Independent Black Arcana teleportation continues to use its canonical server-side destination safety contracts.

## QA

Source behavior is pinned to 5.13.1. Cross-dimension/sublevel behavior and interactions with Sable/portal providers remain runtime/integration QA.

## Dossiê de implementação para perks — ritual exato

- **Classe fonte:** [`RitualWarp.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/ritual/RitualWarp.java), fonte `112920ff774831f204031da75b4c4e73d3765157` para Ars 5.13.1.
- **Admissão:** `canConsumeItem` admite **um** `WarpScroll`, com `WARP_SCROLL` component, `data.isValid()` e `data.canTeleportWithDim(tile.getLevel())`; `canStart` depende de consumido.
- **Conclusão:** a cada 20 ticks incrementa progress; em `>=3` busca `Entity` em AABB `inflate(5)`, extrai `data.pos().orElse(null)`, chama `entity.teleportTo(x,y,z)` para cada alvo se posição existe, toca som e `setFinished`. **Cuidado:** esse método de `teleportTo(double,double,double)` não mostra transição explícita de dimensão, ainda que a admissão teste `canTeleportWithDim`; efeito cross-dimension exige teste, não promessa.
- **Perks:** alcance, quantidade de alvos, filtros de teleport e consumo de scroll devem preservar ownership Ars; não é uma rota para ignorar gates de deslocamento Black Arcana.
- **Mutabilidade externa:** ⛔ nenhum adapter RPG provado que altere lifecycle, Source ou raio sem duplicar settlement; 🟡 fórmula/lógica source-pinned; ⚠️ runtime, receitas/config física, addons e Survival pendentes.
