# 05.10 — Loadout Editor Information Architecture

## State

`PLANNING / NO RUNTIME CHANGE / LOADOUT-EDITOR HARDENING`

This document defines the canonical Stage 05 plan for evolving `BlackArcanaLoadoutScreen` from a bounded membership list into a clearer slot-aware editor without changing server authority, loadout semantics or the canonical cast pipeline.

Baseline used to author this plan: `main@db7f4858b3c5eda3bba957db7de194228b6d4df6`.

This is a planning artifact only. It does **not** add Java runtime behavior, packets, protocol fields, widgets, search boxes, icons, drag/drop handling, acknowledgement packets or provider metadata.

---

## 1. Why this plan exists

`01-input-loadouts.md` already identifies six planned editor refinements:

1. explicit slot awareness;
2. search;
3. provider/domain/school filtering only from real metadata;
4. icon presentation;
5. apply-state feedback;
6. reset-draft ergonomics.

The current runtime supports only the simpler membership-list workflow.

05.10 converts those high-level refinements into one executable information-architecture and state-management plan.

It must remain compatible with:

- `05.07 — Presentation Data Contracts`;
- `05.08 — Visual Language & State Semantics`;
- `05.09 — Keyboard Focus & Navigation`;
- the current 16-entry ordered server loadout;
- the first eight direct quick-cast mappings;
- the current full-snapshot update protocol.

---

## 2. Current verified runtime facts

### 2.1 The server loadout is an ordered dense list

The current contract is **not** sixteen nullable independent cells.

Current behavior is an ordered `List<ArcanaSpellId>`:

- `LoadoutDraft` stores spells in an `ArrayList`;
- adding a spell appends it;
- removing a spell compacts the following entries;
- `snapshot()` preserves order;
- `LoadoutUpdatePayload` preserves the ordered list;
- `LoadoutUpdateService` copies the proposed list without sorting;
- `LoadoutRegistry` stores that list unchanged;
- cast validation resolves the spell at the exact requested list index;
- `LoadoutSnapshotPayload` returns the accepted list in server order.

Therefore the current slot model is:

- positions `1..loadout.size()` are populated;
- positions after `loadout.size()` are unused capacity;
- **gaps in the middle are not representable**;
- removing position N shifts later spells left.

05.10 preserves that contract.

Sparse slots require a separate server-state/protocol migration and are not authorized here.

### 2.2 Current bound

The canonical maximum remains **16 spells**.

### 2.3 Direct quick-cast coverage

Current direct quick-cast mappings address the first **8 positions**.

Those mappings are unbound by default, but positions 1–8 are still the positions eligible for those mappings.

Positions 9–16 remain reachable through the selected-slot/radial workflow under the current design.

### 2.4 Current editor source list

`BlackArcanaLoadoutScreen` currently builds its available-spell list from synchronized `SpellPresentationPayload.Entry` records.

The current presentation contract contains only:

- `spellId`;
- `translationKey`;
- `iconId`.

It does **not** currently contain provider, domain, school, tier, cooldown-group or arbitrary tag metadata.

### 2.5 Current update transport

Applying the draft sends the complete ordered list through `LoadoutUpdatePayload`.

The server returns a `LoadoutSnapshotPayload` containing the canonical resulting list.

The reply contains **no explicit acceptance boolean, rejection category, rejection reason or request id**.

The same snapshot packet type is also used for ordinary synchronization such as login.

Therefore the current client can trust the received snapshot as canonical state, but cannot safely infer an explicit server decision/reason from that snapshot alone.

---

## 3. Authority boundaries

05.10 must preserve the existing authority model.

### Server authority

The server remains authoritative over:

- whether a spell is registered;
- whether an execution engine is installed;
- loadout size bound;
- duplicate rejection;
- accepted loadout order;
- persisted loadout state;
- whether a later cast matches the server-owned slot;
- every gameplay admission gate.

### Client authority

The client may own only editor-local presentation state such as:

- unsaved draft order;
- current editor focus;
- search query;
- current local filter selection when the metadata exists;
- temporary reorder gesture state;
- whether the local draft differs from the opening synchronized snapshot.

