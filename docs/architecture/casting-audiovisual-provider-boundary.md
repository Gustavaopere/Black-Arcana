# 05.15 Casting audiovisual provider boundary

Status: `PHASE A COMPLETE FOR PROVIDER-FREE PHASE B / PROVIDER-SPECIFIC WORK BLOCKED PENDING EXACT REVALIDATION`

Implementation classification: `APPROVED STAGE 05 HARDENING`.

Canonical implementation base: `main@12589c7168163ddd737a0534d6287ce102f97359`.

This note is the Phase A evidence/API-selection output required by `plans/05-casting-ux/15-casting-vfx-audio-animation-presentation.md`. It records what is verified for the first provider-free implementation tranche and what remains deliberately unavailable. It authorizes no audiovisual asset, renderer, camera effect, provider hook, gameplay telegraph or new network payload by itself.

## Evidence boundary

The 05.15 planning audit records the physical coexistence snapshot that was available when the plan was written, including Epic Fight `21.17.3.1`, EFIS compat `3.1.0`, Punchy `2.7e`, Punchy Epic Fight Compat `1.0.0`, FirstPerson `2.7.2`, Better Lock On `2.0.8-neoforge`, Lock-On Movement Fix `1.0.2`, NotEnoughAnimations `1.12.4`, Player Animator `2.0.4+1.21.1`, Player Animation Library `1.1.6+mc.1.21.1`, Spell Actionbar `1.1.4`, Controlling `19.0.5`, Iris `1.8.14-beta.1+mc1.21.1`, Aeronautics Camera Sync `1.4.0` and Sable Ragdolls Patch `1.9`.

That table is planning evidence, not a fresh Phase A physical-instance observation. The repositories accessible for this implementation do not expose a current physical-instance artifact/modlist from which those versions can be independently reconfirmed. No Phase A code therefore treats any of those versions as a currently verified runtime API contract.

Consequence: provider-specific implementation remains fail-closed. Before a later phase imports, reflects on, registers with or otherwise depends on Epic Fight, Player Animator, Player Animation Library, FirstPerson, a camera provider or any other optional presentation mod, its exact physical artifact/version and exact-version API seam must be revalidated from the real pack and provider source/API. Absence or incompatibility must remain a presentation fallback, never a Black Arcana gameplay denial.

Phase B is not blocked by that missing evidence because it requires no third-party provider capability and imports no provider API.

## Current Black Arcana evidence

At the canonical base:

- `CastIntentPayload` already carries bounded `castId`, `spellId`, slot and target hint.
- `CastResultPayload` already returns the same bounded `castId` plus authoritative result status/code/detail.
- `ClientInputController` creates the cast UUID immediately before sending the intent, but currently does not preserve that identifier in a presentation lifecycle.
- `ClientArcanaSyncState` stores authoritative synchronized facts and the latest result; server gameplay never reads that cache.
- `ClientUxState` only owns ephemeral selection timing.
- `BlackArcanaClientConfig` already owns presentation-only particle-density, reduced-motion and reduced-flash preferences.
- `CastingUxSemantics` already establishes the Stage 05 pattern of pure, surface-neutral presentation semantics that never performs gameplay admission.
- Borrowed Sight already owns a separate server-authored camera/view lifecycle and must not be replaced by a generic cast camera system.
- Stage 07 spell/domain runtimes remain the owners of per-spell mechanics and any future spell-specific audiovisual requirements. A presentation layer may communicate their authoritative outcomes but may not manufacture world mutation, impact geometry, channel state or target truth.

The current generic result contract proves cast result attribution, but it does not prove resolved impact entity/block, target geometry, animation id, particle id, sound id, channel progress, projectile impact identity or provider animation state.

## Minimum capability selected for Phase B

No animation or camera provider is required.

The minimum implementation is a Black Arcana-owned pure presentation-state model that can:

1. retain bounded local cast correlation by `ArcanaCastId` and optional locally known `ArcanaSpellId`;
2. classify cue authority as one of the exact 05.15 authority categories;
3. keep local intent visibly/non-semantically anticipatory rather than successful;
4. resolve matching authoritative results without guessing impact/target facts;
5. accept unmatched authoritative results as generic result facts only;
6. deduplicate repeated authoritative settlement;
7. evict stale local/presentation state deterministically;
8. clear all ephemeral state on teardown;
9. evaluate particle-density/reduced-motion/reduced-flash policy as client presentation policy only.

