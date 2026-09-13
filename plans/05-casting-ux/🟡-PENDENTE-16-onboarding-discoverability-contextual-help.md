# 05.16 — Onboarding, Discoverability & Contextual Help

## State

`PLANNING / NO RUNTIME CHANGE / DISCOVERABILITY AND HELP PRESENTATION CONTRACT`

Baseline used for this planning audit: `main@55939167301dfea71b0516b5b1acdb1844ca3305`.

This document defines the presentation boundary for future Black Arcana onboarding, control discovery, contextual help, first-use guidance and recoverable re-entry into help after dismissal.

It does **not** add tutorial screens, toast notifications, advancements, client persistence, new key mappings, server progression state, protocol fields or manual PASS evidence by itself.

Stage 05 remains `IMPLEMENTED / FINAL VALIDATION DEFERRED`. Planning discoverability does not convert any existing real-client matrix row to PASS.

---

## 1. Why this plan exists

Stage 05 already has a functioning casting workflow, but implementation existence and feature discoverability are different problems.

The current runtime exposes multiple input surfaces:

- radial selection;
- cast-selected input;
- loadout editor;
- eight direct quick-cast mappings.

The current default/input facts make discoverability a real product concern:

- radial defaults to `R`;
- cast-selected defaults to `V`;
- loadout editor is unbound by default;
- all eight direct quick-cast mappings are unbound by default;
- the pack includes many other mods with their own controls and casting/combat interfaces;
- Controlling `19.0.5` is physically present, but Black Arcana cannot depend on Controlling for core discoverability;
- current localization already names the Black Arcana key category and the individual mappings;
- repository search at this audit baseline did not identify an existing generic Black Arcana onboarding/tutorial/discoverability subsystem.

A player therefore may have a fully functional Stage 05 runtime without knowing:

1. that a loadout editor exists;
2. that selection and casting are intentionally separate;
3. that direct slots exist but are unbound by default;
4. where to rebind Black Arcana controls;
5. why a dangerous spell can be selectable but still denied or risky;
6. how to recover when another mod conflicts with a default key;
7. where richer inspection/help belongs without cluttering combat HUD space.

05.16 exists to make those capabilities discoverable without turning help UI into gameplay authority, progression authority or a second quest/tutorial system.

---

## 2. Architectural constraints

All 05.16 work must preserve the existing decisions and Stage 05 contracts.

Non-negotiable rules:

- client help is presentation only;
- onboarding never grants spells, unlocks progression, changes costs/cooldowns, changes hazard values or bypasses provider gates;
- onboarding never auto-casts;
- onboarding never converts selection into casting;
- help text never treats a local prediction as authoritative cast success;
- no second persistence authority for gameplay state;
- no second progression/tutorial authority owned by Stage 05;
- no required dependency on Controlling, Spell Actionbar, Epic Fight or any other optional client surface;
- no silent rebinding of another mod's keys;
- no forced global key reassignment;
- no permanent always-on tutorial HUD;
- no per-tick scanning of world/provider/mod state for tutorial triggers;
- no remote documentation dependency for core usability;
- no use of tutorial state to decide server cast legality;
- dedicated-server startup must not load client tutorial/UI classes.

Relevant architecture remains governed by D005, D006, D020, D023, D031 and the Stage 05 master plan.

---

## 3. Current verified discoverability baseline

### 3.1 Existing localized control names

`src/main/resources/assets/black_arcana/lang/en_us.json` currently contains localized labels for:

- `key.categories.black_arcana`;
- `key.black_arcana.open_radial`;
- `key.black_arcana.cast_selected`;
- `key.black_arcana.edit_loadout`;
- `key.black_arcana.quick_cast_1` through `quick_cast_8`.

This means future help can refer to actual Black Arcana controls through localization rather than inventing a parallel control vocabulary.

### 3.2 Existing screen hints

The current language file also contains bounded screen-level guidance such as:

- radial: selection is separate from casting;
- loadout editor: selected count, apply, clear and cancel hints.

These are useful local affordances but they are not a first-use discovery system.

