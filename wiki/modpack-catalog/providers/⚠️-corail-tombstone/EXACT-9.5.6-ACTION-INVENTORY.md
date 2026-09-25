# Corail Tombstone 9.5.6 — exact publisher-artifact action inventory

Status: `EXACT PUBLISHER FILE 8842741 / CLEAN-ROOM STRUCTURAL INVENTORY / 10 COUNTED_RELEASE_BOUNDED ACTIONS / 12 EXACT DEDUPED CONFIG-CONDITIONAL ACTION FAMILIES / DEPLOYED ALLOW_* VALUES MISSING`

## Evidence boundary

Physical pack identity:

- `tombstone-neoforge-1.21.1-9.5.6.jar`;
- mod id `tombstone`;
- runtime `9.5.6`.

Current sibling authority:

`neoforge-rpg-skilltree@0ff0ea0ba454e00713d7bf7e6d8255532470993b`

The sibling does not preserve an independent physical SHA for this row.

Exact publisher artifact:

- CurseForge project `243707`;
- file `8842741`;
- `tombstone-neoforge-1.21.1-9.5.6.jar`;
- SHA-1 `d830d16caa20b0d23a44ed6b1d339bc22afc2460`;
- SHA-256 `520e2a3cb5fb8001da20a23aaf39a7fd8fd937af962c2b43c55460099e30b23b`;
- 2,520,705 bytes.

Evidence state: **release-bounded**, not installed-byte exact.

## NON-MERGE audit checkpoints

Temporary branch:

`feat/audit-corail-tombstone-9.5.6-non-merge-2026-09-24`

Relevant audit runs:

- `36089593345` — exact artifact structural discovery;
- `36089818195` — executable item surface map;
- `36090145572` — prayer/rite identity map;
- `36090293508` — structured reachability/config token scan;
- `36090398893` — focused prayer config signatures.

Temporary workflows/scripts are audit-only and must not be merged into the durable catalog.

## Artifact shape

Exact publisher artifact:

- 590 classes under the Tombstone provider package;
- 1,066 provider resources;
- 0 jar-in-jar libraries.

## Counted prayer identities

| Identity | Exact release evidence | State |
|---|---|---|
| Grave Prayer | `PrayerHelper.onGrave(...)`; `PRAY_ON_GRAVE`; exact Ankh recipe; publisher Ankh prayer documentation | `COUNTED_RELEASE_BOUNDED` |
| Dissonance | `bonus.tombstone.pray_of_dissonance`; `PrayerHelper.dissonance(...)` | `COUNTED_RELEASE_BOUNDED` |
| Empathy | `bonus.tombstone.pray_of_empathy`; `PrayerHelper.empathy(...)` | `COUNTED_RELEASE_BOUNDED` |
| Harmonization | `bonus.tombstone.pray_of_harmonization`; `PrayerHelper.harmonization(...)` | `COUNTED_RELEASE_BOUNDED` |
| Protection | `bonus.tombstone.pray_of_protection`; `PrayerHelper.protection(...)`; provider stat/advancement identities | `COUNTED_RELEASE_BOUNDED` |
| Undead | `bonus.tombstone.pray_of_undead`; `PrayerHelper.undead(...)` | `COUNTED_RELEASE_BOUNDED` |

Exact config signatures relevant to this family expose `prayerCooldown`. No exact prayer enable/disable field was observed.

`exorcism(...)` and `zombify(...)` are not counted independently because the artifact does not expose separate player-facing prayer identities for them; they remain internal behavioral branches.

Prayer subtotal: **6**.

## Counted Ritual Flute identities

Exact `ItemRitualFlute` signatures expose:

| Identity | Exact signature evidence | State |
|---|---|---|
| Heal Dead Coral | `NOTES_HEAL_DEAD_CORAL`; `tryHealDeadCoral(...)` | `COUNTED_RELEASE_BOUNDED` |
| Coral Chant | `NOTES_CORAL_CHANT`; `tryCoralChant(...)` | `COUNTED_RELEASE_BOUNDED` |
| Remanence | `NOTES_REMANENCE`; `tryRemanence(...)` | `COUNTED_RELEASE_BOUNDED` |
| Silent Bond | `NOTES_SILENT_BOND`; `trySilentBond(...)` | `COUNTED_RELEASE_BOUNDED` |

