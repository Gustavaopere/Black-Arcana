# 05A — Arcane Danger, Resistance, Corruption & Backlash

Black Arcana owns the risk of manipulating dangerous and forbidden magic. This inserted stage sits after Casting & UX and before Rituals so later rituals and spell domains can remain extremely powerful without balancing them only through mana, cooldowns or artificially weak numbers.

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

Examples before profile-specific unavoidable floors/caps:
- `R=0 -> 100%` residual backlash.
- `R=10 -> 80%`.
- `R=40 -> 50%`.
- `R=80 -> 33.33%`.
- `R=120 -> 25%`.
- `R=240 -> 14.29%`.

Corruption Resistance is a separate channel with independent providers, constants, caps and consequences. Generic magic resistance, vanilla armor/toughness, Shroud exposure and Volcanoes environmental resistances are not Arcane Resistance by default.

## Causal model

The existing `ArcanaCastId` remains the root cast identity. Hazard attribution adds bounded subordinate damage-instance identities; it does not create a parallel cast engine.

Backlash is derived from confirmed post-mitigation eligible health damage. Multi-hit/AoE aggregation is deterministic and profile-owned. Projectile, DoT and chain damage retain the original root cast. Summon damage is eligible only when the profile explicitly owns that summon/servant family.

## Snapshot rule

After normal checks/resource reservation succeed but before effects can deal eligible damage, the server snapshots the danger profile, Arcane/Corruption Resistance sources, relevant strain/corruption state and provider facts. Delayed damage uses that committed snapshot; swapping gear or perks afterward cannot retroactively evade that cast's risk.

## Canonical ordering

`CAST_REQUEST -> canonical spell/target -> resistance/provider snapshots -> danger preflight -> hard-gate decision -> normal cost reservation -> activate hazard session -> spell effects -> confirmed-damage ledger -> backlash settlement -> corruption/strain settlement -> BA-owned sustain/lifesteal -> final observers/telemetry`

A hazard session that never reaches a committed/successful effect is cancelled without inventing damage or persistent corruption.

## Backlash exclusions

`ARCANE_BACKLASH` must never recurse, count as normal offensive spell damage, award ordinary offensive mastery, crit, lifesteal, trigger normal on-hit proc chains or create a new root cast. Specialized Black Arcana mitigation is resolved before the dedicated backlash damage source.

## Danger profiles

Each dangerous spell resolves a bounded declarative `ArcaneDangerProfile` containing danger tier, backlash aggregation, corruption/strain coefficients, resistance recommendations/minimums, below-minimum policy, unavoidable floors, delayed-damage ownership policy, snapshot policy and hard caps. Datapacks may configure only bounded enums/numbers; no Java class names, commands or scripts.

## Persistence

Persistent player state includes corruption, anti-relog strain/recovery timestamps and any emergency-protection cooldown/charge state. Active hazard ledgers are transient and bounded by default. Persistent state uses the existing global/Overworld `BlackArcanaSavedData` with schema migration and defensive ceilings.

## Public API direction

Other mods register read-only resistance/corruption contributions and observers through Black Arcana-owned interfaces. Black Arcana remains owner of computation and consequences. The RPG Skill Tree contributes through this API rather than being read directly for hazard resistance.

## Curios baseline

Installed-first baseline is Curios NeoForge `9.5.1+1.21.1`. Curios integration is optional and snapshot-only; there is no global/per-tick Curios scan.

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

The stage is not complete until a real NeoForge 1.21.1 runner proves zero-resistance 1:1 backlash for the canonical linear profile; deterministic bounded resistance/corruption/strain; correct direct/AoE/multi-hit/projectile/DoT attribution; non-recursive backlash; snapshot-safe equipment/Curios/external providers; persistence/recovery; side-effect-free preflight; multiplayer/PvP/death/relog/restart coverage; and dedicated-server smoke without mandatory Curios/RPG/client classloading.
