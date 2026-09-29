# Mowzie's Mobs 1.8.2 — player magic/power inventory

Evidence basis: exact hash-matched current artifact plus bounded 1.8.2 public-source corroboration.

| Provider ability id | Semantic disposition | Strict count | Basis |
| --- | --- | ---: | --- |
| `sunstrike` | Heliomancy player power | 1 | active `PLAYER_ABILITIES` member; Sun's Blessing provider route |
| `solar_beam` | Heliomancy player power | 1 | active member; Sun's Blessing-gated player action |
| `solar_flare` | Heliomancy player power | 1 | active member; Sun's Blessing-gated player action |
| `supernova` | Heliomancy player power | 1 | active member; Sun's Blessing-gated player action |
| `wrought_axe_swing` | active provider weapon power | 1 | active member; exact `ItemWroughtAxe` trigger reference |
| `wrought_axe_slam` | active provider weapon power | 1 | active member; exact `ItemWroughtAxe` trigger reference |
| `ice_breath` | Ice player power | 1 | active member; exact `ItemIceCrystal` trigger; Frostmaw loot resource packaged |
| `spawn_boulder` | Geomancy — Boulder Lift | 1 | active member; provider presents the boulder raise/launch flow as one player action |
| `spawn_pillar` | Geomancy — Pillar Rise | 1 | active member; Earthrend/Geomancy eligibility path |
| `rock_sling` | Geomancy staff power | 1 | active member; exact `ItemSculptorStaff` trigger; Sculptor loot resource packaged |
| `tunneling` | Geomancy — Tunnel | 0 | active member but exact `canUse()` reads deployed `enableTunneling`; current value unavailable |
| `hit_boulder` | technical/subaction slot | 0 | exact trigger comes from `EntityBoulderProjectile`; part of Boulder Lift interaction, not a second independent player power |
| `backstab` | technical proc/animation slot | 0 | exact trigger comes from server backstab/critical path, not an independently invoked power |

**Strict counted total: 10.**

**Conditional total: 1 (`tunneling`).**

## Declared but inactive player-ability ids

The exact handler also declares four ids that are not present in `PLAYER_ABILITIES` and therefore contribute zero current semantic identities:

- `fireball`;
- `ground_slam`;
- `boulder_roll`;
- `fissure`.

## Deduplication note

`hit_boulder` is not a second Geomancy power. The provider's player-facing Boulder Lift flow raises a boulder and allows it to be struck/launched; the exact technical slot is the animation/settlement helper for that same action.

`backstab` is likewise not counted as a separate magical action because the gameplay trigger is the dagger's attack-from-behind proc; the exact ability slot is not a distinct player-selected power.
