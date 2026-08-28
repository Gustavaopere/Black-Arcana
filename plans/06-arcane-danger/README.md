# 06 — Arcane Danger, Resistance, Corruption & Backlash

Black Arcana owns the risk of manipulating dangerous and forbidden magic. This stage exists so later rituals and spell domains can remain extremely powerful without balancing them only through mana, cooldowns or artificially weak numbers.

## Canonical fantasy

A character may attempt to wield forbidden power before being ready. The spell can still work, but the caster pays for inadequate preparation through Arcane Backlash, Arcane Strain and Corruption.

Preparation is buildcraft, not a single perk line. Valid sources may include Black Arcana armor/items, Curios, buffs, rituals, RPG Skill Tree providers and other explicitly registered providers.

## Permanent invariant

For a dangerous/forbidden profile whose eligible-damage aggregation is linear:

`effective Arcane Resistance = 0 -> 100% of eligible confirmed damage becomes Arcane Backlash.`

For AoE/multi-hit profiles that explicitly use bounded aggregation, zero resistance still returns 100% of the profile's **eligible causal damage**. The aggregation step is spell/profile-owned and may never silently reduce a single-target dangerous spell below the canonical 1:1 rule.

Arcane Backlash is not reflected attack damage. It is a Black Arcana-owned damage family with its own provenance, mitigation, telemetry and exclusions.

## Resistance curve

Initial canonical curve for Arcane Resistance:

`residualBacklash(R) = K / (K + clamp(R, 0, R_MAX))`

Initial defaults:
- `K = 40` resistance units.
- `R_MAX = 240` effective resistance.
- negative, NaN and infinite contributions are rejected/clamped to zero.
- resistance can never turn backlash into healing.

Examples of the default curve before profile-specific unavoidable floors/caps:
- `R=0 -> 100%` residual backlash.
- `R=10 -> 80%`.
- `R=40 -> 50%`.
- `R=80 -> 33.33%`.
- `R=120 -> 25%`.
- `R=240 -> 14.29%`.

This gives strong diminishing returns: specialized builds become materially safer without allowing a few trivial items to erase the system. Stage 09 balance work may tune bounded constants, but may not break `R=0 -> 100%` for dangerous/forbidden linear profiles.

Corruption Resistance is a separate channel. It may reuse the same mathematical family, but has independent providers, constants, caps and consequences. Generic magic resistance, vanilla armor/toughness, Shroud exposure and Volcanoes environmental resistances are not Arcane Resistance by default.

## Causal model

The existing `ArcanaCastId` is the root cast identity. Do not create a parallel cast machine.

Hazard attribution introduces subordinate identities:
- `ROOT_CAST_ID` — existing `ArcanaCastId`.
- `DAMAGE_INSTANCE_ID` — unique damage attempt/event owned by a root cast.
- damage provenance — direct, projectile, AoE, chain, DoT, summon, environmental or backlash.

Backlash is derived from **confirmed post-mitigation health damage**, not nominal spell damage. Damage is accumulated into a bounded root-cast ledger and deduplicated by damage-instance identity.

For multi-hit/AoE, a profile supplies a monotonic aggregation function `F(totalConfirmedEligibleDamage)`. Incremental backlash basis is `F(newTotal) - F(previousTotal)`, so result is deterministic and independent of hit ordering. Default dangerous/forbidden behavior is linear `F(D)=D`; AoE profiles may explicitly select bounded/diminishing aggregation; catastrophic profiles may deliberately keep full linear aggregation.

DoT/projectile/chain damage retains the original root cast. It must not create a new cast/backlash session each tick or impact. Summon damage is ineligible unless the spell profile explicitly marks the summon/servant family as hazard-owned.

## Snapshot rule

The server performs a read-only preflight first. After normal cast checks and resource reservation succeed, but before spell effects can deal damage, the hazard session activates and snapshots:
- caster identity and root cast id;
- spell danger profile/version;
- Arcane Resistance and full source breakdown;
- Corruption Resistance and full source breakdown;
- current Arcane Strain/corruption state relevant to the profile;
- relevant armor, Curios and provider facts;
- emergency-protection availability as metadata only.

Delayed damage uses this committed snapshot. Swapping armor/Curios, receiving a buff, or changing RPG perks after the cast cannot retroactively avoid that cast's backlash. Channelled spells snapshot at valid channel release by default unless the profile explicitly chooses another bounded policy.

## Canonical ordering

