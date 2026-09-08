# 05.09 — Keyboard Focus & Navigation

## State

`PLANNING / NO RUNTIME CHANGE / ACCESSIBLE SCREEN NAVIGATION`

This document defines the canonical Stage 05 plan for keyboard-only navigation and focus semantics inside Black Arcana's existing client screens.

Baseline used to author this plan: `main@2df7cdedd0a73b5aed87ca9709699e139355fc84`.

This is a planning artifact only. It does **not** add key mappings, focus state, widgets, controller hooks, packets, client config, Java runtime behavior or visual assets.

---

## 1. Why this plan exists

Keyboard-only operation is already an explicit planned refinement in:

- `02-radial-wheel.md`;
- `04-accessibility-client-config.md`;
- `08-visual-language-state-semantics.md`.

The current runtime only partially satisfies that goal.

### Current radial behavior

`BlackArcanaRadialScreen` currently supports:

- mouse hover;
- mouse left-click selection;
- left arrow / Page Up for previous page;
- right arrow / Page Down for next page;
- the configured radial open key closing a `TOGGLE` radial;
- `HOLD` close when the radial key is released.

It does **not** currently expose a keyboard focus index for visible wedges and does not select a wedge through keyboard-only input.

### Current loadout-editor behavior

`BlackArcanaLoadoutScreen` currently supports:

- mouse hover;
- mouse left-click draft toggle;
- Enter / keypad Enter to apply the draft;
- Backspace / Delete to clear the draft;
- left arrow / Page Up for previous page;
- right arrow / Page Down for next page.

It does **not** currently expose keyboard row focus or a keyboard-only draft-toggle path.

Therefore a player who cannot or does not want to use precise mouse pointing cannot currently complete every Stage 05 screen interaction through keyboard input alone.

05.09 plans that missing interaction layer without changing Black Arcana gameplay authority.

---

## 2. Authority boundaries

Keyboard navigation is presentation/input ergonomics only.

It must preserve:

- D005 — direct casting remains available without a universal staff requirement;
- D006 — server owns cast legality, resource cost, cooldown, progression, targeting and world effects;
- D020 — client sends bounded intention, not authoritative gameplay values;
- D023 — no new per-tick server synchronization for focus state;
- D024 — channel/release still converges on the canonical server cast coordinator;
- the server-owned loadout acceptance contract;
- the non-casting nature of radial selection.

Keyboard focus itself is **client-local transient state**.

It must never:

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

A focused row/wedge is not automatically selected, accepted, ready or cast.

---

## 4. Input-design rule: no new global default key required

The first implementation of keyboard-only screen navigation should use keys **while a Black Arcana screen already owns focus** rather than registering more global Minecraft key mappings.

Reasons:

- the modpack already has many key mappings;
- direct quick-cast slots are intentionally unbound by default;
- navigation keys inside an open `Screen` do not need to consume another global binding;
- this keeps Controlling/vanilla keybinding surfaces simpler;
- controller integration remains a separate optional provider-dependent layer.

No new default global mapping is approved by this plan.

If later evidence shows a dedicated global navigation mapping is required, it needs a fresh current-modpack key-conflict audit before implementation.

---

## 5. Input modality model

Stage 05 screens may receive both pointer and keyboard input.

The implementation should track **active navigation modality** for presentation only.

Conceptual modalities:

- `POINTER`;
- `KEYBOARD`.

These names are conceptual, not required Java enum names.

### Pointer activity

A meaningful mouse movement over an interactive row/wedge or a mouse click may make pointer hover the primary focus cue.

### Keyboard activity

A keyboard navigation action makes keyboard focus the primary focus cue.

### Rules

- switching modality never sends gameplay intent by itself;
- pointer hover does not silently rewrite keyboard focus unless a deliberate implementation rule says so;
- keyboard focus does not move the physical mouse cursor;
- the focused spell/tooltip may follow the active modality;
- selected loadout state remains independent of modality;
- modality is cleared when the screen closes.

---

## 6. Radial keyboard-focus model

### 6.1 Initial focus

When the radial opens through keyboard input, keyboard focus should start predictably.

Preferred order:

1. selected slot if that slot is visible on the opening page;
2. otherwise the first visible slot on the current page;
3. no focus only when no visible slot exists.

The current radial already opens on the page derived from the selected slot, so the usual path should focus the selected slot.

### 6.2 Focus identity

Keyboard focus uses the canonical loadout slot index, not merely the visual wedge index.

This matters because:

- page 1 may contain slots 0–7;
- page 2 may contain slots 8–15;
- focus must survive deterministic page movement;
- UI code must not confuse `visibleIndex` with the canonical loadout slot.

