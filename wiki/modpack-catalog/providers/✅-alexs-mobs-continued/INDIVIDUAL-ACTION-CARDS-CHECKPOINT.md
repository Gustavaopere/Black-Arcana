# Alex's Mobs Continued 2.1.13 — individual action-card materialization checkpoint

Status: `3/3 ROOTS INDIVIDUALLY MATERIALIZED / 1 COUNTED_EXACT + 2 CONDITIONAL / NO NUMERATOR DELTA`

## Authority

- preparation base: `c5d978d896ab5ccf4c92880f43bad0d9fd1526cc`;
- physical JAR: `alexsmobs-2.1.13-neoforge+1.21.1.jar`;
- mod id: `alexsmobs`;
- exact physical/publisher SHA-1: `50ddafdf3d12b33331e4eecb4ab514ae451baadd`;
- exact artifact evidence: NON-MERGE PR #511 / run `36949047824`.

This tranche does not alter the already-closed three-root denominator. It only creates one durable card per semantic action.

## Individual cards

1. [Transmutation Table — Item Transmutation](actions/item-transmutation.md) — `COUNTED_EXACT`;
2. [Mysterious Worm — Void Worm Summoning](actions/void-worm-summoning.md) — `CONDITIONAL`;
3. [Dimensional Carver — Void Portal / Dimensional Passage](actions/dimensional-carver-passage.md) — `CONDITIONAL`.

The aggregate [SUPERNATURAL-ACTION-CARDS.md](actions/SUPERNATURAL-ACTION-CARDS.md) remains the compact overview.

## Accounting

Before and after this materialization:

- supernatural roots: **3**;
- `COUNTED_EXACT`: **1**;
- `CONDITIONAL`: **2**;
- Alex's Mobs Continued strict contribution: **+1**;
- global strict minimum: **1849 unchanged**.

No new action identity, config value or reachability claim is introduced.

## Remaining conditional gates

- effective deployed `AMConfig.voidWormSummonable`;
- effective deployed `AMConfig.voidWormSpawnDimensions`;
- Dimensional Carver normal acquisition remains downstream of the Void Worm path.
