# Remote

State: `SOURCE-PINNED 1.6.15 / PERSISTENT CONFIGURATION TOOL / MULTI-SELECTION BOUND NOT PROVEN / RUNTIME QA PENDING`

Registry id: `ars_controle:remote`
Data component: `ars_controle:remote_data`
Source checkpoint: `Vonr/Ars-Controle@ecbb83ba512bc9ca7a025556fb9c62dbd32b6430`

## Acquisition

Enchanting Apparatus:

- reagent: `ars_nouveau:dominion_wand`;
- 4 × tag `c:ender_pearls`;
- 4 × `minecraft:popped_chorus_fruit`;
- recipe `sourceCost`: `0`.

## Persistent/network state

`RemoteData` is both persistent and network synchronized through the registered data component. Fields are:

- optional block target `GlobalPos`;
- optional entity target UUID;
- `locked_first` boolean;
- `multiple` boolean;
- optional `first_corner` `GlobalPos`;
- display-only/provider target name component.

Default state is no target, `locked_first=true`, `multiple=false`, no first corner and empty target name.

Clearing the Remote removes block/entity/first-corner targets while preserving lock/selection mode.

## Configuration semantics

An empty Remote can shift-click a block or living entity to store it as the provider target. Later interactions connect the stored target and the newly interacted `IWandable` endpoint according to first/last locking mode.

Single mode applies one connection. Multiple mode stores a first corner and then iterates `BlockPos.betweenClosed(firstCorner, secondCorner)` for the second interaction, invoking provider wandable callbacks across eligible positions.

The audited source does not show an explicit maximum volume/range check around that `betweenClosed` iteration. Phase 2R therefore records multi-selection size as `UNBOUNDED IN SOURCE PATH / RUNTIME-SAFETY QA REQUIRED`; Black Arcana must not reuse this mechanism for its own target selection.

## Server packet authority

Protocol registration includes three client-to-server Remote control packets:

- `clear_remote`;
- `set_remote_lock_mode`;
- `set_remote_selection_mode`.

The mode packets carry only enum choices; clear carries no target data. On receipt, each handler obtains the player's **server-side main-hand stack** and mutates state only when that stack is the Ars Controle Remote.

Remote target acquisition itself happens in server-side item/block/entity interaction paths; those three UI packets do not authorize arbitrary coordinates/entities.

## Protection and target validity

Block targeting posts an Ars/NeoForge `BlockEvent.BreakEvent` for the interacted block and fails if vetoed. Dimension lookup may fail and returns a provider error. Entity references resolve by UUID through the provider cache.

These checks remain provider-specific and are not a Black Arcana authorization token.

## Highlight behavior

While selected, the server checks the Remote every 5 ticks for a resolvable target and sends Ars highlight data for supported `IDimensionalHighlighter`/`IWandable` targets. This is presentation/selection feedback, not gameplay authority.

## Boundary

- Ars Controle owns Remote state and wandable callbacks.
- Black Arcana targeting stays server-derived through its own target contracts.
- Never import Remote `GlobalPos`/UUID state directly as a valid Black Arcana target.
- Never duplicate provider callbacks or remote transfers.
- Multiple-selection iteration must not be copied as a Black Arcana area-selection implementation.

## QA pending

1. Stress-test very large multiple-selection boxes and confirm practical server bounds/interaction distance constraints.
2. Validate stale block/entity targets after unload, death and restart.
3. Validate claim/protection behavior for both stored and newly selected endpoints.
4. Validate radial/packet state after inventory moves and relog.
