# 05.15 — Casting VFX, Audio & Animation Presentation

## State

`PLANNING / NO RUNTIME CHANGE / AUDIOVISUAL CASTING PRESENTATION CONTRACT`

Baseline used for this planning audit: `main@c5c1fe1346f0e7e9e991018f62c2f2399b41075b`.

This document defines the presentation boundary for future Black Arcana casting VFX, audio, player animation, camera feedback and gameplay-relevant telegraphs.

It does **not** claim that Black Arcana currently has a generic particle engine, sound library, cast-animation controller, camera-shake system, telegraph renderer or animation-provider adapter.

It does **not** add protocol fields, assets, Java runtime, provider hooks or real-client PASS evidence by itself.

Stage 05 remains `IMPLEMENTED / FINAL VALIDATION DEFERRED` until the existing real-client acceptance campaign is actually executed. Planning this audiovisual layer does not convert any manual matrix row to PASS.

---

## 1. Why this plan exists

Stage 05 already defines:

- input/loadout semantics;
- radial selection;
- contextual HUD;
- accessibility/client configuration;
- real-pack coexistence;
- presentation-data authority;
- cross-surface visual semantics;
- keyboard focus/navigation;
- loadout-editor information architecture;
- transient feedback arbitration;
- icon/resource resolution;
- target/aim presentation;
- spell-details/inspection presentation.

What remained unspecified was the cross-cutting audiovisual lifecycle of a cast itself.

Without one canonical plan, later spell work could easily drift into incompatible patterns such as:

- playing a dramatic local animation as soon as a key is pressed and visually implying the server accepted the cast;
- spawning client-only area telegraphs that disagree with server target geometry;
- replaying provider-hosted animation, Black Arcana animation and impact audio for one physical cast;
- tying cast legality to an Epic Fight or animation-library client state;
- introducing per-spell camera hacks that conflict with FirstPerson, lock-on or Borrowed Sight;
- hiding gameplay-critical danger information when particle density is zero;
- using sound as the only denial/success carrier;
- creating unbounded particle/entity scans or per-tick network traffic for decoration;
- copying another mod's spell particles, sounds, poses or signature presentation language.

05.15 closes that architectural gap without moving per-spell audiovisual authorship out of Stage 07.

---

## 2. Current evidence baseline

### 2.1 Current Black Arcana client surface

At this baseline, current Black Arcana client code contains Stage 05 UI/input components plus the separate Stage 07.07 Borrowed Sight client controller.

Repository search at this checkpoint did not identify a generic Black Arcana casting implementation using:

- particle emission APIs as a cross-spell cast presentation system;
- `playSound` as a generic cast lifecycle system;
- a generic animation-provider hook;
- a generic camera-shake/zoom service.

The project asset root `src/main/resources/assets/black_arcana/` currently contains only `lang/`.

Therefore this plan must remain explicit that audiovisual casting infrastructure is future work.

### 2.2 Current synchronization facts

Current generic spell presentation synchronizes only:

- `spellId`;
- `translationKey`;
- `iconId`.

Current authoritative cast result presentation carries:

- `castId`;
- result status;
- result code;
- bounded detail.

It does not generically prove:

- resolved impact entity;
- resolved impact block;
- target geometry;
- animation id;
- particle id;
- sound id;
- provider animation state;
- cast start timestamp suitable for client animation authority;
- channel progress;
- projectile impact identity.

05.15 must therefore not infer those facts from current selection, crosshair state, spell id, display name, namespace or local elapsed time.

### 2.3 Existing client preferences

`BlackArcanaClientConfig` already owns presentation-only preferences for:

- particle density multiplier;
- reduced motion;
- reduced flashes;
- HUD scale/anchor;
- feedback level/duration;
- radial mode.

05.15 consumes those existing presentation preferences where applicable. It does not reinterpret them as gameplay inputs.

### 2.4 Current physical modpack coexistence baseline

The physical modlist used for this audit confirms these adjacent animation/camera/input/presentation components:

| Component | Mod ID | Physical version | 05.15 relevance |
|---|---|---:|---|
| Epic Fight | `epicfight` | `21.17.3.1` | combat/battle-mode/animation environment |
| Epic Fight & Iron's Spellbook animation compat | `efiscompat` | `3.1.0` | Iron's↔Epic Fight presentation compatibility; not Black Arcana authority |
| Punchy | `punchy` | `2.7e` | player/combat presentation environment |
| Punchy Epic Fight Compat | `punchy_epicfight_compat` | `1.0.0` | Punchy↔Epic Fight compatibility surface |
| FirstPerson | `firstperson` | `2.7.2` | first-person body/camera coexistence |
| Better Lock On | `betterlockon` | `2.0.8-neoforge` | targeting/camera-facing coexistence |
| Lock-On Movement Fix | `lockonmovementfix` | `1.0.2` | movement behavior around lock-on |
| NotEnoughAnimations | `notenoughanimations` | `1.12.4` | additional player-animation presentation |
| Player Animator | `playeranimator` | `2.0.4+1.21.1` | animation library present both top-level and jar-in-jar evidence |
| Player Animation Library | `player_animation_library` | `1.1.6+mc.1.21.1` | separate animation library; must not be conflated with Player Animator |
| Spell Actionbar | `spell_actionbar` | `1.1.4` | external casting presentation surface |
| Controlling | `controlling` | `19.0.5` | keybinding discovery only |
| Iris | `iris` | `1.8.14-beta.1+mc1.21.1` | shader/rendering coexistence for real-client QA |
| Aeronautics Camera Sync | `aero_cam_sync` | `1.4.0` | another camera-state coexistence surface |
| Sable Ragdolls Patch | `sable_player_ragdoll_patch` | `1.9` | player pose/ragdoll coexistence, including Punchy-related mixins |

