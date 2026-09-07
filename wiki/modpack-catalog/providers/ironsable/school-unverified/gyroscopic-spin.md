# Gyroscopic Spin

- ID: `ironsable:gyroscopic_spin` — observed in pack runtime logs.
- Provider: IronSable `1.2.0`.
- School: **NÃO VERIFICADO**.
- Levels / rarity: **NÃO VERIFICADO**.
- Cast/channel: channel-dependent behavior confirmed; exact cast type/ticks **NÃO VERIFICADO**.
- Mana / cooldown / damage: **NÃO VERIFICADO**.
- Range / rotation speed formula / caps: **NÃO VERIFICADO**.

## Contract

Official behavior: rotates a ship in place without translating it. Holding/channeling longer makes it spin faster; aiming left or right of the ship center selects rotation direction.

The public description establishes orientation-sensitive directional control and channel scaling, but not the exact angular velocity function or target/ownership rules.

## Acquisition

Same Iron's loot ecosystem; Scroll Forge craftable; every level in IronSable creative tab. Exact loot/crafting values: **NÃO VERIFICADO**.

## Dedup / authority

Rotation is provider-owned. A bridge must not also write yaw/angular velocity after IronSable handles the ship.

## Fail-closed

Do not approximate with teleport/position rotation or client-only visual rotation.

## Evidence state

Exact 1.2.0 release + runtime ID + official semantic contract; school/stats/bytecode pending.