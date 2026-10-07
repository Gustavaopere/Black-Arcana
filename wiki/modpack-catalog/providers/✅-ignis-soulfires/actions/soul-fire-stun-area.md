# Soul-Fire Stun Area

- Provider: **Cataclysm: Ignis Soulfires** (`ignissoulfires`)
- Version: `1.8.0`
- Exact physical/publisher SHA-1: `a6f1c8cfe673aaff17f081ee9546e3600b4c72f1`
- Owner: `ignissoulfires:the_souled_immolator`
- Trigger: charged shift release
- Exact action seam: provider area cooldown/radius/stun-damage path
- State: `COUNTED_EXACT`

## Semantic identity

The provider resolves one soul-fire area-control action against eligible nearby entities. Per-target hits, Stun, Blazing Brand, VFX and screen shake are consequences of the single AoE root.

## Exact acquisition

Exact `cataclysm:weapon_fusion` route from Cataclysm The Immolator + Souled Ignitium Ingot.

## Boundary

Ignis Soulfires remains authority for item/action definitions, cooldowns, provider config/state and settlement; L_Ender's Cataclysm remains authority for Cataclysm-owned base machinery such as `ChargeAttachment` and weapon fusion. Black Arcana catalogs the identity and must not replay the provider action or create a second cooldown/resource ledger.

Source: [`../EXACT-1.8.0-ARTIFACT-AUDIT.md`](../EXACT-1.8.0-ARTIFACT-AUDIT.md).
