# Advanced Dominion Wand

Status: `SOURCE-PINNED 21.3.0 / SERVER-AUTHORITY+BOUNDS AUDITED / RUNTIME QA PENDING`

Exact source pin: `Jarva/Ars-Additions@91f102a90dc058cf40e4eac5a67a881e48b856b4`.

Registry id: `ars_additions:advanced_dominion_wand`.

## Acquisition

Enchanting Apparatus recipe in the exact pin:

- reagent: Ars Nouveau Dominion Rod;
- pedestal items: Amethyst Block + Gold Ingot ×2.

A shapeless self-clear recipe is also generated.

## Persisted connection intent

The provider component stores an origin block position or entity id, dimension, link order and single/multi link mode. It can address Ars Nouveau `IWandable` blocks/entities and preserve which endpoint should be considered first/second in the provider connection callbacks.

## Multi-target network safety

The multi-link UI may discover/preview candidate targets client-side, but `PacketMultiTargetConnection` revalidates them on the server.

The exact source enforces:

- packet sender must be on a server level;
- held item in the specified hand must actually be Advanced Dominion Wand;
- stored origin level must exist;
- total candidates must be **<= 1000**;
- each candidate target must be within **128 blocks** of the player;
- block and entity candidates must pass `BlockUtil.destroyRespectsClaim` at the target position;
- at least one side of a connection must implement `IWandable`.

Only after those checks are provider connection callbacks invoked.

## Black Arcana boundary

This is a useful reference architecture for server-authoritative client intent, but it is still provider-owned. Black Arcana must not reuse the client candidate list as authority, bypass claim checks, duplicate connection callbacks or turn provider link operations into spell casts/procs.
