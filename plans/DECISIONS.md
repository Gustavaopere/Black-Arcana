# Black Arcana — Architectural Decisions

This file records decisions that must survive across sessions. Amend deliberately; do not silently reinterpret them.

## D001 — Target platform

Black Arcana targets Minecraft 1.21.1 on NeoForge with Java 21.

## D002 — Clean-room implementation

Mahou Tsukai is a behavioral/design reference only. Black Arcana will not copy/decompile its code or reuse protected assets. Mechanics are specified from observable/public behavior and then implemented independently with original code, naming, presentation and balancing.

## D003 — Original identity

Black Arcana is not "Mahou Tsukai 2". Strongly derivative names, fiction-specific terminology and presentation should be replaced with original Black Arcana terminology unless a term is generic.

## D004 — No mandatory second mana pool

Black Arcana core must support pluggable cost providers. Spells may consume Iron's mana, Ars resources, Malum spirits, items, health, cooldown budget or composite costs. A permanent Black Arcana mana pool/UI is not the default architecture.

## D005 — Casting is not staff-locked

Core casting must support direct keybind/loadout invocation. Books, weapons, staves and rituals can be optional invocation surfaces, not universal requirements.

## D006 — Server authority

The server validates cast legality, resource costs, cooldowns, progression gates, targets and world effects. Client UI is predictive/presentational only.

## D007 — World destruction is policy-controlled

Every Black Arcana mechanic capable of altering blocks, fluids, explosions, fire or persistent entities must route through a configurable `WorldEffectPolicy`. Default presets favor temporary/limited effects over permanent destruction.

## D008 — Bounded power

No mechanic may scale without an explicit upper bound or diminishing-return function. Resurrection charges, stored damage, weapon strengthening, summoned arsenal size, domain radius/duration and area destruction all require caps/budgets.

## D009 — Integration architecture

External-mod integrations live behind Black Arcana-owned interfaces. Core code must not scatter direct optional-mod references. Adapters activate only when the target mod and compatible API are present.

## D010 — Content taxonomy

Initial content families are: Blood & Curses, Souls & Death, Projection & Arsenal, Space & Displacement, Black Flame, Forbidden Domains, Familiars & Divination. Stage 01 may merge/drop concepts before implementation.

## D011 — Ritual philosophy

Routine combat spells should not require ritual busywork. Rituals are reserved for permanent unlocks, high-impact bargains, grand effects, soul contracts, domain creation/upgrades and other actions that benefit from preparation and world interaction.

## D012 — Progression philosophy

Power should come from knowledge, RPG attributes/mastery, equipment and meaningful ritual milestones—not repetitive resource-spending loops that inflate a mana cap indefinitely.

## D013 — License

Project license is intentionally undecided until the clean-room/provenance stage. Do not add a repository license without an explicit decision. `All Rights Reserved` in mandatory NeoForge mod metadata is a conservative packaging placeholder and is not a decision to publish under a particular license.

## D014 — Foundation toolchain pins

The initial 1.21.1 foundation follows the current official NeoForge MDK baseline observed on 2026-08-27: ModDevGradle `2.0.144`, NeoForge `21.1.248`, Parchment `2024.11.17` for Minecraft `1.21.1`, Java 21, and Gradle `9.2.1`.

## D015 — Reproducible text Gradle bootstrap

Until a standard binary `gradle-wrapper.jar` can be introduced and verified cleanly, the repository uses text `gradlew`/`gradlew.bat` bootstraps pinned to Gradle 9.2.1. The launcher downloads the official binary distribution and verifies it against Gradle's published SHA-256 before executing. This is an implementation detail, not an API contract; replacing it later with the official wrapper is allowed without changing gameplay architecture.
