# Maelstrom

- ID: `ironsable:maelstrom` — observed in pack runtime logs.
- Provider: IronSable `1.2.0`.
- School: Wind **conditional contract active** because Wind's Spellbooks `1.0.5` is installed.
- Levels / rarity: **NÃO VERIFICADO**.
- Cast type / cast time / channel timing: **NÃO VERIFICADO**.
- Mana / cooldown: **NÃO VERIFICADO**.
- Damage / damage type: **NÃO VERIFICADO**.
- Range / radius / duration / formulas / caps: **NÃO VERIFICADO**.

## Contract

Official 1.2.0 behavior: pulls nearby mobs and airships toward the caster.

Exact target eligibility, friendly-fire rules, self-ship behavior, mass scaling, force magnitude, falloff and server tick cadence are not established by public metadata and remain **NÃO VERIFICADO**.

## Acquisition

Official provider rule: same loot ecosystem as Iron's Spells, craftable at the Scroll Forge, and present in the IronSable creative tab at every level. Exact weights/costs: **NÃO VERIFICADO**.

## Dedup / authority

IronSable owns the ship-physics pull. Do not supplement it with a generic velocity pull or a second Sable force. Mob pull behavior is provider-owned as well unless an integration hook explicitly delegates it.

## Fail-closed

If the exact IronSable physics path cannot be invoked/observed, do not approximate ship pulling with entity knockback/teleport.

## Evidence state

Exact release `ironsable-1.2.0.jar` / CurseForge file `8598255`; runtime ID observed locally; semantic contract from official provider page; bytecode not extracted.