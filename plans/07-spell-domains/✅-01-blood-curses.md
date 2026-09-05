# 07.01 — Blood & Curses

## State

`IMPLEMENTED / AUTOMATED VALIDATION GREEN / FINAL REAL-MODPACK VALIDATION DEFERRED`

Fresh latest-`main` resynchronization implemented on PR #45 from canonical Stage 06 baseline `6b77b5c0ec4f0ff4a8688bb105cef055860c061c`. Historical Stage 07 material was used only as reviewed source material; stale PR #22 ancestry was not merged wholesale.

## Candidate mechanics

Life drain, damage exchange/retribution, binding contracts, marks/curses and risk-reward blood casting.

The implemented 07.01 contract currently covers:

- **Blood Price** — bounded partial substitution of an ordinary provider-owned resource cost with real health; the original provider remains authoritative and the health reservation is transactional/refundable until canonical cast commit.
- **Equilibrium Rite** — bounded health transfer between loaded living entities; transfer is capped by source health above its floor, target missing health, request size and the global hard ceiling. The runtime revalidates target admission before mutation.
- **Sanguine Harvest** — bounded one-pulse drain over a bounded candidate list, with range/line-of-sight checks, player/boss exclusion, canonical entity admission, anti-farm weighting and settlement from actual delivered damage rather than requested damage.
- **Law of Recurrence** — bounded timed adaptation to stable semantic damage families; repeated families build capped resistance below immunity while switching family applies bounded vulnerability. Session state is pruned on server tick.
- **Sympathetic Wound** — bounded mirrored damage with a dedicated damage-type recursion marker, explicit propagated provenance, per-event/lifetime ceilings, player-target default denial, canonical target admission and cross-link recursion prevention.

## Balance rules

Health costs cannot create positive-feedback immortality; drain has target/category caps; reflected/replicated damage cannot recursively trigger itself; bosses/PvP use explicit conservative policy. Hard ceilings are centralized in `BloodSafetyCeilings` where applicable.

## Integration direction

Iron's remains authoritative for its mana resource path. `IronsBloodPriceCostProvider` composes Blood Price around the ordinary Iron's provider rather than replacing it, and resolves percent-of-max cost before substitution. Eligibility/progression ownership is injected rather than invented by the provider.

World/entity mutation uses frozen Stage 04 admission. Stage 05A remains authoritative for Arcane Danger/backlash; Blood & Curses does not create a parallel hazard pipeline. Arcane Backlash and Sympathetic Wound propagated damage are classified so they cannot recursively become ordinary direct Blood-domain damage.

## Automated acceptance evidence

The 07.01 implementation followed explicit RED → GREEN cycles on the fresh branch:

- Blood Price minimal quote RED: workflow `33632502573`; first GREEN: `33632911427`.
- Full pure/provider contract RED: workflow `33633554231`; production contracts subsequently compiled and passed against the current mainline APIs.
- Equilibrium Rite server contract RED: workflow `33636124328`; GREEN: workflow `33636681467`.
- Sanguine Harvest server contract RED: workflow `33637067030`; GREEN: workflow `33649642900`.
- Damage-family classifier RED: workflow `33650108293`; GREEN: workflow `33650649152`.
- Law of Recurrence runtime RED: workflow `33651074959`; GREEN: workflow `33651631641`.
- Sympathetic Wound runtime RED: workflow `33652083948`; GREEN: workflow `33654634485` on head `87cd68599a4358a00137fff52bdaed27d1a716ed`.

The final 07.01 GREEN run passed JUnit, diff sanity, NeoForge build, JAR inspection, all 34 required GameTests and dedicated-server smoke.

## Acceptance

Implemented curses/mechanics now have bounded state, source/provenance handling, expiry/cleanup where stateful, recursion guards where propagation exists, canonical admission before target mutation, and deterministic server GameTests. The PR diff against its Stage 06 base contains only shared Stage 07 specification primitives plus Blood & Curses production/tests; no 07.02–07.07 runtime implementation is present.

This automated evidence does **not** convert the deferred real-modpack/manual host campaign to PASS. Optional-provider and presentation acceptance that requires the full modpack remains deferred under D031.
