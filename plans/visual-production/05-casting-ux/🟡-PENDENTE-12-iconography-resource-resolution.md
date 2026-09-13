# 05.12 — Iconography & Resource Resolution

## State

`PLANNING / NO RUNTIME CHANGE / CLIENT RESOURCE PRESENTATION HARDENING`

This document defines the canonical Stage 05 plan for resolving synchronized spell icon presentation safely across Black Arcana client surfaces.

Baseline used for this audit: `main@48cb9a430e0526899e8ae1588283b31de71cadfb`.

This is a planning artifact only. It does **not** add Java runtime behavior, resource reload listeners, texture files, icons, packets, protocol fields, provider bridges, cache implementations or third-party assets.

---

## 1. Why this plan exists

Stage 05 has intentionally carried icon rendering as a future refinement since the first UX plans.

The server already synchronizes an `iconId` alongside each spell's canonical presentation identity, while the current loadout editor, radial wheel and contextual HUD still render spell identity through text/translation data.

That leaves a real implementation gap between:

- **data authority** — already covered by `07-presentation-data-contracts.md`;
- **visual semantics** — already covered by `08-visual-language-state-semantics.md`;
- **surface-specific placement** — already described at a high level in `02-radial-wheel.md`, `03-contextual-hud.md` and `10-loadout-editor-information-architecture.md`;
- **actual resource resolution lifecycle** — not yet frozen as one common contract.

05.12 defines that missing layer.

Its purpose is to prevent future icon work from becoming three independent screen-specific implementations with different fallback, namespace, reload, cache, provenance or failure behavior.

---

## 2. Current verified runtime facts

### 2.1 Presentation payload already carries icon identity

Current `SpellPresentationPayload.Entry` contains exactly:

- `spellId`;
- `translationKey`;
- `iconId`.

The payload constructor currently requires `iconId` to be:

- non-null;
- non-blank;
- no longer than `ArcanaProtocol.MAX_ICON_ID_LENGTH`.

Important boundary:

**the current payload validates bounded text, but it does not parse `iconId` as a Minecraft `ResourceLocation`.**

Therefore a future renderer must not treat successful packet construction as proof that the referenced client resource is syntactically valid or physically present.

### 2.2 Current radial does not consume `iconId`

`BlackArcanaRadialScreen` currently stores synchronized `SpellPresentationPayload.Entry` records, but spell rendering uses:

- slot number;
- translated display name;
- text fallback from the canonical spell path;
- selected/hovered card colors;
- hazard/preflight text.

The current class does not call `entry.iconId()` and does not render a spell texture.

### 2.3 Current loadout editor does not consume `iconId`

`BlackArcanaLoadoutScreen` likewise receives the presentation map, but current rows render:

- `[x]` / `[ ]` draft-membership prefix;
- translated display name or spell-path fallback;
- hazard tooltip where relevant.

The current class does not call `entry.iconId()` and does not render a spell texture.

### 2.4 Current contextual HUD does not consume `iconId`

`BlackArcanaHudLayer` currently resolves selected spell text from `translationKey` or spell-path fallback.

Its current rendering is text-panel based and does not consume `iconId`.

05.12 does not require the HUD to gain an icon merely because radial/editor may do so. HUD density remains governed by 05.03 and transient priority by 05.11.

### 2.5 Current Black Arcana asset tree has no spell-icon textures

At baseline `48cb9a43...`, `src/main/resources/assets/black_arcana/` contains only:

- `lang/`.

There is no `textures/` child in that current Black Arcana asset root.

This proves only the current repository state. It does **not** mean future spell icons must live under one exact directory convention, and it does not authorize copying provider artwork to fill the gap.

### 2.6 No current shared icon-resource resolver is established

Current code inspection finds no Stage 05 consumer of `iconId()` and no repository code-search hit for a `ResourceManager`-based icon resolution layer.

Therefore 05.12 plans the behavior contract before any concrete resolver/cache class is introduced.

No class name, method signature or reload-listener implementation is assumed by this document.

---

## 3. Relationship to other Stage 05 plans

