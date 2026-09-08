# 05.14 — Spell Details & Inspection Presentation

## State

`PLANNING / NO RUNTIME CHANGE / SPELL INSPECTION PRESENTATION CONTRACT`

This document defines the canonical Stage 05 plan for presenting richer Black Arcana spell details without exposing server-only execution state as client authority, duplicating provider UI, or turning combat surfaces into permanent information panels.

Baseline used for this audit: `main@ede7dc310499ec21941504e8e6754d4f7c7f512e`.

This is a planning artifact only. It does **not** add Java runtime behavior, description metadata, new payload fields, tooltips, detail panels, codex screens, cooldown/cost/target synchronization, provider bridges, assets or manual PASS evidence.

---

## 1. Why this plan exists

Stage 05 already has a deterministic input/loadout/radial/HUD runtime plus planning contracts for presentation authority, semantic state, keyboard navigation, editor information architecture, feedback arbitration, icon resolution and target/aim presentation.

The remaining planning gap is **inspection depth**.

The current combat UX intentionally stays compact. `00-master-plan.md` states that dense or verbose information belongs in tooltips or verbose/inspection presentation rather than competing with the playfield. However, no Stage 05 subplan currently defines:

- which spell facts may appear in a tooltip/detail panel;
- which facts are already synchronized to the physical client;
- which server-side fields must remain omitted until an explicit presentation contract exists;
- how static identity differs from dynamic cast-time state;
- how provider-owned resource/cooldown semantics are represented without inventing a second economy;
- how target, world-mutation, hazard and progression facts compose without implying cast success;
- how descriptions/localization are bounded;
- how inspection behaves with keyboard focus, pointer hover, small viewports and the radial;
- how stale snapshots/reloads are invalidated;
- how Black Arcana avoids scraping or copying another provider's tooltips/descriptions/assets.

Without this plan, a future detail UI could read server runtime objects directly on an integrated client, guess costs or cooldowns from IDs, copy provider wording, show target geometry as guaranteed truth, or trigger a network request every time the pointer moves over a spell.

05.14 closes that planning gap.

---

## 2. Current verified runtime facts

### 2.1 The synchronized spell presentation contract is intentionally small

Current:

`src/main/java/dev/gustavopere/blackarcana/network/SpellPresentationPayload.java`

synchronizes one bounded `Entry` containing exactly:

- `spellId`;
- `translationKey`;
- `iconId`.

The payload:

- validates protocol compatibility;
- bounds the total presentation-entry count;
- rejects duplicate spell IDs;
- validates the canonical spell ID syntax;
- requires non-blank translation/icon identifiers;
- bounds translation-key and icon-id lengths.

It does **not** currently synchronize a generic spell description, provider, domain/school, cooldown-group mapping, resource cost, target specification, charge/channel state, progression requirement, world-mutation profile or detailed hazard explanation.

Therefore the baseline safe static identity set for generic Stage 05 inspection is currently only the data actually present in this bounded payload.

### 2.2 The server spell definition contains more data than the presentation payload

Current:

`src/main/java/dev/gustavopere/blackarcana/api/ArcanaSpellDefinition.java`

contains:

- canonical `id`;
- `translationKey`;
- `iconId`;
- `ArcanaCost cost`;
- `boolean requestsWorldMutation`.

This proves those fields exist in the canonical spell definition on the server/runtime side. It does **not** automatically make them client presentation data.

The existence of a server field is not permission to:

- reach into the integrated server from client GUI code;
- mirror it through an ad-hoc packet;
- assume it is sufficient to explain provider economics;
- expose it without bounds/localization/staleness rules;
- treat it as complete cast-time truth.

05.07 remains the authority gate for adding synchronized presentation data.

### 2.3 `ArcanaCost` is a canonical cost descriptor, not a ready-made localized tooltip

Current:

`src/main/java/dev/gustavopere/blackarcana/api/ArcanaCost.java`

contains:

- `resourceId`;
- non-negative finite `amount`;
- unit `FLAT` or `PERCENT_OF_MAX`.

That is an execution/domain contract. A raw resource ID is not necessarily a player-facing localized provider name, and a cost descriptor does not by itself prove the player's current balance or that the eventual transaction will succeed.

Consequently a future inspection UI must distinguish:

- static configured cost identity/amount, if explicitly synchronized for presentation;
- provider-owned current resource availability, which requires a real supported presentation seam;
- authoritative cast admission, which remains server-owned at cast time.

### 2.4 Current loadout tooltip is hazard-specific, not a generic spell dossier

Current:

`src/main/java/dev/gustavopere/blackarcana/client/BlackArcanaLoadoutScreen.java`

