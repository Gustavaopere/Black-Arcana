# T.O Magic n' Extras 4.4.0.1 — exact publisher mechanics baseline

Status: `EXACT FILE 6342780 / 33 REGISTERED SPELLS / DEFAULT HOST INPUTS CLOSED / CURRENT PHYSICAL NOT PROJECTED`

## Authority

This checkpoint is derived from a temporary NON-MERGE clean-room audit of the exact publisher artifact:

- CurseForge project/file: `1046916 / 6342780`;
- exact publisher SHA-1: `3808493ce45cdfeb6408e85578adecf13df698e8`;
- audit PR: **#599**;
- authoritative audit HEAD: `6789b859c3b617e1174e9b0e5ff6df48d2a993b3`;
- workflow run: `37236187715` — **SUCCESS**;
- text artifact: `11315159450`;
- artifact digest: `sha256:7001221a307d3a81ba8ef8b41a0dba29a059a2fbaf6b756fc2db0edb26996eb9`;
- registered concrete spell classes: **33**;
- unresolved retained mechanic fields: **0**.

Earlier parser-development runs in PR #599 are superseded and are not catalog authority.

## Retention boundary

The audit retained only class identity plus direct constant facts for:

- `baseManaCost`;
- `manaCostPerLevel`;
- `baseSpellPower`;
- `spellPowerPerLevel`;
- `castTime` field in ticks;
- `CastType`;
- `DefaultConfig.setMaxLevel(...)`;
- `DefaultConfig.setMinRarity(...)`;
- `DefaultConfig.setCooldownSeconds(...)`.

No method bodies, source reconstruction, loot/recipe payloads, assets, localization prose or binary content are retained.

## Interpretation boundary

These values are **exact defaults/raw host inputs for publisher File `6342780` only**.

They are not promoted to the installed physical Traveloptics SHA-1 `7b74816e89cc15dd0b5a31d9ea1e456024e8fae4`, because that artifact remains `OTHER_VERIFIED` relative to File `6342780`.

Additional limits:

- effective mana and spell power can be modified by Iron's config/entity/school multipliers;
- `baseSpellPower` and `spellPowerPerLevel` are host spell-power inputs, **not** proof of final damage formulas;
- cooldown values are DefaultConfig defaults and can be config-resolved by the host;
- rarity/max-level values are exact defaults from File `6342780`, not deployed-config attestations;
- range, radius, duration, PvP/boss policy, custom damage coefficients, projectile physics and other spell-specific formulas remain separate evidence questions unless already closed elsewhere;
- craftability/acquisition remains governed by the dedicated craftability/loot checkpoints.

Current physical Iron's Spellbooks is `1.21.1-3.16.3`. Its source pin `iron431/irons-spells-n-spellbooks@e4056af90302d37eb1739f5ff05020b020e6e252` shows that these base/per-level fields feed host mana/spell-power calculations, but this does not bridge File `6342780` constants into the modified current Traveloptics JAR.

## Exact baseline — 33/33

