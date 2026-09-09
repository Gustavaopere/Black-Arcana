# Not Enough Glyphs 4.6.1 — Primitive Files

This directory contains one file for every primitive that NEG calls through `APIRegistry.registerSpell` under the current physical pack's loaded-mod conditions.

Current count: **40 registered**, of which **39 are source-enabled**; Momentum is source-disabled. The four real Ars Elemental primitives added only to NEG's internal listing are documented in `../DELEGATION-AND-DISABLED.md`, not duplicated here.

## Canonical functional taxonomy

The first directory level follows the canonical Ars-provider taxonomy used by this wiki:

- `forms/` — cast/delivery forms;
- `effects/` — effects, propagators, filters and contingency spell parts;
- `augments/` — reserved for provider augments; NEG has no current-pack registration in this class.

Provenance is preserved below the functional class rather than replacing it:

- `neg/` — NEG-native registrations;
- `toomanyglyphs-fallback/` — NEG implementations active because Too Many Glyphs is absent;
- `arsomega-fallback/` — NEG implementations active because Ars Omega is absent;
- `ars-trinkets-fallback/` — NEG implementations active because Ars Trinkets is absent;
- `ars-scalaes-fallback/` — Resize registered under the historical Ars Scalaes namespace.

The current 40 registrations therefore resolve to **4 forms + 36 effects + 0 augments**. Historical namespaces remain identity/provenance markers; they do not create duplicate Black Arcana capabilities.

Every page is source-pinned to `Alexthw46/NotEnoughGlyphs@2f0c7b9fcf802c7e85b4ed4d7ed94123bcee398b`. Fields inherited only from Ars/Sauce remain provider-owned rather than guessed.