# 05.10 — Loadout Editor Implementation Checkpoint

## State

`PHASE A A.1–A.6 IMPLEMENTED / AUTOMATED GATES GREEN / A.7 REAL-CLIENT VALIDATION PENDING`

This checkpoint records implementation evidence for the contract defined by [`10-loadout-editor-information-architecture.md`](10-loadout-editor-information-architecture.md). It does not change the overall Stage 05 state: `IMPLEMENTED / FINAL VALIDATION DEFERRED` remains authoritative until the required physical real-client campaign is directly executed.

The original 05.10 document remains the planning/architecture contract. This file records what has actually been promoted into runtime on `feat/stage05-loadout-reorder`.

## Reconciliation baseline

- latest `main` used for the final pre-PR candidate: `6139f58bc0facaddc833fe4074f29dd1df4c6e75`;
- implementation branch: `feat/stage05-loadout-reorder`;
- reconciled runtime candidate before this documentation-only checkpoint: `086745176fba1c15b3cf1d16536e9b3616a52496`;
- merge parents of that candidate: `df43c9076f4bd86bc3c55a28be979b69b28e33d2` and `6139f58bc0facaddc833fe4074f29dd1df4c6e75`;
- comparison after reconciliation: branch ahead of that `main`, behind by zero commits;
- exact reconciled runtime workflow: `34421395161`, GREEN for JUnit/unit tests, diff sanity, NeoForge build, built-JAR verification, Foundation GameTests and dedicated-server smoke. Branch artifact publication was correctly skipped because the candidate was not `main`.

Because this checkpoint itself creates a newer branch HEAD, the final merge gate must run CI again on the exact documentation-inclusive HEAD and must repeat the latest-`main` reconciliation immediately before merge.

## Phase A implementation

### A.1 — Deterministic dense draft reorder

`LoadoutDraft` now supports bounded local reordering while preserving the existing dense ordered-list contract:

- at most 16 entries;
- no sparse slots;
- spell identities and uniqueness preserved;
- reorder changes only local unsaved draft order;
- no cast, resource/cooldown side effect or server update occurs before Apply;
- Apply continues to emit the existing complete ordered loadout snapshot.

### A.2 — Slot position and quick-cast eligibility presentation

The editor exposes the current 1-based populated slot position and distinguishes positions 1–8 as eligible for the existing eight direct quick-cast mappings without claiming that any mapping is currently bound. Positions 9–16 remain ordinary canonical loadout positions rather than unavailable/weaker slots.

### A.3 — Reset and dirty draft semantics

The editor keeps an opening synchronized baseline and can reset unsaved local edits back to that exact baseline. Reset remains distinct from Clear:

- Reset restores the opening ordered membership and clears local dirty state;
- Clear produces an empty local draft only;
- closing without Apply sends no loadout update;
- no second persistence store or client acceptance authority is introduced.

### A.4 — Bounded local catalog search

Search operates only over already-synchronized spell presentation data and resolves display name plus canonical spell id locally. It is bounded, case-insensitive, does not mutate loadout order/membership, does not issue per-keystroke networking and does not infer provider/domain/school from identifiers or translation metadata.

The search `EditBox` owns ordinary text-editing keys while focused so Backspace/Delete do not trigger draft Clear and printable input does not leak into world casting.

### A.5 — `iconId` rendering with safe fallback

The loadout editor now consumes synchronized `SpellPresentationPayload.Entry.iconId` through a bounded client-only resolver. Missing/unresolvable art degrades to a Black Arcana-owned placeholder while the text name and canonical spell identity remain available. Icon resolution does not decide spell availability, provider identity or gameplay legality.

TDD evidence for this tranche includes RED `898cf42f...` with the intended three missing-presentation failures, followed by the GREEN implementation and full CI on the subsequent candidate.

### A.6 — Responsive and keyboard integration

The loadout row icon size is bounded by responsive row geometry, preventing the added icon column from breaking compact layouts. Keyboard reorder is exposed as screen-local `Shift+Up` / `Shift+Down` over the focused catalog spell's current dense draft position while preserving existing controls:

- `Up` / `Down` continue to move focus;
- `Enter` remains Apply;
- the search widget gets first key ownership while focused;
- reorder does not create a new global `KeyMapping`;
- the screen consumes the reorder chord even at a movement boundary so it does not leak to world input;
- no packet, protocol field, server focus state or cast path was added.

TDD evidence: RED `12e6081652ffa4bcf92d3501f9c4dfa041b2ac6f` produced exactly the three intended contract failures; GREEN implementation is `df43c9076f4bd86bc3c55a28be979b69b28e33d2`; the implementation was then reconciled with current `main` into `086745176fba1c15b3cf1d16536e9b3616a52496`, whose full CI run `34421395161` passed.

## A.7 — Validation state

The automated portion has passed on the exact reconciled runtime candidate described above. The required physical real-client validation remains **PENDING** and is not inferred from CI.

The still-unexecuted 05.10 client campaign includes, at minimum:

- add/remove/reorder and server-resynchronized order;
- dense compaction after removal;
- search by display name/id and text-key routing;
- Reset/Clear/Cancel distinction;
- valid and deliberately missing icon behavior;
- keyboard accessibility for every promoted editor operation;
- viewport checks at 854×480, 1920×1080 and 3440×1440;
- GUI scale Auto/2/3/4 where supported;
- coexistence with the exact installed modpack surfaces.

No manual row is converted to PASS by this checkpoint.

## Authority and non-goals preserved

This Phase A implementation adds no sparse server loadout representation, no extra loadout capacity, no ninth direct quick-cast mapping, no default number-row binding, no client-authoritative admission, no provider/domain/school heuristic, no second cast pipeline, no second resource, no per-keystroke server search and no fabricated Apply success/rejection reason.

The existing server remains authoritative for accepted order, spell registration/availability, persistence and later cast-slot validation. Phase B remains unpromoted: explicit Apply acknowledgement/rejection UX and provider/domain/school classification metadata still require their own reviewed server-authored contracts if they ever become necessary.
