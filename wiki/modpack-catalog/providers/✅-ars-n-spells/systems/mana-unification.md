# Mana Unification

## Evidence boundary

This page preserves the detailed Ars 'n' Spells NeoForge 1.21.1 **3.3.0 source baseline** at `otectus/ars-n-spells@a9930223c96806e5d748ea69d02f9a32cab62de9`, with later release boundaries layered on top. The physical pack now runs `ars_n_spells-3.3.4.jar`; public source reaches 3.3.3, while 3.3.4 payment ownership is publisher-release-bounded.

Exact 3.3.4 internal routing/payment signatures are not claimed without binary/source parity evidence.

## Five provider-owned modes

The NeoForge baseline defines:

| Mode | Config name | Baseline role |
|---|---|---|
| `ISS_PRIMARY` | `iss_primary` | Iron's pool is primary |
| `ARS_PRIMARY` | `ars_primary` | Ars pool is primary |
| `HYBRID` | `hybrid` | provider-defined shared/unified pool behavior |
| `SEPARATE` | `separate` | separate pools with provider-defined dual-cost handling |
| `DISABLED` | `disabled` | no mana unification |

At the source baseline `ISS_PRIMARY`, `ARS_PRIMARY` and `HYBRID` are classified by the provider as shared-pool modes. `SEPARATE` is the dual-cost mode.

## Settlement authority

The official NeoForge 3.3.0 release commit documents major correctness hardening around cross-cast cost settlement:

- cost quotes are repeatable and are not charged during quote calculation;
- a cast uses one immutable quote and commits it once at the native payment boundary;
- carrier type determines book-versus-scroll billing semantics instead of trusting serialized cast-source metadata;
- cross-casting reports the real delegated Ars resolver result;
- routing state is published as one provider snapshot rather than independently drifting mode fields.

These are provider contracts, not Black Arcana algorithms to reproduce.

## Black Arcana boundary

Black Arcana must not create:

- another generic Ars↔Iron's combined mana pool;
- another conversion ratio ledger for the same casts;
- another dual-cost debit in `SEPARATE` mode;
- an independent refund after the provider has committed;
- a second max-mana synchronization path;
- a UI-derived assumption about which pool is authoritative.

For a cast routed by Ars 'n' Spells, resource facts must come from an explicit verified provider boundary or from the provider's settled outcome. Similar-looking mana values are not permission to recompute the transaction.

Black Arcana's own Corruption, Strain and Arcane Danger remain separate channels and must never be collapsed into Ars 'n' Spells mana.
## Current 3.3.4 payment boundary

The exact 3.3.4 publisher release states that native cast payment ownership is consolidated at the final host cast lifecycle, with replaced native debit suppressed, final cost listeners running once, shared effect/channel/scroll/cooldown lifecycle, and measured debit/refund recovery. Black Arcana must therefore treat provider payment settlement as authoritative and must not re-debit Ars/Iron's resources for the same routed cast. Exact internal hook signatures remain fail-closed.
