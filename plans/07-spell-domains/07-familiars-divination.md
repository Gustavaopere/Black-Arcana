# 07.07 — Familiars & Divination

## State

`IN PROGRESS — SERVER SUBSTRATE MERGED / CLIENT OBSERVATION SPELLS NOT YET IMPLEMENTED`

PR #72 merged the bounded server-side Noetic/familiar/gaze/sanctuary substrate at `5c818c12bb6f580893e44f31fd0e17b9c1fe5840`. Its exact-SHA automated gates are valid evidence for that substrate. They do **not** prove production camera/HUD/input for remote-view mechanics.

Stage 07.07 is therefore not promoted as a completed domain, and Stage 08 must not treat it as canonical balance input yet.

## Implemented server substrate

The merged runtime provides:

- bounded Noetic observation sessions;
- loaded-only same-dimension target resolution with no force-loading;
- whitelisted `NoeticPerceptionSnapshot` output instead of arbitrary NBT/capability/inventory exposure;
- familiar ownership through bounded explicit providers (`OWNED`, `NOT_OWNED`, `UNSUPPORTED`);
- verified Ars familiar ownership adapter;
- server-side observation privacy/admission policy;
- Gaze of Stillness / Nullifying Gaze runtime and safety ceilings;
- Pact Sanctuary bounded aura/eligibility/target-change enforcement;
- expiry/logout/death/server-stop cleanup, including Soul Anchor-compatible final-death settlement.

These are reusable prerequisites, not proof that every approved spell is invocable end-to-end.

## Blocking spell implementation gaps

### Astral Severance — NOT IMPLEMENTED end-to-end

Canonical design requires a controllable non-combat viewpoint/avatar while the physical body remains vulnerable, with hard range, timeout/interruption return, no unauthorized projection interaction, and logout/death restoration.

The current server observation API accepts an already-loaded `LivingEntity` target and owns session/snapshot state only. It does not create or control an astral avatar/viewpoint, does not provide production client camera/input, and therefore cannot satisfy Astral Severance by itself. This is implementation work, not deferred manual evidence.

### Borrowed Sight — NOT IMPLEMENTED end-to-end

Canonical design requires channeling the viewpoint of an owned familiar or explicitly consenting bonded target, with range/channel cost and return on interruption/unload.

The current server policy correctly rejects foreign ownership and can authorize an owned familiar, but there is no production client camera/input/network flow that invokes and follows the authorized session. GameTests of the server admission boundary do not substitute for that missing implementation.

## Specification gate

`plans/07-spell-domains/README.md` requires every spell to define fantasy, host integration, invocation, target rules, resource cost, cooldown, scaling equation, progression gate, world-effect mode, boss/PvP behavior, config surface, tests and provenance.

The existing candidate entries for the 07.07 spell family do not yet freeze all of those fields. Until the per-spell specifications and the missing production mechanics are implemented/reviewed, 07.07 remains `IN PROGRESS` and Stage 08 must not tune these spells by inventing missing values.

## Existing automated evidence — server substrate only

- final PR #72 runtime head: `673aff57e15ec29a6fc0d6a94f0034726b99a4c1`;
- Black Arcana CI #1562 / `34069825298`: GREEN;
- 103/103 Foundation GameTests and dedicated-server smoke;
- runtime merge: `5c818c12bb6f580893e44f31fd0e17b9c1fe5840`;
- exact-SHA post-merge CI #1563 / `34070253755`: GREEN;
- artifact `black-arcana-5c818c12bb6f580893e44f31fd0e17b9c1fe5840`, ID `10000268004`, SHA-256 `35c8436ab3cbd2f75e8cc6f7ae5554edb7a330205f5166265f96979b6fa65b16`.

This evidence remains authoritative for the code it actually exercises; it is not reclassified as client acceptance.
