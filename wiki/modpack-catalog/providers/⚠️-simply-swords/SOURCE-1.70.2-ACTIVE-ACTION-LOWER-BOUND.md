# Simply Swords 1.70.2 — exact-version active-action lower bound

Checkpoint: 2026-09-27

## Evidence class

`EXACT_PHYSICAL_IDENTITY / EXACT_VERSION_SOURCE / LOWER_BOUND 66 PLAYER_ACTIONS / NON_OPTED_LEGACY + DEPLOYED_REACHABILITY OPEN`

## Physical authority

Sibling physical row #503 at
`neoforge-rpg-skilltree@51d590653d927538f23ba6f1643576dc6cc49859`:

- JAR: `simplyswords-neoforge-1.70.2-1.21.1.jar`;
- mod id: `simplyswords`;
- runtime: `1.70.2-1.21.1`;
- SHA-1: `05b074ff774467f1fe9fb5592151b7845c321cbc`;
- sibling dossier publisher file: CurseForge `8746001`.

## Exact-version source pin

`Sweenus/SimplySwords@359a8031b1a3243d1a3b013dbaa0cbba70ea8278`

`gradle.properties` at this commit declares:

- Minecraft `1.21.1`;
- mod version `1.70.2-1.21.1`;
- Fabric and NeoForge enabled.

No source-build ↔ physical-JAR byte-equality claim is made.

## Unique ability registration chain

`SimplySwords.init()` calls `BuiltinUniqueAbilities.register()`.

That method registers its own definitions and then invokes:

- `Phase2UniqueAbilities.register()`;
- `Phase3UniqueAbilities.register()`;
- `Phase4UniqueAbilities.register()`;
- `Phase5UniqueAbilities.register()`;
- `Phase6UniqueAbilities.register()`;
- `Phase7UniqueAbilities.register()`;
- `Phase8UniqueAbilities.register()`;
- `Phase9UniqueAbilities.register()`;
- `Phase10UniqueAbilities.register()`.

The source defines **122 root definitions = 62 ACTIVE + 60 PASSIVE**.

The provider documentation describes each definition as an identifier plus active/passive kind, tuning keys and child lifecycle events. Child HIT/FINISH/event IDs are not separate roots.

## 62 ACTIVE root IDs

### Builtin — 2

1. `simplyswords:stormbreak`
2. `simplyswords:brimstone_rite`

### Phase 2 — 6

3. `simplyswords:watcher/final_omen`
4. `simplyswords:devourer/mass`
5. `simplyswords:wickpiercer/throw`
6. `simplyswords:gloampiercer/barrage`
7. `simplyswords:wraithfang/throw`
8. `simplyswords:wraithmaw/muster`

### Phase 3 — 7

9. `simplyswords:stormscale/lightning_rod`
10. `simplyswords:ionbound_stormscale/ion_crusher`
11. `simplyswords:ionbound_stormscale/paralysis_beam`
12. `simplyswords:soulrender/reaping`
13. `simplyswords:soulstalker/gloam_stride`
14. `simplyswords:whisperwind/petal_step`
15. `simplyswords:dreadwhisper/reaving_front`

### Phase 4 — 3

16. `simplyswords:awakened_lichblade/soul_anguish_channel`
17. `simplyswords:sunfire/radiant_standard`
18. `simplyswords:harbinger/gravity_standard`

### Phase 5 — 6

19. `simplyswords:hearthflame/furnace_chains`
20. `simplyswords:emberblade/ember_ire`
21. `simplyswords:emberlash/cauterizing_step`
22. `simplyswords:flamewind/flame_seed`
23. `simplyswords:molten_edge/vent`
24. `simplyswords:soulpyre/soul_tether`

### Phase 6 — 7

25. `simplyswords:stormbringer/shock_deflect`
26. `simplyswords:mjolnir/storm`
27. `simplyswords:thunderbrand/thunder_blitz`
28. `simplyswords:tempest/elemental_vortex`
29. `simplyswords:frostfall/frost_fury`
30. `simplyswords:icewhisper/comet_storm`
31. `simplyswords:livyatan/tempest_current`

### Phase 7 — 4

32. `simplyswords:bramblethorn/wild_grasp`
33. `simplyswords:waxweaver/waxweave`
34. `simplyswords:hiveheart/swarm`
35. `simplyswords:chompolotl/rally`

### Phase 8 — 7

36. `simplyswords:soulkeeper/lantern_conclave`
37. `simplyswords:soulstealer/stygian_approach`
38. `simplyswords:soulstealer/soul_reap`
39. `simplyswords:twisted_blade/finale`
40. `simplyswords:shadowsting/shadow_dance`
41. `simplyswords:shadowsting/veilstep`
42. `simplyswords:bloodwake/blood_rites`

### Phase 9 — 13