None of those values is gameplay authority.

---

## 4. Canonical editor mental model

The editor should communicate two separate concepts:

1. **Configured loadout order** — the ordered dense list that the server can accept;
2. **Available spell catalog** — synchronized spells the player may attempt to add to the draft.

The exact visual layout is responsive and is not frozen to a permanent two-pane desktop design.

However every implementation must make those two concepts distinguishable.

A single-scroll-list implementation remains allowed if it clearly exposes slot position and draft membership/order.

---

## 5. Slot semantics

### 5.1 Slot labels

A populated spell should expose its current draft position as a 1-based slot number.

Examples:

- position index `0` → Slot 1;
- position index `7` → Slot 8;
- position index `8` → Slot 9;
- position index `15` → Slot 16.

### 5.2 Quick-cast eligibility marker

Slots 1–8 may display a concise indicator that they correspond to the eight existing direct quick-cast mappings.

Wording must not imply those mappings are currently bound.

Correct meaning:

`eligible for Quick Cast 1–8`

Incorrect meaning:

`press 1–8 to cast`

No number-row default is introduced by this plan.

### 5.3 Slots 9–16

Slots 9–16 remain normal canonical loadout positions.

The editor may label them as not having current direct quick-cast mappings, but must not imply they are unavailable or weaker.

### 5.4 Unused capacity

If the draft contains fewer than 16 spells, the remaining capacity may be represented visually.

Because the server model is dense:

- unused capacity is only trailing capacity;
- the UI must not create a real empty slot between populated spells;
- dragging/reordering cannot leave holes.

---

## 6. Reordering contract

### 6.1 Current protocol compatibility

Reordering populated spells does **not** require a new protocol schema by itself.

The current full-list update already preserves order end-to-end.

### 6.2 Planned local operations

A future `LoadoutDraft` hardening may expose deterministic client-only operations such as:

- move spell from index A to index B;
- move focused spell one position earlier;
- move focused spell one position later;
- optionally reorder through drag/drop.

These are conceptual operations, not required method names.

### 6.3 Invariants

Every reorder operation must preserve:

- maximum 16 spells;
- uniqueness;
- exact spell identities;
- dense list semantics;
- no network update before Apply;
- no cast or cooldown/resource side effect.

### 6.4 Remove semantics

Removing a spell keeps current dense-list semantics:

- later spells shift one position earlier;
- quick-cast associations therefore move with the resulting slot positions.

The UI must make this consequence visible enough that the player is not surprised.

### 6.5 Add semantics

Adding a spell to a non-full draft appends it to the first unused trailing position.

No arbitrary middle insertion is required for the first implementation because the player can reorder after adding.

An implementation may provide explicit insertion as a convenience only if it produces the same dense ordered list.

### 6.6 Sparse slots are out of scope

Do not fake persistent blank slots with client placeholders.

If design later requires:

- Spell A in slot 1;
- empty slot 2;
- Spell B in slot 3;

that requires a new canonical server representation and migration plan.

05.10 explicitly does not authorize it.

---

## 7. Search contract

Search is client-side presentation filtering over the already synchronized spell catalog.

### 7.1 Searchable fields currently supported

The current client safely has:

- resolved display name from `translationKey`;
- canonical `spellId`.

A first search implementation may match either or both.

### 7.2 Search behavior

Search must:

- be case-insensitive in a locale-safe manner;
- operate only over local synchronized presentation entries;
- never make a hidden spell invalid or remove it from the draft;
- never reorder the draft itself;
- never send a server request per keystroke;
- return the full catalog when the query is empty;
- preserve canonical spell identity even when translated display names collide.

### 7.3 Search result order

Search result ordering is presentation only.

A stable client-side ordering may use display name with canonical id as a tie-breaker, but that catalog order must never redefine loadout slot order.

### 7.4 Search and draft visibility

A spell already in the draft may disappear from the filtered catalog view while the search query does not match it.

That must not remove or alter its draft position.

The configured loadout/order surface must remain understandable independently from catalog filtering.

---

## 8. Provider/domain/school filtering gate

Provider/domain/school filtering remains **BLOCKED BY DATA CONTRACT** under the current runtime.

