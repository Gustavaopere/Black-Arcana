# Capability Matrix Delta — Ars 'n' Spells 3.3.2

Phase: **2AG**

Physical provider: `ars_n_spells-3.3.2.jar`.

Evidence model: exact 3.3.2 physical/release facts + official NeoForge 1.21.1 3.3.0 source baseline at `a9930223c96806e5d748ea69d02f9a32cab62de9`. Exact 3.3.2 binary internals remain fail-closed.

| Capability | Provider coverage | Black Arcana implication |
|---|---|---|
| Ars↔Iron's mana routing | Five provider modes: ISS-primary, Ars-primary, hybrid, separate/dual-cost, disabled | **Covered.** Do not create a second generic unified mana ledger. |
| Cross-engine cost settlement | Provider baseline quotes once and settles at native payment boundary using carrier-aware semantics | **Covered.** Do not double-debit/refund or recompute provider cost. |
| Ars spell in Iron's native wheel | Finite eight-slot `ars_cross_*` proxy pool delegates to serialized Ars payload | **Covered.** Proxy is transport identity, not a second spell/proc. |
| Ars spell serialization/carriers | Provider-owned cross-spell components + Spell Loom/export/transcription lifecycle | **Covered.** Do not invent a parallel serializer/universal spellbook for the same bridge. |
| Spell Transcription ritual | One source → one provider-approved carrier output with validation before mutation | **Covered.** No BA duplicate ritual required. |
| Spellbook Binding ritual | Carrier scroll → Iron's spellbook/native-wheel entry, bounded by provider proxy capacity | **Covered.** No BA native-wheel binding path. |
| Spell Uninscription ritual | Provider cleanup/reconciliation of ANS-owned inscription/proxy state | **Covered.** No BA direct foreign-container cleanup. |
| One-shot mana grant ritual | Mana Infusion routes configured grant through provider bridge | **Covered.** No duplicate grant or pool selection. |
| Area mana-regeneration ritual | Mana Well routes bounded-area player grants through provider bridge | **Covered.** No duplicate per-tick aura/global scan. |
| Cross-system school/progression/equipment interoperability | Provider project/source line owns shared progression/school/equipment bridge behavior | **Covered at provider level.** BA may observe only through verified boundaries; do not mirror calculations. |
| Eight `ars_cross_*` registry entries | Infrastructure slots, not eight semantic spells | **No new semantic gap.** Excluded from standalone spell count. |
| Transaction receipt HUD | Removed in exact 3.3.1 release | **Not current capability.** Do not catalog or integrate it as present. |
| Contextual Iron's mana HUD visibility | Exact 3.3.2 fixes full-value/XP-anchor visibility | Presentation-only provider behavior; no gameplay authority transfer. |

## Deduplication result

Ars 'n' Spells materially occupies the generic Ars Nouveau ↔ Iron's Spellbooks bridge niche for mana, carrier storage, native-wheel execution and related progression/school interoperability.

This pass does **not** identify a Black Arcana implementation gap requiring a competing universal mana bridge, universal external spellbook, proxy registry or inscription engine.

Black Arcana's own casting/hazard/runtime authority remains distinct. Corruption, Strain and Arcane Danger are not equivalent to Ars 'n' Spells mana/progression state.

## Phase 3 gate

No Phase 3 implementation is authorized by this delta alone. Provider cataloging/deduplication continues.