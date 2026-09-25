# Dynamic RPG Resource Bars 0.7.1 — presentation surface

## Evidence boundary

Physical provider:

- `dynamic_resource_bars-neoforge-0.7.1-1.21.1.jar`;
- mod id `dynamic_resource_bars`;
- runtime `0.7.1`;
- physical SHA-1 `08512179fdd92b1be480ad16535b036bd30f2d7d`.

Exact publisher release:

- CurseForge project `1188180`;
- file `6964564`;
- NeoForge 1.21.1;
- Release;
- uploaded 2025-09-05.

Current official source repository:

`muon-rw/Dynamic-Resource-Bars`

The source repository currently targets a later Minecraft line, so it is not used as byte-exact 0.7.1 authority.

## Presentation capabilities

Provider-owned capabilities are presentation/UI surfaces:

| Surface | Provider role | Semantic magic disposition |
|---|---|---:|
| health bar | display synced health state | +0 |
| mana bar | display external provider mana | +0 |
| stamina bar | display external stamina when supported | +0 |
| air/armor bars | display vanilla state | +0 |
| absorption/status overlays | presentation | +0 |
| mount-health substitution | presentation | +0 |
| HUD editor | client layout/configuration | +0 |
| animated sprites | presentation | +0 |
| resource-pack customization | presentation | +0 |
| AppleSkin/Farmer's Delight overlays | presentation integration | +0 |

## Resource ownership

The mod can visually integrate with Ars Nouveau and Iron's Spells.

That integration does not transfer ownership of:

- mana values;
- mana consumption;
- mana regeneration;
- spell casting;
- cooldowns;
- spell identity;
- progression.

The HUD observes/presents provider state.

## Semantic exclusion

Do not count as semantic magic objects:

- a mana bar;
- a stamina bar;
- bar animations;
- overlay layers;
- HUD editor actions;
- resource-pack sprites;
- visual interpolation;
- provider-selection logic.

## Strict result

- spells: 0;
- glyphs/spell-parts: 0;
- rituals/rites: 0;
- equivalent discrete magic actions: 0.

Strict semantic delta: **+0**.

Status: **✅ zero-semantic HUD/presentation closure**.