Presence/version establishes only physical environment facts. It does **not** establish supported Black Arcana integration methods.

No class, event, animation-layer API or pose hook from those mods is authorized until exact-version source/API evidence is reviewed.

---

## 3. Relationship to existing plans

### 3.1 05.04 — Accessibility & client configuration

05.04 remains authority for client preferences and accessibility policy.

05.15 applies those rules to audiovisual casting:

- reduced motion affects optional camera/pose/motion presentation;
- reduced flashes affects bright/pulsing cast presentation;
- particle density affects nonessential Black Arcana local particle density;
- no important cast state may rely only on audio, color, flash, motion or particles.

05.15 does not create a second accessibility configuration system.

### 3.2 05.06 — Modpack coexistence

05.06 remains authority for coexistence and optional-provider boundaries.

05.15 specializes that policy for:

- player animation;
- combat mode;
- first-person rendering;
- camera motion;
- lock-on presentation;
- host-provider cast presentation;
- audiovisual deduplication.

### 3.3 05.08 — Visual state semantics

05.08 defines what visual states mean.

05.15 must not use audiovisual intensity to silently redefine those meanings.

For example:

- a bright flourish cannot mean authoritative success unless its trigger is authoritative enough to prove success;
- a red local target circle cannot mean server denial unless the server contract actually proves denial;
- missing animation cannot mean spell unavailable.

### 3.4 05.11 — Contextual feedback orchestration

05.11 remains authority for transient selection/forecast/result arbitration.

05.15 extends the same causal discipline to audiovisual cues.

A result cue must not be attached to the player's **current** spell/aim merely because that is what is visible when an old `castId` result arrives.

### 3.5 05.12 — Iconography/resource resolution

05.12 governs spell-icon resource lookup.

05.15 does not reuse `iconId` as an animation/sound/particle identifier. Each future audiovisual resource contract requires its own explicit semantics and bounds.

### 3.6 05.13 — Targeting/aim presentation

05.13 remains authority for local aim versus server target truth.

05.15 telegraphs must respect that distinction. Local cursor observation may support uncertain presentation, but server-owned gameplay geometry cannot be reconstructed from local crosshair state.

### 3.7 05.14 — Spell details/inspection

05.14 remains authority for rich spell-information fields.

05.15 may define audiovisual presentation identity later, but must not use animation/sound/VFX as a covert metadata channel for unverified mechanics.

### 3.8 Stage 07 — per-spell content

Stage 07 remains authority for each spell's actual fantasy, effect, targeting, resource/cooldown/scaling, progression, world behavior and per-spell audiovisual specification.

05.15 owns the **cross-spell presentation framework and safety rules**.

Stage 07 owns decisions such as:

- which original sound belongs to a spell;
- which original particle family belongs to a spell;
- whether a spell needs a cast pose;
- whether a server-owned effect needs a gameplay telegraph;
- spell-specific timing that is justified by the canonical runtime.

05.15 must not become a second spell-definition catalog.

### 3.9 Stage 07.07 Borrowed Sight boundary

Borrowed Sight already has its own server-authored presentation/camera lifecycle.

05.15 must not replace that lifecycle with a generic camera-effect framework or reinterpret Borrowed Sight camera state as generic cast VFX.

Future camera presentation can share lower-level client utilities only if authority and lifecycle remain explicitly separate.

---

## 4. Non-negotiable authority model

Every audiovisual cue must be classified before implementation.

### 4.1 `LOCAL_INTENT_PRESENTATION`

Meaning:

- immediate acknowledgment that the local player pressed a Black Arcana input;
- purely presentational;
- does not claim legality, acceptance, target validity, resource availability, cooldown readiness or world-effect admission.

Allowed examples:

- subtle keypress/UI tick;
- radial close/select transition;
- tiny non-semantic hand/UI anticipation that is clearly cancellable.

Forbidden examples:

- full cast release animation;
- impact burst;
- success chime;
- damaging area telegraph presented as authoritative;
- provider resource consumption animation.

### 4.2 `SERVER_AUTHORED_FORECAST`

Meaning:

- presentation derived from an explicit bounded server-authored preview contract;
- advisory for the exact facts that preview owns;
- still not cast success.

Examples may include hazard/gate forecast already supported by current Stage 05A contracts.

A forecast cannot authorize impact, mutation or final cast success unless the contract explicitly owns that fact.

### 4.3 `AUTHORITATIVE_CAST_RESULT`

Meaning:

- cue is driven by the server-authored result for a specific `castId`;
- suitable for generic success/denial presentation within what the result proves.

Current limitation:

- generic cast result does not identify resolved impact target;
- therefore success/denial cues must not invent a target attachment.

### 4.4 `SERVER_OWNED_RUNTIME_EVENT`

Meaning:

- a server-owned gameplay lifecycle produces a bounded presentation event because the current cast-result contract is insufficient for the needed phase.

Possible future cases:

- validated channel/session begin;
- channel release;
- projectile/field lifecycle presentation;
- gameplay-relevant area telegraph;
- confirmed impact location;
- bounded persistent hazard/domain visual state.

This category requires a reviewed bounded protocol/event contract before implementation.

### 4.5 `CLIENT_DECORATIVE_EFFECT`

