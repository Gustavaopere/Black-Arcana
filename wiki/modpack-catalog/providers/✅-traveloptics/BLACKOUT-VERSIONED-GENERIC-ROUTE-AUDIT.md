# Traveloptics Blackout — current versioned named generic-surface boundary

Status: `NAMED FILTERS + AUDITED DIRECT IRON'S CONSTRUCTION/ITEM-DELIVERY SURFACES NEGATIVE / DYNAMIC OR UNENUMERATED VERSIONED ROUTES NOT UNIVERSALLY EXCLUDED / ASSEMBLED EXTERNAL + CURRENT PHYSICAL ROUTES UNRESOLVED / FAIL-CLOSED`

## Purpose

This checkpoint closes one narrower exception left by the retained external-route search for `traveloptics:blackout`:

> Do the **current versioned Black Arcana or RPG Skill Tree repositories** contain a generic Iron's acquisition surface that could admit Blackout without naming `blackout` or `traveloptics` literally?

For the current versioned project-owned surfaces audited here, the answer is **no route identified**.

This is not a complete assembled-pack absence proof.

## Authority pins

Black Arcana:

- repository: `Gustavaopere/Black-Arcana`;
- audited main: `4749aac3b2a07e0b2ffdc5f76d55c69b76d53cd2`.

RPG Skill Tree sibling:

- repository: `Gustavaopere/neoforge-rpg-skilltree`;
- audited main: `de80b186357cad20ba5b81892a8682777e96e35a`.

## Generic Iron's surface search

Current default-branch code search on both repositories returned no versioned occurrence of:

- `SpellFilter`;
- `RandomizeSpellFunction`;
- `spell_filter`;
- `randomize_spell`.

These are the specific generic host surfaces left open by the previous literal/object-specific audit.

A search miss alone is not treated as repository-exhaustive evidence; the repository trees and the concrete runtime surfaces below were also inspected.

## RPG Skill Tree — complete tree boundary

The sibling Git tree for `de80b186...` was fetched recursively with `truncated=false`:

- total entries: **4,503**;
- versioned `.js` files: **2**;
- `server_scripts` paths: **0**;
- `startup_scripts` paths: present only under `integration-templates`;
- the two `.js` paths are duplicate template placements of `volcanoes_rns_worldgen.js`, not an assembled KubeJS script tree.

Therefore the sibling repository does not version a current assembled `kubejs/server_scripts` tree that could be treated as pack acquisition authority.

### Versioned loot modifier

The only NeoForge global-loot-modifier entry in the sibling runtime resources is:

`rpgskilltree:reward_risk`.

Direct inspection establishes:

- `global_loot_modifiers.json` contains only `rpgskilltree:reward_risk`;
- `RewardRiskLootModifier` receives **already generated** `ItemStack` entries;
- it scales/copies existing stackable loot and intentionally leaves non-stackable entries copied unchanged;
- it does not select spell IDs, construct scroll identities, invoke Iron's `SpellFilter`, invoke `RandomizeSpellFunction`, or grant a spell.

Thus this versioned GLM is not a generic Blackout acquisition route.

### Versioned Iron's progression adapter

`IronsSpellbookProgressionEvents` was inspected directly.

Its relevant responsibilities are:

- canceling casts when Arcane Access is absent;
- gating permanent inscription by progression/mastery;
- awarding mastery after successful casts.

It does not create scrolls, grant spell identities, inject loot, or provide an acquisition source.

The versioned Eldritch specialization/tree-unlock JSONs contain only class/tag/mastery/domain requirements. They are progression gates, not item/spell grants.

## Black Arcana — complete tree boundary

The Black Arcana Git tree for `4749aac3...` was fetched recursively with `truncated=false`:

- total entries: **3,878**;
- versioned `.js` files: **0**;
- `server_scripts` paths: **0**;
- `startup_scripts` paths: **0**;
- runtime/source paths named for loot/reward/Blackout/Traveloptics generic acquisition: **0** outside catalog documentation/QA observation.

All **16** current `src/main/resources/**/*.json` files were read and checked for:

- `traveloptics`;
- `blackout`;
- `spell_filter`;
- `randomize_spell`;
- `eldritch`;
- `loot`.

Result: **0 matching runtime-resource JSONs**.

The existing catalog QA probe remains observational only and is not an acquisition surface.

## What this establishes

For the two current versioned project repositories:

- literal/object-specific Blackout route — **NOT FOUND**;
- named Iron's `SpellFilter` / `RandomizeSpellFunction` route — **NOT FOUND IN THE AUDITED VERSIONED TREES**;
- RPG Skill Tree versioned global loot modifier as a Blackout route — **EXCLUDED**;
- RPG Skill Tree Iron's progression adapter as a Blackout grant — **EXCLUDED**;
- Black Arcana versioned KubeJS/script acquisition surface — **ABSENT FROM THE AUDITED TREE**;
- sibling versioned assembled `server_scripts` tree — **ABSENT FROM THE AUDITED TREE**.

A later bounded full-`src/main` audit now additionally excludes the **direct Iron's spell-container/scroll construction APIs and reviewed generic item/reward candidates** enumerated in [`BLACKOUT-VERSIONED-ACQUISITION-SURFACE-AUDIT.md`](BLACKOUT-VERSIONED-ACQUISITION-SURFACE-AUDIT.md). That audit scanned 482 Java + 22 resource blobs in Black Arcana `da8a5c18...` and 1,144 Java + 724 resource blobs in sibling `de80b186...`, with zero occurrences of the audited direct Iron's construction/lookup tokens and zero Traveloptics/Blackout/scroll/container resource tokens. It still does **not** prove that every conceivable versioned route is absent: reflection, encoded/dynamic invocation or semantically equivalent custom code not containing those tokens remains outside the negative claim.

## What remains open

This checkpoint does not prove complete current-pack absence because it does not capture:

- the actual assembled instance's external KubeJS folders if they exist outside these repositories;
- user/world datapacks not versioned here;
- other installed mods that may inject a generic Iron's scroll/spell route;
- current physical Traveloptics SHA-1 `7b74816e89cc15dd0b5a31d9ea1e456024e8fae4` content;
- a live survival/world acquisition test.

Therefore the broader assembled-pack generic external route remains **UNRESOLVED**.

## Gate 3 consequence

Blackout remains:

`REGISTERED / UNIQUE / NON-CRAFTABLE / NON-LOOTABLE IN EXACT ALPHA / PROVIDER BUILT-IN ROUTES EXCLUDED / NAMED FILTERS + AUDITED DIRECT VERSIONED CONSTRUCTION/DELIVERY SURFACES NEGATIVE / DYNAMIC + ASSEMBLED EXTERNAL + CURRENT-PHYSICAL ROUTES UNVERIFIED`.

Traveloptics remains:

`⚠️ partial / conditioned / strict +0`.

No acquisition route is synthesized by Black Arcana.
