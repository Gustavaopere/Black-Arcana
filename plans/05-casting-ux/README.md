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
- [`08-visual-language-state-semantics.md`](08-visual-language-state-semantics.md) — cross-surface semantic vocabulary for selection, forecast, denial, danger, temporal state, unavailable/fallback presentation, accessibility and clean-room visual identity;
- [`09-keyboard-focus-navigation.md`](09-keyboard-focus-navigation.md) — keyboard-only focus/navigation semantics for radial and loadout screens while preserving existing mouse behavior, server authority and current keybinding contracts;
- [`10-loadout-editor-information-architecture.md`](10-loadout-editor-information-architecture.md) — dense ordered slot semantics, reordering, search, icon fallback, draft lifecycle, apply/reconciliation evidence limits and the metadata/protocol gates for richer editor feedback.

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
- `BlackArcanaHudLayer` is contextual/event-driven and currently renders synchronized spell presentation, hazard/resistance, predictable-gate and cast-result feedback. Although cooldown-group snapshots are cached client-side, the current HUD does not render them directly as a per-spell cooldown widget.
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

## Current modpack coexistence facts

The current physical modlist confirms relevant adjacent surfaces:

- Iron's Spells 'n Spellbooks `1.21.1-3.16.3`;
- Spell Actionbar `1.1.4`;
- Epic Fight `21.17.3.1`;
- Epic Fight & Iron's Spellbook animation compat (`efiscompat`) `3.1.0`;
- Controlling `19.0.5`;
- no confirmed top-level general controller framework.

Presence does not prove an integration API. The default Stage 05 strategy is **coexistence without forced unification**. See `06-modpack-coexistence.md` for exact deduplication, keybinding, HUD-overlap, Epic Fight and optional-integration rules.

## Planned refinement summary

The master/subplans explicitly retain the forward-looking UX targets that were obscured when PR #73 canonicalized Stage 05 around the already-implemented runtime.

Planned refinements include, subject to the detailed gates in each subplan:

- actually using synchronized `iconId` in loadout/radial presentation;
- better slot ordering/awareness in the 16-slot loadout editor while preserving dense ordered-list semantics;
- client-only search over real synchronized identity/name data;
- provider/domain/school filters only after bounded server-authored metadata exists;
- draft reset and explicit dirty-state semantics;
- explicit apply/rejection feedback only after a bounded server-authored result contract exists;
- compact cooldown/readiness affordance from synchronized server state;
- provider cost preview only through a bounded server-authored presentation contract;
- channel/charge presentation only through canonical server-owned session semantics;
- temporary ritual/domain timers only for owned/supported state;
- keyboard-only radial and loadout-screen navigation without adding another gameplay cast path;
- semantic non-color-only state cues;
- one cross-surface semantic vocabulary so selection, forecast, warning, hard block, authoritative denial, unavailable state and presentation fallback never drift into contradictory meanings;
- systematic reduced-motion/reduced-flash/particle consumption by future effects;
- controller integration only if a real compatible provider enters the modlist/API surface;
- direct current-pack coexistence testing with external casting/actionbar/combat surfaces before adding compatibility code.

None of those bullet points is claimed as implemented merely because it is planned here.

`07-presentation-data-contracts.md` freezes the evidence gate behind data-driven refinements. In particular, current cooldown snapshots are keyed by canonical cooldown `groupId` while spell presentation metadata does not synchronize spell→group mapping, so a generic per-spell cooldown widget is not yet authorized. Exact cost, charge state, channel session/progress and ritual/domain timer presentation likewise require bounded server-authored contracts before implementation. Corruption/Strain client values remain intentionally withheld pending separate approval. Existing spell identity/name/icon, loadout, cast-result and hazard presentation contracts remain usable within their current bounds.

`08-visual-language-state-semantics.md` then freezes the meaning layer **after** data authority is established. It separates selection/focus from legality, forecast from authoritative cast result, warning from hard block, and presentation fallback from gameplay unavailability. It also defines how those meanings compose across editor, radial, HUD and future provider-hosted surfaces without relying only on color/motion/audio or copying another mod's presentation language.

`09-keyboard-focus-navigation.md` converts the existing keyboard-accessibility goal into an explicit screen-navigation contract. The current radial can page by keyboard but cannot focus/select wedges without a mouse, while the current loadout editor can apply/clear/page but cannot focus/toggle rows without a mouse. The plan adds no runtime itself: it specifies deterministic client-local focus, preserves existing Enter/Delete/page semantics, proposes screen-local traversal rather than new global default mappings, and requires keyboard activation to reuse the same existing selection/draft operations.

`10-loadout-editor-information-architecture.md` freezes the next editor layer. It records that the server loadout is a dense ordered list rather than sixteen sparse cells, proves that populated-spell reordering can already travel through the current ordered full-snapshot protocol, limits search to real synchronized display-name/id data, keeps provider/domain/school filtering fail-closed without metadata, and records that the current snapshot reply cannot prove an explicit acceptance/rejection reason. Rich apply-result feedback therefore remains gated behind a future bounded server-authored result contract.

## Automated evidence

Stage 05 has focused JUnit coverage for client selection, loadout drafts, HUD layout, radial layout/toggle semantics and small-viewport geometry. Server loadout persistence/validation and the complete project pipeline are exercised by the canonical CI suite.

Follow-up hardening is canonical:

- PR #56 fixed same-key `TOGGLE` radial close; merge `206e37134b37447b9573541c7013e36dd45654a6`; post-merge workflow `34008702833` (#1152) GREEN.
- PR #57 hardened the 854×480 / GUI-scale-4 layouts. Final head `01a77eab641896173585b66c6310662d820c9f0c` passed workflow `34010736078` (#1169); merge `f2bb9a19db92d869e4443b2047ad1c913f8d2a29` passed exact-SHA workflow `34010968124` (#1170), including JUnit, diff sanity, NeoForge build, built-JAR verification, Foundation GameTests and dedicated-server smoke.
- Canonical artifact for that hardening checkpoint: `black-arcana-f2bb9a19db92d869e4443b2047ad1c913f8d2a29`, artifact ID `9982472491`, SHA-256 `1ba6949ceb04f261646548b6d99a158f4f40211a5017ca1911c0e1a732f86cdb`.

## Final validation handoff

The executable closeout plan is `plans/05-casting-ux/05-final-client-validation-handoff.md`.

It maps the remaining manual matrix to 05.01–05.04, freezes the exact-build/evidence requirements, defines PASS/FAIL/BLOCKED/Stage-09 carry handling, preserves the server-authoritative casting boundaries and specifies the synchronization/CI/merge gate required before this Stage can leave `FINAL VALIDATION DEFERRED`.

`06-modpack-coexistence.md` adds the real-pack coexistence planning layer. Its scenarios become blocking only when they reveal a required input/readability/authority failure; cosmetic unification or unsupported optional bridges do not automatically block Stage 05.

`07-presentation-data-contracts.md`, `08-visual-language-state-semantics.md`, `09-keyboard-focus-navigation.md` and `10-loadout-editor-information-architecture.md` are forward-looking authority/meaning/accessibility/editor gates for future presentation refinements. They do not make optional cooldown/cost/channel/timer/iconography/art/keyboard-navigation/editor polish mandatory for Stage 05 closeout unless a directly observed validation failure or explicit reviewed decision promotes a specific refinement.

Creating or merging planning documents does **not** validate Stage 05 by itself. Manual matrix states change only from direct real-client observations recorded through the canonical runbook.

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
