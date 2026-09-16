# Goety Iron — cross-loader release synchronization evidence

Status: `EXACT 3.1 ARTIFACT HASH MATCH / CROSS-LOADER RELEASE LINE SYNCHRONIZED / SOURCE URL ABSENT / SEMANTIC INVENTORY STILL OPEN`

## Scope

This note records publisher-controlled evidence connecting the installed NeoForge 1.21.1 release line to the parallel Forge 1.20.1 line. It does **not** promote Forge implementation details to NeoForge authority and does not claim binary equivalence.

## Exact installed 3.1 identity

Physical pack authority:

- JAR: `GoetyIron-1.21.1-NeoForge-3.1.jar`
- mod id: `goetyiron`
- runtime: `3.1`
- SHA-1: `c8529867e798661ed01fb2948abda23735888fc6`

Publisher metadata independently matches that artifact:

- CurseForge project/file: `1367643 / 8662179`
- Modrinth project/version: `tZpynDu5 / YZXNIxvk`
- Modrinth file: `GoetyIron-1.21.1-NeoForge-3.1.jar`
- Modrinth SHA-1: `c8529867e798661ed01fb2948abda23735888fc6`
- Modrinth size: `507646` bytes
- Modrinth publication time: `2026-08-16T12:40:42.435094Z`

The Modrinth hash equals the physical modlist hash, so the publisher artifact and the pack artifact are the same file identity at SHA-1 level.

## 3.0.0 NeoForge ↔ 2.1.0 Forge

The paired releases published on 2026-08-06 are:

- NeoForge 1.21.1 `3.0.0`, Modrinth version `GYDNpLkn`
- Forge 1.20.1 `2.1.0`, Modrinth version `QvSYOnxH`

Both publisher changelogs explicitly state that the NeoForge 1.21.1 branch was ported and was **identical in content** to the Forge 1.20.1 branch at that release checkpoint. Both changelogs then enumerate the same feature/fix list.

This is strong publisher evidence of **content equivalence for the 3.0.0/2.1.0 checkpoint**. It is not a statement of byte-for-byte equality and is not automatically inherited by later releases.

## 3.1 NeoForge ↔ 2.2 Forge

The next paired releases are:

- NeoForge 1.21.1 `3.1`, Modrinth version `YZXNIxvk`, published `2026-08-16T12:40:42.435094Z`
- Forge 1.20.1 `2.2`, Modrinth version `kYqXKiOc`, published `2026-08-16T12:41:17.102981Z`

Their English and Chinese changelog bodies are identical and describe the same seven changes:

1. config options fixed;
2. Improved Ominous Fire Orbs allied-destruction fix;
3. compatibility fixes;
4. per-servant spell-attribute config options;
5. Tincture of Forgetfulness resetting Goety's Void Vault;
6. configurable Polar Bear → Polar Bear Servant summon replacement;
7. configurable Vex → Vex Servant summon replacement.

This proves a **synchronized publisher release delta** for 3.1/2.2. It does not, by itself, prove that every registry/resource/class in 2.2 is identical to 3.1. Therefore an inventory reconstructed only from a hypothetical Forge source would still require a controlled cross-loader reconciliation before becoming exact 3.1 authority.

## Public-source status

The exact Modrinth project metadata currently reports:

- `source_url: null`
- `issues_url: null`
- `wiki_url: null`

GitHub repository search did not locate an official Goety Iron source repository tied to the publisher/project. A similarly named public repository, `Rinko1231/GoetyIronLink`, is a different interoperability mod and is not substituted as authority.

Therefore Goety Iron remains `SOURCE REVISION UNLOCATED`.

## License/provenance discrepancy

Publisher platforms currently disagree:

- CurseForge project/file surfaces declare **MIT License**;
- Modrinth project `tZpynDu5` declares **All Rights Reserved**.

Until upstream reconciles those platform declarations or an authoritative source license is located, Black Arcana applies the stricter clean-room posture: factual metadata and interoperability observations may be recorded, but no implementation, source, text, assets, models or sounds are copied/reused on the assumption that the whole project is MIT.

## Semantic-count consequence

This checkpoint improves artifact identity and cross-loader release provenance but does **not** close a complete object-level inventory of Goety Iron Focuses, rituals, servant-producing actions or other independently countable magical actions.

Consequently:

- Goety Iron semantic delta to the strict global denominator: **+0 at this checkpoint**;
- global strict semantic minimum remains **797**;
- provider-component metric remains unchanged;
- exact 3.1 registry/resource inventory remains a blocker.

## Authoritative public surfaces

- CurseForge project: `https://www.curseforge.com/minecraft/mc-mods/goety-iron`
- CurseForge 3.1 file: `https://www.curseforge.com/minecraft/mc-mods/goety-iron/files/8662179`
- CurseForge 2.2 file: `https://www.curseforge.com/minecraft/mc-mods/goety-iron/files/8662199`
- Modrinth project API: `https://api.modrinth.com/v2/project/tZpynDu5`
- Modrinth versions API: `https://api.modrinth.com/v2/project/tZpynDu5/version`
