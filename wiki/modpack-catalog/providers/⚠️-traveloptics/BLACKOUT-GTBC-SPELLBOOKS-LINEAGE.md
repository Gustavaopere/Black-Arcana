# Blackout — GTBC's Spellbooks / T.O line boundary

Status: `OFFICIAL CROSS-PROJECT LINEAGE CLOSED / HISTORICAL GTBC ROUTE CONFIRMED / CURRENT TRAVELOPTICS ACQUISITION STILL UNVERIFIED`

## Purpose

This checkpoint separates three facts that must not be collapsed into one acquisition claim:

1. the full **T.O Tweaks / T.O Magic 'n Extras** line has a documented Dead King → Blackout route;
2. the separate **GTBC's Spellbooks** project also carried that route in its own `gametechbcs_spellbooks` namespace;
3. the exact audited 1.21.1 Traveloptics alpha registers `traveloptics:blackout` but does not expose the supporting Dead King route in the structured/registry surface already closed by Black Arcana.

The first two facts strengthen historical lineage. They do not establish Survival acquisition for the third artifact.

## Official project relationship

GameTechBC's official GTBC's Spellbooks project describes itself as a **cut-down version of T.O Tweaks**, retaining unique spells without the full project's extra dependency surface.

The current official T.O Magic 'n Extras page states that the project was formerly named **T.O Tweaks**.

Therefore these are related publisher-owned lines, but they remain **separate projects / namespaces / artifacts** for catalog authority:

- T.O project: CurseForge project `1046916`; current 1.21.1 namespace `traveloptics`;
- GTBC's Spellbooks project: CurseForge project `1125198`; namespace `gametechbcs_spellbooks`.

Black Arcana does not transfer registry or acquisition facts between those namespaces merely because the publisher documents a shared lineage.

## GTBC's Spellbooks route

Official GTBC's Spellbooks File `5927811` (`gametechbcs_spellbooks-2.0.0-1.21`) introduced **Blackout** and reworked **Call Forth The Dead King** so that the summoned Enraged Dead King could yield the exclusive Blackout spell.

Official File `6167362` (`2.6.5-1.21.1`) still documents Call Forth The Dead King / Enraged Dead King behavior and Blackout fixes, showing that this route remained part of the GTBC line before the final 3.0.0 release.

Official File `6312018` is the final `gametechbcs_spellbooks-3.0.0-1.21.1.jar` release.

## Retained pack runtime evidence

Project Library runtime evidence from **2026-08-16** contains:

- `gametechbcs_spellbooks-3.0.0-1.21.1.jar` in the loaded mod list;
- runtime attribute registration for `gametechbcs_spellbooks:call_forth_the_dead_king`;
- runtime attribute registration for `gametechbcs_spellbooks:blackout`.

This is historical evidence for the **GTBC namespace** only. It does not prove how Blackout was obtained in that particular session, and it does not become a `traveloptics:blackout` acquisition route.

Later retained runtime evidence from **2026-08-18 / 2026-08-19** observes `traveloptics:blackout` in the Traveloptics namespace.

Those observations prove registry presence at those historical runtime checkpoints, not Survival acquisition.

## Full T.O line

Official T.O File `6010839` (`Release-v3.0.1-1.20.1`) records the T.O 3.0.0 content tranche as adding together:

- Blackout;
- Call Forth The Dead King;
- Enraged Dead King.

The living T.O project page likewise documents Blackout as obtainable from the Enraged Dead King.

This strongly establishes the boss acquisition loop as a real **full-line T.O mechanic**.

## Exact 1.21.1 alpha boundary

Exact audited publisher File `6342780` for `traveloptics-4.4.0.1-1.21.1` differs materially from those full/cutdown line surfaces:

- `traveloptics:blackout` is one of the exact 33 registered spell IDs;
- `call_forth_the_dead_king` is **not** one of those 33 registrations;
- the audited 41 structured loot/loot-modifier JSON resources contain no Enraged Dead King acquisition surface;
- `BlackoutSpell` inherits the non-craftable Unique-spell gate;
- no direct provider-owned `TOSpells.BLACKOUT_SPELL` reference outside the registry was found.

Therefore the GTBC/full-T.O lineage **does not close** Blackout acquisition for the exact 1.21.1 alpha.

## Current physical boundary

The actually installed Traveloptics artifact remains SHA-1 `7b74816e89cc15dd0b5a31d9ea1e456024e8fae4` / `OTHER_VERIFIED` relative to publisher File `6342780`.

Historical modified-runtime evidence observed the same 33 Traveloptics IDs as the publisher baseline, including `traveloptics:blackout`, but the log is not cryptographically bound to the current physical hash.

Accordingly:

- current physical registry equality is still unclosed;
- current Blackout object-level acquisition is still unclosed;
- historical GTBC Spellbooks acquisition semantics cannot be used as a substitute.

## Fail-closed disposition

`traveloptics:blackout` remains:

`EXACT PUBLISHER REGISTRY IDENTITY / UNIQUE NON-CRAFTABLE / HISTORICAL RELATED-LINE ACQUISITION KNOWN / CURRENT SURVIVAL ACQUISITION UNVERIFIED`

To close it for the actual pack still requires one of:

1. exact-current physical `7b74816e...` byte/resource evidence establishing a Blackout route;
2. a pack-owned datapack/script/loot/progression route resolving specifically to `traveloptics:blackout`;
3. deterministic current-pack Survival acquisition observation cryptographically bound to the physical artifact.

Black Arcana must not alias `gametechbcs_spellbooks:blackout` to `traveloptics:blackout`, inject the Dead King route, or repair provider progression.
