# 05 — Casting & UX

## State

`IMPLEMENTED / FINAL VALIDATION DEFERRED`

The deterministic Stage 05 runtime is implemented on `main`. The remaining mandatory acceptance surface is the real-client visual/input matrix in `docs/qa/casting-ux-manual-matrix.md`; automated CI is supporting evidence and does not convert those manual rows to PASS.

This directory is also the canonical planning memory for any remaining Stage 05 UX hardening/refinement. Planned refinements are clearly separated from already-implemented runtime behavior.

## Where the plans are

Start here:

- **Master plan:** [`00-master-plan.md`](00-master-plan.md)

Subplans:

- [`01-input-loadouts.md`](01-input-loadouts.md) — input lifecycle, keybinds, 16-slot loadout, eight direct quick-casts, editor, persistence and synchronization;
- [`02-radial-wheel.md`](02-radial-wheel.md) — eight-slot pages, selection/cast separation, paging, geometry and planned icon/cooldown affordances;
- [`03-contextual-hud.md`](03-contextual-hud.md) — contextual selected-spell, hazard/gate/result presentation plus planned cooldown/cost/channel/timer presentation rules;
- [`04-accessibility-client-config.md`](04-accessibility-client-config.md) — client-only preferences, reduced motion/flashes/particles, rebindability, keyboard accessibility and optional controller boundary;
- [`05-final-client-validation-handoff.md`](05-final-client-validation-handoff.md) — exact real-client closeout campaign and evidence procedure;
- [`06-modpack-coexistence.md`](06-modpack-coexistence.md) — coexistence with Spell Actionbar, Iron's, Epic Fight/EFIS, Controlling and future optional input providers without duplicating authority;
- [`07-presentation-data-contracts.md`](07-presentation-data-contracts.md) — audited server/client presentation authority, current synchronized-data coverage and the exact contract gates for cooldown, cost, charges, channels and timers;
- [`08-visual-language-state-semantics.md`](08-visual-language-state-semantics.md) — implemented bounded cross-surface semantic core for focus, admission/result, hazard and accepted-vs-draft loadout state, plus the remaining vocabulary/accessibility gates for future presentation;
- [`09-keyboard-focus-navigation.md`](09-keyboard-focus-navigation.md) — keyboard-only focus/navigation semantics for radial and loadout screens while preserving existing mouse behavior, server authority and current keybinding contracts;
- [`10-loadout-editor-information-architecture.md`](10-loadout-editor-information-architecture.md) — dense ordered slot semantics, reordering, search, icon fallback, draft lifecycle, apply/reconciliation evidence limits and the metadata/protocol gates for richer editor feedback;
- [`11-contextual-feedback-orchestration.md`](11-contextual-feedback-orchestration.md) — bounded arbitration, priority, supersession, correlation and timing across selection context, server-authored forecasts and authoritative cast results;
- [`12-iconography-resource-resolution.md`](12-iconography-resource-resolution.md) — synchronized `iconId` resolution, safe text fallback, resource-reload/cache lifecycle, namespace boundaries, accessibility and clean-room asset provenance;
- [`13-targeting-aim-presentation.md`](13-targeting-aim-presentation.md) — authority-safe reticle/aim/target presentation across the real server-owned target kinds, advisory `targetHint`, stale-state/result correlation, world-safety boundaries, accessibility and coexistence;
- [`14-spell-details-inspection-presentation.md`](14-spell-details-inspection-presentation.md) — bounded spell inspection/detail presentation, field-level authority, static-vs-dynamic semantics, provider/world/target boundaries, localization, accessibility and fail-closed metadata behavior;
- [`15-casting-vfx-audio-animation-presentation.md`](15-casting-vfx-audio-animation-presentation.md) — authority-safe casting VFX/audio/player-animation/camera/telegraph lifecycle, cast-result correlation, sensory-accessibility budgets, optional animation-provider boundaries and real-pack coexistence;
- [`16-onboarding-discoverability-contextual-help.md`](16-onboarding-discoverability-contextual-help.md) — first-use discoverability, live keybind/unbound presentation, bounded contextual help, dismissal/re-entry, localization/accessibility and modpack-safe tutorial coexistence without progression authority.

The master plan prevails for Stage 05 planning structure; `plans/DECISIONS.md` prevails for architecture/authority contracts; current production code/tests prevail for what is actually implemented; the latest physical modlist prevails for installed coexistence surfaces and versions.

