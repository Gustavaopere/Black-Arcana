# Balance and abuse risk register

Status: PREPARATORY. This register defines non-negotiable safety requirements for later implementation.

## Risk scale

- `Low`: ordinary validation/config risk.
- `Medium`: can create exploits or annoyance without bounded parameters.
- `High`: can trivialize progression/PvP/bosses or cause expensive runtime behavior.
- `Critical`: can duplicate value, grant practical immortality, grief worlds, trap players, bypass mod invariants or create unbounded server load.

## Global invariants

1. No permanent resource/power statistic grows solely because the player repeatedly spends that same resource.
2. No Black Arcana mechanic duplicates arbitrary item NBT or converts an ephemeral projection into a persistent item.
3. All terrain/fire/explosion mutations route through `WorldEffectPolicy`; default presets are `OFF`, `COSMETIC` or `TEMPORARY` where feasible.
4. No spell may force-load arbitrary chunks to find targets, portals, familiars or remote storage.
5. PvP control/scrying/health manipulation must have a server policy and may default to disabled or reduced behavior against players.
6. Bosses and tagged protected entities receive explicit resistance/eligibility rules; Black Arcana never assumes vanilla-only boss behavior.
7. External resource conversion must not create a closed positive-feedback loop across Iron's/Ars/Malum/Eidolon/health/durability.
8. Persistent area effects use indexed ownership and bounded tick budgets, never global scans.
9. Every temporary block/entity/domain effect has cleanup semantics for normal expiry, chunk unload, server restart, caster logout/death and interrupted cast.
10. Client prediction never authorizes costs, targets, permissions or world changes.

## Numeric guardrails

`docs/design/server-safety-ceilings.md` is the canonical preparatory table of default runtime budgets and absolute validation ceilings. Stage 08 may tighten/tune defaults but must not silently raise hard ceilings. A higher hard ceiling requires a recorded architecture/risk decision.

## Critical mechanics

### Sanguine Harvest
Threats: mob-farm resource generation, healing loops, mass entity drain.
Requirements:
- cap targets processed per interval and total life converted per cast/ward;
- no automatic conversion to multiple positive resources simultaneously;
- configurable eligible entity tags and player policy;
- diminishing yield for repeated farmed entity types/source contexts;
- server-side LOS/range/ownership checks.

### Reciprocal Transposition
Threats: involuntary player movement, item automation exploits, cross-chunk inconsistency.
Requirements:
- no block/block-entity swap;
- both endpoints loaded naturally; never force load;
- player targets require consent/PvP policy;
- atomic validation before mutation and deterministic failure if either endpoint becomes invalid;
- cooldown/throughput budget for automation.

### Echo Armament / Spectral Arsenal
Threats: NBT duplication, modded weapon side effects, projectile/entity spam.
Requirements:
- derive a whitelist/sanitized immutable `ProjectedWeaponProfile` rather than cloning ItemStack persistence data;
- echoes cannot enter inventories/containers, be picked up, repaired, enchanted, traded or survive logout/restart;
- per-caster active projectile/echo cap;
- damage budget independent of absurd source-item NBT;
- explicit integration tests with modded weapons before profiles are allowed.

### Inner Dominion
Threats: stranded players, duplicated inventories, death-item loss, unloaded dimensions, permanent arena state.
Requirements:
- server-owned session state with origin and participants;
- guaranteed return on expiry, caster death/logout, target logout, server restart recovery and abnormal termination;
- no forced item drop/persistence inside ephemeral domain;
- bounded participants, radius/arena size and duration;
- deny nested dominions unless a later explicit design proves safe.

### Oathforged Ascension
Threats: recursive permanent damage growth and enchantment multiplication.
Requirements:
- finite enhancement-point budget and hard absolute cap;
- sacrificed value converted through diminishing returns;
- result cannot be fed recursively for net-positive growth;
- unsupported/modded attributes ignored unless explicitly adapted;
- transaction consumes inputs atomically.

