# Asterism Arcanum 0.1.0 — Iron's 3.16.3 host loot eligibility audit

Status: `EXACT HASH-MATCHED ASTERISM 0.1.0 ARTIFACT + EXACT IRON'S 3.16.3 SOURCE / NO PACKAGED GATEWAY HOST OVERRIDE / ASTRAL GATEWAY DEFAULT LOOT-ELIGIBLE / DEPLOYED SPELL CONFIG STILL UNVERIFIED`

## Exact sources

Asterism:

- repository: `BirdieVibes/Asterism-Arcanum`;
- source pin: `f1738c7813a85d31a6da10e6c9f2dbce18d2b583`;
- physical provider line: `asterismarcanum-1.21.1-0.1.0.jar`.

Iron's Spells 'n Spellbooks:

- repository: `iron431/Irons-Spells-n-Spellbooks`;
- exact source checkpoint: `e4056af90302d37eb1739f5ff05020b020e6e252`;
- `gradle.properties` at that checkpoint identifies the pack host line `1.21.1-3.16.3`.

## Asterism spell facts

`AstralGatewaySpell` is an active `AbstractSpell` with:

- registry resource: `asterismarcanum:astral_gateway`;
- default school: `asterismarcanum:astral`;
- minimum rarity: `LEGENDARY`;
- max level: `1`;
- no provider override of `allowLooting()`;
- no provider override of `isEnabled()`;
- no provider override of `allowCrafting()`.

Its `DefaultConfig` does not explicitly set `enabled=false` or `allowCrafting=false`.

Asterism constructs the Astral school with the seven-argument Iron's `SchoolType` constructor. In exact Iron's 3.16.3 source, that constructor delegates to:

`requiresLearning=false, allowLooting=true`.

Therefore the Astral school is loot-enabled by default.

## Astromancer loot path

Exact Asterism loot resource:

`data/asterismarcanum/loot_table/entities/astromancer.json`

contains an `irons_spellbooks:scroll` using:

- function: `irons_spellbooks:randomize_spell`;
- quality range: `0.25 .. 0.85`;
- spell filter school: `asterismarcanum:astral`.

## Iron's 3.16.3 selection semantics

Exact `SpellFilter` behavior for a school filter is:

- include spells returned for the selected school;
- require `spell.isEnabled()`;
- require `spell.allowLooting()` unless `force=true`.

Exact `AbstractSpell.allowLooting()` returns the current spell school's `allowLooting` flag.

Exact `RandomizeSpellFunction` does **not** use `quality` to filter spell rarity. It:

1. builds the applicable spell list first;
2. weights each spell by minimum rarity;
3. chooses a spell from that weighted list;
4. only then uses `quality` to calculate the selected spell's level.

Weights are:

- Common 40;
- Uncommon 30;
- Rare 15;
- Epic 8;
- Legendary 4.

Therefore the Astromancer `quality 0.25..0.85` range does **not** exclude a Legendary spell. If Astral Gateway remains enabled, remains in the Astral school and retains the Astral school's default loot eligibility, it is a legitimate candidate in this provider-native loot path.

## Exact host config authority

Iron's 3.16.3 `SpellConfigManager` reads effective spell config from:

- local config root: `/config/irons_spellbooks_spell_config/`;
- per-spell local file: `/config/irons_spellbooks_spell_config/<mod_id>/<spell_id>.json`;
- global fallback: `/config/irons_spellbooks_spell_config/global_config.json`;
- datapack override: `/data/<mod_id>/irons_spellbooks_spell_config/<spell_id>.json`.

For Astral Gateway, the exact per-spell targets are:

- `/config/irons_spellbooks_spell_config/asterismarcanum/astral_gateway.json`;
- datapack resource `/data/asterismarcanum/irons_spellbooks_spell_config/astral_gateway.json`.

Relevant host parameters are:

- `irons_spellbooks:enabled` — default `true`;
- `irons_spellbooks:school` — Asterism default `asterismarcanum:astral`;
- `irons_spellbooks:allow_crafting` — default `true`.

The active config manager also permits global fallback values and applies datapack overrides. Source defaults are not substituted for deployed pack values.

## Closure consequence

This audit removes two false avenues from the Asterism blocker:

- Legendary rarity does **not** exclude Astral Gateway from the Astromancer loot pool;
- Astromancer `quality 0.25..0.85` does **not** exclude Astral Gateway.

The remaining current-pack catalog question is narrower:

1. is `asterismarcanum:astral_gateway` effectively `enabled`?
2. is its effective school still `asterismarcanum:astral`?
3. for crafting, is `allow_crafting` effectively enabled?
4. does any deployed datapack/global config override those values?

Without deployed config/datapack evidence, the catalog must still treat Astral Gateway as **⚠️ conditional** rather than assert survival availability from defaults.

Asterism/Iron's remain runtime authority. Black Arcana does not recreate the spell, alter provider config, or synthesize an acquisition route.


## Exact 0.1.0 binary corroboration — 2026-09-26

NON-MERGE exact-artifact audit commit `1c27d711f1359075edc403d30e86de9397a38f13` / CI run `36252798657` hash-matched publisher File `8157080` to physical SHA-1 `4a25ba80116168ddcc812f71467c0598127e774a`.

The exact binary independently confirms the narrow host-gate assumptions used above:

- `ASARSpellRegistry.class` references all 11 expected registered spell classes;
- Trailblaze is not referenced by the exact binary registrar;
- the exact artifact packages zero `irons_spellbooks_spell_config` resources;
- it packages zero `astral_gateway` host override resources;
- `AstralGatewaySpell` declares none of `allowLooting`, `allowCrafting`, `isEnabled` or `canBeCraftedBy`;
- the Astromancer loot resource is present.

Therefore there is no provider-packaged override that resolves Gateway's effective deployed state one way or the other. The remaining uncertainty is external deployed Iron's config/datapack state, exactly as this checklist requires.
