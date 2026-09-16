# Apprentice's Codex — support-content index

Source checkpoint: `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e` / installed provider `0.9.7.1`.

This file is a navigation boundary only. Detailed registry authorities are intentionally split to avoid duplicated inventories drifting apart.

## Canonical registry catalogs

- [`ITEM-CATALOG.md`](ITEM-CATALOG.md) — **167/167** provider item registry IDs frozen; functional behavior audit remains selective for high-impact item families.
- [`BLOCK-CATALOG.md`](BLOCK-CATALOG.md) — **20/20** provider block registry IDs frozen; spell-created blocks separated from player infrastructure/stations.
- [`EFFECTS-AND-ATTRIBUTES.md`](EFFECTS-AND-ATTRIBUTES.md) — **20** static effect IDs, **25** School-Affinity effect slots and the provider's synced `max_enchantment_table_level` attribute.
- [`SCHOOL-AFFINITY.md`](SCHOOL-AFFINITY.md) — exact dynamic school assignment, +10% spell-power-per-effect-level modifier and potion variants.
- [`ACQUISITION.md`](ACQUISITION.md) — recipes, loot, Errand Mage trades and per-spell acquisition eligibility rules.
- [`COMPATIBILITY.md`](COMPATIBILITY.md) — optional compatibility packages reconciled with the physical modpack.

## Authority rule

Registry identity proves provider ownership, not a universal integration hook. Exact item/block/effect behavior must be audited at the owning class/version before a future bridge consumes it. Black Arcana must not clone provider state or re-settle provider effects merely because a registry entry is observable.
