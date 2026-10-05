# `traveloptics:abyssal_blast`

- Provider: **T.O Magic n' Extras** (`traveloptics`)
- Version line: `4.4.0.1-1.21.1`
- Exact publisher file: CurseForge `6342780`
- School: **Eldritch**
- Registry: `traveloptics:abyssal_blast`
- Registry field: `ABYSSAL_BLAST_SPELL`
- Concrete class: `AbyssalBlastSpell`
- State: `EXACT REGISTRY / RUNTIME CONDITIONAL`

## Publisher semantic context — version-conditioned

stationary straight abyssal beam.

This is **publisher context only** from the living project page; it does not prove exact-alpha or current-physical runtime behavior. See `../PUBLISHER-SEMANTIC-CONTEXT.md`.

## Exact alpha mechanics baseline — File `6342780` only

- Base mana: **50**
- Mana per level: **150**
- Base spell power input: **1**
- Spell power per level input: **1**
- Cast type: **LONG**
- Cast-time field: **50 ticks**
- Max level: **3**
- Minimum rarity: **EPIC**
- Default cooldown: **22 s**

These are direct constants from exact publisher File `6342780`; they are **not** projected to current physical SHA-1 `7b74816e...`. Spell-power inputs are not final damage formulas, and effective host config/multipliers remain separate. See `../EXACT-4.4.0.1-MECHANICS-BASELINE.md`.

## Exact-alpha + current-host effective cast-time bridge

- exact File `6342780` relation: `getEffectiveCastTime(int, LivingEntity)` is a **direct delegate** to `getCastTime(level)`;
- current Iron's `1.21.1-3.16.3` host contract: non-`INSTANT` `getCastTime(level)` returns the spell's raw `castTime` field;
- this spell is exact-alpha `LONG` with raw `castTime = 50` ticks;
- bridged result for File `6342780` running under current Iron's 3.16.3: **50 ticks**.

This is **not** counted as a File-6342780-alone scalar result and is **not** projected to current physical Traveloptics SHA-1 `7b74816e...`. See `../EXACT-4.4.0.1-CURRENT-HOST-EFFECTIVE-CAST-BRIDGE.md`.

## Reachability

`UNIQUE / allowCrafting=false`; exact loot anchor: Leviathan loot.

## Evidence boundary

Identity, school and the File-`6342780` default mechanics baseline above are exact-alpha evidence. Current-physical stats for SHA-1 `7b74816e...` remain unverified. Final damage formulas, range/radius/duration and PvP/boss rules remain `NÃO VERIFICADO` unless separately proven.

Iron's owns host casting/resource settlement; T.O Magic owns this spell. Provider stays **⚠️** because current-physical registry equality/provenance and full runtime closure are not proven.

Sources: `../EXACT-4.4.0.1-ARTIFACT-AUDIT.md`; `../EXACT-4.4.0.1-MECHANICS-BASELINE.md`.
