# Werewolves 2.0.3.3 — Black Arcana integration rules

## 1. Provider-native first

Werewolves owns its supernatural faction semantics through Vampirism infrastructure. Black Arcana may integrate, observe and gate against that state; it must not duplicate it.

Provider-owned domains include:

- Werewolf faction membership and normal/Lord levels;
- forms/transformation-time/full-moon forcing;
- Werewolf skill/action state;
- bite damage/cooldown/status/infection;
- Silver/Wolfsbane/Bleeding/Stun/Howling effects;
- Stone Altar progression transaction;
- refinements;
- Werewolf Lord minions/tasks;
- Werewolf Forest biome mechanics.

## 2. Authority model

### Server authority

Gameplay integration must resolve from server/provider state. Client-only surfaces such as Sense outlines, Hide Name rendering or form model are evidence for presentation, not authoritative gameplay completion.

### Faction authority

Use Vampirism/Werewolves faction state. Do not maintain a second `isWerewolf` flag as gameplay authority.

### Level authority

Use provider faction level plus Werewolf `LevelHandler`/Stone Altar outcome. Generic RPG XP cannot silently substitute provider progress.

## 3. Form integration

A Black Arcana feature that reacts to form must distinguish:

- `none`;
- `human` — human-like but transformed;
- `beast`;
- `survivalist`;
- `beast4l` — provider entity form, not proven as ordinary player form.

Do not simplify to `transformed = true/false` where exact form changes semantics.

Form hooks must preserve:

- day/night modifiers;
- transformation-time budget;
- full moon + Free Will rules;
- collision/size checks;
- armor/inventory swaps;
- provider permissions;
- health-percentage preservation.

## 4. Skill-tree integration

Generated provider tree topology is canonical for normal acquisition.

Rules:

- preserve mutually exclusive choices;
- do not grant sibling skills automatically;
- do not bypass configured tree prerequisites;
- `resistance` and `sixth_sense` remain fail-closed for normal survival acquisition until a path is proven;
- host Vampirism Lord skills referenced in Werewolves Lord tree remain Vampirism-owned.

If Black Arcana adds a perk that enhances a Werewolf skill, gate it on the provider skill handler rather than a duplicate unlock flag.

## 5. Action causal provenance

For actions such as Rage, Howling, Fear, Leap or transformations:

- activation request is not automatically successful settlement;
- verify provider action/state transition where available;
- if also observing downstream effect/damage/entity spawn, use one causal correlation key to prevent duplicate reward/credit;
- client render hooks must never independently grant gameplay credit.

## 6. Bite integration

The bite pipeline is atomic provider behavior. Do not separately recreate:

- range/permission gates;
- `bite_damage` amount;
- provider damage source;
- bite cooldown state;
- Stun/Bleeding enhancement;
- infection chance;
- provider post-bite food logic.

For external perks such as “after a successful Werewolf bite,” trigger only after a provider-confirmed successful bite/damage transaction and deduplicate any subsequent effect callbacks.

## 7. Infection and cure

### Infection

`Lupus Sanguinem` effect presence is a precursor. Faction join is the authoritative completion.

### Cure

`Un Werewolf` is a delayed provider transaction. Do not mark the player cured at injection use; confirm final faction leave/level reset.

Any Black Arcana cache depending on faction must invalidate immediately after provider membership transition.

## 8. Damage / weakness integration

Preserve source semantics:

- form-native damage reduction is not generic armor;
- Survivalist dodges are damage cancellation;
- Silver modifies Werewolf attributes and incoming damage;
- Silver Blooded weakens Silver application rather than granting immunity;
- Wolfsbane is spatial/provider-world influenced;
- Bleeding can drain Vampirism blood and is not merely generic periodic damage;
- Stun is movement suppression.

Do not merge these into one `resistance` or `debuff_resistance` scalar.

## 9. Resource separation

Werewolves has no mana economy.

Keep separate:

- Werewolf `levelProgress`;
- transformation-time state;
- `biteTicks`;
- `bite_damage`;
- food consumption/gain attributes;
- Liver / Cracked Bone / Werewolf Tooth item requirements;
- Vampirism blood;
- Black Arcana mana/stamina/other currencies.

Any conversion between these requires a separately approved bridge and explicit settlement rules.

## 10. Stone Altar settlement

Stone Altar consumes level-up items at start but awards faction level only at completion.

Integration must distinguish:

- ritual accepted/started;
- resources consumed;
- ritual aborted/interrupted;
- ritual completed;
- faction level actually changed.

Never charge Liver/Bone twice or award level-dependent perks at mere start.

## 11. Summon/minion deduplication

Two different systems exist:

### Wolf Pack

Howling can spawn temporary player-tamed `AggressiveWolfEntity` with lifespan restriction.

### Lord minion

Werewolf Lord uses Vampirism minion ownership/state, levels and tasks.

They are not equivalent. A generic “summoned wolf” event must not be used to infer Lord-minion ownership.

## 12. Refinements

Use provider equipped-refinement state. Do not infer equipped status from possessing a refinement item.

Fail closed for `no_leap_cooldown` normal acquisition because its registered/consumer state exists but its ordinary refinement-set path was not found in the exact source.

## 13. Sense and Hide Name

- Sense is partly client-rendered; visuals cannot authorize server gameplay.
- Hide Name suppresses name rendering; it is not invisibility, disguise-to-faction, target suppression or stealth authority.

## 14. Werewolf Forest

`werewolves:werewolf_heaven` is an Overworld biome displayed as Werewolf Forest. Do not route it as a dimension or portal destination unless another provider explicitly creates such a dimension.

## 15. Epic Fight boundary

Installed pack has a known Werewolves/Epic Fight visual/animation compatibility risk. Black Arcana must not assume form animation success as causal proof of form state.

Runtime integration must use provider state even if visual compatibility fails, while any combat-animation-dependent perk must fail closed until Epic Fight interaction is validated.

## 16. Static mismatch policy

Do not “repair” upstream source mismatches inside unrelated Black Arcana perks. Examples include:

- Howling radius/config issues;
- Sense radius/cooldown mismatch;
- level toughness using speed config;
- unused Health Reg/Resistance config/state surfaces;
- unreachable skill/refinement registrations.

If Black Arcana needs behavior affected by one of these, either:

1. depend on measured provider runtime behavior;
2. create an explicit compatibility fix with its own audit/tests; or
3. fail closed.

## 17. Required canonical test scenarios

For any Werewolves-dependent Black Arcana implementation, test at minimum:

- faction join and leave;
- normal level and Lord level transitions;
- each player form by day/night/full moon;
- form change under Epic Fight battle mode;
- successful/failed bite and infection;
- Stun/Bleeding exactly once;
- Silver/Wolfsbane;
- Howling with and without Wolf Pack;
- Leap landing cleanup;
- Stone Altar start/completion/abort;
- minion ownership/task completion;
- death/login/respawn state restoration.

## Contract status

`SOURCE-PINNED CONTRACT / PROVIDER AUTHORITY DEFINED / STATIC RISK FAIL-CLOSED / RUNTIME QA PENDING`.