Meaning:

- local cosmetic detail whose absence cannot hide gameplay-critical state;
- may be reduced or disabled under accessibility/performance settings;
- never feeds server logic.

Examples:

- small ambient wisps around the local player's cast hand;
- decorative screen-edge vignette;
- nonessential flourish after an already-authoritative result.

### 4.6 `PROVIDER_OWNED_PRESENTATION`

Meaning:

- animation/audio/VFX is owned by an external host/provider for its own surface.

Black Arcana must not duplicate it automatically.

For a Black Arcana-owned spell hosted by Iron's, authority remains operation-specific:

- Iron's may own supported host presentation/invocation;
- Black Arcana owns canonical Black Arcana validation/transaction/cooldown;
- any extra Black Arcana audiovisual cue must be intentionally deduplicated so one provider action does not become multiple overlapping cast presentations.

### 4.7 `UNKNOWN_OR_UNAVAILABLE`

Meaning:

- the necessary presentation fact or integration seam is not verified.

Required behavior:

- omit the optional cue;
- preserve core casting;
- preserve authoritative text/HUD feedback where available;
- do not guess from names, local timings, animation state or provider internals.

---

## 5. Canonical audiovisual cast lifecycle

Future audiovisual work should use a consistent conceptual lifecycle rather than arbitrary per-screen callbacks.

### 5.1 Phase A — selection

Source:

- client-local synchronized selection state.

Allowed:

- selection sound/UI animation;
- radial/editor emphasis;
- purely local preview flourish.

Not allowed:

- cast-release animation;
- impact VFX;
- success audio;
- resource depletion presentation not backed by provider/server truth.

### 5.2 Phase B — local intent emitted

Source:

- local input sent as bounded cast intent.

Allowed:

- restrained non-semantic anticipation cue;
- optional short client responsiveness cue that can be visually distinguished from authoritative completion.

Rule:

A keypress is never authoritative acceptance.

If the design cannot make that distinction legible, skip the anticipation cue rather than present a false cast.

### 5.3 Phase C — server denial

Source:

- authoritative cast result for the exact `castId`.

Allowed:

- denial sound;
- bounded failure pulse;
- failure-specific animation cancellation/recovery where a safe animation contract exists;
- HUD text under 05.11.

Rules:

- denial presentation must not be attached to a guessed target;
- denial audio is supplemental to non-audio information;
- denial must not trigger damaging/impact VFX.

### 5.4 Phase D — committed/successful cast

Source:

- authoritative server result or a more specific server-owned runtime presentation event where required.

Allowed:

- release/commit audio;
- cast release VFX;
- player pose transition;
- impact-independent success flourish.

Rules:

- use `castId` correlation where available;
- do not infer current spell identity for an unmatched result;
- if a cue requires spell-specific identity but correlation cannot prove it, use a generic result cue or omit the specific cue.

### 5.5 Phase E — active channel/session

Current generic Stage 05 presentation does not expose a complete canonical channel-progress contract.

Therefore future channel animation/audio must not run from client elapsed time alone and then be treated as gameplay truth.

A future implementation must define:

- server-owned session identity;
- begin/cancel/release semantics;
- bounded progress representation if needed;
- stale-session handling;
- reconnect/screen-change behavior;
- animation teardown.

### 5.6 Phase F — projectile/field/impact

Impact presentation is separate from generic cast success.

If a spell's gameplay depends on a resolved impact, field origin, area or persistent server object, the presentation must bind to an authoritative runtime entity/state/event rather than guessed local aim.

A generic `CastResultPayload` alone does not currently prove impact identity.

### 5.7 Phase G — hazard/backlash consequence

Arcane Danger remains Black Arcana-owned server authority.

Audiovisual consequences may communicate:

- dangerous cast warning;
- confirmed backlash consequence;
- Corruption/Strain-related presentation when an authorized client contract exists.

But presentation must preserve the existing causal rules:

- Backlash does not become a normal offensive proc chain;
- no audiovisual callback may re-enter the canonical cast engine as a new offensive cast;
- warning/preflight is not the same as confirmed consequence;
- Corruption/Strain values not authorized for client sync remain unavailable rather than inferred.

### 5.8 Phase H — teardown

Every temporary audiovisual state must have bounded cleanup for:

- cast denial;
- animation completion;
- channel cancel;
- player death;
- dimension change;
- logout/disconnect;
- resource reload;
- screen/camera mode transition where relevant;
- provider unload/absence;
- stale `castId` eviction.

No presentation state may become an unbounded session registry.

---

## 6. Presentation-cue identity and correlation

### 6.1 Do not overload existing identifiers

Do not treat any of these as interchangeable:

- `spellId`;
- `iconId`;
- cooldown group id;
- provider id;
- animation resource id;
- sound resource id;
- particle/VFX cue id;
- `castId`.

Each has separate authority and lifecycle.

### 6.2 `castId` is the root correlation token

Where a cue represents the result/lifecycle of one root cast, `ArcanaCastId` should remain the natural correlation identity.

Client correlation must be bounded by:

- maximum pending entries;
- maximum age;
- session reset;
- duplicate/replay handling;
- stale-result tolerance.

A missing correlation entry must degrade to generic presentation rather than guessed attribution.

### 6.3 Future cue contracts

If current result/state payloads cannot express a required server-authored presentation event, a future bounded cue contract may be reviewed.

Such a contract should prefer declarative bounded fields such as:

- protocol version;
- `castId` when causally attached to a cast;
- bounded cue identifier;
- bounded phase/type enum;
- bounded entity/block/world reference only when server-authorized and actually required;
- bounded duration/intensity bucket;
- optional server tick/sequence data where needed for stale ordering.

It must not carry:

- Java class names;
- script bodies;
- arbitrary commands;
- arbitrary filesystem paths;
- unbounded NBT/blobs;
- client-authored authoritative geometry;
- provider-private object identities that cannot survive safely across the boundary.

---

## 7. Particle/VFX policy

### 7.1 Decorative particles

Decorative local particles may be density-scaled by the existing Black Arcana particle multiplier.

At multiplier `0`, nonessential particles may disappear entirely.

Therefore they cannot be the sole representation of:

- a dangerous active area;
- a required target boundary;
- a hard denial;
- a lethal countdown;
- an interactable server-owned object;
- a mandatory ritual/domain boundary.

### 7.2 Gameplay-relevant telegraphs

A gameplay-relevant telegraph must reflect server-owned geometry/lifecycle.

Examples include a future damaging zone, domain boundary or delayed strike where the player needs the displayed boundary to make gameplay decisions.

Required properties:

- geometry/range source is canonical server state;
- lifetime is server-owned or server-correlated;
- world/dimension identity is explicit;
- no force-loading is introduced for visualization;
- unloaded/unknown state fails closed;
- accessibility fallback exists if particle density is reduced;
- visual bounds never claim protection/world-mutation permission unless the server contract proves it.

### 7.3 Bounded emission

Every VFX system must have explicit budgets for:

- particles per event;
- particles per client tick;
- active persistent emitters;
- recipient range;
- lifetime;
- spawned client objects;
- cache count/age.

No global entity/chunk scans are authorized for decoration.

### 7.4 Distance and recipient policy

Multiplayer presentation should be scoped to relevant nearby recipients rather than broadcast globally by default.

If the server must distribute a cue, recipient selection must be bounded by actual relevance/range/dimension and must not enumerate the entire world each tick.

### 7.5 Resource reload

Any resource-backed VFX cache must be invalidated safely on reload.

Missing/malformed resource:

- logs/diagnostics may record the presentation failure;
- gameplay continues;
- fallback presentation is used where required;
- spell validity is unchanged.

---

## 8. Audio policy

### 8.1 Audio never owns gameplay truth

Sound may reinforce:

- selection;
- intent;
- denial;
- success;
- channel state;
- impact;
- hazard/backlash;
- persistent field ambience.

It does not determine whether those events happened.

### 8.2 No audio-only critical state

Players with audio disabled must still be able to understand essential cast outcome through another channel.

Critical denial/danger/state must have text/icon/shape/timing or another non-audio carrier.

### 8.3 Spatial versus UI audio

Choose the channel based on the source:

- screen/radial selection → client UI-local sound;
- server-world impact/field → world-positioned sound when canonical position exists;
- denial directed only to the caster → caster-local presentation unless the design intentionally requires an audible world event;
- persistent server object → bounded world ambience owned by that object's lifecycle.

Do not spatialize a guessed target position.

### 8.4 Deduplication

For one physical/provider invocation, avoid simultaneous duplicate:

- host-provider cast sound;
- Black Arcana cast sound;
- compatibility-mod sound;
- delayed result sound.

The intended layer must be chosen explicitly per integration.

### 8.5 Asset provenance

Black Arcana sound assets must be:

- original/project-owned; or
- used under a compatible documented license/permission with provenance.

Do not rip or recreate copyrighted signature sounds from Mahou Tsukai, Iron's, films, television, games or other mods.

---

## 9. Player animation policy

### 9.1 Animation is presentation, not cast authority

A pose beginning, reaching a keyframe or ending does not authorize:

- resource spend;
- cooldown;
- damage;
- target acceptance;
- world mutation;
- progression bypass.

The canonical server cast transaction remains authority.

### 9.2 Animation failure is normally presentation failure

If an optional animation adapter is unavailable or rejects a pose:

- core casting should continue when gameplay is otherwise valid;
- authoritative HUD/result remains available;
- the audiovisual layer degrades gracefully.

Fail-closed here means **do not call an unverified/incompatible provider hook**, not “deny legitimate Black Arcana gameplay because an animation mod is absent”.

An animation may become a gameplay requirement only through a separate explicit architectural decision proving why server gameplay must depend on it.

### 9.3 Animation timing

Do not make server gameplay wait for a client-only keyframe.

If a future spell genuinely requires wind-up/release timing, that timing belongs to a server-owned charge/channel/session or scheduled gameplay contract. Client animation follows that contract.

### 9.4 First-person and third-person

A future cast animation must define behavior for:

- vanilla first-person hand/body;
- FirstPerson mod rendering;
- ordinary third-person;
- Epic Fight battle mode;
- animation-provider absence;
- perspective switch during playback;
- death/ragdoll transition;
- mount/vehicle states where relevant.

Unsupported combinations should degrade to a safe presentation subset, not crash or alter cast authority.

### 9.5 Animation-library boundaries

The physical pack contains both:

- `playeranimator 2.0.4+1.21.1`;
- `player_animation_library 1.1.6+mc.1.21.1`.

They are separate provider surfaces.

Never assume:

- identical APIs;
- identical layer semantics;
- compatible animation resource formats;
- one is an alias for the other;
- either is the canonical Black Arcana provider merely because it is installed.

Before implementation:

