# Semantic Magic Delta — Corail Tombstone 9.5.6

Status: `+10 COUNTED_RELEASE_BOUNDED / PROVIDER STILL PARTIAL`

## Counted identities

### Prayer family — 6

1. Grave Prayer;
2. Dissonance;
3. Empathy;
4. Harmonization;
5. Protection;
6. Undead.

### Ritual Flute — 4

7. Heal Dead Coral;
8. Coral Chant;
9. Remanence;
10. Silent Bond.

## Deduplication/exclusions

Not additive:

- `exorcism` and `zombify` — internal behavioral branches without separate player-facing prayer identity;
- Gemstone of Prayer — invocation/support for the prayer family;
- 11 ScrollBuff variants — MobEffect physicalizations;
- 5 readable Forgotten Knowledge document types — progression/lore;
- 13 enchantments — gear;
- 24 effects — statuses;
- Souls/Knowledge points/perks — resource/progression state.

## Conditional, not strict-counted

Exact castable/action surfaces with provider-specific `allow_*` config and no deployed value:

- five magic tablets;
- Familiar/Guardian/Merchant gemstones;
- Grave Key;
- Lost Tablet;
- Magic Scroll;
- Scroll of Knowledge.

These remain outside the strict sum.

## Evidence state

`COUNTED_RELEASE_BOUNDED` because exact publisher File `8842741` was audited, but the installed physical row has no independent cryptographic digest.

Provider delta: **+10**.

The shared global ledger should add this delta in a separate post-merge reconciliation; this provider-specific file does not assert a new global total.
