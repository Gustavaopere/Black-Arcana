# 00 — Foundation

Establish a reproducible NeoForge 1.21.1 / Java 21 project before any gameplay work.

## Tasks

1. `01-scaffold-ci.md` — Gradle/NeoForge scaffold, CI and dedicated-server smoke baseline.
2. `02-clean-room-provenance.md` — provenance rules and reference evidence format.
3. `03-domain-contracts.md` — core boundaries/interfaces that later stages consume.
4. `04-config-data-contracts.md` — configuration ownership, codecs/data formats and migration rules.

## Exit criteria

Build and tests run in CI; dedicated server can boot; provenance rules are documented; the initial domain API compiles and is tested; configuration/data ownership is explicit. Only then may Stage 01 begin implementation work.
