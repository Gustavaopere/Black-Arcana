# Reliquified Artifacts — 1.0.8

Status: `✅ CATALOGED / CURRENT PHYSICAL 1.0.8 / COUNTED_SOURCE_PINNED / 48 ARTIFACT OWNERS / 52 OWNER-SCOPED ABILITY ROOTS / +52 STRICT / ASSEMBLED QA SEPARATE`

## Current physical identity

Current physical Project Library authority records:

- JAR: `reliquified_artifacts-1.21.1-1.0.8.jar`;
- mod id: `reliquified_artifacts`;
- runtime: `1.0.8`;
- mixin config: `reliquified_artifacts.mixins.json`;
- physical SHA-1: `00ad43d5a1aa287fd0084bc3b48546821494ff80`;
- Minecraft / loader: 1.21.1 / NeoForge.

Official CurseForge identifies the 1.21.1 `1.0.8` build as the current Beta release published 2026-08-22. The project is All Rights Reserved; this catalog is clean-room factual inspection only.

## Exact source-version checkpoint

Official repository: `Octo-Studios/reliquified-artifacts`.

Checkpoint: `529fa0cd865a95dbe1bf02081de0275e90c69aee` on branch `1.21.1`.

The checkpoint is dated 2026-08-22 with commit message `Version bump - 1.0.8`; `gradle.properties` declares `mod_version=1.0.8`, Minecraft 1.21.1 and NeoForge development baseline 21.1.194.

This is an exact **source-version** checkpoint. Reproducible physical-JAR↔source-build byte equality is not claimed.

## Ownership model

Reliquified Artifacts is not a parallel item registry containing copies of the Artifacts inventory. Its `ModItemsMixin` redirects the original Artifacts registrations to Reliquified classes:

- **48 `artifacts:<id>` owners** are replaced/extended;
- those owners map to **47** Reliquified implementation classes;
- `plastic_drinking_hat` and `novelty_drinking_hat` intentionally share `DrinkingHatItem`;
- the provider's own `RAItems` registry separately adds `reliquified_artifacts:mimi_dust`, which is a utility item and not one of the counted ability roots.

Therefore the semantic owner remains the concrete Artifact item identity while Reliquified Artifacts owns the Relics ability implementation layered onto it.

## Semantic inventory

Exact source inspection closes **51 class-level `AbilityTemplate.builder(...)` roots**. Expanding the shared Drinking Hat class across its two distinct Artifact owners yields **52 owner-scoped ability roots**. The English localization contains the same **52 owner/ability roots**, providing an independent cardinality cross-check.

See [`ABILITY-INVENTORY-1.0.8.md`](ABILITY-INVENTORY-1.0.8.md) for all 52.

Owner-scoped counting is required here: ability strings such as `meal` and `jump` are reused under different Artifact owners and are not collapsed across those distinct provider objects.

## Reachability

Of the 48 Artifact owners:

- **47** are backed by implementation classes carrying a provider `LootTemplate`;
- `artifacts:eternal_steak` is the only owner without a direct class-local `LootTemplate`.

`artifacts:everlasting_beef` does have a village loot route. The exact 1.0.8 source then converts Everlasting Beef into Eternal Steak through both furnace and campfire mixins, using provider-preserving stack transmutation. This closes the remaining source-level acquisition path.

Result: all **52** owner-scoped ability roots have a bounded provider/source acquisition route.

## Semantic disposition

The Black Arcana semantic metric counts discrete provider-owned supernatural ability roots while excluding gear containers, rank modifiers, metrics, statistics and downstream consequences.

Reliquified Artifacts therefore contributes:

**+52 `COUNTED_SOURCE_PINNED` semantic magic objects**.

This does not count the 48 Artifact item containers, `mimi_dust`, loot entries or rank modifiers as additional magic objects.

## Authority boundaries

- Artifacts owns the original item identities and base content lineage.
- Reliquified Artifacts owns the replacement Relics templates/ability behavior it injects for those owners.
- Relics owns the generic ability/progression/rank framework.
- Black Arcana must not create a duplicate relic XP/rank/cooldown/effect ledger or count one Artifacts event and one Reliquified event as two causal actions.
- Sophisticated Backpacks/Curios-equivalent infrastructure retains its own storage/equip authority.
- RPG Skill Tree remains sibling authority only for its own progression/contracts; it does not gain Relics/Artifacts runtime authority.

## Runtime QA remains separate

Catalog closure is not an assembled-pack PASS. Important runtime regression gates include:

- physical 1.0.8 + current Artifacts + Relics 0.12.8 boot;
- equip/unequip and modifier cleanup;
- XP/rank/cooldown persistence across relog/restart/death;
- Eternal Beef → Eternal Steak conversion preserving provider state;
- Universal Attractor + Sophisticated Backpacks pickup idempotence;
- active/proc abilities in dedicated multiplayer;
- no duplicate Artifacts + Reliquified processing;
- loot/spawn configuration and Mimic/Mimi-Dust behavior.

## Result

**✅ Cataloged — `COUNTED_SOURCE_PINNED`.**

Current semantic inventory: **52 owner-scoped Reliquified Artifacts ability roots**. Strict semantic delta: **+52**.