builds its available-spell list from the synchronized presentation snapshot and displays synchronized spell names. On pointer hover it may show `hazardTooltip(...)`, which is derived from the synchronized hazard preflight entry.

It does not currently render a general description/cost/cooldown/target/details tooltip.

This distinction matters: the existing hazard tooltip must not be silently reinterpreted as a complete spell-details surface.

### 2.5 Current radial remains a selector with bounded context

Current:

`src/main/java/dev/gustavopere/blackarcana/client/BlackArcanaRadialScreen.java`

renders bounded slot/name context and synchronized hazard information. On compact viewports, hover may show the focused spell name as a tooltip.

The radial:

- selects but never casts;
- does not currently expose a rich details panel;
- must preserve its combat-speed and low-clutter purpose.

05.14 therefore does not turn the radial into a codex.

### 2.6 Current cooldown snapshots are not generically attributable to spells

05.07 already establishes that cooldown synchronization is authoritative by canonical cooldown `groupId`, while the current spell presentation contract does not synchronize the spell→cooldown-group relationship.

Therefore a detail panel must not display a per-spell cooldown by assuming:

`cooldownGroupId == spellId`.

A static or dynamic cooldown line requires the explicit presentation relationship already gated by 05.07.

### 2.7 Current target facts remain server-owned

05.13 establishes that the physical client does not have a generic server-authored target-spec/validity contract. The client may observe local crosshair state, but target resolution remains server-owned.

Therefore inspection must not derive target kind/range/LOS/eligibility from:

- spell name;
- translation key;
- icon path;
- provider namespace;
- current crosshair;
- local geometry guesses.

Exact target details may appear only when the corresponding bounded presentation metadata is deliberately exposed.

### 2.8 Current cast result does not make a static details panel authoritative

`CastResultPayload` remains authoritative for the result identified by `castId`, but it is an event result rather than a generic spell definition.

A details panel must not convert the latest cast denial/success into a permanent property of the inspected spell.

05.11 remains the authority for transient result correlation and supersession.

### 2.9 Current hazard presentation is a separate bounded channel

Stage 05/05A already synchronizes bounded hazard/preflight presentation used by the radial/loadout/HUD.

A detail surface may compose that existing presentation where useful, but must preserve:

- hazard forecast/preflight semantics;
- danger recommendation vs hard-block semantics;
- stale request/snapshot handling;
- the rule that hazard information does not guarantee final cast success.

### 2.10 There is no generic provider/domain/school metadata field in the current presentation entry

The current `SpellPresentationPayload.Entry` has no generic:

- provider id;
- provider display key;
- Black Arcana domain id;
- external school id;
- tags/categories list.

Accordingly, inspection/search/filter UI must not manufacture these values from namespace or naming conventions.

---

## 3. Relationship to existing Stage 05 plans

05.14 owns **inspection/detail presentation**, not the underlying gameplay data.

### `05.01 — Input & Loadouts`

Owns input lifecycle and canonical loadout intent.

Inspection must never become another cast path. Opening, focusing or scrolling details sends no cast intent.

### `05.02 — Radial Wheel`

Owns the compact combat selector.

05.14 may provide a short optional detail affordance for the focused spell, but the radial remains optimized for selection speed. Long descriptions/stat blocks belong outside the normal ring.

### `05.03 — Contextual HUD`

Owns low-clutter transient combat context.

The HUD may show only a concise subset of legitimate detail. Full inspection does not become a permanent HUD panel.

### `05.04 — Accessibility & Client Config`

Owns presentation preferences, reduced effects, bounded text and rebindability principles.

05.14 must remain readable with keyboard-only screen navigation, small viewports and non-color-only semantics.

### `05.05 — Final Client Validation Handoff`

Owns exact-build manual acceptance.

Creating 05.14 changes no existing PASS/PENDING row. Any implemented inspection refinement adds/retests only the affected real-client surface.

### `05.06 — Modpack Coexistence`

Owns coexistence with Iron's, Spell Actionbar, Epic Fight/EFIS, Controlling and other installed UI/input surfaces.

05.14 must not scrape, hide or replace provider-native tooltip/detail UI.

### `05.07 — Presentation Data Contracts`

Owns whether a datum may legitimately be synchronized/presented.

05.14 consumes only data authorized by 05.07. It does not bypass 05.07 by reading server-only runtime objects from client code.

### `05.08 — Visual Language & State Semantics`

Owns semantic meaning.

Static information, advisory forecast, authoritative denial, unknown/unavailable data and presentation fallback remain visually distinct.

### `05.09 — Keyboard Focus & Navigation`

Owns screen-local focus traversal.

Keyboard focus may change which spell is inspected, but focus never changes accepted loadout state or casts a spell.

