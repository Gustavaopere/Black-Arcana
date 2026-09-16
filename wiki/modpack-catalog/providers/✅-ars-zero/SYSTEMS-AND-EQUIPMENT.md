# Ars Zero 2.0.2 — Systems, Equipment and World Surface

## Cast devices

### Spell Staff family

Official current documentation describes Creative/Archmage/Mage/Novice Spell Staff variants with three independent spell phases: Begin, Tick and End, each allowing up to ten glyph slots. Held use supports continuous spell execution.

The exact 2.0.2 release documents hardened multiphase clipboard/parchment handling: packets identify a hand or inventory slot and the server reconstructs/validates the actual device rather than trusting client-supplied item data.

### Psion's Circlet

Tier-3 Curios head equipment using Begin/Tick/End phases and a channel input. Exact 2.0.2 notes confirm invalid destination handling was fixed so malformed packet destinations cannot delete/drop/overwrite the wrong circlet/staff stack.

### Multi-phase Turret

Provider block/turret that executes phase-aware spells. The 2.0.x release line also documents independent phase progress and stale-context cleanup. Black Arcana must not treat automated turret throughput as a BA player cast without a real causal contract.

## Static staff surface

### Direct exact-2.0.2 names

The exact NeoForge 1.21.1 2.0.2 release directly names five production staffs:

1. Staff of Demonbane;
2. Staff of Geometrize;
3. Staff of Convergence / Explosion Arch Wizard;
4. Staff of Lakes;
5. Staff of Switcheroo.

The exact release makes those five Necropolis Lich-exclusive drops with no crafting recipes and adds their production item/preset/presentation/acquisition integration.

### Earlier 2.0.x lineage evidence

Earlier official release material additionally documents:

- Staff of Telekinesis;
- Staff of Aetherwalk.

Those two names are retained as lineage-supported capability evidence, but are not mislabeled as directly re-enumerated by the exact 2.0.2 file page. Exact 2.0.2 item registry IDs/presets/components remain fail-closed until binary/source inspection.

## Conjure Arcane Shield

The exact 2.0.2 release explicitly fixes Arcane Shield projectile ownership, durability enforcement, split limits and surrounding-shield collision behavior, which confirms the mechanic is active in 2.0.2. Older official 2.0.x cross-version release notes describe a stationary spherical barrier with projectile/melee absorption, durability/lifespan and augment interactions; those detailed semantics are retained only as lineage corroboration, not exact 2.0.2 numeric/API authority.

For Black Arcana this is an external barrier capability. Do not mirror shield durability or collision state in a BA-owned ledger absent a verified adapter.

## Voxels

Official current docs define Conjure Voxel variants:

- Arcane — default spell-resolving voxel;
- Fire — fire-world/entity interactions, water/rain vulnerability;
- Water — water-world interactions and collection, heat vulnerability;
- Wind — floating/push behavior and fire reactions;
- Stone — fragile-block breaking and impact damage;
- Ice — water freezing and fragile-block breaking;
- Lightning — living-entity discharge/damage.

Voxel collisions can produce elemental cancellation/combination behavior, and elemental power affects environmental resistance. Exact 2.0.2 fixes cover collision tunnelling, thin blocks, items, fluids, starting-inside hits and Wind voxel fire interactions.

These voxels are provider-owned entities/effects. Black Arcana should consume only a verified observable boundary if one is later required; it must not reproduce the lifecycle from visual similarity.

## World/encounter surface

### Blight

- Conjure Blight places a damaging liquid that withers/destroys living vegetation according to official docs.
- Exact 2.0.2 adds claim and world-bound checks to placement through AOE.
- Blight Forest distribution is configurable; exact 2.0.2 sets the default TerraBlender weight to 10 and makes the configured value affect overworld distribution.

Blight is not Black Arcana Corruption.

### Necropolis / Lich

Exact 2.0.2 notes cover Necropolis structure placement/configuration, Lich static-staff equipment and loot, and removal of an orphaned entrance structure-set entry. Treat this as provider encounter/worldgen authority, not a BA ritual or progression gate.

### Temporal Anchor / geometry process

Exact 2.0.2 hardening scopes Temporal Anchor state by dimension and caster, applies claim checks to affected blocks and prevents stale/duplicate falling-block restoration. Geometry move/cancel packets are restricted to unfinished geometry processes owned by the sending player.

Black Arcana integration must preserve those server ownership and protection boundaries. No client-supplied geometry authority is acceptable.

## Provider QA evidence

The exact release notes state that 22 bypassed GameTests were re-enabled and that all 69 release regression tests execute and pass. This is **upstream provider release evidence**, not Black Arcana's own real-modpack acceptance and not proof that the user's full modpack interop is green.
