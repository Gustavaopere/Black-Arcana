# More Relics 1.7.7 — public relic catalog

## Evidence boundary

This inventory uses the current publisher description plus exact/recent publisher changelogs. It does not derive registry IDs or formulas from the installed JAR.

The publisher says the mod contains **25+** relics and the current visible 1.21.1 loot/evolution list contains **29 named entries**. This file preserves those public names without claiming that the list is a formal registry dump.

## 1. Publisher-listed relics and 1.21.1 acquisition

| # | Public relic name | Publisher-listed 1.21.1 route | Evolution relation |
|---:|---|---|---|
| 1 | Axolotl Cream | Aquatic and Tropic loot; examples include jungle/ocean/trial-chamber chests | — |
| 2 | Crown of the Legend | Nether / Bastions | — |
| 3 | Eject Button | broad/global loot with low chance | — |
| 4 | Guts Orb | Bastions, Deserts, Ruined Portals | — |
| 5 | King Crimson | evolution only | evolves from Tyrant Mask |
| 6 | Tyrant Mask | Bastions | evolves into King Crimson |
| 7 | Made in Heaven | evolution only | evolves from Whispering Amulet |
| 8 | Whispering Amulet | evolution only | evolves from Slumbering Amulet; evolves into Made in Heaven |
| 9 | Slumbering Amulet | Buried Treasure | evolves into Whispering Amulet |
| 10 | Mass Gauntlet | broad/global loot with low chance | — |
| 11 | Opal Necklace | Deserts and Snow/Ice biomes | — |
| 12 | Sentient Rust | Mineshafts, Mountains, Swamps | — |
| 13 | Shieldweave Cape | Caves, Taiga, Mountains; low-chance general Overworld route | — |
| 14 | Bionic Eye | Sculk locations such as Ancient Cities/Deep Dark | — |
| 15 | Thermoseismic Heart | Desert | — |
| 16 | Biojoint | Nether, Mineshafts | — |
| 17 | Whims of Fate | Bastions, Desert | — |
| 18 | Depleted Spool | Caves, Mineshafts, Mountains | evolves into Weavers Spool |
| 19 | Weavers Spool | evolution only | evolves from Depleted Spool |
| 20 | Mood Worm / Moodworm | broad/global loot with low chance | — |
| 21 | VertebraX | End | — |
| 22 | Gravitum Glove | End, Stronghold, Sculk | — |
| 23 | Epoch Apple | Dungeon chests | — |
| 24 | Converging Orb | Woodland Mansions | evolves into Wonder of U |
| 25 | Wonder of U | evolution only | evolves from Converging Orb |
| 26 | Gravitum Strider | End, Sculk | — |
| 27 | Twin Fangs | Pillager Outposts, Mansions | — |
| 28 | Swiftedge | Mountains | — |
| 29 | Runic Plate | Mountains | — |

### Naming normalization

The current description contains minor presentation inconsistencies/typos for some names (for example the loot list renders `Twing Fangs` in one place), while exact changelogs use **Twin Fangs**. The catalog uses the stronger/current changelog spelling where available instead of inventing a registry ID.

## 2. Evolution chains

### Tyrant chain

`Tyrant Mask → King Crimson`

King Crimson is publicly described as evolution-only.

### Amulet chain

`Slumbering Amulet → Whispering Amulet → Made in Heaven`

Made in Heaven received a complete rework in 1.7.0, which is also the source of the documented stale extended-config migration hazard.

### Spool chain

`Depleted Spool → Weavers Spool`

### Orb chain

`Converging Orb → Wonder of U`

Evolution semantics, experience requirements and persistent data remain Relics/More Relics authority. Exact requirements are not inferred from the loot page.

## 3. Exact/recent changelog capability evidence

### More Relics 1.7.7

Publisher changelog establishes:

- per-relic ability/status icon indicators can be disabled individually client-side;
- Moodworm exposes current status as an icon;
- Moodworm received a minor balance buff and a NeoForge starting-stat correction;
- Moodworm change duration is configurable in common config;
- Twin Fangs had a fix targeting an infinite-hit condition;
- Eject Button health threshold is configurable;
- Bionic Eye Vulnerability levels are configurable;
- Cyberpsychosis presentation also renders iron golems as wardens.

`Cyberpsychosis` is a provider-visible status/ability concept named in the changelog, not one of the 29 loot-list relic names. Its exact owning relic/state machine is not asserted here without stronger public evidence.

### More Relics 1.7.6

Publisher changelog establishes:

- Eject Button can occupy charm and ring slots in addition to its prior slot behavior;
- selected relic effects/statuses can appear as small icons above the food bar;
- Mass Gauntlet gains a configurable damage-boost cooldown, defaulted by the publisher to 0.2 seconds at that checkpoint.

Exact 1.7.7 config defaults are not generalized beyond what the 1.7.7 page itself confirms.

### More Relics 1.7.5

Publisher changelog adds:

- Swiftedge;
- Runic Plate.

### More Relics 1.7.3

Publisher changelog adds:

- Twin Fangs.

It also records a NeoForge Wonder of U crash fix related to a Java-21 library dependency in an earlier ability implementation. That historical implementation detail is not reproduced; the only catalog consequence is that Wonder of U had a provider-owned active ability path with platform-specific stability history.

### More Relics 1.7.0

Publisher changelog establishes a complete **Made in Heaven** rework and warns of stale Relics extended-config data causing a `data is null` crash after upgrading from older More Relics versions.

The documented mitigation is configuration regeneration/cleanup, not a Black Arcana fix.

## 4. Authority by capability family

### Loot acquisition

Provider/Relics owns loot eligibility and weighting. Black Arcana must not inject a second copy of a More Relics item into its own generic magical loot simply because the item is useful for a Black Arcana build.

### Relic experience/progression

Base Relics owns the progression/equipment framework; More Relics supplies addon content. Black Arcana/RPG must not increment relic XP by private-state writes or rebuild addon progression.

### Evolution

More Relics/Relics own the evolution chains above. Black Arcana rituals must not substitute themselves as a free evolution trigger unless the provider intentionally exposes a supported integration seam.

### Active/passive abilities

Provider ability settlement remains provider-owned. A Black Arcana observer may react only through a verified causal boundary and must not apply a second copy of the effect.

### Client indicators

Status/ability icons are presentation. Client icon state is not gameplay authority and must not be used as a server progression trigger.

## 5. What remains unverified

Unless separately published and verified, this catalog does **not** assert:

- registry IDs;
- exact rarity values;
- exact loot weights;
- exact relic XP/evolution thresholds;
- exact stats/formulas;
- internal ability IDs;
- exact Curios slot IDs beyond publisher-facing descriptions;
- server event hooks;
- compatibility with current Relics 0.12.8;
- persistence/schema compatibility across Relics 0.10.7.8 → 0.12.8.

## 6. Current compatibility gate

The 29-item content catalog is useful for semantic deduplication, but the current pack runs a host version the addon publisher explicitly says is unsupported.

Therefore no item in this table is treated as a safe provider-specific integration target in Black Arcana while the host remains Relics `0.12.8` without successful real QA.