1. identify the minimum required Black Arcana animation capability;
2. inspect exact-version provider API/source/docs;
3. choose one Black Arcana-owned adapter boundary;
4. prefer an existing compatible provider rather than shipping a parallel animation engine;
5. ensure provider absence is safe;
6. test dedicated-server classloading;
7. document provenance of any animation assets.

### 9.6 Epic Fight boundary

Epic Fight `21.17.3.1` is an environment with its own combat/animation state.

Until an exact supported seam is verified, Black Arcana must not invent:

- battle-mode event names;
- animation-layer APIs;
- stun/lock windows;
- attack-speed synchronization methods;
- pose priorities;
- cancellation callbacks.

Black Arcana cast legality must not depend on a guessed Epic Fight client state.

### 9.7 EFIS boundary

`efiscompat 3.1.0` is specifically an Epic Fight & Iron's Spellbook animation compatibility surface.

Its presence does not prove a Black Arcana-native animation route.

For Black Arcana spells hosted by Iron's, real-client black-box behavior must be observed before adding a second animation layer.

---

## 10. Camera presentation policy

### 10.1 Camera is supplemental

Potential future presentation includes:

- subtle shake;
- zoom/FOV easing;
- vignette;
- directional emphasis;
- recoil-like motion;
- temporary focus framing.

None changes canonical target, raycast, range or effect geometry.

### 10.2 Reduced motion

Nonessential camera motion must consult reduced-motion.

Reduced-motion alternatives should prefer:

- static outline;
- short opacity emphasis;
- text/icon state;
- reduced displacement/amplitude;
- no camera motion where unnecessary.

### 10.3 FirstPerson and camera-mod coexistence

The physical pack includes `firstperson 2.7.2` and `aero_cam_sync 1.4.0`, plus lock-on-related components.

05.15 therefore forbids unconditional camera ownership.

Future camera effects require:

- bounded duration/amplitude;
- teardown on perspective/dimension/logout changes;
- no persistent camera transform leakage;
- real-client coexistence tests;
- optional/provider-aware behavior where a supported seam exists.

### 10.4 Lock-on coexistence

Better Lock On and Lock-On Movement Fix are present.

Black Arcana target presentation must not fight lock-on by forcibly rotating authoritative target state from the client.

A camera flourish may not silently retarget the canonical server cast.

### 10.5 Borrowed Sight

Borrowed Sight remains a Stage 07.07 server-authored camera/viewpoint feature.

Generic 05.15 camera effects must not override or cancel it unless a separately reviewed composition rule exists.

When Borrowed Sight is active and no safe composition contract exists, ordinary cosmetic camera motion should yield rather than corrupt the viewpoint lifecycle.

---

## 11. Provider-hosted presentation and double-processing

### 11.1 Per-operation authority

External host presentation is not the same as external gameplay authority.

For an Iron-hosted Black Arcana spell:

- Iron's may present/invoke through its supported UI;
- Black Arcana still owns the Black Arcana transaction;
- 05.15 decides whether additional Black Arcana audiovisual presentation is necessary and safe.

### 11.2 Dedup key

Future integration should reason about one root physical/provider invocation and one canonical `ArcanaCastId`.

Do not let one action produce:

- provider cast animation + duplicate Black Arcana cast animation + duplicate compatibility animation;
- two release sounds;
- two impact bursts;
- two camera kicks;
- multiple server cue packets for the same phase without explicit composition semantics.

### 11.3 Provider-native first

When a verified provider already owns the appropriate presentation for its host surface, prefer provider-native presentation rather than reproducing it in Black Arcana.

Add Black Arcana-specific presentation only for semantics the provider does not own, such as an explicitly Black Arcana-authored hazard/backlash consequence.

### 11.4 No tooltip/VFX scraping

Do not infer provider animation/sound/VFX contracts by scraping runtime tooltips, resource names or private internals.

Exact supported APIs or black-box coexistence evidence are required before bridge code.

---

## 12. World-effect and telegraph authority

### 12.1 `WorldEffectPolicy` remains authority

A beautiful area marker cannot bypass:

- protection adapters;
- loaded-chunk bounds;
- mutation policy;
- world border;
- Stage 04 admission;
- Stage 07 domain-specific bounds.

### 12.2 Telegraph versus permission

A telegraph communicates the server-owned effect area/lifecycle it was authorized to communicate.

It does **not** automatically mean:

- every block in that area will mutate;
- every entity will be hit;
- protections allow mutation;
- the effect is guaranteed to complete.

Presentation copy/semantics must reflect the exact authority of the data source.

### 12.3 No force-loading for visuals

Do not load chunks merely to render a telegraph or remote VFX.

Unknown/unloaded state is omitted or presented as unavailable under the owning gameplay contract.

---

## 13. Arcane Danger audiovisual semantics

Arcane Danger presentation should remain causally separate from ordinary spell impact.

Suggested semantic families for future original design:

- **danger forecast** — restrained warning, advisory;
- **committed dangerous cast** — confirmed cast consequence presentation;
- **backlash** — disruptive/unstable visual/audio language distinct from ordinary successful damage;
- **corruption** — persistent identity language only when a legitimate client-visible state contract exists;
- **strain** — exertion/instability language only when authorized state exists.

Rules:

- do not make Backlash look like a normal bonus offensive proc;
- do not trigger normal offensive on-cast/on-hit presentation chains from Backlash unless the gameplay contract explicitly says so;
- do not expose hidden exact Corruption/Strain values through animation intensity if those values are intentionally unsynchronized;
- no audiovisual consequence may create a second gameplay settlement path.

---

## 14. Accessibility and sensory safety