### `05.10 — Loadout Editor Information Architecture`

Owns dense-list editor organization, search, reorder and draft/apply semantics.

05.14 defines the optional information shown *about* the currently hovered/focused spell. It does not alter dense ordered-list semantics.

### `05.11 — Contextual Feedback Orchestration`

Owns transient selection/forecast/result arbitration.

An inspection panel must not pin a transient denial/forecast as static spell metadata or attribute a result to the inspected spell without safe correlation.

### `05.12 — Iconography & Resource Resolution`

Owns safe `iconId` resolution and fallback.

05.14 may consume a resolved icon but must remain fully usable through text fallback.

### `05.13 — Targeting & Aim Presentation`

Owns local aim and target presentation authority.

05.14 may eventually display static target-mode metadata only when 05.07/05.13 approve a bounded client source. It never turns that metadata into a “current target valid” claim.

---

## 4. Canonical inspection authority model

The following labels are **planning vocabulary**, not claims that matching Java enums/classes already exist.

### 4.1 `STATIC_PRESENTATION_IDENTITY`

Data explicitly synchronized as bounded presentation metadata and stable until its presentation snapshot is replaced.

Baseline examples:

- canonical spell ID;
- translated spell-name key;
- synchronized icon ID, subject to 05.12 resource resolution.

This data describes identity/presentation, not cast legality.

### 4.2 `STATIC_SERVER_AUTHORED_DETAIL`

A future bounded field explicitly synchronized from the canonical server definition for presentation.

Potential examples, only after contract approval:

- description translation key;
- cost descriptor prepared for presentation;
- cooldown-group relationship or configured cooldown summary;
- target-mode metadata;
- world-mutation warning category;
- provider/domain classification.

No such category becomes available merely because the corresponding server object exists.

### 4.3 `DYNAMIC_SERVER_AUTHORED_PREVIEW`

Short-lived player/cast-context information returned or synchronized by a bounded server-owned presentation seam.

Existing hazard/gate forecast presentation is the model for this category.

Potential future examples include exact provider cost availability or readiness only if a real supported contract is approved.

Dynamic preview must be stale-safe and never rendered as immutable spell metadata.

### 4.4 `AUTHORITATIVE_EVENT_RESULT`

A server-authored cast outcome keyed by `castId`.

This is not a static detail row. It belongs to 05.11 transient feedback and may only be associated with an inspected spell when safe correlation proves the local attempted context.

### 4.5 `PROVIDER_OWNED_EXTERNAL_DETAIL`

Information whose authority belongs to Iron's, Ars Nouveau or another external provider.

Black Arcana may show it only through an exact verified provider-supported presentation seam or a Black Arcana server adapter that deliberately normalizes a bounded presentation value without taking over provider gameplay authority.

### 4.6 `UNKNOWN_OR_UNAVAILABLE`

When the required authority/data contract is absent, the UI omits the field or labels it unavailable where that is genuinely useful.

Unknown is never filled with a guessed value.

---

## 5. Canonical inspection surface hierarchy

### 5.1 Loadout editor — primary inspection surface

The loadout editor is the preferred Stage 05 surface for richer per-spell information because the player is already in a configuration screen rather than active world combat.

A future implementation may use:

- bounded hover tooltip;
- focus-triggered detail pane;
- explicit “details” affordance;
- compact stacked information lines.

The exact rendering is an implementation/art decision. The authority/content rules in this plan apply regardless of layout.

### 5.2 Radial — concise context only

The radial should normally show:

- spell identity;
- selected/focused state;
- compact authorized risk/readiness cues;
- at most a short detail hint when practical.

It should not show a paragraph-length description or large stat sheet during ordinary selection.

If deeper inspection is needed from the radial, prefer a deliberate secondary action/state that does not cast, rather than permanently expanding every wedge.

### 5.3 Contextual HUD — combat summary, not encyclopedia

The HUD remains event-driven and low-clutter.

A selected spell may eventually expose one or two high-value authorized detail lines, but full descriptions, provider documentation and multi-section stats belong to an inspection/configuration surface.

### 5.4 Future codex/wiki surfaces are not implicitly Stage 05

The repository may contain or later gain wiki/codex/reference systems. 05.14 does not create a separate in-game encyclopedia or duplicate the canonical external/project wiki.

If a future codex becomes a product requirement, its ownership, synchronization and progression/discovery semantics require their own plan rather than silently expanding Stage 05.

---

## 6. Baseline field-availability matrix

This table records what generic Stage 05 inspection may safely claim at the current baseline.

