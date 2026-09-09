# Evidence and provenance — Monsters & Spellbooks

## Physical authority

Latest physical Black Arcana modlist:

- `monstersspellbooks-0.0.16.3.jar`
- mod id `monstersspellbooks`
- runtime `0.0.16.3`
- SHA-1 `b3aa89fd081bf4bfaf8d0f4380bcdc393c66ab0e`
- Minecraft 1.21.1
- NeoForge `21.1.248`
- physical host Iron's `1.21.1-3.16.3`

## Exact publisher release

CurseForge project `1428928`, file `8788560`:

- filename `monstersspellbooks-0.0.16.3.jar`;
- Minecraft 1.21.1;
- NeoForge;
- release type `Release`;
- uploaded 2026-09-01;
- current project page describes `90+ spells` and `2 new spell schools`;
- current project page labels the project `MIT License`.

Exact 0.0.16.3 changelog facts are recorded in the provider README.

## Official public source baseline

Repository: `RedReaper28/Monsters-Spellbooks-1.21.1`

Pin inspected: `1ab9b72af2ea44c3c8b816e665d06531ea44ddc2`.

The pin is current public repository history from 2026-09-01, but its build metadata remains `mod_version=0.0.14`, NeoForge `21.1.216`, Iron's `1.21.1-3.15.4`. It is therefore **not exact 0.0.16.3 source authority**.

No repository tags were found and commit search did not locate a `0.0.16.3` source declaration.

## License/provenance divergence

Evidence is internally inconsistent:

- current CurseForge project metadata says `MIT License`;
- source `gradle.properties` at the inspected public pin says `mod_license=All Rights Reserved`;
- repository `TEMPLATE_LICENSE.txt` is the NeoForge/MDK template license and explicitly concerns use of the MDK template/header snippets. It is **not** treated as a license grant for the addon's implementation or assets.

Classification: `REFERENCE_ONLY / COMPATIBILITY_TARGET / LICENSE METADATA DIVERGENCE / CURRENT-SOURCE VERSION MISMATCH`.

This phase uses source strictly read-only for factual cataloging. No provider code, assets, text, models, sounds or implementation are copied/adapted into Black Arcana. Any future derivation/reuse would require a separately resolved exact license/provenance record.

## Evidence ceiling

Proven now:

- exact installed identity/hash;
- exact public 0.0.16.3 release identity and release delta;
- publisher current `90+ spells / 2 schools` scale;
- source-baseline 98 registrations and two source school registrations at the official public pin.

Not proven:

- exact 0.0.16.3 registry total/IDs;
- exact 0.0.16.3 class/signature/API parity;
- exact current Aero registration;
- exact current configs/network/persistence;
- exact installed full-modpack behavior;
- a safe provider-specific Black Arcana hook.

Those remain `UNVERIFIED / FAIL-CLOSED`.