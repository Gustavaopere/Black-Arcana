# Capability Matrix Delta — Reliquified L_Ender's Cataclysm New Relics Fix 1.0.2

Scope: physical `reliquified_lenders_cataclysm_new_relics_fix` 1.0.2 + exact publisher release File ID `8778365`.

| Capability / surface | Exact evidence | Authority | Black Arcana disposition |
|---|---|---|---|
| New standalone spells | none published | none | do not inflate spell catalog |
| New semantic relic identities | none published by fix | none | five repaired relics remain original-addon identities |
| Fixed relic set | Void Cloak, Scouring Eye, Void Vortex in Bottle, Vacuum Glove, Void Bubble | Reliquified L_Ender's Cataclysm | fix adapts only; no identity transfer |
| Old Relics API compatibility | publisher: old 0.10 classes/methods adapted to 0.12 | fix translation + Relics framework | no second bridge |
| Startup/linkage repair | removed `IRelicItem` compatibility | fix | no BA binding to obsolete API |
| Relic definitions | conversion to current `RelicTemplate` | Relics framework | no BA template conversion |
| Curios integration | restored | Curios + addon/fix | no duplicate equip settlement |
| Attribute modifiers | restored | addon intent via provider framework | no duplicate modifiers |
| Stats / levels / ranks | adapted | Relics/addon | no parallel state/progression ledger |
| Cooldowns | adapted | Relics/addon | no duplicate cooldown owner |
| Experience | adapted | Relics/addon | no double XP processing |
| Legacy active abilities | restored | original addon | do not re-trigger from BA |
| Ability order | preserved | original addon/fix | no BA ordering authority |
| Progression values | preserved | original addon | not RPG Skill Tree values |
| Player-motion network seam | replacement published, exact protocol not exposed | provider runtime | fail-closed; no packet contract inferred |
| Descriptions/tooltips | compatibility restored | provider presentation | no gameplay authority inferred |
| 1.0.2 transform scope | limited to addon's base class; avoids global `RelicItem` modifications | fix | confirms bounded bridge; no global Relics override |
| Exact mixins/bytecode internals | not publicly source-pinned | unknown | fail-closed |
| Corruption / Strain / Arcane Danger | none | Black Arcana | no conversion/coupling |
| BA casting/rituals/world effects | none | Black Arcana | no runtime authority transfer |

## Deduplication result

The physical pack already contains a dedicated compatibility owner for Reliquified L_Ender's Cataclysm `0.1.1` against Relics `0.12.x`. Black Arcana must not create another compatibility observer that re-applies template conversion, Curios modifiers, XP/rank/cooldown migration or active-ability settlement for the same relic lifecycle.

## Identity result

The five named relics are existing addon content under Reliquified L_Ender's Cataclysm. The fix contributes **zero new semantic relic identities** and **zero published standalone spell identities**. Its catalog unit is the cross-domain compatibility component itself.

## Gap-analysis result

This component closes a compatibility/deduplication gap, not a Black Arcana spell gap. It supplies no candidate spell/domain for BA and creates no RPG progression contract.

A future BA↔Relics integration, if justified, must use current verified Relics/Curios boundaries and preserve provider state authority rather than leaning on this private compatibility transform as an API.
