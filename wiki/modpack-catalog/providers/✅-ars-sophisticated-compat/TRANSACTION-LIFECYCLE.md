# Sophisticated Backpacks: Ars Compat — transaction and lifecycle boundaries

Status: `INTEGRATION SAFETY MODEL / EXACT PUBLISHER SURFACE / PROVIDER INTERNALS NOT ASSERTED`

This document defines Black Arcana integration constraints derived from the exact 0.3.0 publisher surface for Sophisticated Backpacks: Ars Compat. It is not a claim about the installed JAR's internal algorithm.

## Source storage lifecycle

Black Arcana must preserve one Source authority:

- no Black Arcana-side mirrored Source balance;
- no capacity recalculation from guessed Stack Upgrade formulas;
- no duplicate balance materialization on backpack unload/reload or server restart;
- no invented overflow policy when capacity changes.

Overflow and migration behavior belong to the current provider stack and require supported runtime evidence.

## Item-to-Source conversion

Treat each Sourcelink conversion as one causal provider transaction. Black Arcana may consume a settled provider event/snapshot later if a real hook exists, but must not repeat:

- eligibility resolution;
- item consumption;
- Source credit;
- retries after chunk/server reload.

Concurrency validation must cover player and automation mutation of the same backpack/inventory state where the provider supports it.

## Potion refresh lifecycle

Never treat client-visible duration as authority. Required QA surfaces include:

- upgrade insertion/removal;
- backpack unload/reload;
- server restart;
- Stack Upgrade change;
- target/effect-context disappearance;
- multiple relevant upgrades/containers;
- reconnect.

A removed authoritative provider condition must not leave a Black Arcana-created ghost effect.

## Source-based repair

Enchanter's Upgrade occupies one repair transaction. Black Arcana must not:

- debit Source twice;
- repair durability twice;
- emit ordinary offensive proc chains from repair bookkeeping;
- reinterpret provider repair as a Black Arcana cast;
- synthesize a fallback repair if the provider hook is unavailable.

If progression later depends on repair, it must observe an authoritative settled result with stable causal identity.

## Cross-provider concurrency

Other Ars/Source integrations do not transfer Source authority away from Ars Nouveau, and other inventory integrations do not transfer backpack state authority away from Sophisticated Backpacks/Core.

Any future Black Arcana integration must avoid double-processing when another adapter observes the same inventory or Source mutation.

## Runtime compatibility gate

The exact compat release identity is closed at catalogue level, but exact deployed host versions, hooks, persistence and lifecycle semantics are not inferred here unless separately proven.

Without a verified provider/API boundary or runtime evidence, integration remains fail-closed.
