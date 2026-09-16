# Mana Well

Registry identity at the official NeoForge 1.21.1 source baseline: `ars_n_spells:mana_well`.

## Evidence status

- Physical provider: Ars 'n' Spells `3.3.2`.
- Implementation evidence: official NeoForge `3.3.0` source pin `a9930223c96806e5d748ea69d02f9a32cab62de9`.
- Exact 3.3.2 binary registry parity: `NÃO VERIFICADO`.

The 3.3.0 NeoForge registration handler registers this ritual when Iron's Spellbooks is loaded. Iron's is present in the current physical pack.

## Semantics

Mana Well is a continuous ritual. At the source baseline its server tick:

- reads the provider-configured range;
- builds a bounded area around the brazier;
- walks the current level's player list rather than scanning all entity sections;
- grants the configured regeneration rate to players whose bounding boxes intersect the ritual area;
- routes each grant through the active Ars 'n' Spells `BridgeManager`.

Unlike Spell Transcription, Spellbook Binding, Spell Uninscription and Mana Infusion, Mana Well does **not** extend the provider's one-shot `AnsRitual` base in the audited source. Therefore the 60-tick one-shot duration must not be applied to Mana Well.

Exact duration/termination/config defaults beyond what the current source explicitly exposes remain provider-owned and are not guessed here.

## Deduplication boundary

Black Arcana must not run a parallel per-tick mana aura for the same ritual, duplicate each routed mana grant, or globally scan entities/chunks to reproduce this provider behavior.

If Black Arcana observes the ritual for its own approved hazard/progression purposes, observation must remain causal and deduplicated; provider mana routing remains authoritative.