# `traveloptics:ignited_onslaught`

- Provider: **T.O Magic n' Extras** (`traveloptics`)
- Version line: `4.4.0.1-1.21.1`
- Exact publisher file: CurseForge `6342780`
- School: **Fire**
- Registry: `traveloptics:ignited_onslaught`
- Registry field: `IGNITED_ONSLAUGHT_SPELL`
- Concrete class: `IgnitedOnslaughtSpell`
- State: `EXACT REGISTRY / RUNTIME CONDITIONAL`

## Publisher semantic context — version-conditioned

Ignited Revenant/Berserker ally summon.

This is **publisher context only** from the living project page; it does not prove exact-alpha or current-physical runtime behavior. See `../PUBLISHER-SEMANTIC-CONTEXT.md`.

## Exact alpha mechanics baseline — File `6342780` only

- Base mana: **50**
- Mana per level: **75**
- Base spell power input: **1**
- Spell power per level input: **1**
- Cast type: **LONG**
- Cast-time field: **60 ticks**
- Max level: **5**
- Minimum rarity: **RARE**
- Default cooldown: **360 s**

These are direct constants from exact publisher File `6342780`; they are **not** projected to current physical SHA-1 `7b74816e...`. Spell-power inputs are not final damage formulas, and effective host config/multipliers remain separate. See `../EXACT-4.4.0.1-MECHANICS-BASELINE.md`.

## Exact alpha scalar accessors — File `6342780` only

- `getBerserkerHealth(int)`: **L1 33.0 / L2 41.0 / L3 49.0 / L4 57.0 / L5 65.0**
- `getRevenantHealth(int)`: **L1 40.0 / L2 50.0 / L3 60.0 / L4 70.0 / L5 80.0**

These are exact **raw accessor outputs** from File `6342780`. Count-named values are retained as counts. Health/motion-scale outputs are not converted into final entity health, physical units or final formulas. They are not projected to current physical SHA-1 `7b74816e...`. See `../EXACT-4.4.0.1-SCALAR-ACCESSORS.md`.

## Current-host summon-damage dependency

`getBerserkerDamage(int, LivingEntity)` and `getRevenantDamage(int, LivingEntity)` are exact File-`6342780` entity-reading accessors that depend on host `getSpellPower(int, Entity)` **and** Iron's `SUMMON_DAMAGE` attribute surface.

At the pinned current Iron's `1.21.1-3.16.3` source, `SUMMON_DAMAGE` is a syncable percentage-style attribute with registered base/default **1.0**. The Traveloptics accessor also checks/reads the entity attribute surface, so its final output remains live-entity/modifier/config dependent. No provider coefficient, branch outcome or final damage formula is inferred.

See `../EXACT-4.4.0.1-ALL-ENTITY-DEPENDENCY-MAP.md` and `../CURRENT-HOST-SUMMON-DAMAGE-CONTRACT.md`.

## Reachability

`UNIQUE / allowCrafting=false`; exact loot anchor: Ignited Berserker / Ignited Revenant loot.

## Evidence boundary

Identity, school and the File-`6342780` default mechanics baseline above are exact-alpha evidence. Current-physical stats for SHA-1 `7b74816e...` remain unverified. Final damage formulas, range/radius/duration and PvP/boss rules remain `NÃO VERIFICADO` unless separately proven.

Iron's owns host casting/resource settlement; T.O Magic owns this spell. Provider stays **⚠️** because current-physical registry equality/provenance and full runtime closure are not proven.

Sources: `../EXACT-4.4.0.1-ARTIFACT-AUDIT.md`; `../EXACT-4.4.0.1-MECHANICS-BASELINE.md`; `../EXACT-4.4.0.1-ALL-ENTITY-DEPENDENCY-MAP.md`; `../CURRENT-HOST-SUMMON-DAMAGE-CONTRACT.md`.
