# Hexalia

Status: `PHASE 2 — PROVIDER AUDIT IN PROGRESS`

## Runtime identity

- Provider: **Hexalia**
- Installed JAR: `hexalia-neoforge-1.3.6.jar`
- Runtime version recorded by current modlist/Notion: `1.3.5`
- Loader/game: NeoForge 1.21.1
- Role: `RITUAL / BREWING / WITCHCRAFT PROVIDER`
- Runtime/version authority: current modlist snapshot (2026-09-06) + reconciled Notion sheet.

The filename/runtime mismatch is intentional and must remain visible. Do not normalize `1.3.6` and `1.3.5` into one unqualified version string.

## Provenance / source boundary

The public upstream repository identifies Hexalia as plant-based magic/witchery with rituals and brewing. GitHub repository metadata currently exposes `license: null`; therefore Black Arcana may use public documentation and clean-room observed/provider facts for catalog/deduplication, but **must not copy or derive implementation from Hexalia source unless a compatible license or explicit permission is later established and recorded in the project provenance ledger**.

Source inspection performed during Phase 2 is used here only to record observable/provider-owned behavior and current content identity. It is not implementation authorization.

## Core witchcraft loop

Hexalia owns a preparation-first witchcraft loop rather than an instant spellbook loop:

1. acquire magical herbs/materials;
2. process ingredients (including Mortar & Pestle paths);
3. prepare Small Cauldron / Nature's Ritual / Celestial Infusion content;
4. satisfy environmental/equipment conditions;
5. receive a provider-owned brew, ritual output, node, item or equipment effect.

### Small Cauldron behavior

Current Verdant Grimoire documentation states:

- fill with water;
- heat from below;
- add ingredients;
- stir with a Ladle to begin cooking;
- heat must remain present;
- invalid combinations create a **Spoiled Mixture** that emits corrupted energy and can harm nearby entities until cleansed/removed;
- overcooking reduces yield;
- correct preparation/timing is part of the mechanic.

This preparation loop is canonical provider behavior and is not to be replaced by a Black Arcana instant-cast clone.

## Current brew catalog

The current Grimoire enumerates eight Small Cauldron brews. Seven apply a 240-second provider effect; Homestead is a one-shot teleport consumable.

| ID / name | Recipe inputs | Preparation | Provider behavior | Dedup impact |
|---|---|---|---|---|
| `hexalia:brew_of_arachnid_grace` — Arachnid Grace | Spider Eye + Ghost Powder + Black Dye + String | Small Cauldron, `duration=4800` | 240 s; wall-climb while colliding and not crouching; removes Poison; water/rain applies Weakness; provider description also states cobweb immunity | blocks generic witch wall-climb / poison-immunity brew clones |
| `hexalia:brew_of_bloodlust` — Bloodlust | Mandrake + Spirit Powder + Tree Resin + Rotten Flesh | Small Cauldron, `duration=4800` | 240 s; provider description: increases strength and restores part of damage dealt, while Regeneration is disabled. Current effect class actively removes effects whose registry path contains `regeneration` | overlaps offensive/lifesteal blood-adjacent witch brews; **not** a blood reservoir spell |
| `hexalia:brew_of_daybloom` — Daybloom | Sunfire Tomato + Spirit Powder + Glow Berries + Witchweed | Small Cauldron, `duration=4800` | 240 s; every 100 ticks checks sunlight. No sun: 1.5 magic damage and speed modifier removed. Sun available: heals `2.0 × sunlightGenerationMultiplier` and grants movement-speed multiplier `0.05 × (amplifier+1) × sunlightGenerationMultiplier` | blocks generic sunlight-heal/speed potion; relevant to Celestial design but remains Witchcraft/Nature provider-owned |
| `hexalia:brew_of_hollow_silence` — Hollow Silence | Feather + Ghost Powder + Chillberries + Sculk | Small Cauldron, `duration=4800` | 240 s; registered effect class itself has no tick logic; provider localization describes silenced presence near sound-sensitive entities with periodic vision clouding. Exact event hooks remain to be traced before treating those secondary semantics as implementation-grade | blocks generic stealth-vs-sound brew only after hook verification |
| `hexalia:brew_of_homestead` — Homestead | Tree Resin + Ender Pearl + Spirit Powder + Galeberries | Small Cauldron, `duration=4800` | one-shot consumable; attempts provider safe-return to player spawn and applies vanilla Nausea/Confusion for 600 ticks (30 s) after teleport | blocks generic witch return-home potion |
| `hexalia:brew_of_siphon` — Siphon | Dream Paste + Siren Paste + Iron Ingot + Redstone | Small Cauldron, `duration=4800` | 240 s; provider description: increased mining speed and nearby item attraction, with extra exhaustion on block break. Runtime tick attracts/picks up nearby item entities with radius `config.siphonRadius + amplifier`; also registers +0.4 attack-speed attribute value | blocks magnetic/item-siphon witch brew clones |
| `hexalia:brew_of_slimewalker` — Slimewalker | Slime Ball + Chillberries + Tree Resin + Feather | Small Cauldron, `duration=4800` | 240 s; sets fall distance to zero; on ground applies short Slowness; when landing under its bounce condition launches entity upward at Y velocity 1.0 and emits slime feedback | blocks generic fall/bounce witch brew clones |
| `hexalia:brew_of_spikeskin` — Spikeskin | Celestial Crystal + Iron Nugget + Sweet Berries + Tree Resin | Small Cauldron, `duration=4800` | 240 s; provider description: increased armor + reflected incoming damage + movement penalty. Registered movement modifier is -10% total; armor modifier uses custom amount calculation `3.0 × (amplifier+1)` | blocks generic thorns/armor witch brew clones |

