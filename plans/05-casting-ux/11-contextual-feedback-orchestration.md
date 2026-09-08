# 05.11 — Contextual Feedback Orchestration

## State

`PLANNING / NO RUNTIME CHANGE / EVENT-ARBITRATION HARDENING`

This document defines the canonical Stage 05 plan for arbitrating transient selection, forecast and authoritative cast-result feedback across Black Arcana's contextual HUD.

Baseline used to author this plan: `main@52706b448a8153502885784c435a25aaf8352a12`.

This is a planning artifact only. It does **not** add Java runtime behavior, packets, queues, timers, HUD widgets, protocol fields, client config or provider integrations.

---

## 1. Why this plan exists

`03-contextual-hud.md` defines what the HUD may display and its information hierarchy, but the current runtime has multiple independently timed event sources that can overlap:

- selected-spell presentation;
- selection-time static danger metadata;
- dynamic resistance/gate forecast;
- authoritative cast result;
- future cooldown/charge/channel/timer presentation after 05.07 authorizes those contracts.

The current implementation is intentionally small, but its event arbitration is implicit in render code rather than frozen as a reusable contract.

05.11 makes that arbitration explicit so future HUD refinements do not create:

- stale feedback;
- misleading spell/result association;
- duplicate spam;
- unbounded event queues;
- forecast/result semantic collapse;
- client-side gameplay authority.

---

## 2. Current verified runtime behavior

### 2.1 Selection event clock

`ClientUxState` currently stores only:

- `selectionChangedTick`.

`ClientInputController.castSlot(...)` marks selection changed before sending cast intent.

Mouse selection through `BlackArcanaRadialScreen` also marks selection changed.

Therefore the current selection clock means approximately:

`the client recently selected a slot or emitted a cast intent through castSlot`

It is not an authoritative cast timestamp.

### 2.2 Result event clock

`ClientArcanaSyncState.acceptResult(...)` stores:

- exactly one latest `CastResultPayload`;
- the local player tick at which that result was received.

A newer accepted result replaces the previous cached result.

The current result cache is therefore **latest-received-result wins**, not an event history.

### 2.3 Result identity limitation

`CastResultPayload` currently contains:

- protocol version;
- `castId`;
- authoritative status;
- authoritative bounded code;
- authoritative bounded detail.

It does **not** contain:

- `spellId`;
- loadout slot;
- server-authored spell display identity.

The client currently does not maintain a bounded pending-cast presentation map keyed by `castId`.

Therefore the current HUD cannot prove which spell identity belongs beside a received result merely from `CastResultPayload`.

### 2.4 Current HUD composition

`BlackArcanaHudLayer` currently computes two independent windows:

- selection recent → `SELECTION_DURATION_TICKS`, default 60;
- result recent → `FEEDBACK_DURATION_TICKS`, default 80.

Current feedback levels:

- `MINIMAL`: only recent denials;
- `STANDARD`: selected spell/context plus denial where applicable;
- `VERBOSE`: STANDARD plus success feedback.

When level is not `MINIMAL`, the current renderer may add the **current selected spell line whenever either selection or result keeps the panel alive**.

Hazard/gate lines are restricted to the recent-selection window.

### 2.5 Current possible association mismatch

Because a result has `castId` but no spell identity, and the selected-spell line is resolved from the **current** client selection, this sequence is possible:

1. cast Spell A;
2. before Spell A result is received, change selection to Spell B;
3. Spell A result arrives;
4. HUD renders current selected Spell B alongside Spell A's authoritative result.

The denial/result itself remains authoritative, but the visual juxtaposition can imply a relationship the current protocol does not prove.

This is a presentation correctness gap, not a server-authority failure.

### 2.6 Forecast request behavior

`HazardResistanceForecastClientController` requests a forecast only when:

- contextual HUD is enabled;
- feedback level is not `MINIMAL`;
- selection is still recent;
- a selected spell exists;
- the selected spell has non-`NORMAL` danger metadata.

