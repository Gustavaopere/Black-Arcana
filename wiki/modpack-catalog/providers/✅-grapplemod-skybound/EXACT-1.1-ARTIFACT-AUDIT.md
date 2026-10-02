# Grappling Hook Mod: Skybound 1.1 — exact artifact audit

Status: `EXACT PHYSICAL=PUBLISHER / TRAVERSAL-PHYSICS DENOMINATOR CLOSED`

## Identity gate

- physical JAR: `grapplemod-1.1+1.21.1.neoforge.jar`;
- physical SHA-1: `2b6060de273f721857d715db9a811ddaa5422683`;
- publisher: CurseForge project/file `1559979 / 8176552`.

NON-MERGE PR #524 run `36967140184` succeeded with exact publisher/physical equality.

- artifact: `11210168195`;
- artifact digest: `sha256:b11c803c5f79c0e57334cf06cc710e7c4e83f027f790e51d51c56c4cf04eac53`;
- SHA-256: `6e973cff926db4b70cf36b745933ebdc1469e2c02eefd245f9c2fe3bf2eb1248`;
- bytes: `847,238`.

## Bounded archive inventory

The exact artifact contains:

- archive entries: **580**;
- classes: **285**;
- non-class resources: **295**;
- nested JARs: **2**;
- bounded provider JSON rows selected by Ender/teleport/forcefield/rocket/motor/magnet/grapple/hook keywords: **21**.

The keyword candidate count is intentionally broad and is not treated as a semantic count.

## Exact action-surface findings

### Ender Staff / Ender launch

`EnderStaffItem.use(...)` delegates to the provider client physics tracker's `launchPlayer(...)`. The exact launch path:

1. enforces the provider Ender-staff cooldown;
2. requires an Ender Staff or appropriately customized Grappling Hook in a hand;
3. derives the player's look vector;
4. creates/uses the provider `AIR_FRICTION` physics controller;
5. scales the look vector by the configured Ender-staff strength;
6. settles an Ender-launch movement vector through the provider physics layer.

No exact teleport-position setter, dimension transfer, portal settlement or spell/ritual registry is established by this path. It is a movement-launch mechanic despite the Ender naming.

### Forcefield

`ForcefieldItem.use(...)` toggles the provider `FORCEFIELD` physics controller. It is a movement/repulsion physics mode, not a spell identity.

### Rocket / motor / magnet / dual hook

These exact surfaces are upgrades/controllers inside the grappling-hook traversal system: propulsion, rope motor behavior, attachment attraction and multi-hook behavior. They do not expose an independent magic registry.

### Long Fall Boots

Passive traversal/fall equipment. No separate player-selected semantic magic action.

## Exact data evidence

The JAR packages crafting/smithing data for:

- `grapplemod:grappling_hook`;
- `grapplemod:ender_staff`;
- `grapplemod:forcefield`;
- `grapplemod:rocket`;
- hook upgrades for ender, magnet/forcefield, motor, rocket and double-hook behavior;
- Long Fall Boots.

Advancement data also treats Forcefield/Rocket as physics-controller state. These routes prove item/equipment reachability, not spell identity.

## Semantic disposition

Exact-current provider surface: **0 semantic magic objects**.

State: **`ZERO_SEMANTIC_TRAVERSAL_PHYSICS`**.

The provider remains catalog-relevant as a cross-domain false-positive closure because names such as Ender, Forcefield and Rocket could otherwise be misclassified as magic.

## Clean-room boundary

The durable record retains hashes, counts, identifiers and behavior-level control-flow classification necessary for interoperability/cataloging. It does not redistribute the JAR, source implementation bodies or provider assets.
