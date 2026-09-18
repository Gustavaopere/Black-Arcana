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

These rows remain `PENDING / DEFERRED TO STAGE 09` until observed on an exact release candidate. Automated evidence may support setup but never converts a manual row to PASS. Any FAIL reopens the originating plan for correction before release.
