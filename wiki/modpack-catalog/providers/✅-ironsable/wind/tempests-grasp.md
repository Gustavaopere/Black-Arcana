# Tempest's Grasp

- ID: `ironsable:tempests_grasp` — observed in pack runtime logs.
- Provider: IronSable `1.2.0`.
- School: Wind **conditional contract active** because Wind's Spellbooks `1.0.5` is installed.
- Levels / rarity: **NÃO VERIFICADO**.
- Cast type / cast time / channel timing: **NÃO VERIFICADO**.
- Mana / cooldown: **NÃO VERIFICADO**.
- Damage / damage type: **NÃO VERIFICADO**.
- Range / duration / rotation rate / force / caps: **NÃO VERIFICADO**.

## Contract

Official 1.2.0 behavior: summons a tornado that drags and spins targeted ships toward the caster.

The provider page establishes combined translation + rotation of targeted ships, but not exact target acquisition, ownership/friendly-fire checks, mass limits or numerical force/rotation formulas.

## Acquisition

Same Iron's loot ecosystem; Scroll Forge craftable; IronSable creative tab exposes every level. Exact loot/crafting values: **NÃO VERIFICADO**.

## Dedup / authority

Ship drag and spin are one provider-native contract. Do not implement separate generic pull and rotation overlays that would stack with IronSable.

## Fail-closed

Do not substitute teleportation or vanilla entity velocity for the Sable ship transform/force path.

## Evidence state

Exact release `1.2.0`; runtime ID observed; official semantic contract; exact bytecode/API pending.