05.12 is deliberately narrow.

### `05.07 — Presentation Data Contracts`

05.07 decides whether a datum is legitimate to present.

For spell icon identity, current conclusion remains:

- `iconId` is already synchronized through a bounded server-authored presentation payload;
- no new gameplay-state synchronization is required merely to render that icon identity.

05.12 does not reopen that authority decision.

### `05.08 — Visual Language & State Semantics`

05.08 decides what missing art means.

Canonical rule preserved here:

`MISSING ART = PRESENTATION_FALLBACK`

It must never mean:

- spell unavailable;
- spell denied;
- spell unregistered;
- cooldown;
- provider missing;
- progression blocked.

### `05.02 — Radial Wheel`

05.02 remains authority for:

- radial geometry;
- eight visible slots per page;
- compact-mode behavior;
- selection/cast separation;
- paging and hit regions.

05.12 only defines how a spell icon may be resolved and degraded inside that existing layout.

### `05.03 — Contextual HUD`

05.03 remains authority for:

- whether an icon belongs in the HUD at all;
- anti-clutter behavior;
- density and layout;
- denial/danger readability.

05.12 does not mandate HUD iconography.

### `05.10 — Loadout Editor Information Architecture`

05.10 remains authority for:

- dense ordered loadout semantics;
- catalog/search/order behavior;
- draft state;
- apply/reconciliation semantics.

05.12 defines only the icon-resolution part of the already-planned icon presentation.

### `05.11 — Contextual Feedback Orchestration`

05.11 remains authority for transient selection/result/forecast arbitration.

An icon must never be used to create a false result-to-spell association that 05.11 forbids.

---

## 4. Authority model

### 4.1 Canonical spell identity

The canonical spell identity remains the synchronized/canonical spell ID.

An icon is not identity authority.

The client must never derive or replace canonical spell identity from:

- icon filename;
- icon namespace;
- texture folder;
- provider logo;
- translation key;
- visual similarity.

### 4.2 `iconId` authority

A synchronized `iconId` means only:

> the server-authored presentation contract recommends this resource identifier for the spell's client presentation.

It does not prove:

- that the resource exists in the active client resource stack;
- that the resource belongs to Black Arcana;
- that the resource may legally be redistributed;
- that a third-party provider API exists;
- that the spell uses the resource's namespace as its gameplay provider;
- that resource-pack overrides preserve the original art.

### 4.3 Resource availability is client presentation state

Actual resource availability is determined by the current client resource stack.

Failure to resolve artwork is a client presentation problem only.

It must not send:

- cast packets;
- loadout changes;
- provider queries;
- progression changes;
- server denial events.

---

## 5. Canonical resource-resolution pipeline

Future implementation should conceptually follow one shared resolution policy.

This is a behavior contract, not a required class design.

### Step 1 — obtain the synchronized presentation entry

For the canonical spell ID, read the current synchronized `SpellPresentationPayload.Entry`.

If the entry is absent:

- use existing spell-name/canonical-ID fallback behavior;
- no icon resolution is attempted;
- spell gameplay state is unchanged.

### Step 2 — parse `iconId` safely

Because the current payload bounds the string but does not parse it as a resource location, client presentation must validate/parse it using supported Minecraft resource-identifier semantics before lookup.

If parsing fails:

- classify as `PRESENTATION_FALLBACK`;
- do not throw out of the screen/HUD render path;
- do not invent another path from the spell ID;
- do not log the same malformed value every frame.

### Step 3 — resolve through the normal client resource system

A valid resource identifier may be looked up only through supported Minecraft/NeoForge client resource mechanisms.

Do not resolve icon IDs through:

- arbitrary filesystem paths;
- HTTP/HTTPS URLs;
- remote downloads;
- classpath guesses outside the normal resource contract;
- provider JAR introspection during render;
- world scans.

### Step 4 — produce one of two presentation outcomes

Conceptual result:

#### `RESOLVED`

The active client resource stack can provide the referenced icon for presentation.

#### `FALLBACK`

The icon cannot be parsed or resolved safely.

Fallback retains:

- canonical spell ID;
- synchronized translated name where available;
- current gameplay state.

These names are conceptual only. No enum/class is created by this plan.

---

## 6. No spell-ID-to-texture heuristic

05.12 explicitly forbids inventing a texture path from the spell ID when synchronized icon resolution fails.

Forbidden examples include conceptual assumptions such as:

- `spell namespace + /textures/spell/ + spell path`;
- replacing underscores with folder separators;
- assuming all Black Arcana spells live under one generated icon directory;
- assuming external-provider spells expose their icon under their spell registry path.

Reasons:

1. the server already supplied an explicit presentation identifier;
2. provider resource layouts are not interoperability contracts;
3. path heuristics make missing art look accidentally successful;
4. heuristics become hidden provider coupling;
5. a wrong but existing texture is worse than an explicit text fallback.

Unknown beats guess.

---

## 7. Namespace policy

A parsed `iconId` may use a namespace other than `black_arcana`.

Namespace alone does not establish authority or licensing.

### 7.1 Black Arcana namespace

For project-owned icon resources:

- assets should be original Black Arcana work or otherwise have compatible documented provenance;
- final resource path conventions should be chosen during implementation/art production and then kept stable;
- resource-pack overrides remain presentation-only.

### 7.2 External namespace

If the synchronized contract points to another installed namespace and the ordinary client resource stack can resolve it:

- Black Arcana may present the referenced live resource only if the implementation uses the normal runtime resource system;
- Black Arcana does not copy that asset into its own resources merely for convenience;
- namespace presence is not evidence of a supported provider API;
- disappearing provider/resource content must degrade to fallback safely.

### 7.3 No namespace inference

Do not infer provider/domain/school from `iconId` namespace.

05.10 already forbids using icon paths as provider metadata.

That remains canonical.

---

## 8. Clean-room and provenance rules

`SOURCES.md` explicitly states that a public repository, documentation page, installed JAR, observable mechanic or build dependency is not permission to copy implementation or assets.

05.12 applies that rule directly to iconography.

### 8.1 Preferred asset posture

Preferred order for Black Arcana-owned visual identity:

1. original project-owned artwork;
2. commissioned/user-provided artwork with explicit rights compatible with distribution;
3. third-party artwork only after exact license/permission and notice obligations are verified and recorded.

### 8.2 Provider artwork

Do not copy, recolor, crop, trace, redraw or redistribute provider-owned spell icons merely because:

- the provider is installed;
- Black Arcana interoperates with it;
- a synchronized `iconId` references its namespace;
- a screenshot reveals the icon;
- a source repository is public.

Any actual derivation requires a separate provenance/license review.

### 8.3 Runtime reference is not redistribution

Using an already-present resource through the active client resource system is distinct from bundling a copy of that asset inside Black Arcana.

05.12 plans no redistribution of third-party artwork.

### 8.4 Release documentation

Before shipping any non-original asset, review/update as applicable:

- `SOURCES.md`;
- `THIRD_PARTY_NOTICES.md`;
- `plans/09-hardening-release/06-provenance-license.md`;
- any project asset-provenance record adopted by the implementation/art workflow.

---

## 9. Fallback semantics

Fallback is a first-class presentation state, not an error state.

### 9.1 Spell name remains available

A missing icon should preserve the existing text path:

1. synchronized translated display name where available;
2. existing canonical spell-path text fallback where presentation entry/name cannot be used safely.

### 9.2 No fake unavailable state

A missing icon must not cause:

- disabled row styling by itself;
- blocked/denied semantic symbol;
- red error state that can be confused with gameplay denial;
- removal from radial/loadout catalog;
- replacement of canonical spell identity.

### 9.3 Missing icon and missing translation are independent

A spell may have:

- valid icon + valid translation;
- missing icon + valid translation;
- valid icon + missing translation/fallback text;
- both presentation fallbacks.

These states must remain independent from gameplay availability.

### 9.4 Fallback must remain usable at all GUI scales

A failed icon cannot consume layout space in a way that destroys the existing text-only fallback.

