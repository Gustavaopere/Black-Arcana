# Spell Uninscription

Registry identity at the official NeoForge 1.21.1 source baseline: `ars_n_spells:spell_uninscription`.

## Evidence status

- Physical provider: Ars 'n' Spells `3.3.2`.
- Exact current release delta: 3.3.2.
- Implementation evidence: official NeoForge `3.3.0` source pin `a9930223c96806e5d748ea69d02f9a32cab62de9`.
- Exact 3.3.2 binary registry parity: `NÃO VERIFICADO`.

The 3.3.0 NeoForge `RitualRegistryHandler` registers this ritual unconditionally, including when Iron's Spellbooks is absent.

## Semantics

At the source baseline the ritual cleans one supported ANS-inscribed item. It validates the nearby item set before mutation, rejects ambiguous source/blank combinations, and requires exactly one inscribed target.

The provider cleanup path removes Ars 'n' Spells-owned cross-cast state and reconciles provider-owned native proxy entries rather than treating unrelated/native spells as ANS state.

Baseline search radius: **3 blocks** around the brazier.

This is a one-shot `AnsRitual` at the source baseline. The shared one-shot lifecycle finishes after the provider's default **60 server ticks** unless overridden; this ritual does not override that duration in the audited source.

## Deduplication boundary

Black Arcana must not independently strip Ars 'n' Spells carrier components/proxy entries or create its own cleanup format. If Black Arcana ever exposes an integration action for this lifecycle, provider-native cleanup is authoritative.

Do not infer that every arbitrary item with Ars/Iron's data is a valid uninscription target. Eligibility remains provider-owned.