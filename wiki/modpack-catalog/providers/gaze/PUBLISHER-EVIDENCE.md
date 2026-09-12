# Gaze 1.1.7.1 — publisher evidence ledger

Status: `EXACT PHYSICAL IDENTITY / EXACT CURSEFORGE FILE / EXACT MODRINTH VERSION / EXACT HASH-MATCHED BINARY MATERIALIZED / ARR / STRUCTURAL REGISTRY AUDIT CLOSED`

## Physical pack authority

- JAR: `gaze-1.1.7.1.jar`
- mod id: `gaze`
- runtime: `1.1.7.1`
- SHA-1: `a8cb3190bde157f78160ce65c202ce2d47fb2041`
- CurseForge package fingerprint: `2912704145`
- pack platform: Minecraft `1.21.1`, NeoForge `21.1.248`

These values come from the current physical modlist and remain authoritative for what is installed.

## CurseForge exact release

Publisher project:

- project: `1273454`
- exact installed-line file: `7261638`
- displayed main-file identity: `gaze-1.21.1-1.1.7.1.jar`
- file detail filename: `gaze-1.1.7.1.jar`
- uploaded: `2025-11-25`
- type: Release
- platform: NeoForge / Minecraft 1.21.1
- project license: All Rights Reserved

The exact 1.1.7.1 changelog says the release remains on Malum 1.8 and records only a narrow patch: book-entry movement, Fafnir full-Malignant-set behavior and Anima Bestiary fixes, plus localization.

## Modrinth exact release

Publisher project/version:

- project: `NlvaJ5WE`
- version: `od4ltbRo`
- release name: `1.1.7.1`
- Minecraft: `1.21.1`
- platform: NeoForge
- environment: client and server
- required: Malum `1.8.2`, Lodestone `1.8.2`
- optional: Iron's Spells 'n Spellbooks
- project license: All Rights Reserved
- Maven coordinate: `maven.modrinth:NlvaJ5WE:od4ltbRo`

The Modrinth version page provides no changelog for 1.1.7.1.

## Immediately preceding 1.1.7 release

CurseForge File ID `7250833`, published `2025-11-22`, explicitly updates Gaze for Malum 1.8 and provides the richest publisher-controlled current-line semantic delta available in the audited public surfaces.

Named additions/changes include Spirit-Channel pouch, Domain of Swords Geas, Enchantment Workbench, Seidhr, Spirit Saber, Veil's Edge, Splintered World, Replica Dharmachakra, WorldAnchor/Eir runes, multiple corrupted Rites, Aqua Rite, Pact of Encroaching Malice, Meditation Ring, Mage Ethics Ring, Charge Necklace and Astral Splinter. It also states that Rites moved to deferred registration and that the runes were renamed to a Norse theme.

These publisher facts remain lineage/context. Exact current registry claims are now sourced from the hash-matched 1.1.7.1 artifact rather than extrapolated from this changelog.

## Current project-scale statements

The current publisher project description advertises:

- 2 new Geas;
- a new set of Rites;
- 6 weapons;
- 8 runes;
- 5 Curios;
- Spirit-Channel pouch;
- a new progression screen.

Phase 2BJ's exact-artifact audit independently resolves the relevant registry/count surfaces; these publisher scale statements are retained as provenance, not substituted for binary evidence.

## Exact artifact materialization

The old materialization blocker is superseded. Isolated NON-MERGE PR #201 materialized the direct Modrinth artifact for version `od4ltbRo` and hard-failed unless its SHA-1 equaled the physical pack SHA-1.

Final evidence:

- audit HEAD: `2f4ff6536663b1c629a6a5ea92416765bea17b1e`;
- workflow run: `34676660467` — GREEN;
- evidence artifact: `10292013626`;
- digest: `sha256:fb69f353b672f7c8ec7b470c454d24d1c3110cb996a250076a16d2b053f23f71`.

The resulting exact audit closes, for catalog purposes:

- 26 distinct Gaze Spirit Rite identities, all referenced by provider progression;
- 2 Gaze Geas effect-type identities;
- 8 progression-visible rune items;
- 1 Gaze-owned Iron's spell registration, Soulward Shield;
- the `disableGazeRites` COMMON-config registration gate;
- the optional `irons_spellbooks` provider gate for Gaze's Iron's compatibility registration.

See [`EXACT-1.1.7.1-ARTIFACT-AUDIT.md`](EXACT-1.1.7.1-ARTIFACT-AUDIT.md) for the canonical semantic disposition.

## Semantic disposition

Publisher evidence by itself previously supported only `+0`. Exact artifact evidence now safely promotes only one current semantic object:

- Soulward Shield: **+1 `COUNTED_EXACT`** because the physical pack satisfies the Iron's provider gate;
- 26 Rites: remain **`CONDITIONAL`** because the deployed COMMON value for `disableGazeRites` is unavailable;
- 2 Geas types and 8 rune items: excluded by the existing semantic-action metric definition.

Current strict semantic minimum after Phase 2BJ: **1250**. Gaze remains an open provider component; internal component coverage remains **57/100**.

## Clean-room / license boundary

Gaze is **All Rights Reserved** on current CurseForge and Modrinth surfaces. Exact binary materialization is used only for factual compatibility/catalog evidence and does not authorize source reconstruction or reuse.

No implementation bodies, recipe ingredient lists, numerical balance values, localization prose, source reconstruction, assets, models or sounds are copied/adapted. Any stronger derivation remains prohibited unless separate applicable permission/license evidence is established.

## URLs

- `https://www.curseforge.com/minecraft/mc-mods/gaze-a-malum-addon`
- `https://www.curseforge.com/minecraft/mc-mods/gaze-a-malum-addon/files/7261638`
- `https://www.curseforge.com/minecraft/mc-mods/gaze-a-malum-addon/files/7250833`
- `https://modrinth.com/mod/gaze-a-malum-addon`
- `https://modrinth.com/mod/gaze-a-malum-addon/version/1.1.7.1`
