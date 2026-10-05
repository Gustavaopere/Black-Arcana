# Iron's Spellbooks KubeJS — project-owner authored-content attestation (2026-10-05)

Status: `CATALOG EVIDENCE / OWNER ATTESTATION / ZERO PROJECT-AUTHORED IRON'S SPELL-SCHOOL CONTENT`

## Statement recorded

On 2026-10-05, the project owner explicitly confirmed in the Black Arcana project conversation that the modpack team did not create any custom spells through Iron's Spellbooks KubeJS, and clarified that the addon was included specifically to provide a mechanism for creating such content in the future.

For catalog purposes, this attestation is direct project-authority evidence about authored content. It is not a forensic statement about every byte currently present in a launcher instance.

## Evidence combined with this attestation

The exact addon 4.0.3 provider-source audit already establishes:

- fixed provider-built spell identities: **0**;
- fixed provider-built school identities: **0**;
- exact source repository coverage: **49 / 49 paths classified**;
- no packaged provider `data/**` or generated-resource spell/school roster;
- the addon is a scripting/framework bridge whose semantic additions require external KubeJS definitions.

The current physical modlist independently establishes the installed stack:

- `irons_spells_js-4.0.3.jar`;
- `irons_spellbooks-1.21.1-3.16.3.jar`;
- `kubejs-neoforge-2101.7.2-build.377.jar`.

## Catalog consequence

At the project's catalog-completeness evidence ceiling:

- provider-owned fixed spell contribution: **0**;
- provider-owned fixed school contribution: **0**;
- project-authored custom Iron's spell/school contribution: **0**;
- strict semantic delta: **+0**;
- provider status: **✅ cataloged / ZERO_SEMANTIC_SCRIPTING_FRAMEWORK**.

This follows the provider-folder rule that deployed config/runtime/reachability QA does not by itself keep a closed semantic denominator under `⚠️`.

## Deployment-parity boundary

The exact current assembled instance's `kubejs/startup_scripts/**`, `server_scripts/**`, `client_scripts/**` and `data/**` tree has not been physically inspected in this evidence pass.

Therefore this attestation does **not** claim:

- that the current filesystem contains zero KubeJS files;
- that no stale/example/test file exists;
- that the exact deployment has been parity-verified.

Those are deployment QA questions.

If future physical evidence reveals an actual Iron's spell/school registration, provider #98 must be reopened for exact object-level cataloging.

## Canonical disposition

`✅ ZERO_SEMANTIC_SCRIPTING_FRAMEWORK / +0`

Physical KubeJS-tree parity: `PENDING QA`.
