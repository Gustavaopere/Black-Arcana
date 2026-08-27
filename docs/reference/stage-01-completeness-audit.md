# Stage 01 preparatory completeness audit

Status: PREPARATORY PASS. This audit does not freeze Stage 01 while Stage 00 remains outside `main`.

## Inventory-to-classification reconciliation

The public/observable inventory contains 53 catalog rows across boundaries, displacement, projection, mystic/control, gaze/perception, familiars, exchange/contracts and supporting systems.

All 53 have exactly one disposition in `classification-matrix.md`:

| Disposition | Count | Meaning for implementation |
| --- | ---: | --- |
| REIMAGINE | 27 | Authorized only through an original Black Arcana candidate spec. |
| KEEP | 2 | Fantasy retained, implementation/presentation/naming remain Black Arcana-owned. |
| MERGE | 11 | No standalone clone; use host capability/framework or a narrowly justified Black Arcana module. |
| DROP | 9 | Explicitly excluded from scope. |
| DEFER | 4 | Not authorized for initial implementation. |
| **Total** | **53** | **53/53 classified.** |

No inventory mechanic is unclassified.

## Implementation-facing candidate reconciliation

`candidate-specifications.md` contains 32 implementation-facing candidate contracts:

- Dominion/wards: 7.
- Liminal: 5.
- Noetic: 7.
- Eidetic Arsenal: 5.
- Sanguine/Sepulchral/Cinder: 8.

The count is intentionally larger than `REIMAGINE + KEEP` because three `MERGE` ideas are useful as Black Arcana-owned framework modules rather than standalone reference clones: Vigil Ward, Blood Price and Spirit Sight. Other `MERGE` rows remain host-owned or are folded into an existing candidate (for example weapon-projectile behavior is part of Spectral Arsenal).

Every candidate contract contains behavior, cost class, progression tier, safety rule, preferred host and acceptance-test obligations. T4 candidates remain balance-gated even when their technical design is specified.

## High/Critical risk coverage

Every retained High/Critical classification row is covered by all four layers below:

1. candidate-specific safety and acceptance tests in `candidate-specifications.md`;
2. global invariants and dedicated critical sections in `balance-risk-register.md` where the risk is Critical;
3. numeric/runtime config guardrails in `server-safety-ceilings.md` or an explicit requirement that Stage 08 supply a bounded value under an existing hard runtime budget;
4. server-authoritative validation through the Foundation contracts (`WorldEffectPolicy`, cost/progression/target validation and adapter isolation).

Specific cross-cutting coverage:

| Risk family | Required treatment |
| --- | --- |
| Player surveillance | Namescry/Borrowed Sight: no force-load, whitelisted data only, player use disabled by default unless policy/consent permits. |
| Hard crowd control | Gaze/wards/vector effects: break conditions, boss/PvP multipliers, velocity/duration ceilings and reapplication immunity. |
| Item duplication | Echo/Spectral/Oathforged: sanitized value profiles, no arbitrary NBT/data components, no persistent projected items, atomic sacrifice transactions. |
| Immortality/resource loops | Soul Anchor/Blood Price/Sanguine Harvest/Law: hard anchor cap, anti-farm accounting, health-payment ceiling, no positive feedback and no ordinary 100% immunity. |
| World grief | Black Pyre/domain/ritual areas: `WorldEffectPolicy`, temporary default, bounded cells/area/entities, no forced chunks and deterministic cleanup. |
| Boss/mod invariant bypass | Nullifying Gaze and health/control effects: explicit tags/adapters only, conservative unknown-boss behavior, no reflection/private-state hacks. |
| Session stranding | Inner Dominion/Astral projection: origin journal, timeout, logout/death/restart restoration and no nested domains initially. |

Dropped/deferred Critical mechanics remain non-authorized: Durability Exchange is dropped; Ruinous Convergence and Usurped Mandate are deferred; remote/URL-driven Sigil Projector behavior is not allowed as gameplay infrastructure.

## Host overlap audit

The classification deliberately avoids rebuilding capabilities already provided by the target modpack:

- Ars owns generic Blink/Warp travel and generic familiar ownership.
- Iron's is the preferred active-spell surface when its public extension API is sufficient.
- Malum is the preferred spirit-resource/ecology host, but Black Arcana does not assume the removed historical Spirit Ritual implementation.
- Eidolon is a presentation/ritual candidate only where Stage 03 confirms a stable 1.21.1 integration seam.

No candidate is allowed to introduce a mandatory second mana pool, staff/scroll-only casting, generic duplicate familiar framework or generic duplicate teleport network.

## Clean-room audit

- Reference source used for Mahou behavior: public player-visible documentation only.
- No Mahou source code, decompilation, class/packet/data-layout inspection or protected assets are required by the catalog.
- Player-facing names, domains and art language are Black Arcana-owned.
- Host mod documentation/public APIs may be inspected later for adapters; optional-mod internals remain isolated behind Black Arcana interfaces.

## Preparatory verdict

Stage 01 documentation is **ready for canonical rebase/review** once Stage 00 lands on `main`. It is not frozen and receives no ✅ while its base is preparatory.

Canonical promotion checklist after Foundation merge:

1. recreate/rebase Stage 01 from latest `main`;
2. verify all 53 inventory rows still reconcile 53/53;
3. verify host versions/APIs against the actual modpack/runtime;
4. review any changed safety ceilings/host decisions;
5. mark Stage 01 task files complete only after that review and merge.
