# Asterism Arcanum 0.1.0 — exact binary registry audit

Status: `EXACT HASH-MATCHED PHYSICAL/PUBLISHER ARTIFACT / 11 REGISTERED BINARY SPELL CLASS REFERENCES / 10 PUBLISHER SURVIVAL SPELLS + 1 CREATIVE-ONLY GATEWAY / NO PACKAGED HOST OVERRIDE`

## Provenance

Physical artifact:

- `asterismarcanum-1.21.1-0.1.0.jar`;
- SHA-1 `4a25ba80116168ddcc812f71467c0598127e774a`.

Exact publisher artifact:

- CurseForge project `1456947`;
- file `8157080`;
- Curse Maven `curse.maven:asterism-arcanum-1456947:8157080`.

Source correlation:

- `BirdieVibes/Asterism-Arcanum@f1738c7813a85d31a6da10e6c9f2dbce18d2b583`.

NON-MERGE audit:

- Black Arcana commit `1c27d711f1359075edc403d30e86de9397a38f13`;
- CI run `36252798657`;
- temporary exact-binary audit step: SUCCESS;
- unit tests / diff sanity / NeoForge build / JAR checks / Foundation GameTest / dedicated-server smoke / Stage 05 companion smoke: SUCCESS.

The temporary workflow/script are audit-only and are not merged into the durable catalog.

## Cryptographic equality

Observed exact publisher artifact:

- bytes: `987,245`;
- SHA-1: `4a25ba80116168ddcc812f71467c0598127e774a`;
- SHA-256: `191422cf3096a79e158d3262b52ea98fb1abc745847d4eb356548a5a5f58eebc`.

Physical SHA-1 = publisher artifact SHA-1:

**true**

## Structural inventory

Exact artifact:

- total classes: **113**;
- provider classes: **113**;
- provider resources: **472**;
- provider Spell classes: **11**.

Exact Spell classes:

1. `AstralEchoSpell`;
2. `AstralGatewaySpell`;
3. `BrightburstSpell`;
4. `CelestialTetherSpell`;
5. `LuminousBeamSpell`;
6. `PiercingLightSpell`;
7. `SilveryBarbsSpell`;
8. `StarSwarmSpell`;
9. `StarcutterSpell`;
10. `StarfireSpell`;
11. `SummonLunarMothsSpell`.

## Exact registrar correlation

Binary registrar:

`com/birdie/asterismarcanum/registries/ASARSpellRegistry.class`

Audit result:

- expected registered spell-class references: **11**;
- missing expected references: **0**;
- Trailblaze registry reference: **false**.

All eleven expected spell ID strings are present in provider classfile constants.

This aligns the exact binary with the source-pinned 11-registration registry and excludes Trailblaze from the exact packaged registrar.

## Host-override surface

Exact artifact search:

- packaged `irons_spellbooks_spell_config` resources: **0**;
- packaged `astral_gateway` host override resources: **0**;
- exact Astromancer loot resource present: **true**.

Exact `javap -p` inspection of `AstralGatewaySpell` found no declared method named:

- `allowLooting`;
- `allowCrafting`;
- `isEnabled`;
- `canBeCraftedBy`.

Therefore the exact provider artifact does not itself override those host eligibility methods or ship a provider datapack override for Gateway.

This does **not** prove the effective deployed external Iron's config/datapack state.

## Publisher survival boundary

Exact publisher File `8157080` lists ten normal spells under `Spells` and lists Astral Gateway separately under `Unfinished/Creative Features`, stating that it cannot be accessed in survival.

Catalog disposition:

- ten normal spells: **COUNTED_EXACT**;
- Astral Gateway: **CONDITIONAL / outside strict count**.

## Clean-room boundary

The audit retained only:

- hashes;
- archive/class/resource counts;
- class/resource identities;
- exact registrar class references;
- presence/absence of narrow host override resources;
- declared method-name presence/absence needed for interoperability/cataloging.

No implementation body, assets, textures, models, sounds or proprietary source reconstruction are copied into Black Arcana.

## Result

Exact current Asterism 0.1.0 identity/inventory evidence is now physical-artifact exact for the ten counted survival spells.

Strict Asterism contribution remains **10**.

Semantic delta from this evidence upgrade: **+0**.

Provider remains **⚠️ partial/conditioned** only because Astral Gateway's effective deployed survival state is not authoritative.
