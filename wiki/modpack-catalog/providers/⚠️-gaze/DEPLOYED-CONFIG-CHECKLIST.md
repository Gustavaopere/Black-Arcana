# Gaze 1.1.7.1 — Deployed Config Closure Checklist

Status: `1 COUNTED SPELL / 26 EXACT RITES / DEPLOYED COMMON CONFIG UNVERIFIED / PROVIDER REMAINS CONDITIONAL`

## Purpose

The exact physical Gaze 1.1.7.1 artifact is already hash-matched and its semantic inventory is already closed at the registry level:

- 1 Gaze-owned Iron's spell, Soulward Shield, is `COUNTED_EXACT`;
- 26 Gaze Spirit Rite identities are exact but configuration-conditional;
- 2 Geas effect types are metric-excluded;
- 8 rune items are metric-excluded.

The remaining catalog blocker for the 26 rites is not another registry audit. It is the effective deployed value of Gaze's COMMON boolean `disableGazeRites`.

The source/default value is `false`, but source defaults are not authoritative pack state and must not be substituted for the deployed value.

## Global gate

Exact-artifact control-flow evidence established:

- configuration symbol: `Config.DISABLE_GAZE_RITES` / `disableGazeRites`;
- config scope: `COMMON`;
- when the resolved value is `true`, Gaze skips registration/initialization of the rite surfaces;
- when the effective deployed value is not known, all 26 Rite identities remain `CONDITIONAL`.

Required authoritative evidence is one of:

1. the actual deployed Gaze COMMON config from the current pack/world showing the effective `disableGazeRites` value; or
2. authoritative runtime/provider observation from the actual assembled pack that proves whether the Gaze Rite registry is initialized under the deployed configuration.

Current repository evidence does not contain that effective value. The current RPG Skill Tree sibling was also searched for `disableGazeRites` / Gaze configuration evidence at `main@2a04efe41a2abbc1f7e5cacdbe091908f764016e` with no matching versioned evidence found. Absence from repository search is not proof of the runtime value.

## Object-by-object closure matrix

All rows share the same global configuration gate. No row may be promoted individually merely because its exact registry identity is known.

| Rite identity | Registry identity | Effective `disableGazeRites` | Current disposition |
|---|---|---|---|
| `gaze_lesser_arcane_rite` | EXACT | `NÃO VERIFICADO` | `CONDITIONAL` |
| `gaze_greater_arcane_rite` | EXACT | `NÃO VERIFICADO` | `CONDITIONAL` |
| `gaze_lesser_sacred_rite` | EXACT | `NÃO VERIFICADO` | `CONDITIONAL` |
| `corrupt_gaze_lesser_sacred_rite` | EXACT | `NÃO VERIFICADO` | `CONDITIONAL` |
| `gaze_greater_sacred_rite` | EXACT | `NÃO VERIFICADO` | `CONDITIONAL` |
| `corrupt_gaze_greater_sacred_rite` | EXACT | `NÃO VERIFICADO` | `CONDITIONAL` |
| `gaze_lesser_aerial_rite` | EXACT | `NÃO VERIFICADO` | `CONDITIONAL` |
| `corrupt_gaze_lesser_aerial_rite` | EXACT | `NÃO VERIFICADO` | `CONDITIONAL` |
| `gaze_greater_aerial_rite` | EXACT | `NÃO VERIFICADO` | `CONDITIONAL` |
| `corrupt_gaze_greater_aerial_rite` | EXACT | `NÃO VERIFICADO` | `CONDITIONAL` |
| `gaze_lesser_aqueous_rite` | EXACT | `NÃO VERIFICADO` | `CONDITIONAL` |
| `corrupt_gaze_lesser_aqueous_rite` | EXACT | `NÃO VERIFICADO` | `CONDITIONAL` |
| `gaze_greater_aqueous_rite` | EXACT | `NÃO VERIFICADO` | `CONDITIONAL` |
| `corrupt_gaze_greater_aqueous_rite` | EXACT | `NÃO VERIFICADO` | `CONDITIONAL` |
| `gaze_lesser_earthen_rite` | EXACT | `NÃO VERIFICADO` | `CONDITIONAL` |
| `corrupt_gaze_lesser_earthen_rite` | EXACT | `NÃO VERIFICADO` | `CONDITIONAL` |
| `gaze_greater_earthen_rite` | EXACT | `NÃO VERIFICADO` | `CONDITIONAL` |
| `corrupt_gaze_greater_earthen_rite` | EXACT | `NÃO VERIFICADO` | `CONDITIONAL` |
| `gaze_lesser_infernal_rite` | EXACT | `NÃO VERIFICADO` | `CONDITIONAL` |
| `corrupt_gaze_lesser_infernal_rite` | EXACT | `NÃO VERIFICADO` | `CONDITIONAL` |
| `gaze_greater_infernal_rite` | EXACT | `NÃO VERIFICADO` | `CONDITIONAL` |
| `corrupt_gaze_greater_infernal_rite` | EXACT | `NÃO VERIFICADO` | `CONDITIONAL` |
| `gaze_lesser_wicked_rite` | EXACT | `NÃO VERIFICADO` | `CONDITIONAL` |
| `corrupt_gaze_lesser_wicked_rite` | EXACT | `NÃO VERIFICADO` | `CONDITIONAL` |
| `gaze_greater_wicked_rite` | EXACT | `NÃO VERIFICADO` | `CONDITIONAL` |
| `corrupt_gaze_greater_wicked_rite` | EXACT | `NÃO VERIFICADO` | `CONDITIONAL` |

## Acceptance branches

### If the effective deployed value is `false`

Then the configuration gate is satisfied for all 26 Rite identities. The catalog may promote those 26 from `CONDITIONAL` to the appropriate counted exact state, subject only to confirming that no other deployed gate suppresses them. Runtime mechanics, numerical balance, Malum resource settlement and future Black Arcana adapter APIs remain separate QA and do not need to be invented or reconstructed for catalog closure.

### If the effective deployed value is `true`

The 26 Rite identities remain exact artifact identities but are not active current-pack Rite registrations under the deployed configuration. They must remain excluded from current active semantic counting. No fallback or Black Arcana-side recreation is permitted.

### If the value remains unavailable

Keep Gaze at `⚠️ Parcial / condicionado` and keep all 26 rows `CONDITIONAL`.

## Already closed — do not redo

- physical Gaze 1.1.7.1 JAR identity and SHA-1;
- exact hash-matched Modrinth artifact audit;
- 26 distinct `RiteHolder<SpiritRiteType>` identities;
- player-facing progression linkage for all 26 Rite holders;
- one Gaze-owned Iron's spell, Soulward Shield, with the optional Iron's provider gate satisfied in the physical pack;
- two Geas effect identities, excluded by metric definition;
- eight rune item identities, excluded by metric definition;
- clean-room authority boundaries among Malum, Gaze, Iron's and Black Arcana.

## Authority boundary

Malum remains authority for Spirit Rite/Geas semantics and spirit-resource settlement. Gaze owns its addon-specific identities and its configuration. Iron's remains authority for its spell framework. Black Arcana must not create a second Rite execution path, second spirit ledger, duplicate Iron's settlement or config fallback.

This checklist closes only the evidence workflow required to resolve the 26 conditional Rite identities. It is not a runtime compatibility certificate.