### 14.1 Redundant information

Essential states need at least one non-audio and non-particle carrier.

Where practical, avoid relying solely on:

- color;
- flashing;
- rapid camera motion;
- sound pitch;
- particle density;
- animation pose.

### 14.2 Reduced flashes

Future cast flashes must define a reduced-flash form.

Avoid:

- rapid repeated full-screen brightness pulses;
- strobe-like alternation;
- unbounded additive bloom effects;
- stacking multiple independent flash sources with no cap.

### 14.3 Reduced motion

Future motion-heavy presentation must define a reduced-motion path.

This includes:

- camera shake;
- camera sway;
- radial transitions;
- screen distortion;
- large moving overlays;
- nonessential body motion amplification.

### 14.4 Particle density zero

A density multiplier of zero must not hide mandatory gameplay telegraphs.

If a telegraph is essential, provide an independent geometry/outline/ground-shape/textual cue whose visibility policy is not the ordinary decorative particle density toggle.

### 14.5 Audio accessibility

Critical state must remain understandable with master/game audio muted.

Future sound assets should integrate with supported Minecraft sound categories/subtitle behavior where appropriate rather than inventing an inaccessible parallel audio stack.

No exact registry/API name is frozen here before implementation review.

---

## 15. Performance budgets

Audiovisual presentation must remain bounded even in a large modpack and multiplayer combat.

### 15.1 No global/per-tick discovery

Forbidden by default:

- scanning all loaded entities every client tick to attach cosmetic effects;
- scanning all chunks for VFX anchors;
- scanning provider registries every frame;
- resolving resource files from disk/JAR every frame;
- protection checks every render frame;
- network request per particle/animation frame;
- unbounded history of cast cues.

### 15.2 Recommended budget classes

Future implementation should define explicit limits for:

- active local cast presentations;
- active remote cast presentations;
- persistent telegraph emitters;
- particles/event;
- particles/tick;
- sound instances/cast phase;
- animation layers/player;
- camera effects/player;
- cue cache count and age;
- remote recipient radius;
- packet frequency and payload size.

Numbers should be profiled and selected during implementation rather than invented in this planning-only file.

### 15.3 Diminishing presentation density

When many effects occur simultaneously, client presentation may reduce decorative density while preserving gameplay-critical signals.

Decorative fidelity should degrade before authoritative readability.

---

## 16. Multiplayer and remote-player presentation

### 16.1 Local versus remote fidelity

The local caster may receive richer UI/camera feedback than remote observers.

Remote players generally need:

- bounded world-visible cast cue;
- impact/field information relevant to them;
- no private provider/resource/progression details.

### 16.2 Privacy

Do not broadcast private player state merely to drive cosmetics.

Examples of data that should remain private unless explicitly required:

- detailed progression gates;
- exact provider resource balance;
- hidden Corruption/Strain internals;
- private loadout metadata beyond what gameplay visibility legitimately exposes.

### 16.3 Relevance filtering

Server-authored world presentation should send only to relevant recipients in the same applicable dimension/range or through an equivalent bounded supported mechanism.

No global broadcast by default.

---

## 17. Dedicated-server and optional-dependency boundary

All animation, particle-rendering, screen, camera and local-audio classes remain physical-client-only where required.

Common/server code may own declarative presentation-event data but must not load client renderer/provider classes on a dedicated server.

Optional animation-provider adapters must:

- be isolated behind Black Arcana-owned boundaries;
- activate only when the exact target mod is present and compatible;
- avoid eager classloading when absent;
- fail safely when incompatible;
- never be required for core Black Arcana cast transaction correctness.

Dedicated-server smoke remains a mandatory CI gate for any implementation touching this boundary.

---

## 18. Clean-room and provenance rules

Black Arcana audiovisual identity must remain original.

Do not copy or closely reproduce without compatible rights:

- Mahou Tsukai cast effects;
- Iron's textures/particles/sounds/animations;
- Epic Fight animations;
- other mods' spell poses;
- film/TV/game signature glyphs, portals, audio stingers or VFX timing sequences;
- provider text describing VFX as asset source instructions.

References may inform high-level design goals such as:

- readability;
- weight;
- danger;
- spatial clarity;
- timing categories;
- coexistence problems.

Implementation assets must be project-owned or have documented compatible provenance.

Before any third-party asset derivation, update the provenance/notice records required by `SOURCES.md`, `THIRD_PARTY_NOTICES.md` and Stage 09 provenance policy.

---

## 19. Proposed Black Arcana audiovisual vocabulary

This section is conceptual, not an asset claim.

Future Black Arcana-owned presentation should prefer a small coherent semantic vocabulary rather than each spell inventing unrelated cues.

Possible categories:

### 19.1 Intent

- restrained anticipation;
- short-lived;
- never visually equivalent to committed cast.

### 19.2 Committed cast

- decisive release cue;
- original Black Arcana shape/audio language;
- correlated to authoritative state.

### 19.3 Denial

- clipped/interrupted language;
- readable without sound;
- no impact flourish.

### 19.4 Danger

- asymmetry/instability/warning semantics;
- distinct from ordinary cooldown/unavailable state;
- no false exact risk information.

### 19.5 Backlash

- rupture/disruption semantics;
- distinct from offensive hit confirmation;
- bounded and accessibility-aware.

### 19.6 Persistent field/domain

- stable boundary language;
- server-owned lifecycle;
- clear difference between decorative ambience and gameplay geometry.

Final art direction belongs to reviewed asset/design work, not this planning contract.