No renderer, sound registry, particle engine, animation layer, camera controller, provider adapter or protocol addition is necessary to implement or test those rules.

## Implementation-gate answers

1. **Gameplay/server fact communicated:** Phase B communicates only that local intent was emitted, or that an authoritative cast result exists. It does not communicate impact geometry or runtime world effects.
2. **Owning contract:** local input owns only local intent; `CastResultPayload`/`ArcanaCastResult.Status` own authoritative generic result truth. Stage 07/runtime contracts continue to own world effects.
3. **Cue classification:** Phase B models all seven 05.15 categories, but its live facts are initially `LOCAL_INTENT_PRESENTATION` and `AUTHORITATIVE_CAST_RESULT`; the rest can remain representable without fabricating payloads.
4. **Current protocol sufficient:** yes for generic intent/result correlation because both sides already carry `castId`.
5. **Minimum new bounded contract:** none for Phase B.
6. **`castId` correlation:** yes for matching local anticipation to authoritative result; unmatched results remain generic.
7. **Critical versus decorative:** lifecycle truth is semantic state; any future sensory flourish is decorative unless a separately reviewed server-owned telegraph contract says otherwise.
8. **Accessibility fallbacks:** particle density zero, muted audio, reduced motion and reduced flashes may suppress/reduce optional sensory carriers but cannot change lifecycle truth or gameplay. Mandatory information remains available through existing non-audiovisual Stage 05 surfaces.
9. **Required provider:** none for Phase B.
10. **Exact-version provider API verified:** not applicable to Phase B; provider-specific work remains blocked until exact revalidation.
11. **Provider absent/incompatible:** Phase B behaves identically because it has no provider dependency; later optional provider presentation must fall back/omit rather than deny gameplay.
12. **Duplicate provider presentation risk:** recognized but not activated in Phase B. Later provider adapters must suppress duplicate Black Arcana host presentation per root cast where configured.
13. **Budgets:** Phase B uses a bounded in-memory cast-correlation cache with explicit maximum entry count and stale age. It creates no particle/sound/animation/network budget because none exists yet.
14. **Teardown:** explicit clear plus deterministic stale eviction; client integration must clear on disconnect/session loss just as existing client UX state does.
15. **Dedicated-server safety:** the model lives under the physical-client presentation boundary and has no renderer/provider class references. Common/server gameplay does not read it.
16. **Provenance/license boundary:** Phase B is original Java state logic only. It introduces no third-party audiovisual asset or derived animation. Any later asset derivation remains gated by `SOURCES.md`, `THIRD_PARTY_NOTICES.md` and Stage 09 policy.
17. **Automated tests:** local intent never implies success; matched result settlement; denial cancellation; generic unmatched result; duplicate idempotence; stale eviction; teardown; accessibility-policy branching/bounds.
18. **Real-client rows before acceptance:** Phase B alone makes no perceptual PASS claim. Phase G must directly exercise the 05.15 real-client matrix on the exact CI artifact once concrete audiovisual implementation exists.

## Fail-closed decisions

- Unknown/unverified provider -> no provider hook.
- Unmatched `castId` -> generic authoritative result, no guessed spell/target/impact.
- Result status does not prove impact -> no impact attachment.
- Missing target geometry contract -> no authoritative area marker.
- Borrowed Sight camera lifecycle -> remains separate and wins over unrelated cosmetic camera concepts until an explicit composition contract exists.
- Accessibility preference -> may reduce decoration only; never changes server validation/effects.
- Provider API evidence unavailable -> Phase E remains blocked, Phase B remains provider-free.

## Phase A conclusion

Phase A selects **no animation/camera provider** for Phase B. The first implementation is therefore limited to a deterministic, provider-independent presentation lifecycle and policy model. This is sufficient to make later audiovisual work consume authority correctly without prematurely choosing an animation stack or fabricating information that the current protocol does not carry.
