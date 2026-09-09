# Phase 2AO checkpoint — Soul Fire'd 6.1.0

## State

`CATALOG CLOSURE CANDIDATE / EXACT PHYSICAL+PUBLISHER+SOURCE VERSION / PROMETHEUS-BACKED FIRE CONTENT / NOT CANONICAL UNTIL LATEST-MAIN RECONCILIATION + EXACT-HEAD CI GREEN + MERGE`

## Base

- initial canonical main: `994d2983f0ec54fd54455a14abad473ebaea86bc`
- predecessor: Phase 2AN / PR #149, component #42
- branch: `docs/magic-catalog-phase2ao-soul-fire-d-6.1.0`
- canonical coverage at branch start: `42/100 = 42%`
- proposed result after canonical merge: `43/100 = 43%`

A branch with the intended Phase 2AO name was discovered during creation but pointed exactly at the same canonical main commit and contained no divergent work. No open PR equivalent for Soul Fire'd / Phase 2AO existed. The branch was therefore reused without moving its ref or discarding concurrent changes.

## Physical identity

- JAR: `soul-fire-d-neoforge-1.21-6.1.0.jar`
- mod id: `soul_fire_d`
- runtime: `6.1.0`
- physical SHA-1: `877002a5aa386f9011ebc4eb3360a7647ac359d9`
- physical NeoForge: `21.1.248`
- physical modlist: 595 top-level entries, SHA-1 `7aaece7acbfb07ba4d0c66029042f36c50d046f0`

## Exact publisher release

CurseForge:

- project `662413`;
- file `7364962`;
- filename `soul-fire-d-neoforge-1.21-6.1.0.jar`;
- uploaded `2025-12-22`;
- supports Minecraft 1.21 and 1.21.1;
- NeoForge;
- Client & Server;
- publisher license label `Custom License`.

Modrinth independently exposes the same 6.1.0 line and labels the project `Crystal Nest Community License v1`.

## Exact Soul Fire'd source

- repository `Crystal-Nest/soul-fire-d`;
- branch `1.21`;
- exact revision `0cc7a03b950e74742eb75f51642cc7a0190c7127`;
- tree `a43189fb8689041edb7993d94f85f64597f57303`;
- source version 6.1.0;
- Java 21;
- NeoForge baseline 21.0.143, runtime range `[21.0,)`;
- Cobweb 1.4.0;
- Prometheus 1.2.5.

The physical pack matches Cobweb and Prometheus exactly and satisfies the NeoForge range.

## Exact Prometheus boundary pin

The generic fire API moved from Soul Fire'd to Prometheus in the 6.x architecture.

For exact physical Prometheus 1.2.5:

- repository `Crystal-Nest/prometheus`;
- branch `1.21`;
- revision `3edbe979b3a383b526f38daeba4eb35d18283a9d`.

Inspected only to establish the exact API/authority boundary consumed by Soul Fire'd:

- `FireManager.SOUL_FIRE_TYPE = minecraft:soul`;
- generic fire component registration is Prometheus-owned;
- generic fire-charge registration is Prometheus-owned.

This does not close Prometheus as its own catalog component.

## Closed semantic inventory

Exact Soul Fire'd 6.1.0 result:

- 0 standalone spells;
- 0 glyphs;
- 0 rituals;
- 0 provider mana/cast resource;
- 0 active common/NeoForge mixins;
- 1 Soul Fire definition through Prometheus (`minecraft:soul`);
- light 10;
- damage value 2;
- vanilla Soul Fire flame particle;
- 1 associated `minecraft:soul_fire_charge` item/resource/recipe family;
- 2 enchantments: `minecraft:soul_fire_aspect`, `minecraft:soul_flame`;
- 1 static enchantment datapack registered through Cobweb;
- 1 NeoForge GLM serializer: `soul_fire_d:chest_loot_modifier`;
- 1 bundled Bastion modifier instance with two independent 5% enchanted-book additions.

## Authority result

- Prometheus owns generic fire API/runtime/component registration.
- Soul Fire'd owns its Soul Fire-specific content/definitions, enchantment datapack and acquisition.
- Cobweb owns the registration/static-pack support it provides.
- Minecraft/NeoForge own their registries/event/loot infrastructure.
- Black Arcana owns BA magic runtime, hazards, safety policy, costs, cooldowns/charges, targeting, Corruption, Strain and Arcane Danger.
- RPG Skill Tree receives no fire or magic runtime authority.

## Clean-room / license

Exact source metadata declares `GPL-3.0-or-later`, and the exact source tree contains GNU GPLv3 text. Publisher distribution surfaces instead label the project Custom License / Crystal Nest Community License v1.

This discrepancy is preserved as a reuse/derivation blocker. Source was inspected read-only for factual catalog/interoperability analysis. No code/assets are copied or adapted.

## Remaining QA

Does not block semantic component closure:

- source↔physical-JAR byte reproducibility not proven;
- full 595-mod fire/damage/enchantment interaction QA not run by this catalog phase;
- optional publisher-listed integration hooks not promoted without exact seam evidence;
- runtime multiplayer behavior remains a regression surface;
- any future BA↔Prometheus integration still requires a deliberately verified boundary and must preserve `WorldEffectPolicy`/Backlash causality.

## CI / merge protocol

Before merge:

1. fetch latest main;
2. reconcile if advanced;
3. review exact diff;
4. require Black Arcana CI GREEN on exact reconciled HEAD;
5. re-fetch latest main immediately before merge;
6. merge with expected exact HEAD;
7. confirm final main SHA and PR merged state;
8. verify canonical coverage from final main.

Phase 3 remains blocked until the provider catalog/deduplication pass establishes real Black Arcana gaps.