### 6.3 Focus navigation without breaking current paging

The current runtime already uses:

- `Left` / `Page Up` for previous radial page;
- `Right` / `Page Down` for next radial page.

The first keyboard-navigation implementation should **not silently repurpose those keys** without a real-client migration/usability decision.

Preferred first implementation:

- `Tab` → focus next visible wedge;
- `Shift+Tab` → focus previous visible wedge;
- `Enter` or `Space` → select the focused wedge and close the radial;
- `Page Up` → previous page;
- `Page Down` → next page;
- preserve current `Left`/`Right` page behavior unless a separately reviewed usability change replaces it;
- `Escape` → close without changing selection.

This gives keyboard-only operation while preserving existing page controls.

The exact use of Enter/Space must be validated against vanilla `Screen` behavior before implementation; do not invent raw key handling that conflicts with superclass accessibility semantics.

### 6.4 Page transition focus

When moving between radial pages:

- if the current selected slot belongs to the destination page, focus may land on that selected slot;
- otherwise preserve a deterministic relative wedge position when possible;
- otherwise focus the first visible destination slot;
- never leave focus pointing to an off-page canonical slot;
- empty pages are impossible after canonical clamping and must fail safely if state becomes stale.

### 6.5 Selection

Keyboard selection must reuse the same existing client selection operation used by mouse selection:

- select canonical slot in `ClientLoadoutSelection`;
- mark contextual selection change;
- close the radial;
- do **not** cast.

No keyboard-only code path may call a different gameplay/cast engine.

### 6.6 `TOGGLE` mode

Keyboard focus must coexist with the existing `TOGGLE` behavior.

The radial open key remains a close action when the same mapping is pressed while the radial is open.

That close action:

- does not select the focused wedge automatically;
- does not cast;
- clears transient focus state with the screen lifecycle.

### 6.7 `HOLD` mode

In `HOLD` mode:

- the radial remains open only while the configured radial key is down;
- keyboard focus may move while it is held;
- releasing the radial key closes without automatically selecting the focused wedge unless the player explicitly activated selection before release;
- focus handling must not interfere with detection of the radial key release;
- no stuck key/cursor state is allowed after close.

---

## 7. Radial pointer + keyboard coexistence

### 7.1 Hover remains hover

Pointer hover remains calculated from current mouse geometry.

It must not become `SELECTED` merely because keyboard focus exists elsewhere.

### 7.2 Focus visualization

05.08 requires `FOCUSED`, `HOVERED` and `SELECTED` to remain distinguishable.

A later implementation may render them differently, but the semantic priority is:

- focused = keyboard target;
- hovered = mouse target;
- selected = currently selected loadout slot.

The same wedge may legitimately have two or three of those roles simultaneously.

### 7.3 Tooltip/center presentation

When the active modality is keyboard, focused spell information should be eligible to drive:

- compact-mode tooltip equivalent;
- center spell identity;
- static danger line.

When the active modality is pointer, hover may drive those details.

Fallback remains current selected spell when neither temporary focus exists.

This is presentation only; 05.07 still governs which data is legitimate to render.

---

## 8. Loadout-editor keyboard-focus model

### 8.1 Initial focus

When the loadout editor opens, keyboard focus should start on:

1. the first visible entry that is already part of the synchronized loadout when practical; or
2. the first visible entry.

A future search/filter operation may need a separate focus-reset rule, but search is not currently implemented.

### 8.2 Row focus

Focus uses the absolute index in the `available` synchronized presentation list.

The implementation must not identify a row solely by screen Y coordinate.

Focus must remain bounded against:

- page changes;
- viewport/layout recalculation;
- empty presentation sets;
- future search/filter subsets.

### 8.3 Row navigation

Preferred first implementation while the loadout screen owns focus:

- `Up` → previous visible/available row;
- `Down` → next visible/available row;
- `Space` → toggle the focused spell in the local `LoadoutDraft`;
- `Left` / `Page Up` → previous page, preserving existing behavior;
- `Right` / `Page Down` → next page, preserving existing behavior;
- `Enter` / keypad Enter → apply the draft, preserving existing behavior;
- `Backspace` / `Delete` → clear the local draft, preserving existing behavior;
- `Escape` → close without applying new draft changes.

This avoids changing the current Enter-to-apply contract merely to gain row activation.

### 8.4 Page movement

After moving pages:

- focus must move to a valid row on the new page;
- preserve relative row position when possible;
- otherwise clamp to the last available row on that page;
- an empty presentation set produces no row focus;
- page changes themselves do not toggle draft membership.

### 8.5 Toggle behavior

Keyboard `Space` must invoke the same bounded `LoadoutDraft.toggle` semantics as mouse left-click.

