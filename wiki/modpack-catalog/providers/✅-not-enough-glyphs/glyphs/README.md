# Not Enough Glyphs 4.6.2 — Primitive Files

This directory contains one file for every primitive that NEG calls through `APIRegistry.registerSpell` under the current physical pack's loaded-mod conditions.

Current count: **40 registered**, of which **39 are source-enabled**; Momentum is source-disabled. The four real Ars Elemental primitives added only to NEG's internal listing are documented in `../DELEGATION-AND-DISABLED.md`, not duplicated here.

The remaining deployed-state gate is enumerated in [`../DEPLOYED-CONFIG-CHECKLIST.md`](../DEPLOYED-CONFIG-CHECKLIST.md): 39 source-enabled identities with their exact expected SERVER config paths, all kept `NÃO VERIFICADO` until authoritative pack/world config evidence is available.

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

O conjunto original de cartões usava o pin 4.6.1 `2f0c7b9...`; a matriz de registro foi revalidada para 4.6.2. **Oito fichas deste lote** usam diretamente o source 4.6.2 e corrigem divergências históricas de IDs/defaults. As demais permanecem em análise campo a campo; atributos herdados de Ars/Sauce não foram inferidos.

[Matriz de dossiês 8/40](../PERK-ENGINEERING-MATRIX-4.6.2.md).
