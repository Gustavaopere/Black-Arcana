# 05.06 — Modpack Casting-Surface Coexistence

## State

`PLANNING / NO RUNTIME CHANGE / REAL-PACK VALIDATION DEFERRED`

This plan defines how Black Arcana Casting & UX coexists with other installed casting, HUD, combat-animation and keybinding surfaces without duplicating their authority or inventing unsupported integrations.

Baseline used for this plan: `main@acbea2c897805e0d51476360c27adfd20fabfc64`.

## 1. Why this plan exists

Black Arcana does not run in an empty client. The current physical modpack already contains other systems that present spells, cooldowns, mana, hotkeys, combat state and keybinding search.

A technically correct Black Arcana HUD can still be poor UX if it:

- covers another action bar;
- duplicates an external provider's mana/cooldown information;
- steals common combat keys;
- breaks during Epic Fight battle-mode transitions;
- assumes an input provider that is not installed;
- treats a visual compatibility addon as a gameplay bridge.

This document therefore treats **coexistence** as a Stage 05 planning concern while preserving Black Arcana's own server-authoritative cast runtime.

## 2. Current physical modlist facts

The current `modlist(1).txt` confirms these relevant top-level components:

| Component | Mod ID | Installed version | Relevant surface |
|---|---|---:|---|
| Black Arcana | project-owned | current `main` | own radial/loadout/contextual HUD and canonical cast runtime |
| Iron's Spells 'n Spellbooks | `irons_spellbooks` | `1.21.1-3.16.3` | external spell/resource/casting provider and supported host for the current Black Arcana integration probe |
| Spell Actionbar | `spell_actionbar` | `1.1.4` | external spell action-bar UI |
| Epic Fight | `epicfight` | `21.17.3.1` | combat/battle-mode/input/animation environment |
| Epic Fight & Iron's Spellbook animation compat | `efiscompat` | `3.1.0` | Iron's↔Epic Fight animation compatibility |
| Controlling | `controlling` | `19.0.5` | keybinding discovery/search/conflict UX |

The physical modlist does **not** currently show a confirmed top-level general controller framework such as Controlify, Controllable or MidnightControls.

These facts establish presence/version only. They do not by themselves establish a public integration API.

## 3. Guide-derived UX context

The current project Gameplay/Systems guide describes Spell Actionbar as an Iron's-facing action bar above the hotbar that presents spell icons, cooldowns, mana and keybinds. It also describes EFIS Compat as adapting Iron's casting/actions to Epic Fight animation/battle-mode presentation.

Those guide descriptions are design/context evidence, not proof of exact Java hooks for the installed versions.

Therefore this Stage 05 plan may define coexistence behavior and test requirements, but any **new** direct technical bridge still requires exact-version API/source verification before code is written.

## 4. Authority boundaries

### 4.1 Black Arcana

Black Arcana remains authority for:

- its canonical cast pipeline;
- Black Arcana loadouts;
- Black Arcana cooldown/charge/session state;
- Black Arcana targeting admission;
- Black Arcana Arcane Danger, Corruption and Strain;
- Black Arcana world-effect safety;
- Black Arcana client presentation derived from its own server-authored state;
- validation, transactional cost settlement and cooldown of a **Black Arcana-owned spell even when Iron's hosts its registry/presentation/invocation surface**.

### 4.2 External providers

External mods remain authority for their own provider-owned state, including their own:

- spell lists;
- spellbooks/action bars;
- mana/resource storage and rules for provider-owned spells;
- provider-owned cooldowns;
- combat-mode state;
- animation systems;
- keybinding settings.

This boundary must be applied per spell/operation, not merely per screen or host mod.

For a Black Arcana-owned spell hosted by Iron's, Iron's may own the supported registry/presentation/invocation surface while Black Arcana remains the sole authority for the Black Arcana cast transaction. The host must not re-settle the same cost or cooldown.

Black Arcana must not mirror, mutate or reinterpret unrelated external-provider state merely because it is visible on the same screen.

