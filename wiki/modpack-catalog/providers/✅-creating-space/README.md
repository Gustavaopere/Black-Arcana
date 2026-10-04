# Creating Space — 1.7.22

Status: `✅ CATALOGED / EXACT PHYSICAL=PUBLISHER ARTIFACT / ZERO_SEMANTIC_SPACE_ROCKET_DIMENSION_TRANSPORT / +0 STRICT / RUNTIME QA SEPARATE`

## Current physical identity

- sibling physical row: **#206**;
- JAR: `creatingspace-1.21.1-1.7.22.jar`;
- mod id: `creatingspace`;
- runtime: `1.7.22`;
- Minecraft / loader: 1.21.1 / NeoForge;
- physical SHA-1: `6eca99ee07780ef8918ad6969809f15ed0b1371c`.

Creating Space is a Create-based aerospace/planet-travel addon. Its dimension changes are part of rocket/vehicle/world-transition infrastructure, not provider-owned spell, ritual, glyph or supernatural-action identities.

## Exact publisher-artifact closure

NON-MERGE evidence PR **#558** audits CurseForge project/file `858897 / 8882869` and hard-gates the publisher artifact against the physical pack fingerprint.

- audit HEAD: `c4dc92b1827f270689be2166c6a71614172975e2`;
- exact-artifact run: `37159658138` — **SUCCESS**;
- evidence artifact: `11286778067`;
- evidence digest: `sha256:80593630e1b4b93780558d20d342ee52490599139563a2bef7cbb396faa6b1c7`;
- publisher SHA-1: `6eca99ee07780ef8918ad6969809f15ed0b1371c`;
- publisher SHA-256: `b80103cb546fc83aae2669e1906356ea87b587f59c437d8515e1cddd125f9be5`;
- bytes: `2,528,782`.

The publisher SHA-1 exactly equals the current physical pack SHA-1.

See [`EXACT-1.7.22-ARTIFACT-AUDIT.md`](EXACT-1.7.22-ARTIFACT-AUDIT.md).

## Exact semantic inventory

The exact artifact contains:

- **1,986** archive entries;
- **354** classes;
- **1,632** non-class resources;
- **690** `data/creatingspace/**` paths;
- **248** provider recipe JSONs under `data/creatingspace/recipe/**`;
- **6** exact `dimension` JSONs;
- **6** exact `dimension_type` JSONs;
- **6** exact `rocket_accessible_dimension` definitions.

Bounded semantic-name inventory is zero for:

- spell: **0**;
- magic: **0**;
- ritual: **0**;
- ability: **0**;
- arcane: **0**;
- glyph: **0**;
- summon: **0**;
- soul: **0**;
- portal: **0**;
- warp: **0**.

`dimension`, `planet`, `rocket` and one `teleport`-named infrastructure surface are expected because this provider implements physical aerospace travel.

## Dimension-transition boundary

Exact bytecode closes the only important semantic boundary. `CSEventHandler` detects orbit/planet transition conditions, resolves the planet below the current orbit and uses `CustomTeleporter`/`DimensionTransition` to move the player and, when applicable, the player's vehicle. Passenger state is restored after the vehicle transition.

This is vehicle/world lifecycle settlement. It is not exposed as a player-owned cast, spellbook action, ritual recipe, glyph, mana ability or supernatural action roster.

Rocket destination selection is represented by `RocketAccessibleDimension`, rocket schedule/destination instructions and Create-style vehicle controls. Destination, fuel/cost, launch state and vehicle persistence are parameters of aerospace transport rather than semantic magic identities.

## Authority boundary

Creating Space remains authority for:

- rocket assembly and flight state;
- accessible planet/dimension graph;
- rocket schedule and destination selection;
- player/vehicle dimension transition;
- aerospace resources, recipes and planet worldgen.

Create remains authority for its underlying contraption infrastructure. Black Arcana must not reinterpret rocket travel as teleport magic or mint one semantic action per destination.

## Semantic disposition

**`ZERO_SEMANTIC_SPACE_ROCKET_DIMENSION_TRANSPORT` / +0 strict.**

Detailed disposition: [`SEMANTIC-SURFACE-DISPOSITION.md`](SEMANTIC-SURFACE-DISPOSITION.md).

## Runtime QA remains separate

Catalog closure does not assert assembled-pack runtime PASS. Rocket assembly/disassembly, launch/arrival, passenger preservation, inventory/block-entity state, reconnect/restart, Create version compatibility, Create: Interactive coexistence and Northstar overlap remain runtime/integration QA.

## Result

**✅ Cataloged — zero provider-owned semantic magic objects.**

Strict semantic delta: **+0**.
