# Elastic Tether

**✅ Verificação física mais recente (2026-10-13):** `ironsable:elastic_tether` é registry estático do JAR físico/publicador 1.2.0 (SHA-1 `6ea9ce03144ec741a1e8d322f06985366d9ecc9e`), [Java 21 #38408009738](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38408009738) SUCCESS. **School default Ender** por `DefaultConfig.setSchoolResource` no bytecode. `COUNTED_EXACT` para identidade/escola de configuração default, **+0** raízes. As referências históricas abaixo de bytecode/escola não verificados foram superadas somente para symbols/IDs/default school. Config live, mana, cooldown, ship physics, Sable/Survival **⚠️ pendentes**. [Dossiê](../EXACT-BINARY-SPELLS-1.2.0.md).


- ID: `ironsable:elastic_tether` — observed in pack runtime logs.
- Provider: IronSable `1.2.0`.
- School (default verificado no JAR): **Ender**; a configuração realmente carregada no pack permanece ⚠️.
- Levels / rarity: **NÃO VERIFICADO**.
- Cast sequence: provider describes a three-cast setup; exact recast implementation/timing **NÃO VERIFICADO**.
- Mana / cooldown / damage: **NÃO VERIFICADO**.
- Range / tether force / duration / caps: **NÃO VERIFICADO**.

## Contract

Official behavior is an arcane tether established through three casts: mark one point, mark another, then the two anchors are hauled together until they touch. Terrain is immovable, so tethering a ship to terrain can lock it in place. Casting again snaps/breaks the tether.

The provider description makes anchor type matter: terrain is an immovable authority, not another movable physics body.

## Acquisition

Same Iron's loot ecosystem; Scroll Forge craftable; every level in IronSable creative tab. Exact values: **NÃO VERIFICADO**.

## Dedup / authority

Anchor recording, tether lifecycle, attraction and snap cleanup are IronSable-owned. Do not add a parallel pull constraint.

## Fail-closed

If either anchor cannot be resolved to the provider's exact world/sublevel frame, do not invent a global-coordinate tether.

## Evidence state

Exact release + runtime ID + official semantic contract; school/stats/API/bytecode pending.