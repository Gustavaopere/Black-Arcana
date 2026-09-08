# Ars Hex 5.0.4b — Perks & Equipment

Status: `SOURCE CATALOG CLOSED / INSTALLED EQUIPMENT QA OPEN`

## Ars thread perks — 3/3 Malum-conditioned

`ArsNouveauRegistry.registerCompatPerks()` registers exactly three perks while Malum is loaded. Hexerei and Iron's perk placeholders are commented and are not production registrations.

### Soul Ward — `ars_hex:thread_soul_ward`

Direct provider attribute modifiers:

- Malum `SOUL_WARD_CAPACITY`: `+2 × slotValue`, `ADD_VALUE`;
- Malum `SOUL_WARD_INTEGRITY`: `+0.5 × slotValue`, `ADD_MULTIPLIED_BASE`.

### Magic Proficiency — `ars_hex:thread_magic_proficiency`

- Lodestone `MAGIC_PROFICIENCY`: `+0.1 × slotValue`, `ADD_MULTIPLIED_BASE`.

### Spirit Spoils — `ars_hex:thread_soul_spoils`

- Malum `SPIRIT_SPOILS`: `+slotValue`, `ADD_VALUE`.

These perks do not establish new Ars Hex resource ledgers. They project host-owned attributes through Ars thread infrastructure.

## Enchanter's Scythe

Active registration while Malum is loaded:

`ars_hex:enchanter_scythe`

Construction delegates to Malum `MagicScytheItem` with Netherite tier and source arguments `-4F`, `0F`, `3.0F`, stack size 1. Phase 2W does not reinterpret those Malum constructor parameters beyond the exact source call.

The class also implements:

- Ars `ICasterTool`;
- Ars `IManaDiscountEquipment`.

### Scribing contract

A scribed spell is accepted only if its recipe contains no `AbstractCastMethod`. When the spell is written, the provider prepends Ars `MethodTouch`.

This makes the scythe a host-owned spell-on-hit invocation surface rather than a new independent cast engine.

### On-hit cast path

On `hurtEnemy` the scythe:

1. obtains its Ars `SpellCaster`;
2. wraps the attacker as `PlayerCaster` or `LivingCaster`;
3. constructs an Ars `SpellContext` using the caster-modified spell;
4. constructs Ars `SpellResolver` / `EntitySpellResolver`;
5. invokes `resolver.onCastOnEntity(...)` against the struck target;
6. then delegates to Malum `super.hurtEnemy(...)`.

Black Arcana must not replay this on-hit cast or treat the child resolver as an independent BA cast.

### Necromancy mana discount

For every spell part where Ars `SpellSchools.NECROMANCY.isPartOfSchool(part)` is true, the provider adds:

`0.2 × part.getCastingCost()`

The final discount is `ceil(sum)`.

This is an Ars mana discount. It does not authorize a second BA mana resource or duplicate refund path.

### Repairing perk seam

`inventoryTick` invokes Ars `RepairingPerk.attemptRepair(stack, player)` for player-held/inventory scythes. The repair lifecycle remains Ars-owned.

## Malum scythe-boomerang / Reactive seam

`MalumCompat` listens to `LivingDamageEvent.Post`.

When the direct entity is Malum `ScytheBoomerangEntity`:

- if the boomerang item is `ICasterTool` and owner is a living entity, provider code invokes that item's `hurtEnemy` path;
- otherwise, if the source living entity and Reactive enchantment conditions are satisfied, it calls Ars `ReactiveEvents.castSpell`.

The event already has a provider-native exactly-once causal path that BA integrations must observe rather than replay.

## Light-manager bridge

In post-init, Malum entities are registered with Ars `LightManager`:

- Natural Spirit: 8;
- Etheric Nitrate: 15;
- Vivid Nitrate: 15.

This is a rendering/light interoperability seam, not a BA gameplay resource.

## Acquisition

All three perks and the scythe use Malum-conditioned source recipes documented in [`ACQUISITION.md`](ACQUISITION.md).