The current text-only implementation is the compatibility baseline.

---

## 10. Resource reload lifecycle

Minecraft resource state can change while the client remains connected.

Examples include:

- resource-pack reload;
- language/resource reload;
- development resource refresh;
- pack enable/disable before reconnect where supported.

Any future icon-resolution cache must therefore define reload invalidation.

### 10.1 Canonical rule

After a resource reload, prior positive **and negative** icon-resolution assumptions are stale until re-evaluated against the new resource state.

### 10.2 Negative-cache consequence

If an implementation caches “icon missing”, that cache must not survive a resource reload blindly.

A newly enabled resource pack may make the previously missing identifier resolvable.

### 10.3 Positive-cache consequence

Likewise, a previously resolved icon may disappear or change after reload.

Do not retain a direct stale texture/resource handle across reload unless the supported client API explicitly makes that handle reload-safe.

### 10.4 No gameplay reset

Resource reload must not:

- clear the server-owned loadout;
- alter selected canonical spell identity unnecessarily;
- send loadout/cast requests;
- reset cost/cooldown/progression;
- mutate provider state.

Only presentation resource state is invalidated.

---

## 11. Server presentation refresh lifecycle

Resource reload and server presentation refresh are distinct events.

If a newer `SpellPresentationPayload` changes a spell's `iconId`:

- the newest accepted presentation snapshot becomes the presentation source;
- any cached resolution associated with the old `(spellId, iconId)` pair becomes stale for that spell;
- no gameplay registry identity changes merely because artwork changes.

A safe implementation should key presentation resolution strongly enough that stale art is not retained after the synchronized icon identifier changes.

This does not require a protocol extension.

---

## 12. Disconnect/session lifecycle

Client icon-resolution state may be reusable across sessions only where it is purely resource-derived and safely keyed.

Spell-to-icon presentation association, however, comes from the synchronized server presentation snapshot.

Therefore:

- disconnect clears/replaces synchronized spell presentation through the existing client sync lifecycle;
- no old server's spell→icon association may be treated as current authority after joining another session;
- pure resource existence caches, if retained at all, still need resource-reload invalidation;
- safest initial implementation is bounded/simple rather than building a long-lived global cache before profiling proves a need.

---

## 13. Cache and performance policy

The icon layer must not turn render into I/O-heavy work.

### 13.1 No render-path scans

Never perform during each frame:

- filesystem traversal;
- JAR traversal;
- namespace enumeration;
- provider registry discovery;
- world/entity/chunk scans;
- network requests.

### 13.2 Bounded resolution

The current Stage 05 surfaces are already bounded:

- radial: at most 8 visible entries per page;
- canonical loadout: at most 16 entries;
- presentation payload: bounded by `MAX_PRESENTATION_ENTRIES`.

Use those bounds rather than building an unbounded global icon registry.

### 13.3 Cache only when it improves evidence-backed performance

A cache is permitted, not mandated.

If introduced, it must define:

- key;
- maximum/bounded growth behavior;
- positive result semantics;
- negative result semantics;
- resource-reload invalidation;
- presentation-snapshot invalidation where needed;
- thread/client lifecycle ownership.

### 13.4 No log spam

Malformed/missing icon resources must not emit repeated errors every render frame.

Diagnostics, if implemented, should be deduplicated/bounded and should not turn optional missing art into a runtime failure.

---

## 14. Radial presentation contract

05.02 remains geometry authority.

Once icon resolution is implemented, normal radial cards may use:

- resolved spell icon;
- slot number;
- short translated spell name;
- selected/hover/focus semantics from 05.08/05.09;
- hazard marker where already authorized.

### 14.1 Normal viewport

Preferred hierarchy:

1. icon when resolved;
2. slot identity;
3. short name where space allows.

The icon must not reduce hit-region correctness.

### 14.2 Compact viewport

Compact mode may prioritize:

- slot number;
- small resolved icon where readable;
- focused tooltip/name.

If the icon cannot remain legible, the existing slot-number + tooltip fallback remains valid.

### 14.3 Missing icon