| Detail | Baseline authority | Current generic client availability | Rule |
|---|---|---:|---|
| Spell canonical ID | Black Arcana | yes | safe identity/fallback |
| Display name | Black Arcana presentation | yes (`translationKey`) | safe localized identity |
| Icon identity | Black Arcana presentation | yes (`iconId`) | resolve only under 05.12; fallback to text |
| Long description | none in current presentation payload | no | do not invent; requires bounded metadata/translation contract |
| Configured `ArcanaCost` | server spell definition | no generic presentation sync | do not read server object from client; 05.07 gate |
| Current provider balance / affordability | provider/server | no generic Stage 05 contract | provider-native or bounded server preview only |
| Cooldown group mapping | server/runtime | not in spell presentation | never assume group id equals spell id |
| Current cooldown readiness | server snapshot by group | only useful once mapping is authoritative | 05.07 gate |
| Charges | server-owned runtime | no generic inspection contract | omit until synchronized deliberately |
| Channel/charge progress | server-owned session | no generic inspection contract | omit until bounded lifecycle sync exists |
| Target kind/range/LOS rules | server target spec/runtime | no generic presentation contract | 05.13 gate; never infer |
| Current valid target | server target selector | no generic preview contract | local observation is advisory only |
| `requestsWorldMutation` | server spell definition | not in generic presentation payload | may become warning metadata only through deliberate contract |
| World-effect permission | Stage 04 server admission | no generic client authority | never infer or probe per hover |
| Danger/hazard preflight | Black Arcana server presentation | bounded existing channel | may compose with current semantics/staleness rules |
| Gate forecast | Black Arcana server presentation | bounded existing channel where supported | advisory only; not final admission |
| Current Corruption/Strain value | Black Arcana server state | intentionally not generically synchronized | remain withheld until separately approved |
| Provider/domain/school | provider/content authority | absent from current `Entry` | no namespace/name heuristics |
| Damage/effect magnitude | effect/runtime/provider authority | no generic presentation contract | never parse from wiki/name or duplicate server formulas |
| Progression requirement | RPG/server gate authority | no generic static field in current presentation entry | only through an approved bounded presentation contract |

The safe default is **less information with correct authority** rather than a detailed but false stat sheet.

---

## 7. Description and explanatory text contract

### 7.1 Description text is presentation, not executable data

If descriptions are added later, prefer localization identifiers/content that cannot execute gameplay logic.

Descriptions must never contain:

- commands to execute;
- Java class names as behavior hooks;
- scripts;
- formula expressions interpreted as gameplay code;
- provider reflection paths.

D021's declarative/non-executable rule remains applicable.

### 7.2 Description must not promise more than the server contract

A player-facing description should avoid categorical claims such as “always hits”, “cannot be resisted”, “safe”, or “ignores protection” unless the canonical runtime actually guarantees that behavior.

Where values are contextual/provider-dependent, wording must communicate the bounded truth rather than hard-code a number that can drift from server configuration.

### 7.3 Localization

Any new player-facing description/detail labels require translation keys or another explicitly approved bounded localization route.

Do not embed copied English provider documentation into Java or packets.

### 7.4 Text bounds

Future payload/UI contracts must bound:

- identifier lengths;
- number of detail fields;
- line/section counts where relevant;
- rendered width/height;
- any server-authored free/bounded detail string.

Prefer enumerated semantic codes + local translation keys over arbitrary unbounded server prose when practical.

---

## 8. Cost/resource detail semantics

### 8.1 Configured cost is not affordability

If a static cost descriptor is later synchronized, “cost: 20 mana” means only the configured requested cost represented by that contract.

It does not mean:

- the player currently has 20 mana;
- no other composite cost exists unless the contract covers all components;
- provider reservation will succeed;
- progression/cooldown/target/hazard checks will pass;
- the cast will commit.

### 8.2 Provider-native ownership

Black Arcana must not create a second Iron's mana, Ars Source/mana, Malum spirit or other provider-resource state merely to populate details.

Current resource/balance details remain provider-owned unless Black Arcana has a verified supported read-only presentation adapter.

### 8.3 Composite transactions

If future spell definitions expose multiple cost components, inspection must represent the complete bounded descriptor supplied by the server contract. Do not flatten one component into “the cost” while hiding another transaction requirement.

D017 transaction semantics remain server execution authority.

### 8.4 Percentage costs

`ArcanaCost.Unit.PERCENT_OF_MAX` is semantically distinct from `FLAT`.

If exposed later, presentation must preserve that distinction rather than converting it using an unsynchronized/stale local maximum.

---

## 9. Cooldown, charge and channel detail semantics

### 9.1 Cooldown

A configured cooldown duration and current readiness are different facts.

