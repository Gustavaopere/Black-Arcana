# Bloodlines 3.0.9 — provider audit

Status: `SOURCE-PINNED 3.0.9 / GRANULAR SOURCE CATALOG COMPLETE / RUNTIME QA + INSTALLED-ADDON INTEROP PENDING`

## Version authority

- mod id: `bloodlines`
- installed JAR: `bloodlines-1.21-3.0.9.jar`
- runtime/version: `1.21-3.0.9`
- Minecraft: `1.21.1`
- loader: NeoForge
- required base provider: Vampirism `1.10.13`
- official source: `TheDrOfDoctoring/bloodlines`
- exact source pin: `c8fd517d204d09dfcb9a544c17d7df87755eaa5c`

This pin is the mechanical authority for the installed 3.0.9 line. Public prose and later commits are not promoted over the exact source when they disagree with it.

## Provider role in the pack

Bloodlines is a structural Vampirism addon. It does not introduce a separate magic engine; it adds a second identity/progression layer to Vampire/Hunter players while reusing Vampirism registries and handlers for skills, skill trees, actions and tasks.

The installed build registers five Bloodlines:

| Bloodline | Base faction | Skill tree |
|---|---|---|
| Noble | Vampire | `bloodlines:vampire/noble` |
| Zealot | Vampire | `bloodlines:vampire/zealot` |
| Ectotherm | Vampire | `bloodlines:vampire/ectotherm` |
| Bloodknight | Vampire | `bloodlines:vampire/bloodknight` |
| Gravebound | Hunter | `bloodlines:hunter/gravebound` |

The custom Bloodline registry is synchronized and uses `bloodlines:empty` as its default key.

## Source-level inventory closed

| Surface | Confirmed count |
|---|---:|
| Bloodlines | **5** |
| Vampire Bloodlines | **4** |
| Hunter Bloodlines | **1** |
| Bloodline skill trees | **5** |
| `ISkill` registrations | **101** |
| Noble skills | **19** |
| Zealot skills | **19** |
| Ectotherm skills | **19** |
| Bloodknight skills | **20** |
| Gravebound skills | **24** |
| `IAction` registrations | **29** |
| Semantic player actions normally reachable under the current provider tree | **28** |
| Registered-but-not-normally-reachable action | **1** — Sorcerous Strike |
| Rank tasks | **15** |
| Bloodline-perk tasks | **7** |
| Total Bloodlines task keys | **22** |
| Bloodline ranks | **4 per Bloodline** |
| Own mob effects audited in core | **4** (`blood_frenzy`, `heinous_curse`, `cold_blooded`, `soul_rending`) |

## Provider-native authority

### Identity, rank and state

`BloodlineManager` is a serialized NeoForge Player attachment with `copyOnDeath()` and is authoritative for:

- current Bloodline;
- rank 0–4;
- Bloodline perk-point wallet;
- charged enabled-Bloodline-skill count;
- optional Bloodline-specific state;
- persistence and synchronization.

Changing/removing Bloodline also disables previous Bloodline skills through Vampirism's `SkillHandler`, clears Bloodline points/state, recalculates skill-tree locks and refreshes attributes. Black Arcana must not replace this lifecycle with a scoreboard/tag/NBT shadow copy.

### Rank

Rank and perk points are separate systems. `BloodlineParentSkill` represents the Rank 1–4 milestones without charging Bloodline perk points. Ranks 2–4 settle through `BloodlineRankReward`; the normal reward path requires `currentRank == targetRank - 1` and therefore does not support silent rank skipping.

### Bloodline perk wallet

Persistent fields:

- `blSkillPoints` — task points;
- `blOtherSkillPoints` — other authorized points;
- `blEnabledSkills` — charged enabled skills.

`remaining = max(0, taskSkillPoints + otherSkillPoints - enabledSkills)`.

### Skills

Bloodline skills are registered in Vampirism's skill registry and remain subject to Vampirism tree topology/parents/sibling locks plus Bloodlines-specific point/rank/default-skill gates injected into `SkillHandler`.

### Actions

All 29 Bloodlines actions are registered in Vampirism's action registry. Vampirism's `IActionHandler` remains the timer/activation lifecycle authority, with Bloodlines extending behavior through its action classes and `ActionHandler` mixin.

One registered action, Sorcerous Strike, is excluded from the current semantic player-action count because its corresponding skill node is not connected to the exact generated Gravebound configured tree and is not present in any of the four Gravebound rank-default skill lists. No dedicated provider-native alternate grant for that skill is present in the exact source pin. Generic perk tasks and the Bloodline perk command add points, not Sorcerous Strike itself. This is a normal-provider survival reachability classification; operator commands or externally modified datapacks are outside that scope.

## Source findings that remain runtime-QA gates

