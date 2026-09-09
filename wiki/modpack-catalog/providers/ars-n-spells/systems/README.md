# Systems Index — Ars 'n' Spells 3.3.2

Physical provider: `ars_n_spells-3.3.2.jar`.

The current provider component is primarily a cross-engine bridge rather than an independent fixed-spell library. The core system pages are:

- [Mana Unification](mana-unification.md) — five provider-owned modes and resource-settlement authority;
- [Cross-Casting and Proxy Pool](cross-casting-and-proxy-pool.md) — delegated Ars casting through Iron's native wheel, with eight transport proxy slots and zero standalone semantic spells represented by those fixed ids;
- [Spell Loom and Carriers](spell-loom-and-carriers.md) — provider-owned serialization, inscription/export, carrier validation and cleanup lifecycle.

Implementation evidence for these internals is pinned to the official NeoForge 1.21.1 3.3.0 source baseline at `a9930223c96806e5d748ea69d02f9a32cab62de9`. Exact 3.3.2 internal parity remains `NÃO VERIFICADO` unless an exact release fact states otherwise.

Black Arcana does not duplicate these bridge runtimes. It keeps authority only over its own cast/hazard/world-safety systems and integrates through verified boundaries.