---

## 20. Implementation phases

### Phase A — evidence and API selection

Before code:

1. fetch latest `main` and record SHA;
2. confirm exact physical modlist versions again;
3. inspect current Stage 07 content that actually needs audiovisual presentation;
4. identify the minimum required animation/camera capabilities;
5. inspect exact-version provider APIs only for providers genuinely needed;
6. record unsupported combinations as fail-closed rather than inventing hooks;
7. reconcile clean-room/provenance requirements.

Output:

- verified provider-boundary note;
- no runtime yet.

### Phase B — pure presentation-state model

Design a small Black Arcana-owned model for audiovisual cue lifecycle that separates:

- local intent;
- server forecast;
- authoritative result;
- server-owned runtime event;
- decorative local effect;
- provider-owned presentation;
- unknown/unavailable.

TDD first.

No renderer/provider coupling in the pure model.

### Phase C — generic result/denial audiovisual layer

Implement only cues supportable by current authoritative result/correlation state.

Goals:

- no guessed spell/target attribution;
- bounded deduplication;
- accessibility settings consumed;
- no new gameplay authority.

### Phase D — original asset/resource pipeline

Add project-owned resource conventions for:

- sounds;
- particles/VFX assets;
- animation assets if a verified provider format is selected.

Requirements:

- resource reload safety;
- missing-resource fallback;
- no arbitrary filesystem access;
- provenance recorded before third-party derivation.

### Phase E — optional animation provider adapter

Only if a concrete spell/player requirement needs it.

Requirements:

- exact-version API verified;
- one Black Arcana-owned adapter boundary;
- dedicated-server safe;
- provider absence safe;
- Epic Fight/FirstPerson coexistence tested;
- no client keyframe gameplay authority.

### Phase F — gameplay-relevant telegraph contract

Only for content that actually needs authoritative geometry/lifecycle presentation.

Requirements:

- server-owned bounded event/state;
- Stage 04/05.13 authority preserved;
- no force-loading;
- accessibility fallback;
- multiplayer relevance bounds;
- deterministic tests.

### Phase G — real-pack audiovisual QA

Execute the real-client matrix on exact CI artifact with:

- default perspective;
- first person/third person;
- FirstPerson enabled;
- Epic Fight battle mode on/off;
- Iron-hosted Black Arcana probe where applicable;
- Spell Actionbar visible;
- Punchy coexistence;
- lock-on active/inactive;
- shaders/Iris representative state;
- particle density 0/0.5/1;
- reduced motion on/off;
- reduced flashes on/off;
- muted audio;
- representative low/high effect density.

Only direct observation may produce PASS for perceptual rows.

---

## 21. TDD and automated validation plan

### 21.1 Pure/unit tests

Future tests should cover deterministic presentation-state logic such as:

- local intent never upgrades itself to authoritative success;
- unmatched authoritative result remains generic;
- matched `castId` result may resolve bounded local correlation;
- duplicate result/cue deduplication;
- stale cue eviction;
- phase ordering;
- denial cancels pending local anticipation presentation;
- session teardown;
- reduced-motion/reduced-flash branching;
- particle-density decisions;
- provider-owned presentation suppresses duplicate Black Arcana layer where configured;
- missing optional provider selects fallback rather than gameplay denial.

### 21.2 Protocol tests

If a new server-authored cue payload is later approved:

- version bounds;
- string/id lengths;
- enum validation;
- malformed entity/block reference rejection;
- payload size limit;
- stale sequence handling;
- rate limiting where appropriate;
- no arbitrary execution fields.

### 21.3 GameTests/integration

Use GameTests only for gameplay/server-state behavior that actually requires world integration.

Do not attempt to declare visual quality PASS through GameTest.

Possible integration coverage:

- one committed cast emits at most one intended server presentation event;
- denied cast does not emit committed-impact cue;
- persistent field lifecycle emits bounded begin/end state;
- no double-processing through hosted provider route;
- world telegraph state obeys loaded-chunk/world-policy boundaries.

### 21.4 CI

Any implementation must retain the full repository gates:

- JUnit;
- diff sanity;
- NeoForge build;
- built-JAR verification;
- Foundation GameTests;
- dedicated-server smoke;
- exact-head revalidation after final `main` synchronization;
- post-merge exact-SHA validation.

No audiovisual change is allowed to weaken these gates merely because it is “client-only”.

---

## 22. Real-client validation matrix

When applicable implementation exists, record direct observations for at least:

| Scenario | Expected evidence |
|---|---|
| successful direct cast | one coherent committed presentation, no duplicate settlement/presentation |
| denied direct cast | denial cue only after authoritative result; no fake impact |
| quick-cast | same canonical presentation lifecycle as selected cast |
| radial selection | selection presentation only, never cast-release presentation |
| Iron-hosted Black Arcana cast | no duplicate Black Arcana/provider/EFIS presentation chain |
| Epic Fight battle mode | no crash/stuck pose; cast authority unchanged |
| Punchy + Epic Fight | no presentation loop/pose corruption observed |
| FirstPerson | no broken camera/body state after cast |
| third-person | remote/local pose readable and bounded |
| Better Lock On active | no client retargeting authority or camera fight that changes gameplay target |
| perspective switch during effect | temporary state cleans up correctly |
| reduced motion | nonessential camera/motion reduced without gameplay change |
| reduced flashes | flash-heavy presentation reduced without hiding critical state |
| particle density 0 | decorative particles absent while mandatory information remains understandable |
| muted audio | denial/success/danger remains understandable visually/textually |
| shader/Iris representative config | no catastrophic rendering/readability failure |
| logout/dimension change mid-effect | no leaked camera/animation/persistent client state |
| resource reload | caches/resources recover safely |
| high simultaneous effect density | decorative density degrades before gameplay readability |

