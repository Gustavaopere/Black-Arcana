# Ice And Fire Community Edition 2.1.2 — exact artifact audit

Status: `EXACT PHYSICAL=PUBLISHER / CLEAN-ROOM ITEM-ACTION SURFACE + CURRENT-JAR REACHABILITY / SOURCE-SEMVER CORROBORATED`

## Provenance

Initial item-action audit:

- audit branch: `audit/iceandfire-ce-2.1.2-exact-artifact-2026-09-27`;
- initial audit HEAD: `1a1dd133d2c6c381b927b19702f70d04e422f6e2`;
- workflow run: `36316219802` — GREEN;
- text-only evidence artifact: `10930462794`;
- evidence-artifact digest: `sha256:292dbae5303da16c6c81796970c8e0b594c407fb45d0b8ce06f95278f5b94736`.

Reachability extension:

- extended audit HEAD: `a328f75e811540f97296fb68da3d4b70aa8239d6`;
- workflow run: `36323035696` — GREEN;
- text-only evidence artifact: `10933115713`;
- evidence-artifact digest: `sha256:06a3f1e1faefdcfc8e32080da6d1cf46d8980baa117e92c752b6778a1960818a`.

## Exact artifact identity

- CurseForge project/file: `1040076 / 8757837`;
- physical SHA-1: `0786f4142b7cabd958688f68beef3e63e9c0ae8b`;
- publisher/audit SHA-1: `0786f4142b7cabd958688f68beef3e63e9c0ae8b`;
- audit SHA-256: `3ce264a17bc06e5372077f64e80870d6c84ffbd5383aef59faeaa81d297769a6`.

Hash equality closes physical↔publisher artifact identity for both audit passes.

## Clean-room item-action facts

The hash-gated artifact contains **53** provider item classes under the bounded rule, **37** item classes declaring selected active/use-related methods, **39** candidate localization keys and **17** candidate recipe paths under the bounded legendary/active item name set. The audit retained class/resource identities and method signatures only.

## Exact source-semver corroboration

Public source pin `IAFEnvoy/IceAndFire-CE@0cf5a2458e1ccf552b9859531ee21c4816e5a686` declares `mod_version=2.1.2`. The following `gradle.properties` change bumps to 2.1.3, making this a version-exact semantic checkpoint.

The exact source confirms the nine candidate actions documented in [`ACTIVE-MAGIC-INVENTORY.md`](ACTIVE-MAGIC-INVENTORY.md), including the Ghost Sword `SUMMON_GHOST_SWORD` swing ability and its `phantasmalBladeAbility` gate.

## Exact current-JAR reachability facts

The extension scans exact `data/iceandfire/**/*.json` for the candidate item IDs after the same physical SHA-1 gate.

Closed exact acquisition references:

- `cockatrice_scepter` — recipe + recipe advancement;
- three `deathworm_gauntlet_*` variants — recipe + advancement each;
- `gorgon_head` — Gorgon entity loot table + advancement;
- `pixie_wand` — recipe + advancement;
- `siren_flute` — recipe;
- three `summoning_crystal_*` variants — recipe/reset-recipe surfaces;
- `stymphalian_feather_bundle` — recipe;
- `ghost_sword` — recipe + advancement + provider tag.

No exact provider data reference is present for `iceandfire:lich_staff`.

The source pin independently proves Dread Lich equips `IafItems.LICH_STAFF`, but no explicit provider-native staff drop chance/drop override has been proven. Generic vanilla equipment-drop behavior is not inferred.

## Semantic consequence

Seven independent action families are now **`COUNTED_EXACT`** on current artifact identity + exact provider reachability:

Cockatrice Scepter, Deathworm Gauntlet, Gorgon Head, Pixie Wand, Siren Flute, Summoning Crystal and Stymphalian Feather Bundle.

Two remain `CONDITIONAL`:

- Dread Lich Staff — acquisition not explicitly closed;
- Ghost Sword — acquisition closed, deployed `tools.phantasmalBladeAbility` unresolved.

## Limits

This audit still does not certify current deployed Jupiter values, runtime settlement, multiplayer correctness, balance, assembled-pack worldgen/entity availability or addon compatibility.
