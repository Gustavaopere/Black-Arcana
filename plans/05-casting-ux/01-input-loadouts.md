# 05.01 — Input & Loadouts

## State

`IMPLEMENTED / FINAL VALIDATION DEFERRED`

This file is both the current contract and the executable plan for any remaining Input & Loadout work. Planned refinements are explicitly marked and are not implementation claims.

## Goal

Provide a fast, rebindable casting workflow that remains usable inside a very large modpack while preserving server ownership of loadouts and cast legality.

The player should be able to:

1. configure a bounded loadout outside combat;
2. select a slot through radial/direct input;
3. cast explicitly;
4. reconnect and recover the server-owned loadout cleanly;
5. understand when the server rejects an edit or cast;
6. avoid mandatory conflicts with other mods' keys.

## Current canonical contract

- Key conflicts remain discoverable/rebindable through Minecraft key mappings.
- Quick-slot defaults are unbound where collision risk is high; no gameplay-critical action requires mouse side buttons.
- `BlackArcanaKeyMappings` currently exposes radial `R`, selected cast `V`, an unbound loadout-editor mapping and eight unbound quick-cast mappings.
- The canonical loadout bound is **16 slots**.
- The current direct quick-cast array addresses the first **8** loadout slots; the remaining slots remain reachable through selection/radial paging rather than receiving default extra bindings.
- Loadouts are server-owned persistent state. The client submits an edit; `ArcanaServerRuntimeManager.handleLoadoutUpdate` validates both registered spell identity and an installed server execution engine before accepting it, then persists accepted state through `BlackArcanaSavedData`.
- A spell may appear only once in a loadout. `LoadoutRegistry` preserves the same bounded/unique invariant for direct writes and snapshot restore, with invalid restore snapshots rejected atomically.
- Persisted loadout entries are parsed fail-closed per caster. An oversized, unparsable or duplicate persisted entry is discarded without invalidating valid neighboring caster entries or aborting server restore.
- `ClientInputController` sends cast intent only. Switching or selecting a loadout cannot bypass server progression, cooldown or resource gates.
- GUI focus suppresses direct cast input.
- Client selection reconciles against the current synchronized server loadout.

## Current editor behavior

`BlackArcanaLoadoutScreen` currently:

- snapshots synchronized presentation and hazard metadata when opened;
- builds a `LoadoutDraft` from the synchronized loadout;
- lists synchronized spell presentation entries;
- toggles spells into/out of the bounded draft;
- clears the draft through a dedicated key action;
- paginates for small viewports;
- sends the bounded update on apply;
- closes after apply while the server remains authority over the accepted final state.

The draft itself has no gameplay authority.

## Input model

### Required mappings

Core Stage 05 must always have rebindable equivalents for:

- open radial;
- cast selected spell;
- edit loadout.

Quick-cast mappings are convenience mappings rather than required gameplay access.

### Direct quick cast

A quick-cast slot may select/reconcile the slot and emit cast intent in one input operation, but the server still performs every authoritative gate.

A direct slot binding must never:

- skip loadout validation;
- skip cooldown/resource/progression checks;
- provide client-authored damage/range/cost values;
- cast while another GUI owns focus;
- infer a target list on the client.

### Radial + selected cast

The two-step path remains:

`open radial -> select -> close radial -> explicit cast input`

Selection alone is intentionally non-casting.

## Planned loadout-editor refinements

The following are **PLANNED / NOT YET CLAIMED AS IMPLEMENTED**.

### 1. Explicit slot awareness

The editor should make slot position meaningful instead of behaving only as an unordered membership picker.

Plan:

- show slot numbers `1–16`;
- visibly distinguish slots `1–8` as currently eligible for direct quick-cast mappings;
- permit bounded reordering without changing the server slot limit;
- preserve uniqueness while moving entries;
- send the complete ordered bounded snapshot for server validation;
- never let client drag/reorder operations become accepted until the server synchronizes the resulting state.

Implementation gate: first inspect the current server loadout update contract to prove ordered replacement is already semantically supported. If not, design the smallest compatible protocol change rather than inventing a parallel slot store.

### 2. Search

Add client-side filtering by synchronized display name.

Rules:

- search changes only which entries are visible in the editor;
- it does not change server availability;
- empty search restores the full synchronized presentation list;
- filtering must remain bounded to the already-synchronized spell presentation set.

### 3. Provider/domain/school filtering

Only add these filters when a real bounded presentation field exists for the classification.

Do not derive school/provider/domain from resource-id string patterns or client heuristics.

If the current presentation payload lacks this information, record the need for a server-authored presentation schema change instead of silently fabricating metadata.

### 4. Icon presentation

`SpellPresentationPayload.Entry` already exposes an `iconId`.

