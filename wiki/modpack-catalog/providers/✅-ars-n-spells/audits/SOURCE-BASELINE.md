# Source Baseline Notes — Ars 'n' Spells

This directory intentionally does **not** copy upstream source code. It records only the compatibility facts needed by the Black Arcana provider catalog.

Official source baseline used by Phase 2AG:

- repository: `otectus/ars-n-spells`;
- branch: `port/neoforge-1.21.1`;
- commit: `a9930223c96806e5d748ea69d02f9a32cab62de9`;
- declared mod version: `3.3.0`;
- Minecraft: `1.21.1`;
- NeoForge: `21.1.248`;
- Java toolchain: 21;
- Ars Nouveau target: `5.13.1.1400`;
- Iron's target: `1.21.1-3.16.3`.

The physical pack now runs 3.3.4. Exact public NeoForge source reaches 3.3.3 at `41fac17065c381104b17fdaab307d89ba21b49ab`. `RitualRegistryHandler.java` is blob `b25378e8a67ea084c77116bfe936f10512d3f691` at both this checkpoint and the 3.3.0 baseline; `ArsCrossProxyRegistry.java` is blob `f4e35f708aa41f7c4bf2599f2517429a4871f82b` at both; and the 3.3.3 source still declares `PROXY_POOL_SIZE = 8`. The exact 3.3.4 publisher delta is lifecycle/config/network/loot-oriented and does not announce registry identity additions/removals. Therefore the current semantic surface is `COUNTED_RELEASE_BOUNDED`, never mislabeled as exact 3.3.4 binary source.