## Objective

Deliver direct, low-clutter casting after server contracts and integrations are stable:

- no universal staff requirement;
- no permanent extra mana HUD;
- fast loadouts;
- concise radial selection;
- readable authoritative failure reasons;
- rebindable input;
- presentation accessibility where practical;
- safe coexistence with the actual modpack's other casting/input/combat UIs;
- no transfer of gameplay authority to the client.

## Canonical implementation

- `ClientInputController` owns client intent emission only. Quick-cast and selected-cast input send `CastIntentPayload`; gameplay admission remains in the server runtime.
- `LoadoutNetworkBridge` synchronizes edits while `ArcanaServerRuntimeManager.handleLoadoutUpdate` validates spell availability and persists accepted loadouts through `BlackArcanaSavedData`.
- `BlackArcanaRadialScreen` is a client-only selector. Choosing a wedge changes selection and closes the screen; it never executes a cast.
- `CastingUxSemantics` maps already-authorized client/server presentation facts into surface-neutral focus, admission/result, hazard and loadout-membership roles. The radial consumes distinct selected/hovered/composite roles with non-color markers; the loadout editor distinguishes synchronized accepted membership from local draft additions/removals; the HUD distinguishes authoritative denial, effect failure and success without converting forecasts into cast results. This layer has no gameplay admission or provider authority.
- `BlackArcanaHudLayer` is contextual/event-driven and currently renders synchronized spell presentation, hazard/resistance, predictable-gate and cast-result feedback. Although cooldown-group snapshots are cached client-side, the current HUD does not render them directly as a per-spell cooldown widget.
- `SpellPresentationPayload.Entry` currently synchronizes `spellId`, `translationKey` and bounded non-blank `iconId`, but current radial/loadout/HUD rendering does not consume `iconId`; icon rendering remains a planned client presentation refinement under 05.12.
- `BlackArcanaClientConfig` owns presentation-only preferences: HUD enable/scale/anchor, feedback duration/intensity, radial hold/toggle, particle density, reduced motion and reduced flashes. These settings do not participate in gameplay validation.
- `BlackArcanaClient` is a physical-client entrypoint (`Dist.CLIENT`); dedicated-server runtime registration remains in the common mod entrypoint without loading client classes.

## Current bounded UX facts

- canonical loadout maximum: **16 slots**;
- current loadout representation: **ordered dense list** with no representable gaps between populated entries;
- current radial: **8 visible slots per page**;
- current direct quick-cast mappings: **8**, unbound by default;
- radial default key: `R`;
- selected-cast default key: `V`;
- loadout-editor mapping: unbound by default;
- radial modes: `TOGGLE` and `HOLD`;
- feedback levels: `MINIMAL`, `STANDARD`, `VERBOSE`.

These are current implementation facts, not a requirement that future versions can never change. Any change must preserve server authority, bounds and migration/rebind safety.

The current language resources localize the Black Arcana key category, radial, cast-selected, loadout-editor and all eight quick-cast mappings, plus bounded in-screen radial/loadout hints. Repository search at the 05.16 audit baseline did not identify a generic Black Arcana onboarding/tutorial/discoverability subsystem. Therefore current localized control labels are an available building block, not evidence that first-use discovery is already implemented.

## Current modpack coexistence facts

The current physical modlist confirms relevant adjacent surfaces:

- Iron's Spells 'n Spellbooks `1.21.1-3.16.3`;
- Spell Actionbar `1.1.4`;
- Epic Fight `21.17.3.1`;
- Epic Fight & Iron's Spellbook animation compat (`efiscompat`) `3.1.0`;
- Punchy `2.7e` + Punchy Epic Fight Compat `1.0.0`;
- FirstPerson `2.7.2`;
- Better Lock On `2.0.8-neoforge` + Lock-On Movement Fix `1.0.2`;
- NotEnoughAnimations `1.12.4`;
- Player Animator `2.0.4+1.21.1`;
- Player Animation Library `1.1.6+mc.1.21.1`;
- Controlling `19.0.5`;
- no confirmed top-level general controller framework.

Presence does not prove an integration API. The default Stage 05 strategy is **coexistence without forced unification**. See `06-modpack-coexistence.md` for exact deduplication, keybinding, HUD-overlap, Epic Fight and optional-integration rules, 05.15 for the audiovisual/player-animation/camera specialization, and 05.16 for discoverability/help coexistence. Controlling may improve key discovery but is not a core dependency.

