# Stage 07.07 — Noetic spell provenance map

Status: `CANONICAL TRACEABILITY MAP / DOES NOT FREEZE BALANCE`

This document closes only the clean-room provenance-link requirement for the seven Stage 07.07 Familiars & Divination candidates. It does not make any spell specification-complete by itself and does not freeze resource amounts, cooldowns, scaling, progression values, production control limits, provider selection or client/runtime acceptance.

## Canonical clean-room chain

Every row below is derived through the same Black Arcana-owned chain:

1. [`REFERENCE_LEDGER.md`](./REFERENCE_LEDGER.md) records the 2026-08-27 Mahou Tsukai CurseForge reference as **public project/gameplay documentation only**, with **no Mahou source code or assets consulted** and with the upstream All Rights Reserved notice preserved.
2. [`mahou-observable-catalog.md`](../reference/mahou-observable-catalog.md) records only player-visible/publicly documented behavior and explicitly excludes classes, algorithms, packet formats, data structures, assets and implementation details.
3. [`classification-matrix.md`](../reference/classification-matrix.md) converts the useful fantasy into an original Black Arcana disposition (`REIMAGINE` here), with Black Arcana-owned names, constraints and safety boundaries.
4. [`candidate-specifications.md`](../design/candidate-specifications.md) is the Black Arcana-owned implementation-facing candidate contract. It explicitly leaves exact numeric balance to Stage 08.
5. [`candidate-host-viability.md`](../reference/candidate-host-viability.md) separates Black Arcana authority from optional provider surfaces. `CORE`, `PUBLIC_API` and `PROBE` are engineering confidence/boundary labels, not permission to import undocumented provider internals.
6. Current production code/tests and Stage 07 checkpoints prevail wherever runtime behavior has already been implemented.

Mahou Tsukai remains a design/behavior reference only. No Stage 07.07 implementation may require Mahou code, decompilation, assets, localization, packet formats, class structure or implementation logic.

## Per-spell linkage

| Black Arcana spell | Observable/public reference | Stage 01 disposition | Black Arcana-owned specification | Host-authority boundary | Provenance conclusion |
| --- | --- | --- | --- | --- | --- |
| **Astral Severance** | `Mental Displacement` in the observable catalog: finite-radius astral projection / vulnerable-body reconnaissance | `REIMAGINE` → `Astral Severance` | `candidate-specifications.md` → Noetic / Astral Severance | Black Arcana owns projection session, physical-body vulnerability, return/control authority; Eidolon flavor remains optional `PROBE` | Original Black Arcana projection/session architecture may preserve the vulnerable-body reconnaissance fantasy, but not Mahou implementation details. Current lifecycle, representation, control transport, camera presentation and config authority are Black Arcana-owned runtime contracts. |
| **Namescry** | `Scrying`: temporary perception of a resolved loaded same-dimension target with visibility/privacy concerns | `REIMAGINE` → `Namescry` | `candidate-specifications.md` → Noetic / Namescry | Black Arcana owns privacy policy, target resolution and perception payload; Eidolon ritual presentation is optional `PROBE` | Original Black Arcana remote-perception contract may preserve the limited divination fantasy while enforcing loaded-only, privacy and no-force-load policy. No Mahou targeting/network implementation is imported. |
| **Gaze of Stillness** | `Binding gaze`: facing/eye-contact-oriented immobilization fantasy | `REIMAGINE` → `Gaze of Stillness` | `candidate-specifications.md` → Noetic / Gaze of Stillness | Black Arcana owns LOS/facing/CC and diminishing-return policy; Iron's may provide a public channeled invocation surface | Original Black Arcana CC policy reinterprets the gaze fantasy with bounded reciprocal facing/LOS and boss/PvP safety. Iron's hosting, where used, is an invocation/resource boundary rather than borrowed spell logic. |
| **Nullifying Gaze** | `Reversion`: cleansing/nullification fantasy with unsafe reference-specific immunity/behavior bypasses | `REIMAGINE` → `Nullifying Gaze` | `candidate-specifications.md` → Noetic / Nullifying Gaze | Black Arcana owns nullifiable/protected allowlists and explicit adapters; Iron's may host invocation | Original Black Arcana nullification is allowlist/tag/adapter driven. The reference behavior specifically motivates rejecting hardcoded cross-mod invariant/boss bypasses; no Mahou nullification implementation is reused. |
| **Occult Appraisal** | `Insight`: effects/held-item/inventory information fantasy with privacy risk | `REIMAGINE` → `Occult Appraisal` | `candidate-specifications.md` → Noetic / Occult Appraisal | Black Arcana owns metadata whitelist and privacy; Iron's presentation is optional | Original Black Arcana read-only appraisal exposes only approved metadata under server policy. Arbitrary capability/NBT/inventory access is not inherited from the reference. |
| **Borrowed Sight** | `Shared Vision`: viewing another entity/player's viewpoint | `REIMAGINE` → `Borrowed Sight` | `candidate-specifications.md` → Noetic / Borrowed Sight | Black Arcana owns camera/session recovery and consent policy; Ars familiar ownership may supply supported target identity | Original Black Arcana camera/session contract restricts the fantasy to owned familiars or explicitly consenting bonded targets. Arbitrary hostile-player surveillance is deliberately rejected. |
| **Pact Sanctuary** | `Familiar's Garden`: familiar-centered friendliness/non-hostility area | `REIMAGINE` → `Pact Sanctuary` | `candidate-specifications.md` → Noetic / Pact Sanctuary | Black Arcana owns aura scheduling/hostility policy; Ars familiar lifecycle/ownership is provider-bound only through supported seams | Original Black Arcana sanctuary is a bounded, temporary, eligibility-controlled AI/targeting influence with boss/event exclusions and no permanent faction mutation. No Mahou AI implementation is imported. |

## Provider-source boundary

The provider names in the table are not additional design references for spell behavior. They are possible integration surfaces governed by the existing provenance ledger and Stage 03/07 integration evidence.

- Iron's: use only documented/public API surfaces and exact-version contracts independently verified by Black Arcana for the **specific operation being integrated**. Verification of one operation does not authorize another; unverified operations remain fail-closed. Provider-native mana/cooldown must not become a second authority for Black Arcana-hosted transactions.
- Ars Nouveau: familiar ownership/lifecycle may be consumed only through supported provider boundaries independently verified for the **specific integration path**. Verification is operation-scoped; unsupported or unverified provider state remains fail-closed.
- Eidolon: thematic/ritual presentation remains optional unless a supported exact-version integration seam is separately proven for the required operation; Black Arcana mechanics must continue to function without undocumented Eidolon internals.

Theme, naming similarity or the existence of a similar provider mechanic is never sufficient evidence for an integration contract.

## What this closes

For Stage 07.07, this document supplies the required clean-room **per-spell provenance link** for Astral Severance, Namescry, Gaze of Stillness, Nullifying Gaze, Occult Appraisal, Borrowed Sight and Pact Sanctuary.

It does **not** close any remaining `MISSING / BLOCKER` or `PREPARATORY` field for resource cost, cooldown, scaling, progression, invocation, boss/PvP tuning, config tuning, tests or real-client acceptance. The Stage 07.07 specification gate remains authoritative for those fields and remains `IN PROGRESS` until they are independently frozen and evidenced.