### 8.1 Why it is blocked

`SpellPresentationPayload.Entry` does not synchronize these fields.

### 8.2 Forbidden heuristics

The client must not infer provider/domain/school from:

- namespace conventions;
- resource-id prefixes/suffixes;
- translation-key patterns;
- icon path;
- client-maintained duplicated maps;
- assumptions about external mods.

### 8.3 Future contract

If these filters are promoted to implementation, first define a bounded server-authored presentation schema for the exact metadata required.

Any such schema must answer:

- authoritative field owner;
- allowed value format;
- per-entry size bound;
- total payload bound;
- reload invalidation;
- missing-value semantics;
- optional provider behavior.

Until then, the corresponding filter controls should not appear as fake/empty UI.

---

## 9. Icon presentation contract

`SpellPresentationPayload.Entry` already carries `iconId`, so icon use is an authorized planned refinement under 05.07.

### 9.1 Rules

- icon is presentation only;
- canonical spell identity remains `spellId`;
- missing/unresolvable icon never invalidates the spell;
- missing icon uses the 05.08 `PRESENTATION_FALLBACK` semantic;
- text name remains available;
- icon must not be treated as provider metadata;
- icon loading must remain bounded/client-only.

### 9.2 Resource safety

The current payload bounds icon-id string length but does not by itself prove the referenced client asset exists.

Therefore implementation must resolve artwork safely and fall back without throwing a screen-breaking error.

### 9.3 Clean-room

New Black Arcana-owned icon assets remain subject to project provenance/licensing rules.

Do not copy provider artwork merely to make the editor visually consistent.

---

## 10. Hazard presentation in the editor

Current synchronized hazard preflight may continue to provide concise spell risk context.

Rules:

- `NORMAL` tier must not activate danger styling under 05.08;
- non-`NORMAL` danger is informational/risk semantics, not loadout rejection by itself;
- recommendation met does not mean universally safe;
- missing hazard data is not a spell-unavailable signal;
- detailed hazard text should remain tooltip/contextual rather than dominating every catalog row.

05.10 does not add new hazard network fields.

---

## 11. Draft state model

A future editor should explicitly model local draft state without claiming server acceptance.

Conceptual states:

### `CLEAN`

Local draft equals the synchronized snapshot used as the editor baseline.

### `DIRTY`

Local draft differs from that baseline.

### `SUBMITTING`

An update request was emitted and the UI is awaiting server synchronization.

This state is only meaningful if the future screen remains open after submit or otherwise surfaces pending state.

### `SYNCHRONIZED`

A new authoritative server snapshot has been received.

Important: with the current protocol this state proves only that a server snapshot exists. It does **not** prove why the submitted request was accepted/rejected.

These names are conceptual, not required enum names.

---

## 12. Apply and server-reconciliation contract

### 12.1 Current behavior

Current `BlackArcanaLoadoutScreen.apply()`:

1. sends the complete draft;
2. closes immediately.

The reply later updates `ClientArcanaSyncState` through the ordinary snapshot channel.

### 12.2 Current evidence limit

The current reply does not contain:

- request id;
- accepted/rejected flag;
- reason code;
- reason text.

Therefore the UI must not display fabricated messages such as:

- `Loadout saved successfully`;
- `Spell unavailable`;
- `Server rejected slot 4`;

unless a future bounded result contract actually proves that statement.

### 12.3 Snapshot equality is not enough

Do not infer acceptance solely because the returned snapshot equals the submitted list.

Example failure mode:

- a stale accepted loadout still contains a spell whose execution runtime became unavailable;
- client resubmits the same list;
- server rejects the update and returns the existing canonical list;
- returned list equals submitted list even though the decision was rejection.

Therefore explicit decision feedback requires an explicit server-authored result contract.

### 12.4 First implementation options

A no-protocol editor hardening may choose either:

#### Option A — preserve close-after-apply

- send draft;
- close;
- next editor open uses the latest synchronized server state;
- no explicit save/reject claim.

This is fully compatible with current transport.

#### Option B — remain open awaiting snapshot

