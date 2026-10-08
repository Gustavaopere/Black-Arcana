# `traveloptics:mechanized_predator`

- Provider: **T.O Magic n' Extras** (`traveloptics`)
- Version line: `4.4.0.1-1.21.1`
- Exact publisher file: CurseForge `6342780`
- School: **Lightning**
- Registry: `traveloptics:mechanized_predator`
- Registry field: `MECHANIZED_PREDATORS_SPELL`
- Concrete class: `MechanizedPredatorSpell`
- State: `EXACT REGISTRY / RUNTIME CONDITIONAL`

## Publisher semantic context — version-conditioned

Watcher/Prowler ally deployment.

This is **publisher context only** from the living project page; it does not prove exact-alpha or current-physical runtime behavior. See `../PUBLISHER-SEMANTIC-CONTEXT.md`.

## Exact alpha mechanics baseline — File `6342780` only

- Base mana: **100**
- Mana per level: **100**
- Base spell power input: **1**
- Spell power per level input: **1**
- Cast type: **LONG**
- Cast-time field: **80 ticks**
- Max level: **5**
- Minimum rarity: **RARE**
- Default cooldown: **540 s**

These are direct constants from exact publisher File `6342780`; they are **not** projected to current physical SHA-1 `7b74816e...`. Spell-power inputs are not final damage formulas, and effective host config/multipliers remain separate. See `../EXACT-4.4.0.1-MECHANICS-BASELINE.md`.

## Exact alpha scalar accessors — File `6342780` only

- `getWatcherCount(int)`: **L1 1.0 / L2 2.0 / L3 3.0 / L4 4.0 / L5 5.0**

These are exact **raw accessor outputs** from File `6342780`. Counts are counts; no unit is assigned to the other numeric values unless independently established. They are not projected to current physical SHA-1 `7b74816e...`. See `../EXACT-4.4.0.1-SCALAR-ACCESSORS.md`.
- `getWatcherHealth(int)`: **L1 5.0 / L2 10.0 / L3 15.0 / L4 20.0 / L5 25.0**
- `getProwlerHealth(int)`: **L1 80.0 / L2 100.0 / L3 120.0 / L4 140.0 / L5 160.0**

## Exact alpha entity-dependent accessor contracts — File `6342780` only

- `getWatcherDamage(int, LivingEntity)` — **Family B / host spell power + Iron's `SUMMON_DAMAGE`**; entity local-slot loads: **3**. The bounded audit also observes `LivingEntity.getAttributes()`, `AttributeMap.hasAttribute(...)`, `LivingEntity.getAttributeValue(...)`, `AttributeRegistry.SUMMON_DAMAGE` and exactly one branch.
- `getProwlerDamage(int, LivingEntity)` — **Family B / host spell power + Iron's `SUMMON_DAMAGE`**; entity local-slot loads: **3**. The bounded audit also observes `LivingEntity.getAttributes()`, `AttributeMap.hasAttribute(...)`, `LivingEntity.getAttributeValue(...)`, `AttributeRegistry.SUMMON_DAMAGE` and exactly one branch.

These are **dependency contracts**, not reconstructed formulas or entity-independent numeric results. Each listed method calls Iron's `getSpellPower(int, Entity)` and additionally depends on the host `SUMMON_DAMAGE` attribute surface. Under the pinned current Iron's `1.21.1-3.16.3` host contract, spell power depends on the spell's base/per-level power inputs plus the caster's global `SPELL_POWER`, current-school power and effective `POWER_MULTIPLIER`. The audit does not infer the branch semantics or numeric coefficient for `SUMMON_DAMAGE`.

No result in this section is projected to current physical Traveloptics SHA-1 `7b74816e...`. See `../EXACT-4.4.0.1-ALL-ENTITY-DEPENDENCY-MAP.md`.

## Reachability

`UNIQUE / allowCrafting=false`; exact loot anchor: Prowler / Watcher loot.

## Evidence boundary

Identity, school and the File-`6342780` default mechanics baseline above are exact-alpha evidence. Current-physical stats for SHA-1 `7b74816e...` remain unverified. Final damage formulas, range/radius/duration and PvP/boss rules remain `NÃO VERIFICADO` unless separately proven.

Iron's owns host casting/resource settlement; T.O Magic owns this spell. Provider stays **⚠️** because current-physical registry equality/provenance and full runtime closure are not proven.

Sources: `../EXACT-4.4.0.1-ARTIFACT-AUDIT.md`; `../EXACT-4.4.0.1-MECHANICS-BASELINE.md`.