## Planned refinement summary

The master/subplans explicitly retain the forward-looking UX targets that were obscured when PR #73 canonicalized Stage 05 around the already-implemented runtime.

Planned refinements include, subject to the detailed gates in each subplan:

- actually using synchronized `iconId` in loadout/radial presentation through one safe resource-resolution/fallback lifecycle rather than screen-specific path heuristics;
- better slot ordering/awareness in the 16-slot loadout editor while preserving dense ordered-list semantics;
- client-only search over real synchronized identity/name data;
- provider/domain/school filters only after bounded server-authored metadata exists;
- draft reset and explicit dirty-state semantics beyond the now-implemented accepted-vs-local-draft membership cues;
- explicit apply/rejection feedback only after a bounded server-authored result contract exists;
- compact cooldown/readiness affordance from synchronized server state;
- provider cost preview only through a bounded server-authored presentation contract;
- channel/charge presentation only through canonical server-owned session semantics;
- temporary ritual/domain timers only for owned/supported state;
- keyboard-only radial and loadout-screen navigation without adding another gameplay cast path;
- broader semantic non-color-only state cues beyond the implemented selected/hovered and accepted/draft markers;
- bounded feedback arbitration so current selection, forecast and authoritative result cannot be visually misattributed when their timing overlaps;
- authority-safe aim/target presentation that distinguishes local observation from server resolution and never turns reticle state into cast/world-safety authority;
- bounded spell inspection/detail presentation that shows only legitimately synchronized/server-authored facts and never reconstructs cost, cooldown, target, damage, provider or progression truth from IDs/names;
- one bounded audiovisual cast lifecycle that distinguishes local intent, server forecast, authoritative result, server-owned runtime events, decorative effects and provider-owned presentation;
- gameplay-relevant telegraphs only from server-owned geometry/lifecycle rather than local aim guesses;
- optional player-animation/camera adapters only after exact-version API verification, with provider absence degrading presentation rather than denying valid gameplay;
- first-use/contextual discovery that teaches loadout → select → explicit cast without auto-casting or creating progression;
- live current-binding/unbound presentation rather than hardcoded `R`/`V` instructions after rebinding;
- deterministic dismissal and re-entry so help is neither spammy nor permanently lost;
- systematic reduced-motion/reduced-flash/particle consumption by future effects;
- controller integration only if a real compatible provider enters the modlist/API surface;
- direct current-pack coexistence testing with external casting/actionbar/combat/animation/camera/tutorial/control surfaces before adding compatibility code.

None of those remaining bullet points is claimed as implemented merely because it is planned here.

`07-presentation-data-contracts.md` freezes the evidence gate behind data-driven refinements. In particular, current cooldown snapshots are keyed by canonical cooldown `groupId` while spell presentation metadata does not synchronize spell→group mapping, so a generic per-spell cooldown widget is not yet authorized. Exact cost, charge state, channel session/progress and ritual/domain timer presentation likewise require bounded server-authored contracts before implementation. Corruption/Strain client values remain intentionally withheld pending separate approval. Existing spell identity/name/icon, loadout, cast-result and hazard presentation contracts remain usable within their current bounds.

`08-visual-language-state-semantics.md` freezes the meaning layer **after** data authority is established and now implements its bounded currently-authorized core through `CastingUxSemantics`. Selection/focus remains separate from legality, forecast remains separate from authoritative cast result, effect failure remains separate from denial/success, and accepted server loadout membership remains separate from unsent local draft deltas. Temporal/provider states that 05.07 cannot currently authorize remain omitted rather than inferred.

`09-keyboard-focus-navigation.md` converts the existing keyboard-accessibility goal into an explicit screen-navigation contract. The current radial can page by keyboard but cannot focus/select wedges without a mouse, while the current loadout editor can apply/clear/page but cannot focus/toggle rows without a mouse. The plan adds no runtime itself: it specifies deterministic client-local focus, preserves existing Enter/Delete/page semantics, proposes screen-local traversal rather than new global default mappings, and requires keyboard activation to reuse the same existing selection/draft operations.

`10-loadout-editor-information-architecture.md` freezes the next editor layer. It records that the server loadout is a dense ordered list rather than sixteen sparse cells, proves that populated-spell reordering can already travel through the current ordered full-snapshot protocol, limits search to real synchronized display-name/id data, keeps provider/domain/school filtering fail-closed without metadata, and records that the current snapshot reply cannot prove an explicit acceptance/rejection reason. Rich apply-result feedback therefore remains gated behind a future bounded server-authored result contract.