A player who never discovers the screen cannot benefit from its in-screen hint.

### 3.3 Unbound defaults

The loadout editor and all eight direct quick-cast mappings are intentionally unbound by default.

This is compatible with a large modpack and avoids aggressively reserving keys, but it creates a discoverability requirement:

- unbound must be communicated as a valid state;
- the UI must never display an invented fallback key;
- help must point the player toward rebinding rather than pretending the action is inaccessible or broken;
- any displayed binding must reflect current client binding state rather than documentation defaults.

### 3.4 External key-management environment

Controlling `19.0.5` is physically installed.

Its presence may improve the player's ability to search/manage key mappings, but:

- presence is not an integration API;
- Black Arcana core help must still work if Controlling is absent;
- Stage 05 must use normal Minecraft key-mapping semantics as its base contract;
- direct Controlling integration requires exact-version API/source verification if ever needed.

### 3.5 No generic onboarding subsystem confirmed

Repository search at `main@55939167...` did not identify a Black Arcana-owned generic tutorial/toast/onboarding/help subsystem.

Therefore 05.16 must not describe such a subsystem as current runtime.

---

## 4. Relationship to existing Stage 05 plans

05.16 does not replace prior subplans.

- 05.01 owns input/loadout behavior.
- 05.02 owns radial behavior.
- 05.03 owns contextual combat HUD behavior.
- 05.04 owns presentation accessibility/client config.
- 05.05 owns final real-client validation handoff.
- 05.06 owns current-pack coexistence.
- 05.07 owns presentation-data authority.
- 05.08 owns visual/state semantics.
- 05.09 owns keyboard focus/navigation inside screens.
- 05.10 owns loadout-editor information architecture.
- 05.11 owns transient feedback arbitration/correlation.
- 05.12 owns icon/resource resolution.
- 05.13 owns target/aim presentation.
- 05.14 owns rich spell inspection/details.
- 05.15 owns cross-spell VFX/audio/animation/camera/telegraph presentation.

05.16 owns only:

- how the player discovers those surfaces;
- how the client communicates actual current bindings and unbound state;
- how first-use/contextual guidance is triggered, dismissed and revisited;
- how help remains bounded, localized and non-authoritative;
- how guidance avoids fighting the large modpack's other tutorial/control surfaces.

---

## 5. Discoverability authority model

Every help datum must be classified before rendering.

### 5.1 `CLIENT_BINDING_FACT`

Examples:

- current bound key for the Black Arcana radial;
- current bound key for cast-selected;
- whether loadout editor is unbound;
- whether a direct quick-cast mapping is unbound.

This is local client configuration fact.

It is presentation only and has no gameplay authority.

### 5.2 `SYNCHRONIZED_PLAYER_PRESENTATION_FACT`

Examples:

- accepted loadout is empty/non-empty;
- selected slot exists;
- a synchronized spell presentation entry exists;
- server-authored hazard/gate presentation is available.

These facts may help choose a relevant guidance message, but help must not reinterpret their gameplay meaning.

### 5.3 `AUTHORITATIVE_SERVER_RESULT`

Examples:

- cast denied with a bounded server-authored code/detail;
- cast accepted result for a `castId`.

Help may explain where to look for more information, but it must not rewrite the server result into a different gameplay diagnosis.

### 5.4 `CLIENT_HELP_PREFERENCE`

Examples:

- tutorial hints enabled/disabled;
- a local hint was dismissed;
- the player requested to reopen help.

This is client presentation state only.

It must never become a progression prerequisite.

### 5.5 `STATIC_LOCALIZED_GUIDANCE`

Examples:

- "selection and casting are separate";
- "configure Black Arcana controls in Minecraft key settings";
- "quick-cast slots are optional and may be unbound".

This guidance must remain generic and architecture-correct.

It must not contain balance/provider facts that can drift independently of the runtime.

### 5.6 `UNKNOWN_OR_UNAVAILABLE`

If the client cannot prove a binding, control surface or synchronized fact, guidance must omit or label it unavailable rather than fabricate a value.

