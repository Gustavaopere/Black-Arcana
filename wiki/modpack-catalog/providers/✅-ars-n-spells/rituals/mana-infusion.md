# Mana Infusion

Registry identity at the official NeoForge 1.21.1 source baseline: `ars_n_spells:mana_infusion`.

## Evidence status

- Physical provider: Ars 'n' Spells `3.3.2`.
- Implementation evidence: official NeoForge `3.3.0` source pin `a9930223c96806e5d748ea69d02f9a32cab62de9`.
- Exact 3.3.2 binary registry parity: `NÃO VERIFICADO`.

The 3.3.0 NeoForge registration handler registers this ritual when Iron's Spellbooks is loaded. Iron's is present in the current physical pack.

## Semantics

Mana Infusion is a one-shot ritual that resolves the provider's ritual recipient and grants a configured mana amount through `BridgeManager` rather than directly owning either host pool.

At the source baseline the mana grant therefore follows the active Ars 'n' Spells bridge routing rather than Black Arcana or the ritual itself becoming a separate mana authority.

This ritual uses the provider's one-shot `AnsRitual` lifecycle and its default **60 server-tick** completion interval.

## Deduplication boundary

Black Arcana must not mirror the grant into a second pool, independently choose which host pool receives it, or award a second grant after observing provider completion.

The configured amount, active routing mode and settlement remain provider-owned. If an exact 3.3.2 integration hook is needed, it remains fail-closed until that hook is verified on the installed artifact.