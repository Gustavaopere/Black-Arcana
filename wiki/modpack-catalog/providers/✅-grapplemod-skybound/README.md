# Grappling Hook Mod: Skybound — 1.1+1.21.1.neoforge

Status: `✅ CATALOGED / EXACT PHYSICAL=PUBLISHER ARTIFACT / ZERO_SEMANTIC_TRAVERSAL_PHYSICS / +0 STRICT / RUNTIME QA SEPARATE`

## Current physical identity

- JAR: `grapplemod-1.1+1.21.1.neoforge.jar`;
- mod id: `grapplemod`;
- runtime: `1.1+1.21.1.neoforge`;
- Minecraft / loader: 1.21.1 / NeoForge;
- physical SHA-1: `2b6060de273f721857d715db9a811ddaa5422683`;
- physical sibling row: #308.

The current sibling dossier classifies Skybound as QoL/exploration/player-transport. It owns grappling-hook rope/tension physics, movement settlement and upgrades. It is cross-domain relevant only because several upgrades have names such as Ender, Forcefield and Rocket that could otherwise be mistaken for magic actions.

## Exact artifact closure

NON-MERGE evidence PR **#524** audits CurseForge project/file `1559979 / 8176552` and hard-gates the publisher artifact against the physical pack fingerprint.

- audit HEAD: `ed430c222aa3a13ad4b1dcbece7e2c2977bdf40a`;
- exact-artifact run: `36967140184` — **SUCCESS**;
- evidence artifact: `11210168195`;
- artifact digest: `sha256:b11c803c5f79c0e57334cf06cc710e7c4e83f027f790e51d51c56c4cf04eac53`;
- publisher SHA-1: `2b6060de273f721857d715db9a811ddaa5422683`;
- publisher SHA-256: `6e973cff926db4b70cf36b745933ebdc1469e2c02eefd245f9c2fe3bf2eb1248`;
- bytes: `847,238`.

The publisher SHA-1 exactly equals the current physical SHA-1.

See [`EXACT-1.1-ARTIFACT-AUDIT.md`](EXACT-1.1-ARTIFACT-AUDIT.md).

## Semantic conclusion

Skybound contributes **0 independent semantic magic objects** under the Black Arcana catalog metric.

The exact JAR exposes traversal/physics equipment and hook customization, not a provider-owned spell/ritual/glyph/ability roster:

- Grappling Hook / rope / hook attachment — traversal physics;
- motor — hook movement behavior;
- rocket — propulsion/movement controller;
- magnet — hook/attachment behavior;
- dual hook — hook configuration;
- forcefield — movement/repulsion physics controller;
- Ender Staff / Ender launch — directional launch/impulse mechanics, not teleportation;
- Long Fall Boots — passive traversal/fall equipment.

The exact `EnderStaffItem.use(...)` delegates to `GrappleModClient.launchPlayer(...)`. The exact launch path checks its cooldown/held owner, creates the provider air-friction physics controller, derives a look-vector, scales it by `getEnderStaffStrength()` and settles an Ender-launch movement vector. No teleport destination, dimension transfer, portal, spell registry or ritual settlement is established by that action.

`ForcefieldItem.use(...)` toggles the provider `FORCEFIELD` physics controller. Rocket, motor, magnet and rope behavior remain the same provider-owned traversal-physics family. The names alone do not make them semantic magic objects.

Detailed classification: [`SEMANTIC-SURFACE-DISPOSITION.md`](SEMANTIC-SURFACE-DISPOSITION.md).

## Provider data / acquisition

The exact artifact packages ordinary crafting/smithing routes for the grappling hook and its upgrades, including Ender Staff, Forcefield, Rocket and hook-upgrade recipes. Those recipes establish equipment reachability but do not convert the traversal mechanics into magic identities.

## Nested compatibility modules

The physical artifact contains two nested JarJar modules:

- Create compatibility;
- Sable compatibility.

They adapt hook/attachment coordinates to external moving structures/sublevels and remain part of the host provider. They do not create standalone top-level magic providers or semantic actions.

## Authority boundary

Skybound remains authority for hook/rope state, physics controllers, attachment, movement settlement and upgrade behavior. Create/Sable remain authorities for their transforms/sublevels. Black Arcana only records the semantic classification and must not replay movement, teleport/launch, hook attachment or resource/equipment effects.

## Runtime QA remains separate

Catalog closure does not claim assembled-pack runtime PASS. Multiplayer rope state, relog, chunk lifecycle, Create/Sable moving structures, ParCool/other movement-mod coexistence and exact once-only input settlement remain runtime QA.

## Result

**✅ Cataloged — `ZERO_SEMANTIC_TRAVERSAL_PHYSICS`.**

Strict semantic delta: **+0**.
