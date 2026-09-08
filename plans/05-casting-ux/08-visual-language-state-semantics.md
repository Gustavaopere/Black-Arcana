# 05.08 — Visual Language & State Semantics

## State

`PLANNING / NO RUNTIME CHANGE / CROSS-SURFACE UX SEMANTICS`

This document defines the canonical visual-language and state-semantics plan for Black Arcana Casting & UX.

Baseline used to author this plan: `main@019eb1723b7a70b9fd888ce44d1eb9b85dfa7b13`.

Environment authority at this checkpoint:

- Minecraft `1.21.1`;
- NeoForge `21.1.248` from the current physical modlist;
- Java `21`;
- Iron's Spells 'n Spellbooks `1.21.1-3.16.3` is present as an external spell/resource/UI provider;
- Spell Actionbar `1.1.4` is present as an external action-bar surface;
- Epic Fight `21.17.3.1` and `efiscompat 3.1.0` are present as combat/animation environment;
- Controlling `19.0.5` is present for keybinding discovery;
- no top-level general controller framework is currently confirmed.

Presence/version is coexistence context only. It does not create a provider API or transfer visual/gameplay authority.

This plan is deliberately presentation-focused. It does **not** add Java classes, packets, registries, assets, shaders, animations, sounds, controller hooks or provider integrations.

---

## 1. Why this plan exists

Stage 05 already has separate detailed plans for:

- input/loadouts;
- radial selection;
- contextual HUD;
- accessibility/client config;
- real-client closeout;
- current-modpack coexistence;
- server-authored presentation-data contracts.

Those plans correctly describe their own surfaces, but several state concepts appear in more than one place:

- selected;
- hovered/focused;
- unavailable;
- blocked;
- cooldown;
- danger/warning;
- authoritative denial;
- forecast;
- missing presentation data;
- missing artwork.

Without one cross-surface semantic contract, the same gameplay fact can drift into different meanings across the loadout editor, radial, HUD and future invocation surfaces. A red-looking radial slot, a disabled editor row and a HUD warning could accidentally describe three different facts while appearing equivalent to the player.

05.08 prevents that drift.

The objective is not to freeze a final art style. The objective is to freeze **meaning** before later art polish.

---

## 2. Relationship to the other Stage 05 plans

This document does not replace the existing subplans.

- `01-input-loadouts.md` remains authority for loadout/input lifecycle and server-owned loadout semantics.
- `02-radial-wheel.md` remains authority for radial geometry, paging and selection interaction.
- `03-contextual-hud.md` remains authority for HUD lifecycle, density and feedback timing.
- `04-accessibility-client-config.md` remains authority for client-only preferences and accessibility behavior.
- `05-final-client-validation-handoff.md` remains authority for real-client acceptance and evidence.
- `06-modpack-coexistence.md` remains authority for overlap/deduplication with installed casting/combat/keybinding surfaces.
- `07-presentation-data-contracts.md` remains authority for whether a datum is currently safe to render at all.

05.08 sits **after** those authority decisions and answers a narrower question:

> Once a piece of state is legitimately available for presentation, what semantic role does it have and how must that role stay consistent across Stage 05 surfaces?

A visual design never upgrades unavailable data into available data. If 05.07 says a datum is blocked on a server-authored contract, 05.08 cannot bypass that gate.

---

## 3. Non-negotiable authority rules

The visual layer must preserve `plans/DECISIONS.md`, especially D004, D005, D006, D018, D019, D020, D023, D024, D029 and D031.

Therefore:

1. **Visual state is never gameplay authority.**
   A cue can represent a server-authored fact, forecast or presentation interpolation, but it cannot grant cast legality.

2. **Selection is not casting.**
   Selection/focus styling may never look like an executed spell result.

3. **Forecast is not final admission.**
   `CLEAR` or equivalent forecast language may not visually imply guaranteed cast success.

