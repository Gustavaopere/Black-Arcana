# T.O Magic n' Extras 4.4.0.1 — five remaining entity-power dependency checkpoint

Status: `HISTORICAL FIVE-IDENTITY SUBSET / SUPERSEDED FOR COMPLETE ENTITY-READING SURFACE BY EXACT-4.4.0.1-ALL-ENTITY-DEPENDENCY-MAP.md / NUMERIC OUTPUTS STILL ENTITY+CONFIG CONDITIONAL`

## Supersession

This file remains canonical evidence for the five identity-gap methods audited in PR #623. Audit #658 later dependency-classified all **34/34** `ENTITY_SLOT_READ` numeric accessors. For the complete current dependency surface, use [`EXACT-4.4.0.1-ALL-ENTITY-DEPENDENCY-MAP.md`](EXACT-4.4.0.1-ALL-ENTITY-DEPENDENCY-MAP.md).

## Purpose

After the File-only scalar layer and the current-host effective-cast bridge, exact numeric accessor/bridge coverage touches **28/33** Traveloptics spell identities.

The five exact registered identities still outside that numeric coverage are:

- `traveloptics:reversal`;
- `traveloptics:spectral_blink`;
- `traveloptics:ashen_breath`;
- `traveloptics:lingering_strain`;
- `traveloptics:rapid_laser`.

Each has a selected numeric accessor that reads `LivingEntity`. This checkpoint closes the **dependency surface** only. It does not reconstruct provider formulas and does not assign entity-independent numeric results.

## Exact provider evidence

Temporary NON-MERGE clean-room audit PR **#623**:

- exact artifact: CurseForge `1046916 / 6342780`;
- exact SHA-1: `3808493ce45cdfeb6408e85578adecf13df698e8`;
- audit HEAD: `4ecdab979ecfcd7b5504d100a06569b49e762f2c`;
- workflow run: `37250324497` — **SUCCESS**;
- text artifact: `11320896895`;
- artifact digest: `sha256:eddd9da1c50ba042dda5edc82b46b87327c08621cf01ff3a81d495e5f0c5c3ca`.

Retention was limited to:

- exact class/method identity and descriptor;
- entity local-slot load count;
- branch count;
- unordered field/member invocation identities;
- arithmetic opcode counts.

No numeric constants, instruction sequence, reconstructed formula, method body, asset, localization text or binary content is retained.

## Five exact dependency rows

| Registry ID | Exact accessor | Entity reads | Provider fields | Branches | Exact retained host/member dependency | Arithmetic classification |
| --- | --- | ---: | --- | ---: | --- | --- |
| `traveloptics:reversal` | `calculateDamageMultiplier(int, LivingEntity)` | 1 | none | 0 | only `getSpellPower(int, Entity)` | `fadd ×1; fmul ×1` |
| `traveloptics:spectral_blink` | `getEffectLevel(int, LivingEntity)` | 1 | none | 0 | only `getSpellPower(int, Entity)` | `fmul ×1; f2i ×1; iadd ×1` |
| `traveloptics:ashen_breath` | `getDamage(int, LivingEntity)` | 1 | none | 0 | only `getSpellPower(int, Entity)` | none |
| `traveloptics:lingering_strain` | `getDuration(LivingEntity, int)` | 1 | none | 0 | only `getSpellPower(int, Entity)` | `imul ×1; f2i ×1; iadd ×1` |
| `traveloptics:rapid_laser` | `getDamage(int, LivingEntity)` | 1 | none | 0 | only `getSpellPower(int, Entity)` | `fadd ×1` |

This table is intentionally **not** a reconstructed provider formula. Operation counts are retained only to show that four methods transform host spell power further while Ashen Breath does not expose additional arithmetic in the bounded audit.

## Current Iron's host dependency contract

Current physical host authority:

- Iron's Spellbooks `1.21.1-3.16.3`;
- physical SHA-1 `017fd8140c477f9ae602cf95594f1c23bef1d6e3`.

Matching public source pin:

- `iron431/irons-spells-n-spellbooks@e4056af90302d37eb1739f5ff05020b020e6e252`;
- `gradle.properties`: `mod_version=1.21.1-3.16.3`.

At that source pin, `AbstractSpell.getSpellPower(int, Entity)` depends on:

1. the spell's `baseSpellPower + spellPowerPerLevel * (level - 1)`;
2. the entity's global `SPELL_POWER` attribute when the source is a LivingEntity;
3. the current school power for that LivingEntity;
4. effective `SpellConfigParameter.POWER_MULTIPLIER`.

For all five exact Traveloptics rows above, File `6342780` closes:

- `baseSpellPower = 1`;
- `spellPowerPerLevel = 1`.

Therefore the provider-side dependency is structurally bounded to the host spell-power result for the selected level/entity/config, but the final accessor outputs remain entity/config dependent.

## Catalog consequence

After this checkpoint:

- File-only resolved bounded scalar outputs remain **37 across 24/33** spell identities;
- provider+current-host effective-cast bridge remains **7 results**, with combined numeric accessor/bridge coverage at **28/33** spell identities;
- the five previously uncovered spell identities now have their selected numeric accessor **dependency-classified**;
- therefore **33/33 exact spell identities now have at least one bounded accessor result, host bridge, or entity-dependent accessor contract documented**;
- this is **not** 33/33 numeric closure;
- the five methods in this document still have no entity-independent numeric return value assigned;
- the broader `ENTITY_SLOT_READ` dependency surface is now closed by `EXACT-4.4.0.1-ALL-ENTITY-DEPENDENCY-MAP.md`; numeric outputs remain entity/config conditional.

No result is projected to current physical Traveloptics SHA-1 `7b74816e89cc15dd0b5a31d9ea1e456024e8fae4`.

Traveloptics remains **⚠️ partial/conditioned** and strict current-physical contribution remains **+0**.
