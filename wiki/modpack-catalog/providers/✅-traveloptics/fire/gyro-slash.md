# `traveloptics:gyro_slash`

**Current physical inventory (2026-10-08):** this is one of **33/33 identities** directly registered in the SHA-1 `7b74816e...` JAR. Catalog **✅**; publisher-File-only mechanics and actual deployed runtime/survival remain version-conditioned or ⚠️. See `../PHYSICAL-JAR-DIRECT-AUDIT-2026-10-08.md`.

- Provider: **T.O Magic n' Extras** (`traveloptics`)
- Version line: `4.4.0.1-1.21.1`
- Exact publisher file: CurseForge `6342780`
- School: **Fire**
- Registry: `traveloptics:gyro_slash`
- Registry field: `GYRO_SLASH_SPELL`
- Concrete class: `GyroSlashSpell`
- State: `✅ CURRENT PHYSICAL ID CATALOGED / ⚠️ RUNTIME QA OPEN`

## Publisher semantic context — version-conditioned

weapon slash; evolved pull-projectile/fire jets.

This is **publisher context only** from the living project page; it does not prove exact-alpha or current-physical runtime behavior. See `../PUBLISHER-SEMANTIC-CONTEXT.md`.

## Publisher quantitative / conditional note — version-conditioned

Extended projectile/pull/fire-jet behavior is described for **Infernal Devastator Evo 2 or higher** on the current official project page.

This is **publisher-only context**, not exact-alpha/current-physical proof. The corresponding runtime value or rule remains unverified for File `6342780` and SHA-1 `7b74816e...` unless independently proven.

## Exact alpha mechanics baseline — File `6342780` only

- Base mana: **180**
- Mana per level: **0**
- Base spell power input: **1**
- Spell power per level input: **1**
- Cast type: **LONG**
- Cast-time field: **25 ticks**
- Max level: **1**
- Minimum rarity: **LEGENDARY**
- Default cooldown: **30 s**

These are direct constants from exact publisher File `6342780`; they are **not** projected to current physical SHA-1 `7b74816e...`. Spell-power inputs are not final damage formulas, and effective host config/multipliers remain separate. See `../EXACT-4.4.0.1-MECHANICS-BASELINE.md`.

## Exact-alpha + current-host effective cast-time bridge

- exact File `6342780` relation: `getEffectiveCastTime(int, LivingEntity)` is a **direct delegate** to `getCastTime(level)`;
- current Iron's `1.21.1-3.16.3` host contract: non-`INSTANT` `getCastTime(level)` returns the spell's raw `castTime` field;
- this spell is exact-alpha `LONG` with raw `castTime = 25` ticks;
- bridged result for File `6342780` running under current Iron's 3.16.3: **25 ticks**.

This is **not** counted as a File-6342780-alone scalar result and is **not** projected to current physical Traveloptics SHA-1 `7b74816e...`. See `../EXACT-4.4.0.1-CURRENT-HOST-EFFECTIVE-CAST-BRIDGE.md`.

## Exact alpha entity-dependent accessor contracts — File `6342780` only

- `getDamage(int, LivingEntity)` — **Family A / host spell-power only**; entity local-slot loads: **1**; retained arithmetic classification: `fadd ×1; fmul ×1`. The bounded audit found no field refs, branches or additional entity-member calls.
- `getFlameJetDamage(int, LivingEntity)` — **Family A / host spell-power only**; entity local-slot loads: **1**; retained arithmetic classification: `f2i ×1; fadd ×1; fmul ×1`. The bounded audit found no field refs, branches or additional entity-member calls.

These are **dependency contracts**, not reconstructed formulas or entity-independent numeric results. Each listed method calls Iron's `getSpellPower(int, Entity)`. Under the pinned current Iron's `1.21.1-3.16.3` host contract, that host value depends on the spell's base/per-level power inputs plus the caster's global `SPELL_POWER`, current-school power and effective `POWER_MULTIPLIER`.

No result in this section is projected to current physical Traveloptics SHA-1 `7b74816e...`. See `../EXACT-4.4.0.1-ALL-ENTITY-DEPENDENCY-MAP.md`.

## Reachability

`WEAPON / allowCrafting=true`; provider item references exist; assembled-pack runtime still unverified.

## Evidence boundary

Identity, school and the File-`6342780` default mechanics baseline above are exact-alpha evidence. Current-physical stats for SHA-1 `7b74816e...` remain unverified. Final damage formulas, range/radius/duration and PvP/boss rules remain `NÃO VERIFICADO` unless separately proven.

Iron's owns host casting/resource settlement; T.O Magic owns this spell. **✅ Cataloged:** the current physical ID is verified; current-physical numerical parity, publisher lineage, survival availability and runtime acceptance are separate unproven gates.

Sources: `../EXACT-4.4.0.1-ARTIFACT-AUDIT.md`; `../EXACT-4.4.0.1-MECHANICS-BASELINE.md`.
