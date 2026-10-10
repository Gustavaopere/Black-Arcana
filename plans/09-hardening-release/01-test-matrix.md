# 09.01 — Test Matrix

## Layers
Unit tests, codec/config tests, GameTests, networking tests, dedicated-server smoke, integration-mod profiles and manual client UX checks.

## Required scenarios
Fresh world, existing world, death/relog/restart, dimension travel, multiplayer concurrent casts, absent optional mods, malformed datapack/config, maxed RPG stats and destructive-mode variants.

## Acceptance
Matrix is executable/documented and all release-blocking rows are green before completion.


## Consolidated real-client / real-modpack campaign

Under D035, Stage 09 is the release-blocking owner of physical/manual observations transferred from completed implementation stages. For Stage 05 this includes the canonical matrix and runbook in `docs/qa/`, including:

- rebind + restart persistence and GUI-focus suppression;
- apply/clear/reopen/reconnect server-owned loadout behavior;
- physical reachability of all canonical slots `0..15`;
- denial/forecast/result-correlation and stale-state behavior;
- client-config authority isolation;
- Iron's-hosted one-root/one-cost/one-cooldown settlement;
- Epic Fight/EFIS coexistence without cast-legality authority transfer;
- optional-provider absent/incompatible fail-closed behavior and provider-free core input.

For Stage 05A Arcane Danger, the executable transfer contract is
`plans/05a-arcane-danger/✅-13-final-validation-handoff.md` and the evidence ledger is
`docs/qa/arcane-danger-final-validation-evidence.md`. Release-blocking transferred rows include:

- dangerous-profile reload/preflight convergence and stale forecast rejection;
- baseline/equipment/Curios/RPG resistance-provider snapshots and post-activation swap safety;
- real loaded-provider classification, including the currently absent top-level RPG Skill Tree artifact;
- Corruption and Arcane Strain reconnect/death/restart/recovery behavior;
- representative Backlash 1:1/reduced/delayed/terminal causal behavior in the assembled modpack;
- 05A.11 real-client forecast thresholds, bounded gate presentation, reconnect/reload staleness, readability and accessibility;
- optional-provider fail-closed behavior and dedicated-server isolation.

For Stage 06 Rituals, the physical acceptance source is
`plans/06-rituals/05-final-validation-handoff.md`, with the dated and reconciled
`docs/qa/rituals-final-validation-evidence.md` ledger. Stage 06.05 is still
**🟡 ACTIVE / NOT ENGINEERING CLOSED**; listing its release-candidate tests here
is an explicit D035 handoff, **not** Stage promotion or manual PASS:

- **06-P01** exact candidate boot with the intended Eidolon/Malum physical JARs;
- **06-P02–06-P03** real Eidolon ritual host, cost, anchor-scoped exactly-once completion and same-save restart;
- **06-P04** real Malum typed-spirit presence/binding and `4 arcane + 2 wicked` access;
- **06-P05** player-side Survival altar activation through the now-existing server-authoritative ingress; source and synthetic tests alone remain insufficient;
- **06-P06–06-P09** real requirement denial, pre/post-commit interruption, resource consumption and one-time outcome;
- **06-P10–06-P11** real multiplayer same-anchor exclusion, lifecycle, loaded-chunk, logout/dimension/death and restart recovery;
- **06-P12–06-P14** controlled optional-provider variants and dedicated-server isolation in the actual provider topology;
- **06-P15–06-P16** currently NOT APPLICABLE for the non-world-mutating, non-hazard-owning representative outcomes; reassess if representative effects change;
- independently retain the **provider-vs-SavedData abrupt-crash consistency window** as PENDING; transition-time capture is not durable atomic disk commit.

These rows remain `PENDING / DEFERRED TO STAGE 09` until observed on an exact release candidate. Automated evidence may support setup but never converts a manual row to PASS. Any FAIL reopens the originating plan for correction before release.