### Sympathetic Wound
Threats: reflect recursion, boss one-shots, potion/effect amplification.
Requirements:
- link only Black Arcana-approved damage contribution; never recursively mirror reflected/shared damage;
- cap mirrored damage per event and per link lifetime;
- separate player/boss multipliers;
- do not copy arbitrary potion/data-component state;
- link breaks on distance/dimension/death according to explicit spec.

### Malison Constellation
Threats: mass PvP grief and O(n²) node/entity work.
Requirements:
- strict node count, edge length, polygon area and affected-entity budgets;
- graph computed only when dirty/activated, not every tick;
- spatial query limited to bounded area;
- players excluded by default unless server enables hostile ritual PvP;
- effects encoded by Black Arcana data, not arbitrary commands.

### Gaze of Stillness
Threats: hard stun chains and latency disagreement.
Requirements:
- server-authoritative facing/LOS tolerance;
- short reapplication immunity/diminishing CC window;
- boss/player duration multiplier;
- break on caster interruption and victim escape conditions;
- accessibility-friendly telegraph and clear HUD status.

### Black Pyre
Threats: exponential fire spread, base grief and thousands of ticking blocks/entities.
Requirements:
- `TEMPORARY` default; permanent block replacement disabled by default;
- per-cast spread radius, active-cell count, propagation-per-tick and lifetime budget;
- unloaded chunks are not loaded to continue spread;
- protected/claimed blocks and fire-immune tags honored through world policy;
- entity damage independent from terrain mutation so safe mode remains useful.

### Mortal Ledger / Soul Anchor
Threats: mob-farm immortality and logout/death duplication.
Requirements:
- hard cap on full anchors;
- eligible-death rules and anti-farm contribution/rarity weighting;
- anchor consumption is atomic with death prevention;
- post-revival vulnerability/recovery lockout;
- configurable boss/PvP behavior and no recursive activation in one death event.

### Nullifying Gaze
Threats: disabling arbitrary mod mechanics/boss phases.
Requirements:
- only remove effects/behaviors explicitly exposed through tags/API adapters;
- never mutate another mod's private state by reflection/hardcoded internals;
- protected effect tag and boss resistance;
- deterministic list of affected categories exposed to config/docs.

### Pact Sanctuary
Threats: trivializing combat and AI path recalculation storms.
Requirements:
- bounded radius and affected-entity query interval;
- no per-tick forced path recalculation;
- boss/hostile-event exclusions;
- effect is temporary hostility suppression, not permanent faction mutation;
- deactivate cleanly when familiar unloads/dies/logs out.

### Blood Price
Threats: regeneration→mana/resource arbitrage.
Requirements:
- cast-time substitution only; never passive damage income;
- inefficient conversion and maximum fraction of total cost payable with health;
- cannot reduce caster below configured safety floor unless a specific forbidden spell explicitly permits lethal payment;
- no conversion of absorption/temporary health unless explicitly enabled.

### Law of Recurrence
Threats: full immunity chains.
Requirements:
- resistance has hard ceiling below total immunity for ordinary mode;
- vulnerability has hard floor/ceiling to avoid overflow;
- stable Black Arcana damage-family classifier;
- duration and stack count bounded; reset behavior deterministic.

### Equilibrium Rite
Threats: boss/PvP health swap cheese.
Requirements:
- operates on eligible transferable health budget, not raw arbitrary max-health percentage;
- bosses/protected entities default disabled or heavily capped;
- hostile player use follows PvP config/consent;
- cannot resurrect or produce health above target caps;
- long cooldown and significant explicit cost.

## Deferred critical mechanics

`Ruinous Convergence`, `Usurped Mandate` and any future remote/URL-driven Sigil Projector are prohibited from implementation until their own reviewed risk specification exists. `Noetic Foresight` is deferred for complexity/value reasons rather than catastrophic risk.