This requires careful event correlation because the same snapshot channel is used for ordinary synchronization and contains no request id.

Do not implement a fake correlation layer based only on timing.

If robust in-screen acknowledgement is required, use the future explicit result contract in Section 20.

### 12.5 Server always wins

After any synchronized snapshot:

- authoritative server order becomes canonical;
- client draft must not overwrite it silently;
- stale local draft must be reconciled or clearly separated from the new baseline.

---

## 13. Reset, clear and cancel semantics

### 13.1 Reset draft

Add a client-only conceptual operation:

`Reset draft to opening synchronized snapshot`

It must:

- discard only local unsaved changes;
- send no network packet;
- restore order/membership exactly to the editor baseline;
- clear dirty state.

If the screen later becomes live-updating, the reset baseline policy must be revisited explicitly.

### 13.2 Clear draft

Current Backspace/Delete behavior clears the local draft.

05.10 preserves that as local unsaved state until Apply.

### 13.3 Cancel/close

Closing without Apply discards local draft changes.

No update packet should be sent merely because the user exits the screen.

### 13.4 Distinguish Clear from Reset

These actions are different:

- Clear → local draft becomes empty;
- Reset → local draft becomes the synchronized opening state.

The UI must not label both as the same action.

---

## 14. Keyboard-accessibility relationship to 05.09

05.09 is the authority for screen-local focus/navigation.

05.10 adds editor operations that a keyboard path must eventually expose.

Requirements for implementation:

- search input must be reachable without breaking existing editor navigation;
- slot/order operations must be keyboard accessible if exposed;
- draft membership and keyboard focus remain semantically distinct;
- Enter keeps its existing Apply meaning unless an explicit reviewed migration changes it;
- Backspace/Delete current Clear semantics must not be silently changed because a search field exists;
- when text input owns focus, normal text-editing keys must not accidentally clear/apply/reorder the draft;
- screen ownership must continue suppressing world casting.

Because adding a text field changes key routing materially, implementation must update the 05.09 keyboard contract before code merges if the existing key semantics need context-sensitive exceptions.

---

## 15. Search-field key-routing rule

A future text-search field introduces a conflict with existing raw-screen shortcuts.

Therefore the implementation plan must distinguish:

### Search field focused

- printable input edits query;
- Backspace/Delete edit text through supported widget behavior;
- Enter behavior must be deliberately defined and tested;
- draft Clear must **not** fire from text editing keys;
- world casting remains suppressed.

### Search field not focused

Existing 05.09 screen navigation/apply/clear semantics remain active.

Do not implement global key interception that makes it impossible to edit text naturally.

---

## 16. Responsive information architecture

05.10 does not mandate one fixed pixel layout.

It mandates that the following concepts remain discoverable:

- configured order/slot number;
- quick-cast eligibility for positions 1–8;
- available spell identity;
- draft membership;
- current search query/results when search exists;
- Apply;
- Clear;
- Reset;
- Cancel/close.

### Normal viewport

A wider viewport may use separate regions/panels.

### Small viewport

A compact viewport may use:

- mode/tabs;
- stacked regions;
- one list with slot badges;
- contextual details.

The exact presentation can vary, but the dense ordered loadout model must remain clear.

No essential control may be placed off-screen without keyboard/page access.

---

## 17. Slot/order visual semantics

05.08 remains the meaning authority.

Useful independent roles include:

- `FOCUSED` — keyboard target;
- `HOVERED` — pointer target;
- `DRAFT_ONLY` — unsaved local difference/membership;
- synchronized accepted state — server baseline;
- `PRESENTATION_FALLBACK` — missing art;
- danger state — non-`NORMAL` synchronized risk metadata only.

Slot position is structural identity, not a readiness/success state.

A Quick Cast 1–8 marker must not use the same visual semantics as spell readiness.

---

## 18. Catalog sorting and identity

The available catalog may sort independently from loadout order.

Rules:

- canonical identity always comes from `spellId`;
- duplicate translated display names remain distinguishable by identity/context;
- changing locale may change catalog display sort without changing loadout order;
- sorting never mutates the draft;
- search/filter result order never becomes slot order automatically.

---