## 5. Default coexistence strategy

Default policy is **side-by-side coexistence, not forced unification**.

Black Arcana should:

- keep its contextual HUD transient;
- keep direct quick-cast mappings unbound by default;
- retain a configurable HUD anchor/scale;
- avoid a permanent resource bar;
- avoid taking ownership of unrelated external action bars;
- use standard Minecraft key mappings so external key-management tools can discover them;
- suppress direct cast input while another normal `Screen` owns focus;
- fail closed when an optional integration is absent or incompatible.

No external UI mod is required for Black Arcana core casting.

The existing supported Iron-hosted Black Arcana probe is a separate already-implemented integration surface and must be validated rather than treated as hypothetical future work.

## 6. Spell Actionbar coexistence

### 6.1 Current disposition

`spell_actionbar 1.1.4` is installed and is an external casting UI surface.

Black Arcana does **not** currently claim a direct Spell Actionbar-specific integration from this plan alone. Whether the already Iron-registered Black Arcana probe is surfaced by that action bar is a real-client observation, not an assumption.

### 6.2 Deduplication rule

Black Arcana must not add a second persistent panel that reproduces Spell Actionbar's provider-owned information for Iron's-owned spells.

In particular, Black Arcana should not mirror unrelated external-provider:

- mana bars;
- provider spell slots;
- external-provider cooldown wheels/bars;
- provider key labels;
- provider spellbook progression.

Black Arcana may still show a concise **Black Arcana-authored** denial/risk/context line when a Black Arcana cast operation requires it, including when the invocation was hosted by Iron's.

### 6.3 Future bridge rule

If a future requirement asks for deeper Black Arcana-specific Spell Actionbar behavior beyond whatever naturally results from the verified Iron's registration surface:

1. verify exact `spell_actionbar 1.1.4` API/source/docs;
2. verify whether it exposes a supported third-party registration/presentation boundary;
3. decide which system owns selection/loadout identity;
4. preserve the canonical Black Arcana server cast pipeline;
5. prevent double-cast/double-cost/double-cooldown processing;
6. preserve Black Arcana hazard feedback even if selection occurs through another UI;
7. fail closed if the provider cannot preserve Black Arcana spell identity and authority.

Without a verified safe seam, deeper integration is rejected and the UIs remain separate.

## 7. Iron's Spells coexistence

Iron's `1.21.1-3.16.3` is an external magic provider with its own spell/resource semantics **and** an already-used supported host surface for one current Black Arcana integration spell.

### 7.1 Verified current Black Arcana-hosted route

Current `main` contains a concrete integration that this plan must not describe as future-only:

- `IronsSpellRegistryBridge` registers `black_arcana:irons_integration_probe` into Iron's supported spell registry;
- `IronsArcanaProbeSpell.onCast` dispatches the invocation back into the Black Arcana hosted-cast dispatcher;
- the source-level contract states: **Iron's owns presentation and invocation; Black Arcana owns validation, cost transaction and cooldown**;
- `IronsHostedSpellEvents` sets Iron's native mana cost to zero at high and low event priority for Black Arcana-hosted spell IDs so provider-native deduction cannot charge the same Black Arcana transaction a second time.

This is current implemented runtime evidence. It does not imply that every future Black Arcana spell should be hosted in Iron's.

### 7.2 Authority distinction

For **Iron's-owned spells**:

- Iron's owns its resource/cooldown semantics unless a verified adapter contract states otherwise;
- Black Arcana must not duplicate provider settlement.

For **Black Arcana-owned spells hosted by Iron's**:

- Iron's owns the supported registration/presentation/invocation host surface;
- Black Arcana owns cast validation, the canonical transactional `CostProvider` settlement and Black Arcana cooldown;
- Iron's native charge for that hosted Black Arcana transaction remains neutralized as required by the current runtime contract;
- compatibility work must preserve exactly-once settlement rather than “restoring” a second native Iron's charge/cooldown.