Request refresh interval is currently 20 client ticks.

The controller requests immediately for a changed selected spell or when refresh is due.

### 2.7 Forecast stale protection

`HazardResistanceForecastPayload` includes:

- `requestId`;
- `spellId`;
- resistance status/data;
- gate-forecast availability/status.

`ClientArcanaSyncState`:

- rejects an older request id than the currently cached forecast;
- exposes a forecast only for matching `spellId`;
- clears the dynamic forecast when static hazard preflight is replaced.

`BlackArcanaHudLayer` additionally requires forecast tier/minimum/recommended metadata to match current static preflight before rendering it.

This is the current strongest correlation/staleness model in Stage 05 and should remain the reference for future bounded request/response presentation.

---

## 3. Authority model

05.11 never changes gameplay authority.

### Authoritative sources

- `CastResultPayload.status/code/detail` → server-authored result for the referenced cast id;
- hazard/gate forecast → server-authored bounded projection for its request/spell;
- static hazard preflight → synchronized server-authored spell metadata;
- future cooldown/charge/channel/timer state → authoritative only after 05.07 approves its server-authored contract.

### Client presentation sources

- current selected slot;
- selection-change tick;
- local receive tick for a result;
- optional future bounded pending-cast presentation context keyed by a client-generated cast id;
- visual lifetime, layout and feedback-level preferences.

Client presentation context may identify **what the client attempted**, but it never proves the server accepted that identity or cast legality.

---

## 4. Feedback channels

Stage 05 should reason about transient feedback as independent bounded channels rather than one ambiguous HUD state.

### Channel A — Selection context

Contains presentation such as:

- current selected spell identity;
- current static danger data;
- matching dynamic hazard/gate forecast.

Lifetime is controlled by selection duration.

### Channel B — Authoritative cast result

Contains:

- latest received authoritative result status/code/detail;
- optional safely correlated presentation identity if available under Section 8.

Lifetime is controlled by feedback duration.

### Channel C — Future temporal gameplay presentation

Potential future data:

- cooldown;
- charges;
- channel state;
- ritual/domain timers.

This channel does not exist generically today and remains gated by 05.07.

### Channel D — Editor/navigation state

Loadout editor state and keyboard focus belong to 05.09/05.10 and must not leak into combat HUD event arbitration.

---

## 5. Supersession rules

### 5.1 Selection

A newer selection event supersedes the previous selection-event timestamp/context.

Do not queue historical selections.

The HUD is not a selection history log.

### 5.2 Cast result

Default Stage 05 rule remains:

**latest received authoritative cast result supersedes the previous result.**

Do not add an unbounded result queue.

This preserves the current low-clutter model.

### 5.3 Forecast

A forecast is valid only for:

- its exact spell id;
- the newest accepted request id under the current client cache rules;
- matching current static preflight revision values.

A selection change may immediately make the old forecast irrelevant even if its payload remains temporarily cached.

### 5.4 Future temporal state

Each future 05.07-authorized state family must define its own identity/revision/supersession key.

Do not reuse selection timestamps as a substitute for server lifecycle identity.

---

## 6. Cross-channel priority

Priority determines what is emphasized when multiple channels are simultaneously recent. It does **not** change which event remains cached.

Canonical priority:

1. **authoritative denial**;
2. authoritative success, when feedback level permits it;
3. current hard-block/warning forecast for the current selected spell;
4. current selected-spell identity/context;
5. lower-value explanatory detail.

Reasons:

- denial is the most actionable result of an actual cast request;
- authoritative result must not be visually demoted beneath a predictive forecast;
- forecast remains useful context but is not an executed-cast result;
- selected identity is context rather than outcome.

The physical line order may remain compact and need not map literally to one vertical ordering, but semantic emphasis must follow this priority.

---

## 7. No false result-to-selection association

This is the central 05.11 correctness rule.

