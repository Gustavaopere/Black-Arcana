# Werewolves 2.0.3.3 — actions, forms and bite

Exact source pin: `TeamLapen/Werewolves@b72635b3e014e406b25bb79adb9d340f7443660b`.

## Registered actions — 9/9

| ID | Provider behavior | Default timing / gate | Integration notes |
|---|---|---|---|
| `human_form` | Activates `WerewolfForm.HUMAN`; provider applies human-form attributes and preserves health percentage across max-health changes | cooldown 0 s; unlocked by Human Form skill | transformed but human-like; does not consume transformation-time budget |
| `beast_form` | Activates `WerewolfForm.BEAST`; high armor/health/bite/damage form | cooldown 0 s | consumes daytime transformation time unless provider exemptions apply |
| `survival_form` | Activates `WerewolfForm.SURVIVALIST`; high mobility/defense form | cooldown 0 s | Climber can add step height +0.4 while active |
| `howling` | Applies Howling effect and, with Wolf Pack, summons temporary tamed aggressive wolves | cooldown 35 s | aura AABB source has a static anomaly; runtime radius QA required |
| `rage` | Lasting transformed-form action; adds bite damage and refreshes Strength/Speed | duration `(30 + 2*level)` s; cooldown 60 s | Beast gets stronger damage amp; Survivalist stronger speed amp |
| `sense` | Lasting action that activates client vision shader/outlining | duration 30 s; source cooldown arithmetic anomalous | actual renderer uses Vampirism blood-vision distance, not the exposed Werewolves sense-radius config in the inspected path |
| `fear` | Clears targets/navigation of nearby non-werewolf mobs and drives them away | cooldown 25 s; AABB 10×3×10 inflation | provider-native crowd control |
| `leap` | Arms a leap; next jump receives directional impulse; deactivates on fall | default cooldown 6 s; hidden from normal action selector | `no_leap_cooldown` refinement can make cooldown 0, but reachability is unproven |
| `hide_name` | Suppresses player name rendering while transformed through client event hook | default duration `Integer.MAX_VALUE` ticks; cooldown 1 s | UI/render effect, not invisibility or aggro suppression |

## Form registry

`WerewolfForm` contains five states:

| Form | Player-accessible via registered action? | Human-like | Transformed | Damage reduction | Leap modifier | Notes |
|---|---|---:|---:|---:|---:|---|
| `none` | state only | yes | no | 0 | 0 | base state |
| `human` | yes | yes | yes | 0.05 | 0.16 | 3 skin types |
| `beast` | yes | no | yes | 0.20 | 0.32 | 11 skin types |
| `beast4l` | no player action found | no | yes | 0.30 | 0.32 | Alpha Werewolf entity form; four-legged renderer |
| `survivalist` | yes | no | yes | 0.40 | 0.80 | 11 skin types |

Do not expose `beast4l` as an ordinary player perk without provider-native evidence that grants it.

## Transformation lifecycle

`WerewolfFormAction` owns the form transaction:

1. snapshot current health percentage;
2. deactivate any currently active Werewolf form action;
3. set provider form and synchronize it;
4. apply day/night form modifiers;
5. restore the same health percentage using the new max health;
6. refresh display name/dimensions and provider inventory/armor behavior.

Day/night modifiers are reconciled every 20 ticks while the form action is active.

### Transformation-time budget

The form action itself reports effectively unlimited duration, but transformed player forms use a separate normalized `transformationTime` state during daytime when outside the provider Werewolf biome.

Default configured form-time limit: **80 seconds**, further extended by form-duration refinements.

At night or inside the Werewolf Forest, normal form-time consumption is bypassed by `usesTransformationTime()`.

Beast Rage additionally stops Beast-form time consumption and forces night-strength modifiers while Rage + Beast Rage skill are active.

When no form is active, `transformationTime` regains over time using provider attribute `werewolves:time_regain`.

### Full moon

Full moon behavior is provider-enforced:

- without `free_will`, an untransformed werewolf can be forced into the last/unlocked form;
- an active form cannot simply be deactivated during full moon without `free_will`;
- full-moon transformation triggers provider advancement state.

Black Arcana must not bypass these rules by directly toggling model/form state.

## Form defaults

### Human Form

Default configured modifiers:

- armor +4 night; day factor 0.7;
- armor toughness +2 night; day factor 0.7;
- movement-speed form amount 0.05, with code baseline using 80% unless Speed skill grants full configured amount; day factor 0.5;
- food-consumption attribute +0.1 multiplied total;
- food-gain config 0.85, implemented as `0.85 - 1 = -0.15` multiplied total;
- does **not** consume transformation time.

### Beast Form

Defaults:

- bite damage +6;
- max health +8 night; day factor 0.5;
- armor +16 night; day factor 0.7;
- armor toughness +8 night; day factor 0.7;
- movement speed configured 0.15; baseline uses 80%, Speed skill gives full amount; day factor 0.5;
- attack damage configured +2; baseline uses 50%, Damage skill gives full amount; day factor 0.5;
- food-consumption +0.3 multiplied total;
- food-gain 0.70 -> -0.30 multiplied total.

### Survivalist Form

Defaults:

- bite damage +4;
- max health +4 night; day factor 0.5;
- armor +12.8 night; day factor 0.7;
- armor toughness +6 night; day factor 0.7;
- movement speed configured 0.5; baseline uses 80%, Speed skill gives full amount; day factor 0.6;
- attack damage configured +1.5; baseline uses 50%, Damage skill gives full amount; day factor 0.5;
- food-consumption +0.2 multiplied total; Efficient Diet reduces that provider amount;
- food-gain 0.77 -> -0.23 multiplied total;
- Climber: transient step-height +0.4 while active.

## Bite pipeline

The player bite is provider-owned and separate from the nine registered action IDs.

### Gates

A bite requires:

- Werewolf faction level >0;
- transformed form;
- not spectator;
- provider `biteTicks <= 0`;
- permission gate;
- target within player block-interaction range +1;
- player-target permission if applicable.

### Settlement

On a successful provider bite-damage hit:

1. damage amount is read from `werewolves:bite_damage`;
2. provider bite damage source is applied;
3. provider sounds play;
4. provider post-bite feeding hook runs;
5. `biteTicks` is set from `BALANCE.PLAYER.bite_cooldown` — default **200 ticks**;
6. in non-human-like forms, enabled bite skills may add STUN or BLEEDING;
7. bite state is synchronized;
8. provider may apply Lupus Sanguinem infection according to permissions/chance.

### Bite enhancements

- **Stun Bite:** STUN default 40 ticks; refinement can extend duration.
- **Bleeding Bite:** provider BLEEDING effect for configured duration; refinement changes amplifier from 0 to 3.
- **Rage:** adds provider bite-damage modifier +4 by default while active.

### Static config mismatch

There are two bite-cooldown config fields in the source. The actual inspected player `bite()` transaction uses `BALANCE.PLAYER.bite_cooldown` (default 200 ticks). A separate `BALANCE.SKILLS.bite_cooldown` default 5 seconds exists but was not consumed by that path. Treat the actual provider transaction as authority and runtime-test the effective cooldown.

## Fail-closed integration rule

Never synthesize a successful form/bite/action event from animation alone. For perks/quests, use a provider-confirmed causal event or validated state transition; do not award twice from both action activation and downstream damage/effect/world deltas.