4. **Provider ownership remains provider-specific.**
   Black Arcana does not recolor or mirror unrelated Iron's/Ars/provider mana/cooldown state as though it were Black Arcana state.

5. **Missing data fails visually closed.**
   Unknown/unmapped state is omitted or marked unavailable; it is never guessed.

6. **No permanent second resource language.**
   The visual identity of Black Arcana must not imply that Black Arcana has a universal permanent mana pool when D004 says it does not.

7. **No client-side target truth.**
   Reticles, outlines or previews must not imply server target legality unless an explicit bounded contract exists for the exact fact shown.

8. **Presentation degradation may not affect gameplay.**
   Missing icons, translations, animations, particles, sound or configuration must never invalidate a spell or mutate server state.

---

## 4. Semantic model: orthogonal state families

Stage 05 must not collapse every visual condition into one `GOOD/BAD` color.

The player-facing state model is separated into independent families.

### 4.1 Identity / focus state

Describes **what the player is interacting with**, not whether a cast is legal.

Conceptual states:

- `SELECTED` — current client-selected canonical loadout slot;
- `FOCUSED` — current keyboard focus or equivalent navigation focus;
- `HOVERED` — pointer emphasis only;
- `IN_LOADOUT` — accepted synchronized membership/position where relevant;
- `DRAFT_ONLY` — client editor draft state that has not been accepted by the server.

These are interaction/presentation states. They must never imply cooldown, affordability, progression or target legality.

### 4.2 Admission / gate state

Describes a bounded server-authored forecast or authoritative result.

Conceptual states:

- `FORECAST_CLEAR` — no predictable gate in the current bounded forecast is blocking;
- `FORECAST_BLOCKED` — a bounded predictable server gate currently reports a blocking category;
- `FORECAST_UNAVAILABLE` — the forecast cannot currently be trusted/provided;
- `CAST_DENIED` — the actual server cast request was denied;
- `CAST_SUCCEEDED` — the actual server cast request succeeded where success feedback is enabled.

`FORECAST_CLEAR` must not be visually synonymous with `CAST_SUCCEEDED`.

### 4.3 Temporal readiness state

Describes server-owned cooldown/charge/channel/timer state only where 05.07 permits it.

Potential states include:

- `COOLDOWN_ACTIVE`;
- `CHARGES_AVAILABLE / CHARGES_EMPTY`;
- `CHANNEL_ACCEPTED / CHANNEL_PROGRESS / CHANNEL_CANCELLED`;
- `OWNED_TIMER_ACTIVE`.

At the current baseline, generic per-spell cooldown presentation is still blocked on authoritative spell→cooldown-group mapping, and generic charge/channel/timer presentation is blocked on corresponding bounded server contracts.

Therefore these conceptual states are part of the visual grammar **without being claims that the current client can render them today**.

### 4.4 Hazard / risk state

Describes Black Arcana danger semantics.

Conceptual roles:

- `DANGER_PRESENT` — the selected spell has synchronized **non-`NORMAL`** danger tier metadata; mere presence of a synchronized `NORMAL` profile does not activate danger styling;
- `BELOW_MINIMUM` — server-authored hazard presentation says the relevant minimum threshold is not met;
- `BELOW_RECOMMENDED` — warning state; not guaranteed failure;
- `RECOMMENDATION_MET` — recommendation is met; never equivalent to “safe”;
- `HAZARD_FORECAST_UNAVAILABLE` — dynamic resistance forecast is unavailable/stale while static metadata may still be valid.

Danger styling must not imply that meeting a recommendation removes Backlash/Corruption risk. A synchronized `NORMAL` profile remains ordinary presentation state and must not be promoted to `DANGER_PRESENT` merely because hazard metadata exists.

### 4.5 Presentation confidence state

Describes **how strongly the client knows the shown fact**.

The confidence ladder is inherited from 05.07:

1. `AUTHORITATIVE_CURRENT_FACT` — synchronized/server-authored current state or cast result;
2. `SERVER_AUTHORED_FORECAST` — bounded projection that may become stale;
3. `CLIENT_INTERPOLATION` — visual animation between known server facts only;
4. `UNAVAILABLE` — no supported value exists for this surface;
5. `PRESENTATION_FALLBACK` — art/translation fallback only, unrelated to gameplay validity.

Confidence should influence wording and ornamentation, not gameplay.

### 4.6 Presentation-integrity state

Describes failure of presentation assets, not failure of the spell.

Examples:

- missing icon;
- missing translation;
- unsupported optional provider icon/theme data;
- unresolved optional visual resource.

Required response:

- preserve canonical spell identity;
- fall back to text/canonical id as needed;
- do not mark the spell blocked;
- do not emit a cast denial;
- do not remove the spell from the accepted loadout.

---

## 5. Canonical semantic matrix

| Fact being represented | Semantic family | Allowed meaning | Must never mean |
|---|---|---|---|
| selected loadout slot | identity/focus | “this is the player's current selection” | “the spell is legal/ready” |
| pointer hover | identity/focus | “the pointer is over this entry” | “selected” or “cast” |
| editor draft membership | identity/focus | “local unsaved draft contains this spell” | “server accepted this loadout” |
| accepted loadout snapshot | identity/focus + authoritative fact | “server synchronized this loadout” | “all entries can cast right now” |
| `CLEAR` gate forecast | admission forecast | “no predictable projected gate currently blocks” | “cast guaranteed to succeed” |
| blocked gate forecast | admission forecast | “this bounded predicted category currently blocks” | “the final cast request already happened” |
| cast denial | authoritative result | “server denied this exact request” | “generic long-lived spell status” |
| cast success | authoritative result | “server reported success for this request” | “future casts are ready” |
| non-`NORMAL` static danger tier | hazard | “spell has synchronized danger metadata whose tier is non-normal” | “player will definitely Backlash” |
| `NORMAL` static danger tier | ordinary/static metadata | “no danger styling is activated from tier alone” | `DANGER_PRESENT` |
| below recommended resistance | hazard warning | “risk recommendation is not met” | “hard cast denial unless server says minimum blocks” |
| recommendation met | hazard information | “recommendation threshold is met” | “magic is safe/no corruption/backlash” |
| cooldown state, once mapped | temporal | “server-owned cooldown group has remaining time” | “client may authorize cast when visual timer reaches zero” |
| channel animation, once contracted | temporal + interpolation | “server accepted a channel session; local bar animates between server anchors” | “local key duration controls authority” |
| missing icon | presentation fallback | “art failed/unavailable; use fallback” | “spell unavailable” |
| provider preview unavailable | confidence/unavailable | “no supported exact preview exists” | guessed provider cost/resource value |

This matrix is semantic authority for all Stage 05 presentation work.

---

## 6. Composition and precedence

Orthogonal states may coexist. The system should not force one state to erase another unnecessarily.

Example: a spell can be simultaneously:

- selected;
- dangerous;
- below recommended resistance;
- on cooldown;
- hovered.

Those are different facts.

### 6.1 Priority for attention

When screen space is constrained, the attention order is:

1. **authoritative cast denial / direct blocking fact**;
2. **current blocking forecast or hard hazard minimum state**;
3. **server-owned temporal unavailability** once safely mapped;
4. **danger/risk warning**;
5. **selection/focus identity**;
6. **supplemental/decorative information**.

This priority is about what receives scarce visual space. It does not merge state ownership.

### 6.2 Event vs persistent state

- `CAST_DENIED` and `CAST_SUCCEEDED` are short-lived request-result events.
- `SELECTED`, accepted loadout membership and current **non-`NORMAL`** danger metadata are stateful presentation facts; a synchronized `NORMAL` profile does not create a danger state.
- Forecasts are stateful only while their stale-state identity remains valid.
- Cooldown/charge/channel/timer presentation, when implemented, follows owner-specific lifecycle rules from 05.07.

