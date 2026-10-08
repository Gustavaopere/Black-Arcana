# `traveloptics:aerial_collapse`

**Current physical inventory (2026-10-08):** this is one of **33/33 identities** directly registered in the SHA-1 `7b74816e...` JAR. Catalog **✅**; publisher-File-only mechanics and actual deployed runtime/survival remain version-conditioned or ⚠️. See `../PHYSICAL-JAR-DIRECT-AUDIT-2026-10-08.md`.

- Provider: **T.O Magic n' Extras** (`traveloptics`)
- Version line: `4.4.0.1-1.21.1`
- Exact publisher file: CurseForge `6342780`
- School: **Nature**
- Registry: `traveloptics:aerial_collapse`
- Registry field: `AERIAL_COLLAPSE_SPELL`
- Concrete class: `AerialCollapseSpell`
- State: `✅ CURRENT PHYSICAL ID CATALOGED / ⚠️ RUNTIME QA OPEN`

## Publisher semantic context — version-conditioned

lift then slam; health-percentage damage.

This is **publisher context only** from the living project page; it does not prove exact-alpha or current-physical runtime behavior. See `../PUBLISHER-SEMANTIC-CONTEXT.md`.

## Publisher quantitative / conditional note — version-conditioned

Lift timing: **2.5 seconds** before the slam. The same current page describes the slam as percentage-health damage that ignores damage caps.

This is **publisher-only context**, not exact-alpha/current-physical proof. The corresponding runtime value or rule remains unverified for File `6342780` and SHA-1 `7b74816e...` unless independently proven.

## Exact alpha mechanics baseline — File `6342780` only

- Base mana: **60**
- Mana per level: **60**
- Base spell power input: **1**
- Spell power per level input: **1**
- Cast type: **LONG**
- Cast-time field: **10 ticks**
- Max level: **5**
- Minimum rarity: **UNCOMMON**
- Default cooldown: **45 s**

These are direct constants from exact publisher File `6342780`; they are **not** projected to current physical SHA-1 `7b74816e...`. Spell-power inputs are not final damage formulas, and effective host config/multipliers remain separate. See `../EXACT-4.4.0.1-MECHANICS-BASELINE.md`.

## Exact alpha scalar accessors — File `6342780` only

- `getRadius(int, LivingEntity)`: **L1 4.0 / L2 6.0 / L3 8.0 / L4 10.0 / L5 12.0**

These are exact **raw accessor outputs** from File `6342780`. Audit #616 proved the `LivingEntity` parameter is not read by these exact methods before #617 evaluated them. Recast values are counts; range/radius values are not assigned a physical unit here. They are not projected to current physical SHA-1 `7b74816e...`. See `../EXACT-4.4.0.1-SCALAR-ACCESSORS.md` and `../EXACT-4.4.0.1-LIVINGENTITY-ACCESSORS.md`.

## Exact-alpha + current-host effective cast-time bridge

- exact File `6342780` relation: `getEffectiveCastTime(int, LivingEntity)` is a **direct delegate** to `getCastTime(level)`;
- current Iron's `1.21.1-3.16.3` host contract: non-`INSTANT` `getCastTime(level)` returns the spell's raw `castTime` field;
- this spell is exact-alpha `LONG` with raw `castTime = 10` ticks;
- bridged result for File `6342780` running under current Iron's 3.16.3: **10 ticks**.

This is **not** counted as a File-6342780-alone scalar result and is **not** projected to current physical Traveloptics SHA-1 `7b74816e...`. See `../EXACT-4.4.0.1-CURRENT-HOST-EFFECTIVE-CAST-BRIDGE.md`.

## Exact alpha entity-dependent accessor contracts — File `6342780` only

- `getDamage(int, LivingEntity)` — **Family C / host spell power + bounded `Math.min(float,float)`**; entity local-slot loads: **1**; retained arithmetic classification: `fadd ×1; fmul ×1`; no field refs or branch were retained.

This is a **dependency contract**, not a reconstructed formula or entity-independent numeric result. The method calls Iron's `getSpellPower(int, Entity)` and contains one `Math.min(float,float)` call. Under the pinned current Iron's `1.21.1-3.16.3` host contract, spell power depends on the spell's base/per-level power inputs plus the caster's global `SPELL_POWER`, current-school power and effective `POWER_MULTIPLIER`. The operands and threshold of `Math.min` are not inferred.

No result in this section is projected to current physical Traveloptics SHA-1 `7b74816e...`. See `../EXACT-4.4.0.1-ALL-ENTITY-DEPENDENCY-MAP.md`.

## Reachability

`HOST/PUBLISHER-DEFAULT CRAFTABLE + ENABLED / EFFECTIVE ELIGIBILITY CONDITIONAL`: exact File `6342780` class has no direct craftability or enabled-default mutator and no concrete `isEnabled()` / `canBeCraftedBy(Player)` override; current Iron's `1.21.1-3.16.3` defaults both `allowCrafting` and `enabled` to `true`. Effective Scroll Forge eligibility still depends on active server/datapack/global config, a compatible focus/school path, and player-specific learning where applicable; unconditional survival acquisition is not established. See `../HOST-ENABLED-3.16.3-CHECKPOINT.md`.

## Evidence boundary

Identity, school and the File-`6342780` default mechanics baseline above are exact-alpha evidence. Current-physical stats for SHA-1 `7b74816e...` remain unverified. Final damage formulas, range/radius/duration and PvP/boss rules remain `NÃO VERIFICADO` unless separately proven.

Iron's owns host casting/resource settlement; T.O Magic owns this spell. **✅ Cataloged:** the current physical ID is verified; current-physical numerical parity, publisher lineage, survival availability and runtime acceptance are separate unproven gates.

Sources: `../EXACT-4.4.0.1-ARTIFACT-AUDIT.md`; `../EXACT-4.4.0.1-MECHANICS-BASELINE.md`; `../HOST-CRAFTABILITY-3.16.3-CHECKPOINT.md`.