A received cast result must **not** be visually attributed to the current selected spell unless that relationship is safely established.

### Current protocol-safe baseline

Without additional correlation state or protocol fields:

- denial/success result may render as a standalone authoritative result;
- current selection may render as separate selection context when its own selection window is recent;
- the HUD must not format those two facts as one sentence/card that claims the selected spell produced that result.

### Important consequence

A `resultRecent` event by itself must not force a current selected-spell identity line merely to provide a label for the result.

If the current selection is not independently recent, the safe no-correlation presentation is the result alone.

This is a planned hardening rule; it is not a claim that current runtime already behaves this way.

---

## 8. Optional bounded cast-result presentation correlation

A future no-protocol hardening may correlate a server result with the client intent using the echoed `castId`.

### 8.1 Allowed presentation context

When `ClientInputController` emits a cast intent, a bounded client-only pending presentation record may remember:

- `castId`;
- attempted `spellId`;
- attempted loadout slot;
- local send tick.

The server result already echoes `castId`.

### 8.2 Meaning

Such correlation means only:

`the authoritative result corresponds to this locally recorded attempted cast id`

It does not make the locally remembered spell/slot authoritative gameplay data.

### 8.3 Safety rules

- bound the pending record count;
- expire old records by bounded age;
- one cast id maps to at most one pending presentation context;
- consume/remove the matching record when result arrives;
- unknown result cast id → render result without inferred spell identity;
- duplicate/replayed result id → do not recreate stale presentation context;
- disconnect/session change → clear all pending presentation context;
- no server validation reads this table;
- no retry/cast packet is generated from this table.

### 8.4 Better future protocol option

If product requirements demand fully server-authored result identity, a future bounded result schema may include server-confirmed spell/slot context.

That is a protocol design task, not authorized by 05.11 itself.

Do not add fields merely because a client-only correlation table is aesthetically inconvenient.

---

## 9. Feedback-level arbitration

### `MINIMAL`

Show only recent authoritative denials.

Rules:

- no selection panel;
- no success message;
- no hazard/gate forecast request solely for HUD presentation;
- denial remains authoritative standalone feedback;
- no attempt to label the denial with current selection without safe correlation.

### `STANDARD`

May show:

- recent selection context;
- hazard/gate context for the current selected dangerous spell;
- recent authoritative denial.

Routine success remains suppressed.

### `VERBOSE`

May additionally show latest recent authoritative success.

Verbose does not authorize:

- queues of old results;
- duplicated server detail;
- client-generated success reasons;
- extra provider economics.

---

## 10. Timing semantics

### 10.1 Selection duration

`SELECTION_DURATION_TICKS` controls the selection-context channel.

Default current value: 60 ticks.

A value of zero disables the selection-context visibility window under current `HudLayout.isRecent` semantics.

### 10.2 Feedback duration

`FEEDBACK_DURATION_TICKS` controls the authoritative-result channel.

Default current value: 80 ticks.

A value of zero disables result visibility under current semantics.

### 10.3 Clock source

Current event windows are based on local player ticks.

For results, the timestamp is the client receipt tick, not a server execution timestamp.

05.11 preserves that as presentation timing unless a future protocol explicitly exposes an authoritative event-time need.

### 10.4 No pause/extension while another screen is open

Current HUD rendering returns while another `Screen` is open, but local tick windows continue to age.

Default planning rule:

- hiding the HUD behind another screen does not pause or extend transient feedback timers;
- closing the screen does not replay already expired feedback.

This keeps feedback windows simple and avoids storing a deferred message queue.

---

## 11. Forecast request lifecycle

Current 20-tick refresh is a bounded implementation fact, not a magic gameplay tick rate.

Preserve these principles:

- requests occur outside HUD render;
- requests occur only while the relevant selection context can be displayed;
- `MINIMAL` suppresses forecast traffic needed only for hidden HUD context;
- `NORMAL` danger tier suppresses dynamic resistance/gate forecast requests;
- changed spell may request immediately;
- same spell refresh remains rate-limited;
- no per-frame request;
- forecast response is presentation-only and never reserves cost/cooldown/resources.

A future tuning change to the refresh interval requires performance/usability evidence; it does not change spell legality.

---

## 12. Selection changes during pending result

Canonical behavior must remain semantically safe.

Sequence:

1. Cast A sent;
2. Selection changes to B;
3. Result A arrives.

Required outcome:

- Result A is displayed as the latest authoritative result according to feedback level;
- Selection B may display only as independently recent selection context;
- Result A must not be labeled as B's result;
- B's forecast remains scoped to B;
- A's result must not cause a new forecast for A;
- no automatic reselection of A occurs.

If Section 8 correlation exists, Result A may display an attempted-spell identity for A while selection context separately remains B.

---

## 13. Multiple rapid cast results

Current cache stores only one latest result.

05.11 freezes **latest-received-result wins** as the first implementation contract.

Example:

- Result A denial received;
- Result B success received later;
- result channel now represents B.

At `STANDARD`, success B may be visually suppressed, so the old denial A does not remain artificially pinned as if it were still the latest result.

This avoids misleading history retention.

If later usability testing demonstrates that rapid denials are being lost unacceptably, any message-history solution must be:

- explicitly designed;
- bounded in count and lifetime;
- correlated by cast id;
- visually ordered;
- non-authoritative beyond the server results it stores.

No queue is approved by this plan today.

---

## 14. Duplicate and replay presentation handling

Server replay protection belongs to the canonical cast pipeline, not the HUD.

Client presentation still needs bounded behavior if duplicate result packets are observed.

Planned rule:

- repeated delivery of the same `castId` should not extend feedback forever through repeated timestamp refreshes if a dedup layer is introduced;
- client may remember a bounded set of recently rendered cast ids for presentation dedup only;
- absence of a presentation dedup cache does not authorize modifying server replay semantics;
- never suppress a genuinely distinct cast merely because status/code/detail happen to match.

Dedup identity is `castId`, not message text.

---

## 15. Forecast versus authoritative denial

A predictive gate forecast and a cast result can legitimately disagree because later gates or world state can change.

Required semantics:

- forecast `CLEAR` is not success;
- forecast `COOLDOWN/COST/...` is not itself a cast result;
- authoritative denial wins outcome emphasis when both are visible;
- do not rewrite a prior forecast line to look like it authored the denial;
- a successful result does not retroactively prove that every prior forecast category was exhaustive.

This preserves 05.08's `FORECAST_*` versus `RESULT_*` distinction.

---

## 16. Hazard warning versus denial

Hazard/resistance presentation is spell-risk context.

Rules:

- below-recommended warning remains warning;
- below-minimum presentation may correspond to a predictable block, but the actual cast denial line still comes from the server result;
- `RECOMMENDED` never means universally safe;
- a normal-tier profile does not activate danger styling;
- a denial from an unrelated gate must not be described as hazard denial unless the server result says so.

---

## 17. Config changes while events are recent

Client config is presentation-only.

### HUD disabled

Disabling contextual HUD suppresses rendering.

It must not clear authoritative synchronized gameplay snapshots merely to hide UI.

### Re-enable

Current runtime may render an event again if it is still within its original tick window.

This behavior is acceptable as baseline because the timer was not paused or reset.

If future UX decides that re-enable should not replay still-recent events, implement a presentation-local visibility epoch/latch rather than clearing shared synchronized gameplay caches.

### Feedback level change

Changing feedback level changes what the current valid channels are allowed to render.

It must not mutate server results, forecasts or loadout state.

---

## 18. Session and lifecycle reset

On client player/connection absence, existing code clears:

- `ClientArcanaSyncState`;
- `ClientUxState`.

Any future 05.11 presentation state must clear at the same session boundary, including:

- pending cast-id presentation correlation;
- presentation dedup ids;
- local orchestration latches.

No previous-session result or pending context may appear after reconnect.

---

## 19. Interaction with future 05.07 temporal data

When cooldown/charge/channel/timer contracts are eventually implemented, they should not be shoved into the transient result channel.

Each state has different lifetime semantics:

- cast result → transient event;
- cooldown → server-owned temporal state;
- charges → server-owned pool state;
- channel → active session lifecycle;
- ritual/domain timer → owner-specific active-state lifetime.

05.11 may arbitrate emphasis between them, but 05.07 remains authority for whether the data may exist on the client at all.

Do not model a channel session as repeated success/result events.

---

## 20. Anti-spam and boundedness rules

The first implementation remains intentionally small:

- one current selection context;
- one latest authoritative result;
- one current selected-spell forecast cache;
- no general message queue;
- no unbounded pending-cast table;
- no per-frame networking;
- no world/entity scans.

If pending cast correlation is implemented, its bound and expiry must be explicit before GREEN.

If message history is ever implemented, its count/lifetime must be explicit before GREEN.

---

## 21. Planned implementation architecture

This section describes responsibilities, not required class names.

Prefer a small deterministic presentation-orchestration helper/state model rather than adding more ad hoc conditions inside render code.

Conceptual responsibilities:

- decide which channels are recent;
- apply feedback-level filtering;
- determine safe result identity correlation;
- order/emphasize simultaneous channels;
- enforce latest-result supersession;
- reject stale/mismatched forecast context;
- clear presentation-only state on session reset.

The helper must not:

- validate a cast;
- compute provider costs;
- decide cooldown legality;
- resolve targets;
- mutate loadout;
- send server state merely because render changed.

`BlackArcanaHudLayer` remains a renderer of already-classified presentation state.

---

## 22. TDD plan for future implementation

### 22.1 Event-window RED tests

Test:

- selection-only recent;
- result-only recent;
- both recent;
- both expired;
- selection duration zero;
- feedback duration zero;
- local time before event tick fails safely.

### 22.2 Feedback-level RED tests

Test:

- MINIMAL + denial → denial visible;
- MINIMAL + success → no feedback;
- STANDARD + recent selection → selection context;
- STANDARD + result-only denial → denial without falsely forced current-spell attribution;
- STANDARD + result-only success → no result line;
- VERBOSE + result-only success → success result;
- feedback level never changes underlying cached authoritative data.

### 22.3 Result/selection mismatch RED test

Explicit regression:

- send/record Cast A context;
- change current selection to B;
- receive Result A;
- orchestration must not identify Result A as B.

If no correlation helper exists, result renders without spell attribution.

If Section 8 correlation is implemented, result identity resolves to attempted A and remains distinct from current selection B.

### 22.4 Latest-result RED tests

Test:

- A received then B → B supersedes A;
- identical text but distinct cast ids remain distinct results;
- duplicate same cast id does not create an unbounded history if dedup is implemented.

### 22.5 Forecast RED tests

Test:

- selected spell mismatch suppresses cached forecast;
- older request id cannot replace newer cached forecast;
- static preflight mismatch suppresses forecast;
- `NORMAL` tier suppresses dynamic danger context;
- MINIMAL mode generates no forecast demand;
- result arrival does not retarget forecast to the result's spell.

### 22.6 Session RED tests

Test that session reset clears all future orchestration-only correlation/dedup state.

---

## 23. Real-client validation plan

After an implementation is approved, test at least:

### Normal single cast

- select A;
- cast A;
- observe selection context then authoritative result;
- verify result does not appear before server reply.

### Selection race

- cast A;
- switch to B before reply;
- verify no visual claim that Result A belongs to B.

### Rapid casting

- emit multiple legal/denied attempts within feedback duration;
- verify latest received result semantics;
- verify no stale denial remains pinned after a later result supersedes it;
- verify no unbounded stacking/spam.

