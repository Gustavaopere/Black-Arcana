# Capability Matrix Delta — Ars Additions 21.3.0

Status: `PHASE 2Q / SOURCE-PINNED PROVIDER DELTA / RUNTIME+PACK QA PENDING`

Provider authority in this file is restricted to installed `ars_additions` 21.3.0 and factual source pin `Jarva/Ars-Additions@91f102a90dc058cf40e4eac5a67a881e48b856b4`.

| Capability surface | Ars Additions evidence | Disposition for Black Arcana |
|---|---|---|
| reactive targeting | Retaliate resolves against provider/vanilla last-attacker state | `OVERLAP`; do not duplicate reactive-target resolution; five-second description remains runtime QA |
| persistent target references | Mark stores block/entity/player references in Unstable Reliquary; Recall resolves through that provider state | `STRONG OVERLAP`; Black Arcana remote targeting must use its own approved identity/safety contracts, not read Reliquary data heuristically |
| remote/cross-dimensional storage access | Warp Index controls Ars Storage/Crafting Lecterns; Stabilized Warp Index removes same-dimension restriction but still requires loaded target state | `EXISTING PROVIDER AUTHORITY`; no second remote-container authority and no force-load inference |
| teleport/warp network | Warp Nexus + Nexus Warp Scroll + Explorer's Warp Scroll use provider WarpScrollData/teleport infrastructure | `STRONG OVERLAP`; Black Arcana Space & Displacement keeps its own server validation/safe-destination authority and must not replay provider teleport |
| Source economy | Ender Source Jar persists a UUID-keyed global Source pool; Warp Nexus/Spawner/Ritual systems consume Ars Source | `EXISTING PROVIDER AUTHORITY`; never mirror/convert into Black Arcana resource state |
| force loading | Arcane Permanence explicitly force-loads a bounded configurable chunk area | `PROVIDER-OWNED EXCEPTION`; Black Arcana no-force-load policy remains unchanged and cannot inherit this permission |
| structure location | Locate Structure has 15 built-in recipes and async provider search with configurable thread pool | `EXISTING PROVIDER AUTHORITY`; do not perform a second unbounded search or treat a located point as world-effect authorization |
| entity spawning/replication | Source Spawner reconstructs entities from Mob Jar context with recipe/denylist/Source checks | `EXISTING PROVIDER AUTHORITY`; no duplicate spawn settlement, loot/mastery credit or global scans |
| remote inventory routing | Handy Haversack binds `GlobalPos` + side/filter state and only obtains a handler when target dimension/chunk is loaded | `EXISTING PROVIDER AUTHORITY`; no force-load, no duplicate pickup/transfer processing |
| configuration/state transfer | Memory Crystal stores 10 provider-defined slots and delegates payload interpretation to registered MemoryHandlers | `EXISTING PROVIDER AUTHORITY`; Black Arcana must not deserialize arbitrary provider NBT as spell state |
| mass linking/configuration | Advanced Dominion Wand sends candidate targets but server revalidates held item, origin, <=1000 targets, <=128-block distance and claim permission | `SERVER-AUTHORITY EXEMPLAR`; do not trust client target lists and do not duplicate provider link callbacks |
| consumable zero-mana spell casting | Imbued Spell Parchment stores a spell, makes its provider cost zero and consumes itself after successful cast | `EXISTING PROVIDER AUTHORITY`; do not add a second mana charge or independent Black Arcana cast settlement |
| glyph learning | Codex Entry variants unlock one unknown eligible Ars glyph of their tier or fall back to vanilla XP | `EXISTING PROVIDER AUTHORITY`; no duplicate glyph/progression ledger |
| protective/utility charms | 12/12 charms use provider event hooks/charges and can be discovered across hands, Curios and inventory | `EXISTING PROVIDER AUTHORITY`; do not reapply protection based on item presence or assume Curios-only activation |
| armor Thread slots | Spellweave adds Ars perk-slot capability to eligible non-Ars armor through provider mixins/data components | `CROSS-PROVIDER OVERLAP`; RPG Skill Tree/Black Arcana must not interpret the same slots as a second perk system |
| Ars crafting automation | Enchanting Wixie extends Ars Wixie/Enchanting Apparatus and routes completed outputs to a bound storage target | `EXISTING PROVIDER AUTHORITY`; do not duplicate recipe execution or output insertion |
| bulk scribing | addon recipe system extends Scribes Table workflows with Source-backed bulk output | `EXISTING PROVIDER AUTHORITY`; provider owns recipe/resource settlement |
| worldgen/progression structures | Arcane Library, Nexus Tower and Ruined Warp Portal families provide provider loot/transport/progression surfaces | `WORLDGEN AUTHORITY`; Black Arcana may observe them but does not claim or mutate them outside normal world-safety policy |
| local weather infrastructure | codecs/components/attachments exist, but audited production path is dormant | `DO NOT PROMOTE`; registered plumbing is not active magic without executable evidence |

## Cross-provider rules

1. Ars Nouveau remains authority for mana, Source primitives, spell grammar/resolver, glyph capability and the base ritual/automation framework.
2. Ars Additions child/provider actions remain within the originating Ars causal action; Black Arcana must not double-charge mana/Source, Mastery, Arcane Danger or cooldowns.
3. Client packets or UI previews never become authority. Where Ars Additions itself revalidates candidate lists server-side, Black Arcana preserves the same architectural principle for its own systems.
4. Provider force loading is not precedent for Black Arcana force loading.
5. Any future adapter requires a real exact-version seam; item names, visuals, NBT guesses or spatial proximity are insufficient.

## Remaining validation

Installed-JAR runtime behavior against Ars Nouveau 5.13.1, effective config/datapack overrides, event ordering with the full pack, client UI/presentation and full dedicated-server/modpack QA remain separate from this source-catalog delta.
