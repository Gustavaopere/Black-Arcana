# Werewolves 2.0.3.3 — progression

Exact source pin: `TeamLapen/Werewolves@b72635b3e014e406b25bb79adb9d340f7443660b`.

## Normal faction progression — levels 1–14

Werewolves registers `HIGHEST_WEREWOLF_LEVEL = 14` and delegates faction level state to Vampirism's `FactionPlayerHandler` while maintaining its own `LevelHandler.levelProgress` for the next-level ritual gate.

### Progress source

On a provider-confirmed entity kill, `WerewolfPlayer.onEntityKilled` adds:

`floor(victim.maxHealth × 0.2)`

to Werewolf `levelProgress`, then synchronizes that provider state.

This is not generic Minecraft XP and must not be substituted by Black Arcana XP.

### Level requirements

| Target level | Required provider progress | Liver | Cracked Bone |
|---:|---:|---:|---:|
| 2 | 50 | 3 | 2 |
| 3 | 75 | 4 | 3 |
| 4 | 100 | 5 | 4 |
| 5 | 125 | 6 | 5 |
| 6 | 150 | 7 | 6 |
| 7 | 175 | 8 | 7 |
| 8 | 200 | 9 | 8 |
| 9 | 225 | 10 | 9 |
| 10 | 250 | 11 | 10 |
| 11 | 275 | 12 | 11 |
| 12 | 300 | 13 | 12 |
| 13 | 325 | 14 | 13 |
| 14 | 350 | 15 | 14 |

## Stone Altar transaction

Normal level-up 2–14 is a provider-owned ritual transaction.

### Activation gates

- current player must be Werewolf faction;
- target level must be 2–14;
- at least four Stone Altar Fire Bowls must exist in the searched local structure and at least four must be lit;
- ritual can activate only at night;
- altar inventory must contain the target-level Liver and Cracked Bone requirements;
- Werewolf `LevelHandler.canLevelUp()` must be true.

### Settlement sequence

1. target player and target level are bound to altar state;
2. ritual enters `STARTING`, default 40 ticks;
3. required items are consumed **at ritual start**;
4. enters `FOG`, default 300 ticks;
5. ending transition applies Blindness and extinguishes altar lit state;
6. enters `ENDING`, default 90 ticks;
7. only on successful end does provider reset `levelProgress` and call `FactionPlayerHandler.setFactionLevel(WEREWOLF_FACTION, current+1)`.

Do not create a parallel settlement that charges items/progress again or awards the level before the provider transaction completes.

## Level-based attributes

`WerewolfPlayer.onLevelChanged` applies provider level-scaled modifiers for movement speed, armor toughness and attack damage.

Source-level anomaly in 2.0.3.3: the armor-toughness `LevelAttributeModifier` call uses `WerewolvesConfig.BALANCE.PLAYER.werewolf_speed_amount` rather than the separately declared `werewolf_armor_toughness` config. Runtime QA must establish the effective installed behavior; Black Arcana must not silently “correct” it.

At level <=0, provider action timers reset and all Werewolves skills are disabled.

## Lord progression — levels 1–5

`HIGHEST_WEREWOLF_LORD_LEVEL = 5`.

Lord levels are task-driven through Vampirism task/reward infrastructure, not Stone Altar `levelProgress`.

| Task | Unlock | Requirements | Reward |
|---|---|---|---|
| `werewolf_lord1` | normal Werewolf level 14 | 10 Vampires; 10 Hunters; 2 Werewolf Tooth; 32 Gold Ingots; 3 village-capture wins | Lord level 1 |
| `werewolf_lord2` | Lord 1 | 20 Vampires; 20 Hunters; 2 Tooth; 32 Gold Ingots | Lord level 2 |
| `werewolf_lord3` | Lord 2 | 20 Vampires; 20 Hunters; 3 Tooth; 32 Gold Ingots | Lord level 3 |
| `werewolf_lord4` | Lord 3 | 35 Vampires; 35 Hunters; 3 Tooth; 64 Gold Ingots | Lord level 4 |
| `werewolf_lord5` | Lord 4 | 50 Vampires; 50 Hunters; 4 Tooth; 64 Gold Ingots; capture-village stat 6 | Lord level 5 |

These requirements use provider/Vampirism tags and stats. Black Arcana should not assume that killing an arbitrary visually similar entity satisfies them.

## Additional provider tasks — 9

Beyond the five Lord-level tasks, Werewolves defines nine other tasks:

### Minion progression

- `werewolf_minion_binding`: Lord 1; 4 advanced Hunters, 6 advanced Vampires, 32 Gold Ingots → Werewolf Minion Charm.
- `werewolf_minion_upgrade_simple`: Lord 2; 6 advanced Hunters, 8 advanced Vampires, 16 Gold Blocks → simple upgrade item.
- `werewolf_minion_upgrade_enhanced`: Lord 3; 8 advanced Hunters, 10 advanced Vampires, 16 Liver, 1 Werewolf Tooth, 3 Diamond Blocks → enhanced upgrade.
- `werewolf_minion_upgrade_special`: Lord 5; 10 advanced Hunters, 12 advanced Vampires, 32 Liver, 5 Werewolf Tooth, 8 Diamond Blocks → special upgrade.

### Refinement/task rewards

- `random_refinement1`: 10 advanced Hunters + 2 Gold Ingots → random Werewolf refinement.
- `random_refinement2`: 3 Alpha Werewolves + 2 Gold Ingots → EPIC Werewolf refinement.
- `random_refinement3`: Villager trades stat 15 + 2 Gold Ingots → random Werewolf refinement.
- `random_rare_refinement`: Raid win 1 → RARE Werewolf refinement.

### Oblivion

- `oblivion_potion`: Poison Potion + Liver + Vampirism Human Heart → Vampirism Oblivion Potion.

This is a provider-to-host composition; Werewolves does not create a second Oblivion item authority.

## Infection / joining progression

Werewolf infection uses `Lupus Sanguinem` rather than direct Black Arcana progression:

- eligible target receives provider effect according to player/mob bite infection chance;
- effect is intentionally persistent until its resolution condition;
- on resolution for a player, it calls `FactionPlayerHandler.joinFaction(WEREWOLF_FACTION)`.

Player sleep/wake hooks cause the effect to resolve. Joining is therefore provider/Vampirism faction authority.

## Leaving / cure progression

Source-level cure path:

1. use Vampirism empty injection on a WerewolfBaseEntity;
2. provider consumes the empty injection and grants `INJECTION_UN_WEREWOLF`;
3. a current Werewolf uses it on Vampirism Med Chair;
4. provider applies `UN_WEREWOLF` for 2000 ticks and consumes the injection;
5. on the effect's final tick, provider calls `setFactionAndLevel(null, 0)`.

Do not shortcut this through a generic “remove curse” flag unless design explicitly intends to bypass provider progression and the integration contract approves it.

## World progression context

`werewolves:werewolf_heaven` is the registry key for the provider **Werewolf Forest** biome. Generated tags classify it as Overworld. Transformation-time rules also treat the provider Werewolf biome specially.

## Integration requirements

- provider progression is server-authoritative;
- award external quest/perk credit only after causal provider confirmation;
- Stone Altar item consumption and faction-level settlement must be deduplicated;
- Lord task kills/stats must use the same provider identities/tags or verified equivalent events;
- leaving/joining events should invalidate incompatible Black Arcana cached gates fail-closed.