### 7.3 Stage 05 UX rules

- do not create a second Iron's mana bar;
- do not copy Iron's spellbook/actionbar slot model into Black Arcana;
- do not derive external-provider spell legality client-side;
- provider-specific cost preview is shown only through a real server/provider presentation contract;
- Black Arcana direct invocation surfaces may coexist with the already-implemented Iron-hosted Black Arcana route;
- one physical/provider invocation must result in one canonical Black Arcana root cast and one Black Arcana cost/cooldown settlement;
- never allow both Iron's native settlement and Black Arcana settlement to debit the same hosted Black Arcana cast.

The existence of Iron's UI does not transfer Black Arcana spell runtime ownership to Iron's.

### 7.4 Required real-client hosted-spell observation

Stage 05 current-pack coexistence validation must exercise the existing `black_arcana:irons_integration_probe` through the real Iron's-hosted player-facing invocation path available in the exact test pack.

Record:

- how the hosted spell is surfaced/equipped by the installed Iron's UI in the real pack;
- one successful invocation through that host surface;
- one legitimate denied invocation where a Black Arcana denial can be exercised without changing production semantics;
- whether one host action produces exactly one Black Arcana cast result/root action;
- whether Black Arcana transactional cost is settled exactly once;
- whether Iron's native mana is **not** additionally deducted for the Black Arcana-hosted transaction;
- whether Black Arcana cooldown is applied exactly once;
- whether the resulting Black Arcana feedback remains readable with Spell Actionbar visible when applicable;
- repeat the hosted invocation while Epic Fight battle mode is active when the real installed UI permits that flow.

If the exact real pack cannot legitimately surface/equip the probe without debug-only or production-semantic changes, mark that scenario `BLOCKED` with the concrete reason rather than claiming PASS.

## 8. Epic Fight coexistence

### 8.1 Current evidence

The current repository search did not identify a Black Arcana-owned direct `epicfight` integration surface.

The installed `efiscompat 3.1.0` is specifically an Epic Fight & Iron's Spellbook compatibility component. Its presence does **not** prove that Black Arcana casting is automatically animation-compatible with Epic Fight.

The existing Black Arcana spell hosted by Iron's still needs black-box testing under battle mode because Iron's hosting and EFIS presence do not by themselves prove correct Black Arcana transaction/input behavior.

### 8.2 Planning rule

Until a real Black Arcana↔Epic Fight hook is verified:

- do not invent battle-mode APIs;
- do not infer animation locks or cast windows;
- do not route Black Arcana legality through Epic Fight client state;
- test Black Arcana key/radial/HUD behavior while Epic Fight battle mode is active;
- test the existing Iron-hosted Black Arcana probe under battle mode when the host UI permits it;
- classify visual/animation incompatibility separately from server cast authority;
- if a direct integration becomes necessary, audit exact Epic Fight `21.17.3.1` API/source/docs first.

### 8.3 Required black-box coexistence observations

Real-client validation should record at minimum:

- radial open/close while out of battle mode;
- radial open/close while battle mode is active;
- selected cast while battle mode is active;
- quick-cast input while battle mode is active;
- current Iron-hosted Black Arcana probe invocation while battle mode is active when legitimate;
- no stuck mouse/key state after radial close;
- no duplicate cast from one physical/provider input;
- no client crash from animation/state transitions;
- Black Arcana denial/result HUD remains readable during normal combat presentation.

A cosmetic animation mismatch does not justify weakening server cast authority.

## 9. Controlling coexistence

`controlling 19.0.5` is present and can improve the user's ability to search/discover key mappings.

Black Arcana policy:

- continue registering ordinary Minecraft `KeyMapping`s;
- do not add a hard dependency on Controlling;
- do not call Controlling-specific APIs merely for ordinary binding registration;
- ensure Black Arcana category/name translations remain clear enough to be searchable;
- keep optional quick-cast mappings unbound by default;
- never rewrite another mod's binding automatically.