### Related non-brew preparations already in provider surface

- `Brambleguard Salve`: 90 s provider effect; provider localization describes increased magical/physical resistance and Bleeding prevention/removal.
- `Mender's Salve`: 90 s vanilla Regeneration provider consumable.
- `Bleeding`: harmful provider effect; localization describes damage over time similar to Poison.
- `Overfed`: provider effect; saturation preservation with movement penalty.
- `Stunned`: provider harmful immobilization effect.

These are capability-bearing entries and will receive granular pages if they materially participate in the final overlap matrix.

## Nature's Ritual — confirmed outputs in current generated data

Current 1.21.1 generated resources prove `hexalia:natures_ritual` recipes for multiple outputs. Player-facing outputs found so far include:

- `Aegiflora`
- `Astrylis`
- `Grimshade`
- `Lourdes`
- `Morphora`
- `Nautilite`
- `Windsong`
- `Air Node`
- `Earth Node`
- `Fire Node`
- `Water Node`
- `Rootshaper`
- `Kelpweave Blade`
- `Rabbage Seeds`
- Bloomwrap armor pieces

`debug_natures_ritual` exists in generated data but is explicitly **not** counted as player-facing content.

Exact ingredient/output semantics for each current ritual remain to be expanded into the Hexalia subcatalog.

## Celestial Infusion — confirmed provider surface

Current generated/Grimoire data includes Celestial Infusion outputs such as:

- Celestial Crystal;
- Galeberries;
- Moonweave Hood;
- Moonweave Mantle;
- Moonweave Bindings;
- Moonweave Footwraps.

This is important to Black Arcana's planned Divine/Celestial discipline: the name/theme does **not** make Hexalia a Holy spell provider, but any future celestial crafting/infusion must remain distinct from this existing lunar/celestial witchcraft preparation path.

## Deduplication consequences

### Witchcraft

Black Arcana Witchcraft must **integrate, not replace**, Hexalia's:

- cauldron brewing;
- herbs/material preparation;
- provider brews;
- Nature's Ritual;
- Celestial Infusion;
- Mortar & Pestle processing;
- mutations/provider transformations;
- nodes/idols where mechanically relevant.

A future Black Arcana recipe may require or transform a real Hexalia preparation, but must not silently recreate its result as a generic spell.

### Blood / Binding

`Brew of Bloodlust` is blood-themed but is **not** evidence of a blood-volume resource, external blood reservoir, blood link, or blood-only casting authority. It does not occupy the planned Hematic Reservoir / typed blood-binding architecture.

### Divine / Celestial

`Daybloom` and Celestial Infusion create real overlap with solar/celestial presentation. The planned Divine school must therefore reserve its identity for Holy/miracle/authority semantics rather than merely 'sun-powered buff' or 'celestial crystal crafting'.

### Order / Chaos

No current Hexalia evidence audited here establishes the planned server-authoritative imposed-law or causal/probability systems. Individual rituals must still be checked before those gaps can be declared free.

## Acquisition / learning

The provider progression is documented through the **Verdant Grimoire** and recipe/advancement surface. Brews require their actual ingredients and Small Cauldron process; they are not learned as Iron's scrolls. Nature's Ritual and Celestial Infusion likewise remain provider-owned preparation systems.

## Open audit items

- enumerate every current Nature's Ritual recipe and its exact acquisition/result;
- enumerate every Celestial Infusion recipe;
- enumerate Mortar & Pestle transformations relevant to magical recipes;
- trace Hollow Silence event hooks before promoting its sound/vision behavior from provider-description confidence to runtime-confirmed confidence;
- catalog mutation mechanics and all capability-bearing idols/nodes;
- verify whether any current integration API/event exists that can be used without source-derived implementation.

## Phase 3 gate

Hexalia integration is `BLOCKED FOR IMPLEMENTATION` until the full provider subcatalog and semantic matrix are complete.