A row stays `PENDING`, `BLOCKED` or `NOT APPLICABLE` until actually exercised.

---

## 23. Fail-closed rules

Future audiovisual implementation must prefer omission/fallback over invented truth.

Examples:

- unknown animation provider → no provider animation; cast still uses canonical gameplay path;
- malformed animation resource → fallback/no animation, not spell denial;
- missing sound → silent fallback plus non-audio feedback;
- missing decorative particle → no decorative particle;
- missing gameplay-critical telegraph resource → use approved non-particle fallback or block that **presentation implementation** from shipping until readable, without inventing geometry;
- unmatched `castId` → generic result cue, no guessed spell/target;
- stale channel/session → tear down presentation;
- missing target geometry contract → no authoritative area marker;
- provider host already owns cast animation → suppress duplicate Black Arcana host animation unless an explicit composition rule exists;
- Borrowed Sight active with no camera-composition contract → ordinary cosmetic camera effect yields;
- optional camera/animation provider absent → no direct class load/crash;
- player enters ragdoll/death state → temporary cast animation tears down;
- unknown world/dimension target → no remote telegraph;
- inaccessible flash/motion mode → reduced/static alternative;
- unverified third-party asset rights → do not ship the asset.

---

## 24. Non-goals

05.15 does not authorize:

- a second cast engine driven by animation;
- client keyframes spending resources or dealing damage;
- client-predicted impact treated as authoritative;
- local aim geometry presented as guaranteed server target geometry;
- per-frame target/protection queries;
- global entity/chunk scans for particles;
- force-loading for visual effects;
- permanent camera takeover;
- mandatory Epic Fight, Punchy, FirstPerson, Player Animator or Player Animation Library dependency for core casting;
- conflating Player Animator with Player Animation Library;
- restoring provider-native cost/cooldown processing for Black Arcana-owned hosted casts;
- duplicate provider + Black Arcana presentation by default;
- audio-only or particle-only critical state;
- copying Mahou Tsukai/Iron's/film/TV/game/mod audiovisual assets or signature presentation without compatible rights;
- declaring reduced-motion/reduced-flash quality PASS from static code or CI;
- changing Stage 07 spell mechanics merely to fit an animation system;
- reopening already-frozen server authority contracts without a separate reviewed architectural decision.

---

## 25. Exit criteria for this planning substage

05.15 planning is complete when this document and the Stage 05 index/master plan establish that:

1. audiovisual effects are presentation, not cast authority;
2. local intent, forecast, authoritative result and server-owned runtime events are distinct;
3. `castId` correlation is used where result/lifecycle attribution requires it;
4. current result payload limitations are recorded honestly;
5. gameplay-relevant telegraphs require server-owned bounded geometry/lifecycle;
6. animation provider failure does not normally deny valid gameplay;
7. Epic Fight/EFIS/Punchy/FirstPerson/lock-on/animation-library coexistence is treated as exact-version optional integration/QA, not assumed API;
8. Player Animator and Player Animation Library remain distinct provider candidates;
9. camera effects do not override targeting or Borrowed Sight authority;
10. Arcane Danger/Backlash audiovisuals preserve causal/no-proc-chain contracts;
11. particle/audio/motion/flash presentation obeys 05.04 accessibility settings and redundant-information rules;
12. particle/network/animation/camera work is explicitly bounded;
13. dedicated-server classloading remains safe;
14. provider-hosted presentation is deduplicated per root cast;
15. assets remain clean-room/provenance-safe;
16. Stage 07 remains owner of per-spell audiovisual content specification;
17. implementation requires TDD, exact-version provider audit where needed, real-client QA and the normal latest-main reconciliation/CI/merge protocol;
18. no runtime/asset/protocol/manual-PASS claim is made merely by merging this plan.

---

## 26. Implementation gate

Before anyone implements a 05.15 item, classify it as one of:

- `REQUIRED TO FIX A VALIDATION FAIL`;
- `APPROVED STAGE 05 HARDENING`;
- `STAGE 07 CONTENT PRESENTATION REQUIREMENT`;
- `OPTIONAL FOLLOW-UP`;
- `CARRIED TO STAGE 09`.

Then answer, with evidence:

1. What gameplay/server fact does the presentation communicate?
2. Which current contract owns that fact?
3. Is the cue local intent, forecast, authoritative result, server runtime event, decorative or provider-owned?
4. Does current protocol already provide enough information?
5. If not, what is the minimum bounded new contract?
6. Is `castId` correlation required?
7. Is the cue gameplay-critical or decorative?
8. What happens when particle density is zero/audio is muted/reduced motion is enabled?
9. Which exact animation/camera provider, if any, is required?
10. Is that provider's exact-version API verified?
11. What happens when the provider is absent/incompatible?
12. Could the provider already render the same cast, causing duplicate presentation?
13. What are the count/rate/lifetime/distance budgets?
14. How is teardown guaranteed?
15. Does dedicated-server startup avoid client/provider classloading?
16. Are every code/asset/source provenance requirement and license boundary documented?
17. Which automated tests cover deterministic behavior?
18. Which real-client rows must be executed before claiming acceptance?

If these cannot be answered precisely, implementation remains fail-closed/planning-only.
