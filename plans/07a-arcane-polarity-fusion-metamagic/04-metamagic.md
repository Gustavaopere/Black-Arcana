# 07A.04 — Metamagic

## State

`PLANNED / NOT IMPLEMENTED`

## Objective

Add a bounded doctrine layer that transforms approved Black Arcana cast semantics while preserving the single canonical engine and provider authority.

## Metamagic is not Ars augments

Ars Nouveau already owns a mature grammar for amplification, AOE, duration, piercing, splitting and other glyph-level composition. Black Arcana must not clone that feature set under different names.

07A metamagic exists for cross-domain/high-risk transformations whose meaning belongs to Black Arcana danger, sourcing and ritual/cast rules.

## Planned doctrines

### Overchannel

Trade sharply increased canonical Strain/Corruption and resource cost for bounded potency and/or duration.

Requirements:

- hard per-spell ceiling;
- no multiplication after downstream provider scaling that can compound without bound;
- high-power world effects still separately budgeted;
- no cast allowed when the transformed hazard/cost cannot be preflighted atomically.

### Concentrate

Trade area/target count for precision and a bounded potency benefit.

Requirements:

- cannot turn an area spell into an unsafe single-target boss bypass;
- target geometry remains server-owned;
- explicit boss/PvP policy.

### Sanctify

Where a spell explicitly permits alternate sourcing, replace extractive cost/source semantics with self-owned or proven consensual resources.

Requirements:

- generally higher cost/slower cast/stricter ritual preparation;
- cannot cosmetically relabel theft as white magic;
- resolved polarity changes only after every extractive source is removed or made consensual;
- unsupported provider source replacement fails closed.

### Predation

Allow an explicitly eligible spell to externalize a bounded portion of cost into stolen life/blood or another reviewed extractive source.

Requirements:

- always Umbral when non-consensual;
- heavy progression/hazard gate;
- target eligibility and PvP consent/permissions evaluated server-side;
- Blood & Curses/07.08 accounting reused;
- never siphon from protected/invalid targets or infer blood from generic damage;
- no positive feedback loop that mints more usable resource than the proven loss.

### Echo

Schedule at most one bounded delayed re-resolution that remains part of the original causal cast identity.

Requirements:

- not a second reward identity;
- no second ordinary offensive proc chain;
- no recursive Echo;
- delayed work uses canonical bounded scheduler and revalidates live target/world safety;
- original cast stores only bounded continuation state.

### Anchor

Trade caster mobility/position freedom for a more stable bounded channel/field.

Requirements:

- server-owned channel state;
- movement/dimension/death interruption rules explicit;
- no client-authoritative stationary flag;
- no chunk forcing.

## Admission model

A spell must opt into each metamagic explicitly. There is no global “works on every spell” flag.

Planned metadata:

- admitted doctrine ids;
- mutual exclusions;
- min/max rank or progression gate;
- transformed cost formula strategy;
- transformed hazard formula strategy;
- target/area transformation strategy;
- cooldown strategy;
- hard cap;
- presentation key.

All strategies are registered server code with bounded semantics. Datapacks select among those strategies but cannot execute arbitrary code.

## Canonical cast interaction

Metamagic selection is client intent only. The server resolves the actually unlocked doctrine and final parameters, then freezes an immutable resolved cast specification before cost reservation.

No doctrine may mutate provider resources, cooldowns, world state or hazards during “preview.” Preflight stays side-effect free.

If fusion and metamagic are both present, order is explicit and deterministic:

1. resolve base spell;
2. resolve admitted fusion into one semantic specification;
3. resolve admitted metamagic over that specification;
4. clamp/check absolute safety ceilings;
5. continue through normal canonical target/world/hazard/cost/effect transaction.

Definitions must declare conflicts where that order is unsafe.

## Proc/reward rule

Metamagic is not allowed to multiply ordinary offensive proc chains or progression rewards by merely duplicating sub-effects. Echo/secondary hits must carry causal metadata that downstream Black Arcana logic can recognize as part of the original cast.

If an external provider lacks a way to preserve this causality safely, that provider-specific metamagic combination is unsupported/fail-closed.

## Tests first

RED tests must cover:

- locked doctrine cannot be client-forced;
- unsupported spell/doctrine pair is denied;
- Overchannel respects absolute potency/duration/hazard caps;
- Sanctify cannot change polarity while any unresolved extractive source remains;
- Predation uses canonical blood/life accounting once;
- Echo runs at most once and cannot Echo itself;
- Echo cannot create second reward/proc identity;
- Anchor ends on configured movement/death/dimension/session invalidation;
- fusion+metamagic ordering is deterministic;
- transformed cost/hazard/world policy is fully preflighted before commit;
- provider adapter failure fails closed.

## Acceptance

- every doctrine bounded and opt-in;
- no Ars augment duplication;
- no second cast engine/resource state;
- deterministic composition with fusion;
- Stage 08 receives explicit tunable formulas and caps.