A short-lived denial must not permanently recolor the spell as unavailable after the event lifetime ends.

### 6.3 Unknown beats guess

If two signals cannot be reconciled safely, the visual outcome is `UNAVAILABLE/UNKNOWN`, not a guessed composite.

Examples:

- cooldown group exists but spell→group mapping is absent → omit generic per-spell cooldown;
- dynamic hazard forecast mismatches refreshed static profile → discard dynamic forecast;
- provider cost preview lacks exact supported contract → omit/mark unavailable;
- old channel session belongs to prior connection/session → clear it.

---

## 7. Visual vocabulary principles

05.08 intentionally does not freeze exact RGB/hex values, texture files, font files or final art assets.

It freezes qualitative rules.

### 7.1 Black Arcana identity

Casting UX should feel like one coherent Black Arcana system rather than a collage of provider UIs.

Direction:

- restrained, occult/forbidden-arcana framing;
- compact geometry rather than oversized fantasy panels;
- readable hierarchy before ornament;
- original project-owned symbols/shapes;
- contextual appearance rather than permanent visual occupation;
- visual intensity proportional to importance, not to how visually dramatic a spell is.

Do not copy the specific UI language, icons, textures, glyph art, sounds, models or animations of Mahou Tsukai, Iron's, Ars Nouveau or another provider unless a separately verified compatible license/permission explicitly allows reuse and provenance is recorded.

### 7.2 Semantic cues must be redundant

Important states should be represented by at least two channels where practical, for example:

- label/text;
- symbol/icon;
- outline/shape;
- fill/pattern;
- brightness/contrast;
- optional motion;
- optional sound.

Color alone is not enough.

### 7.3 Decorative intensity is subordinate
Decorative runes, glows, particles, pulsing borders or animated flourishes may reinforce identity, but they must not obscure:

- spell name;
- slot identity;
- denial reason;
- warning/block status;
- paging/focus affordances.

---

## 8. Conceptual icon/symbol vocabulary

The following names are **conceptual semantic tokens**, not existing resource IDs, Java enum constants or approved final assets.

A future asset pass may create original symbols for:

- selection/focus;
- blocked/denied;
- warning/danger;
- cooldown/time;
- unavailable/unknown;
- page/navigation;
- direct quick-cast-enabled slot;
- server-synchronized/accepted state where an explicit distinction is useful.

Rules:

- spell-specific icon remains the synchronized `iconId` where available;
- semantic status icons are separate from spell identity icons;
- one symbol must not mean both “warning” and “hard blocked”;
- missing semantic art falls back to text/outline rather than changing meaning;
- semantic symbols must remain legible at small GUI scales;
- all new project-owned assets require provenance tracking consistent with repository clean-room rules.

No provider logo or provider-owned spell icon may be repurposed as a generic Black Arcana state symbol without compatible permission.

---

## 9. Color and contrast policy

Exact palette values are deferred to an art implementation pass and real-client readability testing.

The semantic rules are:

- selected/focused styling must remain distinguishable from blocked/error styling;
- warning/danger must remain distinguishable from authoritative denial;
- unknown/unavailable should not look like success/ready;
- foreground text must preserve useful contrast over bright, dark and visually complex Minecraft scenes;
- important state needs a non-color cue;
- provider-owned colors are not automatically imported into Black Arcana semantics;
- one school/domain color may identify theme, but it must not replace state semantics.

A later high-contrast pass may tune backgrounds/outlines based on direct client observation. Static source review is not sufficient to claim readability.

---

## 10. Typography, wording and localization

### 10.1 Semantic wording

Use wording that preserves authority distinctions.

Preferred semantic distinctions:

- forecast: “No predictable gate blocks” rather than “Ready” when later gates can still fail;
- warning: “Below recommended” rather than “Unsafe” if the server contract only defines a recommendation;
- recommendation met: “Recommendation met” rather than “Safe”;
- unavailable preview: “Unavailable” rather than guessed zero/empty values;
- authoritative denial: actual bounded server-authored denial detail.

### 10.2 Translation rules

All new player-facing state labels should use translation keys.

Layout must tolerate:

- longer translations;
- missing translation fallback;
- non-English word order;
- different text widths.

Critical interaction geometry must not depend on English string width.

### 10.3 Truncation policy

When space is limited:

1. preserve the state-defining word/symbol;
2. preserve slot/spell identity where possible;
3. move explanatory detail to focused/center/HUD/tooltip surface;
4. truncate secondary descriptive text;
5. never truncate into a misleading opposite meaning.

---

## 11. Surface-specific semantic profiles

### 11.1 Loadout editor

Primary questions:

- which spells are in the current accepted loadout;
- what the unsaved draft contains;
- what slot each spell occupies;
- which slots 1–8 correspond to direct quick-cast mappings;
- whether an apply is still awaiting authoritative reconciliation if that future state is implemented.

The editor must not overload rows with live combat readiness unless a later requirement demonstrates that this improves configuration usability.

Planned semantic layers:

- accepted synchronized state;
- local draft delta;
- slot position/order;
- optional danger metadata;
- optional spell icon;
- future provider/domain/school filters only from server-authored presentation metadata.

A draft change should look distinct from an authoritative denial/block.

### 11.2 Radial wheel

Primary questions:

- which slot is under pointer/focus;
- which slot is selected;
- what page is active;
- which spell is being considered;
- whether a concise blocking/warning fact matters immediately.

The radial should not become a dense diagnostic dashboard.

Normal-space priority:

1. spell identity/icon/name;
2. selected/focus cue;
3. concise block/cooldown/warning cue when safely available;
4. page/slot identity.

Detailed denial text remains better suited to the contextual HUD/result feedback.

### 11.3 Contextual HUD

Primary questions:

- what is selected;
- what important danger/gate fact currently matters;
- what the server said about the last cast request.

The HUD owns the highest-fidelity transient wording for:

- authoritative denial;
- danger threshold explanation;
- forecast category;
- future bounded cooldown/cost/channel/timer detail if those contracts are deliberately approved.

The HUD must remain transient/contextual.

### 11.4 External/provider-hosted invocation surfaces

If Iron's or another provider hosts presentation/invocation for a Black Arcana-owned operation:

- the provider may own that host surface's own appearance;
- Black Arcana must not require the external UI to adopt Black Arcana's entire visual language;
- Black Arcana-authored denial/risk/context must retain the same semantic wording/meaning when surfaced by Black Arcana's own contextual layer;
- host UI appearance must never be treated as proof that provider-owned mana/cooldown semantics apply to the Black Arcana transaction.

For unrelated provider-owned spells, provider visual semantics remain provider-owned.

### 11.5 Future book/weapon/staff surfaces

D005 allows optional invocation surfaces.

Any future Black Arcana-owned surface should reuse the semantic roles in this plan rather than inventing new meanings for selection, blocked, warning, denial or unavailable.

It must still terminate in the same canonical cast pipeline.

---

## 12. Motion, flashes, particles and audio

### 12.1 Motion

Motion may reinforce:

- focus transition;
- page change;
- short denial/success emphasis;
- channel progress once a server lifecycle contract exists.

Motion must not:

- be the only carrier of state;
- alter timing or cast authority;
- create camera movement that hides required information;
- ignore the reduced-motion preference.

Reduced motion should replace decorative movement with static emphasis where necessary.

### 12.2 Flashes

Bright/full-screen flashes are never required for understanding a Stage 05 cast state.

Any future flash/pulse must:

- consume the reduced-flashes preference;
- remain supplemental;
- avoid repeated high-frequency flicker as a semantic dependency;
- preserve denial/warning meaning through text/static cue.