If Controlling is absent, Black Arcana must remain fully configurable through the normal controls screen.

## 10. Controller/gamepad boundary

No general controller framework is confirmed in the current physical modlist.

Therefore:

- keyboard/mouse is the guaranteed Stage 05 input baseline;
- gamepad-specific integration is not a current completion requirement;
- no speculative controller classes, events or button identifiers are authorized;
- if a controller provider is later installed, exact presence/version/API is verified first;
- any controller action maps to the existing client intent layer and canonical server pipeline;
- provider absence must leave keyboard/mouse unaffected.

## 11. HUD overlap plan

### 11.1 Principle

The Black Arcana HUD is contextual specifically to reduce collision with permanent provider/action bars.

### 11.2 Required coexistence checks

In the real current pack, observe Black Arcana contextual HUD together with the installed external casting UI at:

- 854×480;
- 1920×1080;
- 3440×1440;
- GUI scale Auto/2/3/4 where supported;
- each Black Arcana HUD anchor;
- HUD scale 0.5×/1×/2×.

Record whether:

- Black Arcana covers the external action bar;
- external UI covers Black Arcana denial/danger text;
- hotbar/actionbar readability is reduced materially;
- tooltips obscure interactive Black Arcana controls;
- F1/hidden GUI behavior is coherent across both systems.

### 11.3 Conflict resolution order

If an overlap is confirmed:

1. prefer moving/rescaling Black Arcana through its existing configurable anchor/scale;
2. prefer reducing transient density/line count;
3. add a Black Arcana layout reservation/avoidance mechanism only when a supported boundary exists;
4. do not patch another mod's renderer through brittle mixins merely to obtain a preferred layout;
5. if no safe automatic coexistence exists, document a recommended Black Arcana client anchor rather than silently altering external config.

## 12. Keybinding conflict plan

### Current Black Arcana defaults

- radial: `R`;
- selected cast: `V`;
- loadout editor: unbound;
- eight quick-cast mappings: unbound.

### Required real-pack audit

Use the actual installed client and its current keymap to verify:

- whether `R` conflicts with a gameplay-critical installed action;
- whether `V` conflicts with a gameplay-critical installed action;
- whether Controlling correctly discovers Black Arcana mappings;
- whether rebinds remain functional after restart;
- whether Battle Mode changes key handling unexpectedly;
- whether duplicate physical bindings cause one or more cast-intent emissions.

Do not change default keys from static modlist inference alone. Any default-key change requires direct current-pack evidence and a migration/rebind note.

## 13. Provider invocation surfaces

D005 allows books, weapons, staves and other surfaces to coexist with direct keybind casting.

### 13.1 Existing Iron-hosted surface

The Iron-hosted integration probe described in 7.1 is already implemented and is a required Stage 05 coexistence validation target. Its contract must be preserved rather than re-designed as though it were hypothetical.

### 13.2 Any future external invocation surface

For every **new** external invocation surface, the planning checklist is:

1. identify the provider that owns the item/action/host surface;
2. verify an exact-version supported event/API boundary;
3. establish whether the spell/operation itself is provider-owned or Black Arcana-owned;
4. convert the provider action into one bounded Black Arcana cast intent/reference where Black Arcana owns the operation;
5. preserve one canonical `ArcanaCastId` root;
6. reserve/commit costs exactly once under the spell operation's canonical authority;
7. preserve server targeting and canonical cooldown ownership;
8. avoid provider-native cast/settlement plus Black Arcana cast/settlement both firing for one Black Arcana-owned action;
9. define recursion/deduplication protection;
10. define fallback when the provider is absent;
11. test dedicated-server classloading and optional-dependency failure.

No thematic similarity is enough to create a new bridge.

## 14. Coexistence test matrix

