# More Relics 1.7.7 — Relics addon provider audit

## Status

`EXACT INSTALLED ARTIFACT 1.7.7 / EXACT CURSEFORGE FILE 8685815 + MODRINTH 1.7.7 / ARR / 29 PUBLISHER-LISTED RELIC NAMES+LOOT ROUTES / EVOLUTION CHAINS MAPPED / CURRENT PACK RELICS 0.12.8 EXPLICITLY UNSUPPORTED BY ADDON PUBLISHER / 0.12.8 SUPPORT DESCRIBED AS FUTURE MINI-BETA / CURATORIAL DECISION = MANTER WITH RISK ACCEPTED / PROVIDER-SPECIFIC RUNTIME+PROGRESSION INTEGRATION FAIL-CLOSED`

## Runtime identity

Current physical modlist authority:

- provider: **More Relics**;
- installed JAR: `morerelics-1.7.7-1.21.1.jar`;
- mod id: `morerelics`;
- runtime version: `1.7.7`;
- SHA-1: `ba0c920bc7712d1ff85012327b26e1a808c648f6`;
- CurseForge/package fingerprint recorded by the modlist: `1163810056`;
- loader/game: NeoForge 1.21.1;
- role: `RELIC / EQUIPMENT / EVOLUTION / PASSIVE+ACTIVE ABILITY ADDON`.

Current host/dependency identities relevant to the audit:

- Relics: `relics-1.21.1-0.12.8.jar` / runtime `0.12.8` / **Beta** publisher channel;
- Curios API: `curios-neoforge-9.5.1+1.21.1.jar` / `9.5.1+1.21.1`.

The modlist remains authoritative for what is physically installed. It does not prove that the installed versions are supported together.

## Exact public release checkpoint

Official publisher surfaces:

- CurseForge project: **More Relics**;
- author: **blorbilon**;
- project ID: `1269280`;
- license: **All Rights Reserved**;
- environment: Client & Server;
- exact NeoForge 1.21.1 file: `morerelics-1.7.7-1.21.1.jar`;
- CurseForge file ID: `8685815`;
- uploaded: `2026-08-19`;
- release channel: Release;
- Modrinth project: More Relics / ARR;
- Modrinth exact 1.7.7 NeoForge version is also published for Minecraft 1.21.1.

No official public source repository for exact 1.7.7 was located in this checkpoint. No installed-JAR decompilation is used.

## Critical current-pack compatibility finding

This is the most important operational result of the provider audit.

The publisher's current NeoForge notice states:

- Relics `0.11` and `0.12` are beta releases;
- they are **not yet supported** by More Relics;
- for Minecraft 1.21.1, users should use Relics `0.10.7.8` instead.

The exact More Relics `1.7.7` changelog reinforces that state: the author says a **future** update may be a mini beta specifically for Relics `0.12.8`, may not include all content and would only receive bug fixes.

The current pack instead installs **Relics `0.12.8`**, and that exact Relics build is itself published as **Beta**.

Therefore the current pairing is:

`PHYSICALLY INSTALLED / CURATORIALLY KEPT / EXPLICITLY UNSUPPORTED BY MORE RELICS PUBLISHER`

This is stronger than “compatibility not documented.” It is a direct upstream support mismatch.

It does **not** prove a crash in this exact pack. Until real runtime validation exists, the correct engineering state is:

`PROVIDER-SPECIFIC PATHS FAIL-CLOSED / RUNTIME COMPATIBILITY BLOCKER`

The existing curatorial decision `Manter` is preserved as requested; it does not become a compatibility claim.

## Provider identity and authority

More Relics is an addon to **Relics**. It does not own the base Relics progression/equipment engine.

Authority split:

- **Relics** owns the host relic framework, progression/data lifecycle, base equip/experience/evolution contracts and provider architecture;
- **More Relics** owns its addon relic content, its addon-specific abilities/statuses/evolution relationships/configs and addon loot placement;
- **Curios** owns accessory-slot plumbing where used by the provider stack;
- Black Arcana must not create a second relic progression ledger or re-settle addon abilities.

## Public content inventory

The current publisher description says **25+** high-quality relics and publicly lists **29 named relics** with loot/evolution routes. The discrepancy is not treated as an error: `25+` is an approximate lower-bound claim, while the visible list contains 29 names at the audited checkpoint.

See [`RELIC-CATALOG.md`](RELIC-CATALOG.md) for the full publisher-visible list.

### Public evolution chains

