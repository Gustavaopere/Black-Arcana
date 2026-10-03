# Pufferfish's Unofficial Additions 2.2.8 — exact extension surface

Status: `ZERO_SEMANTIC_SKILL_XP_REWARD_BRIDGE`

| Surface | Exact role | Semantic disposition |
|---|---|---|
| `pufferfish_unofficial_additions:harvest_crops` | experience source from crop harvest context | Progression XP source — `+0` |
| `pufferfish_unofficial_additions:fishing` | experience source from fishing result context | Progression XP source — `+0` |
| `pufferfish_unofficial_additions:spell_casting` | experience source observing an existing Iron's cast | Bridge over external spell identity — `+0` |
| `pufferfish_unofficial_additions:effect` | configurable reward for mob-effect grant/immunity/modification | Data-driven reward factory, no fixed action identity — `+0` |
| spell/school conditions | filters existing Iron's holders | Compatibility/filter infrastructure — `+0` |
| calculation prototypes | expose player/item/spell/school/cast parameters | Calculation infrastructure — `+0` |
| `walk_on_powder_snow` tag hook | allows powder-snow walking when progression state/tag is present | Passive state consequence — `+0` |

## Ownership rule

An Iron's spell observed by `spell_casting` remains owned by Iron's or the addon that registered that spell. A configured mob effect used by the `effect` reward remains a reward parameter, not a new provider spell.

## Packaged-content result

- provider-owned concrete skill-tree JSONs: **0**;
- provider-owned discrete supernatural player-action identities: **0**;
- strict semantic contribution: **+0**.
