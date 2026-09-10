# Tunes n' Tomes 1.1.0-HOTFIX — release-bounded provider catalog

## Status

`EXACT PHYSICAL 1.1.0-HOTFIX / EXACT PUBLISHER FILE 8370271 / CURRENT PUBLISHER MELODIC ROSTER 16/16 / SOURCE-JAR INTERNALS + RUNTIME QA PENDING / FAIL-CLOSED FOR PROVIDER-SPECIFIC HOOKS`

## Installed authority

- provider: **Tunes n' Tomes: a bards journey**
- mod id: `tunes_n_tomes`
- installed JAR: `tunes_n_tomes-1.1.0-HOTFIX.jar`
- runtime version: `1.1.0-HOTFIX`
- Minecraft / loader: NeoForge 1.21.1
- physical SHA-1: `6cac45631ea63577f8eeeab454e1df0ce8f78386`
- CurseForge project / exact file: `1509193 / 8370271`
- exact file published: `2026-07-04`, Release
- declared license: All Rights Reserved
- casting substrate: Iron's Spells 'n Spellbooks
- physical pack Iron's version: `3.16.3`

The physical modlist is authority for installed identity. The exact publisher file independently confirms the 1.1.0-HOTFIX artifact for NeoForge 1.21.1.

## Provider identity and ownership migration

Tunes n' Tomes is an Iron's addon that owns the **Melodic School**, its provider spells and the Resonance/Segno mechanic. Iron's remains authority for the generic spellcasting substrate, mana, spell registration/casting framework and provider-facing school infrastructure.

The 4.0 release changelog of Alshanex's Familiars explicitly removes Sound School from that mod and moves the Sound-related content to Tunes n' Tomes. FamiliarsLib 1.7 likewise removes its historical Sound content. Therefore the old Alshanex/FamiliarsLib Sound roster is not counted a second time under those providers.

The current Alshanex project/wiki still contains stale Sound/Bard prose. For 4.x ownership, the version-specific 4.0 migration changelog takes precedence over that stale generic description.

## Current publisher roster — 16 semantic spell identities

The current Tunes n' Tomes project page states that the Melodic School **features these spells** and enumerates exactly sixteen names:

1. Chord Blast
2. Crescendo
3. Grand Finale
4. Celestial Chant
5. Rhapsody
6. Sonata
7. Serenade
8. Fortissimo
9. Dal Segno
10. Swift Melody
11. Hymn of Hope
12. Slumber Note
13. Clamor Note
14. Encore
15. Harmonic Aria
16. Piercing Solo

For semantic-coverage accounting this closes a current publisher roster of **16** provider-owned spell identities at `COUNTED_RELEASE_BOUNDED` confidence. It does not prove registry IDs, classes, exact numerical values or byte-for-byte source/JAR equivalence.

The exact HOTFIX changelog only states that the build was updated to work with Iron's 3.16.2. It does not announce a spell-roster delta. The physical pack has Iron's 3.16.3, so runtime compatibility is still a regression gate rather than something inferred from the publisher's 3.16.2 statement.

## Resonance / Segno causal boundary

Publisher documentation describes Resonance as a mechanic in which eligible casts leave Segno markers and full Bard Armor can cause those markers to resonate and cast the spell again. This is a provider-owned amplification path.

Black Arcana must not:

- reinterpret one original cast plus its provider-created resonances as unrelated player intents;
- charge a second Black Arcana resource to represent an Iron's/Tunes settlement;
- duplicate provider cooldown or damage/heal settlement;
- infer that client particles/sounds are authoritative casts;
- award progression multiple times from one causal chain without an explicit deduplication contract;
- bypass provider PvP/targeting rules for `Encore` or other forced/repeated-cast behavior.

Any future integration must preserve one canonical causal identity or an explicitly verified parent/child identity supplied by a real provider seam.

## Current semantic overlap

The roster materially covers direct damage, stun/control, healing/protection, ally buffs, summon-like support, sleep/deafening, knockback, Segno teleportation and forced recast. These are existing provider capabilities for deduplication; visual or thematic similarity alone cannot justify a duplicate Black Arcana spell.

`Encore` is especially sensitive because publisher prose says it forces the targeted player to recast the last spell used. Exact validation, payment, cooldown, recursion and PvP behavior remain runtime/API QA items; no hidden protections are invented here.

## Runtime and implementation gates

Still unverified for the installed pack:

- exact spell registry IDs/classes and internal APIs;
- exact mana/cooldown/damage/range/duration values after config;
- runtime compatibility against Iron's 3.16.3 rather than the HOTFIX's stated 3.16.2 target;
- Resonance/Segno persistence, cleanup, caps and multiplayer causality;
- forced-recast recursion/permission behavior for Encore;
- stable supported integration hooks suitable for Black Arcana or RPG Skill Tree;
- exact source-to-installed-JAR equivalence.

Provider-specific integration therefore remains fail-closed until a safe current boundary is demonstrated.

## Sources

- physical modlist: current Black Arcana `modlist.txt`, SHA-1 `7aaece7acbfb07ba4d0c66029042f36c50d046f0`
- current project: `https://www.curseforge.com/minecraft/mc-mods/tunes-n-tomes-a-bards-journey`
- exact HOTFIX file: `https://www.curseforge.com/minecraft/mc-mods/tunes-n-tomes-a-bards-journey/files/8370271`
- Alshanex 4.0 migration release: `https://www.curseforge.com/minecraft/mc-mods/alshanexs-familiars/files/7920260`