---

## 6. Help-surface hierarchy

05.16 should prefer a small number of predictable surfaces instead of a tutorial framework that competes with gameplay.

### 6.1 Primary: contextual first-use hint

A compact, bounded first-use hint is the preferred initial discovery surface.

It should communicate only the minimum useful path, for example conceptually:

1. configure a loadout;
2. open radial/select;
3. cast with a separate input;
4. rebind controls if needed.

Exact copy belongs to localization/content review, not this architecture plan.

### 6.2 Secondary: loadout-editor help

The loadout editor is the natural persistent/revisit surface because:

- it is already configuration-oriented;
- it is not the combat-critical HUD;
- 05.10 already owns editor information architecture;
- 05.14 already prefers the editor for rich inspection.

A future Help/Controls area inside or adjacent to this screen may explain:

- current bindings;
- unbound direct slots;
- dense ordered slot semantics;
- selection versus casting;
- how Apply/Cancel works;
- how to revisit control settings.

It must not become a replacement for Minecraft's normal keybinding screen.

### 6.3 Tertiary: contextual failure/help affordance

Repeated user-facing confusion may justify a bounded help affordance after a denial or missing binding, but:

- the authoritative denial text remains primary;
- help cannot guess a reason not present in the server result;
- a help affordance must not obscure the normal HUD result;
- it must not create a permanent notification queue.

### 6.4 Re-entry path

Any first-use guidance must be revisitable.

A one-shot hint with no way to recover is insufficient, especially when:

- the user changes keybinds later;
- a modpack update adds conflicts;
- a player returns after a long break;
- a client config/profile is reset.

The exact UI entry point is an implementation decision, but a deterministic re-entry path is required before any one-shot dismissal is treated as complete UX.

---

## 7. Binding-display contract

### 7.1 Never hardcode documentation defaults as current bindings

`R` and `V` are current defaults, not permanent truth.

Any runtime help that claims "press R" or "press V" must obtain the current local binding through the supported Minecraft/NeoForge key-mapping surface.

If the user has rebound the action, help must show the rebound key.

### 7.2 Unbound is a first-class state

For an unbound mapping:

- render an explicit localized `Unbound`-equivalent presentation;
- do not invent a substitute key;
- do not imply the feature is unavailable server-side;
- give a bounded path toward key configuration.

### 7.3 Conflict presentation

05.16 does not authorize a custom key-conflict engine by assumption.

If future product requirements demand explicit conflict reporting:

- verify the exact supported Minecraft/NeoForge key-mapping APIs first;
- treat Controlling as optional presentation only unless an exact supported integration seam is verified;
- never modify another mod's keybind automatically;
- never choose a replacement binding silently.

### 7.4 Input-modality neutrality

Current guaranteed support is keyboard/mouse.

If a compatible controller provider is later installed and verified, 05.16 help should resolve the active provider's supported control label through an adapter rather than hardcoding keyboard-centric instructions everywhere.

Until then, controller-specific help remains unavailable/fail-closed.

---

## 8. Trigger lifecycle

Onboarding must be event-driven and bounded.

### 8.1 Candidate trigger classes

Potential triggers may include:

- first relevant client session after the feature is available;
- first accepted non-empty Black Arcana loadout snapshot;
- first opening of the loadout editor;
- first selection of a Black Arcana spell;
- attempt to use an action whose mapping is currently unbound;
- explicit player request to reopen help.

These are candidate product triggers, not implemented facts.

### 8.2 Trigger restrictions

A trigger must not:

- poll every tick for tutorial eligibility;
- scan world entities/chunks;
- query provider registries continuously;
- send a network request merely to decide whether to show local help;
- depend on hidden progression state not already legitimately synchronized;
- fire repeatedly because a server snapshot refreshes with identical content;
- fire during every cast;
- create an unbounded history of dismissed messages.

### 8.3 Session scope versus durable preference

The implementation must deliberately choose whether a hint is:

- session-only;
- client-profile durable;
- manually resettable.

