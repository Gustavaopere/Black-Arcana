# Capability Matrix Delta — GTBC's SpellLib 2.2.0

Phase: **2AY**
Physical provider: `gtbcs_spell_lib-2.2.0-1.21.1.jar`
Mod id: `gtbcs_spell_lib`
Runtime version: `2.2.0-1.21.1`
Physical SHA-1: `36cce8ab3117e89ae992a84a566d596709db2ffe`

## Closure disposition

GTBC's SpellLib is a shared Iron's-addon library/API, not an independent player-facing spell provider at the current publisher-defined surface.

| Surface | Current evidence | Authority / disposition | Semantic magic delta |
|---|---|---|---:|
| Spell-related attributes | publisher lists spell crit/damage/projectile-related attributes; 2.2.0 adds Healing Received, Damage Taken and Summon Health | GTBC library owns these provider attributes where consumed; attributes are not spells | 0 |
| Reusable spell abstraction | publisher lists an `AdvancedSpell` base/helper abstraction | developer infrastructure; consumer provider owns concrete registered spell identity | 0 |
| Spell imbuement helpers | publisher lists reusable Curio/armor imbuement abstractions | infrastructure for holding/assigning external consumer spells; no new semantic spell inferred | 0 |
| Particle/trade/Curio/GeckoLib/summon helpers | publisher lists reusable utility classes/frameworks | API/support surface, not standalone magical actions | 0 |
| Independent gameplay/spell catalog | publisher explicitly says the library does not provide standalone gameplay on its own | **0 independent semantic magic objects** | **0** |
| Black Arcana integration | no exact public source/API signature contract is pinned; project is closed-source ARR | **FAIL-CLOSED** for provider-specific runtime coupling beyond externally proven contracts | 0 |

## Provider-component coverage

GTBC's SpellLib is part of the reconciled magic/cross-domain provider inventory represented by the established 100-component denominator.

- canonical base on `main@ff5b99106c91723cce2a13f363f7af1336c5d5c1`: **52/100**;
- Phase 2AY candidate after this audit: **53/100**;
- denominator delta: **0**.

Do not report `53/100` as a percentage of spells/magics. It is only the internal component-audit metric and remains candidate until latest-main reconciliation, exact-HEAD CI, merge and post-merge confirmation.

## Semantic spell/magic metric

Phase 2AY adds no independent semantic magic object:

- strict semantic counted minimum before Phase 2AY: **796**;
- semantic numerator delta: **+0**;
- semantic denominator delta attributable to GTBC's SpellLib: **+0**;
- strict counted minimum after this audit candidate: **796**.

The global semantic denominator remains open because unresolved spell/ritual providers still lack complete current inventories.

## Exactness / clean-room boundary

Physical identity is exact from the current modlist and the exact public 2.2.0 NeoForge release is pinned to CurseForge Project/File `1194714 / 8824651`.

The project is All Rights Reserved and publisher text explicitly prohibits decompilation/extraction/reuse of its code/assets. No source revision is used. This closure is therefore publisher-bounded and factual only; internal registries, Java signatures and unsupported integration seams remain fail-closed.

## Black Arcana boundary

Black Arcana retains authority for its canonical casting pipeline, costs, targeting/effects, cooldowns/charges, hazards, rituals, Corruption, Strain, Arcane Danger, Backlash and WorldEffectPolicy. GTBC's SpellLib does not authorize a second spell/resource pipeline or direct mutation of consumer-provider state.