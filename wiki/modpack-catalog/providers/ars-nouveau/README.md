# Ars Nouveau — Core Compositional Spell Provider

Status: `CORE SPELL MODEL VERIFIED; BASE GLYPH INVENTORY NORMALIZED FROM CURRENT 1.21.1 GUIDE; ADDON PROVIDERS CATALOGED SEPARATELY`

- Current JAR: `ars_nouveau-1.21.1-5.13.1.jar`
- Mod id: `ars_nouveau`
- Runtime version: `5.13.1`
- Provider class: `ENGINE / PRIMARY PROVIDER`

## Why Ars is cataloged differently

Ars Nouveau does not primarily expose a fixed list of finished spells. The player composes spells from **Glyphs**.

The current 1.21.1 Ars guide defines three major glyph categories:

- **Forms** — delivery/targeting method. A spell begins with one Form;
- **Effects** — actions resolved by the spell, and multiple Effects may be chained in order;
- **Augments** — modifiers applied to the compatible Form/Effect to their left.

Glyphs are tiered I/II/III. Higher-tier spell books unlock higher-tier glyph use. Casting consumes the Ars **player mana** authority; **Source** is a separate Ars world/crafting/automation resource and must not be conflated with player mana.

Therefore Phase 2 catalogs the finite glyph primitives and rituals, then maps their semantic capabilities. It does **not** enumerate every possible player-created spell chain.

## Current official 1.21.1 guide as provider-aware catalog

The current Ars guide aggregates Ars Nouveau and addon glyphs but exposes a registry ID for each entry. Phase 2 assigns ownership by namespace rather than treating every entry on that page as Ars Nouveau core.

Examples:

- `ars_nouveau:glyph_blink` → Ars Nouveau;
- `ars_elemental:glyph_life_link` → Ars Elemental;
- `ars_controle:glyph_filter_random` → Ars Controle;
- `ars_zero:effect_geometrize` → Ars Zero.

This namespace rule is essential for provider→capability coverage.

## Ars Nouveau core forms verified in the current guide

| Display | Registry id | Tier | Base cost |
|---|---|---:|---:|
| Projectile | `ars_nouveau:glyph_projectile` | 1 | 10 |
| Self | `ars_nouveau:glyph_self` | 1 | 10 |
| Touch | `ars_nouveau:glyph_touch` | 1 | 5 |
| Underfoot | `ars_nouveau:glyph_underfoot` | 1 | 5 |
| Pantomime | `ars_nouveau:glyph_pantomime` | 1 | 5 |

`Pantomime` resolves against the nearest block in line of sight and therefore occupies ranged block-targeting space even without using Projectile.

## Ars Nouveau core augments verified in the current guide

| Display | Registry id | Tier | Base cost | Semantic role |
|---|---|---:|---:|---|
| Amplify | `ars_nouveau:glyph_amplify` | 1 | 20 | power scaling |
| Sensitive | `ars_nouveau:glyph_sensitive` | 1 | 10 | changes targeting rules / effect behavior |
| Randomize | `ars_nouveau:glyph_randomize` | 1 | 0 | randomizes supported behavior/selection |
| Accelerate | `ars_nouveau:glyph_accelerate` | 2 | 10 | projectile speed up |
| AOE | `ars_nouveau:glyph_aoe` | 2 | 35 | area scaling |
| Dampen | `ars_nouveau:glyph_dampen` | 2 | 0 | power reduction / semantic modifier |
| Decelerate | `ars_nouveau:glyph_decelerate` | 2 | 5 | projectile speed down |
| Extend Time | `ars_nouveau:glyph_extend_time` | 2 | 10 | duration scaling |
| Extract | `ars_nouveau:glyph_extract` | 2 | 30 | silk-touch / non-destructive extraction semantics |
| Luck | `ars_nouveau:glyph_fortune` | 2 | 80 | loot/drop modifier |
| Pierce | `ars_nouveau:glyph_pierce` | 2 | 40 | penetration/depth/continuation |
| Reduce Time | `ars_nouveau:glyph_duration_down` | 2 | 15 | duration reduction |
| Split | `ars_nouveau:glyph_split` | 3 | 20 | multi-projectile / multi-resolution expansion |

## Ars Nouveau core effects verified in the current guide

The table below is a finite primitive inventory, not a set of prescribed spell recipes.

