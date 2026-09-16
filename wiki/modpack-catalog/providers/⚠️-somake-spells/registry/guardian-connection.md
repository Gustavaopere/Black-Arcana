# `guardian_connection`

- Provider: **Somake Spells** (`somakespells`)
- Artifact: `somakespells-1.0.8-1.21.1-fix.jar`
- SHA-1: `b0ad94c1504709662bee2d08700375ccecbb5ec7`
- Substrate: **Iron's Spells 'n Spellbooks**
- Registry ID: `guardian_connection`
- Gate: `mowziesmobs` present
- State: `EXACT_REGISTRY / REACHABILITY_CONDITIONAL`

## Registration gate

Exact 1.0.8-fix bytecode gates this registration on `ModList.get().isLoaded("mowziesmobs")`. The physical pack contains Mowzie's Mobs `1.8.2`; the registration gate is satisfied.

## Evidence boundary

Identity is exact, but object-level survival reachability and the deployed `enableSpellLockSystem` COMMON value are not proven. Do not infer display name, school, level, rarity, costs, timing, formulas, targeting or acquisition from the ID. Those fields remain `NÃO VERIFICADO` unless separately evidenced.

Iron's owns host casting/resource settlement; Somake owns this spell identity and provider progression. Black Arcana does not duplicate either runtime.

Sources: `../EXACT-1.0.8-FIX-ARTIFACT-AUDIT.md`, `../SPELL-CATALOG-1.0.8-FIX.md`.
