# Remote Detonator — corroboration of the existing nuclear effect contract (1.0.10)

**Scope:** consumer evidence, not a new semantic root, object certificate or runtime integration. `NO_MUTATION`, `WORLD_SAFETY_BLOCKED`, `physical_qa=NOT_TESTED`. The canonical [nuclear contracts](EXACT-NUCLEAR-CONTRACTS-1.0.10.md), [Nuke](damage-types/nuke.md), [Intentional Game Design](damage-types/intentional-game-design.md) and [Irradiated](effects/irradiated.md) already certify their own static scopes. Reuse those proofs, not their certificate status, for Remote Detonator. No changes to these sealed files.

## Reproduction and provenance

Publisher 1.0.10, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c32e9f2e95bffae0e7c`; NuclearExplosionEntity SHA-256 `d9c827a9acb2d0f9e7050252ed57e6a3d0a8ad49053e54f19a8eaeb6b84da912`. [Run 45332141161](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45332141161), job 138235568708, HEAD `8f0c6bde39036d5d1e6b569979d4a19be1e38311`, artifact 14891907844, five synthetic cases passed; 20 executable bodies, report 206,285 bytes SHA-256 `9bb19b18b085cec164ebea4f4f23735f1560e3deda766b3df8194cb1ddc6bd2e`. [Probe](../../../../docs/qa/alexscaves_1010_nuclear_explosion_effect_probe.py), [workflow](../../../../.github/workflows/alexscaves-1010-nuclear-explosion-effects.yml). General CI of that HEAD failed before Java tests due to Maven Central HTTP 429 resolving Gson 2.10.1; fresh final-head CI required.

The new collection corroborates the existing exact numerical and target/world manifests; no new full disassembly or independent certificate is needed. The report pins the observed bounded projection rather than a copy of implementation. In particular, the input-order and local-slot interpretations below derive from the existing certified Nuke dossier, cross-checked against the current arithmetic and callsite evidence.

## Consumer parameter cross-reference

| Parameter | Canonical interpretation and current proof |
|---|---|
| Size s | getSize() synced accessor. Native bomb passes config double converted to float; default 3D is a declaration, not effective runtime. |
| AOE | c=(int)ceil(s), B=15*c; inflate existing body AABB by (1.5B,0.6B,1.5B). Damage radius operand r=1.5B+1. tick @389/@466. |
| Damage | D=((r-d)/r)*M(s), M=100 if s<=1.5, else 100+400*(s-1.5). calculateDamage(FF)F SHA `38f53b2135a6f607c93226399c19b64f00e3d238def92d64add22d9510d4988f`. d=LivingEntity.distanceTo. No clamp in helper. |
| Targeting | LivingEntity query @421. Player movement coefficient halved; Raycat zero damage; RESISTS_RADIATION damage x0.25 and movement coefficient x0.1; Tremorzilla special zero within resistance branch. No own LOS/owner/team or explicit server guard surrounding the entity loop. |
| Settlement | Select one DamageSource @605/@618, hurt @623 if positive, return discarded. Movement write @643 and Irradiated @698 not conditioned on hurt acceptance. No player Entity passed to damage factories. |
| Status | 48000 ticks, amplifier 1 if s<=1.5, else 2, if later intentional flag false. See Irradiated certificate for tick and heal consumers. |
| Lifecycle | tick Code SHA `66c083bcb10ea2df151c20fe1faf1cc7d760fc077a1000332ea63cca436f8f3b`; removal when tickCount>40 and queue empty, not fixed lifetime. Own save/read only WasLoadingChunks. |
| World | removeChunk(I)V SHA `323b5bd7a77445c4aeeb14075644a8523f414755f4e1c7e66bd9541e45bb9402`; 16x16x16 candidate lattice per queue origin; maximum three queue entries per processing tick. Nonpositive max resistance returns after pop; tag/resistance and egg exception; own callbacks for drops, onBlockExploded and fire. See canonical Nuke §5 for non-spherical noise geometry and exact probability formula. |

At default s=3, conditional arithmetic gives c=3, B=45, AABB inflation (67.5,27,67.5), r=68.5, M=700, not a guaranteed damage value. Different sizes and distance alter these values; the selector box is not a sphere. Neither the provider config max nor the arithmetic gives a safe operational cap. No mutation or gameplay promise.

## Config declaration corroboration

ACServerConfig class SHA `67abf51943537e735a08c268607ca08901c2b197f0b278fa4b464887d40ea129`. Constructor field writes @617 (nuke_max_block_explosion_resistance: default 1000, [0,2147483647]), @638 (nuke_spawn_item_drops: true), @665 (nuclear_explosion_size_modifier: 3D, [0,Double.MAX_VALUE]). Current collection matches canonical Nuke §5.

## Causal boundary and open safety requirements

Nuke certificate already identifies four native producers: SackOfSatingItem, NuclearBombEntity, NucleeperEntity and NuclearFurnaceBlockEntity. Do not globally modify this shared consumer for Remote Detonator perks. [Existing exact ticket proof](EXACT-NEOFORGE-TICKETS-21.1.248.json) confirms the explosion's true,true acquisition vs false,false removal category mismatch on selected static branches; actual persistent leak is NOT_OBSERVED. This is distinct from the player's UUID tickets of RemoteDetonatorItem (different owner and no own false call found). [Engine bridge](EXACT-REMOTE-DETONATOR-ENGINE-21.1.248.md) corroborates owner and category selection. The physical NT-01…NT-07 plan remains unexecuted. Cross-dimensional world-write, effective tags/config, TNT downstream, world protection and actual admission remain open. No new casts or counts. Remote Detonator remains partial.