- static configured summary requires an authorized spell→cooldown contract;
- current readiness requires the authoritative group snapshot plus that mapping;
- client local wall-clock timing is not canonical gameplay time;
- a stale snapshot must not be labeled current after session/reload invalidation.

### 9.2 Charges

Charge capacity/current charges/recharge timing remain server-owned.

No generic charge line appears until the server deliberately synchronizes the necessary bounded state and relationship to the inspected spell.

### 9.3 Channel/charge-up sessions

D024 states that channel sessions are server-owned and release converges on the canonical engine.

Inspection may eventually describe that a spell supports channeling when bounded static metadata exists. Live progress requires the canonical session presentation contract; local key-hold duration is not authority.

---

## 10. Target and world-effect detail semantics

### 10.1 Static targeting description

A future field may describe target mode/range/geometry only from an approved server-authored presentation snapshot.

It remains a **rule description**, not current target-validity proof.

### 10.2 Current target state

05.13 owns current aim presentation. A static inspection pane does not turn local crosshair observation into a server-valid target line.

### 10.3 World mutation

`requestsWorldMutation` exists in `ArcanaSpellDefinition`, but actual terrain admission belongs to Stage 04 policy/profile/chunk/budget/protection checks.

If the field is later exposed, safe wording is a warning/category such as “may request world effects”, not “can modify this block” or “allowed here”.

### 10.4 No protection oracle

Hovering/focusing a spell must not trigger world/protection queries. Inspection must never reveal hidden region ownership or policy boundaries.

---

## 11. Hazard, resistance and progression detail semantics

### 11.1 Hazard

Existing synchronized hazard/preflight data may be included as a bounded section or tooltip line.

It must preserve 05.08 semantics:

- danger != denial;
- recommendation != immunity;
- `NORMAL` danger does not activate warning styling merely because the field exists;
- missing forecast remains unavailable/neutral rather than safe.

### 11.2 Resistance

Server-authored resistance/forecast values remain presentation only. Showing them does not transfer resistance calculation to the client.

### 11.3 Corruption and Strain

Current values remain intentionally absent from generic client synchronization under the Stage 05/05A contract.

05.14 does not reopen that decision. A future request to show these values requires separate approval and bounded server-authoritative synchronization.

### 11.4 Progression gates

A static “requires X” line may be useful, but it must come from a canonical server/RPG presentation contract.

The client must not inspect RPG internal storage or infer gates from locked/unlocked history.

---

## 12. Inspection state lifecycle

### 12.1 Current inspected spell

Inspection focus is client-local presentation state derived from a currently visible/selected/focused spell in a Stage 05 surface.

It is not synchronized as gameplay state.

### 12.2 Invalidation

Inspection state must reconcile or clear when relevant context changes, including:

- synchronized presentation snapshot replaced;
- inspected spell removed/unavailable from the current presentation/loadout context;
- resource reload invalidates icon resolution under 05.12;
- language reload changes localized text;
- screen closes;
- disconnect/session reset;
- dimension/session transition where dynamic preview state is invalidated;
- dynamic forecast request/result supersession.

### 12.3 Dynamic data is not cached as static definition

Hazard/gate/provider preview data with request/snapshot identity must retain its own lifetime and correlation.

Closing/reopening a detail surface must not “promote” expired dynamic data into permanent metadata.

---

## 13. Keyboard, pointer and accessibility semantics

### 13.1 Pointer hover

Hover may choose the local inspected item but must not:

- toggle draft membership;
- select radial slot automatically;
- cast;
- send a network request per pointer movement.

### 13.2 Keyboard focus

When 05.09 navigation is implemented, the focused row/wedge may drive the same inspection context as hover.

`FOCUSED`, `HOVERED`, `SELECTED`, draft membership and server-accepted loadout state remain distinct semantics.

### 13.3 Activation

A separate details-open action, if later needed, must be screen-local and must not reuse the gameplay cast mapping in a way that makes inspection accidentally cast.

Exact keys are implementation work; 05.14 does not invent a new global default keybinding.

### 13.4 Non-color-only state

Labels/symbols/layout must distinguish:

- static info;
- advisory preview;
- hard block/denial;
- danger/warning;
- unavailable/unknown;
- presentation fallback.

Do not encode the difference only as green/yellow/red.

### 13.5 Motion/flash/particles/audio

Inspection must not require decorative animation, particles, flashes or sound to communicate essential facts. Any such future polish remains subject to 05.04 preferences.

---

## 14. Layout and density rules

### 14.1 Information order

For a richer inspection surface, default priority is:

1. spell identity/name;
2. short description, when legitimately available;
3. immediate hard/unavailable state when server-authored;
4. cooldown/readiness when authorized;
5. cost/resource summary when authorized;
6. target/use mode when authorized;
7. danger/gate context;
8. lower-priority technical/detail lines.