It does not send a network update.

Only the existing apply operation sends the complete bounded draft intent to the server.

### 8.6 Clear behavior

Backspace/Delete currently clears the draft.

Because draft changes remain local until apply, this is not a direct server mutation.

Nevertheless keyboard-focus implementation must ensure:

- Delete on a focused row does **not** become “remove only this row” accidentally;
- existing clear-all semantics are preserved unless a separately reviewed UX change intentionally changes them;
- focus remains valid after draft clear because `available` entries still exist.

---

## 9. Loadout pointer + keyboard coexistence

Mouse hover and keyboard focus are independent.

Rules:

- a mouse click toggles the clicked spell using the existing draft path;
- pointer hover may drive hazard tooltip presentation;
- keyboard focus may drive an equivalent tooltip/focus presentation when keyboard modality is active;
- mouse movement does not apply or submit draft state;
- keyboard focus does not imply the row is included in the draft;
- chosen `[x]` state continues to describe `draft.contains(spell)`, not focus.

The visual design must follow 05.08 so focused, hovered and chosen states cannot be confused.

---

## 10. Focus lifecycle and stale-state rules

### Open

Initialize bounded focus from current synchronized client snapshots.

### Resize / GUI scale change

If screen dimensions/layout change while open:

- keep the same canonical focused item when it still exists;
- recalculate its visual location from the current layout;
- clamp page/focus if the previous visible arrangement is no longer valid.

### Synchronized snapshot replacement

Current screens snapshot state at construction rather than live-replacing their lists.

05.09 does not change that contract by itself.

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

`ClientInputController` already suppresses direct cast processing while a `Screen` owns focus.

05.09 must preserve that invariant.

A key such as Space, Enter, arrow, Tab, Page Up or Page Down used inside a Black Arcana screen must not simultaneously trigger a normal world cast intent.

This requires real-client validation because physical key mappings and event ordering can interact with the large modpack.

Any duplicate world cast generated while a Stage 05 screen is open is a blocking regression.

---

## 12. Rebindability and Controlling

05.09 does not add global key mappings for focus traversal.

Therefore:

- current Black Arcana global mappings remain registered through vanilla `KeyMapping`;
- Controlling continues to discover those mappings naturally;
- keyboard navigation inside `Screen` uses screen-local controls rather than polluting the global key list;
- absence of Controlling does not affect screen navigation;
- no other mod's key mapping is rewritten.

If implementation later adds a new global action, 05.06 key-conflict rules apply first.

---

## 13. Controller boundary

No general controller framework is currently confirmed in the physical modlist.

Therefore controller implementation remains optional/provider-dependent.

05.09 still defines a useful future boundary: a verified controller integration should map directional/focus/activate/cancel actions onto the same **screen navigation operations**, not create controller-specific gameplay logic.

A future provider may map:

- move focus;
- change page;
- activate focused entry;
- cancel/close.

But:

- exact provider/version/API must be verified first;
- keyboard/mouse remains fully functional without the provider;
- activation must reuse existing radial selection/loadout draft operations;
- no provider button sends an authoritative cast result from the client.

---

## 14. Accessibility requirements

Keyboard-only navigation is an accessibility feature, but it must not create a second semantic mode.

Requirements:

- focused state has a visible non-color-only cue;
- focus order is deterministic;
- the player can identify which item will activate before activation;
- no pointer precision is required to select a radial wedge;
- no pointer precision is required to toggle a loadout entry;
- closing/cancelling is always available;
- selection and activation remain distinct where the existing surface defines them as distinct;
- important hazard/denial information remains available when keyboard modality is active;
- focus cues remain readable at the Stage 05 small-viewport matrix.

Reduced motion/flashes must apply to any future animated focus treatment.

---

## 15. Localization and labels

Keyboard navigation should not require embedding English key names into immutable strings.

Any future player-facing navigation hint should:

- use translation keys;
- use Minecraft-supported key-label components where appropriate instead of hardcoded English names;
- remain optional/compact on small viewports;
- not require displaying every possible action simultaneously;
- preserve semantic action wording after rebinding global keys.

Screen-local controls such as Tab/Space/Enter may be documented through translatable hints, but the final implementation should use actual localized key names where the API supports that safely.

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
| keyboard focus + danger | orthogonal composition | danger styling only for non-`NORMAL` tier under 05.08 |
| keyboard focus + forecast block | orthogonal composition | focus does not cause block |
| focus with missing icon | `FOCUSED + PRESENTATION_FALLBACK` | spell remains valid |

No single focus border/color may be reused as an authoritative denial marker.

---

## 17. Performance boundaries

Keyboard focus state is tiny client-local state.