No durable storage design is approved merely by this plan.

If durable client help-state is added later, it must be clearly separated from:

- server loadout persistence;
- spell unlock/progression state;
- cooldown/charge persistence;
- Arcane Danger state;
- RPG Skill Tree state.

### 8.4 Dismissal

Dismissal must be explicit and safe.

Dismissal:

- changes presentation only;
- does not disable casting;
- does not mark a gameplay objective complete;
- does not suppress authoritative denial/danger feedback;
- must not hide critical mandatory telegraphs from 05.13/05.15.

---

## 9. First-use guidance sequence

The minimum discoverability story should teach concepts rather than a rigid mandatory tutorial.

### Phase A — Find configuration

The player learns that Black Arcana has a loadout and that its editor may be unbound.

If the editor is unbound, guidance should say so explicitly and direct the player to the normal controls configuration path.

### Phase B — Understand selection

The player learns that radial interaction selects a spell.

Selection remains non-casting under 05.02.

### Phase C — Understand explicit cast

The player learns that casting is a separate action.

Help must never imply that opening/closing the radial casts automatically.

### Phase D — Understand optional quick slots

The player learns that quick-cast slots are optional accelerators and are unbound by default.

This must not create pressure to reserve eight default keys in the modpack.

### Phase E — Understand server feedback

The player learns that a selected spell can still be denied or dangerous because the server owns:

- progression;
- cost;
- cooldown;
- target;
- hazard;
- world-effect admission.

Help should explain the authority model generically, not reproduce dynamic internals as static tutorial text.

---

## 10. Contextual help and authoritative denials

### 10.1 Denial remains the source of truth

When a cast is denied:

- render the normal 05.03/05.11 authoritative result first;
- help may offer generic navigation or explanation;
- help must not replace the server-authored reason with an inferred one.

### 10.2 No denial diagnosis from selection state

Current `CastResultPayload` does not prove the current selected spell identity by itself.

Therefore a contextual help message must not say:

- "this selected spell failed because..."

unless safe correlation exists under 05.11.

Unknown/unmatched results remain generic.

### 10.3 Hazard guidance

If synchronized hazard presentation exists, help may explain the meaning of:

- normal;
- warning;
- below recommendation;
- hard blocked where the canonical gate actually says blocked.

It must preserve 05.08 semantics:

- recommended resistance is not a guarantee of safety;
- warning is not always a hard block;
- unknown data is not success.

---

## 11. Relationship to progression and RPG Skill Tree

05.16 must not become a progression engine.

Black Arcana onboarding may explain that some spells can be gated by progression, but:

- RPG Skill Tree remains authority only through its real provider contract;
- help does not award Mastery;
- help does not unlock perks;
- help does not create quests that substitute for real progression;
- help does not infer locked/unlocked state beyond legitimately synchronized presentation facts;
- completing/dismissing help never satisfies a spell gate.

A future quest/tutorial integration with another mod requires a separate provider boundary and is not implied by 05.16.

---

## 12. Modpack coexistence

The pack already has multiple UI/input/combat layers.

05.16 must therefore avoid becoming another aggressive tutorial overlay.

### 12.1 Controlling

Controlling may make Black Arcana mappings easier to find.

Black Arcana should remain usable without it.

No direct API is assumed from physical presence.

### 12.2 Spell Actionbar

Spell Actionbar owns its own presentation/control model.

Black Arcana help must not claim that Spell Actionbar controls Black Arcana unless an exact supported integration contract exists.

### 12.3 Iron's Spells 'n Spellbooks

Iron's may host resources/spell lifecycle in approved integrations.

Black Arcana onboarding must not duplicate or rewrite Iron's own tutorials/help as if Black Arcana owned them.

### 12.4 Epic Fight / EFIS / Punchy / lock-on / first-person stack

These mods can materially affect combat input and presentation.

05.16 should teach Black Arcana's own controls without assuming:

- Epic Fight mode is active;
- lock-on is active;
- a first-person body renderer is active;
- EFIS provides a Black Arcana bridge;
- Punchy owns Black Arcana casting.

