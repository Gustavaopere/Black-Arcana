# Simply Swords 1.70.2 — release-correlated active-action lower bound

> **Superseded denominator state — 2026-09-29:** this file preserves the release-correlated source inventory that originally established `LOWER_BOUND 66`. Exact hash-matched artifact audit PR #448 / run `36524073819` subsequently closed the residual legacy/secondary action surface with **0 additional roots**, so the current provider denominator is **EXACT 66**. See [`EXACT-1.70.2-ARTIFACT-ACTION-AUDIT.md`](EXACT-1.70.2-ARTIFACT-ACTION-AUDIT.md). Deployed reachability remains open and strict contribution remains +0.

Checkpoint: 2026-09-27

## Evidence class

`HISTORICAL RELEASE_CORRELATED_SOURCE / ORIGINAL LOWER_BOUND 66 PLAYER_ACTIONS / SUPERSEDED BY EXACT HASH-MATCHED DENOMINATOR 66 / DEPLOYED REACHABILITY OPEN`

## Physical authority

Sibling physical row #503 at
`neoforge-rpg-skilltree@51751e6c77530a7d8825ec42493ffccedf978d1a`:

- JAR: `simplyswords-neoforge-1.70.2-1.21.1.jar`;
- mod id: `simplyswords`;
- runtime: `1.70.2-1.21.1`;
- SHA-1: `05b074ff774467f1fe9fb5592151b7845c321cbc`;
- sibling dossier publisher file: CurseForge `8746001`.

Publisher file:
`https://www.curseforge.com/minecraft/mc-mods/simply-swords/files/8746001`

The publisher changelog names:

- Epic Fight crash fix;
- Lootr loot-injection/pity fix;
- Simplified Chinese localization update.

## Release-correlated source chain

Primary checkpoint:

`Sweenus/SimplySwords@c82eeaf4479543a728340b9763ab445c9c9d4c0d`

This is the source commit whose message is the Epic Fight crash fix explicitly named in the 1.70.2 publisher changelog.

Its history already contains:

- `91edb6eb3a2f58def74fac5b035a8bc21df1fdbf` — Lootr injection/pity fix;
- the Simplified Chinese localization update/merge.

Therefore `c82eeaf...` is used as the primary **release-correlated content checkpoint**.

Later same-day cross-check:

`Sweenus/SimplySwords@359a8031b1a3243d1a3b013dbaa0cbba70ea8278`

At that revision `gradle.properties` declares:

- Minecraft `1.21.1`;
- mod version `1.70.2-1.21.1`;
- NeoForge enabled.

The later checkpoint retains the exact same 62 ACTIVE root IDs and the same four player-use Runic action families. It adds one passive companion definition only.

No source checkpoint is asserted to be byte-identical to the CurseForge JAR.

## Unique ability registration chain

At the primary release-correlated checkpoint, `SimplySwords.init()` calls `BuiltinUniqueAbilities.register()`.

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

At `c82eeaf...` the source defines **121 roots = 62 ACTIVE + 59 PASSIVE**.

At `359a8031...`, the ACTIVE set remains exactly **62** while PASSIVE becomes 60.

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

## PASSIVE definitions — excluded

The primary release-correlated checkpoint contains **59 PASSIVE definitions**.

The later version-declared cross-check contains **60**, due to one additional passive companion definition.

The semantic-magic metric excludes these passive gear/proc identities unless they form a distinct player-invoked action.

Contribution: **+0**.

## Runic/Gem Power classification

`GemPower` exposes separate hooks for:

- `postHit`;
- `onSwing`;
- `inventoryTick`;
- `use`;
- held-use ticks/release.

At `c82eeaf...`, `GemPowerComponent.use(...)` delegates to the selected power and `RunicSwordItem.use(...)` invokes that path from player input.

Four causal power families implement a real player `use(...)` action:

| Semantic root | Registry IDs | Evidence |
|---|---|---|
| Immolation | `simplyswords:immolation` | active `ImmolationPower.use(...)` |
| Momentum | `simplyswords:momentum`, `simplyswords:greater_momentum` | one shared `MomentumPower` action family; greater is a tier |
| Throwing | `simplyswords:throwing` | active `ThrowingPower.use(...)` |
| Ward | `simplyswords:ward` | active `WardPower.use(...)` |

Subtotal: **4 semantic player actions**.

Other power implementations use trigger/passive hooks such as `postHit`, `onSwing` or `inventoryTick` and are excluded from the current semantic count.

## Weapon implicit classification

At `c82eeaf...`, `WeaponImplicitRegistry.registerBuiltins()` installs **17** built-in implicit identities.

`WeaponImplicitDefinition` exposes only:

- damage modification;
- on-hit handling;
- incoming-damage cancellation.

These are equipment/proc identities, not player-invoked semantic actions.

Contribution: **+0**.

## Lower-bound arithmetic

`62 ACTIVE Unique roots + 4 player-use Runic roots = 66`.

## Why this source-only checkpoint was a lower bound

The release-line developer docs explicitly say that abilities may opt into the modifier-definition system while **existing abilities that do not opt in continue using the unchanged `UniqueWeaponActiveAbility` contract**.

At the source-only checkpoint, that meant the 62 registered active definitions could not prove completeness of all 1.70.2 player-invoked Unique actions.

That historical denominator blocker is now closed by exact hash-matched artifact audit PR #448 / run `36524073819`: the residual registered action-shaped surface is limited to two Secondary continuations and two direct-use pass-through overrides, all deduplicated at **+0 additional roots**. The current denominator is therefore **EXACT 66**.

Only deployed reachability remains open: Awakening/unlock state, acquisition/reformation, effective config/datapack/script suppression, compat-dependent materialization and final addon ownership reconciliation.

## Reachability boundary

Normal `UniqueWeaponActiveAbility` player use checks `AwakeningApi.isAbilityUnlocked(stack)`.

Release-line identity therefore does not establish the deployed pack's currently reachable subset by itself.

The 1.70.x line is also config-breaking/save-sensitive. Effective pack config is required before strict promotion.

## Clean-room / license

Source license: **Timefall Development License 1.2**.

It permits library/integration use but forbids bundling/publishing/distributing copies outside the license's permissions. This audit retains factual metadata, IDs, API structure and behavior-level semantics only.

## Result

- exact physical identity: **closed**;
- primary release-correlated source checkpoint: **closed**;
- later version-declared source cross-check: **closed**;
- registered active Unique roots: **62**;
- player-use Runic action families: **4**;
- original source-only semantic lower bound: **66**;
- PASSIVE definitions excluded: **59 at release-correlated checkpoint / 60 at later cross-check**;
- weapon implicits excluded: **17**;
- legacy/non-opted active-action denominator: **historical blocker; closed by exact artifact audit PR #448 / run `36524073819` with +0 additional roots**;
- current exact action denominator: **66**;
- deployed active reachability/config: **open**;
- strict contribution: **+0**;
- status: **⚠️**.