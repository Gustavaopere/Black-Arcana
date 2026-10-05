# `traveloptics:psychic_bolt`

- Provider: **T.O Magic n' Extras** (`traveloptics`)
- Version line: `4.4.0.1-1.21.1`
- Exact publisher file: CurseForge `6342780`
- School: **Eldritch**
- Registry: `traveloptics:psychic_bolt`
- Registry field: `PSYCHIC_BOLT_SPELL`
- Concrete class: `PsychicBoltSpell`
- State: `EXACT REGISTRY / RUNTIME CONDITIONAL`

## Publisher semantic context — version-conditioned

multi-target bolts; confusion/retargeting.

This is **publisher context only** from the living project page; it does not prove exact-alpha or current-physical runtime behavior. See `../PUBLISHER-SEMANTIC-CONTEXT.md`.

## Exact alpha mechanics baseline — File `6342780` only

- Base mana: **50**
- Mana per level: **20**
- Base spell power input: **1**
- Spell power per level input: **1**
- Cast type: **INSTANT**
- Cast-time field: **0 ticks**
- Max level: **3**
- Minimum rarity: **EPIC**
- Default cooldown: **40 s**

These are direct constants from exact publisher File `6342780`; they are **not** projected to current physical SHA-1 `7b74816e...`. Spell-power inputs are not final damage formulas, and effective host config/multipliers remain separate. See `../EXACT-4.4.0.1-MECHANICS-BASELINE.md`.

## Exact alpha scalar accessors — File `6342780` only

- `getRecastCount(int, LivingEntity)`: **L1 5 / L2 5 / L3 5**

These are exact **raw accessor outputs** from File `6342780`. Audit #616 proved the `LivingEntity` parameter is not read by these exact methods before #617 evaluated them. Recast values are counts; range/radius values are not assigned a physical unit here. They are not projected to current physical SHA-1 `7b74816e...`. See `../EXACT-4.4.0.1-SCALAR-ACCESSORS.md` and `../EXACT-4.4.0.1-LIVINGENTITY-ACCESSORS.md`.

## Reachability

`HOST-DEFAULT CRAFTABLE / EFFECTIVE ELIGIBILITY CONDITIONAL`: exact File `6342780` class has no direct craftability mutator; current Iron's `1.21.1-3.16.3` host defaults `allowCrafting` to `true`. This closes only the host-default craftability gate. Effective Scroll Forge eligibility still depends on `isEnabled()`, effective `allow_crafting` configuration, a compatible focus/school path, and player-specific learning where applicable; unconditional survival acquisition is not established.

## Evidence boundary

Identity, school and the File-`6342780` default mechanics baseline above are exact-alpha evidence. Current-physical stats for SHA-1 `7b74816e...` remain unverified. Final damage formulas, range/radius/duration and PvP/boss rules remain `NÃO VERIFICADO` unless separately proven.

Iron's owns host casting/resource settlement; T.O Magic owns this spell. Provider stays **⚠️** because current-physical registry equality/provenance and full runtime closure are not proven.

Sources: `../EXACT-4.4.0.1-ARTIFACT-AUDIT.md`; `../EXACT-4.4.0.1-MECHANICS-BASELINE.md`; `../HOST-CRAFTABILITY-3.16.3-CHECKPOINT.md`.
