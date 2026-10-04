# Creating Space 1.7.22 — exact artifact audit

Status: `EXACT PHYSICAL=PUBLISHER / ZERO PROVIDER-OWNED MAGIC-ACTION ROSTER`

## Identity gate

- physical JAR: `creatingspace-1.21.1-1.7.22.jar`;
- mod id: `creatingspace`;
- runtime: `1.7.22`;
- physical SHA-1: `6eca99ee07780ef8918ad6969809f15ed0b1371c`.

NON-MERGE PR #558 downloads CurseForge File `858897 / 8882869` and fails unless the publisher SHA-1 equals the physical fingerprint.

- audit HEAD: `c4dc92b1827f270689be2166c6a71614172975e2`;
- run: `37159658138` — SUCCESS;
- artifact: `11286778067`;
- digest: `sha256:80593630e1b4b93780558d20d342ee52490599139563a2bef7cbb396faa6b1c7`;
- publisher SHA-1: `6eca99ee07780ef8918ad6969809f15ed0b1371c`;
- publisher SHA-256: `b80103cb546fc83aae2669e1906356ea87b587f59c437d8515e1cddd125f9be5`;
- bytes: `2,528,782`.

Result: exact publisher/physical equality is proven.

## Archive inventory

- entries: **1,986**;
- classes: **354**;
- resources: **1,632**;
- provider-data paths: **690**;
- provider recipes: **248**;
- dimensions: **6**;
- dimension types: **6**;
- rocket-accessible-dimension definitions: **6**.

Semantic-name path/class counts from the bounded audit:

- spell 0;
- magic 0;
- ritual 0;
- ability 0;
- mana 6;
- arcane 0;
- glyph 0;
- summon 0;
- soul 0;
- teleport 1;
- portal 0;
- dimension 60;
- planet 20;
- rocket 257;
- warp 0.

The `mana` text hits do not establish a provider magic-resource system; no spell/ritual/ability registry accompanies them. Rocket/planet/dimension hits dominate the semantic surface.

## Exact travel control seam

The audit disassembles every provider class and finds dimension transitions in the aerospace lifecycle rather than a magic-action registry.

Key behavior-level facts:

- `RocketAccessibleDimension` defines the accessible interplanetary graph;
- rocket schedule/destination classes select travel targets;
- `CSEventHandler` resolves orbit/planet boundary transitions;
- `CustomTeleporter` produces the Minecraft `DimensionTransition`;
- when a player is riding a vehicle, the provider ejects passengers, transitions vehicle and player, then reattaches the player;
- transition settlement is tied to orbit/planet/rocket state, not a spell/ritual/glyph cast surface.

## Data surface

The provider data is dominated by:

- rocket engine/propellant/power/exhaust definitions;
- recipes and advancements;
- planet/orbit dimensions and dimension types;
- rocket-accessible-dimension graph entries;
- worldgen, ores, loot and technological blocks.

No provider-owned spell, glyph, ritual, rite, summon or discrete supernatural-action data family is present.

## Semantic disposition

`ZERO_SEMANTIC_SPACE_ROCKET_DIMENSION_TRANSPORT / +0 strict`.

One destination, planet, orbit, rocket stage or transition event is not counted as a magic action. These are parameters/states of one technological aerospace system.

## Clean-room boundary

The durable catalog retains hashes, counts, registry/path identities and behavior-level control-flow facts required for denominator classification. It does not redistribute JAR bytes, implementation bodies or assets.
