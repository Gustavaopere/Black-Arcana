# Ozymandias Sundries 0.0.5 — exact artifact audit

Status: `EXACT PHYSICAL=PUBLISHER ARTIFACT / CLEAN-ROOM TEXT EVIDENCE / 2 REGISTERED SPELLS`

## Audit provenance

- audit branch: `audit/ozymandias-sundries-0.0.5-exact-artifact-2026-09-26`;
- final audit HEAD: `fb5e410b82b8d9f8345d46ac13e8eb6598fea120`;
- final workflow run: `36286741917` — GREEN;
- text-only evidence artifact: `10920474113`;
- evidence-artifact digest: `sha256:554575c37938230e160f4a2c37421f615b471dd550840b3b257390edec71b24d`.

The temporary workflow is evidence-only and is intentionally not merged into the canonical branch.

## Exact identity

- CurseForge project/file: `1209674 / 6978561`;
- pack filename: `ozymandias_sundries-0.0.5.jar`;
- physical SHA-1: `b973622ed90f47108aba481fec3beb19b432d853`;
- publisher/audit SHA-1: `b973622ed90f47108aba481fec3beb19b432d853`;
- audit SHA-256: `9a8e878674933d8ebca69f70727a4d2618351d7f65dc52c8342dc773b8a84d1c`;
- embedded metadata mod id: `ozymandias_sundries`;
- embedded metadata version: `0.0.1`;
- embedded metadata license: `MIT`.

Hash equality closes physical↔publisher artifact identity. The embedded metadata-version mismatch is preserved rather than normalized away.

## Clean-room extraction

The isolated workflow retained only factual text evidence. It did not publish the JAR, implementation bodies, assets, models, textures or sounds.

Exact facts retained from the hash-gated artifact:

- root provider spell localization IDs: `levitate`, `lightning_warp`, `solar_ray`;
- provider spell-named classes: **8**;
- candidate `SpellRegistries` classes: **1**;
- final `Supplier<AbstractSpell>` fields in that registrar: **2**;
- `registerSpell(...)` calls in its static initializer: **2**;
- conditional branches in that initializer: **0**;
- instantiated registered classes: `LevitateSpell`, `LightningWarpSpell`;
- constructor resource roots: `levitate`, `lightning_warp`;
- packaged `irons_spellbooks_spell_config` paths: **0**;
- provider overrides among `allowCrafting`, `allowLooting`, `isEnabled`, `canBeCraftedBy`: **0** for both registered spells.

## Registry-vs-residue rule

Class presence and localization do not create a semantic spell identity when the current registrar does not register that spell.

Consequently the exact count is **2**, not 3 localization roots and not 8 spell-named classes. `solar_ray` and the other unregistered spell classes remain factual artifact contents but contribute zero current semantic registrations.

## Corroborating public source

Public repository `Ozymandias336/Ozymandias_Sundries` at release-date-era main checkpoint `734d5376986c2bae61453bc9837ca934af1b89e0` independently shows the same two active registry calls while several prototype registrations are commented. This is corroboration only; the exact hash-matched binary above is current artifact authority.

## Runtime boundary

`COUNTED_EXACT` closes current semantic identity/inventory. It does not certify assembled-pack config, acquisition probabilities, casts, networking, balance, equipment behavior or compatibility. Those remain separate runtime QA.
