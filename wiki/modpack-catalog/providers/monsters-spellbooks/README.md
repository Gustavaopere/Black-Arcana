# Monsters & Spellbooks 0.0.16.3 — Iron's addon provider audit

## Status

`EXACT INSTALLED ARTIFACT 0.0.16.3 / EXACT CURSEFORGE FILE 8788560 / PUBLISHER PROJECT+CHANGELOG AUDITED / NECRO PRIMARY CURRENT SEMANTIC SURFACE / 90+ SPELL CLAIM + GEAR/MOBS/STRUCTURES RECORDED / AERO SOFT-DELETED IN 0.0.16.2 + REMNANTS REMOVED IN 0.0.16.3 / SOURCE REPO VERSION 0.0.14 + LICENSE METADATA CONFLICT / EXACT CURRENT REGISTRY NOT SOURCE-PINNED / GRANULAR CURRENT SPELL INVENTORY INCOMPLETE / PROVIDER-SPECIFIC IMPLEMENTATION FAIL-CLOSED`

## Runtime identity

Current physical modlist authority:

- provider: **Monsters & Spellbooks**;
- installed JAR: `monsterspellbooks-0.0.16.3.jar`;
- mod id: `monstersspellbooks`;
- runtime version: `0.0.16.3`;
- SHA-1: `b3aa89fd081bf4bfaf8d0f4380bcdc393c66ab0e`;
- CurseForge/package fingerprint: `3089819119`;
- loader/game: NeoForge 1.21.1;
- role: `IRON'S SPELL PROVIDER / GEAR / MOBS / STRUCTURES / CONTENT ADDON`.

## Exact publisher release

Official CurseForge evidence:

- project: **Monsters & Spellbooks: Iron's Spells 'n Spellbooks Addon**;
- author: RedTablos;
- project ID: `1428928`;
- exact file: `8788560`;
- exact filename: `monsterspellbooks-0.0.16.3.jar`;
- uploaded: `2026-09-01`;
- release channel: Release;
- game/loader: Minecraft 1.21.1 / NeoForge;
- CurseForge project license display: **MIT License**.

The publisher describes the addon as adding **90+ spells**, **2 new spell schools**, many gear items and spellcasting enemies. The longer current description says the content is mainly focused on the **Necro** school, whose stated identity is debuffs, damage over time and curses.

## Current public content claims

The publisher currently advertises at least:

- `12+` armor sets with spell stats;
- `90+` spells distributed across spell schools;
- `30+` weapons with unique skills/stats;
- `5+` ores used to upgrade Iron's gear;
- `10+` accessories and a new accessory slot;
- `10+` mobs with special spells;
- `2+` overworld structures.

These are **publisher cardinality claims**, not a verified exact registry count. The addon is explicitly described by its publisher as actively developed and likely to have content reworked, removed or added between updates.

## Necro authority

The current project description identifies **Necro** as the main school and characterizes it around:

- debuffs;
- damage over time;
- curses.

Current 0.0.16.x publisher changelogs additionally name active/reworked Necro-related surfaces such as:

- Fall Curse;
- Wither Bomb / Wither Bombs;
- Summon Death Knights;
- Soul Boost;
- Soul Chain;
- Necro Rune;
- Necro visuals.

Older publisher changelogs also expose numerous additional spell names. Those are cataloged as **public historical/current-line evidence** in [`PUBLIC-CHANGELOG-AUDIT.md`](PUBLIC-CHANGELOG-AUDIT.md), but exact 0.0.16.3 registry membership is not inferred when the current release does not explicitly restate it.

## Aero school — current exact-version contradiction

A material correction is required for any older catalog that treats Monsters & Spellbooks as an active Aero/Wind provider.

Publisher evidence says:

- the general project header still advertises **2 new spell schools**;
- historical releases contained Aero content;
- 0.0.16.2 explicitly says **`Soft Deleted Aero School, download Snackpirates Aeromancy instead`**;
- 0.0.16.3 explicitly says it deleted remaining Aero content from files to prevent tags from interfering.

Therefore the safe exact-version interpretation is:

`NECRO = ACTIVE PUBLISHER-IDENTIFIED SCHOOL`

`AERO = LEGACY/SOFT-DELETED SURFACE; DO NOT TREAT AS ACTIVE PROVIDER AUTHORITY WITHOUT RUNTIME REGISTRY EVIDENCE`

The pack already installs **SnackPirate's Aeromancy Additions 1.2.8**, so Black Arcana deduplication must prefer that real Wind/Aeromancy provider rather than resurrecting stale Monsters & Spellbooks Aero assumptions.

## Iron's authority relationship

Monsters & Spellbooks is an **Iron's Spells 'n Spellbooks addon**, not a replacement casting engine.

Iron's remains authority for the base spellcasting framework, including the host's mana/casting/cooldown/spellbook contracts. Monsters & Spellbooks owns the addon content it registers through that ecosystem.