1. **Bloodline points vs normal Vampirism points:** Bloodlines adds its own point gate but some Bloodline skills still expose ordinary `getSkillPointCost()` values. Runtime behavior must be verified before any payment/respec bridge.
2. **Own wallet charges one enabled skill**, even when a skill exposes cost 2–3 on the Vampirism side.
3. **Repeating perk tasks:** reward settlement resets unique tasks. Gravebound caps task-derived Bloodline points at 15 through three `MaxPerkUnlocker` ranges; the other four Bloodlines have no analogous source cap.
4. **`MaxPerkUnlocker.CODEC` min/max naming is inverted** in its getter mapping.
5. **Ectotherm cross-reference:** `BloodlineFrost.onCrit` tests `ZEALOT_POISONED_STRIKE`.
6. **Shadowwalk distance mismatch:** Bloodlines defines its own max-distance config, but the audited action uses Vampirism Teleport distance.
7. **Bloodknight upkeep mismatch:** Sanguine Infusion, Blood Hunt and Daywalker debit 2 blood per interval while config comments describe one.
8. **Sorcerous Strike reachability — CLOSED FOR SEMANTIC COUNT:** registry/node/action/config exist, but the exact configured Gravebound tree omits the node and rank defaults grant only `gravebound`, `gravebound_rank_2`, `gravebound_rank_3` and `gravebound_rank_4`; no dedicated normal-provider alternate grant was found. The action is therefore registered but not normally survival-reachable in the exact 3.0.9 build and contributes zero semantic objects.
9. **Sorcerous Strike Wither mismatch:** specific config default is 8 s, while the hit hook uses the general action duration, 10 s by default.
10. **Devour Soul success semantics:** an invalid LivingEntity target can cause the action method to return success without a completed devour.
11. **Mist Form strict Soul threshold:** deactivation-resurrection requires `souls > requiredSouls`; exactly the configured cost enters the death path.
12. **Wall Climb client-side movement:** vertical velocity is modified on the client path and therefore needs dedicated-server QA.
13. **Heinous Elixir documentation drift:** exact 3.0.9 source config default is **15 seconds**, while public prose describing 30 seconds is stale/inconsistent for this build.

None of these findings is silently patched by the catalog.

## Joining/leaving confirmed

- **Noble:** Vampire without Bloodline, configured minimum Lord rank, weakened Vampire Baron under the configured health threshold, Lordslayer Injection.
- **Zealot:** Vampire without Bloodline, Zealot Ritual Catalyst + Zealot Altar; 700-tick ritual, join at remaining tick 50, abort if player is missing/dead.
- **Ectotherm:** Vampire without Bloodline under `Cold Blooded`, in water, receiving lethal Vampirism sun damage; lethal event is canceled and Ectotherm is granted.
- **Bloodknight:** Vampire without Bloodline surviving through the end of `Heinous Curse`; exact source default Heinous Elixir duration is **15 s**.
- **Gravebound:** Hunter without Bloodline under `Soul Rending` + `Heinous Curse`, lethal hit, nearby unowned Phylactery; join binds ownership and initializes 10 Souls.
- **Leaving:** Purity Injection is handled through a mixin into Vampirism's **Med Chair**, invoking full Bloodline lifecycle cleanup rather than a generic item-use path.

Changing/losing the base Vampirism faction also clears Bloodline state through the provider event lifecycle.

## Resource authority

Three resource domains are deliberately distinct:

1. **Vampirism blood/saturation/exhaustion** — base-provider authority;
2. **Bloodline perk points** — Bloodlines wallet;
3. **Gravebound Souls + Phylactery storage/state** — Bloodlines authority.

They must not be collapsed into a generic Black Arcana resource by naming similarity.

## Documents

- [`BLOODLINE-CATALOG.md`](./BLOODLINE-CATALOG.md): five Bloodlines, identity, joins, innate mechanics and state.
- [`SKILL-CATALOG.md`](./SKILL-CATALOG.md): 101/101 skills, costs/gates, sibling choices and tree topology.
- [`ACTION-CATALOG.md`](./ACTION-CATALOG.md): 29/29 actions, defaults, settlement semantics and static discrepancies.
- [`PROGRESSION-AND-TASKS.md`](./PROGRESSION-AND-TASKS.md): ranks, 22 tasks, rewards, repeatability and perk wallet.
- [`RESOURCE-AUTHORITY.md`](./RESOURCE-AUTHORITY.md): Vampirism blood vs Bloodline points vs Gravebound Souls/Phylactery.
- [`TECHNICAL-AUDIT.md`](./TECHNICAL-AUDIT.md): registry/attachment lifecycle, events, mixins, authority boundaries and QA matrix.
- [`INTEGRATION-RULES.md`](./INTEGRATION-RULES.md): Black Arcana ↔ Bloodlines/Vampirism provider-native-first contract.

## Closure state

The **granular source catalog is complete** for the exact installed Bloodlines 3.0.9 build: registries, Bloodlines, skills/trees, actions, tasks/progression, joining/leaving, resource authority, persistent state, high-impact mixins/events and Black Arcana integration constraints are documented.

For the semantic denominator, the build contributes **28 normally reachable provider-owned supernatural actions**. Sorcerous Strike remains implemented and registered but is excluded because the exact normal Gravebound tree/default progression does not provide a normal acquisition path.

This does **not** grant `RUNTIME QA CONFIRMED`.

Runtime validation is still required for the known discrepancies, dedicated-server movement/network behavior, task/point settlement, Blood/Gravebound resource conservation, Mist Form/Possession and exact interop with the installed Vampirism/addon stack.

Vampire Spells Addon 0.0.9 has now been source-cataloged separately on the same catalog branch; Bloodlines must still be runtime-tested together with that addon before any cross-addon behavior is promoted from fail-closed.