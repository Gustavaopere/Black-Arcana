# Pull

- Registry ID: `ars_nouveau:glyph_pull`
- Source class: `EffectPull`
- School: Elemental Air
- Default tier: **1**
- Default mana: **15**
- Default entity velocity config: **1.0** base + **0.5** per amplification unit
- Exact source: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Source-pinned behavior

Pull moves entity targets toward the caster. On block targets it can convert harvestable blocks into Ars enchanted falling-block entities and give them motion relative to the hit face. Sensitive disables block pulling.

Compatible augments: Amplify, Dampen, AOE, Pierce, Sensitive. Sensitive is limited to 1 by default.

## Boundary

Ars owns Pull motion and block conversion. Black Arcana displacement remains server-owned and any block movement remains under `WorldEffectPolicy` and bounded work.

Status: `SOURCE-PINNED 5.13.1 / RUNTIME+CONFIG QA PENDING`.