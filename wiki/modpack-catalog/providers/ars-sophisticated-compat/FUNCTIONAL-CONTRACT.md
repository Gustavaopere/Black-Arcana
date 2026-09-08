# Ars Sophisticated Compatibility — functional contract

Status: `OFFICIAL 0.3.0 FAMILY CONTRACT / PHYSICAL INTERNALS UNKNOWN`

The official NeoForge 1.21.1 0.3.0 release documents four gameplay-facing upgrade families. Because the installed JAR is a different byte artifact, this file records only the public functional contract and Black Arcana deduplication boundary.

## 1. Source Storage Upgrade

Official contract: a Sophisticated Storage block can store Ars Source and its capacity scales with Sophisticated Stack Upgrades.

Boundary:

- Sophisticated Storage owns the storage block and upgrade lifecycle;
- Ars Nouveau owns Source identity/economy;
- the compat layer connects those systems;
- Black Arcana must query provider-final state rather than reconstructing a presumed capacity formula.

No exact capacity value/formula is asserted for the physical JAR.

## 2. Storage Source Link Upgrade

Official contract: valid stored items can be converted into Source.

Required causal invariant for any future BA observer:

`one provider-accepted conversion -> one provider item settlement -> one provider Source credit`

BA must not independently consume the item, credit Source, retry the same provider conversion after reload, or award progression from pre-settlement intent.

No exact eligibility table, conversion yield or cadence is asserted for the physical JAR.

## 3. Potion Jar Upgrade

Official contract: potion duration can be stored and effects can be automatically refreshed. The official project description also states potion duration scales with Stack Upgrades.

Boundary:

- authoritative effect state remains server gameplay state;
- storage/upgrade state remains Sophisticated-owned;
- GUI/timer/tooltips are presentation;
- BA must not add a second refresh scheduler.

No exact duration schema, interval or refresh algorithm is asserted for the physical JAR.

## 4. Enchanter's Upgrade

Official contract: enchanted items can be repaired using Source.

Boundary:

- Source debit must happen once in provider authority;
- durability repair must happen once in provider authority;
- BA must not turn observing the operation into a second repair proc;
- repair bookkeeping is not a BA cast and must not implicitly create Arcane Strain/Corruption/Backlash.

No exact cost, repair amount or cadence is asserted for the physical JAR.

## Auxiliary content

Official 0.3.0 also documents:

- Ars Nouveau-themed storage upgrade template;
- inverted storage-edition item textures.

These are acquisition/presentation surfaces, not new Source or casting authorities.

## Explicitly unconfirmed for installed artifact

Without exact binary/API inspection, do not assert:

- registry/resource IDs;
- recipes;
- classes/methods/events;
- configs;
- dependency ranges;
- mixins/payloads;
- numerical capacity/yield/repair values;
- update cadence;
- physical-artifact license.