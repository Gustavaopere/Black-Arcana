# Sophisticated Backpacks: Ars Compat — functional contract

Status: `EXACT 0.3.0 PUBLISHER SURFACE / BACKPACK UPGRADE BRIDGE / ZERO STANDALONE SPELL-GLYPH-RITUAL IDENTITIES / RUNTIME INTERNALS FAIL-CLOSED`

The installed `arssophisticatedcompat-0.3.0.jar` is aligned at release identity level with official CurseForge File ID `8653384`, the NeoForge 1.21.1 release of **Sophisticated Backpacks: Ars Compat**. This document records only publisher-visible gameplay contracts and Black Arcana ownership constraints; it does not reconstruct implementation internals.

## 1. Source Storage Upgrade

Official contract: a Sophisticated Backpack can store Ars Nouveau Source, with capacity scaling through Sophisticated Stack Upgrades.

Boundary:

- Sophisticated Backpacks/Core own backpack storage and upgrade lifecycle;
- Ars Nouveau owns Source identity/economy;
- the compat connects those systems;
- Black Arcana must observe provider-final state rather than reconstruct a capacity formula.

No exact capacity number/formula is asserted here.

## 2. Backpack Sourcelink upgrades

Official project description names Agronomic, Alchemical, Mycelial, Volcanic and Vitalic Sourcelink upgrades. Their public role is to convert eligible backpack contents into Source.

Required causal invariant for any future Black Arcana observer:

`one provider-accepted conversion -> one provider item settlement -> one provider Source credit`

Black Arcana must not independently consume the item, credit Source, retry the provider conversion after reload, or award progression from pre-settlement intent.

Exact eligibility tables, yields and cadence remain runtime/API questions.

## 3. Potion Jar Upgrade

Official contract: potion duration can be stored and potion effects can be maintained from that stored duration.

Boundary:

- authoritative effect state remains server gameplay state;
- backpack/upgrade state remains Sophisticated-owned;
- GUI/timer/tooltips remain presentation;
- Black Arcana must not add a second refresh scheduler.

Exact duration schema, tick interval and refresh algorithm are not asserted.

## 4. Enchanter's Upgrade

Official project description states that enchanted items can be repaired using stored Source.

Boundary:

- Source debit happens once in provider authority;
- durability repair happens once in provider authority;
- Black Arcana must not turn observation into a second repair proc;
- repair bookkeeping is not a Black Arcana cast and must not implicitly create Strain, Corruption or Backlash.

Exact repair cost/amount/cadence remain unverified.

## 5. Templates and recipes

The exact release also publishes Ars Nouveau-themed backpack upgrade templates and recipes. These are acquisition/presentation surfaces and do not create new spell, glyph, ritual or Source authorities.

## Semantic result

The exact publisher surface defines compatibility upgrades and no standalone casting content:

- standalone spells: **0**;
- glyph/spell parts: **0**;
- rituals: **0**;
- strict semantic spell/action contribution: **+0**.

This result is catalogue closure, not certification of internal registry topology.

## Explicitly unconfirmed implementation details

Without an allowed exact internal/API boundary, do not assert:

- exact item/upgrade/resource IDs;
- classes/methods/events;
- configs or dependency ranges beyond publisher-declared required families;
- mixins/payloads;
- numerical capacity/yield/repair values;
- update cadence;
- persistence/serialization mechanics.
