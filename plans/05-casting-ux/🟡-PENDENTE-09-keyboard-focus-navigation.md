# 05.09 — Keyboard Focus & Navigation

## State

`MERGED / AUTOMATED GATES GREEN / REAL-CLIENT VALIDATION DEFERRED`

This document records the implemented Stage 05 keyboard-only navigation and focus semantics inside Black Arcana's existing client screens.

Planning baseline: `main@2df7cdedd0a73b5aed87ca9709699e139355fc84`.
Implementation branch baseline: `main@3c9795820f48cbe01a28ed1d4c3f1238cce816a0`.
Implementation PR: **#157 — `feat: implement Stage 05 keyboard focus navigation`**.
Canonical runtime merge: `29a0099e899e03d80bf904c2d5ead72f40421fe8`.
Exact-SHA post-merge workflow: `34405514309` — GREEN through JUnit, diff sanity, NeoForge build, built-JAR verification, Foundation GameTests, dedicated-server smoke and canonical QA artifact publication.
Canonical QA artifact: `black-arcana-29a0099e899e03d80bf904c2d5ead72f40421fe8`, artifact ID `10125267266`, SHA-256 `de2da7faf18971c9f6e06b7b5896b0390c03c3a9b058b549f7b72eb6d5ec6030`.

The implementation is deliberately client-local. It adds no gameplay-authoritative packet, server focus state, provider hook, persistence channel, second cast path or new global key mapping. Real-client accessibility/coexistence acceptance remains deferred and must not be inferred from automated CI.

---

## 1. Why this work exists

Keyboard-only operation is an explicit Stage 05 refinement in:

- `02-radial-wheel.md`;
- `04-accessibility-client-config.md`;
- `08-visual-language-state-semantics.md`.

Before 05.09, both Black Arcana client screens required pointer precision for part of their interaction model. PR #157 closes that deterministic runtime gap while preserving the existing mouse paths and server authority.

### Implemented radial behavior

`BlackArcanaRadialScreen` now supports:

- mouse hover and mouse left-click selection;
- client-local canonical keyboard focus;
- deterministic initial focus on the selected visible slot, otherwise first visible slot;
- `Tab` / `Shift+Tab` same-page focus traversal with wrap;
- `Left` / `Page Up` previous-page behavior;
- `Right` / `Page Down` next-page behavior;
- page-change focus reconciliation;
- `Enter` / keypad Enter / `Space` selection-only activation of the focused wedge;
- the configured radial open key closing a `TOGGLE` radial;
- `HOLD` close when the radial key is released;
- independent keyboard/pointer presentation modality;
- non-color focus cues that remain distinct from hover and selected state.

Selecting from the radial still only changes `ClientLoadoutSelection`, marks the contextual selection change and closes the screen. It does **not** cast.

### Implemented loadout-editor behavior

`BlackArcanaLoadoutScreen` now supports:

- mouse hover and mouse left-click draft toggle;
- deterministic client-local row focus using the absolute synchronized `available` index;
- `Up` / `Down` row navigation with same-page clamp;
- `Space` toggling only the focused `LoadoutDraft` entry;
- `Enter` / keypad Enter applying the complete draft through the existing loadout update path;
- `Backspace` / `Delete` preserving the existing clear-all local-draft behavior;
- `Left` / `Page Up` previous-page behavior;
- `Right` / `Page Down` next-page behavior;
- page-change focus reconciliation preserving/clamping relative row position;
- keyboard-focused hazard tooltip presentation;
- independent pointer/keyboard modality and a visible non-color `[F]` focus cue.

No focus move and no `Space` draft toggle sends a cast request or directly changes server-owned accepted loadout state.

---

## 2. Authority boundaries

Keyboard navigation is presentation/input ergonomics only.

It preserves:

