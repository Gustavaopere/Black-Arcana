# Stage 07 — Spell Domains preparatory architecture

Status: PREPARATORY. Source checkpoint `958ab5ef8c23f8a4aaeab6d8c96d7e3b72b45626` passed the full CI pipeline in run `33193403989`. This document records implementation boundaries; it does not promote Stage 07 ahead of unresolved Stage 05/06 ordering gates.

## Common rule

Stage 07 mechanics are implementations of the frozen Stage 01 candidate contracts. They reuse Stage 02 server authority, Stage 03 optional integrations, Stage 04 world safety and Stage 06 ritual transactions. Domain code must not create alternate casting, cost, targeting, world-mutation or ritual-authority paths.

## Blood & Curses

The current layer provides bounded planning/state for Sanguine Harvest, Sympathetic Wound, Blood Price, Law of Recurrence and Equilibrium Rite. Health conversion has a floor and cannot create resources; mirrored damage carries recursion state and event/lifetime ceilings; harvest and transfers operate under total budgets rather than unconstrained percentages.

## Souls & Death

Soul Anchor state is hard-capped and explicitly persisted/snapshotted by its ledger contract. Death credit is filtered through eligibility policy so invalid/summoned/repeated sources do not automatically form an infinite resurrection loop. Spirit Sight exposes supported occult traces only and is not a generic hidden-entity reveal.

## Projection & Arsenal

Projected equipment uses sanitized `ProjectedWeaponProfile` data instead of cloning live `ItemStack`/NBT/data components. Registries and active projection budgets are bounded. Ascension allocation uses finite points and cannot grow a weapon without a configured ceiling.

## Space & Displacement

Teleport/displacement primitives accept only loaded/safe destinations, bounded search/throughput and explicit ownership/revalidation. They do not move blocks or block entities and do not create chunk tickets.

## Black Pyre

Black Pyre does not delegate spread to vanilla fire. `BlackPyreFrontierScheduler` owns a finite set of frontiers, a finite number of cells per frontier and a finite number of candidates processed per tick. Unloaded candidates are dropped rather than retained as implicit future chunk-load requests. Terrain presentation is specified as `TEMPORARY` by default and must route through Stage 04 world-effect policy; entity damage is a separate policy-controlled outcome.

Technical ceilings at this checkpoint: radius <= 12 blocks, <= 256 cells/frontier, <= 16 candidate cells processed/tick/frontier, <= 8 concurrent frontiers and <= 1200 ticks lifetime. Stage 08 may tighten normal balance but must not silently raise these technical ceilings.

## Forbidden Domains

Stage 07 selects a localized-session-first architecture for `Inner Dominion`. Dynamic/temporary dimensions are deliberately deferred because their cleanup, chunk ownership and restart recovery risk is materially higher.

`InnerDominionSessionJournal` limits active sessions, participants and duration; one participant cannot be in two domain sessions simultaneously. Every participant has a recorded origin plus fallback return route. Recovery chooses a loaded/safe origin first, then a loaded/safe fallback, and never invents an unchecked destination. Session snapshots can be restored after restart while expired/overlapping state is dropped fail-closed.

Technical ceilings at this checkpoint: radius <= 32 blocks, duration <= 2400 ticks, <= 16 participants/session and <= 4 active sessions.

## Familiars & Divination

Familiar ownership is explicit UUID state with a hard per-owner cap and cannot be stolen by rebinding. Namescry requires a currently loaded, same-dimension target inside the bounded range; player targets additionally require consent/covenant authorization. Borrowed Sight requires an owned familiar. Occult Appraisal filters requested metadata through an allowlist rather than exposing arbitrary NBT, capabilities or container contents.

Remote-view/familiar entity adapters must implement logout, unload, death and dimension cleanup when wired to real entities. These primitives intentionally do not force-load the familiar or target chunk.

Technical ceilings at this checkpoint: <= 2 familiars/owner, remote perception range <= 96 blocks, remote-view duration <= 400 ticks and Pact Sanctuary target processing <= 32 entities.

## Verification

`feat/verify-spell-domains-v1` at `958ab5ef8c23f8a4aaeab6d8c96d7e3b72b45626` passed:
- unit tests;
- diff sanity;
- NeoForge build;
- built-JAR inspection;
- GameTest server;
- dedicated-server smoke.

Task files remain unrenamed because Stage 07 is stacked behind non-canonical Stages 05–06.
