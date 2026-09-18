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
- Immediate-cast ingress revalidates the canonical registered spell and the server-owned loadout slot before engine execution; a client-authored `spellId` cannot substitute a different registered/executable spell for the selected slot.
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

Canonical focused coverage includes `ClientInputAuthorityWiringTest`, `ClientInputChannelGuiFocusWiringTest`, `ClientInputDisconnectSelectionWiringTest`, `ClientLoadoutSelectionTest`, `RadialCanonicalLoadoutReachabilityTest`, `LoadoutDraftTest`, `LoadoutRegistryTest`, `ArcanaServerRuntimeManagerLoadoutWiringTest`, `ArcanaServerRuntimeLoadoutAuthorityTest` and `BlackArcanaSavedDataLoadoutTest` plus the normal build/JAR/GameTest/dedicated-server pipeline.

`ClientInputAuthorityWiringTest` pins ordinary rebindable `KeyMapping` registration/defaults and the fail-closed GUI-focus guards on radial, editor, selected-cast and quick-cast paths. `ClientInputChannelGuiFocusWiringTest` pins that GUI focus cancels an already-active channel through the canonical cancel transport before channel-release processing. `ClientInputDisconnectSelectionWiringTest` pins that disconnect clears the local selection in the same client tick before the controller returns. `ArcanaServerRuntimeLoadoutAuthorityTest` pins that immediate casts cannot forge a different registered/executable spell for a server-owned slot and that a spell removed from the live registry cannot remain executable through stale loadout/engine state. `BlackArcanaSavedDataLoadoutTest` includes explicit coverage that a persisted loadout above the canonical 16-slot bound is discarded per caster rather than truncated, while a valid neighboring caster remains intact. These are deterministic supporting evidence only; they do not replace the required real-client observation below.

`RadialCanonicalLoadoutReachabilityTest` deterministically drives the production radial paging/focus/hit-test helpers and the non-casting radial selector across every canonical slot `0..15` for both keyboard and pointer paths. This proves machine-level reachability of the complete 16-slot bound without changing casting authority; the required real-client/physical observation remains pending.

The historical hardening checkpoint `30b111fc2a50f8fa3efb4bbf9b8cac1ad4c1f053` passed workflow `34150180682` after explicit RED cycles for execution-engine validation, duplicate direct writes, duplicate restore and persisted duplicate isolation.

The immediate-cast loadout-authority hardening is canonical via PR #271 at merge SHA `1d0e221440506005fd4cd16220436f3573c0adec`. RED workflow `35034535110` reproduced the forged-slot bypass. Final branch workflow `35035822174`, PR-head workflow `35036140396` and post-merge workflow `35036436151` passed the applicable automated gates; the post-merge run also published exact-SHA artifact `black-arcana-1d0e221440506005fd4cd16220436f3573c0adec` (artifact ID `10423705741`, SHA-256 `f61d7f3f533e220e1f81e72ee75e98dacd7358367e5def88ce6a6df173a73629`). This closes that deterministic authority gap only and does not satisfy the physical acceptance below.

The Block J Iron's-hosted provider preflight is canonical via PR #317 at merge SHA `1944e45c122a24c36101e97efe2195730b5019f0`. RED workflow `35282073048` proved that the provider-hosted probe was absent from the synchronized presentation catalog and therefore could not be placed legitimately into the server-owned loadout. A second RED workflow, `35286696874`, proved that a presentation-ID collision could leave partial hosted runtime state. The final clean feature SHA `762dcc7824c543d932fb3a81645e92a424043395` passed branch workflow `35287227515` and PR workflow `35287405001`; post-merge workflow `35292207167` (#3212) passed unit tests, diff sanity, NeoForge build, built-JAR checks, Foundation GameTest, production dedicated-server smoke, artifact publication, and the separate Stage 05 QA companion dedicated-server smoke. The canonical production artifact is `black-arcana-1944e45c122a24c36101e97efe2195730b5019f0` (artifact ID `10527221605`, SHA-256 `45b754d81597c9f75e00b203347f93c99be94883fe5b2874abfce33ea72a0e43`); the matching Block I companion is `black-arcana-stage05-qa-1944e45c122a24c36101e97efe2195730b5019f0` (artifact ID `10526747373`, SHA-256 `278741a5742f1e7090242dc739329eb362fa33bc8c62689279b49cf04119a5b6`). This closes only the deterministic provider-presentation/loadout/partial-install blockers. Block J provider-real execution and all physical acceptance below remain pending; no manual PASS is created by this checkpoint.

## Remaining engineering acceptance

- rebind behavior and GUI-focus suppression observed in a real client;
- server-owned apply/clear/reconnect behavior observed without stale authority;
- 16-slot bound remains reachable through supported selection paths;
- no provider/controller integration weakens canonical server authority.

Visual/editor layout, search/filter, icon rendering, apply-state communication and small-viewport presentation are not engineering blockers here; they are tracked under visual production.