- D005 — direct casting remains available without a universal staff requirement;
- D006 — server owns cast legality, resource cost, cooldown, progression, targeting and world effects;
- D020 — client sends bounded intention, not authoritative gameplay values;
- D023 — no new per-tick server synchronization for focus state;
- D024 — channel/release still converges on the canonical server cast coordinator;
- the server-owned loadout acceptance contract;
- the non-casting nature of radial selection.

Keyboard focus itself is **client-local transient state**.

It does not:

- modify the accepted loadout merely by moving focus;
- cast a spell merely by moving focus;
- bypass GUI-focus suppression in `ClientInputController`;
- become a new network field;
- become persistent player progression/gameplay state;
- infer provider resource/cooldown legality;
- force chunks or scan world state.

---

## 3. Relationship to 05.08 visual semantics

`08-visual-language-state-semantics.md` defines:

- `FOCUSED`;
- `HOVERED`;
- `SELECTED`;
- `DRAFT_ONLY`;
- accepted synchronized state.

05.09 operationalizes those roles for keyboard interaction.

The meanings remain independent:

- `FOCUSED` = current keyboard navigation target;
- `HOVERED` = current pointer target;
- `SELECTED` = current selected loadout slot used by the existing client selection model;
- `DRAFT_ONLY` = local unsaved editor membership/change;
- accepted loadout = latest synchronized server-owned state.

`CastingUxSemantics.FocusState` now represents the bounded combinations required by the radial: none, selected, hovered, focused and their composites. Focus is not presented as legality, readiness or server acceptance.

A focused row/wedge is not automatically selected, accepted, ready or cast.

---

## 4. Input-design rule: no new global default key

The implementation uses keys **while a Black Arcana screen already owns focus** rather than registering more global Minecraft key mappings.

Reasons:

- the modpack already has many key mappings;
- direct quick-cast slots are intentionally unbound by default;
- navigation keys inside an open `Screen` do not need another global binding;
- this keeps Controlling/vanilla keybinding surfaces simpler;
- controller integration remains a separate optional provider-dependent layer.

No new global mapping was added by PR #157.

If later evidence shows a dedicated global navigation mapping is required, it needs a fresh current-modpack key-conflict audit before implementation.

---

## 5. Input modality model

Stage 05 screens receive both pointer and keyboard input.

The implementation tracks presentation-only modality through `KeyboardFocusNavigation.InputModality`:

- `POINTER`;
- `KEYBOARD`.

### Pointer activity

Meaningful pointer movement over an interactive row/wedge, or mouse activation, makes pointer presentation primary without silently rewriting canonical keyboard focus.

### Keyboard activity

A handled keyboard navigation/activation action makes keyboard presentation primary.

### Rules

- switching modality never sends gameplay intent by itself;
- pointer hover does not silently rewrite keyboard focus;
- keyboard focus does not move the physical mouse cursor;
- focused spell/tooltip presentation follows keyboard modality;
- pointer hover presentation follows pointer modality;
- selected loadout state remains independent of modality;
- screen-local focus/modality disappears with the screen instance.

---

## 6. Radial keyboard-focus model

### 6.1 Initial focus

When the radial opens, keyboard focus initializes predictably:

1. selected slot if that slot is visible on the opening page;
2. otherwise the first visible slot on the current page;
3. no focus only when no visible slot exists.

The current radial opens on the page derived from the selected slot, so the normal path focuses the selected slot.

### 6.2 Focus identity

Keyboard focus uses the canonical loadout slot index, not merely the visual wedge index.

This matters because:

- page 1 may contain slots 0–7;
- page 2 may contain slots 8–15;
- focus must survive deterministic page movement;
- UI code must not confuse `visibleIndex` with the canonical loadout slot.

### 6.3 Canonical radial traversal contract

The implemented screen-local controls are:

- `Tab` → focus next visible wedge on the **current page**;
- `Shift+Tab` → focus previous visible wedge on the **current page**;
- `Enter`, keypad Enter or `Space` → select the focused wedge and close the radial;
- `Page Up` → previous page;
- `Page Down` → next page;
- `Left` → previous page, preserving existing behavior;
- `Right` → next page, preserving existing behavior;
- `Escape` → vanilla screen close without changing selection.

Traversal boundary is frozen and implemented:

- `Tab` wraps last → first on the current visible page;
- `Shift+Tab` wraps first → last on the current visible page;
- Tab traversal never changes radial page;
- page changes occur only through the existing page controls;
- a one-entry page keeps focus on that single entry;
- an empty visible set has no focus and activation safely does nothing.

### 6.4 Page transition focus

When moving between radial pages:

1. if the current selected slot belongs to the destination page, focus that selected slot;
2. otherwise preserve the prior visible wedge position when it exists on the destination page;
3. otherwise clamp to the last visible wedge on the destination page;
4. if no visible slot exists, clear focus.

Additional rules:

- page transition never activates a wedge;
- page transition never casts;
- focus never points to an off-page canonical slot;
- empty/stale states fail safely through bounded helper logic.

### 6.5 Selection

Keyboard selection reuses the same existing client selection operation used by mouse selection:

- select canonical slot in `ClientLoadoutSelection`;
- mark contextual selection change;
- close the radial;
- do **not** cast.

`BlackArcanaRadialScreen.selectFocused(...)` is a bounded selection seam for tests and does not call a cast engine or cast network bridge.

### 6.6 `TOGGLE` mode

The radial open key remains a close action when the same mapping is pressed while a `TOGGLE` radial is open.

That close action:

- does not select the focused wedge automatically;
- does not cast;
- discards transient focus state with the screen instance.

### 6.7 `HOLD` mode

In `HOLD` mode:

- the radial remains open only while the configured radial key is down;
- keyboard focus may move while it is held;
- releasing the radial key closes without automatically selecting the focused wedge unless selection was explicitly activated first;
- focus handling does not replace the existing release-close check;
- no server focus state exists to become stuck across close/reconnect.

A physical-client check for stuck cursor/key behavior remains part of deferred manual validation.

---

## 7. Radial pointer + keyboard coexistence

### 7.1 Hover remains hover

Pointer hover remains calculated from current mouse geometry.

It does not become `SELECTED` merely because keyboard focus exists elsewhere.

### 7.2 Focus visualization

05.08 requires `FOCUSED`, `HOVERED` and `SELECTED` to remain distinguishable.

The radial now composes these facts independently. Focus has a distinct border/background treatment and a non-color `[F]`/compact `F` marker; selected and hovered markers remain independently representable.

The same wedge may legitimately have two or three roles simultaneously.

### 7.3 Tooltip/center presentation

When active modality is keyboard, focused spell information can drive:

- compact-mode tooltip equivalent;
- focused spell identity;
- static hazard line.

When active modality is pointer, hover drives those details.

Fallback remains the current selected spell when neither temporary target applies.

This is presentation only; 05.07 still governs which data is legitimate to render.

---

## 8. Loadout-editor keyboard-focus model

### 8.1 Initial focus

When the loadout editor initializes, keyboard focus starts on:

1. the first visible entry already part of the synchronized accepted loadout when practical;
2. otherwise the first visible entry;
3. no focus when the available list is empty.

A future search/filter operation needs a separate focus-reset rule; search is not currently implemented.

### 8.2 Row focus

Focus uses the absolute index in the `available` synchronized presentation list.

The implementation does not identify a row solely by screen Y coordinate.

Focus remains bounded across:

- page changes;
- viewport/layout recalculation;
- empty presentation sets;
- current screen-instance lifecycle.

### 8.3 Canonical row navigation contract

Implemented controls while the loadout screen owns focus:

- `Up` → previous visible/available row;
- `Down` → next visible/available row;
- `Space` → toggle the focused spell in the local `LoadoutDraft`;
- `Left` / `Page Up` → previous page;
- `Right` / `Page Down` → next page;
- `Enter` / keypad Enter → apply the draft;
- `Backspace` / `Delete` → clear the local draft;
- `Escape` → vanilla screen close without applying new draft changes.

Row-boundary behavior is frozen and implemented:

- `Up` at the first row of the current page clamps to that first row;
- `Down` at the last row of the current page clamps to that last row;
- Up/Down do not wrap and do not change pages;
- page traversal remains explicit through Left/Right/Page Up/Page Down;
- an empty list has no focused row and Space performs no toggle.

### 8.4 Page movement

After moving pages:

1. preserve the prior relative row position when that row exists on the destination page;
2. otherwise clamp to the last available row on that page;
3. an empty presentation set produces no row focus.

Page changes themselves do not toggle draft membership or apply the draft.

### 8.5 Toggle behavior

Keyboard `Space` invokes the same bounded `LoadoutDraft.toggle` semantics used by mouse interaction.

It does not send a network update.

Only the existing apply operation sends the complete bounded draft intent to the server through `LoadoutNetworkBridge`.

### 8.6 Clear behavior

Backspace/Delete continue to clear the draft.

Because draft changes remain local until apply, this is not a direct server mutation.

The implementation preserves:

- Delete on a focused row is **not** “remove only this row”;
- existing clear-all semantics;
- focus remains valid after draft clear because `available` entries still exist.

---

## 9. Loadout pointer + keyboard coexistence

Mouse hover and keyboard focus are independent.

Rules implemented by the editor:

- a mouse click toggles the clicked spell using the existing draft path;
- pointer hover may drive hazard tooltip presentation;
- keyboard focus drives equivalent hazard tooltip presentation when keyboard modality is active;
- mouse movement does not apply or submit draft state;
- keyboard focus does not imply the row is included in the draft;
- accepted/draft membership markers continue to describe `CastingUxSemantics.loadoutMembership(...)`, not focus;
- focused rows add a separate non-color `[F]` marker.

---

## 10. Focus lifecycle and stale-state rules

### Open / init

Initialize bounded focus from current synchronized client snapshots using Sections 6.1 and 8.1.

### Resize / GUI scale change

When `Screen.init()` runs again after resize/layout change:

- keep the same canonical focused item when it still exists;
- recalculate its visual location from the current layout;
- clamp page/focus if the previous arrangement is no longer valid.

### Synchronized snapshot replacement

Current screens snapshot state at construction rather than live-replacing their lists.

05.09 does not change that contract.

If a future screen becomes live-updating:

- canonical identity must be used to reconcile focus;
- removed entries clear/move focus deterministically;
- stale focus cannot activate a removed spell.

### Close

All screen-local focus/modality state disappears with the screen.

### Reconnect

No keyboard focus state survives reconnect as authoritative state.

New screens initialize from fresh synchronized snapshots.

---

## 11. No-cast-through-screen invariant

`ClientInputController` suppresses direct cast processing while a `Screen` owns focus.

05.09 preserves that architecture and does not add a cast bridge to either screen.

A key such as Space, Enter, arrow, Tab, Page Up or Page Down used inside a Black Arcana screen must not simultaneously trigger a normal world cast intent.

Static/wiring tests protect the absence of a screen-local cast path, but physical key mapping/event ordering in the full modpack still requires direct real-client validation.

Any duplicate world cast generated while a Stage 05 screen is open is a blocking regression.

---

## 12. Rebindability and Controlling

05.09 adds no global key mapping for focus traversal.

Therefore:

- current Black Arcana global mappings remain registered through vanilla `KeyMapping`;
- Controlling continues to discover those mappings naturally;
- keyboard navigation inside `Screen` uses screen-local controls rather than polluting the global key list;
- absence of Controlling does not affect screen navigation;
- no other mod's key mapping is rewritten.

If implementation later adds a new global action, 05.06 key-conflict rules apply first.