### 12.3 Particles

Particles are spell/effect presentation, not HUD authority.

Stage 05 semantics must remain understandable when the Black Arcana client particle-density multiplier is zero.

A gameplay-critical telegraph cannot be particle-only.

### 12.4 Audio

Sound may supplement:

- selection;
- confirmation;
- denial;
- warning;
- page navigation.

Sound must not be the only carrier of a required state.

Exact sound assets/volume/pitch are outside this planning document and require original/compatible provenance.

### 12.5 Haptics

No general controller provider is currently confirmed.

Future haptics, if a verified provider is introduced, are supplemental presentation only and map to the same semantic roles. They do not become a gameplay or accessibility requirement for keyboard/mouse users.

---

## 13. Pending, loading and reconciliation semantics

A large source of UI ambiguity is the interval between local intent and server synchronization.

### 13.1 Loadout apply

Current editor behavior closes after sending the update. If a future UX exposes an awaiting-response state, the meanings must remain:

- `DRAFT_ONLY` — local unsent draft;
- `SUBMITTED / AWAITING AUTHORITATIVE SNAPSHOT` — request sent, no acceptance claim;
- `ACCEPTED SYNCHRONIZED STATE` — new server snapshot received;
- `REJECTED` — only if an explicit server-authored bounded result exists.

Do not show a green accepted checkmark merely because the client sent the packet.

### 13.2 Forecast request

While a forecast is pending:

- retain still-valid static metadata;
- do not reuse mismatched old dynamic forecast as current;
- use unavailable/pending wording only if it improves clarity without clutter;
- never treat absence of a reply as a gameplay denial.

### 13.3 Session/reconnect

On disconnect/session change:

- clear stale transient result/forecast state;
- clear any future channel/timer presentation tied to the old session;
- wait for fresh authoritative snapshots;
- do not flash previous-session accepted/denied state as current.

---

## 14. Modpack coexistence visual policy

05.06 remains authority for current-pack coexistence.

05.08 adds these visual rules:

1. Black Arcana's contextual layer should be visually identifiable without attempting to replace external provider action bars.
2. Black Arcana must not recolor another mod's resource/action bar to imply ownership.
3. If overlap occurs, resolve in this order:
   - current Black Arcana anchor/scale configuration;
   - reduced Black Arcana density;
   - safe supported layout reservation if a real provider seam exists;
   - documentation of a recommended anchor;
   - never brittle renderer takeover merely for cosmetic unification.
4. External UI being visible does not make its state part of Black Arcana's semantic matrix.
5. Black Arcana denial/danger information must remain readable when external casting/combat UI is present.

Real-client coexistence evidence remains mandatory for required rows; this plan does not convert them to PASS.

---

## 15. Layout and density budgets

### 15.1 Global rule

Meaning must survive smaller presentation before decoration does.

### 15.2 Radial

At most the current eight visible slots per page are rendered.

When space shrinks:

- reduce descriptive text first;
- preserve slot/focus identity;
- use icon/symbol with text fallback;
- move details to focused/center presentation;
- do not shrink hit regions below practical usability merely to retain ornament.

### 15.3 HUD

If contextual lines exceed a safe viewport:

- preserve denial/block/warning priority;
- wrap bounded text;
- reduce scale within documented limits where current layout permits;
- suppress lower-priority optional detail;
- never push required text off-screen.

### 15.4 Loadout editor

Pagination/search/filter should reduce density without changing server availability.

A visually filtered-out spell remains available according to server state; filtering is not a gameplay gate.

---

## 16. Provider/domain/school visual metadata

Future UX may want grouping/badges for provider, domain or school.

Rules:

- use only synchronized/server-authored presentation metadata or an exact supported provider presentation seam;
- do not infer categories from namespace/path naming conventions;
- do not infer spell ownership from color/icon art;
- a provider badge does not transfer resource/cooldown authority;
- mixed-ownership host cases must label semantics carefully if a label is ever needed.

