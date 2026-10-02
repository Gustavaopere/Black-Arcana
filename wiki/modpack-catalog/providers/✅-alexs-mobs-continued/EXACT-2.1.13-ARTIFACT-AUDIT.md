# Alex's Mobs Continued 2.1.13 — exact artifact audit

Status: `EXACT PHYSICAL=PUBLISHER / INTERACTION DENOMINATOR CLOSED / 3 SUPERNATURAL ROOTS`

## Identity gate

Physical sibling authority identifies:

- `alexsmobs-2.1.13-neoforge+1.21.1.jar`;
- mod id `alexsmobs`;
- runtime `2.1.13`;
- SHA-1 `50ddafdf3d12b33331e4eecb4ab514ae451baadd`.

NON-MERGE PR #511 downloads CurseForge File `1635121 / 8856498` and fails before semantic inspection unless publisher SHA-1 equals the physical fingerprint.

Final bounded audit:

- HEAD: `59cb7ffaba397a84f64d047be4b51096e5a392e7`;
- audit run: `36949047824` — SUCCESS;
- artifact: `11202548934`;
- artifact digest: `sha256:e134c3ba8552fad8c0f174cf2dcd23eb112294a46506bdd1f8bceec6c5e8d31d`;
- publisher SHA-1: `50ddafdf3d12b33331e4eecb4ab514ae451baadd`;
- publisher SHA-256: `eef0b4d36f1e40292b23f90ad3052e2e9aace3a33c6a48c65b8b5f2b061ab6c8`;
- bytes: `27,452,738`.

Result: exact publisher/physical equality is proven.

## Bounded archive inventory

- archive entries: **5,584**;
- classes: **1,270**;
- non-class resources: **4,314**;
- top-level item classes: **45**;
- block classes: **27**;
- tile/block-entity classes: **12**;
- message classes: **22**;
- `data/alexsmobs/**` paths: **638**.

No third-party JAR bytes are committed to Black Arcana.

## Exhaustive activation pass

The audit disassembles every exact top-level item class and indexes relevant interaction signatures. It also scans all exact block classes for direct interaction hooks.

Results:

- item classes with relevant activation/interact signatures: **26**;
- block classes with relevant interaction/entity-inside signatures: **11**.

Every one of these 37 surfaces is dispositioned in the durable catalog rather than inferred from class naming.

## Exact supernatural control seams

### Dimensional Carver

Exact `ItemDimensionalCarver` bytecode establishes a deliberate channel/use action that:

- ray-traces the portal attachment/destination surface;
- creates `EntityVoidPortal`;
- sets attachment/destination/dimension/lifespan provider-side;
- adds the portal entity to the level;
- settles item durability.

This is one dimensional-passage semantic identity.

Exact acquisition is currently conditional: the shaped recipe requires Void Worm Eye and Mandible, and the exact provider loot surface supplies those through the Void Worm loot table.

### Mysterious Worm / Void Worm summon

Exact `ItemMysteriousWorm.onEntityItemUpdate` checks:

- `AMConfig.voidWormSummonable`;
- membership of the current dimension in `AMConfig.voidWormSpawnDimensions`;
- the provider depth condition;
- item liveness.

On success the provider consumes/kills the dropped item entity, constructs/configures the Void Worm, triggers the summon advancement for the owner when applicable and server-spawns the boss.

The identity therefore exists exactly, but effective current-world eligibility is not proven because deployed config values are not captured.

### Transmutation Table

Exact block/menu/message/block-entity inspection closes one direct player action:

- player opens the Transmutation Table UI;
- provider exposes three current possibilities;
- a menu selection routes to the server-side transmutation path;
- the selected result replaces the input;
- configured XP levels are removed;
- provider records the transmutation and rerolls result state.

Exact recipe `alexsmobs:transmutation_table` closes catalog-level owner acquisition. This is one parameterized transmutation identity rather than one identity per possible input/output.

## Capsid processing surface

The exact artifact contains four `CapsidRecipe` JSONs. Exact `BlockCapsid`/`TileEntityCapsid` control shows item insertion followed by automatic recipe matching, timed transformation and result replacement.

These four transformations are classified as processing/crafting infrastructure, not separate semantic player actions.

## Acquisition evidence

Exact data closes:

- Transmutation Table — shaped provider recipe;
- Capsid — Enderiophage entity loot plus block loot after placement;
- Mysterious Worm — exact Capsid recipe from Mosquito Larva;
- Dimensional Carver — exact shaped recipe from Void Worm Eye + Mandible + Netherite;
- Void Worm Eye/Mandible — exact Void Worm entity loot.

The last two roots remain conditional because normal current Void Worm summon eligibility is itself config-gated.

## Semantic disposition

- Transmutation Table — Item Transmutation: **1 `COUNTED_EXACT`**;
- Mysterious Worm — Void Worm Summoning: **1 `CONDITIONAL`**;
- Dimensional Carver — Dimensional Passage: **1 `CONDITIONAL`**;
- all other inspected item/block interactions: **EXCLUDED** from the semantic-magic metric.

Strict semantic contribution: **+1**.

## Clean-room boundary

The durable catalog retains hashes, identifiers, counts, method-level seams, owner/acquisition relations and behavior-level classification needed for cataloging. It does not redistribute JAR bytes, implementation bodies, assets or localization prose.
