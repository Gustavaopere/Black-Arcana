# Ars Additions 21.3.0 — Direct magical items

Status: `SOURCE-PINNED / DIRECT ITEM CATALOG IN PROGRESS / RUNTIME+PACK QA PENDING`

Exact source pin: `Jarva/Ars-Additions@91f102a90dc058cf40e4eac5a67a881e48b856b4`.

The exact `AddonItemRegistry` registers 14 direct items plus 12 dynamically registered charms. Charms are cataloged separately under [`../charms/`](../charms/). Stateful items that require a larger authority discussion are also cross-linked to [`../systems/`](../systems/).

## Direct item inventory — 14/14 identities

1. Warp Index — `ars_additions:warp_index`
2. Stabilized Warp Index — `ars_additions:stabilized_warp_index`
3. Codex Entry — `ars_additions:codex_entry`
4. Lost Codex Entry — `ars_additions:lost_codex_entry`
5. Ancient Codex Entry — `ars_additions:ancient_codex_entry`
6. Unstable Reliquary — `ars_additions:unstable_reliquary`
7. Explorer's Warp Scroll — `ars_additions:exploration_warp_scroll`
8. Nexus Warp Scroll — `ars_additions:nexus_warp_scroll`
9. XP Jar — `ars_additions:xp_jar`
10. Handy Haversack — `ars_additions:handy_haversack`
11. Advanced Dominion Wand — `ars_additions:advanced_dominion_wand`
12. Wayfinder — `ars_additions:wayfinder`
13. Imbued Spell Parchment — `ars_additions:imbued_spell_parchment`
14. Memory Crystal — `ars_additions:memory_crystal`

## Detailed pages

- [Codex Entries](codex-entries.md)
- [Unstable Reliquary](unstable-reliquary.md)
- [Explorer's Warp Scroll](exploration-warp-scroll.md)
- [Nexus Warp Scroll](nexus-warp-scroll.md)
- [Imbued Spell Parchment](imbued-spell-parchment.md)
- [Wayfinder](wayfinder.md)

System pages cover Warp Index/Warp Nexus, XP Jar, Handy Haversack, Advanced Dominion Wand and Memory Crystal.

## Black Arcana boundary

Direct item identity does not transfer runtime authority. Glyph unlocks, Ars spell execution, warp data, vanilla XP conversion, Source accounting and provider inventories continue to be settled by Ars Nouveau / Ars Additions. Black Arcana observes only through verified hooks and never infers a second cast or resource transaction from possession/use of these items.
