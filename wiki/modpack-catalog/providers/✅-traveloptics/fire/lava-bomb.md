# `traveloptics:lava_bomb`

**Current physical inventory (2026-10-08):** this is one of **33/33 identities** directly registered in the SHA-1 `7b74816e...` JAR. Catalog **✅**; publisher-File-only mechanics and actual deployed runtime/survival remain version-conditioned or ⚠️. See `../PHYSICAL-JAR-DIRECT-AUDIT-2026-10-08.md`.

- Provider: **T.O Magic n' Extras** (`traveloptics`)
- Version line: `4.4.0.1-1.21.1`
- Exact publisher file: CurseForge `6342780`
- School: **Fire**
- Registry: `traveloptics:lava_bomb`
- Registry field: `LAVAL_BOMB_SPELL`
- Concrete class: `LavaBombSpell`
- State: `✅ CURRENT PHYSICAL ID CATALOGED / ⚠️ RUNTIME QA OPEN`

## Publisher semantic context — version-conditioned

explosive arcing shots; lava pools/absorption.

This is **publisher context only** from the living project page; it does not prove exact-alpha or current-physical runtime behavior. See `../PUBLISHER-SEMANTIC-CONTEXT.md`.

## Publisher quantitative / conditional note — version-conditioned

Projectile launch geometry: **45° forward angle** on the current official project page.

This is **publisher-only context**, not exact-alpha/current-physical proof. The corresponding runtime value or rule remains unverified for File `6342780` and SHA-1 `7b74816e...` unless independently proven.

## Exact alpha mechanics baseline — File `6342780` only

- Base mana: **40**
- Mana per level: **20**
- Base spell power input: **1**
- Spell power per level input: **1**
- Cast type: **LONG**
- Cast-time field: **50 ticks**
- Max level: **3**
- Minimum rarity: **EPIC**
- Default cooldown: **18 s**

These are direct constants from exact publisher File `6342780`; they are **not** projected to current physical SHA-1 `7b74816e...`. Spell-power inputs are not final damage formulas, and effective host config/multipliers remain separate. See `../EXACT-4.4.0.1-MECHANICS-BASELINE.md`.

## Exact alpha scalar accessors — File `6342780` only

- `getMotionScale()`: **1.0**

These are exact **raw accessor outputs** from File `6342780`. Count-named values are retained as counts. Health/motion-scale outputs are not converted into final entity health, physical units or final formulas. They are not projected to current physical SHA-1 `7b74816e...`. See `../EXACT-4.4.0.1-SCALAR-ACCESSORS.md`.

## Exact alpha entity-dependent accessor contracts — File `6342780` only

- `getProjectileCount(int, LivingEntity)` — **Family A / host spell-power only**; entity local-slot loads: **1**; retained arithmetic classification: none. The bounded audit found no field refs, branches or additional entity-member calls.

These are **dependency contracts**, not reconstructed formulas or entity-independent numeric results. Each listed method calls Iron's `getSpellPower(int, Entity)`. Under the pinned current Iron's `1.21.1-3.16.3` host contract, that host value depends on the spell's base/per-level power inputs plus the caster's global `SPELL_POWER`, current-school power and effective `POWER_MULTIPLIER`.

No result in this section is projected to current physical Traveloptics SHA-1 `7b74816e...`. See `../EXACT-4.4.0.1-ALL-ENTITY-DEPENDENCY-MAP.md`.

## Reachability

`HOST/PUBLISHER-DEFAULT CRAFTABLE + ENABLED / EFFECTIVE ELIGIBILITY CONDITIONAL`: exact File `6342780` class has no direct craftability or enabled-default mutator and no concrete `isEnabled()` / `canBeCraftedBy(Player)` override; current Iron's `1.21.1-3.16.3` defaults both `allowCrafting` and `enabled` to `true`. Effective Scroll Forge eligibility still depends on active server/datapack/global config, a compatible focus/school path, and player-specific learning where applicable; unconditional survival acquisition is not established. See `../HOST-ENABLED-3.16.3-CHECKPOINT.md`.

## Evidence boundary

Identity, school and the File-`6342780` default mechanics baseline above are exact-alpha evidence. Current-physical stats for SHA-1 `7b74816e...` remain unverified. Final damage formulas, range/radius/duration and PvP/boss rules remain `NÃO VERIFICADO` unless separately proven.

Iron's owns host casting/resource settlement; T.O Magic owns this spell. **✅ Cataloged:** the current physical ID is verified; current-physical numerical parity, publisher lineage, survival availability and runtime acceptance are separate unproven gates.

Sources: `../EXACT-4.4.0.1-ARTIFACT-AUDIT.md`; `../EXACT-4.4.0.1-MECHANICS-BASELINE.md`; `../HOST-CRAFTABILITY-3.16.3-CHECKPOINT.md`.