The current description establishes at least these evolution relationships:

- Tyrant Mask → **King Crimson**;
- Slumbering Amulet → **Whispering Amulet** → **Made in Heaven**;
- Depleted Spool → **Weavers Spool**;
- Converging Orb → **Wonder of U**.

Evolution remains provider/Relics-owned. Black Arcana/RPG progression must not grant the evolved item directly merely because a prerequisite item is present.

## Current 1.7.7 behavior surfaces

The exact 1.7.7 changelog documents provider-owned changes for:

- relic icon indicators — individually disableable client-side;
- **Moodworm** — status indicator, minor buff, corrected NeoForge starting-stat typo, configurable mood-change duration;
- **Twin Fangs** — fix attempt for an infinite-hit condition;
- **Eject Button** — configurable health threshold;
- **Bionic Eye** — configurable Vulnerability levels;
- **Cyberpsychosis** — also renders iron golems as wardens.

These are semantic/public release facts. Exact registry IDs, formulas and implementation internals remain unverified.

## Earlier current-line behavior evidence

Recent publisher changelogs additionally establish:

- **Swiftedge** and **Runic Plate** added in 1.7.5;
- Eject Button support for charm and ring slots in 1.7.6;
- visual status icons above the food bar in 1.7.6;
- **Mass Gauntlet** damage-boost cooldown added/configurable in 1.7.6;
- **Twin Fangs** added in 1.7.3;
- 1.7.0 fully reworked **Made in Heaven** and introduced a known stale extended-config crash path after upgrades.

Older publisher changelog facts help identify provider semantics, but exact current numbers are not inferred when not restated.

## Upgrade/config migration risk

The publisher warns that upgrading from an older More Relics version to `1.7.0+` can produce a `data is null` crash for **Made in Heaven** when Relics extended configs are enabled and stale ability values remain.

The documented recovery is to disable extended configs or regenerate the relevant More Relics config file; servers may require cleanup on both server and client.

This is not claimed to affect a fresh current installation automatically. It is a persistent-world/config migration QA item for the modpack.

## Black Arcana overlap

More Relics occupies item-driven capability space, including:

- passive/conditional combat bonuses;
- active relic abilities;
- health-threshold behavior;
- target debuffs such as Vulnerability;
- movement/physics-adjacent utility;
- status/effect presentation;
- progression/evolution from one relic into another;
- specialized loot acquisition.

This means a Black Arcana artifact should not duplicate an existing More Relics item by merely moving the same ability into a forbidden-magic item.

However More Relics does **not** own:

- Black Arcana casting transactions;
- Arcane Danger;
- Corruption/Strain/Backlash;
- Black Arcana ritual authority;
- Mortal Ledger/Soul Anchor semantics;
- Black Arcana world-effect policy.

## Files

- [`RELIC-CATALOG.md`](RELIC-CATALOG.md) — 29 publisher-listed relic names, loot/evolution routes and confidence boundaries;
- [`INTEGRATION-RULES.md`](INTEGRATION-RULES.md) — Relics/Curios/RPG/Black Arcana authority and deduplication rules;
- [`TECHNICAL-AUDIT.md`](TECHNICAL-AUDIT.md) — exact artifact/support mismatch/provenance/runtime QA gates.

## Remaining gates

1. runtime-load exact More Relics 1.7.7 + Relics 0.12.8 + Curios 9.5.1 in the actual pack;
2. verify whether the explicitly unsupported combination crashes, disables content, corrupts progression, or appears to work despite lack of support;
3. validate Relics data/progression/evolution persistence under 0.12.8;
4. validate all More Relics slot types and Curios integration;
5. test evolved relic migration and persistent data after save/reload;
6. check the 1.7.0 Made in Heaven extended-config migration hazard against the current instance configs;
7. validate client/server status icons and ability state without leaking gameplay authority to the client;
8. identify a supported external provider boundary before any Black Arcana/RPG provider-specific integration;
9. re-audit when the author actually publishes the promised/possible 0.12.8 compatibility build.

## Phase 3 disposition

`CATALOG ADVANCED / CURRENT PACK DEPENDENCY COMBINATION EXPLICITLY UNSUPPORTED UPSTREAM / PROVIDER-SPECIFIC IMPLEMENTATION FAIL-CLOSED`

No Phase 3 integration should depend on More Relics-specific state while the pack remains on Relics 0.12.8 unless real compatibility is demonstrated and the provider contract is separately verified.