43. `simplyswords:arcanethyst/arcane_suspension`
44. `simplyswords:arcanethyst/amethyst_impact`
45. `simplyswords:stars_edge/constellation`
46. `simplyswords:magiscythe/storm_core`
47. `simplyswords:magiblade/warden_head`
48. `simplyswords:magiblade/sonic_judgment`
49. `simplyswords:magispear/spear_rain`
50. `simplyswords:magispear/magislam`
51. `simplyswords:enigma/stormchaser`
52. `simplyswords:enigma/vortex`
53. `simplyswords:caelestis/rift_host`
54. `simplyswords:caelestis/breach_maw`
55. `simplyswords:caelestis/unbound_pact`

### Phase 10 — 7

56. `simplyswords:watching_warglaive/nightwing_hunt`
57. `simplyswords:watching_warglaive/sanguine_watch`
58. `simplyswords:ribboncleaver/ribbon_rush`
59. `simplyswords:riftmane/vanguard_rank`
60. `simplyswords:riftmane/spectral_rider`
61. `simplyswords:dawnquiver/seraphs_draw`
62. `simplyswords:dreadtide/void_assault`

Subtotal: **62**.

## 60 PASSIVE definitions — excluded

The same registration chain contains **60 `PASSIVE` definitions**.

They are provider-owned behavior but remain outside the semantic-magic count because the current metric excludes passive gear/proc mechanics unless they form a discrete player-invoked action.

Subtotal contribution: **+0**.

## Runic/Gem Power classification

`GemPower` exposes separate hooks for:

- `postHit`;
- `onSwing`;
- `inventoryTick`;
- `use`;
- held-use ticks/release.

`GemPowerComponent.use(...)` delegates to registered powers, and `RunicSwordItem.use(...)` invokes that component path for player input.

At the exact-version source pin, four causal power families implement a real player `use(...)` action:

| Semantic root | Registry IDs | Evidence |
|---|---|---|
| Immolation | `simplyswords:immolation` | `ImmolationPower.use(...)` applies the active effect and cooldown |
| Momentum | `simplyswords:momentum`, `simplyswords:greater_momentum` | one shared `MomentumPower` action family; greater is a tier, not a second root |
| Throwing | `simplyswords:throwing` | `ThrowingPower.use(...)` launches the weapon entity |
| Ward | `simplyswords:ward` | `WardPower.use(...)` applies Ward and cooldown |

Subtotal: **4 semantic player actions**.

Other registered Gem Power implementations observed at this source pin use trigger/passive hooks such as `postHit`, `onSwing` or `inventoryTick` and are excluded from the current semantic count.

## Weapon implicit classification

`WeaponImplicitRegistry.registerBuiltins()` installs 17 built-in implicit identities:

- armor pierce / spear armor pierce;
- cutlass plunder;
- glaive bleed;
- backstab / dagger backstab;
- claymore / longsword deflect;
- greathammer / hammer sunder;
- katana double damage;
- chakram haste;
- scythe execute;
- greataxe / halberd bleed;
- twinblade haste;
- warglaive double strike.

`WeaponImplicitDefinition` exposes only damage-modification, on-hit and incoming-damage handlers.

These are equipment/proc identities, not player-invoked semantic actions.

Subtotal contribution: **+0**.

## Lower-bound arithmetic

`62 ACTIVE Unique roots + 4 player-use Runic roots = 66`.

## Why this remains a lower bound

The exact-version developer docs explicitly say:

- abilities can opt into the definition/modifier system;
- **existing abilities that do not opt in continue using the unchanged `UniqueWeaponActiveAbility` contract**.

Therefore the 62 active registered definitions do not prove completeness of all 1.70.2 player-invoked Unique actions.

The remaining closure work is:

1. enumerate legacy/non-opted `UniqueWeaponActiveAbility` actions;
2. reconcile any secondary-action inputs;
3. deduplicate them against the 62 registered active roots;
4. classify disabled/config-gated actions;
5. settle deployed Awakening/reachability where it changes the current active subset;
6. deduplicate addon-owned actions from the base provider.

## Reachability boundary

Normal `UniqueWeaponActiveAbility` player use checks `AwakeningApi.isAbilityUnlocked(stack)`.

Source identity therefore does not establish the deployed pack's currently reachable subset by itself.

The 1.70.x line is also config-breaking/save-sensitive. Effective pack config is required before strict promotion.

## Clean-room / license

Source license: **Timefall Development License 1.2**.

It permits library/integration use but forbids bundling/publishing/distributing copies outside the license's permissions. This audit retains factual metadata, IDs, API structure and behavior-level semantics only.

## Result

- exact physical identity: **closed**;
- exact-version source pin: **closed**;
- registered active Unique roots: **62**;
- player-use Runic action families: **4**;
- semantic lower bound: **66**;
- passive Unique definitions excluded: **60**;
- weapon implicits excluded: **17**;
- legacy/non-opted active-action denominator: **open**;
- deployed active reachability/config: **open**;
- strict contribution: **+0**;
- status: **⚠️**.