| Effect | Registry id | Tier | Base cost | Capability family |
|---|---|---:|---:|---|
| Access Ender Inventory | `ars_nouveau:glyph_ender_inventory` | 2 | 50 | remote storage |
| Animate Block | `ars_nouveau:glyph_animate_block` | 2 | 200 | summon / block manipulation |
| Blink | `ars_nouveau:glyph_blink` | 3 | 50 | teleport / warp |
| Bounce | `ars_nouveau:glyph_bounce` | 1 | 50 | mobility |
| Break | `ars_nouveau:glyph_break` | 1 | 10 | block breaking |
| Bubble | `ars_nouveau:glyph_bubble` | 1 | 20 | crowd control / lift |
| Burst | `ars_nouveau:glyph_burst` | 3 | 500 | spherical propagation |
| Cold Snap | `ars_nouveau:glyph_cold_snap` | 2 | 30 | cold burst / freeze interaction |
| Conjure Mageblock | `ars_nouveau:glyph_phantom_block` | 1 | 5 | temporary/permanent conjured block |
| Conjure Magelight | `ars_nouveau:glyph_light` | 1 | 25 | light / vision / glow |
| Conjure Water | `ars_nouveau:glyph_conjure_water` | 2 | 80 | water placement / wet state |
| Craft | `ars_nouveau:glyph_craft` | 1 | 50 | remote crafting UI |
| Crush | `ars_nouveau:glyph_crush` | 2 | 30 | material processing / damage |
| Cut | `ars_nouveau:glyph_cut` | 1 | 0 | shear/axe-like interaction / light damage |
| Delay | `ars_nouveau:glyph_delay` | 1 | 0 | delayed resolution |
| Dispel | `ars_nouveau:glyph_dispel` | 1 | 30 | effect/summon dispel |
| Evaporate | `ars_nouveau:glyph_evaporate` | 1 | 50 | fluid removal |
| Exchange | `ars_nouveau:glyph_exchange` | 2 | 50 | block swap / caster-target transposition |
| Explosion | `ars_nouveau:glyph_explosion` | 2 | 200 | explosion |
| Fangs | `ars_nouveau:glyph_fangs` | 3 | 35 | conjured offensive fangs |
| Fell | `ars_nouveau:glyph_fell` | 1 | 150 | tree/vegetation harvesting |
| Firework | `ars_nouveau:glyph_firework` | 2 | 50 | firework creation |
| Flare | `ars_nouveau:glyph_flare` | 2 | 40 | fire-state detonation / mage fire |
| Freeze | `ars_nouveau:glyph_freeze` | 1 | 15 | freeze / ice conversion / slow |
| Glide | `ars_nouveau:glyph_glide` | 3 | 100 | temporary elytra-style flight |
| Gravity | `ars_nouveau:glyph_gravity` | 2 | 15 | gravity / forced fall |
| Grow | `ars_nouveau:glyph_grow` | 2 | 70 | growth acceleration |
| Harm | `ars_nouveau:glyph_harm` | 1 | 15 | direct magic damage / poison interaction |
| Harvest | `ars_nouveau:glyph_harvest` | 1 | 10 | crop harvest |
| Heal | `ars_nouveau:glyph_heal` | 2 | 50 | healing / anti-undead damage |
| Hex | `ars_nouveau:glyph_hex` | 3 | 100 | damage amplification + mana/heal suppression under conditions |
| Ignite | `ars_nouveau:glyph_ignite` | 1 | 15 | fire / mage fire |
| Infuse | `ars_nouveau:glyph_infuse` | 2 | 30 | potion/flask application |
| Intangible | `ars_nouveau:glyph_intangible` | 3 | 30 | temporary block intangibility |
| Interact | `ars_nouveau:glyph_interact` | 1 | 10 | remote player-like interaction |
| Invisibility | `ars_nouveau:glyph_invisibility` | 2 | 30 | invisibility |
| Item Pickup | `ars_nouveau:glyph_pickup` | 1 | 10 | item collection |
| Knockback | `ars_nouveau:glyph_gust` | 1 | 15 | force / knockback / block motion |
| Launch | `ars_nouveau:glyph_launch` | 1 | 30 | vertical entity/block force |
| Leap | `ars_nouveau:glyph_leap` | 1 | 25 | directional mobility |
| Lightning | `ars_nouveau:glyph_lightning` | 3 | 100 | lightning / shocked interaction |
| Linger | `ars_nouveau:glyph_linger` | 3 | 500 | lingering field / repeated application |
| Name | `ars_nouveau:glyph_name` | 2 | 25 | entity/item naming |
| Orbit | `ars_nouveau:glyph_orbit` | 3 | 50 | orbiting spell carriers |
| Place Block | `ars_nouveau:glyph_place_block` | 1 | 10 | block placement from inventory |
| Prestidigitation | `ars_nouveau:glyph_prestidigitation` | 1 | 0 | cosmetic/particle temporary block |
| Pull | `ars_nouveau:glyph_pull` | 1 | 15 | force pull / block motion |
| Redstone Signal | `ars_nouveau:glyph_redstone_signal` | 1 | 0 | temporary/targeted redstone power |
| Reset | `ars_nouveau:reset` | 1 | 0 | spell-chain target reset |
| Rewind | `ars_nouveau:rewind` | 3 | 100 | temporal rollback of position/health and moved blocks |
| Rotate | `ars_nouveau:glyph_rotate` | 1 | 10 | block/entity rotation |
| Rune | `ars_nouveau:glyph_rune` | 1 | 30 | temporary trigger rune |
| Sense Magic | `ars_nouveau:glyph_sense_magic` | 2 | 50 | magical detection / rune reading |
| Slowfall | `ars_nouveau:glyph_slowfall` | 2 | 30 | fall control |
| Smelt | `ars_nouveau:glyph_smelt` | 2 | 100 | smelting/processing |
| Snare | `ars_nouveau:glyph_snare` | 1 | 100 | immobilization |
| Summon Decoy | `ars_nouveau:glyph_summon_decoy` | 3 | 200 | decoy / aggro manipulation |
| Summon Steed | `ars_nouveau:glyph_summon_steed` | 1 | 100 | mount summon |
| Summon Undead | `ars_nouveau:glyph_summon_undead` | 3 | 150 | undead combat summon |
| Summon Vex | `ars_nouveau:glyph_summon_vex` | 3 | 150 | vex combat summon |
| Summon Wolves | `ars_nouveau:glyph_summon_wolves` | 1 | 100 | wolf combat summon |
| Toss | `ars_nouveau:glyph_toss` | 1 | 10 | item transfer/throw |
| Wall | `ars_nouveau:glyph_wall` | 3 | 500 | lingering wall / repeated application |
| Wind Burst | `ars_nouveau:glyph_wind_burst` | 1 | 30 | radial force / wind charge |
| Wind Shear | `ars_nouveau:glyph_wind_shear` | 2 | 50 | air-state conditional damage |
| Wither | `ars_nouveau:glyph_wither` | 3 | 100 | wither debuff |
| Wololo | `ars_nouveau:wololo` | 1 | 30 | color transformation |