## 19. Performance boundaries

All first-stage editor refinements should remain bounded local work.

Do not introduce:

- per-keystroke server search;
- world/entity/chunk scans;
- provider API calls during each render/search event;
- per-tick loadout synchronization;
- unbounded icon loading queues;
- local copies of provider registries solely for filtering;
- O(world-size) operations.

Search/sort/filter operate over the already bounded synchronized presentation list.

Reorder operates over at most 16 loadout entries.

---

## 20. Optional future explicit apply-result contract

Explicit save/rejection feedback is not safely available today.

If implementation requirements promote it, design a bounded server-authored loadout-update result contract before UI work.

The contract should minimally answer:

- which client request the result corresponds to;
- whether the proposal was accepted;
- bounded machine-readable rejection category if rejected;
- authoritative resulting loadout snapshot or revision reference;
- protocol version/bounds;
- stale/out-of-order handling.

Do not send arbitrary exception text or provider internals to the client.

Potential rejection categories should derive from real server decisions rather than be invented client-side.

Examples of existing server decision concepts include:

- too large;
- duplicate spell;
- unknown spell;
- spell execution runtime unavailable.

Exact packet/class/enum names remain an implementation design task after protocol review.

---

## 21. Provider/domain/school metadata future extension

If classification filters are later approved, keep them separate from the loadout update result contract.

Classification is presentation metadata; update acceptance is transaction/result metadata.

Do not overload one payload with unrelated state merely to reduce packet count.

Any classification extension must preserve 05.07's bounded/event-driven synchronization rules.

---

## 22. TDD plan for future implementation

### 22.1 Draft-order RED tests

Add failing tests for:

- move first→last preserves all identities;
- move last→first preserves all identities;
- move middle positions preserves uniqueness;
- invalid indexes fail safely;
- reorder does not alter size;
- reorder does not send network state by itself;
- remove compacts later entries;
- add appends to trailing unused position;
- 16-entry bound remains enforced.

### 22.2 Search RED tests

Test deterministic local filtering for:

- empty query returns full catalog;
- case-insensitive display-name match;
- canonical-id match if enabled;
- no-match returns empty view without mutating draft;
- duplicate display names remain distinct by spell id;
- search does not reorder configured loadout;
- clearing query restores results.

### 22.3 Reset/dirty RED tests

Test:

- opening draft starts clean;
- toggle marks dirty;
- reorder marks dirty;
- clear marks dirty when baseline non-empty;
- reset restores exact opening order/membership;
- reset returns to clean;
- close without apply produces no update request.

### 22.4 Apply/reconciliation RED tests

Current-protocol tests should prove:

- apply sends complete ordered bounded snapshot;
- server preserves valid requested order;
- rejection returns canonical current server snapshot;
- client accepts server snapshot as authority;
- snapshot equality is not treated as proof of acceptance.

If Section 20 is implemented later, add request-correlation/out-of-order/reason tests before GREEN.

### 22.5 Icon/fallback RED tests

Where feasible in pure presentation helpers:

- valid icon id maps to icon presentation request;
- missing/unresolvable artwork chooses fallback semantics;
- missing art does not remove spell identity;
- icon state does not alter loadout membership.

---

## 23. Real-client validation plan

After implementation, validate with the exact modpack build.

### Editor basic flow

- open editor;
- add spell;
- remove spell;
- reorder populated spells;
- observe slot-number changes;
- verify slots 1–8 quick-cast eligibility markers are descriptive, not assumed-bound;
- Apply;
- reopen and confirm server-synchronized order.

### Dense-list behavior

- remove slot 2 from a multi-spell draft;
- verify later entries compact visibly;
- verify no fake blank slot is created;
- verify resulting radial/direct positions match accepted order after server sync.

### Search

- search by display name;
- search by canonical id if implemented;
- clear search;
- verify filtering never removes draft membership;
- verify keyboard text editing does not trigger Clear/Apply shortcuts.

### Reset/Clear/Cancel

- Reset restores opening synchronized state;
- Clear empties local draft only;
- Escape/cancel leaves server loadout unchanged;
- Apply is the only mutation request.

### Icons