This hierarchy does not mean every row must exist.

### 14.2 Small viewport

At `854×480` and high GUI scale, the detail surface must:

- remain fully inside the viewport;
- prefer scrolling/section reduction over text overlap;
- preserve the primary name/state line;
- not cover the entire central playfield from the radial;
- retain an accessible close/cancel route.

### 14.3 Long localization

Do not size hit regions from English strings alone.

Descriptions and labels need bounded wrapping/truncation/scroll behavior. Truncation must not remove the semantic state prefix while leaving a misleading number/value alone.

### 14.4 No permanent combat dossier

A full spell detail panel is opt-in/contextual. Idle gameplay remains visually quiet.

---

## 15. Provider/modpack coexistence

Current physical modpack context includes Iron's Spells, Spell Actionbar, Epic Fight/EFIS and Controlling as adjacent surfaces. Presence does not prove a details API.

### 15.1 Provider UI remains provider-owned

Do not:

- scrape another mod's tooltip widget;
- copy its localized description text into Black Arcana resources;
- reflect into private client classes merely to obtain a number;
- suppress provider tooltips globally;
- duplicate provider spell panels for provider-hosted casts where Black Arcana is not the cast authority.

### 15.2 Black Arcana transaction context

When Black Arcana owns the canonical cast transaction but delegates a resource/payment/effect facet to a provider, Black Arcana may expose only the bounded information its own verified adapter contract legitimately obtains for presentation.

Authority follows the actual transaction boundary, not thematic similarity.

### 15.3 Exact-version gate

Any new provider-specific detail adapter requires:

1. exact current mod/version/mod id confirmed from physical modlist;
2. exact API/source/docs inspected;
3. a stable read-only presentation seam identified;
4. no double-processing or duplicate resource state;
5. safe absence/incompatibility behavior.

No speculative provider class/method name is authorized here.

---

## 16. Performance and networking budgets

### 16.1 Default inspection should be snapshot-driven

Static details should render from already-synchronized bounded client presentation data.

### 16.2 No hover spam

Forbidden default pattern:

`mouse/focus changes -> send request -> receive full dossier`

on every frame or every row traversal.

If dynamic preview is genuinely necessary:

- reuse an existing bounded request/response where semantically correct;
- otherwise define a deliberate rate-limited event-driven contract;
- correlate request/response;
- cap payload fields/count/string lengths;
- protect against stale replies;
- cancel/ignore irrelevant replies rather than accumulating history.

### 16.3 No runtime scraping/scans

Inspection must not perform:

- filesystem/JAR scans;
- reflection discovery per hover/render;
- global world/entity/chunk scans;
- remote downloads;
- provider registry crawling every frame;
- protection queries every frame;
- unbounded text/layout caches;
- unbounded inspected-spell history.

### 16.4 Cache bounds

Any future formatted-detail cache must key off bounded presentation revision/identity and be invalidated on the relevant snapshot/language/resource reload. Do not cache dynamic player-specific admission facts as static definition text.

---

## 17. Dedicated-server and physical-client boundary

Inspection rendering remains physical-client-only.

Future code must preserve:

- common API/network records free of client GUI classes;
- server definition/cast/provider services free of `Minecraft` client singleton/render classes;
- GUI/detail renderer registered only on physical client;
- optional provider UI adapter isolated behind Black Arcana boundaries;
- no dedicated-server classloading of screens, fonts, textures or client resource helpers.

Dedicated-server smoke remains mandatory after any implementation that touches common/network/client registration boundaries.

---

## 18. Clean-room and provenance

05.14 does not authorize copying another mod's:

- spell description prose;
- tooltip wording;
- stat-block layout trade dress;
- icons;
- frames/backgrounds;
- animations;
- source code;
- sounds.

Reference mods may inform generic usability concepts. Black Arcana text/art/layout must be original or use assets/text with compatible permission and recorded provenance.

If provider names/trademarks are displayed as factual integration labels, use only what is necessary and sourced from the verified integration contract; do not imply ownership or redistribute provider assets.

Stage 09 provenance/notice rules remain applicable.

---

## 19. Proposed future implementation phases

These phases are planning only.

### Phase A — data/authority audit

1. fetch latest `origin/main` and record SHA;
2. inspect current `SpellPresentationPayload`, `ArcanaSpellDefinition`, active registry/data loaders, hazard/gate presentation and client sync state;
3. produce an explicit field-by-field authority table for the desired detail surface;
4. classify each field through 05.07 and this plan;
5. remove/defer any field lacking a legitimate bounded source.

### Phase B — minimal static inspection

Without changing gameplay authority:

- render current synchronized identity/name;
- consume icon only through 05.12 when implemented;
- preserve hazard tooltip behavior;
- add description only if a bounded presentation/localization contract is deliberately approved;
- keep unknown fields omitted.

### Phase C — static server-authored detail extensions

Only for demonstrated product needs, add the smallest bounded fields necessary for such facts as:

- description key;
- static target/use category;
- static cost descriptor;
- cooldown relationship/summary;
- world-effect warning category;
- provider/domain classification.

Every added field requires versioning, bounds, reload/update semantics and tests. Do not add a generic unbounded metadata map “for future flexibility”.

### Phase D — dynamic player-specific preview

Only where useful and supported:

- compose existing hazard/gate preview;
- add provider/resource/readiness preview only through verified server/provider contracts;
- maintain correlation/staleness rules;
- never merge dynamic preview into static definition cache.

### Phase E — real-pack coexistence and polish

Validate:

- external provider tooltips/actionbars remain intact;
- no duplicate/inconsistent resource/cooldown display;
- keyboard/pointer inspection works;
- small/ultrawide layouts;
- long localization;
- no accidental cast/draft mutation from details interaction.

---

## 20. Future TDD and automated test matrix

Do not create tests merely because this plan exists. When implementation begins, use actual current test structure and names.

### 20.1 Authority/fallback tests

- current presentation fields render without needing server runtime object access;
- absent description/detail fields remain omitted/unavailable;
- no guessed provider/domain/cooldown/target field is generated from IDs;
- missing/unresolvable icon remains presentation fallback only;
- static cost detail, if introduced, is distinct from affordability;
- dynamic preview never becomes static cached metadata.

### 20.2 Lifecycle tests

- presentation snapshot replacement reconciles inspected spell;
- inspected removed spell clears safely;
- disconnect/session reset clears inspection/dynamic context;
- stale dynamic reply cannot overwrite newer inspected context;
- resource/language reload invalidates only relevant presentation cache/state.

### 20.3 Interaction tests

- hover/focus changes inspection only;
- inspection never casts;
- inspection never mutates loadout draft by itself;
- keyboard focus and pointer hover resolve deterministic current inspected item;
- closing/cancel restores normal screen behavior;
- radial remains selection-only.

### 20.4 Bounds tests

- added payload field counts/string lengths are bounded;
- long description/translation layout remains contained where deterministic helpers permit testing;
- any dynamic request rate/cache/count is bounded;
- malformed optional metadata fails to safe fallback.

### 20.5 Regression tests

- existing spell presentation payload compatibility remains deliberate/versioned;
- loadout validation/persistence unchanged;
- cast ingress/engine authority unchanged;
- hazard/gate presentation semantics unchanged unless explicitly modified;
- dedicated-server classloading remains safe.

---

## 21. Real-client validation matrix for an implemented 05.14 refinement

Any implemented inspection/detail surface requires direct physical-client evidence.

Viewport/GUI baseline:

- `854×480`;
- `1920×1080`;
- `3440×1440`;
- GUI scale `Auto`;
- GUI scale `2`;
- GUI scale `3`;
- GUI scale `4` where selectable/applicable.

Applicable scenarios:

1. spell with only baseline identity fields;
2. spell with hazard information;
3. missing/malformed/unresolvable optional icon;
4. missing optional detail field;
5. long localized spell name;
6. long description/detail text if implemented;
7. pointer hover changes inspected spell without draft mutation;
8. keyboard focus changes inspected spell without draft mutation/cast;
9. page change/clamp and inspected-state reconciliation;
10. small viewport clipping/scroll containment;
11. ultrawide alignment;
12. radial retains low-clutter selection behavior;
13. HUD remains contextual, not permanent details panel;
14. server snapshot/reload removes/changes a spell while screen context exists;
15. dynamic hazard/gate preview becomes stale/superseded;
16. Iron's/Spell Actionbar present simultaneously;
17. no duplicate/conflicting provider resource/cooldown truth;
18. Epic Fight combat screen/context does not make details intercept world cast input incorrectly;
19. disconnect/reconnect clears stale inspection state;
20. client language/resource reload behaves safely.

If exact cost/cooldown/target/provider metadata is implemented later, add direct rows proving each displayed field matches the server/provider-authored source and degrades safely when the optional source is unavailable.

Manual evidence must record the exact build/SHA and follow `05-final-client-validation-handoff.md`.

---

## 22. Implementation gate

No 05.14 runtime implementation begins until all applicable boxes are satisfied.

### Synchronization

- [ ] Latest `origin/main` fetched and SHA recorded.
- [ ] Correct branch/PR checked for equivalent work.
- [ ] Branch reconciled with latest relevant `main` before editing.