Implementation must not introduce:

- world scans;
- entity scans;
- chunk queries;
- server requests on every focus move;
- per-tick full state synchronization;
- provider API calls merely to move focus;
- dynamic allocation proportional to world state.

Focus traversal operates on the already-snapshotted bounded radial/loadout lists.

Radial maximum visible entries remain eight per page.

Loadout editor remains bounded by synchronized spell presentation limits and viewport pagination.

---

## 18. Planned implementation architecture

This section describes planning shape, not required class names.

Prefer a small deterministic client-only focus/navigation state helper rather than embedding unrelated key rules throughout render code.

Conceptual responsibilities:

- current focused canonical index;
- active input modality;
- next/previous focus traversal;
- page transition reconciliation;
- focus initialization;
- invalid/empty-state clamping.

Surface code remains responsible for:

- rendering;
- geometry;
- invoking the existing draft/selection operation when activation occurs.

Do not put casting, cost, cooldown, hazard or provider authority into the focus helper.

---

## 19. TDD plan for future implementation

When 05.09 implementation is approved, start with pure deterministic tests.

### 19.1 Radial RED tests

Add failing tests for:

- focus initializes to selected visible slot;
- empty loadout creates no focus;
- Tab advances through current-page canonical slots;
- Shift+Tab moves backward;
- traversal wraps or clamps according to the final implementation decision, documented before GREEN;
- Page Up/Page Down move to valid destination-page focus;
- focus never points outside current visible slots;
- activate focused wedge invokes selection semantics only;
- close without activate preserves prior selected slot;
- `TOGGLE` close key does not select focused wedge;
- `HOLD` release does not select focused wedge;
- pointer modality and keyboard modality are distinguishable.

### 19.2 Loadout RED tests

Add failing tests for:

- focus initializes to a valid row;
- Up/Down stay bounded;
- page movement preserves/clamps relative focus;
- Space toggles only focused draft entry;
- Enter still means apply rather than row toggle;
- Delete/Backspace preserve current clear-all draft contract;
- focus survives local draft toggle/clear because available list is unchanged;
- empty list is safe;
- close without apply leaves server update unsent.

### 19.3 Integration regression tests

Where technically representable:

- a Black Arcana `Screen` owning focus suppresses direct cast processing;
- one keyboard activation causes one local draft/selection operation;
- no network cast packet is generated merely by focus movement.

---

## 20. Real-client validation plan

Automated focus tests are insufficient for physical input acceptance.

After implementation, directly test:

### Radial

- mouse-only selection still works;
- keyboard-only focus traversal;
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

---

## 21. Acceptance failures that block implementation merge

A 05.09 implementation must not merge with:

- keyboard focus causing a cast;
- focus movement changing server loadout;
- keyboard activation using a second cast path;
- radial close implicitly selecting a different spell;
- page movement producing invalid/off-page focus;
- Enter unexpectedly changing from apply semantics without an explicit reviewed UX migration;
- screen navigation leaking through to world casting;
- stuck key/cursor state;
- focus invisible except by color;
- keyboard navigation breaking current mouse behavior;
- mandatory dependence on Controlling or a controller provider.

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

05.09 is a planning refinement and does not automatically reopen Stage 05 completion requirements.

Current state remains:

`IMPLEMENTED / FINAL VALIDATION DEFERRED`

Keyboard-only radial/loadout operation becomes a required Stage 05 fix only when:

- the current manual/accessibility acceptance criteria explicitly require it; or
- a directly observed accessibility/usability failure is promoted to blocking; or
- an explicit reviewed decision promotes 05.09 to required hardening.

Otherwise implementation may remain an approved follow-up or Stage 09 carry.

The current manual matrix remains the authority for actual closeout PASS/BLOCKED status.

---

## 24. Non-goals

This plan does not authorize:

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
- declaring keyboard accessibility validated from this planning document.

---

## 25. Exit criteria for this planning task

05.09 is planning-complete when:

- current mouse/keyboard behavior is recorded accurately;
- radial keyboard focus has deterministic initialization/navigation/activation semantics;
- loadout keyboard focus has deterministic row/page/toggle/apply semantics;
- existing Left/Right/PageUp/PageDown and Enter/Delete behavior is preserved unless separately reviewed;
- focus, hover, selection and draft membership remain semantically distinct under 05.08;
- no new global default mapping is required;
- no focus action grants gameplay authority;
- controller support remains optional/provider-dependent;
- stale/resize/session focus behavior is defined;
- performance remains bounded/client-local;
- TDD and real-client validation requirements are explicit;
- Stage 05 validation state remains unchanged;
- no Java/runtime/network/provider implementation is included in this planning change.