| Surface | Test | Expected |
|---|---|---|
| Iron's hosted Black Arcana | invoke `black_arcana:irons_integration_probe` through the real Iron's host UI | one Black Arcana cast/result; Black Arcana validates and settles its transaction exactly once |
| Iron's hosted Black Arcana | inspect resource settlement | Black Arcana transactional cost settles once; Iron's native mana is not additionally charged for the hosted Black Arcana cast |
| Iron's hosted Black Arcana | inspect cooldown/result settlement | Black Arcana cooldown/result occurs once; no duplicate provider-native settlement |
| Iron's hosted Black Arcana | host invocation + Epic Fight battle mode when legitimate | no duplicate cast/cost/cooldown, stuck input or crash |
| Spell Actionbar | external action bar visible + BA idle | BA adds no permanent duplicate resource/action bar |
| Spell Actionbar | external action bar visible + BA denial | bounded BA denial remains readable without taking unrelated provider authority |
| Spell Actionbar | external action bar visible + BA dangerous selection | hazard/gate context is readable and transient |
| Epic Fight | battle mode + radial | radial behaves predictably; no stuck input/crash |
| Epic Fight | battle mode + selected cast | one physical input produces at most one BA cast intent |
| Epic Fight | battle mode + quick cast | no duplicate cast/cost/cooldown processing |
| Controlling | search BA category/actions | mappings are discoverable through standard key mapping registration |
| Vanilla controls | Controlling absent/ignored | BA mappings remain rebindable without external helper |
| HUD | all required resolutions/scales | BA contextual layer remains bounded with existing pack UI |
| F1 | hide GUI | BA follows the intended vanilla client visibility behavior |
| Reconnect | external UIs active | stale BA state does not flash as authority |

These rows are planning targets. They become PASS only through direct real-client evidence.

Because `05-final-client-validation-handoff.md` Task 5A delegates current-pack coexistence requirements to this plan, the four Iron-hosted rows above are **required current-runtime coexistence scenarios**, not optional future-polish rows.

## 15. What counts as a blocker

### Stage 05 blocker

- one physical/provider input can trigger duplicate Black Arcana casts;
- a Black Arcana-hosted spell is charged by both Black Arcana and Iron's native settlement;
- a Black Arcana-hosted spell receives duplicate Black Arcana/provider cooldown settlement;
- an installed current-pack UI makes Black Arcana's required denial/danger information unusable with no safe configuration;
- battle-mode transition causes stuck input/crash in ordinary supported casting flow;
- external UI/input state bypasses server cast authority;
- required core key action cannot be rebound or used in the current pack.

### Optional follow-up

- cosmetic animation mismatch with no gameplay/input breakage;
- preference for deeper visual unification with Spell Actionbar;
- controller integration while no controller provider is installed;
- provider-specific icon/theme polish;
- automatic HUD avoidance when manual Black Arcana anchoring already resolves the collision safely.

## 16. Implementation rule

This plan does not authorize proactive compatibility code merely because the mods are installed.

Compatibility code is written only when:

1. direct evidence demonstrates a real conflict or an explicitly approved UX requirement needs a bridge;
2. exact provider API/source/docs are verified for any **new** seam;
3. the boundary preserves causal identity and exactly-once processing;
4. spell-operation authority is preserved even when another provider hosts presentation/invocation;
5. the integration can fail safely;
6. regression tests and real-client coexistence evidence are defined before merge.

The already-implemented Iron-hosted probe is tested against its current verified contract; it is not reclassified as a hypothetical future bridge.

Otherwise, keep systems separate and test them together.

## 17. Exit criteria

05.06 planning is satisfied when:

- the relevant installed casting/input/combat UI surfaces are explicitly listed with current versions;
- the existing Iron-hosted Black Arcana route and its transaction authority are accurately documented;
- authority and deduplication rules are documented per spell/operation rather than inferred from the host UI;
- the exact-version API verification gate is explicit for any future/new bridge;
- real-pack coexistence scenarios include the already-implemented hosted spell route;
- controller support is correctly optional while no provider exists;
- no unsupported integration is presented as implemented.

Runtime coexistence is only validated when the corresponding real-client/current-pack observations are executed and recorded.
