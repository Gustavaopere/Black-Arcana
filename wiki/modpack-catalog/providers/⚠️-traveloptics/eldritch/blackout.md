# `traveloptics:blackout`

- Provider: **T.O Magic n' Extras** (`traveloptics`)
- Version line: `4.4.0.1-1.21.1`
- Exact publisher file: CurseForge `6342780`
- School: **Eldritch**
- Registry: `traveloptics:blackout`
- Registry field: `BLACKOUT_SPELL`
- Concrete class: `BlackoutSpell`
- State: `EXACT REGISTRY / RUNTIME CONDITIONAL`

## Publisher semantic context — version-conditioned

persistent anti-magic suppression field.

This is **publisher context only** from the living project page; it does not prove exact-alpha or current-physical runtime behavior. See `../PUBLISHER-SEMANTIC-CONTEXT.md`.

## Exact alpha mechanics baseline — File `6342780` only

- Base mana: **100**
- Mana per level: **50**
- Base spell power input: **1**
- Spell power per level input: **1**
- Cast type: **LONG**
- Cast-time field: **39 ticks**
- Max level: **3**
- Minimum rarity: **LEGENDARY**
- Default cooldown: **120 s**

These are direct constants from exact publisher File `6342780`; they are **not** projected to current physical SHA-1 `7b74816e...`. Spell-power inputs are not final damage formulas, and effective host config/multipliers remain separate. See `../EXACT-4.4.0.1-MECHANICS-BASELINE.md`.

## Exact alpha scalar accessors — File `6342780` only

- `getRadius(int)`: **L1 8.0 / L2 10.0 / L3 12.0**
- `getEffectDuration(int)`: **L1 30.0 / L2 30.0 / L3 30.0**
- `getAntiMagicZoneDuration(int)`: **L1 160.0 / L2 200.0 / L3 240.0**

These are exact **raw accessor outputs** from File `6342780`. Counts are counts; no unit is assigned to the other numeric values unless independently established. They are not projected to current physical SHA-1 `7b74816e...`. See `../EXACT-4.4.0.1-SCALAR-ACCESSORS.md`.

## Reachability

`UNIQUE / allowCrafting=false`; no direct exact acquisition anchor found — survival reachability `UNVERIFIED`.

## Evidence boundary

Identity, school and the File-`6342780` default mechanics baseline above are exact-alpha evidence. Current-physical stats for SHA-1 `7b74816e...` remain unverified. Final damage formulas, range/radius/duration and PvP/boss rules remain `NÃO VERIFICADO` unless separately proven.

Iron's owns host casting/resource settlement; T.O Magic owns this spell. Provider stays **⚠️** because current-physical registry equality/provenance and full runtime closure are not proven.

Sources: `../EXACT-4.4.0.1-ARTIFACT-AUDIT.md`; `../EXACT-4.4.0.1-MECHANICS-BASELINE.md`.