Black Arcana must not:

- create a second mana cost for these spells;
- settle a second cooldown;
- duplicate damage/effect application after Iron's/provider settlement;
- reinterpret addon schools as Black Arcana schools merely because themes overlap;
- bypass provider acquisition/lootability restrictions.

## Arch / Hybrid gear progression

The publisher describes two armor design tiers/concepts:

- **Arch** — focused on builds specializing in one spell school and providing school-specific skills;
- **Hybrid** — focused on combinations of two compatible schools, trading some specialization for versatility.

These are Monsters & Spellbooks/Iron's gear-progression concepts. They are not RPG Skill Tree classes or specialization nodes.

## Required/optional ecosystem relations

Current CurseForge relations list:

Required:

- Iron's Spells 'n Spellbooks;
- Ace's Spell Utils;
- AzureLib.

Optional:

- AttributeFix;
- Better Combat.

The current pack contains Iron's `1.21.1-3.16.3`, Ace's Spell Utils `1.2.7.2-1.21.1`, AzureLib `3.1.11` and AttributeFix `21.1.3`.

0.0.16.2 additionally states that **Iron's Gems 'n Jewelry compatibility** was added. The current pack contains Iron's Gems 'n Jewelry `1.21.1-2.0.2`. Exact runtime behavior of this compatibility remains a QA item; the changelog establishes only the publisher's compatibility claim.

## Public-source mismatch and provenance blocker

CurseForge links a public repository:

`RedReaper28/Monsters-Spellbooks-1.21.1`

At the repository's current only branch/head inspected during this checkpoint:

- `gradle.properties` still declares `mod_version=0.0.14`;
- it declares `mod_license=All Rights Reserved`;
- it builds against Iron's `1.21.1-3.15.4`;
- the root contains `TEMPLATE_LICENSE.txt`, whose MIT text explicitly applies only to NeoForged template files;
- no matching 0.0.16.3 source revision/branch was located.

This conflicts with the current CurseForge project display of **MIT License** and does not match the installed/public release version.

Consequences:

- do **not** use current repository internals as exact 0.0.16.3 implementation authority;
- do **not** derive a 0.0.16.3 registry from the 0.0.14 tree;
- source-derived implementation remains blocked pending exact-version and license reconciliation;
- publisher release/changelog/gameplay information may still support factual semantic cataloging;
- exact current registry/API facts remain fail-closed.

## Exact 0.0.16.3 release delta

Publisher changelog for the installed release records:

- removal of remaining Aero content/files to avoid tag interference;
- increased Fall Curse slowness level;
- reduced the prior Wither Bomb nerf;
- further Necro visual changes;
- fix allowing Necro Rune to be placed into jewelry;
- correction of an attribute operation;
- correction of effects not being removed properly.

These are exact-release facts, but they do not expose exact spell numeric values or internal APIs.

## Provider overlap most relevant to Black Arcana

High-overlap capability families include:

- necromancy-themed offensive magic;
- curses/debuffs/damage-over-time;
- undead/soul-themed summons;
- wither/soul-fire interactions;
- gear that modifies school-specific spell builds;
- spellcasting hostile mobs;
- exploration structures tied to magical content.

This substantially narrows novelty space for generic “Necro school” clones. Any Black Arcana death/soul spell must be compared by actual semantics, cost, causal ownership and world effect rather than by name or VFX.

## Files

- [`PUBLIC-CHANGELOG-AUDIT.md`](PUBLIC-CHANGELOG-AUDIT.md) — publisher-visible current/historical spell and content evidence;
- [`INTEGRATION-RULES.md`](INTEGRATION-RULES.md) — authority/dedup/fail-closed rules;
- [`TECHNICAL-AUDIT.md`](TECHNICAL-AUDIT.md) — artifact/source/provenance/runtime QA gates.

## Remaining gates

1. obtain/pin exact public 0.0.16.3 source if the publisher exposes it later;
2. reconcile CurseForge MIT display with repository `All Rights Reserved` metadata;
3. prove current 0.0.16.3 spell/school registry rather than reusing 0.0.14 source;
4. resolve the stale `2 new spell schools` description versus exact 0.0.16.2/0.0.16.3 Aero removal in runtime;
5. runtime-test current Iron's 3.16.3 integration;
6. runtime-test current Iron's Gems 'n Jewelry 2.0.2 compatibility;
7. verify acquisition/lootability for named spells where earlier changelogs deliberately made some spells unlootable;
8. verify dedicated-server behavior and no double-processing with Black Arcana/RPG hooks.

## Phase 3 disposition

`CATALOG ADVANCED / EXACT CURRENT SPELL REGISTRY INCOMPLETE / PROVIDER-SPECIFIC IMPLEMENTATION FAIL-CLOSED`

The provider clearly occupies a large amount of necromancy/curses/summon/gear design space, but the exact current registry is not safely source-pinned.