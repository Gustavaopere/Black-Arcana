# Capability Matrix Delta — Dynamic RPG Resource Bars 0.7.1

Status: `✅ CLIENT HUD / RESOURCE PRESENTATION / +0 SEMANTIC MAGIC ACTIONS`

| Capability | Authority | Black Arcana consequence |
|---|---|---|
| health display | Dynamic Resource Bars presentation; Minecraft health state | never treat visual change as health mutation |
| Ars mana display | HUD presentation; Ars Nouveau owns mana | no second mana ledger |
| Iron's mana display | HUD presentation; Iron's owns mana | no second mana ledger |
| stamina display | HUD presentation; installed stamina provider owns value | do not infer provider or mutation |
| food/saturation overlays | presentation over provider state | no resource settlement |
| mount health | client display substitution | entity health remains server-owned |
| HUD editor | client config | no gameplay authority |
| resource-pack sprites | presentation assets | no semantic identity |

## Semantic boundary

Dynamic RPG Resource Bars owns no spell, glyph, ritual or equivalent action registry.

Strict semantic delta: **+0**.

## Runtime boundary

Provider-selection, overlay composition, client config, reload and visual lifecycle remain UI/runtime QA.
