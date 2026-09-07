# Apprentice's Codex 0.9.7.1 — Lightning

Exact source pin: `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`.

Exact registry count: **10/10**.

| ID | Name | Max level | Min rarity | Cooldown | Cast |
|---|---|---:|---|---:|---|
| `apprenticecodex:sky_edge` | Sky Edge | 5 | Rare | 8 s | Long |
| `apprenticecodex:commence_fire` | Commence Fire | 5 | Uncommon | 12 s | Long + recast |
| `apprenticecodex:quick_arms` | Quick Arms | 5 | Common | 8 s | Instant + recast |
| `apprenticecodex:breaching_enemy` | Breaching Enemy | 5 | Rare | 12 s | Long |
| `apprenticecodex:bullet_stream` | Bullet Stream | 3 | Epic | 12 s | Continuous |
| `apprenticecodex:fly_swatter` | Fly Swatter | 3 | Epic | 12 s | Continuous lock-on |
| `apprenticecodex:shock` | Shock | 10 | Common | 1 s | Instant |
| `apprenticecodex:dual_acrobat` | Dual Acrobat | 5 | Uncommon | 12 s | Continuous |
| `apprenticecodex:field_overseer` | Field Overseer | 5 | Uncommon | 30 s | Long + recast lifecycle |
| `apprenticecodex:shiden` | Shiden | 5 | Rare | 10 s | Long |

All ten use Iron's canonical Lightning school and Iron's mana.

## Capability summary

- **Sky Edge** — delayed multi-projectile weapon volley aimed toward line of sight.
- **Commence Fire** — summoned DMR-like rifle with a bounded recast/fire count and headshot scaling.
- **Quick Arms** — short-lived summoned handgun with repeated recasts.
- **Breaching Enemy** — short-range 12-pellet magical shotgun with strong knockback semantics.
- **Bullet Stream** — fixed-duration minigun channel after a spin-up, firing every server tick.
- **Fly Swatter** — continuous target-lock acquisition followed by homing explosive attacks.
- **Shock** — low-cooldown direct lightning hit with assisted targeting.
- **Dual Acrobat** — continuous dual-SMG barrage.
- **Field Overseer** — persistent temporary placed staff with internal mana, owner-mana transfer and multi-target lightning strikes.
- **Shiden** — charged katana rising slash with reduced damage through block obstruction.

Several spells use provider-owned multi-hit/recast/autonomous-entity causal chains. A future Black Arcana/RPG observer must deduplicate one player intent from its child shots, recasts and summoned entities rather than treating every callback as a new cast.