# Downburst

- ID: `ironsable:downburst` — observed in pack runtime logs.
- Provider: IronSable `1.2.0`.
- School: Wind **conditional contract active** because Wind's Spellbooks `1.0.5` is installed.
- Levels / rarity: **NÃO VERIFICADO**.
- Cast type: charge-up behavior confirmed qualitatively; exact type/ticks **NÃO VERIFICADO**.
- Mana / cooldown: **NÃO VERIFICADO**.
- Damage / damage type: **NÃO VERIFICADO**.
- Mark radius / vertical reach / force / duration / caps: **NÃO VERIFICADO**.

## Contract

Official 1.2.0 behavior: charges, marks the ground and then slams every ship above the marked point straight downward. It is explicitly described as working on ships hovering high above the point, and **the caster's own ship is not spared**.

That self-ship behavior is part of the provider contract and must not be silently filtered out by a bridge.

## Acquisition

Same Iron's loot ecosystem; Scroll Forge craftable; all levels in IronSable creative tab. Exact values: **NÃO VERIFICADO**.

## Dedup / authority

The downward ship impulse is IronSable-owned. Apply at most once per eligible ship/cast.

## Fail-closed

Do not replace with entity knockback, block teleport or a second downward velocity injection if IronSable is present.

## Evidence state

Exact release `1.2.0`; runtime ID observed; public semantic contract; numerical/runtime internals pending.