| Registry ID | Base mana | Mana/level | Base power | Power/level | Cast type | Cast time (ticks) | Max level | Min rarity | Cooldown default (s) |
| --- | ---: | ---: | ---: | ---: | --- | ---: | ---: | --- | ---: |
| `traveloptics:blood_howl` | 70 | 20 | 1 | 1 | INSTANT | 0 | 5 | UNCOMMON | 20 |
| `traveloptics:abyssal_blast` | 50 | 150 | 1 | 1 | LONG | 50 | 3 | EPIC | 22 |
| `traveloptics:blackout` | 100 | 50 | 1 | 1 | LONG | 39 | 3 | LEGENDARY | 120 |
| `traveloptics:psychic_bolt` | 50 | 20 | 1 | 1 | INSTANT | 0 | 3 | EPIC | 40 |
| `traveloptics:reversal` | 50 | 50 | 1 | 1 | INSTANT | 0 | 3 | RARE | 3 |
| `traveloptics:spectral_blink` | 10 | 20 | 1 | 1 | INSTANT | 0 | 3 | RARE | 25 |
| `traveloptics:eternal_sentinel` | 100 | 100 | 1 | 1 | LONG | 80 | 3 | EPIC | 330 |
| `traveloptics:orbital_void` | 40 | 40 | 1 | 1 | LONG | 40 | 5 | RARE | 25 |
| `traveloptics:cursed_minefield` | 10 | 20 | 1 | 1 | LONG | 45 | 8 | COMMON | 30 |
| `traveloptics:void_eruption` | 70 | 55 | 1 | 1 | LONG | 8 | 3 | EPIC | 25 |
| `traveloptics:vortex_punch` | 70 | 70 | 1 | 1 | LONG | 15 | 3 | LEGENDARY | 18 |
| `traveloptics:astral_sense` | 100 | 50 | 1 | 1 | INSTANT | 0 | 3 | RARE | 120 |
| `traveloptics:ashen_breath` | 5 | 2 | 1 | 1 | CONTINUOUS | 100 | 10 | COMMON | 15 |
| `traveloptics:lingering_strain` | 50 | 50 | 1 | 1 | INSTANT | 0 | 3 | EPIC | 120 |
| `traveloptics:ignited_onslaught` | 50 | 75 | 1 | 1 | LONG | 60 | 5 | RARE | 360 |
| `traveloptics:burning_judgment` | 40 | 40 | 1 | 1 | LONG | 50 | 6 | COMMON | 18 |
| `traveloptics:meteor_storm` | 50 | 30 | 1 | 1 | LONG | 15 | 6 | EPIC | 90 |
| `traveloptics:lava_bomb` | 40 | 20 | 1 | 1 | LONG | 50 | 3 | EPIC | 18 |
| `traveloptics:gyro_slash` | 180 | 0 | 1 | 1 | LONG | 25 | 1 | LEGENDARY | 30 |
| `traveloptics:nullflare` | 40 | 30 | 1 | 1 | LONG | 16 | 5 | COMMON | 40 |
| `traveloptics:summon_desert_dwellers` | 100 | 75 | 1 | 1 | LONG | 60 | 5 | RARE | 420 |
| `traveloptics:sword_of_the_ancients` | 100 | 100 | 1 | 1 | LONG | 80 | 3 | LEGENDARY | 330 |
| `traveloptics:axe_of_the_doomed` | 120 | 100 | 1 | 1 | LONG | 80 | 3 | LEGENDARY | 360 |
| `traveloptics:cursed_revenants` | 40 | 30 | 1 | 1 | LONG | 45 | 5 | COMMON | 150 |
| `traveloptics:despair` | 18 | 18 | 1 | 1 | INSTANT | 0 | 10 | COMMON | 18 |
| `traveloptics:halberd_horizon` | 30 | 40 | 1 | 1 | LONG | 21 | 6 | RARE | 20 |
| `traveloptics:cursed_blast` | 200 | 0 | 1 | 0 | LONG | 28 | 1 | LEGENDARY | 3 |
| `traveloptics:mechanized_predator` | 100 | 100 | 1 | 1 | LONG | 80 | 5 | RARE | 540 |
| `traveloptics:rapid_laser` | 4 | 1 | 1 | 1 | CONTINUOUS | 100 | 10 | COMMON | 12 |
| `traveloptics:death_laser` | 100 | 50 | 1 | 1 | LONG | 20 | 3 | UNCOMMON | 16 |
| `traveloptics:em_pulse` | 0 | 50 | 1 | 1 | LONG | 20 | 5 | COMMON | 45 |
| `traveloptics:aerial_collapse` | 60 | 60 | 1 | 1 | LONG | 10 | 5 | UNCOMMON | 45 |
| `traveloptics:stele_cascade` | 35 | 25 | 1 | 1 | LONG | 20 | 6 | COMMON | 22 |

## Aggregate observations

- cast types: **7 INSTANT / 2 CONTINUOUS / 24 LONG**;
- max-level distribution is exact per row; no inferred level ceilings;
- all 33 classes define a minimum rarity and cooldown default;
- all 33 classes define the five host scalar fields;
- `traveloptics:cursed_blast` is the only row with `spellPowerPerLevel = 0`;
- `traveloptics:gyro_slash` and `traveloptics:cursed_blast` use `manaCostPerLevel = 0`;
- `traveloptics:em_pulse` uses `baseManaCost = 0`.

These are descriptive constants, not balance judgments.

## Catalog disposition

This checkpoint closes the **publisher-alpha mechanics baseline** for all 33 registered File-6342780 spells.

It does **not** change provider status:

- current physical Traveloptics remains **⚠️ partial/conditioned**;
- current physical registry/stat equality remains unverified;
- `traveloptics:blackout` survival acquisition remains unresolved;
- current physical loot-modifier wiring/provenance remains unresolved;
- strict contribution remains fail-closed until current-physical authority is sufficient.