Until such metadata exists, omit the badge/filter instead of deriving it heuristically.

---

## 17. Asset provenance and clean-room rules

Every new Black Arcana visual asset must have a provenance record appropriate to the repository's clean-room policy.

Allowed sources include:

- original project-created asset;
- user-created asset with clear ownership;
- third-party asset with verified compatible license/permission and attribution requirements satisfied;
- generated asset where the project's provenance policy permits it and the generation/source record is retained.

Do not copy/retrace provider UI textures, icons, spell glyphs, models, sounds or animations merely because they are useful references.

Behavioral/reference study may inform **what information must be readable**, not produce a clone of another mod's protected presentation.

---

## 18. Failure/degradation ladder

Presentation should fail in a deterministic order.

### Missing spell icon

`icon -> semantic/text card -> canonical name/id fallback`

No gameplay effect.

### Missing translation

`translated label -> translation fallback -> bounded canonical id`

No gameplay effect.

### Missing optional presentation metadata

`optional badge/value -> omit or Unavailable`

No client inference.

### Stale forecast

`dynamic forecast -> discard -> retain valid static metadata where applicable`

No stale override.

### Missing cooldown mapping

`generic selected-spell cooldown -> omitted`

Never assume `groupId == spellId`.

### Missing provider preview

`exact provider cost/resource preview -> Unavailable/omitted`

Never reconstruct provider formula.

### Missing optional provider/UI integration

`integration-specific polish -> disabled`

Core Black Arcana keyboard/mouse casting and contextual presentation continue.

---

## 19. Planned semantic implementation architecture

This section defines planning boundaries, not concrete classes.

When implementation is eventually approved, prefer a small client-only semantic mapping layer that converts already-authorized presentation facts into surface-neutral semantic roles.

The mapping layer should:

- consume Black Arcana-owned DTO/snapshot values only;
- not query world entities/chunks;
- not call resource/cost/cooldown admission services as gameplay authority;
- not contain provider implementation classes in common code;
- make the same semantic role reusable by editor/radial/HUD;
- keep surface geometry/rendering separate from state meaning;
- remain deterministic enough for pure unit testing.

Do not create a giant universal UI-state packet merely to simplify rendering. 05.07 authority/lifecycle boundaries remain primary.

Conceptual structure:

`server-authored/client-local presentation fact -> semantic role(s) -> surface-specific rendering`

Not:

`surface visual guess -> gameplay fact`.

---

## 20. Implementation gate for any 05.08-backed visual change

Before code/assets are written:

1. fetch latest `origin/main` and record SHA;
2. confirm no concurrent PR owns the same Stage 05 surface;
3. identify the exact state being represented;
4. identify its owner;
5. classify it through `07-presentation-data-contracts.md`;
6. identify the semantic family/role from this plan;
7. prove the visual does not collapse forecast, warning and authoritative result into one meaning;
8. define missing/stale fallback;
9. define reduced-motion/reduced-flash/particle behavior where relevant;
10. define localization and small-viewport behavior;
11. verify asset provenance for any new art/audio;
12. write deterministic RED tests for semantic-state mapping/helpers where applicable;
13. implement minimum GREEN presentation change;
14. run dedicated-server/client-classloading safeguards and full CI;
15. execute affected real-client rows;
16. re-fetch/reconcile latest `main`;
17. rerun exact-head validation before merge.

Aesthetic preference alone is not permission to add a new gameplay-data contract.

---

## 21. Automated test plan for future implementation

Where applicable, pure/client-state tests should cover:

- selection and hover remain independent;
- draft-only vs synchronized accepted loadout state;
- forecast clear does not map to cast success;
- warning vs hard block are distinct;
- authoritative denial overrides lower-priority transient presentation without becoming persistent spell state;
- stale forecast maps to unavailable/static fallback;
- missing icon maps to art fallback only;
- missing cooldown mapping produces no guessed per-spell cooldown;
- provider preview unavailable does not generate a fake value;
- semantic composition for selected + danger + cooldown + hover remains deterministic;
- feedback-level reductions remove detail without changing semantic truth;
- reduced-motion/reduced-flash branches preserve non-motion/non-flash cues;
- long translations keep critical state markers intact;
- session reset clears transient semantic state.

Tests should target pure/state logic rather than pixel-perfect colors unless a later stable render-test framework is deliberately introduced.

---

## 22. Real-client validation plan

Any implemented 05.08 visual refinement must be observed under the canonical Stage 05 matrix where relevant.

Minimum representative visual checks:

- 854×480;
- 1920×1080;
- 3440×1440;
- GUI scale Auto/2/3/4 where supported;
- bright outdoor scene;
- dark underground/interior scene;
- visually complex combat scene;
- external Spell Actionbar/provider UI visible where legitimate;
- Epic Fight battle mode where relevant;
- feedback `MINIMAL/STANDARD/VERBOSE` where the surface is affected;
- reduced motion/flashes where an applicable implemented effect exists.

Observe specifically:

- selected vs hovered distinction;
- warning vs hard block distinction;
- forecast vs authoritative denial wording;
- missing/unavailable state clarity;
- text/icon fallback behavior;
- no essential state carried only by color/motion/particles/audio;
- no new overlap that makes required denial/danger state unreadable.

Direct real-client observations become evidence only when attached to the exact tested SHA. Planning/CI does not convert rows to PASS.

---

## 23. Relationship to Stage 05 completion

05.08 is a planning refinement, not a new completion blocker by itself.

The current Stage 05 state remains:

`IMPLEMENTED / FINAL VALIDATION DEFERRED`

A visual-language item becomes mandatory only when:

- an existing required manual row fails because current semantics are ambiguous/unreadable; or
- an explicit reviewed decision promotes the refinement to required Stage 05 hardening.

Otherwise it remains:

- `APPROVED STAGE 05 HARDENING`;
- `OPTIONAL FOLLOW-UP`; or
- `CARRIED TO STAGE 09`.

The existence of this plan does not require implementing every conceptual icon, animation, badge, cooldown display, channel bar or provider visual integration before Stage 05 can close.

---

## 24. Non-goals

This plan does not authorize:

- new gameplay state;
- client-authoritative casting;
- client-side cooldown/cost/resource/progression calculation;
- a permanent Black Arcana mana/resource bar;
- `CLEAR = guaranteed success` semantics;
- `recommendation met = safe` semantics;
- `groupId == spellId` cooldown assumptions;
- local key duration as channel authority;
- guessed provider/domain/school classification;
- provider UI/resource ownership transfer;
- automatic recoloring/replacement of external HUDs;
- speculative controller APIs;
- world/entity scanning for presentation;
- copying another mod's protected visual/audio assets;
- fixed palette/font claims without an implementation/art-review task;
- declaring visual/manual validation complete from planning or automated CI.

---

## 25. Exit criteria for this planning task

05.08 is planning-complete when:

- cross-surface state families are explicit;
- selection/focus is separated from cast legality;
- forecast is separated from authoritative result;
- warning is separated from hard block;
- danger recommendation wording cannot imply safety;
- temporal UI remains gated by 05.07 contracts;
- missing data/art degrades without changing gameplay semantics;
- editor/radial/HUD/provider-hosted surfaces share one semantic vocabulary while retaining their own geometry/lifecycle;
- state does not rely exclusively on color/motion/flashes/particles/audio;
- provider/domain/school visuals require real metadata rather than heuristics;
- asset provenance/clean-room boundaries are explicit;
- implementation/test/real-client gates are defined;
- Stage 05 validation state remains unchanged;
- no Java/runtime/network/art implementation is included in this planning change.