`CAST_REQUEST -> canonical spell/target -> resistance/provider snapshots -> danger preflight -> hard-gate decision -> normal cost reservation -> activate hazard session -> spell effects -> confirmed-damage ledger -> backlash settlement -> corruption/strain settlement -> BA-owned sustain/lifesteal -> final observers/telemetry`

The exact integration with the frozen Stage 02 transaction must preserve its refund semantics: a hazard session that never produces a committed/successful effect is cancelled without inventing damage or persistent corruption.

## Backlash exclusions

`ARCANE_BACKLASH` must never:
- create another backlash record;
- count as eligible offensive spell damage;
- award normal offensive mastery;
- crit;
- lifesteal;
- trigger normal on-hit offensive proc chains;
- register as a new root cast;
- become healing through negative resistance.

Vanilla armor/toughness and generic magic resistance do not automatically reduce it. Specialized Black Arcana mitigation is resolved before applying the dedicated backlash damage source.

## Danger profiles

Each relevant spell resolves a bounded, declarative `ArcaneDangerProfile` containing at minimum:
- danger tier (`NORMAL`, `UNSTABLE`, `DANGEROUS`, `FORBIDDEN`, `CATASTROPHIC` or finalized equivalents);
- forbidden-magic semantic flag/derived state;
- backlash aggregation/profile;
- base corruption and optional damage-linked corruption coefficient;
- base strain and optional damage-linked strain coefficient;
- minimum/recommended Arcane Resistance;
- below-minimum policy (`ALLOW`, `DENY`, `CATASTROPHIC` or equivalent);
- unavoidable backlash/corruption floors where applicable;
- DoT/projectile/summon ownership policy;
- snapshot policy;
- per-cast hard caps/ceilings.

Profiles may be data-driven only through bounded enums/numbers. No Java class names, commands or scripts may come from datapacks.

## Persistent vs transient state

Persistent player state:
- corruption;
- strain/recovery timestamps where needed to prevent relog cleansing;
- emergency-protection cooldown/charge state where applicable.

Transient bounded state:
- active root-cast hazard sessions;
- damage-instance dedupe sets;
- confirmed-damage ledgers;
- temporary preflight snapshots.

Persistent state belongs in the existing global/Overworld `BlackArcanaSavedData` with schema migration and defensive ceilings. Damage ledgers are not persisted by default; a future long-lived effect may persist an immutable hazard snapshot only through an explicit recovery contract.

## Public API direction

Black Arcana exposes a stable server-side hazard API. Other mods register contributions/observers; Black Arcana remains the owner of computation and consequences.

Planned API surfaces include resistance providers, corruption providers, immutable snapshots, danger/profile queries, read-only preflight, hazard observers and telemetry views. Provider queries must be side-effect free.

The RPG Skill Tree must register contributions through this API rather than Black Arcana reading RPG internals for hazard resistance.

## Curios baseline

Installed-first baseline is Curios NeoForge `9.5.1+1.21.1`. Curios integration is optional and snapshot-only: no global/per-tick Curios scan. Missing Curios simply removes Curios contributions; it does not disable Black Arcana.

## Stage tasks

1. [Arcane Danger Model](01-arcane-danger-model.md)
2. [Arcane Resistance](02-arcane-resistance.md)
3. [Corruption Resistance](03-corruption-resistance.md)
4. [Arcane Strain](04-arcane-strain.md)
5. [Backlash Pipeline](05-backlash-pipeline.md)
6. [Equipment & Containment Items](06-equipment.md)
7. [Curios Integration](07-curios.md)
8. [Spell Danger Profiles](08-spell-profiles.md)
9. [Public Hazard API](09-public-api.md)
10. [RPG Skill Tree Integration](10-rpg-skilltree-integration.md)
11. [HUD, Tooltip & Preflight](11-hud-tooltip-preflight.md)
12. [Tests & Hardening](12-tests-hardening.md)

## Exit criteria

The stage is not complete until a real NeoForge 1.21.1 runner proves all of the following:
- zero resistance produces exact 1:1 backlash for the canonical dangerous/forbidden linear test spell;
- resistance curve/caps are deterministic and bounded;
- confirmed causal damage is attributed correctly across direct, AoE, multi-hit, projectile and DoT cases;
- backlash cannot recurse or behave as a normal offensive hit;
- equipment, Curios and an external/RPG provider contribute through snapshots without post-cast gear-swap exploits;
- corruption and strain persist/recover under their contracts;
- read-only preflight has no side effects and matches server execution inputs;
- multiplayer/PvP/death/relog/restart tests pass;
- dedicated-server smoke has no client/Curios/RPG mandatory classloading.
