# 07A.01 — Polarity, Source & Agency

## State

`PLANNED / NOT IMPLEMENTED`

## Objective

Freeze a deterministic server-side classification for Luminal (white), Umbral (black) and neutral Arcane magic without reducing polarity to damage type or visual style.

## Contract to implement

Introduce a Black Arcana-owned semantic contract conceptually containing:

- power-source category;
- agency/consent category;
- whether a living owner, soul owner, identity owner or world resource is being depleted/coerced;
- the resolved polarity;
- provenance/reason code suitable for diagnostics and tests.

Names and exact Java types are implementation decisions. The contract must be immutable at cast preflight and derived from server-owned spell/resource/target state.

### Planned source categories

At minimum distinguish:

- self-owned resource;
- explicitly consensual transfer;
- bounded ambient/non-owned resource;
- provider-owned ordinary spell resource;
- living vitality extraction;
- blood extraction;
- soul/spirit extraction;
- coerced agency/contract;
- identity/authority theft;
- parasitic world-state extraction.

Do not infer consent from team membership, friendliness or absence of resistance. Consent requires an explicit server-owned contract or a mechanic whose specification defines voluntary transfer unambiguously.

## Resolution rules

1. non-consensual living/soul/agency theft resolves Umbral;
2. self-owned or proven consensual restorative/warding costs may resolve Luminal;
3. ordinary provider mana/Source expenditure is not automatically white; it is normally neutral unless the spell contract supplies a stronger source/agency meaning;
4. dealing damage does not make a spell black;
5. healing does not make a spell white when the healing is funded by stolen life/soul/resource;
6. polarity must be recomputed after metamagic changes sourcing;
7. mixed-source casts resolve by the strongest disqualifying extractive component unless a spell-specific reviewed rule says otherwise;
8. unknown provider/source semantics fail closed to neutral for presentation and cannot be promoted to Luminal for gates/benefits;
9. unknown consent never converts an extractive mechanic into Luminal;
10. polarity does not replace danger profile, Corruption or Strain.

## Existing-content migration audit

Before adding new mechanics, audit every canonical Stage 07 spell specification and assign one of:

- fixed Luminal;
- fixed Umbral;
- fixed Arcane;
- context-derived polarity;
- not classifiable until prerequisite provider/resource semantics are implemented.

Required special cases:

- `Sanguine Harvest`: Umbral when draining unwilling targets; do not create a duplicate drain runtime;
- Blood Price/self-health costs: self-sacrifice alone is not automatically Umbral;
- Soul Anchor/Mortal Ledger resurrection: Luminal-eligible when self/consensual but still high-danger;
- Black Flame: visual darkness does not decide polarity;
- spatial/projective magic: normally Arcane unless its resource/agency contract makes it otherwise;
- Borrowed Authority / authority theft fantasies: Umbral when the authority is taken without consent.

## Planned implementation surfaces

Expected future changes, to be verified against the then-current tree before coding:

- add polarity metadata/derivation under `src/main/java/dev/gustavopere/blackarcana/core/domain/` or a narrower cross-domain package;
- extend authoritative spell/domain specifications only through a versioned bounded schema;
- expose read-only presentation metadata to client synchronization without accepting client-authored polarity;
- integrate the resolved polarity into hazard/progression policy only through explicit interfaces, never by direct mutation of Corruption/Strain storage.

Do not create these paths/types blindly if the tree has changed before implementation.

## Tests first

RED tests must cover:

- fire/damage spell can remain Arcane/Luminal;
- stolen-life heal is Umbral;
- voluntary self-cost is not forced Umbral;
- explicit consensual transfer differs from forced transfer;
- mixed source with one non-consensual soul/life component resolves Umbral;
- unknown consent cannot produce Luminal;
- client packet cannot override server polarity;
- identical server inputs produce deterministic result;
- metamagic source rewrite triggers a new preflight classification, not a stale cached value.

## Acceptance

- one deterministic server-owned polarity resolver;
- no damage-based shortcut;
- no duplicated hazard state;
- every canonical Stage 07 mechanic has a disposition or explicit blocked reason;
- terminology/localization remains original Black Arcana identity.