### Authority

- [ ] Desired detail fields enumerated explicitly.
- [ ] Every field classified under 05.07/Section 4.
- [ ] Server-side existence is not being mistaken for client presentation permission.
- [ ] No provider-owned resource/state is duplicated.
- [ ] No dynamic preview is being presented as static definition truth.

### Data/network

- [ ] Existing payload is sufficient, or the exact missing field is justified before schema change.
- [ ] New fields are typed/bounded/versioned; no arbitrary metadata bag.
- [ ] Reload/update invalidation is defined.
- [ ] No per-hover/per-frame network spam.
- [ ] Dynamic requests, if any, are rate-limited, correlated and stale-safe.

### UX/accessibility

- [ ] Loadout editor remains the primary rich-inspection candidate.
- [ ] Radial remains compact and selection-only.
- [ ] HUD remains contextual.
- [ ] Important state is non-color-only.
- [ ] Long localization and small viewport behavior are defined.
- [ ] Pointer/keyboard inspection cannot cast or mutate draft implicitly.

### Target/world safety

- [ ] Target details obey 05.13.
- [ ] `requestsWorldMutation` presentation, if exposed, is not permission.
- [ ] No protection/world scans are introduced for details.
- [ ] No hidden ownership/protection data is leaked.

### Provider/clean-room

- [ ] Current physical modlist rechecked for provider versions.
- [ ] Exact provider API/source verified before any adapter.
- [ ] No tooltip scraping/private reflection path.
- [ ] No copied provider descriptions/assets/layout trade dress.
- [ ] Provenance recorded where new assets/text require it.

### Validation

- [ ] Deterministic RED tests added first where applicable.
- [ ] Minimum GREEN implementation follows.
- [ ] Full CI green on exact branch HEAD.
- [ ] Affected real-client rows executed on exact build.
- [ ] `origin/main` fetched again immediately before merge.
- [ ] Relevant main changes reconciled semantically.
- [ ] CI re-run after final reconciliation.
- [ ] Merge only with valid exact-head evidence.
- [ ] Final main SHA recorded.

---

## 23. Fail-closed rules

When information is missing or uncertain:

- missing presentation entry → canonical ID/name fallback where possible;
- missing description → omit description, do not synthesize lore/mechanics;
- missing provider/domain/school metadata → omit classification, do not infer from namespace/name;
- server has a cost but client lacks an approved presentation contract → do not show raw/guessed cost;
- raw resource ID lacks player-facing provider semantics → do not pretend it is a localized resource label;
- no authoritative spell→cooldown-group mapping → omit per-spell cooldown;
- charge/channel state unavailable → omit it;
- target spec unavailable → omit exact target mode/range/LOS claims;
- `requestsWorldMutation` not synchronized → do not infer from spell effect/name;
- world/protection admission unavailable → never show “allowed here”;
- hazard/gate forecast unavailable/stale → render unavailable/neutral according to 05.08, never safe/success;
- Corruption/Strain current value unavailable → do not estimate it;
- progression/provider state unavailable → do not inspect internal storage or guess;
- optional provider bridge incompatible → disable only that detail section;
- stale inspected spell → reconcile/clear presentation only;
- malformed optional detail metadata → drop/fallback without invalidating the spell or cast path.

Fail-closed here means withholding unsupported presentation claims. It must not block a legitimate server cast merely because optional inspection data is missing.

---

## 24. Non-goals

05.14 does not authorize:

- a permanent spell encyclopedia overlay;
- a second mana/resource bar;
- client-authoritative affordability/readiness;
- client-side damage/effect formula reconstruction;
- local target-validity/world-safety decisions;
- per-hover server dossiers;
- arbitrary metadata maps or executable descriptions;
- provider private-class reflection/scraping;
- copying provider descriptions/tooltips/assets;
- a second loadout persistence model;
- a second cast path from inspection;
- automatic casting on hover/focus/details activation;
- exposing current Corruption/Strain without separate approval;
- treating server runtime fields as client presentation data by default.

---

## 25. Exit criteria for this planning artifact

05.14 planning is complete when it provides a future implementation with an unambiguous answer to:

1. what detail is currently safe to show;
2. what data requires a new server/provider presentation contract;
3. which Stage 05 plan owns each adjacent semantic;
4. how static and dynamic information stay distinct;
5. how inspection remains low-clutter, bounded and accessible;
6. how provider/world/target authority remains server/provider-owned;
7. how missing information fails closed;
8. how implementation and real-client evidence will be validated.

Creating/merging this document does **not** implement spell details and does not move Stage 05 out of `IMPLEMENTED / FINAL VALIDATION DEFERRED`.
