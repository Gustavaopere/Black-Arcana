# 05.05 — Final Real-client Runtime/Input Validation Handoff

## State

`HANDOFF COMPLETE / REAL-CLIENT EXECUTION DEFERRED TO STAGE 09 / PRESENTATION QA SPLIT`

This numbered handoff owns only physical-client checks that can prove or regress Black Arcana input, synchronization, provider integration or gameplay authority. Presentation/perceptual acceptance is tracked separately at:

`plans/visual-production/05-casting-ux/🟡-PENDENTE-05-final-client-validation-handoff.md`

The exact pre-extraction mixed handoff is retained at `plans/visual-production/_migration-source/05-casting-ux/05-final-client-validation-handoff.pre-extraction.md`.

## Authority rule

Do not redesign casting to make a client row pass. Preserve D005, D006, D019, D020, D023, D024, D029 and D034. A client-side failure may justify a numbered Stage 05 fix only when direct evidence shows an input, network, state-lifecycle, provider or authority regression.

D035 supersedes D034 for validation timing. This plan now owns the explicit transfer of physical/runtime-input/provider rows into the Stage 09 exact-release-candidate campaign. The rows remain mandatory release evidence and remain PENDING until directly observed; they no longer block implementation-stage progression.

## Freeze the exact candidate

For any physical campaign:

- test one exact reconciled `main` SHA with the matching Black Arcana artifact/build;
- record Minecraft `1.21.1`, current physical-modlist NeoForge, Java 21 and the actual modpack snapshot;
- do not promote automated CI into manual PASS;
- if the exact build cannot launch, record the launch/runtime blocker before evaluating downstream rows.

## Input and loadout runtime rows

Directly verify, where applicable:

- Black Arcana key mappings can be rebound through normal Minecraft controls and remain usable after restart;
- GUI focus suppresses selected/quick cast intent; inventory/chat/ordinary screens must not leak a cast;
- the bounded server loadout remains authoritative, including legitimate 16-slot state even though only a subset may have direct quick-cast mappings;
- editor apply/reopen converges to synchronized server state rather than trusting a local draft;
- clear/apply/reopen cannot bypass server slot/availability validation;
- disconnect/reconnect does not allow stale client loadout/result/HUD state to execute as current authority;
- a legitimate denial shown by the client corresponds to the server-authored result rather than a locally invented gate.

## Radial input/selection authority rows

Visual geometry/readability is handled by visual-production. The numbered runtime checks are:

- radial selection is not casting;
- one selection action changes only selected intent/state and requires a separate cast action;
- `TOGGLE`/`HOLD` input closes without leaving a stuck input state;
- paging/selection cannot exceed the synchronized bounded loadout or select a forged spell;
- GUI/screen focus cannot turn radial interaction into a bypass.

## Synchronized feedback-data rows

Layout, wording and perceptual readability are visual-production. Runtime/client-data validation must prove:

- denial, hazard/resistance forecast and predictable-gate data originate from synchronized server-authored presentation contracts;
- `CLEAR` does not become a client guarantee of successful cast settlement;
- reconnect/reload/profile changes cannot let stale forecast/tier/gate snapshots override newer authoritative state;
- unavailable/incompatible provider projection does not get promoted to a fabricated complete value;
- client presentation cannot mutate the underlying hazard/gate/resource state.

## Client configuration authority rows

Client preferences may persist locally, but no client setting may alter damage, power, cost, cooldown, progression, target admission, Arcane Danger or world mutation. Reset/default recovery must not create gameplay state. Visual effect compliance for reduced motion/flashes/particle density is owned by visual-production.

## Current-modpack integration rows

Where the exact assembled pack legitimately exposes the path, verify:

- one Iron's-hosted invocation of `black_arcana:irons_integration_probe` produces at most one Black Arcana root cast/result;
- Black Arcana transactional cost settles exactly once;
- Iron's native mana is not additionally charged for the Black Arcana-hosted transaction under the canonical bridge;
- Black Arcana cooldown settles exactly once;
- Epic Fight/EFIS client state cannot become Black Arcana cast-legality authority;
- optional provider absence/incompatibility does not crash the dedicated server or create a free fallback.

Readability, action-bar overlap, battle-mode animation and cosmetic coexistence are visual-production rows.

## Failure triage

For a directly observed runtime/input/provider failure:

1. record exact candidate SHA and physical sequence;
2. reproduce on the same SHA;
3. add a deterministic regression test when the failing boundary can be isolated;
4. observe RED before the production fix;
5. make the smallest authority-preserving fix;
6. rerun focused + full applicable automated gates and then the failed physical row.

Do not mark sibling rows PASS from a single fix. Do not create debug-only production ingress merely to manufacture manual evidence.

## Completion boundary

This numbered handoff closes when every required physical runtime/input/provider row is explicitly represented in the Stage 09 final-validation matrix with its evidence requirements preserved. That transfer is complete under D035. The rows themselves remain `PENDING / DEFERRED TO STAGE 09`; a future `BLOCKED` or `FAIL` result remains release-blocking and may reopen the originating Stage 05 plan for correction.

UI/HUD layout, visual accessibility, animation/VFX/audio and perceptual full-pack acceptance retain their own visual-production evidence ledger and do not silently change runtime authority.