Plan:

- render the icon where it resolves safely;
- retain a text/name fallback;
- missing/broken artwork must not remove the spell from the list or change loadout authority;
- icon rendering must remain client-only.

### 5. Apply-state feedback

Current apply closes immediately after sending intent.

Plan the UX for three states without making the client authoritative:

- draft not submitted;
- update sent / awaiting authoritative snapshot;
- authoritative snapshot received.

If explicit rejection feedback is added, it must come from a bounded server result. Do not interpret lack of immediate local change as acceptance or denial.

### 6. Clear and restore ergonomics

Keep clear bounded and reversible at the draft level until apply.

Potential UX improvement:

- a client-only `Reset draft to synchronized state` action before apply.

This must not create local history that overrides a newer server snapshot.

## Session and stale-state plan

### Disconnect

On loss of player/connection:

- synchronized client state is cleared;
- contextual UX state is cleared;
- no old loadout/result may flash as current authority on the next connection.

### Reconnect

The client waits for fresh server snapshots and then reconciles selection.

### Datapack/provider change

If a previously selected or loaded spell is no longer available:

- the server rejects invalid loadout state/update;
- client selection reconciles to the current synchronized list;
- stale spell identity must not remain castable from an old quick slot.

## Key-conflict plan

The pack contains many key mappings.

Rules:

- use ordinary Minecraft `KeyMapping` registration;
- keep quick slots unbound by default;
- do not silently rewrite another mod's keys;
- do not require a side mouse button;
- do not take the vanilla number-row by default;
- Controlling may help users discover conflicts when installed, but Stage 05 does not depend on it.

Any new default binding requires a deliberate conflict audit against the current physical modlist.

## Optional controller boundary

Controller/gamepad support is not currently guaranteed because the current physical modlist does not expose a confirmed general controller provider.

If a controller provider is added later:

1. verify exact mod/version/API;
2. map controller actions to the same existing client intent operations;
3. keep server cast authority unchanged;
4. keep keyboard/mouse fully functional when the provider is absent;
5. fail closed on incompatible provider versions.

Do not add speculative controller API code.

## Automated coverage

Focused coverage includes `ClientLoadoutSelectionTest`, `LoadoutDraftTest`, `LoadoutRegistryTest`, `ArcanaServerRuntimeManagerLoadoutWiringTest` and `BlackArcanaSavedDataLoadoutTest`; the full CI pipeline also exercises NeoForge build/JAR verification, Foundation GameTests and dedicated-server startup.

Follow-up hardening on 2026-09-07 was developed through isolated RED -> GREEN cycles:

- workflow `34147636556` proved that loadout update wiring accepted registry presence without proving an installed execution engine;
- workflow `34148523955` proved that direct `LoadoutRegistry.setLoadout` accepted duplicate spells;
- workflow `34149143928` proved that `LoadoutRegistry.restoreSnapshot` accepted duplicate spells;
- workflow `34149596497` proved that a duplicate persisted loadout could propagate into strict restore and abort that restore path;
- final code checkpoint `30b111fc2a50f8fa3efb4bbf9b8cac1ad4c1f053` passed workflow `34150180682` (#1704): unit tests, diff sanity, NeoForge build, built-JAR verification, Foundation GameTests and dedicated-server smoke all GREEN.

These are automated implementation/hardening gates only. They do not promote this task to `VALIDATED / COMPLETE`.

## Test plan for future changes

Any Input & Loadout change must cover, where applicable:

### Pure/unit

- slot bounds;
- uniqueness;
- reorder semantics;
- selection reconciliation;
- draft reset/apply state;
- search/filter behavior;
- stale snapshot handling.

### Server/network

- malformed/oversized payload rejection;
- unavailable spell rejection;
- engine-unavailable rejection;
- persistence across reconnect;
- removed spell/provider recovery;
- no duplicate cost/cast processing.

### Real client

- key rebind conflict discovery;
- GUI-focus suppression;
- apply/clear/reopen;
- disconnect/reconnect;
- small viewport and GUI scale;
- quick slot 1–8 behavior;
- full 16-slot radial accessibility.

## Deferred acceptance

Keyboard variants, GUI focus in a real client, death/relog and stale server-denied loadouts remain in `docs/qa/casting-ux-manual-matrix.md`. Those rows remain PENDING until directly observed.

## Exit criteria

05.01 is fully validated only when:

- the 16-slot bounded server-owned loadout contract remains intact;
- duplicate/invalid state fails safely;
- key mappings remain rebindable;
- direct quick-cast and radial-selected cast both converge on canonical server casting;
- GUI focus cannot leak casts;
- reconnect cannot expose stale authority;
- applicable manual matrix rows have direct evidence.
