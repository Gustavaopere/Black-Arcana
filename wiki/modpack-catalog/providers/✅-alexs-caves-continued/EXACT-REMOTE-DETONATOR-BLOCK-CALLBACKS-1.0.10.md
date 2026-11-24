# Remote Detonator — publisher Nuclear Bomb callback discovery 1.0.10

**Status:** static discovery only; `NOT_CERTIFIED`, `NO_MUTATION`, `WORLD_SAFETY_BLOCKED`, `physical_qa=NOT_TESTED`. No new cast or certification.

## First exact collection

[CI #45328173245](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45328173245), job 138222685414, HEAD `1cb68fccb32fc5278b1c35b80e30004bcbd0ba06`, artifact 14890363054. Five synthetic candidate checks passed. Publisher SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c32e9f2e95bffae0e7c`, 1,555 class paths inspected for candidate names. Report 100,794 bytes SHA-256 `ed238bb858c33dc610b53a87fd8408f8ada7e210a92fc05f12ea4324f6330300`. Reproduce using the read-only probe in docs/qa and its workflow. This first schema is historical evidence; the expanded schema requires its own CI and pin.

| Owner | Class SHA-256 |
|---|---|
| server/block/NuclearBombBlock | `5ae2d94f0b9f870eaa75fa53b6baaa539d9be9959c2cca86e3a203a986580f63` |
| server/entity/item/NuclearBombEntity | `36ccc6ce0993d0ff7884c50857a11f6edb7bace66c15c1b157e8013627b4f3d3` |
| server/entity/item/NuclearExplosionEntity | `d9c827a9acb2d0f9e7050252ed57e6a3d0a8ad49053e54f19a8eaeb6b84da912` |

All owners use prefix `com/github/alexmodguy/alexscaves/`.

## Static causal boundaries

- `ACBlockRegistry` links literal `nuclear_bomb` @2307, bootstrap 174 @2310 to factory `lambda$static$162`, registration request @2315 and field `NUCLEAR_BOMB` @2318. Factory creates NuclearBombBlock @0. This is a declaration, not executed registry bootstrap.
- `NuclearBombBlock.onCaughtFire(BlockState,Level,BlockPos,Direction,LivingEntity)V`: Code SHA `688e162008b1de1e854e9f5211ed20e5c538c63db6d9e955838b21abde90ad71`, 49 instructions. Client-side branch @4 skips body; on server requests `ACEntityRegistry.NUCLEAR_BOMB` @7 and `ACCompat.createEntity` @19, position @52 with X/Z 0.5 literals, insertion @58, sound TNT_PRIMED @90 (two float 1 operands), game event PRIME_FUSE @100. No conditional branch after insertion; acceptance not established. The direct callback does not itself call explosion or remove the block.
- `NuclearBombEntity.tick()V`: Code SHA `c822d2af9f7ce24f56741d25cba5195ca1f9ddb0bf4dfaf27b6e324902387035`, 126 instructions. Observed gravity literal -0.04, drag 0.98, ground movement scale (0.7,-0.7,0.7), siren scheduling operands 10 and 256. Reads time @127; increments by 1 and compares against 300 @137; above threshold calls discard @141, checks non-client and spawnedExplosion guard @158 before explode @162 and flag write @167. Otherwise writes time @175. Effective fuse duration, tick start, persistence and actual scheduling require accessor/initialization proof.
- `NuclearBombEntity.explode()V`: Code SHA `0ef24d0b4bf1004060e876974f40146da5d2b21e95586150a3e45702781ffb33`, 24 instructions. Requests NUCLEAR_EXPLOSION entity @0–15, copies position @24, reads common config `nukeExplosionSizeModifier` @31–40, calls setSize @43 and requests insertion @51. No branch in method; insertion success not established. No numeric size default inferred.
- Bomb entity's additional save/read declarations both have one instruction, zero typed member references, Code SHA `149488d869cbef080602a371ab0d39d97af103fb726aaeb02ccd36c06f494e5d`. This alone does not prove absence of inherited persistence or sync. No ownership guarantee.
- The initial registry probe found no direct constructor links in ACEntityRegistry because its search was limited to NEW factories and direct clinit handles. Nested bootstrap discovery is added for the next collection, not a claim of absent entity registration.

## Expanded collection — registry closure and synchronized state

[CI #45329311305](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45329311305), job 138226352097, HEAD `99d0a01dfb10beccd41b59f265644dfe4cfe9bd4`, artifact 14891635581; report 128,197 bytes SHA-256 `5b4ab93082e611bfd5a540e4ea33316fc2d472bec303561ae78bee33fc3f5635`. Five synthetic candidate cases passed. This replaces the initial projection, not its provenance.

- `ACEntityRegistry` class SHA `7d7c91ddbb534d7c0e86a590ef7d7c3154ec2a628153c31e9fc7318a4b29e072`: NUCLEAR_EXPLOSION registration literal @469, bootstrap 142 @472, field write @480. Supplier `lambda$static$26` contains constructor handle kind 8, bootstrap 89 @0 targeting NuclearExplosionEntity(EntityType,Level). NUCLEAR_BOMB literal @486, bootstrap 143 @489, field @497; supplier `lambda$static$27` contains constructor handle kind 8, bootstrap 88 @0 targeting NuclearBombEntity(EntityType,Level). Both builders declare MISC category and call sized, update interval, velocity and tracking configuration; literal builder values not projected here. Runtime registration remains unobserved.
- Bomb `defineSynchedData` defines TIME=0 @8; getTime reads TIME @7, setTime writes @11. Constructor (EntityType,Level) initializes spawnedExplosion=false @8. Starting from zero, uninterrupted successive invocations of the normal increment branch yield the transition at invocation 301, nominal 15.05 s at 20 TPS; scheduler, lag, unload/reload and transformed runtime remain unverified. Additional save/read methods are empty; do not infer persisted TIME from synced data.
- Explosion `defineSynchedData` declares SIZE=1F @8, NO_GRIEFING=false @20, INTENTIONAL_GAME_DESIGN=false @32. getSize and setSize use synced SIZE @7/@11; setSize has no own clamp or branch. Native bomb explode overwrites the default with the config value; default of config and effect formulas remain unaudited.
- Other block activation routes: `acUse` accepts flint and steel or fire charge, invokes onCaughtFire @46, sets AIR @59 (flags literal 11), and outside creative branches invokes hurtAndBreak @96 or shrink @105 with literal 1; stat award @118. `neighborChanged` checks signal @2 and calls onCaughtFire @14 then removeBlock @20. `onPlace` checks old block and neighbor signal, calls onCaughtFire @26 then removeBlock @32. `onProjectileHit` checks non-client, projectile fire and ACCompat.mayInteract @33 before onCaughtFire @62 and removeBlock @69. This permission call belongs to projectile ingress, not proof of equivalent validation in Remote Detonator.
- Explosion remove: non-client and loadingChunks guard, sets flag false then asks entity-owned loadChunksAround(false) @24 before base Entity.remove @29. This is not proof of cleanup of UUID-owned Remote Detonator tickets.

## Remaining scope

Verify ACCompat.createEntity, config default/effective values and sync persistence, actual downstream explosion processing, TNT vanilla branch, exact NeoForge engine delegation, world policy and claim safety. [Ticket lifecycle](EXACT-REMOTE-DETONATOR-TICKET-LIFECYCLE-1.0.10.md) remains a separate boundary. The [individual fiche](items/remote-detonator.md) remains partial; no counter changes, no physical acceptance.
