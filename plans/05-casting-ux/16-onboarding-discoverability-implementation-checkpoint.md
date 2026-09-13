# 05.16 — Onboarding / Discoverability / Contextual Help — Implementation Checkpoint

## State

`PHASES A–C + AUTHORIZED D BINDING PRESENTATION IMPLEMENTED / MERGED / POST-MERGE AUTOMATED GATES GREEN / PHYSICAL-CLIENT VALIDATION PENDING`

This checkpoint records the bounded implementation promoted from `🟡-PENDENTE-16-onboarding-discoverability-contextual-help.md`. It does not convert direct real-client/full-pack rows to PASS.

## Implemented scope

### Phase A — pure discoverability model

- bounded topic/priority model;
- once-per-session seen/dismissed state;
- explicit reopen/dismiss behavior;
- eight independent quick-cast binding presentations;
- explicit unbound state with no fabricated `R`/`V` fallback;
- bounded viewport layout.

### Phase B — minimal first-use cue

- trigger is event-driven from the already-accepted server-authored loadout snapshot;
- cue is client-only, non-modal and bounded to one active hint;
- cue teaches loadout → radial selection → explicit cast separation;
- current bindings are read from the actual `KeyMapping` state at presentation time;
- no cast legality, progression, cooldown, cost, target or world-safety fact is reconstructed on the client.

### Phase C — deterministic help re-entry

- the loadout editor exposes screen-local `H` Help without a new global key mapping;
- Help uses the player's current radial/cast/editor bindings plus quick-cast bound/unbound summary;
- while Help is open, pointer clicks and Enter/Delete/R/Space/reorder/page actions are intercepted before draft mutation or Apply;
- closing Help never applies the draft and never casts;
- session teardown clears discoverability session state on disconnect/player-session loss.

### Authorized Phase D subset — current binding / unbound presentation

Exact Minecraft 1.21.1 `KeyMapping` APIs are used:

- `KeyMapping.isUnbound()`;
- `KeyMapping.getTranslatedKeyMessage()`.

No independent key-conflict engine, Controlling API, controller-provider bridge or unsupported external integration is introduced. Those remain evidence-gated.

## Authority and persistence boundaries

- gameplay authority remains server-side;
- tutorial/help state does not grant spells, Mastery, progression or cast permission;
- first-use state is session-local;
- the only durable switch added is the existing client-config pattern `discoverabilityHints`, which changes presentation only;
- provider absence cannot deny a valid cast.

## TDD / automated evidence

- first RED: `36c709bb93e620e98017c9651aaa370de85bfc21`;
- pure-model GREEN: `5dd76aff257cb8d51b64057fbb48e55c42730753`, workflow `34758843055` GREEN;
- client-wiring RED: `9db31ea88d06097b03ec035d6c2b1ad864d700d4`, workflow `34759052907` failed at the expected missing-production contract;
- production head before checkpoint: `4ce87a4e4d200e5f5246f34fdf78272657b66d4c`, workflow `34760715703` GREEN through unit tests, diff sanity, NeoForge build, built-JAR verification, Foundation GameTests and dedicated-server smoke;
- latest-main reconciliation: `1b71443d2d3a8e7d6b48ab2b606da1218ceaab81`, behind `main` by zero at the merge gate; workflow `34760965231` GREEN;
- PR #232 merged by squash as `12ed7dab61cb32f7ac254ddc4f4f7e77c08a2f4a`;
- post-merge `main` workflow `34761284839` GREEN, including canonical QA JAR publication.

The deterministic implementation/merge gate for 05.16 is therefore closed.

## Remaining gate

`PHYSICAL-CLIENT / FULL-PACK QA PENDING`.

The real assembled-client matrix must directly validate first-use readability, rebound/unbound presentation, keyboard-only re-entry, GUI scaling/localization, coexistence with the installed control/HUD surfaces, restart behavior and multiplayer isolation. Automated CI does not fabricate those PASS states.