Any specific integration remains gated by exact-version evidence.

### 12.5 Other tutorial/quest systems

If another installed mod later becomes the chosen global onboarding surface:

- Black Arcana may expose presentation metadata through a narrow adapter;
- Black Arcana must not create duplicate tutorial spam in parallel;
- gameplay authority remains unchanged;
- provider absence must fall back to Black Arcana's minimal local discoverability path.

---

## 13. Localization and text contract

All reusable help copy must be localized.

Rules:

- no hardcoded English in production help rendering;
- control names should reuse the existing key-mapping localization identity;
- current bound-key labels should be resolved dynamically rather than embedded in translation prose as fixed defaults;
- long help text must be bounded and wrap safely at small GUI scales;
- localization expansion must be accounted for in layout budgets;
- a missing translation degrades to a bounded fallback key/string presentation rather than breaking the screen;
- tutorial prose must not duplicate third-party copyrighted descriptions/tooltips.

Future PT-BR/localization work may add translations, but 05.16 does not claim any language pack beyond what actually exists.

---

## 14. Accessibility contract

Discoverability must remain accessible to players who cannot rely on one sensory channel.

Requirements:

- critical control guidance must be textual, not particle/audio-only;
- important states must not be color-only;
- help must respect reduced motion/reduced flashes for any animated emphasis;
- any notification timing must allow sufficient reading time or provide a revisitable surface;
- keyboard-only users must be able to dismiss and reopen help if the relevant screen supports the action;
- help must not steal combat focus unexpectedly;
- small viewport / high GUI-scale layouts must remain bounded;
- narration/screen-reader integration, if implemented, must use supported Minecraft client accessibility APIs verified for the target version rather than invented hooks.

---

## 15. Interaction and focus rules

### 15.1 No surprise modal during combat

A first-use tutorial should not unexpectedly open a full modal screen during active gameplay merely because a trigger fired.

Preferred behavior is a bounded non-blocking cue plus an explicit path to deeper help.

### 15.2 Screen ownership

When a Black Arcana screen is open:

- its normal input/focus rules remain governed by 05.09;
- help controls must not trigger world casts;
- text/search focus must not accidentally invoke Enter/Delete shortcuts owned by 05.10;
- dismissal must not implicitly apply loadout changes.

### 15.3 Escape/cancel behavior

Closing help with Escape/cancel:

- closes/dismisses presentation only;
- never casts;
- never applies a draft;
- never changes server state.

---

## 16. Persistence and reset policy

A future durable tutorial preference may be useful, but it must be narrow.

Permitted conceptual state:

- hints enabled;
- optional per-topic dismissed/seen flags;
- optional client-only schema/version for resetting obsolete hints.

Forbidden coupling:

- spell unlocks;
- server progression;
- mastery;
- loadout ownership;
- cooldowns;
- charge pools;
- ritual completion;
- Corruption/Strain;
- provider resources.

A migration/reset of help state must never affect gameplay state.

If implementation cannot guarantee this separation, durable state should be omitted and guidance should remain session-local.

---

## 17. Versioning and stale-help policy

Help text can become harmful when controls/runtime change.

Therefore:

- control-specific help should derive key labels dynamically;
- static help should describe stable concepts, not fragile numeric details;
- if a help schema/version is introduced, stale topics may be reset client-side after a relevant UX contract changes;
- version reset must not affect gameplay persistence;
- provider-specific help should be omitted if the provider contract is absent/incompatible;
- removed actions must not leave stale first-use prompts indefinitely.

---

## 18. Performance and network budgets

Onboarding is not permitted to become a background polling subsystem.

Hard requirements:

- event-driven triggers;
- bounded topic count;
- bounded active hint count;
- no global entity/chunk scans;
- no per-frame provider/API reflection;
- no per-tick network packets;
- no per-hover server dossier requests;
- no remote HTTP documentation lookup during gameplay;
- no unbounded history/log of shown hints;
- no unbounded client persistence growth;
- no duplicate hints on every identical snapshot refresh.

