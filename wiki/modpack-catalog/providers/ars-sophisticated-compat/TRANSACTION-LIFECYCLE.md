# Ars Sophisticated Compatibility — transaction and lifecycle boundaries

Status: `INTEGRATION SAFETY MODEL / PROVIDER INTERNALS NOT ASSERTED`

This document defines Black Arcana integration constraints derived from the documented 0.3.0 family surface. It is not a claim about the installed JAR's internal algorithm.

## Source storage lifecycle

Black Arcana must preserve one Source authority:

- no BA-side mirrored Source balance;
- no capacity recalculation from guessed Stack Upgrade formulas;
- no duplicate balance materialization on storage move/break/reload/restart;
- no invented overflow policy when capacity changes.

Overflow and migration behavior belong to the current provider stack and require runtime observation.

## Item-to-Source conversion

Treat each provider conversion as one causal transaction. BA may consume a settled provider event/snapshot later if a real hook exists, but must not repeat:

- eligibility resolution;
- item consumption;
- Source credit;
- retries after chunk/server reload.

Concurrency validation must cover player and automation mutation of the same inventory.

## Potion refresh lifecycle

Never treat client-visible duration as authority. Required QA surfaces include:

- upgrade insertion/removal;
- storage unload/reload;
- server restart;
- Stack Upgrade change;
- target/effect-context disappearance;
- multiple relevant storages/upgrades;
- reconnect.

A removed authoritative provider condition must not leave a BA-created ghost effect.

## Source-based repair

Enchanter's Upgrade occupies one repair transaction. BA must not:

- debit Source twice;
- repair durability twice;
- emit ordinary offensive proc chains from repair bookkeeping;
- reinterpret the provider repair as a Black Arcana cast;
- synthesize a fallback repair if the provider hook is unavailable.

If progression later depends on repair, it must observe an authoritative settled result with stable causal identity.

## Cross-provider concurrency

Current pack also contains Ars/Source integrations such as Ars Creo, Ars Technica and Ars Sable, plus Sophisticated Storage Create Integration. They do not transfer Source authority away from Ars or inventory authority away from Sophisticated Storage.

Any future BA integration must avoid double-processing when another adapter observes the same container mutation.

## Runtime compatibility gate

Current physical hosts are Ars Nouveau 5.13.1, Sophisticated Core 1.5.1 and Sophisticated Storage 1.5.91. Presence/version alone do not prove the installed compat binary's exact hooks remain valid.

Without exact installed-binary/API evidence, integration remains fail-closed.