`11-contextual-feedback-orchestration.md` freezes the transient-feedback arbitration layer. Selection context, advisory forecast and authoritative cast result remain independent bounded channels; an authoritative result outranks contradictory advisory state, but `CastResultPayload` currently carries `castId/status/code/detail` without spell or slot identity. The HUD must therefore never attribute a received result to the current selection by inference. A future bounded client-local `castId -> attempted spell/slot` context may improve presentation without gaining gameplay authority; unknown/unmatched results remain safely displayable without spell attribution. The current low-clutter model remains latest-received-result wins rather than an unbounded notification history.

`12-iconography-resource-resolution.md` freezes the resource-resolution layer for the already-synchronized icon identity. The current payload bounds `iconId` as text but does not itself parse it as a Minecraft resource identifier or prove that the resource exists. Future icon rendering must therefore parse/resolve through supported client resource semantics, fail to text/presentation fallback without changing spell validity, invalidate positive/negative assumptions on resource reload, avoid spell-ID/provider-path heuristics and preserve clean-room provenance. At baseline `48cb9a43...`, radial, loadout editor and HUD do not consume `iconId`, and the Black Arcana asset root contains only `lang/`; 05.12 adds no assets or runtime by itself.

`13-targeting-aim-presentation.md` freezes the target/aim presentation boundary around the existing server targeting runtime. Current `ClientInputController` only submits an advisory entity `targetHint` when `Minecraft.hitResult` is an `EntityHitResult`; `ServerEntityTargetSelector` resolves the canonical `ArcanaTargetSpec.Kind` paths from live server state, and `WorldEffectAdmissionService` remains the terrain-admission authority. Any future reticle, entity/block marker or area guide must therefore expose local uncertainty honestly, avoid per-frame network/protection/world scans, preserve `castId` correlation and never imply target legality, resolved impact identity or world-mutation permission without an explicit bounded server-authored presentation contract. 05.13 adds no reticle/runtime/protocol/asset or manual PASS evidence by itself.

`14-spell-details-inspection-presentation.md` freezes the spell-inspection boundary around the deliberately small current presentation contract. `SpellPresentationPayload.Entry` exposes identity/name/icon metadata, while richer server/runtime facts such as `ArcanaSpellDefinition.cost`, `requestsWorldMutation`, target semantics, cooldown relationships and provider/progression state are not generic client presentation data merely because they exist internally. Future details therefore require field-level authority classification, bounded/versioned synchronization where genuinely needed, static-vs-dynamic separation, localization/accessibility bounds and provider-native/fail-closed behavior. 05.14 adds no description metadata, detail UI, protocol fields or runtime by itself.

`15-casting-vfx-audio-animation-presentation.md` freezes the audiovisual cast-presentation boundary around the current server-authoritative runtime. Current Black Arcana has no generic cross-spell particle/sound/animation/camera system and the project asset root remains `lang/`-only at the 05.15 audit baseline. Future audiovisual work therefore distinguishes local intent from authoritative result, requires server-owned lifecycle/geometry for gameplay-relevant telegraphs, treats `castId` as the natural root correlation token where attribution is needed, keeps animation/camera provider failure as presentation degradation rather than gameplay denial, deduplicates provider-hosted presentation per root cast, consumes reduced-motion/reduced-flash/particle preferences and preserves Stage 07 ownership of per-spell audiovisual content. 05.15 adds no VFX/audio/animation assets, protocol fields, runtime adapters or manual PASS evidence by itself.

`16-onboarding-discoverability-contextual-help.md` freezes the discoverability boundary around the existing control/runtime facts. It treats current bindings and explicit unbound state as local presentation facts, requires runtime help to resolve the player's actual binding rather than repeating documentation defaults, keeps Controlling optional, separates help preferences from all gameplay/progression persistence, defines bounded first-use/dismissal/re-entry semantics and forbids tutorial completion from granting spells, Mastery or cast authority. 05.16 adds no tutorial UI, toast, new binding, protocol field, persistence or manual PASS evidence by itself.

## Automated evidence

Stage 05 has focused JUnit coverage for client selection, loadout drafts, HUD layout, radial layout/toggle semantics and small-viewport geometry. Server loadout persistence/validation and the complete project pipeline are exercised by the canonical CI suite.

Follow-up hardening is canonical:

- PR #56 fixed same-key `TOGGLE` radial close; merge `206e37134b37447b9573541c7013e36dd45654a6`; post-merge workflow `34008702833` (#1152) GREEN.
- PR #57 hardened the 854×480 / GUI-scale-4 layouts. Final head `01a77eab641896173585b66c6310662d820c9f0c` passed workflow `34010736078` (#1169); merge `f2bb9a19db92d869e4443b2047ad1c913f8d2a29` passed exact-SHA workflow `34010968124` (#1170), including JUnit, diff sanity, NeoForge build, built-JAR verification, Foundation GameTests and dedicated-server smoke.
- Canonical artifact for that hardening checkpoint: `black-arcana-f2bb9a19db92d869e4443b2047ad1c913f8d2a29`, artifact ID `9982472491`, SHA-256 `1ba6949ceb04f261646548b6d99a158f4f40211a5017ca1911c0e1a732f86cdb`.
- Stage 05.08 followed two explicit RED→GREEN cycles. CI #2173 (`34303964888`) failed because `CastingUxSemantics` did not yet exist; code checkpoint `8be77235f8118d28d41d467f5245066e65560758` passed CI #2175 (`34304304807`); the second RED CI #2177 (`34304569061`) failed because radial/loadout/HUD had not yet consumed the semantic helpers; reconciled code head `8f7777c68852f829e360f75b62dd7a8d88e59c93` passed CI #2183 (`34305182690`) through unit tests, diff sanity, NeoForge build, built-JAR verification, Foundation GameTests and dedicated-server smoke.

## Final validation handoff

The executable closeout plan is `plans/05-casting-ux/05-final-client-validation-handoff.md`.

It maps the remaining manual matrix to 05.01–05.04, freezes the exact-build/evidence requirements, defines PASS/FAIL/BLOCKED/Stage-09 carry handling, preserves the server-authoritative casting boundaries and specifies the synchronization/CI/merge gate required before this Stage can leave `FINAL VALIDATION DEFERRED`.

`06-modpack-coexistence.md` adds the real-pack coexistence planning layer. Its scenarios become blocking only when they reveal a required input/readability/authority failure; cosmetic unification or unsupported optional bridges do not automatically block Stage 05.

`08-visual-language-state-semantics.md` now has a bounded implemented semantic core whose direct visual acceptance remains deferred. `07-presentation-data-contracts.md`, `09-keyboard-focus-navigation.md`, `10-loadout-editor-information-architecture.md`, `11-contextual-feedback-orchestration.md`, `12-iconography-resource-resolution.md`, `13-targeting-aim-presentation.md`, `14-spell-details-inspection-presentation.md`, `15-casting-vfx-audio-animation-presentation.md` and `16-onboarding-discoverability-contextual-help.md` retain forward-looking authority/accessibility/editor/feedback/resource/target/inspection/audiovisual/discoverability gates for refinements not yet implemented. They do not make optional cooldown/cost/channel/timer/iconography/art/keyboard-navigation/editor/feedback/aim/inspection/VFX/audio/animation/camera/onboarding polish mandatory for Stage 05 closeout unless a directly observed validation failure or explicit reviewed decision promotes a specific refinement.

Implementing or merging a deterministic refinement does **not** validate Stage 05 by itself. Manual matrix states change only from direct real-client observations recorded through the canonical runbook.

## Implementation rule for planned refinements

A planned refinement does not automatically reopen or block Stage 05 closeout.

Before implementing one, classify it as either:

- `REQUIRED TO FIX A VALIDATION FAIL` — blocks the affected acceptance row until fixed;
- `APPROVED STAGE 05 HARDENING` — may merge without changing authority, then affected rows are retested;
- `OPTIONAL FOLLOW-UP` — does not block Stage 05 validation unless explicitly promoted to a requirement;
- `CARRIED TO STAGE 09` — future presentation/compatibility item whose real effect surface does not yet exist.

This prevents an endless UX wish list from making completion impossible while still preserving a precise roadmap.

## Exit criteria

The deterministic exit criterion is satisfied: a player can equip/select/cast Black Arcana spells through a concise workflow while spell availability, progression, cooldown, resource cost and denial remain server-authoritative.

Stage 05 reaches `VALIDATED / COMPLETE` only after all applicable manual rows are directly observed on an exact build and any legitimate future-only rows are explicitly carried forward rather than falsely marked PASS.

No manual PASS is inferred from CI.