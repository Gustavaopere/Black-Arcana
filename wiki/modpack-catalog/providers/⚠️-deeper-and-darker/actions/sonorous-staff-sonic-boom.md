# Sonorous Staff Sonic Boom

Status: `PUBLIC_SOURCE_BASELINE / PHYSICAL EXACTNESS OPEN / +0 STRICT`

- Provider: **Deeper and Darker** (`deeperdarker`)
- Version line: `1.4.1`
- Semantic owner: `deeperdarker:sonorous_staff`
- Public/source seam: `SonorousStaffItem.use(...)` + `SonorousStaffItem.releaseUsing(...)`
- Exact source pin: `KyaniteMods/DeeperAndDarker@f7ba235d078411a1165a8cac184adfe0ccc8cebe`
- Public publisher SHA-1: `b6094adde68bd4b909bc75c64901e1f3fb99ad8f`
- Current physical SHA-1: `83f7edd0a8516b2767c2cda7a3b2402f9e290d88`
- Semantic type: deliberate supernatural charged staff attack
- Current strict state: `OPEN_PHYSICAL_ARTIFACT / +0`

This card describes the **official/public 1.4.1 + exact-source baseline**. It is not projected onto the unmatched physical JAR.

## Item contract

Exact 1.4.1 registration defines:

- durability: **320**;
- rarity: **RARE**;
- repair item: `deeperdarker:soul_crystal`.

## Trigger and charge state

Ordinary item use starts the use/charge state. Releasing the use executes the sonic attack.

Exact source exposes:

- maximum use duration: **72,000 ticks**;
- `charged` presentation flag after **128 ticks** of continuous use.

The 128-tick value controls the charged presentation/foil state. `releaseUsing(...)` does not use it as an admission gate.

Let:

- `t` = ticks actually used before release;
- `V` = Volume enchantment level;
- `R` = Reverberation enchantment level.

## Exact baseline damage formula

Pre-distance damage:

`round(50 × (1 + V/4) / (1 + 16 / exp(0.06 × t)))`

Consequences directly implied by the formula:

- charge time increases damage toward its asymptote;
- Volume scales the numerator;
- asymptotic pre-distance damage approaches **50** at `V = 0`;
- asymptotic pre-distance damage approaches **100** at `V = 4`.

## Exact baseline range formula

Forward scan range:

`min(80, round(4.5 × (1 + 2R/3) × ln(t + 1)))`

- hard cap: **80 blocks**;
- Reverberation increases range;
- Reverberation remains a modifier of this action, not a second semantic identity.

## Propagation and targets

The provider scans forward from the player's eye position in one-block index steps.

For each step:

- the scan stops when the encountered block is non-air and can occlude;
- a per-step AABB is inflated by **0.4** blocks;
- living entities in that AABB are eligible;
- the caster is excluded;
- multiple living entities may be affected along the scan.

Distance-adjusted damage:

`round(baseDamage × (1 - (1/3) × (i/range)^2))`

where `i` is the current scan index.

The hit uses Minecraft's sonic-boom damage source with the player as source and applies directional push scaled by target knockback resistance.

## Settlement

Each executed release settles:

- Sonorous Staff durability damage: **1**;
- item-used statistic increment;
- provider staff sonic-boom sound;
- item cooldown: **20 ticks**.

## Public/source acquisition

Exact generated shaped recipe:

```text
 CH
 BC
B  
```

Ingredients:

- `H` = `deeperdarker:heart_of_the_deep`;
- `C` = `deeperdarker:soul_crystal`;
- `B` = `deeperdarker:sculk_bone`.

Result: **1 `deeperdarker:sonorous_staff`**.

This is baseline acquisition evidence only; exact physical reachability is not asserted while the installed JAR remains byte-different.

## Enchantment relationship

Volume and Reverberation modify this same action and do not create separate semantic roots.

Other Deeper and Darker enchantment effects such as Catalysis and Sculk Smite remain enchantment mechanics/modifiers, not standalone castable identities under the Black Arcana action metric.

## Evidence boundary

The public artifact and exact source pin mutually support this action family and its formulas. The current physical JAR does not hash-match the public artifact or clean source build.

Therefore:

- public/source baseline: **present**;
- exact-current physical action: **not proven**;
- strict semantic contribution: **+0**;
- provider remains **⚠️ partial**.

Sources inside this provider folder: `../PUBLIC-1.4.1-BASELINE-AUDIT.md`, `PUBLIC-BASELINE-ACTIONS.md`.
