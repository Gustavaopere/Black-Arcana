# `traveloptics:ashen_breath`

- Provider: **T.O Magic n' Extras** (`traveloptics`)
- Version line: `4.4.0.1-1.21.1`
- Exact publisher file: CurseForge `6342780`
- School: **Evocation**
- Registry: `traveloptics:ashen_breath`
- Registry field: `ASHEN_BREATH_SPELL`
- Concrete class: `AshenBreathSpell`
- State: `EXACT REGISTRY / RUNTIME CONDITIONAL`

## Publisher semantic context — version-conditioned

damaging, blinding ash cloud.

This is **publisher context only** from the living project page; it does not prove exact-alpha or current-physical runtime behavior. See `../PUBLISHER-SEMANTIC-CONTEXT.md`.

## Exact alpha mechanics baseline — File `6342780` only

- Base mana: **5**
- Mana per level: **2**
- Base spell power input: **1**
- Spell power per level input: **1**
- Cast type: **CONTINUOUS**
- Cast-time field: **100 ticks**
- Max level: **10**
- Minimum rarity: **COMMON**
- Default cooldown: **15 s**

These are direct constants from exact publisher File `6342780`; they are **not** projected to current physical SHA-1 `7b74816e...`. Spell-power inputs are not final damage formulas, and effective host config/multipliers remain separate. See `../EXACT-4.4.0.1-MECHANICS-BASELINE.md`.

## Exact-alpha entity-power dependency — File `6342780`

- selected numeric accessor: `getDamage(int, LivingEntity)`;
- LivingEntity slot reads: **1**;
- provider field references: **none**;
- branches: **0**;
- only retained member dependency: host `getSpellPower(int, Entity)`;
- retained arithmetic classification: none.

Current Iron's `1.21.1-3.16.3` resolves `getSpellPower` from the spell's base/per-level power plus entity Spell Power, school power and effective `POWER_MULTIPLIER`. This exact Traveloptics spell uses File-`6342780` spell-power inputs `1 / 1`.

The provider-side formula is deliberately **not reconstructed**. This accessor remains entity/config dependent and no entity-independent numeric result is assigned. See `../EXACT-4.4.0.1-ENTITY-POWER-DEPENDENCY-CHECKPOINT.md`.

## Reachability

`HOST/PUBLISHER-DEFAULT CRAFTABLE + ENABLED / EFFECTIVE ELIGIBILITY CONDITIONAL`: exact File `6342780` class has no direct craftability or enabled-default mutator and no concrete `isEnabled()` / `canBeCraftedBy(Player)` override; current Iron's `1.21.1-3.16.3` defaults both `allowCrafting` and `enabled` to `true`. Effective Scroll Forge eligibility still depends on active server/datapack/global config, a compatible focus/school path, and player-specific learning where applicable; unconditional survival acquisition is not established. See `../HOST-ENABLED-3.16.3-CHECKPOINT.md`.

## Evidence boundary

Identity, school and the File-`6342780` default mechanics baseline above are exact-alpha evidence. Current-physical stats for SHA-1 `7b74816e...` remain unverified. Final damage formulas, range/radius/duration and PvP/boss rules remain `NÃO VERIFICADO` unless separately proven.

Iron's owns host casting/resource settlement; T.O Magic owns this spell. Provider stays **⚠️** because current-physical registry equality/provenance and full runtime closure are not proven.

Sources: `../EXACT-4.4.0.1-ARTIFACT-AUDIT.md`; `../EXACT-4.4.0.1-MECHANICS-BASELINE.md`; `../HOST-CRAFTABILITY-3.16.3-CHECKPOINT.md`.
