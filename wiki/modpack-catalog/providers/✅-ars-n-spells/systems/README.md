# Systems Index — Ars 'n' Spells 3.3.4

Physical provider: `ars_n_spells-3.3.4.jar` / runtime `3.3.4` / physical SHA-1 `53966330a468e626cd6469259af6778a5a7d9305`.

The current provider component is primarily a cross-engine bridge rather than an independent fixed-spell library. The core system pages are:

- [Mana Unification](mana-unification.md) — five provider-owned modes and resource-settlement authority;
- [Cross-Casting and Proxy Pool](cross-casting-and-proxy-pool.md) — delegated Ars casting through Iron's native wheel, with eight transport proxy slots and zero standalone semantic spells represented by those fixed ids;
- [Spell Loom and Carriers](spell-loom-and-carriers.md) — provider-owned serialization, inscription/export, carrier validation and cleanup lifecycle;
- [School, Progression and Equipment Bridge](school-progression-equipment.md) — provider-owned school resolution, affinity/progression/cooldown attribution, resonance/scaling boundary and equipment cross-feed.

Implementation details are evidence-layered: historical 3.3.0 source remains the baseline for claims not re-pinned later; exact public NeoForge source reaches 3.3.3 at `41fac17065c381104b17fdaab307d89ba21b49ab`; exact 3.3.4 publisher facts cover the current lifecycle/config/network/loot delta. Exact 3.3.4 internal parity remains `NÃO VERIFICADO` unless independently proven.

Black Arcana does not duplicate these bridge runtimes. It keeps authority only over its own cast/hazard/world-safety systems and integrates through verified boundaries.