# Protection Pixel 2.2.1 — exact artifact audit

Status: `EXACT PHYSICAL=PUBLISHER / ZERO SEMANTIC MAGIC PROVIDER`

## Identity gate

Current physical sibling dossier:

- `protection_pixel-2.2.1-neoforge-1.21.1.jar`;
- mod id `protection_pixel`;
- runtime `2.2.1`;
- physical SHA-1 `c35da610425f735eea4d027ad159c88de6ec6e3f`.

NON-MERGE PR #520 downloads CurseForge File `1023409 / 7549821` and fails before semantic inspection unless the publisher SHA-1 equals the physical fingerprint.

Final audit:

- HEAD: `4c3168f33c2d702e19f97534436e26bb93faa10c`;
- run: `36962672381` — SUCCESS;
- evidence artifact: `11208357031`;
- digest: `sha256:0005d0954a20bf8b2aa8f06192c8f0ab8df12da8dbdfc435e173a1b673f8cc62`;
- publisher SHA-1: `c35da610425f735eea4d027ad159c88de6ec6e3f`;
- publisher SHA-256: `a496e6263a0c2cd4341f05a1a71085e467cfe85b453a6aef1c38f614b61129f4`;
- bytes: `2,608,196`.

Result: exact publisher/physical equality is proven.

## Bounded archive inventory

- entries: **1,292**;
- classes: **659**;
- resources: **633**;
- provider classes: **659**;
- procedure classes: **222**;
- item classes: **104**;
- input/network classes: **13**;
- provider data paths: **111**.

The audit disassembles the complete provider class set and indexes interaction/input, event, movement, damage, cooldown, shield, magnet, reactor and device seams.

## Input/action surface

The exact client key registry exposes exactly three named key mappings:

- `key.protection_pixel.armortabletrigger`;
- `key.protection_pixel.wingfly`;
- `key.protection_pixel.flyfoward`.

Exact provider procedures include active technological/device flows such as:

- `CannonactionProcedure` / cannon-shell handling;
- `HookcannonactionProcedure` / hook hit/release/tick handling;
- `ThrusteractionProcedure` / thrust movement;
- `WingactionProcedure`, `OpenwingactionProcedure`, `WingflyactiveProcedure` and `WingflyingProcedure`;
- `BlooddialysisProcedure`;
- armor/equipment handlers for hunter, lancer, plague, magnetic-storm, float-shield, drone and other gear families.

These procedures are equipment/device implementation surfaces, not a provider magic registry.

## Data/acquisition surface

The exact JAR packages Create and vanilla recipes/loot for provider items, armor, devices, shells, reactor/platform infrastructure and upgrades. Examples include Cannon Arm, Hook Cannon, Maneuvering Wing, Steam Exoskeleton, Suspended Jetpack, armor families and armor plates.

No exact provider recipe/resource defines a spell, ritual, glyph or other provider-owned magic identity.

## Negative semantic proof

A complete path/name scan of the exact JAR finds no provider-owned spell/ritual/rite/magic/mana/arcane/glyph/wizard/witch/sorcery/occult registry or resource surface.

The apparent `enchantable` paths are vanilla item-tag interoperability and do not represent Protection Pixel-owned enchantments/spells.

## Disposition

Protection Pixel 2.2.1 is classified:

`ZERO_SEMANTIC_TECH_GEAR`

Strict contribution: **+0**.

Technological gadget actions, equipment passives/procs, movement assistance, force-field presentation, drones, projectiles, armor/reactor support and Create machine operations remain outside the semantic-magic numerator.

## Clean-room boundary

The durable catalog retains identifiers, hashes, counts, high-level action classes and semantic classification. It does not redistribute the JAR, source implementation bodies, textures/models, or long localization text.
