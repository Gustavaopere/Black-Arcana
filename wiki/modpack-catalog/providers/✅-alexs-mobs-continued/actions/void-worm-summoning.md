# Mysterious Worm — Void Worm Summoning

- Provider: **Alex's Mobs Continued** (`alexsmobs`)
- Version: `2.1.13`
- Exact physical/publisher SHA-1: `50ddafdf3d12b33331e4eecb4ab514ae451baadd`
- Owner item: `alexsmobs:mysterious_worm`
- Semantic type: deliberate supernatural boss-summoning setup/action
- State: `CONDITIONAL`

## Identity and trigger

The exact current artifact implements the summon path from a deliberately obtained/dropped Mysterious Worm item.

Exact `ItemMysteriousWorm.onEntityItemUpdate` checks provider-owned eligibility before settling the summon. The exact gate includes:

- `AMConfig.voidWormSummonable`;
- membership of the current dimension in `AMConfig.voidWormSpawnDimensions`;
- the provider depth condition;
- item liveness.

## Settlement

When the exact provider gates pass, the provider:

- consumes/kills the dropped item entity;
- constructs and configures the Void Worm;
- server-spawns the boss;
- credits the summon advancement to the owner when applicable.

Entity initialization, AI, particles, sounds and downstream boss behavior remain consequences of this same root.

## Exact acquisition chain

Exact current data closes:

- Mysterious Worm production through a Capsid recipe using `alexsmobs:mosquito_larva`;
- Capsid availability through exact provider acquisition/loot surfaces.

Capsid processing is recipe machinery and does not create an additional semantic action identity.

## Deployed config gate

The action identity is exact-current, but effective deployed values for:

- `voidWormSummonable`;
- `voidWormSpawnDimensions`;

are not captured by the current catalog evidence.

Defaults are not substituted for deployed state.

## Disposition

- exact action identity: closed;
- normal provider acquisition chain: structurally closed;
- effective current summon eligibility: unresolved;
- state: `CONDITIONAL`;
- strict contribution from this root: **+0** until deployed gate evidence closes it.

Source: `../EXACT-2.1.13-ARTIFACT-AUDIT.md`.

## Matriz de execução e progressão (2026-10-29)

`Mysterious Worm` é uma **raiz condicional**, não um cast de mão: o JAR exato processa o dropped item em `onEntityItemUpdate` e o server só pode invocar após os gates de config, dimensão, profundidade e item vivo. Capturar configs **implantadas**, não defaults de release futura. Validar `AMC-V01..V03` no servidor físico antes de habilitar perks de spawn ou marcar a raiz como estrita. Mutadores **⛔ fail-closed**; não fabricar um segundo Void Worm. Veja [grafo de aquisição e QA](../EXACT-ARTIFACT-PERK-QA-GATES-2.1.13.md).
