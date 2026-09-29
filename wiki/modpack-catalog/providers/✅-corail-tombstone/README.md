# Corail Tombstone — 9.5.6

Status: `✅ CATALOGED / EXACT PHYSICAL=PUBLISHER ARTIFACT / COMPLETE 22-ACTION-FAMILY CATALOG / 10 COUNTED_EXACT PRAYER-RITE ACTIONS / 12 EXACT DEDUPED CONFIG-CONDITIONAL CASTABLE ACTION FAMILIES / DEPLOYED ALLOW_* VALUES MISSING / RUNTIME QA FAIL-CLOSED`

> Folder-prefix rule (2026-09-29): **✅ means the current semantic/action denominator is fully cataloged and materialized.** Deployed config, reachability or runtime QA may still keep individual identities conditional or outside the strict numerator; those conditions remain documented here and do not make the folder structurally partial.

## Current physical identity

Current sibling authority:

``neoforge-rpg-skilltree` current `main` with Tombstone dossier blob `7b99ee63892e9bd3711e27a651c0b62c0d71ba47``

Certified dossier:

`PROJECT-INSTRUCTIONS/modlist/Adventure and RPG + Magic + Mobs + Utility & QoL/✅-corail-tombstone v9.5.6.md`

Physical identity preserved there:

- JAR: `tombstone-neoforge-1.21.1-9.5.6.jar`;
- mod id: `tombstone`;
- runtime: `9.5.6`;
- Minecraft 1.21.1 / NeoForge / Java 21.

The sibling dossier preserves filename/version but not the digest. Independent physical authority is supplied by the Project Library physical modlist snapshot `modlist(1).txt` (2026-09-16): its Tombstone row records SHA-1 `d830d16caa20b0d23a44ed6b1d339bc22afc2460`. That equals the audited publisher File `8842741` SHA-1, so installed physical bytes and the audited publisher artifact are exact-equal for this current 9.5.6 line.

## Exact publisher artifact

CurseForge project: `243707`.

Exact NeoForge 1.21.1 file:

- file ID: `8842741`;
- filename: `tombstone-neoforge-1.21.1-9.5.6.jar`;
- uploaded: 2026-09-09;
- Release;
- NeoForge 1.21.1.

Clean-room NON-MERGE audit of that exact artifact observed:

- bytes: `2,520,705`;
- SHA-1: `d830d16caa20b0d23a44ed6b1d339bc22afc2460`;
- SHA-256: `520e2a3cb5fb8001da20a23aaf39a7fd8fd937af962c2b43c55460099e30b23b`;
- 590 provider classes;
- 1,066 provider resources;
- 0 embedded jar-in-jar libraries.

Physical Project Library SHA-1 equality closes the installed artifact as the same bytes audited from publisher File `8842741`. The ten already-counted prayer/Ritual-Flute identities are therefore promoted in confidence from `COUNTED_RELEASE_BOUNDED` to `COUNTED_EXACT`; their cardinality does not change.

See `EXACT-9.5.6-ACTION-INVENTORY.md`.

Individual action cards: [`actions/README.md`](actions/README.md).

## Publisher-confirmed magic system

The current publisher description explicitly states that Tombstone has a magic system based on enchantable items powered by Souls haunting Decorative Graves.

The publisher also confirms:

- Ankh prayer near a Decorative Grave;
- Knowledge of Death progression;
- readable Forgotten Knowledge scrolls;
- Ritual Flute as loot used to start some forgotten-knowledge flows;
- Elyra's Diary unlocking enhanced prayers;
- Rite of Silent Bound;
- Souls used for magic scroll/tablet enchanting and Grave Key upgrades.

Naming reconciliation: the publisher prose uses **Rite of Silent Bound**, while the exact 9.5.6 artifact exposes **Rite of Silent Bond** / `NOTES_SILENT_BOND` / `trySilentBond(...)`. The catalog preserves the publisher wording as provenance but uses **Silent Bond** as the release-exact counted action identity.

These public facts are now reconciled against the exact 9.5.6 artifact rather than being the only evidence.

## Strict counted action surface

The exact release closes **10 provider-owned player-facing semantic magic actions** that are not item/status duplicates.

### Prayer actions — 6

1. Grave Prayer — exact `PrayerHelper.onGrave(...)` action plus publisher-documented Ankh prayer near a Decorative Grave;
2. Dissonance — exact provider bonus identity + `PrayerHelper.dissonance(...)`;
3. Empathy — exact provider bonus identity + `PrayerHelper.empathy(...)`;
4. Harmonization — exact provider bonus identity + `PrayerHelper.harmonization(...)`;
5. Protection — exact provider bonus/stat/action identity + `PrayerHelper.protection(...)`;
6. Undead — exact provider bonus identity + `PrayerHelper.undead(...)`.

`exorcism(...)` and `zombify(...)` are implementation branches/helpers and are not promoted to separate player-facing identities.

Exact reachability support:

- the exact artifact packages `data/tombstone/recipe/ankh_of_prayer.json`;
- the matching recipe advancement is packaged;
- current publisher documentation independently describes the Ankh prayer loop;
- the exact config surface exposes `prayerCooldown`, not a prayer-disable switch;
- Elyra's Diary is referenced by the exact PrayerHelper surface and the publisher documents it as the enhanced-prayer unlock.

### Ritual Flute actions — 4

The exact `ItemRitualFlute` signature exposes four distinct note/action paths:

1. Heal Dead Coral — `NOTES_HEAL_DEAD_CORAL` / `tryHealDeadCoral(...)`;
2. Coral Chant — `NOTES_CORAL_CHANT` / `tryCoralChant(...)`;
3. Remanence — `NOTES_REMANENCE` / `tryRemanence(...)`;
4. Silent Bond — `NOTES_SILENT_BOND` / `trySilentBond(...)`.

The exact config scan found no Ritual Flute/rite enable-disable field. Current publisher documentation says the Ritual Flute can be found as loot and is used to begin some Forgotten Knowledge flows.

### Semantic state

These ten identities are:

`COUNTED_EXACT = 10`

Provider-specific strict semantic delta from this checkpoint:

**+10**

Shared global semantic ledgers are intentionally not changed in this provider-specific PR; they should be reconciled separately after this provider checkpoint merges.

## Explicit exclusions

### Scroll buffs — +0

Exact enum `ItemScrollBuff$SpellBuff` contains 11 variants:

- Preservation;
- Unstable Intangibility;
- Feather Fall;
- Purification;
- True Sight;
- Reach;
- Lightning Resistance;
- Frost Resistance;
- Aquatic Life;
- Mercy;
- Projectile Reflection.

Each variant maps to a `MobEffect` supplier. The Black Arcana semantic metric excludes status/effect identities and physical item wrappers around them.

Therefore:

**11 scroll-buff variants = +0 semantic actions.**

### Enchantments/effects — +0

The publisher-listed 13 enchantments remain gear identities.

The publisher-listed 24 effects remain status identities.

Neither family enters the strict semantic action numerator.

### Forgotten Knowledge documents — +0 by themselves

Exact `ReadableScrollType` identities:

- Rite of Silent Bond;
- Elyra's Diary;
- Coral Chant;
- Erdos Fragments;
- Nights of Nour.

These are progression/lore documents. Their resulting prayer/rite actions are counted once under the action owner; the documents themselves add zero.

### Books and progression state — +0 by themselves

Books, Souls, Knowledge of Death points/perks and advancement/progression records are support/progression surfaces unless they independently mint a player-facing action identity.

## Remaining conditional action candidates

The exact 9.5.6 artifact exposes additional active `ItemCastableMagic`/magic-item surfaces, but the provider has per-item `allow_*` config for them and the deployed pack config is unavailable.

Examples include:

- Tablet of Assistance;
- Tablet of Cupidity;
- Tablet of Guard;
- Tablet of Home;
- Tablet of Recall;
- Gemstone of Familiar;
- Gemstone of Guardian;
- Gemstone of Merchant;
- Grave Key;
- Lost Tablet;
- Magic Scroll;
- Scroll of Knowledge.

These are **not added to the strict numerator** in this checkpoint.

Gemstone of Prayer is treated as an invocation/support surface for the already-counted prayer family, not a new prayer identity.

Exact semantic deduplication of these 12 candidates is now closed by the hash-matched 9.5.6 castable-surface audit. Each candidate maps to one action family and one provider `allow_*` eligibility gate; internal modes/effects are not multiplied into extra identities. See `EXACT-9.5.6-CONDITIONAL-CASTABLE-MATRIX.md`. Only the deployed `AllowedMagicItems` values remain before any of these 12 families can enter the strict numerator.

The read-only collection path is standardized by [`docs/qa/provider-catalog-deployed-evidence.md`](../../../../docs/qa/provider-catalog-deployed-evidence.md): it records only the exact 9.5.6 physical fingerprint comparison plus the 12 Tombstone eligibility booleans relevant to these candidates from bounded deployed config roots. Canonical acceptance steps are in [`DEPLOYED-CONFIG-CHECKLIST.md`](DEPLOYED-CONFIG-CHECKLIST.md). No actual current-instance value has been captured by this repository checkpoint; the provider therefore remains fail-closed.

## Runtime / authority boundary

Corail Tombstone remains authority for:

- grave creation/recovery;
- Grave Souls and magic items;
- Knowledge of Death/perks;
- Forgotten Knowledge;
- provider prayers and Ritual Flute action state;
- provider enchantments/effects;
- Tombstone teleport/death utilities.

Black Arcana must not duplicate those runtimes. RPG Skill Tree remains progression/Mastery/perk/gate authority only where a real contract exists; Tombstone's Knowledge of Death remains provider-owned state.

## Still fail-closed

- deployed `AllowedMagicItems` state for the 12 exact one-to-one action gates;
- strict promotion of the corresponding enabled conditional action families;
- exact resource/Soul consumption and exactly-once settlement;
- prayer/rite persistence and multiplayer authority;
- Knowledge of Death persistence;
- death/grave/XP restoration;
- Create Aeronautics respawn-on-vehicle;
- Curios/external inventory recovery;
- multiplayer ownership/protection;
- restart/reload/migration behavior;
- any Black Arcana adapter.

## Result

**✅ Catalog complete at the known 9.5.6 action-family level; deployed `allow_*` values remain conditional.**

The exact physical=publisher 9.5.6 artifact closes **10 `COUNTED_EXACT` semantic prayer/rite actions** and multiple explicit zero-semantic families. The remaining magic-item surface is exactly deduplicated to **12 config-gated action families**; provider config, not semantic identity ambiguity, is now the catalog blocker.

Provider strict semantic delta: **+10**.