- valid artwork displays;
- intentionally missing artwork falls back cleanly;
- no crash/off-screen corruption.

### Accessibility

Exercise 05.09 keyboard paths for every new editor operation that is promoted to implementation.

### Viewports

Test at least:

- 854×480;
- 1920×1080;
- 3440×1440;
- GUI scale Auto/2/3/4 where supported.

### Modpack coexistence

Verify no new key conflicts or HUD/actionbar interactions with current installed Stage 05 coexistence surfaces.

---

## 24. Acceptance failures that block implementation merge

A 05.10 implementation must not merge with:

- client-generated sparse slots sent as if server supported them;
- reorder changing spell identity/duplicates/size unexpectedly;
- reorder sending casts or server updates before Apply;
- search/filter changing server availability;
- provider/domain/school inferred from resource-id heuristics;
- missing icon causing gameplay unavailability;
- UI claiming successful save/rejection reason without server-authored proof;
- text-search Backspace/Delete accidentally clearing the draft;
- Enter behavior becoming ambiguous/unreviewed;
- Apply sending a different order than displayed;
- server canonical snapshot ignored after reply;
- screen interaction leaking world cast input;
- layout becoming unusable at required small viewport;
- mandatory provider/Controlling/controller dependency.

---

## 25. Relationship to Stage 05 completion

05.10 is a planning refinement.

Creating or merging this document does not change:

`IMPLEMENTED / FINAL VALIDATION DEFERRED`

The editor refinements become mandatory only when:

- a current manual Stage 05 acceptance row requires them;
- a directly observed required usability/accessibility defect makes them necessary;
- an explicit reviewed project decision promotes a specific refinement to required hardening.

Otherwise individual items remain approved follow-up work or Stage 09 carry candidates.

---

## 26. Implementation sequencing

If 05.10 implementation is approved, prefer this sequence:

### Phase A — no protocol extension

1. deterministic draft reorder helper;
2. slot-position/quick-cast eligibility presentation;
3. local Reset semantics;
4. search over existing display name/id;
5. icon rendering with fallback;
6. responsive/keyboard integration;
7. automated + real-client validation.

These can remain on current loadout protocol if no in-screen explicit result is required.

### Phase B — only if required

8. explicit apply acknowledgement/rejection-result protocol;
9. in-screen pending/confirmed/reconciled feedback;
10. server-authored classification metadata for provider/domain/school filters.

Do not pull Phase B into Phase A merely because the future features are desirable.

---

## 27. Non-goals

This plan does not authorize:

- sparse server loadout slots;
- more than 16 loadout entries;
- more than eight direct quick-cast mappings;
- binding number keys by default;
- client-authoritative acceptance;
- client-side spell availability decisions;
- duplicate spells in one loadout;
- provider/domain/school inference from names/ids;
- second loadout persistence store;
- per-keystroke networking;
- automatic server update on every drag/toggle;
- automatic casting from editor interactions;
- provider-specific resource/cooldown calculations;
- speculative protocol classes/methods;
- claiming explicit server rejection feedback exists today;
- implementation of Java/UI/network code in this planning change.

---

## 28. Exit criteria for this planning task

05.10 is planning-complete when:

- dense ordered list semantics are recorded explicitly;
- sparse-slot behavior is explicitly rejected without a future server migration;
- positions 1–8 quick-cast eligibility and 9–16 normal slot semantics are defined;
- reordering is proven compatible with the current ordered full-list protocol;
- remove/add compaction/append semantics are defined;
- local search fields are bounded to real synchronized data;
- provider/domain/school filters remain gated by missing server-authored metadata;
- icon fallback rules are defined;
- draft dirty/reset/clear/cancel semantics are defined;
- current snapshot-only apply evidence limits are recorded;
- snapshot equality is explicitly rejected as proof of acceptance;
- explicit ack/rejection UX is gated behind a future bounded result contract;
- search-field keyboard routing is reconciled with 05.09 requirements;
- performance and clean-room boundaries are preserved;
- TDD and real-client validation plans are explicit;
- Stage 05 completion state remains unchanged;
- no runtime/network/provider implementation is included in the planning diff.
