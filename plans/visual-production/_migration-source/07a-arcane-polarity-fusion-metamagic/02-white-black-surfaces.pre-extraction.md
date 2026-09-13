# 07A.02 — White/Black Identity Surfaces

## State

`PLANNED / NOT IMPLEMENTED`

## Objective

Give Luminal and Umbral magic distinct player-facing progression/presentation without creating new magic engines or replacing canonical Stage 07 mechanics.

## Umbral Codex

The planned Black Arcana identity for the requested black-magic grimoire role is **Umbral Codex**. `Darkhold` remains user/design shorthand only and must not ship as the Black Arcana identity.

The Codex may expose:

- discovered Umbral techniques;
- known bargains/contracts;
- danger/corruption warnings;
- provenance/lore entries;
- progression requirements;
- explicit indication of stolen/consensual/self-owned power sourcing.

It does not own mana, cooldown, spell execution, corruption, strain or ritual completion.

Stage 08 decides final unlock progression and whether the Codex is a physical item, UI surface, knowledge state or combination. Any physical item is optional presentation/access, not mandatory cast authority.

## Ankh of Continuance

The planned white-magic resurrection surface is **Ankh of Continuance**.

It is a ritual focus/token over the existing Stage 07.02 resurrection authority. It must not implement a separate death interception, second soul-charge ledger or independent respawn system.

Required composition:

`Ankh ritual/presentation -> canonical Stage 06 ritual completion -> canonical Soul Anchor/Mortal Ledger state -> canonical death settlement`

Rules:

- self-anchoring or explicitly consensual anchoring is Luminal-eligible;
- resurrection remains high-danger/forbidden regardless of Luminal polarity;
- charges/capacity stay bounded;
- repeated ritual completion is replay/idempotency protected;
- offline/dead-target behavior must follow the existing Souls & Death persistence contract;
- no infinite resurrection loop;
- no free charge from provider bridge failure.

### Eidolon routing

Eidolon: Repraised is the preferred ritual presentation language for occult altar/sigil preparation when the exact installed callback can prove the Black Arcana caster/session identity needed for one authoritative completion.

The existing project evidence already keeps player-specific Eidolon completion fail-closed where that identity cannot be proven. 07A must preserve that rule. It may improve the adapter only after exact-version evidence; it may not infer the caster from proximity, GUI user or last interactor.

### Malum routing

Malum spirits may participate only if the exact adapter exposes a real spirit cost/reservation that can satisfy D017. Do not make a Luminal resurrection secretly depend on stealing another living soul unless that is an explicit separate Umbral variant with distinct specification.

## Life stealing

The requested black-magic life theft maps to the already canonical Blood & Curses capability, principally `Sanguine Harvest`.

07A work is classification/composition, not a duplicate spell:

- unwilling vitality extraction -> Umbral;
- gained health/blood/resource cannot exceed bounded proven loss;
- no positive health<->mana/blood feedback loop;
- target caps and deterministic ordering remain canonical;
- boss/PvP reductions follow the existing spell specification;
- Stage 07.08 owns Hematic Reserve/Vampirism transfer semantics when implemented.

If a future consensual life-transfer rite is desired, specify it separately and prove consent server-side rather than weakening the theft rules.

## Presentation differentiation

White and black magic should feel mechanically and visually distinct without making color the authority.

Luminal presentation direction:

- precise geometric symmetry;
- restrained gold/ivory/blue-white palette where original assets support it;
- protective/continuity motifs;
- clear telegraphs for consent/benefit and death-state anchoring.

Umbral presentation direction:

- asymmetric/contractual/binding motifs;
- dark red/violet/black-gold palette where original assets support it;
- visible extraction link from source to beneficiary where gameplay readability benefits;
- explicit consequence feedback for Corruption/Strain.

These are presentation guidelines only. Server polarity remains source/agency-derived.

## Tests first

RED tests must prove:

- Ankh request cannot create a charge outside the canonical resurrection ledger;
- duplicate ritual completion cannot duplicate a charge;
- Eidolon callback without proven caster identity cannot award player-specific Ankh state;
- Sanguine Harvest is not double-applied by a new Umbral wrapper;
- vampire blood/thirst routes, once 07.08 exists, are not credited twice;
- a Luminal Ankh still receives its configured high-danger hazard profile;
- Codex/UI data cannot mutate server unlocks.

## Acceptance

- original player-facing identity;
- single resurrection authority;
- single life-drain authority;
- provider presentation is optional/fail-closed;
- no new resource economy introduced by either surface.