## Learning / progression authority

Current Ars documentation establishes the core progression model:

- glyphs belong to Tiers I–III;
- the Novice Spell Book is limited to Tier I;
- Apprentice and Archmage spell books unlock higher tiers;
- glyph knowledge is learned and then used compositionally rather than acquiring one immutable fixed spell scroll for every finished combination.

Exact recipe/acquisition data for each glyph will be normalized where it materially affects Phase 2 overlap; the registry/tier/cost table above already gives the core mechanical surface.

## Critical deduplication findings

### Chaos is **not** starting from zero

Ars core already supplies `Randomize`, which randomizes supported glyph behavior/selection. In the currently installed Ars ecosystem, **Ars Controle** also supplies `Filter: Random`, a true probability gate with a documented base **50%** resolution chance and Amplify/Dampen probability formula.

Therefore a Black Arcana Chaos school cannot claim “randomness” or “probability” generically as a unique mechanic. A real Chaos gap would need stronger semantics such as controlled entropy budgets, weighted outcome families, probability debt, persistent instability or reality-rule distortion that cannot already be constructed through Ars primitives.

### Order / geometry is also already contested

The currently installed Ars ecosystem includes **Ars Zero `Geometrize`** plus cube/sphere/flatten/hollow geometry augments, while Ars core supplies Rune, Wall, Snare, Dispel, Gravity, Exchange and other constraint primitives.

Order must therefore prove a delta in **authoritative laws/seals/rules** rather than simply drawing circles, walls, geometric fields or immobilizing entities.

### Binding has direct overlap

The installed **Ars Elemental** addon exposes `Life Link`, which shares caster damage with a linked target and shares target healing with the caster; Sensitive reverses direction and Cut severs the link.

This is direct overlap with part of Arcana Vincular. Black Arcana's remaining candidate delta is the broader persistent typed contract/resource-routing architecture (blood reservoir, spirit source, familiar/servant/source links, transactional reservation and fail-closed settlement), not generic “link two health pools”.

### Temporal / spatial overlap is extensive

Ars core contains Blink, Exchange and Rewind. Rewind explicitly rolls an entity back to previous locations and health and can restore spell-moved blocks. Any Doctor Strange/Fate-inspired time/space mechanic must deduplicate against these primitives in addition to Iron's, Leyline and Black Arcana 07.04.

### Divine / Infernal / Witchcraft overlap

Ars core already exposes Heal, Hex, Wither, Ignite, Flare, Gravity, summons, detection and field forms. Addons extend poison, water, soul, life-link and other areas. The complete Ars addon pages must be evaluated before a Phase 3 spell is approved in those identities.

## Provenance / confidence

- Presence/version: current 2026-09-06 modlist — HIGH.
- Glyph architecture, registry IDs, tiers, base costs and descriptions above: current public Ars 1.21.1 guide — HIGH.
- The guide is addon-aware; ownership is determined by registry namespace, not page location.
- No Java bytecode was decompiled for this catalog.