---

## 13. Controller boundary

No general controller framework is confirmed in the current physical modlist.

Controller implementation remains optional/provider-dependent.

A future verified controller integration should map directional/focus/activate/cancel actions onto the same **screen navigation operations**, not create controller-specific gameplay logic.

A future provider may map:

- move focus;
- change page;
- activate focused entry;
- cancel/close.

But:

- exact provider/version/API must be verified first;
- keyboard/mouse remains fully functional without the provider;
- activation must reuse existing radial selection/loadout draft operations;
- no provider button may send an authoritative cast result from the client.

---

## 14. Accessibility requirements

Keyboard-only navigation is an accessibility feature, but it does not create a second semantic authority mode.

Implemented deterministic requirements:

- focused state has a visible non-color-only cue;
- focus order is deterministic;
- the player can identify the keyboard target before activation;
- no pointer precision is required to select a radial wedge;
- no pointer precision is required to toggle a loadout entry;
- closing/cancelling remains available;
- selection and activation remain distinct where the existing surface defines them as distinct;
- keyboard-focused hazard information is available from already-synchronized data.

Still requiring direct real-client evidence:

- readability at the Stage 05 small-viewport matrix;
- no stuck cursor/key state;
- physical keyboard/pointer modality behavior in the target pack;
- interaction with Controlling, Spell Actionbar and Epic Fight.

Reduced motion/flashes must apply to any future animated focus treatment. PR #157 adds no new animation.

---

## 15. Localization and labels

The implementation does not add a new immutable English-only player-facing navigation hint.

Existing localized screen/key labels remain unchanged. The visual focus marker is symbolic (`[F]`) rather than a sentence containing hardcoded English key names.

Any future expanded navigation hint should:

- use translation keys;
- use Minecraft-supported key-label components where appropriate;
- remain optional/compact on small viewports;
- not require displaying every action simultaneously;
- preserve semantic action wording after rebinding global keys.

---

## 16. Visual-language mapping

The following 05.08 semantic roles are directly relevant to 05.09:

| Interaction fact | Semantic role | Notes |
|---|---|---|
| keyboard target | `FOCUSED` | no legality or selection implication |
| pointer target | `HOVERED` | no automatic keyboard focus requirement |
| radial chosen slot | `SELECTED` | existing client selection; still non-casting |
| loadout row included in unsaved draft | `DRAFT_ONLY` / draft membership | not server acceptance |
| loadout accepted snapshot | synchronized authoritative loadout | server remains authority |
| keyboard focus + danger | orthogonal composition | danger styling only for authorized hazard facts |
| keyboard focus + forecast block | orthogonal composition | focus does not cause block |
| focus with missing icon | `FOCUSED + PRESENTATION_FALLBACK` | spell remains valid |

No single focus border/color is reused as an authoritative denial marker.

---

## 17. Performance boundaries

Keyboard focus state is tiny client-local state.

The implementation introduces no:

- world scans;
- entity scans;
- chunk queries;
- server requests on focus movement;
- per-tick full state synchronization;
- provider API calls merely to move focus;
- dynamic allocation proportional to world state.

Focus traversal operates on the already-snapshotted bounded radial/loadout lists.

Radial maximum visible entries remain eight per page.

Loadout editor remains bounded by synchronized spell presentation limits and viewport pagination.

---

## 18. Implemented architecture

PR #157 uses a small deterministic client-only helper, `KeyboardFocusNavigation`, rather than putting page/traversal math into gameplay/network code.

Its responsibilities are bounded to:

- input modality identity;
- radial initial focus;
- radial next/previous same-page traversal;
- radial page-transition focus reconciliation;
- loadout initial focus;
- loadout row clamp navigation;
- loadout page-transition focus reconciliation;
- invalid/empty-state clamping.

Surface code remains responsible for:

- rendering and geometry;
- pointer hit testing;
- invoking existing draft/selection operations when activation occurs.