The radial must remain fully selectable/paged/cast-independent when every icon is missing.

The text-only current behavior is the minimum safe fallback.

---

## 15. Loadout editor presentation contract

05.10 remains information-architecture authority.

A future editor row/catalog card may use:

- resolved spell icon;
- synchronized display name;
- canonical slot/order information;
- draft-membership state;
- quick-cast-eligibility marker where applicable.

### 15.1 Search remains text/identity based

Do not make icon existence or icon filename a searchable provider/domain classification field.

Search remains based on legitimate synchronized identity/name fields defined by 05.10.

### 15.2 Missing art does not affect draft operations

Toggle, reorder, clear, reset, apply and cancel behavior must be identical whether an icon resolves or not.

### 15.3 Layout reserve

If rows reserve fixed icon space, unresolved icons must use a neutral presentation fallback or allow text to occupy the area without changing row semantics unpredictably.

Exact pixel values are deferred to implementation/real-client validation.

---

## 16. Contextual HUD presentation contract

An icon in `BlackArcanaHudLayer` remains optional.

05.03 and 05.11 take priority over decorative spell identity.

If future HUD implementation includes a resolved icon:

- authoritative denial remains higher-priority content;
- danger/gate information remains readable;
- the icon must not create false result-to-selection association;
- a result-only event with no safely correlated spell identity must not borrow the current selection icon;
- missing icon must never suppress the text result.

If these conditions cannot fit a compact HUD, omit the icon.

---

## 17. Resource-pack compatibility

Resource packs may legitimately replace compatible client resources.

05.12 treats that as presentation customization.

Rules:

- resource-pack override may change appearance, not gameplay meaning;
- a pack cannot change canonical spell ID, cost, cooldown, hazard or cast result through icon art;
- missing override falls through according to the normal resource stack;
- reload must refresh resolution assumptions;
- alternate art must still leave essential states readable through non-icon cues.

Do not create a Black Arcana gameplay trust decision from who supplied the final resource.

---

## 18. Accessibility rules

Spell icons are supplemental identity cues.

They must not become the sole carrier of essential state.

### Required redundancy

Where a spell must be identified reliably, preserve at least one non-icon route such as:

- translated name;
- slot number;
- canonical ID fallback in diagnostic/fallback contexts.

### Semantic state

Do not encode these solely inside spell artwork:

- selected/focused;
- blocked/denied;
- danger/warning;
- cooldown/readiness;
- unavailable preview.

Those roles belong to 05.08 semantic cues and must remain distinguishable independently of custom spell art.

### Motion

Static icon resolution does not require motion.

If animated iconography is proposed later:

- it becomes a separate presentation feature;
- reduced-motion requirements apply;
- animation cannot carry essential information alone;
- performance/reload behavior must be re-audited.

---

## 19. Provider-hosted and external UI boundary

Black Arcana-owned Stage 05 surfaces may render their synchronized icon metadata under this plan.

This does not mean Black Arcana should restyle or replace provider-owned UI.

For example:

- Iron's-hosted presentation remains provider-owned where Iron's is the host surface;
- Spell Actionbar remains an external UI surface;
- provider-specific live UI is not scraped for icon pixels;
- no external screen is monkey-patched solely to force Black Arcana iconography.

Any direct UI integration still requires the exact supported seam under 05.06/provider-specific audit.

---

## 20. Security and robustness

Icon presentation consumes data that originated from a synchronized string field.

Although bounded, it must still be treated as presentation input rather than arbitrary file access authority.

### Required safeguards

- parse only as supported Minecraft resource identifiers;
- reject/fallback on malformed identifiers;
- never interpret `iconId` as a URI;
- never concatenate it into host filesystem paths;
- never download missing icons from the network;
- never execute provider code merely to inspect artwork during render;
- keep errors bounded/non-fatal;
- preserve dedicated-server separation from client resource classes.

### Dedicated-server rule

Any implementation of icon resolution must stay physical-client-only.

The server may author the bounded icon identifier, but dedicated-server startup must not load client texture/resource-rendering classes.

---

## 21. Proposed implementation phases