A reasonable implementation should be idle-cost-negligible after onboarding is dismissed/disabled.

---

## 19. Security and privacy boundary

05.16 help does not need sensitive player data.

It must not:

- upload keybind configuration;
- expose local filesystem paths;
- transmit tutorial-dismissal history to external services;
- infer or reveal protected world information;
- use server protection state as a tutorial oracle;
- scrape third-party UI internals dynamically.

If a server needs to provide a bounded help-related presentation fact in the future, that field requires the same validation/versioning discipline as other Stage 05 payloads.

---

## 20. Fail-closed behavior

Examples:

- current binding unavailable → show generic action name or `Unbound`/settings guidance; never invent a key;
- loadout editor unbound → feature remains valid; guide to key settings instead of declaring it broken;
- optional Controlling integration unavailable → use normal Minecraft control-discovery path;
- provider-specific help metadata unavailable → omit provider-specific claim;
- result cannot be correlated to attempted spell → generic result/help only;
- synchronized loadout absent/stale → do not trigger spell-specific guidance from guessed local state;
- help localization missing → bounded fallback presentation; no gameplay impact;
- help-state storage corrupt/missing → reset help presentation safely; never reset gameplay state;
- old help topic references removed action → suppress/reset topic rather than expose stale instruction;
- controller provider absent → no controller-specific button glyph/key claim;
- small viewport cannot fit rich help → compact/revisitable fallback rather than overlapping combat UI;
- user disables hints → suppress optional hints, but authoritative denial/hazard/gameplay telegraphs remain unaffected.

---

## 21. Proposed implementation phases

This is a future implementation plan only.

### Phase A — Pure discoverability model

Define pure client-side models for:

- help topic identity;
- topic priority;
- seen/dismissed/session state;
- current binding presentation state;
- eligibility from already-available local/synchronized facts;
- bounded active hint arbitration.

No network/progression changes.

### Phase B — Minimal first-use cue

Add one bounded, non-blocking first-use discoverability surface.

It should point toward:

- loadout configuration;
- radial selection;
- explicit casting;
- key configuration when mappings are unbound.

### Phase C — Re-entry/help surface

Add a deterministic way to revisit help after dismissal.

Prefer a configuration/editor-adjacent route rather than an always-visible HUD control.

### Phase D — Contextual unbound/conflict assistance

Only after exact API verification, add richer assistance for:

- unbound editor/quick slots;
- potential local key conflicts;
- current binding labels.

No silent rebinding.

### Phase E — Optional provider-aware help

Only if a real requirement appears and exact APIs are verified:

- provider-hosted casting help;
- controller-provider button labels;
- global quest/tutorial adapter.

These remain optional adapters, never core authority.

---

## 22. Deterministic test plan

Future implementation should add RED → GREEN tests for pure/state behavior before UI polish.

### 22.1 Binding presentation

Test:

- rebound key is displayed instead of default;
- unbound state is explicit;
- no fallback `R`/`V` is invented for rebound/unbound mappings;
- quick-cast 1–8 remain independently representable.

### 22.2 Topic arbitration

Test:

- only bounded active hints render;
- higher-priority required discoverability suppresses lower-priority optional hints;
- identical snapshot refresh does not retrigger a dismissed topic;
- session reset follows the chosen lifecycle contract;
- disabling hints suppresses optional topics.

### 22.3 Authority separation

Test:

- dismissing help never changes loadout/progression/cooldown/cost/hazard state;
- help activation never emits cast intent;
- help dismissal never applies a loadout draft;
- unknown result correlation never receives guessed spell identity.

### 22.4 Stale state

Test:

- removed/rebound action invalidates cached label presentation;
- stale synchronized loadout cannot drive spell-specific hint after reset;
- corrupt/missing help-state recovers without touching server state.

### 22.5 Layout

Test pure layout bounds where practical for:

- 854×480;
- high GUI scale;
- long localized strings;
- explicit `Unbound` labels;
- multiple current binding labels without overlap.

---

## 23. Real-client validation matrix

