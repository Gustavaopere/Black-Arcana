# 05.01 — Input & Loadouts — Runtime Contract

## State

`IMPLEMENTED / PHYSICAL INPUT VALIDATION PENDING`

## Goal

Provide a fast, rebindable casting workflow while preserving server ownership of loadouts and cast legality.

Presentation of the loadout editor is owned by `../visual-production/05-casting-ux/01-loadout-editor-presentation.md` from the `plans/` root, canonically `plans/visual-production/05-casting-ux/01-loadout-editor-presentation.md`.

## Canonical runtime contract

- Key conflicts remain discoverable/rebindable through ordinary Minecraft key mappings.
- Quick-slot defaults are unbound where collision risk is high; no gameplay-critical action requires side mouse buttons.
- `BlackArcanaKeyMappings` exposes radial `R`, selected cast `V`, an unbound loadout-editor mapping and eight unbound quick-cast mappings.
- The canonical loadout bound is **16 slots**.
- Direct quick-cast addresses the first **8** slots; all slots remain reachable through selection/radial paging.
- Loadouts are server-owned persistent state. Client edits are intents; `ArcanaServerRuntimeManager.handleLoadoutUpdate` validates registered spell identity and an installed execution engine before acceptance and persistence.
- A spell may appear only once. Oversized, duplicate, malformed or unavailable state fails closed.
- Invalid persisted state is isolated per caster and must not corrupt valid neighboring entries.
- `ClientInputController` sends cast intent only. Selection or loadout editing cannot bypass progression, cooldown, cost, target, hazard or world-effect gates.
- GUI focus suppresses direct cast input. If a server-advertised channel is already active when another `Screen` takes focus, the client cancels the exact local channel and sends the bounded `ChannelCancelIntentPayload` before release processing; GUI focus must never convert key release into channel execution.
- Client selection reconciles against the synchronized server loadout.

## Input model

Required rebindable operations are open radial, cast selected spell and edit loadout. Quick-cast mappings are convenience access only.

A direct quick-cast operation may select/reconcile a slot and emit cast intent in one input operation, but the server still performs every authoritative gate. It may never submit authoritative damage/range/cost, infer a target list, bypass loadout validation or cast while another GUI owns focus.

The radial path remains `open -> select -> close -> explicit cast`; selection alone does not execute gameplay.

## Ordered loadout evolution

If presentation work adds drag/reorder or explicit slot editing, the client still sends one complete bounded ordered snapshot for server validation. Before changing protocol, prove the current loadout-update contract already preserves ordered replacement semantics. Do not create a client-owned parallel slot store.

## Session/stale-state contract

On disconnect, synchronized client state and contextual client session state are cleared. `ClientInputController` reconciles its local `ClientLoadoutSelection` against an empty snapshot in the same disconnect tick before returning, so the selected slot cannot survive as stale contextual state. Reconnect waits for fresh server snapshots before treating any loadout/selection/result as current.

After datapack/provider changes, unavailable spells are rejected by the server and old quick-slot identity cannot remain castable.

## Key/provider boundary

- use ordinary `KeyMapping` registration;
- never rewrite another mod's keys;
- do not take the number row by default;
- Controlling may assist discovery but is not a gameplay dependency;
- future controller support must map onto existing intent methods after exact provider/API verification and must not create a second cast engine.

## Automated coverage

Canonical focused coverage includes `ClientInputAuthorityWiringTest`, `ClientInputChannelGuiFocusWiringTest`, `ClientInputDisconnectSelectionWiringTest`, `ClientLoadoutSelectionTest`, `LoadoutDraftTest`, `LoadoutRegistryTest`, `ArcanaServerRuntimeManagerLoadoutWiringTest` and `BlackArcanaSavedDataLoadoutTest` plus the normal build/JAR/GameTest/dedicated-server pipeline.

`ClientInputAuthorityWiringTest` pins ordinary rebindable `KeyMapping` registration/defaults and the fail-closed GUI-focus guards on radial, editor, selected-cast and quick-cast paths. `ClientInputChannelGuiFocusWiringTest` pins that GUI focus cancels an already-active channel through the canonical cancel transport before channel-release processing. `ClientInputDisconnectSelectionWiringTest` pins that disconnect clears the local selection in the same client tick before the controller returns. `BlackArcanaSavedDataLoadoutTest` includes explicit coverage that a persisted loadout above the canonical 16-slot bound is discarded per caster rather than truncated, while a valid neighboring caster remains intact. These are deterministic supporting evidence only; they do not replace the required real-client observation below.

The historical hardening checkpoint `30b111fc2a50f8fa3efb4bbf9b8cac1ad4c1f053` passed workflow `34150180682` after explicit RED cycles for execution-engine validation, duplicate direct writes, duplicate restore and persisted duplicate isolation.

## Remaining engineering acceptance

- rebind behavior and GUI-focus suppression observed in a real client;
- server-owned apply/clear/reconnect behavior observed without stale authority;
- 16-slot bound remains reachable through supported selection paths;
- no provider/controller integration weakens canonical server authority.

Visual/editor layout, search/filter, icon rendering, apply-state communication and small-viewport presentation are not engineering blockers here; they are tracked under visual production.