This document does not implement these phases.

### Phase A — Pure resolution policy

Before screen changes:

- define the client-only parse/resolve/fallback contract;
- write deterministic tests for valid/malformed/missing identifiers where the test harness permits;
- define reload invalidation behavior;
- keep no gameplay side effects.

### Phase B — Radial consumption

- use the common resolution policy in radial cards;
- retain current text fallback;
- preserve geometry/hit regions;
- test compact/normal viewports.

### Phase C — Loadout editor consumption

- reuse the same resolution/fallback policy;
- preserve 05.10 dense-list/draft semantics;
- ensure icon failure does not affect search/order/apply.

### Phase D — HUD decision

Do not automatically implement.

First verify whether a selected-spell icon materially improves readability without increasing clutter or creating 05.11 association ambiguity.

### Phase E — Original asset production

Only if/when Black Arcana spell icons are actually authored:

- follow project art workflow;
- record provenance;
- add assets through a separately reviewed implementation/art change;
- validate at real GUI scales/resource reload.

---

## 22. TDD and automated validation plan

When implementation is approved, prefer RED → GREEN → refactor for deterministic parts.

### Pure/unit coverage

Test at minimum:

- valid synchronized icon identifier parses;
- malformed icon identifier returns fallback, not exception;
- missing resource returns fallback;
- resolved resource returns resolved presentation state;
- resource reload invalidates positive result assumptions;
- resource reload invalidates negative result assumptions;
- icon-id change for the same spell invalidates old association;
- fallback preserves canonical spell identity/name path;
- icon failure never changes loadout membership or selection state;
- repeated missing icon does not create unbounded diagnostic state if diagnostics/cache exist.

Exact test class names are intentionally not invented here.

### Screen/state coverage

Radial:

- icon-present card;
- icon-missing fallback card;
- all icons missing;
- mixed namespaces;
- compact viewport;
- page 1/page 2;
- selection still non-casting.

Loadout editor:

- icon-present row;
- icon-missing row;
- draft toggle/reorder independent of icon state;
- search independent of icon path;
- layout remains bounded.

HUD, only if implemented:

- selected icon never overrides denial priority;
- result with no safe 05.11 spell correlation does not borrow current selection icon;
- missing icon preserves result text.

### Dedicated server

Full CI must continue proving dedicated-server startup without client-class loading.

---

## 23. Real-client validation plan

Static review and automated tests cannot prove final artwork readability.

Any implemented icon pass must be directly observed at the Stage 05 matrix resolutions:

- 854×480;
- 1920×1080;
- 3440×1440;
- GUI scales Auto/2/3/4 where available.

Verify:

- icons are legible without covering names/slot identity;
- missing icons degrade cleanly;
- resource-pack reload does not leave stale/broken rendering;
- mixed resolved/fallback icons do not shift hit regions unpredictably;
- radial cards remain clickable and correctly mapped;
- editor rows remain readable;
- all-text fallback remains fully usable;
- semantic state remains readable without relying only on icon art;
- no provider HUD overlap is worsened materially;
- F1/hidden-GUI behavior remains correct for any HUD icon addition.

No row is marked PASS from source inspection or CI alone.

---

## 24. Failure handling matrix

| Condition | Required presentation behavior | Forbidden behavior |
|---|---|---|
| presentation entry absent | name/canonical fallback | invent icon path |
| `iconId` blank | should already be rejected by payload constructor; fail closed if encountered defensively | render arbitrary default as gameplay state |
| malformed resource identifier | fallback | screen crash / filesystem interpretation |
| valid id, resource absent | fallback | remove/disable spell |
| external namespace absent | fallback | install/query provider automatically |
| resource disappears after reload | invalidate/re-resolve | retain stale handle blindly |
| resource appears after reload | allow new resolution | permanent negative-cache miss |
| icon changes for same spell | newest synchronized presentation wins | persist old association indefinitely |
| missing icon during cast denial | keep denial text | hide denial |
| result has no safe spell correlation | no result icon attribution | borrow current selection icon |
| provider art license unknown | do not bundle/copy | redistribute based on presence alone |

