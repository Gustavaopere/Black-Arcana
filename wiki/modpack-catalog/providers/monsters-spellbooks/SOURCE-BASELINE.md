# Source baseline — official public repository

Status: `REFERENCE BASELINE / NOT EXACT 0.0.16.3 BINARY AUTHORITY`

## Pin

- Repository: `RedReaper28/Monsters-Spellbooks-1.21.1`
- Branch: `main`
- Commit: `1ab9b72af2ea44c3c8b816e665d06531ea44ddc2`
- Commit date: 2026-09-01
- Commit message: `Removed Pale Garden Content,moved to other project`

## Build metadata observed at the pin

`gradle.properties` declares:

- Minecraft `1.21.1`;
- NeoForge `21.1.216`;
- mod id `monstersspellbooks`;
- mod name `Monsters & Spellbooks`;
- mod version `0.0.14`;
- Iron's Spells `1.21.1-3.15.4`;
- source metadata license `All Rights Reserved`.

Physical pack authority is newer/different:

- installed JAR `monstersspellbooks-0.0.16.3.jar`;
- NeoForge `21.1.248`;
- Iron's `1.21.1-3.16.3`.

No official repository tag was found, and repository commit search did not locate a commit declaring `0.0.16.3`.

## What this baseline may prove

This pin may support factual statements explicitly scoped as **source-baseline observations**, including:

- source-visible spell registration families and count;
- source-visible custom school registrations;
- package/registry structure;
- semantic overlap candidates useful for deduplication.

It does **not** prove:

- exact installed 0.0.16.3 registry count or IDs;
- exact 0.0.16.3 class/signature/API parity;
- exact 0.0.16.3 configs/defaults;
- exact network payload or persistence schema;
- exact host-version compatibility behavior;
- that source-visible Aero registration survives unchanged in 0.0.16.3.

## Fail-closed rule

Where a Black Arcana integration would require any exact provider identifier, API signature, event ordering, resource settlement contract or server/client boundary, this source baseline is insufficient by itself. Require release-exact evidence or an inspectable exact artifact before implementation.