Any actual 05.16 implementation requires direct client evidence.

At minimum validate:

| Scenario | Required observation |
|---|---|
| fresh/default client help state | minimal discoverability appears only as designed |
| radial default binding | displayed key matches actual current mapping |
| radial rebound | help updates to rebound key, not `R` |
| cast-selected rebound | help updates to rebound key, not `V` |
| loadout editor unbound | explicit unbound/settings guidance |
| quick-cast unbound | no invented key; action remains optional |
| multiple modpack key conflicts | no automatic rebinding/stealing |
| Controlling absent in test profile where feasible | core discoverability still works |
| keyboard-only navigation | help dismiss/re-entry remains usable |
| small viewport/high GUI scale | no clipping/overlap |
| reduced motion/flashes | no essential help lost |
| authoritative denial while hint visible | denial/result remains primary and correct |
| disconnect/reconnect | stale contextual help does not leak across sessions incorrectly |
| help disabled | optional help disappears; gameplay feedback remains |
| revisit help | deterministic route exists after dismissal |

No row is PASS until observed on a real client/build.

---

## 24. Implementation gate

Before any 05.16 runtime work:

1. fetch latest `origin/main` and record SHA;
2. confirm no concurrent PR owns onboarding/help for Stage 05;
3. inspect current key mapping implementation and exact Minecraft/NeoForge API for current-binding labels;
4. verify whether any client config persistence mechanism already exists and can safely host presentation-only help preferences;
5. classify each proposed trigger by Section 5 authority;
6. define exact topic bounds/lifetimes;
7. define re-entry before adding one-shot dismissal;
8. verify focus/input behavior against 05.09/05.10;
9. verify result/hazard semantics against 05.08/05.11;
10. add deterministic RED tests;
11. implement minimum GREEN behavior;
12. run full CI;
13. execute affected real-client rows;
14. reconcile latest `main` again;
15. rerun exact-head gates before merge.

---

## 25. Non-goals

05.16 does not authorize:

- a mandatory questline;
- a new progression tree;
- tutorial completion as a spell unlock;
- tutorial completion as Mastery;
- automatic spell granting;
- automatic cast execution;
- auto-equipping a loadout;
- silent keybinding changes;
- forcing eight quick-cast default keys;
- a custom replacement for Minecraft's entire controls screen;
- requiring Controlling;
- requiring a controller mod;
- provider-specific instructions without verified provider contracts;
- a permanent tutorial HUD;
- a notification feed/history with unbounded growth;
- per-tick tutorial eligibility scans;
- remote web docs as a runtime dependency;
- gameplay truth inferred from local help state;
- copied Iron's/Ars/other-mod tutorial text, layouts or branded assets without compatible rights.

---

## 26. Clean-room and provenance

Black Arcana help text and visual assets should be original.

Third-party mods may inform interoperability requirements and observed user-flow constraints, but:

- do not copy their tutorial prose;
- do not copy branded key icons, diagrams or layouts without permission;
- do not reuse sounds/animations/screenshots as bundled assets without compatible rights;
- record any externally derived asset/code provenance under the repository's existing provenance process.

Generic platform terms such as keybind, radial, loadout and cooldown do not imply third-party ownership of Black Arcana's presentation.

---

## 27. Exit criteria for 05.16 planning

This planning document is complete when it defines:

- current discoverability facts and gaps;
- binding truth and unbound semantics;
- help authority categories;
- first-use and re-entry hierarchy;
- trigger/dismissal/session lifecycle;
- denial/hazard/help composition;
- progression/provider boundaries;
- localization/accessibility/focus rules;
- persistence/versioning separation;
- performance/security budgets;
- fail-closed behavior;
- implementation phases;
- deterministic and real-client validation gates;
- clean-room/provenance requirements.

Creating or merging this document does **not** implement those behaviors.

05.16 is not automatically a Stage 05 completion blocker. It becomes required implementation only when a direct real-client validation failure, explicit reviewed UX decision or concrete downstream product requirement promotes a specific discoverability item from optional planning to required hardening.
