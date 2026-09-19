# Somake Spells 1.0.9 — current public named-spell ledger

Status: `PUBLISHER-NAMED SURFACE / NOT A REGISTRY INVENTORY / CURRENT 1.0.9`

## Scope

This ledger records only spell names, published school labels and high-level semantics explicitly exposed by the official **NeoForge 1.21.1** Somake 1.0.9 release changelog.

Primary publisher checkpoint:

- CurseForge project/file: `1461634 / 8867079`;
- filename: `somakespells-1.0.9-1.21.1.jar`;
- uploaded: 2026-09-12;
- game/loader: Minecraft 1.21.1 / NeoForge;
- official file page: `https://www.curseforge.com/minecraft/mc-mods/somake-spells-irons-spells-addon/files/8867079`.

This file is **not** a registry inventory. A public display name does not prove a registry ID, class, unconditional registration, host enablement, acquisition path or survival reachability.

## Sixteen spell names explicitly published for 1.0.9

| Public name | Published school label | Publisher-described role | Catalog disposition |
|---|---|---|---|
| Procession of Souls | Spirit / Evocation | forward sequence of spiritual eruptions | `PUBLISHER_NAMED / REGISTRY UNVERIFIED` |
| Grave Sigil | Spirit / Evocation | ground sigil producing crossed spectral eruption waves | `PUBLISHER_NAMED / REGISTRY UNVERIFIED` |
| Soul Bastion | Spirit / Evocation | concentric spectral shield rings striking inward/outward | `PUBLISHER_NAMED / REGISTRY UNVERIFIED` |
| Soul Latch | Spirit / Evocation | binds and pulls a target, then releases a final burst | `PUBLISHER_NAMED / REGISTRY UNVERIFIED` |
| Spiral of Ruin | Spirit / Evocation | spectral trident impact followed by a spiral of soul eruptions | `PUBLISHER_NAMED / REGISTRY UNVERIFIED` |
| Soulfall Judgment | Spirit / Evocation | local soul impact plus descending spectral blades | `PUBLISHER_NAMED / REGISTRY UNVERIFIED` |
| Phantom Daggers | Spirit / Evocation | multiple spectral daggers that can hit again on return | `PUBLISHER_NAMED / REGISTRY UNVERIFIED` |
| Spectral Rondo | Spirit / Evocation | spinning charge with circular strikes and Soul Pillar trails | `PUBLISHER_NAMED / REGISTRY UNVERIFIED` |
| Winged Ruin | Spirit / Evocation | Red Soul-powered rise and dive finisher | `PUBLISHER_NAMED / REGISTRY UNVERIFIED` |
| Crimson Reflection | Spirit / Evocation | consumes stored Red Soul Lantern spells to summon the caster's Red Echo | `PUBLISHER_NAMED / REGISTRY UNVERIFIED` |
| Sovereign Armory | Holy | conjured golden portals fire weapons toward a target | `PUBLISHER_NAMED / REGISTRY UNVERIFIED` |
| Comforting Lullaby | Sound | channelled healing pulses that also apply Sleepy to healed players | `PUBLISHER_NAMED / REGISTRY UNVERIFIED` |
| Summon Drowned | Aqua | summons an allied Drowned scaling from Aqua Spell Power | `PUBLISHER_NAMED / REGISTRY UNVERIFIED` |
| Bloodbound Blade | Blood | throws the held sword and roots the target with crystallized blood | `PUBLISHER_NAMED / REGISTRY UNVERIFIED` |
| Withered Rose Vortex | Blood | petal vortex that pulls enemies, damages repeatedly and applies Wither | `PUBLISHER_NAMED / REGISTRY UNVERIFIED` |
| Funeral Bloom | Blood | giant withered rose drops explosive buds and can heal the caster against withered targets | `PUBLISHER_NAMED / REGISTRY UNVERIFIED` |

Published distribution within this named 1.0.9 tranche:

- Spirit / Evocation: **10**;
- Holy: **1**;
- Sound: **1**;
- Aqua: **1**;
- Blood: **3**;
- total explicitly named in the 1.21.1 File `8867079` **New Spells** section: **16**.

These counts describe the changelog list only. They are not a total for the provider's 1.0.9 registry.

## Explicit replacement

The same official 1.0.9 changelog states:

- `Summon Zombie` was replaced by `Summon Drowned`.

The exact resource-only audit independently observed:

- historical localization root `summon_zombie` absent from the 1.0.9 base-key surface;
- candidate 1.0.9 root `summon_drowned` present.

This is strong current-line evidence for the public replacement at the name/resource-surface level. It still does not establish the exact current registry ID/class without a registry-authoritative source.

## Relationship to the exact 1.0.9 resource audit

`EXACT-1.0.9-RESOURCE-AUDIT.md` closes an exact release surface of:

- 83 base `spell.somakespells.<id>` localization roots;
- 83 matching `.guide` keys;
- 17 candidate-added roots versus the historical 1.0.8-fix registry surface;
- one historical root absent: `summon_zombie`.

The 16 publisher-named spells above are a **current public semantic surface** that coexists with the larger 83-root resource surface. This audit does not assert a one-to-one name→root→registry mapping, and neither surface substitutes for a registry inventory.

Do not infer that:

- every one of the 83 localization roots is registered;
- every one of the 16 public names is unconditional;
- lexical similarity between a display name and a localization root proves a registry ID;
- the 16 names are the complete 1.0.9 spell inventory.

## Optional-provider boundary

The **1.21.1** File `8867079` changelog explicitly confirms only the broad Legendary Monsters condition for the new Spirit/Red Soul/items tranche: that content loads when Legendary Monsters is installed.

The separate **1.20.1** 1.0.9 release page contains additional compatibility wording for Magic From The East. That cross-version wording is **not imported** into the 1.21.1 registry/predicate authority. Exact 1.21.1 Magic From The East and other optional-registration predicates remain open until independently confirmed for File `8867079`.

## Catalog consequence

This ledger improves current 1.0.9 naming/semantic provenance but changes no strict catalog count:

- Somake remains `⚠️ Parcial / condicionado`;
- strict semantic delta remains `+0`;
- no technical component is promoted;
- exact 1.0.9 registry identities, optional predicates, deployed config/host gates and survival reachability remain unresolved.

The historical `PUBLIC-NAMED-SPELLS.md` remains useful only for the 1.0.8/1.0.8-fix publication line.