### Feedback levels

Repeat representative success/denial paths in:

- MINIMAL;
- STANDARD;
- VERBOSE.

### Dangerous spell

- current non-`NORMAL` spell selection;
- forecast refresh;
- selection switch;
- stale old-spell forecast must not display;
- cast denial must remain outcome-distinct from forecast.

### Screen suppression

Open another screen during a live feedback window:

- HUD hides;
- timers continue aging;
- expired message does not replay after close;
- no world cast leaks through GUI focus.

### Modpack coexistence

Repeat representative feedback with Spell Actionbar and Epic Fight conditions already covered by 05.06.

---

## 24. Acceptance failures that block implementation merge

A 05.11 implementation must not merge with:

- result for Cast A visually attributed to currently selected Spell B without safe correlation;
- forecast presented as authoritative executed-cast result;
- current selected spell forced as result identity merely because a result is recent;
- denial reason invented client-side;
- stale forecast overriding current selected/preflight state;
- result event retargeting hazard forecast to an unrelated spell;
- unbounded result/pending-context queue;
- feedback timer extended indefinitely by duplicate packet presentation;
- HUD config changes mutating gameplay state;
- reconnect replaying previous-session results;
- screen suppression leaking a cast;
- provider resource/cooldown calculations introduced in orchestration code.

---

## 25. Relationship to Stage 05 completion

05.11 is a planning refinement.

Creating or merging this plan does not change:

`IMPLEMENTED / FINAL VALIDATION DEFERRED`

A feedback-orchestration hardening becomes a required Stage 05 blocker only when:

- an existing mandatory manual row exposes a real misleading/stale feedback defect; or
- an explicit reviewed decision promotes a specific 05.11 rule to required hardening.

The current runtime remains implemented; this plan documents correctness requirements for future refinement.

---

## 26. Implementation sequencing

If 05.11 implementation is approved:

### Phase A — semantic hardening with current protocol

1. extract/test deterministic channel arbitration;
2. stop forcing current selected-spell identity into result-only presentation;
3. preserve latest-result semantics;
4. preserve current bounded forecast behavior;
5. validate feedback levels/timing/session reset.

### Phase B — optional client-only correlation

6. bounded pending cast-id presentation context;
7. result correlation by echoed cast id;
8. bounded duplicate-result presentation handling if real evidence requires it.

### Phase C — only if product requirements require server-authored result identity/history

9. design a bounded protocol extension;
10. version/correlate it explicitly;
11. revalidate all Stage 05 networking/dedup semantics.

Do not jump to Phase C to solve a problem Phase A can solve safely.

---

## 27. Non-goals

This plan does not authorize:

- changing server cast order/gates;
- client-authoritative cast results;
- changing replay protection;
- an unbounded notification history;
- permanent combat log UI;
- automatic retry of failed casts;
- automatic reselection of a result's spell;
- retargeting current selection from a result;
- provider cost/cooldown recomputation;
- per-frame/per-tick full-state packets;
- client-side hazard admission;
- mandatory protocol extension;
- implementation of Java/network/HUD changes in this planning PR.

---

## 28. Exit criteria for this planning task

05.11 is planning-complete when:

- current selection/result/forecast clocks are recorded accurately;
- current latest-result cache semantics are explicit;
- the result spell-identity limitation is explicit;
- result/current-selection false association is prohibited;
- selection, result and forecast channels have explicit lifetimes and supersession rules;
- cross-channel priority is defined;
- feedback-level behavior is defined;
- forecast request/staleness rules are preserved;
- rapid-result behavior is deterministic without an unbounded queue;
- pending cast correlation is optional, bounded and presentation-only;
- session reset behavior is explicit;
- future 05.07 temporal state is kept distinct from transient result events;
- TDD and real-client validation cover race/overlap cases;
- Stage 05 completion state remains unchanged;
- no runtime/network/provider implementation is included in this planning change.
