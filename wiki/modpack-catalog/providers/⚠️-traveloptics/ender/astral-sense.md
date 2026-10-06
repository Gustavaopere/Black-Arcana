# `traveloptics:astral_sense`

- Provider: **T.O Magic n' Extras** (`traveloptics`)
- Version line: `4.4.0.1-1.21.1`
- Exact publisher file: CurseForge `6342780`
- School: **Ender**
- Registry: `traveloptics:astral_sense`
- Registry field: `ASTRAL_SENSE_SPELL`
- Concrete class: `AstralSenseSpell`
- State: `EXACT REGISTRY / RUNTIME CONDITIONAL`

## Publisher semantic context — version-conditioned

threat/path sensing; crouch loot/trap sensing.

This is **publisher context only** from the living project page; it does not prove exact-alpha or current-physical runtime behavior. See `../PUBLISHER-SEMANTIC-CONTEXT.md`.

## Exact alpha mechanics baseline — File `6342780` only

- Base mana: **100**
- Mana per level: **50**
- Base spell power input: **1**
- Spell power per level input: **1**
- Cast type: **INSTANT**
- Cast-time field: **0 ticks**
- Max level: **3**
- Minimum rarity: **RARE**
- Default cooldown: **120 s**

These are direct constants from exact publisher File `6342780`; they are **not** projected to current physical SHA-1 `7b74816e...`. Spell-power inputs are not final damage formulas, and effective host config/multipliers remain separate. See `../EXACT-4.4.0.1-MECHANICS-BASELINE.md`.

## Exact alpha scalar accessors — File `6342780` only

- `getRadius(int)`: **L1 25.0 / L2 30.0 / L3 35.0**

These are exact **raw accessor outputs** from File `6342780`. Counts are counts; no unit is assigned to the other numeric values unless independently established. They are not projected to current physical SHA-1 `7b74816e...`. See `../EXACT-4.4.0.1-SCALAR-ACCESSORS.md`.

## Exact alpha entity-dependent accessor contracts — File `6342780` only

- `getDuration(int, LivingEntity)` — **Family A / host spell-power only**; entity local-slot loads: **1**; retained arithmetic classification: `f2i ×1; fadd ×1; fmul ×1`. The bounded audit found no field refs, branches or additional entity-member calls.

This is a **dependency contract**, not a reconstructed formula or entity-independent numeric result. The method calls Iron's `getSpellPower(int, Entity)`. Under the pinned current Iron's `1.21.1-3.16.3` host contract, that host value depends on the spell's base/per-level power inputs plus the caster's global `SPELL_POWER`, current-school power and effective `POWER_MULTIPLIER`.

No result in this section is projected to current physical Traveloptics SHA-1 `7b74816e...`. See `../EXACT-4.4.0.1-ALL-ENTITY-DEPENDENCY-MAP.md`.

## Reachability

`HOST/PUBLISHER-DEFAULT CRAFTABLE + ENABLED / EFFECTIVE ELIGIBILITY CONDITIONAL`: exact File `6342780` class has no direct craftability or enabled-default mutator and no concrete `isEnabled()` / `canBeCraftedBy(Player)` override; current Iron's `1.21.1-3.16.3` defaults both `allowCrafting` and `enabled` to `true`. Effective Scroll Forge eligibility still depends on active server/datapack/global config, a compatible focus/school path, and player-specific learning where applicable; unconditional survival acquisition is not established. See `../HOST-ENABLED-3.16.3-CHECKPOINT.md`.

## Evidence boundary

Identity, school and the File-`6342780` default mechanics baseline above are exact-alpha evidence. Current-physical stats for SHA-1 `7b74816e...` remain unverified. Final damage formulas, range/radius/duration and PvP/boss rules remain `NÃO VERIFICADO` unless separately proven.

Iron's owns host casting/resource settlement; T.O Magic owns this spell. Provider stays **⚠️** because current-physical registry equality/provenance and full runtime closure are not proven.

Sources: `../EXACT-4.4.0.1-ARTIFACT-AUDIT.md`; `../EXACT-4.4.0.1-MECHANICS-BASELINE.md`; `../HOST-CRAFTABILITY-3.16.3-CHECKPOINT.md`.