The helper contains no casting, cost, cooldown, hazard, persistence or provider authority.

---

## 19. TDD implementation evidence

05.09 was implemented through explicit RED → GREEN cycles.

### 19.1 Navigation helper RED → GREEN

- RED commit `dc457ad711ba02e9e14bdc04d3a61e69752d8425`: deterministic navigation contracts were added before production helper code; CI failed in `Unit tests` as expected.
- GREEN helper commit `c7f196daf5d0737b371f6e23b40db7b7885821b7`: `KeyboardFocusNavigation` satisfied those pure contracts; unit tests and subsequent automated stages advanced successfully.

Covered contracts include:

- radial initial focus and empty safety;
- Tab/Shift+Tab same-page wrap;
- single-entry stability;
- radial page reconciliation;
- loadout initial focus;
- Up/Down same-page clamp;
- loadout page reconciliation;
- empty-state safety.

### 19.2 Screen integration and promotion

- RED commit `9032aaae705cb426e59f056a1293a01c81a22dca`: screen integration/wiring contracts were added before radial/loadout production wiring; CI failed in `Unit tests` as expected.
- GREEN implementation head `8fcc90fc4b5e5b82519d63c5a1d2a93b543820da`: full CI pipeline passed after radial/loadout integration.
- reviewed semantic/test head `3e560b202a0fd35630fd366293d35c7ad03ca31e`: workflow `34403555530` passed JUnit, diff sanity, NeoForge build, built-JAR verification, Foundation GameTests and dedicated-server smoke.
- final reconciled PR head `4f451a67d471f9373ff64050f5284a66e0869fd1`: both push workflow `34405021764` and PR workflow `34405028047` passed the complete pre-merge gate.
- canonical merge `29a0099e899e03d80bf904c2d5ead72f40421fe8`: exact-SHA post-merge workflow `34405514309` passed the complete pipeline and published the canonical QA artifact recorded above.

Additional regression coverage verifies:

- focused/hovered/selected semantic combinations;
- non-color radial focus markers;
- radial activation uses selection semantics only;
- loadout `Space` toggles only the focused draft entry;
- source wiring contains no new cast-packet path merely for focus navigation.

Automated tests are implementation evidence only. They do not convert Section 20 real-client rows to PASS.

---

## 20. Real-client validation plan — still pending

Automated focus tests are insufficient for physical input acceptance.

Directly test:

### Radial

- mouse-only selection still works;
- keyboard-only focus traversal;
- Tab wrap from last→first on each page;
- Shift+Tab wrap from first→last on each page;
- keyboard-only selection;
- `TOGGLE` mode;
- `HOLD` mode;
- page 1 and page 2 of a full 16-slot loadout;
- pointer → keyboard modality switch;
- keyboard → pointer modality switch;
- Escape/close without changing selection;
- no cast produced merely by selecting;
- separate cast input works only after the radial closes;
- no stuck cursor/key state.

### Loadout

- keyboard-only row traversal;
- Up/Down clamping at page boundaries;
- keyboard-only draft toggle;
- keyboard page movement;
- Enter apply;
- Escape close without apply;
- Delete/Backspace clear draft behavior;
- pointer and keyboard mixed use;
- reopen after apply shows server-synchronized state.

### Viewport/accessibility matrix

Exercise relevant paths at:

- 854×480;
- 1920×1080;
- 3440×1440;
- GUI scale Auto/2/3/4 where supported.

Confirm focus indication is readable without color alone.

### Modpack coexistence

Repeat representative keyboard-only behavior with:

- Controlling installed;
- Spell Actionbar visible where legitimate;
- Epic Fight battle mode active for radial/cast coexistence.

No current external provider must be modified to support the navigation.

All rows remain `PENDING` until directly observed. CI does not make them PASS.

---

## 21. Acceptance failures that block release acceptance

05.09 must not be accepted with:

- keyboard focus causing a cast;
- focus movement changing server loadout;
- keyboard activation using a second cast path;
- radial close implicitly selecting a different spell;
- Tab/Shift+Tab changing radial pages;
- radial traversal failing the frozen same-page wrap contract;
- loadout Up/Down wrapping or changing pages instead of clamping;
- page movement producing invalid/off-page focus;
- Enter unexpectedly changing from apply semantics;
- screen navigation leaking through to world casting;
- stuck key/cursor state;
- focus invisible except by color;
- keyboard navigation breaking current mouse behavior;
- mandatory dependence on Controlling or a controller provider.

Deterministic items are covered by current tests/wiring review. Physical-input/coexistence items remain release/manual acceptance obligations under D031.

---

## 22. Optional future refinements

The following are not required by the first keyboard-only implementation:

- spatial arrow-key navigation around radial angles;
- Home/End row jumps;
- type-to-search in the loadout editor;
- provider/domain/school filter keyboard shortcuts;
- configurable screen-local navigation bindings;
- gamepad-specific prompts;
- haptics;
- narration integration beyond what supported Minecraft GUI APIs provide naturally;
- mouse-warp-to-focus behavior.

Each may be evaluated later from real-client usability evidence.

Do not implement all of them merely because they are listed.

---

## 23. Relationship to Stage 05 completion

05.09 is an implemented and merged Stage 05 follow-up hardening change, but it does **not** change the parent Stage 05 validation state.

Current parent state remains:

`IMPLEMENTED / FINAL VALIDATION DEFERRED`

Reason:

- deterministic keyboard focus/navigation behavior is implemented, merged and automated gates are green on both the final PR head and exact merge SHA;
- the Stage 05 real-client visual/input matrix remains genuinely unexecuted;
- the physical-input/accessibility/coexistence rows in Section 20 are also unexecuted.

The current manual matrix and real-client runbook remain the authority for actual closeout PASS/BLOCKED status.

---

## 24. Non-goals

05.09 does not authorize or implement:

- new gameplay key mappings by default;
- client-authoritative casting;
- a second cast pipeline;
- automatic casting from focus movement;
- automatic casting from radial selection;
- client-side cooldown/cost/progression authority;
- changing the 16-slot server loadout bound;
- changing eight direct quick-cast mappings;
- changing current global `R`/`V` defaults;
- rewriting external mod bindings;
- mandatory Controlling integration;
- speculative controller APIs;
- provider-specific input hooks without verified APIs;
- world/entity scans for navigation;
- turning focus into server-persistent state;
- declaring keyboard accessibility manually validated from CI.

---

## 25. Implementation promotion evidence

The implementation portion of 05.09 has satisfied its deterministic promotion criteria:

- current mouse/keyboard behavior is recorded accurately;
- radial keyboard focus has deterministic initialization/navigation/activation semantics;
- radial Tab/Shift+Tab traversal is same-page wrap;
- loadout Up/Down behavior is same-page clamp;
- loadout keyboard focus has deterministic row/page/toggle/apply semantics;
- existing Left/Right/PageUp/PageDown and Enter/Delete behavior is preserved;
- focus, hover, selection and draft membership remain semantically distinct under 05.08;
- no new global default mapping exists;
- no focus action grants gameplay authority;
- controller support remains optional/provider-dependent;
- stale/resize/session focus behavior is bounded;
- performance remains bounded/client-local;
- RED→GREEN evidence exists for deterministic behavior and screen wiring;
- final reconciled PR HEAD passed the complete CI pipeline;
- PR review had no unresolved blocking findings;
- exact merge SHA passed the complete post-merge CI pipeline and published the canonical QA artifact;
- Stage 05 real-client validation state remains unchanged and explicitly deferred.

05.09 is **not** `VALIDATED / COMPLETE` until the applicable Section 20/manual Stage 05 acceptance rows have direct evidence.
