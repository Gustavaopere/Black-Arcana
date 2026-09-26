# More Relics 1.7.7-forRelics-0.12.8 — JAR closure checklist

Status: `PHYSICAL BUILD IDENTIFIED / PUBLISHED CONTENT ENUMERATED / EXACT JAR ABILITY INVENTORY REQUIRED`

## Required artifact

Obtain the exact current pack file:

`morerelics-1.7.7-forRelics-0.12.8-1.0-1.21.1.jar`

Expected SHA-1 from the current sibling physical dossier:

`bc220ed291187c97bd1896f1fdd29b2377879ae1`

Official CurseForge file:

`8859015`

Do not audit the main `morerelics-1.7.7-1.21.1.jar` instead; that is a different line requiring Relics 0.10.7.8.

## Structural inventory

After hash verification, enumerate without copying proprietary implementation:

1. `META-INF/neoforge.mods.toml` / mod metadata;
2. registered item/resource IDs owned by `morerelics`;
3. Relics ability-template or equivalent owner/ability IDs referenced by provider classes/data;
4. evolution definitions and source→target identities;
5. loot/data files establishing survival acquisition;
6. common/client config names and defaults relevant to semantic availability;
7. packet/mixin surfaces only as needed for interoperability.

## Semantic counting rule

For every provider-owned relic, record zero, one or multiple discrete supernatural ability roots.

Count a root only when the exact artifact establishes a distinct player-facing/provider-owned causal action under the Black Arcana metric.

Do not count as extra identities:

- relic items themselves;
- passive stats/modifiers;
- ranks/levels;
- evolution stages unless they expose a distinct ability root;
- projectiles/entities/effects spawned downstream;
- loot entries;
- UI indicators;
- repeated ticks/procs of one persistent ability.

## Ownership and deduplication

If More Relics delegates to a generic Relics ability ID, attribute ownership according to the actual registration/template authority. Do not count the same generic framework ability once in Relics and again in More Relics unless the provider creates a distinct owner-scoped semantic action.

## Survival / strict eligibility

For every counted ability root, close:

- relic acquisition or evolution path;
- any config enable/disable gate;
- any required equipment slot;
- normal survival reachability;
- debug/admin-only exclusions.

## Clean-room

Project license is All Rights Reserved. Binary inspection is for factual interoperability/catalog metadata only. Do not copy code, assets, localization or implementation text into Black Arcana.

## Promotion condition

Promote from ⚠️ only after the exact installed artifact is hash-matched and every provider-owned ability root is enumerated/deduplicated with reachability evidence.

Until then:

- published relic identities: **29**;
- strict semantic addition: **+0 pending closure**;
- status: **⚠️ partial / conditioned**.
