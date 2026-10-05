# `traveloptics:spectral_blink`

- Provider: **T.O Magic n' Extras** (`traveloptics`)
- Version line: `4.4.0.1-1.21.1`
- Exact publisher file: CurseForge `6342780`
- School: **Eldritch**
- Registry: `traveloptics:spectral_blink`
- Registry field: `SPECTRAL_BLINK`
- Concrete class: `SpectralBlinkSpell`
- State: `EXACT REGISTRY / RUNTIME CONDITIONAL`

## Publisher semantic context — version-conditioned

look-target teleport; nearby-entity reveal.

This is **publisher context only** from the living project page; it does not prove exact-alpha or current-physical runtime behavior. See `../PUBLISHER-SEMANTIC-CONTEXT.md`.

## Publisher quantitative / conditional note — version-conditioned

Activation/teleport decision window: **3 seconds** on the current official project page.

This is **publisher-only context**, not exact-alpha/current-physical proof. The corresponding runtime value or rule remains unverified for File `6342780` and SHA-1 `7b74816e...` unless independently proven.

## Exact alpha mechanics baseline — File `6342780` only

- Base mana: **10**
- Mana per level: **20**
- Base spell power input: **1**
- Spell power per level input: **1**
- Cast type: **INSTANT**
- Cast-time field: **0 ticks**
- Max level: **3**
- Minimum rarity: **RARE**
- Default cooldown: **25 s**

These are direct constants from exact publisher File `6342780`; they are **not** projected to current physical SHA-1 `7b74816e...`. Spell-power inputs are not final damage formulas, and effective host config/multipliers remain separate. See `../EXACT-4.4.0.1-MECHANICS-BASELINE.md`.

## Exact-alpha entity-power dependency — File `6342780`

- selected numeric accessor: `getEffectLevel(int, LivingEntity)`;
- LivingEntity slot reads: **1**;
- provider field references: **none**;
- branches: **0**;
- only retained member dependency: host `getSpellPower(int, Entity)`;
- retained arithmetic classification: `fmul ×1; f2i ×1; iadd ×1`.

Current Iron's `1.21.1-3.16.3` resolves `getSpellPower` from the spell's base/per-level power plus entity Spell Power, school power and effective `POWER_MULTIPLIER`. This exact Traveloptics spell uses File-`6342780` spell-power inputs `1 / 1`.

The provider-side formula is deliberately **not reconstructed**. This accessor remains entity/config dependent and no entity-independent numeric result is assigned. See `../EXACT-4.4.0.1-ENTITY-POWER-DEPENDENCY-CHECKPOINT.md`.

## Reachability

`HOST/PUBLISHER-DEFAULT CRAFTABLE + ENABLED / EFFECTIVE ELIGIBILITY CONDITIONAL`: exact File `6342780` class has no direct craftability or enabled-default mutator and no concrete `isEnabled()` / `canBeCraftedBy(Player)` override; current Iron's `1.21.1-3.16.3` defaults both `allowCrafting` and `enabled` to `true`. Effective Scroll Forge eligibility still depends on active server/datapack/global config, a compatible focus/school path, and player-specific learning where applicable; unconditional survival acquisition is not established. See `../HOST-ENABLED-3.16.3-CHECKPOINT.md`.

## Evidence boundary

Identity, school and the File-`6342780` default mechanics baseline above are exact-alpha evidence. Current-physical stats for SHA-1 `7b74816e...` remain unverified. Final damage formulas, range/radius/duration and PvP/boss rules remain `NÃO VERIFICADO` unless separately proven.

Iron's owns host casting/resource settlement; T.O Magic owns this spell. Provider stays **⚠️** because current-physical registry equality/provenance and full runtime closure are not proven.

Sources: `../EXACT-4.4.0.1-ARTIFACT-AUDIT.md`; `../EXACT-4.4.0.1-MECHANICS-BASELINE.md`; `../HOST-CRAFTABILITY-3.16.3-CHECKPOINT.md`.
