# Incinerator Slam

- Provider: **Cataclysm: Ignis Soulfires** (`ignissoulfires`)
- Version: `1.8.0`
- Exact physical/publisher SHA-1: `a6f1c8cfe673aaff17f081ee9546e3600b4c72f1`
- Owner: `ignissoulfires:the_souled_incinerator`
- Trigger: non-shift release after the exact 60-tick charge threshold
- Exact action seam: `useIncineratorSlam(...)`, `spawnStrike(...)`, `slamCooldown`
- State: `COUNTED_EXACT`

## Semantic identity

The provider resolves one forward ground/strike sequence as a single causal slam. Individual spawned strikes are substeps, not independent semantic powers.

## Exact acquisition

Exact smithing-transform route from Cataclysm The Incinerator + Souled Ignitium materials/template.

## Boundary

Ignis Soulfires remains authority for item/action definitions, cooldowns, provider config/state and settlement; L_Ender's Cataclysm remains authority for Cataclysm-owned base machinery such as `ChargeAttachment` and weapon fusion. Black Arcana catalogs the identity and must not replay the provider action or create a second cooldown/resource ledger.

Source: [`../EXACT-1.8.0-ARTIFACT-AUDIT.md`](../EXACT-1.8.0-ARTIFACT-AUDIT.md).
