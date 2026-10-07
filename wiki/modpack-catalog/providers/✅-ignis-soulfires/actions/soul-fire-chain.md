# Soul-Fire Chain

- Provider: **Cataclysm: Ignis Soulfires** (`ignissoulfires`)
- Version: `1.8.0`
- Exact physical/publisher SHA-1: `a6f1c8cfe673aaff17f081ee9546e3600b4c72f1`
- Owner: `ignissoulfires:souled_gauntlet_of_bulwark`
- Trigger: shift-channel
- Exact action seam: `chainCooldown`, `chainRange`, `chainPullSpeed`, `chainHitDamage`, `chainHitKnockback`
- State: `COUNTED_EXACT`

## Semantic identity

The provider resolves the first eligible target along the look path, pulls it toward the user and settles the terminal hit/effects as one targeted control action. Pull, damage, Stun and Blazing Brand are stages of this same root.

## Exact acquisition

Exact `cataclysm:weapon_fusion` route from Cataclysm Gauntlet of Guard + provider Bulwark.

## Boundary

Ignis Soulfires remains authority for item/action definitions, cooldowns, provider config/state and settlement; L_Ender's Cataclysm remains authority for Cataclysm-owned base machinery such as `ChargeAttachment` and weapon fusion. Black Arcana catalogs the identity and must not replay the provider action or create a second cooldown/resource ledger.

Source: [`../EXACT-1.8.0-ARTIFACT-AUDIT.md`](../EXACT-1.8.0-ARTIFACT-AUDIT.md).
