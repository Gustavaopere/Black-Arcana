# `traveloptics:sword_of_the_ancients`

**Current physical inventory (2026-10-08):** this is one of **33/33 identities** directly registered in the SHA-1 `7b74816e...` JAR. Catalog **✅**; publisher-File-only mechanics and actual deployed runtime/survival remain version-conditioned or ⚠️. See `../PHYSICAL-JAR-DIRECT-AUDIT-2026-10-08.md`.

- Provider: **T.O Magic n' Extras** (`traveloptics`)
- Version line: `4.4.0.1-1.21.1`
- Exact publisher file: CurseForge `6342780`
- School: **Holy**
- Registry: `traveloptics:sword_of_the_ancients`
- Registry field: `SWORD_OF_THE_ANCIENTS_SPELL`
- Concrete class: `SwordOfTheAncientsSpell`
- State: `✅ CURRENT PHYSICAL ID CATALOGED / ⚠️ RUNTIME QA OPEN`

## Publisher semantic context — version-conditioned

Kobolediator ally summon.

This is **publisher context only** from the living project page; it does not prove exact-alpha or current-physical runtime behavior. See `../PUBLISHER-SEMANTIC-CONTEXT.md`.

## Exact alpha mechanics baseline — File `6342780` only

- Base mana: **100**
- Mana per level: **100**
- Base spell power input: **1**
- Spell power per level input: **1**
- Cast type: **LONG**
- Cast-time field: **80 ticks**
- Max level: **3**
- Minimum rarity: **LEGENDARY**
- Default cooldown: **330 s**

These are direct constants from exact publisher File `6342780`; they are **not** projected to current physical SHA-1 `7b74816e...`. Spell-power inputs are not final damage formulas, and effective host config/multipliers remain separate. See `../EXACT-4.4.0.1-MECHANICS-BASELINE.md`.

## Exact alpha scalar accessors — File `6342780` only

- `getKobolediatorHealth(int)`: **L1 90.0 / L2 125.0 / L3 160.0**

These are exact **raw accessor outputs** from File `6342780`. Count-named values are retained as counts. Health/motion-scale outputs are not converted into final entity health, physical units or final formulas. They are not projected to current physical SHA-1 `7b74816e...`. See `../EXACT-4.4.0.1-SCALAR-ACCESSORS.md`.

## Exact alpha entity-dependent accessor contracts — File `6342780` only

- `getKobolediatorDamage(int, LivingEntity)` — **Family B / host spell power + Iron's `SUMMON_DAMAGE`**; entity local-slot loads: **3**. The bounded audit also observes `LivingEntity.getAttributes()`, `AttributeMap.hasAttribute(...)`, `LivingEntity.getAttributeValue(...)`, `AttributeRegistry.SUMMON_DAMAGE` and exactly one branch.

These are **dependency contracts**, not reconstructed formulas or entity-independent numeric results. Each listed method calls Iron's `getSpellPower(int, Entity)` and additionally depends on the host `SUMMON_DAMAGE` attribute surface. Under the pinned current Iron's `1.21.1-3.16.3` host contract, spell power depends on the spell's base/per-level power inputs plus the caster's global `SPELL_POWER`, current-school power and effective `POWER_MULTIPLIER`. The audit does not infer the branch semantics or numeric coefficient for `SUMMON_DAMAGE`.

No result in this section is projected to current physical Traveloptics SHA-1 `7b74816e...`. See `../EXACT-4.4.0.1-ALL-ENTITY-DEPENDENCY-MAP.md`.

## Reachability

`UNIQUE / allowCrafting=false`; exact loot anchor: Kobolediator loot.

## Evidence boundary

Identity, school and the File-`6342780` default mechanics baseline above are exact-alpha evidence. Current-physical stats for SHA-1 `7b74816e...` remain unverified. Final damage formulas, range/radius/duration and PvP/boss rules remain `NÃO VERIFICADO` unless separately proven.

Iron's owns host casting/resource settlement; T.O Magic owns this spell. **✅ Cataloged:** the current physical ID is verified; current-physical numerical parity, publisher lineage, survival availability and runtime acceptance are separate unproven gates.

Sources: `../EXACT-4.4.0.1-ARTIFACT-AUDIT.md`; `../EXACT-4.4.0.1-MECHANICS-BASELINE.md`.
