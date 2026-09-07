# Kinetic Barrier

- ID: `ironsable:kinetic_barrier` — observed in pack runtime logs.
- Provider: IronSable `1.2.0`.
- School: **NÃO VERIFICADO**.
- Levels / rarity: **NÃO VERIFICADO**.
- Cast/channel timing: **NÃO VERIFICADO**.
- Mana / cooldown / damage: **NÃO VERIFICADO**.
- Barrier radius / force / duration / caps: **NÃO VERIFICADO**.

## Contract

Official behavior: raises a force sphere around the ship the caster is standing on and pushes away anything that drifts too close. The spell **only works while the caster is aboard a ship**.

The aboard-ship gate is part of spell identity. It must not be weakened into a generic player-centered knockback aura.

## Acquisition

Same Iron's loot ecosystem; Scroll Forge craftable; every level in IronSable creative tab. Exact values: **NÃO VERIFICADO**.

## Dedup / authority

Barrier admission and ship/object repulsion are provider-owned. Do not add an independent radial force layer.

## Fail-closed

If ship membership/ownership cannot be resolved through exact provider/Sable hooks, fail closed instead of treating nearby vanilla entities as equivalent ships.

## Evidence state

Exact release + runtime ID + official semantic contract; school/stats/bytecode pending.