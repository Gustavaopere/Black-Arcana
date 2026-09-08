# Explosion

- Registry ID: `ars_nouveau:glyph_explosion`
- Source class: `EffectExplosion`
- School: Elemental Fire
- Default tier: **2**
- Default mana: **200**
- Default source config: intensity **0.75**, amplification intensity **0.5**, AOE intensity **1.5**, damage **6.0**, damage per Amplify **2.5**
- Exact source: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Source-pinned behavior

Creates Ars Nouveau's custom explosion at the resolved position. AOE raises blast size without directly raising the configured damage term; Amplify affects size and damage; Dampen reduces size/damage. Extract changes block interaction from decay-style destruction to full-destroy/drop behavior. NeoForge's explosion-start hook can veto execution.

Compatible augments: Amplify, Dampen, AOE, Extract. Amplify is limited to 2 by default.

## Boundary

This is a destructive provider-native capability. Black Arcana must never route its own explosions through this as a way around `WorldEffectPolicy`; its destructive effects remain independently budgeted and policy-controlled.

Status: `SOURCE-PINNED 5.13.1 / HIGH-RISK WORLD EFFECT / RUNTIME+CONFIG QA PENDING`.