---

## 25. Performance budgets

05.12 adds no new numeric protocol budget.

Implementation must fit within existing bounded surfaces.

Required qualitative budgets:

- no per-frame filesystem/JAR scans;
- no per-frame network traffic;
- no resource download;
- no world scan;
- no unbounded map keyed by arbitrary remote strings;
- no repeated exception path for ordinary missing art;
- no texture decoding/upload loop caused by every render frame;
- resource reload work bounded to relevant client presentation state.

If profiling shows a common resolver/cache is needed, choose the smallest lifecycle-correct design and test its invalidation explicitly.

---

## 26. Documentation and provenance gate

An implementation PR that only teaches screens to resolve already-present resources may not need a new third-party notice by itself.

An implementation/art PR that adds actual icon files must classify each new asset:

- original project-owned;
- user/commissioned with permission;
- third-party under verified compatible license;
- generated asset with documented project provenance where applicable.

Before merge, verify the repository's provenance documents reflect any material third-party reuse.

Do not postpone an unresolved asset-license question by silently shipping the file and promising Stage 09 will discover it later.

Stage 09 remains final release audit, not permission to merge knowingly unproven asset rights.

---

## 27. Non-goals

05.12 does **not** authorize or implement:

- spell icon PNGs/textures;
- final art style/palette;
- provider logos as generic Black Arcana symbols;
- copying Iron's/Ars/Mahou/other mod spell art;
- a provider-specific icon API bridge;
- new `SpellPresentationPayload` fields;
- new spell identity semantics;
- provider/domain/school inference from icon paths;
- client-authoritative availability;
- runtime downloads of icon art;
- arbitrary filesystem loading;
- an animated-icon system;
- a permanent HUD icon bar;
- a new resource/mana HUD;
- a second casting pipeline;
- any Stage 05 manual PASS.

---

## 28. Implementation gate checklist

Before any code implementing 05.12 is approved:

- [ ] latest `origin/main` fetched and recorded;
- [ ] no competing PR owns the same Stage 05 icon/resource surface;
- [ ] `SpellPresentationPayload` current schema rechecked;
- [ ] current resource identifier parsing API verified against Minecraft/NeoForge 1.21.1 rather than guessed;
- [ ] 05.07 data authority preserved;
- [ ] 05.08 fallback semantics preserved;
- [ ] 05.02 radial geometry preserved;
- [ ] 05.10 editor semantics preserved;
- [ ] 05.11 result-correlation rules preserved for any HUD icon;
- [ ] no provider-specific resource path heuristic introduced;
- [ ] resource reload invalidation designed;
- [ ] dedicated-server classloading boundary preserved;
- [ ] asset provenance reviewed for every newly bundled asset;
- [ ] RED tests added for deterministic resolution/fallback behavior;
- [ ] full CI green on reconciled exact HEAD;
- [ ] affected real-client rows rerun on exact build;
- [ ] final `main` sync repeated immediately before merge.

---

## 29. Exit criteria

05.12 planning is complete when the repository has one unambiguous contract stating that:

- `iconId` is synchronized presentation metadata, not canonical spell identity;
- current payload bounds do not prove resource syntax/existence;
- radial/editor/HUD cannot each invent independent resource-path heuristics;
- normal Minecraft client resource resolution is the only allowed resource source;
- malformed/missing resources fail to text/presentation fallback without gameplay impact;
- positive and negative resolution assumptions respect resource reload;
- synchronized icon-id changes invalidate stale presentation associations;
- provider namespaces do not transfer provider authority or redistribution permission;
- original/provenance-safe Black Arcana assets are preferred;
- missing artwork remains distinct from gameplay unavailability;
- icon rendering remains optional where it would harm HUD readability;
- implementation remains client-only, bounded and dedicated-server safe;
- no runtime, packet, provider or asset change is falsely claimed from this plan.

Creating or merging 05.12 does **not** change Stage 05 from `IMPLEMENTED / FINAL VALIDATION DEFERRED` and does not satisfy any pending manual client validation row by itself.