The exact config scan found no `ritual_flute` enable/disable token and no server/common config token for Coral Chant, Remanence or Silent Bond.

Naming reconciliation: publisher-facing prose has used **Rite of Silent Bound**. The exact 9.5.6 artifact instead exposes `NOTES_SILENT_BOND`, `trySilentBond(...)` and `ReadableScrollType` = **Rite of Silent Bond**. For current release identity/accounting, the exact artifact spelling **Silent Bond** controls.

Current publisher documentation independently states that Ritual Flute can be found as loot to begin some Forgotten Knowledge flows.

Ritual Flute subtotal: **4**.

## Strict counted total

`6 prayers + 4 Ritual Flute actions = 10`

Strict provider contribution from this checkpoint:

**+10 `COUNTED_RELEASE_BOUNDED`**

## Excluded duplicate/support surfaces

### Scroll buffs

Exact enum `ItemScrollBuff$SpellBuff` has 11 constants:

1. Preservation;
2. Unstable Intangibility;
3. Feather Fall;
4. Purification;
5. True Sight;
6. Reach;
7. Lightning Resistance;
8. Frost Resistance;
9. Aquatic Life;
10. Mercy;
11. Projectile Reflection.

Each enum identity stores a `MobEffect` supplier. Under the canonical metric, status effects and their physical scroll wrapper are excluded.

Semantic contribution: **+0**.

### Forgotten Knowledge readable scrolls

Exact `ReadableScrollType`:

- Rite of Silent Bond;
- Elyra's Diary;
- Coral Chant;
- Erdos Fragments;
- Nights of Nour.

These are lore/progression documents, not additional casts. Actions they unlock are counted once under prayer/rite ownership.

Semantic contribution: **+0 by themselves**.

### Enchantments/effects

- 13 publisher-listed enchantments: gear identities;
- 24 publisher-listed effects: status identities.

Semantic contribution: **+0**.

## Conditional exact-release action candidates

The exact config exposes independent `allow_*` booleans for additional active magic-item families; deployed values are not present in repository evidence.

### Five tablets

- Tablet of Assistance;
- Tablet of Cupidity;
- Tablet of Guard;
- Tablet of Home;
- Tablet of Recall.

Each exact class extends `ItemTablet` / `ItemCastableMagic` and exposes provider `doEffects(...)`.

Current state: **CONDITIONAL**.

### Three non-prayer gemstones

- Gemstone of Familiar;
- Gemstone of Guardian;
- Gemstone of Merchant.

Each exact class extends `ItemCastableMagic` and exposes `doEffects(...)`.

Current state: **CONDITIONAL**.

Gemstone of Prayer is not counted separately from the prayer action family.

### Other config-gated castable candidates

- Grave Key;
- Lost Tablet;
- Magic Scroll;
- Scroll of Knowledge.

A later exact hash-matched castable-surface audit resolves these together with the tablets/gemstones to **12 one-to-one action families**. The semantic ambiguity in this section is superseded by [`EXACT-9.5.6-CONDITIONAL-CASTABLE-MATRIX.md`](EXACT-9.5.6-CONDITIONAL-CASTABLE-MATRIX.md).

These candidates do not enter the strict +10 until the corresponding deployed `allow_*` values are known.

## Clean-room boundary

Recorded facts are limited to cryptographic digests, archive counts/resource paths, exact type/field/enum identities, method signatures, structured recipe/advancement references and configuration field names.

No implementation bodies, assets, models, textures or sounds are copied into Black Arcana.

## Result

Current exact-release semantic state:

- **10 counted release-bounded actions**;
- explicit effect/gear/lore exclusions;
- 12 exact deduplicated config-sensitive castable action families remain conditional on deployed booleans;
- provider remains **⚠️ partial / conditioned**.

This closes the previous no-positive-cardinality blocker without falsely claiming total provider closure.
