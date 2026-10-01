# Artifacts 13.2.5 — current item/ability surface

Status: `49/49 ITEM ENTRIES RECONCILED / BASE ITEM EFFECTS CATALOGED / +0 INDEPENDENT SEMANTIC MAGIC IDENTITIES`

This file closes the current Artifacts item denominator without converting item containers, attributes, passive effects or data-component implementation types into standalone spell identities.

## Non-wearable / utility — 4

| Item | Current provider surface | Semantic disposition |
|---|---|---|
| `mimic_spawn_egg` | provider Mimic spawn item | item/entity materialization; `EXCLUDED` |
| `umbrella` | dedicated utility item behavior | item behavior; `EXCLUDED` |
| `everlasting_beef` | reusable food with provider cooldown/state | consumable behavior; `EXCLUDED` |
| `eternal_steak` | reusable food with provider cooldown/state | consumable behavior; `EXCLUDED` |

## Head — 8

| Item | Base Artifacts behavior family | Semantic disposition |
|---|---|---|
| `plastic_drinking_hat` | eating/drinking-speed modifiers | gear attribute; `EXCLUDED` |
| `novelty_drinking_hat` | eating/drinking-speed modifiers + provider lore component | gear attribute/presentation; `EXCLUDED` |
| `snorkel` | conditional water-breathing equipment effect | gear effect; `EXCLUDED` |
| `night_vision_goggles` | night-vision equipment effect with toggle state | gear/toggle state; `EXCLUDED` |
| `villager_hat` | villager-reputation modifier | gear attribute; `EXCLUDED` |
| `superstitious_hat` | looting modifier | gear attribute; `EXCLUDED` |
| `cowboy_hat` | mount-speed modifier | gear attribute; `EXCLUDED` |
| `anglers_hat` | fishing enchantment modifiers | gear/enchantment modifier; `EXCLUDED` |

## Necklace — 9

| Item | Base Artifacts behavior family | Semantic disposition |
|---|---|---|
| `lucky_scarf` | fortune modifier | gear/enchantment modifier; `EXCLUDED` |
| `scarf_of_invisibility` | invisibility equipment state + toggle/hide helpers | gear/toggle/effect; `EXCLUDED` |
| `cross_necklace` | invulnerability-window modifier + post-damage cooldown | gear defensive effect; `EXCLUDED` |
| `panic_necklace` | post-damage movement effect + cooldown | reactive gear proc; `EXCLUDED` |
| `shock_pendant` | lightning retaliation + configured immunity branch | reactive gear proc; `EXCLUDED` |
| `flame_pendant` | fire retaliation / fire-related defensive behavior | reactive gear proc; `EXCLUDED` |
| `thorn_pendant` | thorns retaliation with provider chance/cooldown state | reactive gear proc; `EXCLUDED` |
| `charm_of_sinking` | sinking/underwater behavior + toggle + defensive component | movement/gear state; `EXCLUDED` |
| `charm_of_shrinking` | scale modifier + toggle | gear attribute/toggle; `EXCLUDED` |

## Belt — 8

| Item | Base Artifacts behavior family | Semantic disposition |
|---|---|---|
| `cloud_in_a_bottle` | `DOUBLE_JUMP` component | item-granted movement ability, no independent action ID; `EXCLUDED` |
| `obsidian_skull` | post-fire-damage defensive effect + cooldown | reactive gear proc; `EXCLUDED` |
| `antidote_vessel` | `CURE_EFFECTS` component | automatic gear effect; `EXCLUDED` |
| `universal_attractor` | magnetism equipment behavior + toggle | gear/toggle state; `EXCLUDED` |
| `crystal_heart` | maximum-health modifier | gear attribute; `EXCLUDED` |
| `helium_flamingo` | `SWIM_IN_AIR` movement component | item-granted movement ability, no independent action ID; `EXCLUDED` |
| `chorus_totem` | `DEATH_PROTECTION_TELEPORT` component | reactive death-protection gear effect; `EXCLUDED` |
| `warp_drive` | Ender Pearl hunger-cost / damage-immunity components | modifies an existing vanilla item action; `EXCLUDED` |

## Hands — 10

| Item | Base Artifacts behavior family | Semantic disposition |
|---|---|---|
| `digging_claws` | break-speed + `TOOL_TIER_UPGRADE` | gear/tool modifier; `EXCLUDED` |
| `feral_claws` | attack-speed modifier | gear attribute; `EXCLUDED` |
| `power_glove` | attack-damage modifier | gear attribute; `EXCLUDED` |
| `fire_gauntlet` | attack burning-duration behavior | on-hit gear effect; `EXCLUDED` |
| `pocket_piston` | attack-knockback modifier | gear attribute; `EXCLUDED` |
| `vampiric_glove` | `DAMAGE_ABSORPTION` / lifesteal-like settlement | on-hit gear proc; `EXCLUDED` |
| `golden_hook` | entity-experience modifier | gear attribute/economy effect; `EXCLUDED` |
| `onion_ring` | post-eating effect | consumable/equipped proc; `EXCLUDED` |
| `pickaxe_heater` | auto-smelt behavior | tool/drop transformation; `EXCLUDED` |
| `withered_bracelet` | `ATTACK_EFFECTS` provider effect | on-hit gear proc; `EXCLUDED` |

## Feet — 9

| Item | Base Artifacts behavior family | Semantic disposition |
|---|---|---|
| `aqua_dashers` | `FLUID_COLLISION` movement surface | equipment movement behavior; `EXCLUDED` |
| `bunny_hoppers` | jump/safe-fall modifiers + hurt sound | equipment movement attributes; `EXCLUDED` |
| `kitty_slippers` | creeper/phantom repellents + hurt sound | passive equipment behavior; `EXCLUDED` |
| `running_shoes` | sprint-speed / step-height modifiers | gear attributes; `EXCLUDED` |
| `snowshoes` | powder-snow traversal + snow movement behavior | passive movement gear; `EXCLUDED` |
| `steadfast_spikes` | knockback/slip resistance | gear attributes; `EXCLUDED` |
| `flippers` | swim-speed modifier | gear attribute; `EXCLUDED` |
| `rooted_boots` | hunger-on-grass + post-eating plant growth | passive/reactive gear behavior; `EXCLUDED` |
| `strider_shoes` | lava `FLUID_COLLISION` + hot-floor immunity behavior | passive movement/defense gear; `EXCLUDED` |

## Generic Curio — 1

| Item | Base Artifacts behavior family | Semantic disposition |
|---|---|---|
| `whoopee_cushion` | provider flatulence/chance + sound behavior | novelty gear effect; `EXCLUDED` |

## Deduplication against Reliquified Artifacts

The current pack's Reliquified Artifacts 1.0.8 catalog already closes **48 Artifact owners / 52 owner-scoped named Relics ability roots**. Those roots are the discrete supernatural identities counted in the semantic ledger.

This base-provider inventory therefore records Artifacts ownership and behavior without adding a second semantic identity for:

- the item container;
- an attribute modifier;
- a data-component implementation class;
- an automatic proc;
- a toggle bit;
- the same owner later extended by a Reliquified named ability.

## Result

- current item denominator: **49/49**;
- current base item/effect surface: cataloged;
- independent spell/glyph/ritual/action-ID roster: **0**;
- strict semantic contribution: **+0**.
