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

Exact castable/action surfaces are now deduplicated one-to-one against provider `allow_*` gates:

1. Tablet of Assistance — player-assistance/join teleport request;
2. Tablet of Cupidity — randomized location-search/relocation;
3. Tablet of Guard — Spectral Wolf summon;
4. Tablet of Home — respawn/home teleport;
5. Tablet of Recall — bound-location teleport;
6. Gemstone of Familiar — familiar revival;
7. Gemstone of Guardian — Grave Guardian summon;
8. Gemstone of Merchant — merchant/villager trade-level improvement;
9. Grave Key — grave/tomb-location teleport;
10. Lost Tablet — one destination-discovery/travel family with `EXPLORATION/VILLAGE/TREASURE` modes;
11. Magic Scroll — one generic MobEffect-casting wrapper; individual effects remain non-additive;
12. Scroll of Knowledge — one XP/knowledge storage-recovery/reward family; internal readable-scroll rewards remain non-additive.

Conditional ceiling: **+12** if all twelve deployed eligibility booleans are enabled.

These remain outside the strict sum because the actual deployed booleans are not present in repository evidence.

## Evidence state

`COUNTED_RELEASE_BOUNDED` because exact publisher File `8842741` was audited, but the installed physical row has no independent cryptographic digest.

Provider delta: **+10**.

The shared global ledger should add this delta in a separate post-merge reconciliation; this provider-specific file does not assert a new global total.
