# Bloodlines 3.0.9 — skill catalog

Source authority: `TheDrOfDoctoring/bloodlines@c8fd517d204d09dfcb9a544c17d7df87755eaa5c`.

## Registry model

Bloodlines registers **101 `ISkill` entries** into the Vampirism skill registry. They are not a parallel skill engine.

Distribution:

| Tree | Registry entries |
|---|---:|
| Noble | **19** |
| Zealot | **19** |
| Ectotherm | **19** |
| Bloodknight | **20** |
| Gravebound | **24** |
| **Total** | **101** |

Each bloodline has:

- rank-1 root `BloodlineParentSkill`;
- rank-2/3/4 `BloodlineParentSkill`s;
- normal `BloodlineSkill`s;
- optional `BloodlineActionSkill`s that expose registered Vampirism actions.

`BloodlineParentSkill` has `requiresBloodlineSkillPoints=false`. Other Bloodline skills normally have that flag true unless explicitly constructed otherwise.

## Cost/gate semantics

There are two different values in source:

1. **Bloodline wallet gate** — boolean `requiresBloodlineSkillPoints()`; Bloodlines requires at least one remaining own Bloodline point and increments `blEnabledSkills` by one on enable.
2. **Base skill cost** — inherited `getSkillPointCost()` used by Vampirism's normal `SkillHandler.canSkillBeEnabled`.

Because Bloodlines does not replace the base `canSkillBeEnabled` implementation, a skill with base cost >0 can statically appear to require both an own Bloodline point and enough regular Vampirism skill points. The provider README says Bloodline perk points are used *instead of regular skill points*. This mismatch is a runtime QA gate; do not repair it externally.

## Default/rank skills

By default each bloodline config automatically grants only its root and rank parents:

- Rank 1: bloodline root;
- Rank 2: corresponding `_rank_2`;
- Rank 3: corresponding `_rank_3`;
- Rank 4: corresponding `_rank_4`.

`defaultNotManuallyUnlockable=true` blocks manual unlock of those configured defaults through a Bloodlines mixin.

Gravebound additionally auto-manages Mist Form when the configured immortality rank is reached; default rank is 3.

## Noble — 19

Root/ranks, own Bloodline cost **no**:

- `noble` — Rank 1 root;
- `noble_rank_2`;
- `noble_rank_3`;
- `noble_rank_4`.

Own Bloodline point **yes**, base cost 0 unless noted:

- `noble_better_prices` — required Bloodline rank 2;
- `noble_better_blood_drain`;
- `noble_faster_resurrect`;
- `noble_more_ticks_in_sun` — base cost **1**;
- `noble_bat_flying_speed` — base cost **1**;
- `noble_faster_movement_speed`;
- `noble_bottomless_chalice`;
- `noble_enhanced_leeching`;
- `noble_intrigue`;
- `noble_celerity` — action skill;
- `noble_mesmerise` — action skill;
- `noble_leeching` — action skill;
- `noble_invisibility` — action skill;
- `noble_flank` — action skill;
- `noble_bat_armour`.

### Configured tree topology

Root branches:

- Better Trade Prices;
- Rank 2 trunk;
- More Ticks in Sun;
- Better Blood Drain.

Rank 2 trunk branches to:

- Faster Movement → Celerity;
- Rank 3;
- Leeching → Enhanced Leeching.

Rank 3 branches to:

- Mesmerise;
- Intrigue → Flank;
- Rank 4 → Bat Flight Speed → Bat Armour, and Bottomless Chalice;
- Faster Resurrect;
- Invisibility.

## Zealot — 19

Root/ranks, own Bloodline cost **no**:

- `zealot`;
- `zealot_rank_2`;
- `zealot_rank_3`;
- `zealot_rank_4`.

`zealot_poisoned_strike` is also explicitly constructed with `requiresBloodlineSkillPoints=false` and base cost 0; it shares a node with Frenzy.

Own Bloodline point **yes** unless stated:

- `zealot_stone_speed` — base cost 0;
- `zealot_darkcloak` — action, base cost **1**;
- `zealot_shadowwalk` — action, base cost **2**;
- `zealot_wall_climb` — action, base cost 0;
- `zealot_fall_damage`;
- `zealot_flesh_eating`;
- `zealot_tunneler`;
- `zealot_spider_friend` — base cost **1**;
- `zealot_shadow_mastery`;
- `zealot_swift_sneak`;
- `zealot_obscured_power` — base cost **1**;
- `zealot_hex_protection` — base cost **1**;
- `zealot_frenzy` — action, base cost 0;
- `zealot_shadow_armour`.

### Multi-skill/sibling-choice nodes

- `zealot_flesh_shadow_armour`: **Flesh Eating OR Shadow Armour**;
- `zealot_frenzy`: **Frenzy OR Poisoned Strike**.

These are actual single `SkillNode`s with multiple skills. Vampirism's handler returns `OTHER_NODE_SKILL` after one option is enabled.

### Configured tree topology

Root branches:

- Stone Speed → Tunneler;
- Rank 2 trunk;
- Spider Friend → Swift Sneak.

Rank 2 branches:

- Shadowwalk;
- Rank 3;
- Flesh Eating/Shadow Armour choice → Hex Protection.

Rank 3 branches:

- Dark Cloak;
- Rank 4 → Shadow Mastery → Obscured Power;
- Fall Damage → Wall Climb → Frenzy/Poisoned Strike choice.

## Ectotherm — 19

Root/ranks, own Bloodline cost **no**:

- `ectotherm` — Rank 1 root; enables Vampirism water resistance through toggle action;
- `ectotherm_rank_2` — also exposes Lord of Frost action;
- `ectotherm_rank_3`;
- `ectotherm_rank_4`.

Own Bloodline point **yes**, base cost 0:

- `ectotherm_fishmonger`;
- `ectotherm_refraction`;
- `ectotherm_diffusion`;
- `ectotherm_tentacles`;
- `ectotherm_icelord`;
- `ectotherm_frost_control`;
- `ectotherm_mining_speed_underwater`;
- `ectotherm_frozen_attack`;
- `ectotherm_slowness_attack`;
- `ectotherm_dolphin_leap` — action;
- `ectotherm_snow_walker`;
- `ectotherm_lord_of_frost_multiplier`;
- `ectotherm_underwater_duration`;
- `ectotherm_hydrodynamic_form`;
- `ectotherm_ink_splash` — action.

### Multi-skill node

`ectotherm_frozen_slowness`: **Frozen Attack OR Slowness Attack**.

### Configured tree topology

Root branches:

- Snow Walker;
- Rank 2 trunk;
- Underwater Mining Speed;
- Dolphin Leap.

Rank 2 branches:

- Refraction → Diffusion;
- Rank 3;
- Ice Lord → Frost Control;
- Fishmonger.

Rank 3 branches:

- Frozen/Slowness choice;
- Rank 4 → Frost Duration → Underwater Duration, and Ink Splash → Hydrodynamic Form;
- Tentacles.

## Bloodknight — 20

Root/ranks, own Bloodline cost **no**:

- `bloodknight`;
- `bloodknight_rank_2`;
- `bloodknight_rank_3`;
- `bloodknight_rank_4`.

Own Bloodline point **yes**, base cost 0 unless noted:

- `bloodknight_still_water` — required rank 3;
- `bloodknight_feigned_mercy`;
- `bloodknight_feeding_frenzy_1`;
- `bloodknight_feeding_frenzy_2`;
- `bloodknight_crimson_leap` — action;
- `bloodknight_sanguine_infusion` — action;
- `bloodknight_blood_hunt` — action;
- `bloodknight_vampire_blood_bonus`;
- `bloodknight_infusion_haste`;
- `bloodknight_infusion_step_assist`;
- `bloodknight_sapping_strike`;
- `bloodknight_day_walker` — action, base cost **2**, required rank 4;
- `bloodknight_bat_frenzy`;
- `bloodknight_blood_extraction` — action;
- `bloodknight_frenzied_attacks`;
- `bloodknight_hidden_strike`.

### Multi-skill node

`bloodknight_haste_step_infusion`: **Infusion Haste OR Infusion Step Assist**.

### Configured tree topology

Root has two major branches.

Feeding branch:

`Feeding Frenzy I → Feigned Mercy → Feeding Frenzy II → Still Blood`.

Rank branch:

`Rank 2` splits to:

- `Crimson Leap → Vampire Blood Bonus → Blood Extraction → Daywalker`;
- `Rank 3`, which splits to:
  - `Sanguine Infusion → Haste/Step Assist choice → Bat Frenzy`;
  - `Rank 4 → Blood Hunt → Sapping Strike → Hidden Strike → Frenzied Attacks`.

## Gravebound — 24

Root/ranks, own Bloodline cost **no**:

- `gravebound` — Rank 1 root; directly exposes Devour Soul action;
- `gravebound_rank_2`;
- `gravebound_rank_3`;
- `gravebound_rank_4`.

Other non-wallet/default exception:

- `gravebound_mist_form` — base cost 0, `requiresBloodlineSkillPoints=false`; exposes both Mist Form and Force End Mist Form actions and is auto-enabled/disabled by the provider's immortality-rank logic.

Own Bloodline point **yes** unless stated:

- `gravebound_soul_infusion` — action, base cost 0;
- `gravebound_regen_devour` — base cost 0;
- `gravebound_powerful_devour` — base cost 0;
- `gravebound_crit_ability` — Sorcerous Strike action, base cost 0, required rank 2;
- `gravebound_linger_devour` — action, base cost 0, required rank 2;
- `gravebound_soul_claim` — action, base cost 0, required rank 3;
- `gravebound_passive_soul_claim` — base cost **2**, required rank 4;
- `gravebound_teleport` — Phylactery Teleport action, base cost **2**, required rank 3;
- `gravebound_poison_immunity` — base cost 0;
- `gravebound_poison_healing` — base cost **1**, required rank 3;
- `gravebound_soul_transfer` — base cost **1**, required rank 2;
- `gravebound_ghost_walk` — action, base cost **3**, required rank 4;
- `gravebound_cheaper_resurrection` — base cost **1**;
- `gravebound_reduced_resurrection_cooldown` — base cost 0;
- `gravebound_phylactery_transfer` — action, base cost **1**, required rank 3;
- `gravebound_soul_speed` — base cost 0;
- `gravebound_undead_lord` — base cost **1**, required rank 2;
- `gravebound_possession_action` — action, base cost **1**, required rank 3;
- `gravebound_possession_swap_action` — action, base cost **1**, required rank 4.

### Configured tree topology

Four root branches:

1. `Soul Infusion → Regen Devour → Lingering Devour → Soul Claiming → Passive Soul Claiming`, with `Powerful Devour` branching from Regen Devour;
2. `Rank 2 → Rank 3 → Rank 4`;
3. `Poison Immunity`, splitting to:
   - Poison Healing;
   - Soul Transfer → Phylactery Transfer and Phylactery Teleport → Ghost Walk;
4. `Soul Speed → Undead Lord`, splitting to:
   - Possession → Possession Swap;
   - Cheaper Resurrection → Faster Resurrection.

## Gravebound survival-reachability discrepancy

`gravebound_crit_ability` / Sorcerous Strike is:

- registered as an `ISkill`;
- assigned a registered `ISkillNode` (`bloodlines:gravebound_sorcerous_strike`);
- connected to a registered `IAction`;
- given config defaults for action cooldown/duration/effect;
- **not present in the generated configured Gravebound tree**;
- **not included in any default rank-skill list**;
- not auto-enabled by `BloodlineGravebound.handleSpecialSkills`, which only handles Mist Form.

Therefore default 3.0.9 source provides no proven survival path to enable Sorcerous Strike. Treat it `REGISTERED / SURVIVAL REACHABILITY UNPROVEN-BLOCKED` until runtime/datapack inspection proves another path.

Mist Form is different: it is also absent from the configured tree, but provider code directly enables/disables it from the immortality-rank gate, so its reachability is proven.

## Topology authority

The generated `configured_skill_tree/*.json` files are canonical topology for the exact source pin. Registered nodes alone do not prove survival reachability. Black Arcana integrations must check actual unlocked tree/parent state and must not unlock a registered-but-unwired skill merely because its registry id exists.
