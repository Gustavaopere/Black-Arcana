# Mobstein 5.4.4 — Registry & Semantic Boundary Closure Checklist

Status: `PUBLIC CATALOG MATERIALIZED / PHYSICAL AUTHORITY CORRECTED / MACHINE+STATE BOUNDARY PARTIALLY CLOSED / SYRINGE-ACTION IDENTITY UNVERIFIED / PROVIDER REMAINS CONDITIONAL`

## Purpose

Mobstein 5.4.4 is already cataloged extensively from publisher-facing material without reverse engineering its All Rights Reserved artifact. The current tree materializes the public surfaces as individual cards, including resurrected families, surgery/stretch workflows, failed experiments, syringes, structures, named entities, workstations/supports, internal perks, anatomy and acquisition/progression surfaces.

The remaining catalog blocker is no longer a generic lack of editorial coverage. The public guide is sufficient to classify several surfaces as machines, items, entities, states/effects or acquisition/progression processes that are excluded by the global semantic-magic metric. What remains unresolved is whether any provider-exposed syringe-triggered behavior or other active surface has a distinct independent Mobstein-owned action identity, and whether such an identity is active/reachable in the assembled pack.

Until that mapping exists, Black Arcana must not invent registry IDs, classes, APIs, event hooks, persistence fields or a semantic count from names alone.

## Physical authority already closed

Installed provider line already recorded by the canonical Mobstein dossier and technical/provenance audit:

- JAR: `mobstein-5.4.4-neoforge-1.21.1.jar`;
- mod id: `mobstein`;
- version: `5.4.4`;
- physical SHA-1: `3672d88f940ddd474a5429d7066b099cd0ce0c29`;
- package fingerprint: `3386302902`;
- CurseForge project/file: `1193873 / 8040734`;
- exact publisher filename: `mobstein-5.4.4-neoforge-1.21.1.jar`;
- license: All Rights Reserved.

These facts establish provider identity. They do not expose internal registry/API contracts.

This section supersedes the stale physical identifiers that were accidentally introduced in the first version of this checklist. The canonical provider dossier and `TECHNICAL-AUDIT.md` already carried the exact physical authority above.

## Global semantic metric applied here

The canonical semantic ledger counts one discrete provider-owned magical action identity when it is a spell, glyph/spell-part primitive, ritual/rite or equivalent discrete supernatural player action. It explicitly excludes machines, items, gear, entities/familiars, effects/statuses, resource entries, ordinary recipes/processes, aliases and downstream consequences of an already-owned action.

Therefore a Mobstein surface is not countable merely because its result is supernatural. A machine, item, companion, boss state or stat modifier remains outside the metric unless authoritative evidence proves a separate player-facing action identity behind it.

## Public semantic boundary already closed

Publisher-authored guide material already establishes the following classifications without requiring internal ARR implementation inspection:

| Public surface | Publisher-visible form | Ledger consequence at this checkpoint |
|---|---|---|
| Clinical Stretch resurrection | dedicated machine/process using a compatible full body, nighttime gate and lightning presentation | machine/process itself is excluded; resurrected creature is an entity/result state |
| Surgery Stretch reconstruction | dedicated machine combining body/head/anatomical inputs plus Mobstein modifiers | machine/process and input modifiers are excluded |
| Organ Extractor | dedicated machine processing full bodies with Tweezers into organs | machine/acquisition process and resource outputs are excluded |
| Subject Assembly Machine / head workflow | dedicated assembly machine for mannequin/test-subject construction | machine/process and resulting subject entity are excluded |
| Igor failed-experiment workflow | Igor + Station/Table + Suspicious Syringe interaction producing experiment entities | machine/entity/result surfaces are excluded; the Suspicious Syringe trigger remains in the unresolved action bucket below |
| Attack / Health / Speed / Template perks | provider-internal surgery inputs/stat modifiers | item/modifier state, not RPG Skill Tree perks and not independent semantic actions |
| resurrected mobs / failed experiments | provider-owned entities with tame/AI/aura behavior | entities and downstream effects are excluded |
| structures / named NPCs / bosses | acquisition/progression/world surfaces | structures/entities/progression state are excluded |
| companion auras and status effects | downstream entity effects | effects/statuses are excluded |

These exclusions do not prove anything about hidden implementation structure. They close only the semantic status of the publisher-visible machine/entity/state surfaces under the existing global counting rule.

## Clean-room constraint

The exact installed JAR must not be decompiled or otherwise used to reconstruct proprietary implementation details merely to close this catalog.

Permitted closure evidence includes:

1. official source code or API documentation if the publisher later releases it;
2. official registry/data documentation published by the provider;
3. provider-exposed resource/datapack/registry identifiers available through normal game/runtime interfaces;
4. deterministic registry/resource dumps or logs produced by an authorized assembled-pack runtime without reverse engineering implementation;
5. exact public data files/resources distributed in a form intended to be inspected/consumed as data;
6. direct provider/runtime observation that establishes ownership and action identity without inferring internals.

Not acceptable as registry proof:

- guessing IDs from English display names;
- filenames, translation keys or guide headings treated as registry IDs without authoritative linkage;
- decompiled ARR classes or copied implementation;
- inferred event names/classes/methods;
- generic full-pack QA used as a substitute for semantic identity.

## Gate 1 — residual exact action identity mapping

The machine/entity/state surfaces listed above no longer need to be re-litigated as semantic objects. The residual finite question is whether any provider-exposed active behavior has a distinct independent action identity rather than being only an item effect or progression interaction.

At minimum, resolve the four publisher-named syringe behaviors:

| Surface | Publicly documented trigger/result | Exact independent action identity |
|---|---|---|
| Reviver Syringe | item use revives compatible mobs; also activates Witherstein at its skeleton | `NÃO VERIFICADO` |
| Lightningbolt Syringe | provider item route enabling compatible resurrection during daytime | `NÃO VERIFICADO` |
| Mobstenio Blood Syringe | provider item route used to revive Dr. Mobstenio | `NÃO VERIFICADO` |
| Suspicious Syringe | thrown at Igor during the Station/Table workflow to produce failed experiments | `NÃO VERIFICADO` |

For each surface, establish one of:

- exact provider registry/resource/action ID when such an independent action exists;
- authoritative provider/runtime proof that the behavior is only the effect of an item interaction and has no separate action identity under the global metric;
- authoritative proof that the named surface is acquisition/progression/result state rather than an independent semantic action.

Also capture any additional provider-exposed active action surfaced by an allowed registry/resource dump. Do not infer that none exists merely because the public guide does not name one.

## Gate 2 — semantic action boundary

For every residual candidate from Gate 1, apply the global rule consistently:

- do not count the syringe item itself;
- do not count the resurrected mob, experiment, boss or aura/result state;
- do not count the machine or structure that hosts the interaction;
- count only a distinct provider-owned supernatural player action identity if authoritative evidence proves one exists independently of those objects.

This specifically prevents both failure modes: inflating the ledger from every supernatural-looking item/result, or suppressing a real action identity merely because an item initiates it.

## Gate 3 — ownership and deduplication

For every candidate independent action proven by Gate 1/2:

1. identify Mobstein as the semantic owner, or attribute it to the actual external provider when appropriate;
2. ensure acquisition objects, catalysts, structures, entities and result states do not duplicate the same action identity;
3. preserve one identity per provider-owned action under the global counting rule;
4. keep compatibility-only behavior from creating a second semantic identity.

If optional compatibility with another magic provider modifies execution but does not add a distinct Mobstein-owned action, it remains integration/compatibility metadata and contributes zero additional semantic objects.

## Gate 4 — current-pack activation

After exact independent action identities exist, confirm whether each is active/reachable in the current assembled pack when activation can be suppressed by config, optional dependency or progression gate.

This gate must use deployed pack evidence or deterministic provider-native runtime evidence. Source/publisher defaults alone are not deployed state.

If Gate 1/2 authoritatively closes all residual candidates as item/progression effects with no independent semantic action identity, there is no semantic object whose activation must be promoted; runtime compatibility remains a separate integration QA concern.

## Acceptance branches

### A. No independent Mobstein spell/ritual/action identities are proven

If supported evidence establishes that all residual syringe/active surfaces are item/progression effects without a distinct independent action identity under the global metric:

- close Mobstein as a fully cataloged provider with zero independent semantic magic/actions for this ledger scope;
- retain the granular cards as provider mechanics/acquisition documentation;
- do not promote any guessed registry identity;
- keep runtime/API integration fail-closed separately where hooks remain unknown.

### B. One or more independent action identities are proven

For each exact identity:

- add a canonical object-level card with authoritative ID/ownership evidence;
- classify reachability/config state;
- add it to the strict semantic ledger only when it satisfies the global counting rule and current-pack activation evidence;
- deduplicate catalysts, entities, result states and acquisition objects.

Provider status may move to ✅ only when the finite action inventory is closed for the current provider line.

### C. Exact mapping remains unavailable

Keep Mobstein at `⚠️ Parcial / condicionado`.

Do not use reverse engineering, guessed IDs or implementation assumptions to force closure.

## Already closed — do not redo

- exact physical provider identity/version/hash/file mapping shown above;
- publisher-facing gameplay catalog;
- object-level cards for resurrected families;
- object-level cards for surgery/stretch workflows;
- object-level cards for failed experiments;
- syringe catalog;
- structure catalog;
- named progression entities;
- workstation/support catalog;
- internal perk catalog at the public-documentation boundary;
- anatomy and acquisition/progression cards;
- semantic exclusion of publisher-visible machine, entity, resource, modifier and downstream-effect surfaces under the global metric;
- known public-guide inconsistencies preserved as evidence rather than silently reconciled;
- clean-room prohibition against inventing internal contracts.

## Separate integration/runtime QA — not this catalog gate

A future Black Arcana adapter still requires real supported hooks/contracts for any Mobstein integration. Unknown event APIs, persistence, causal identity, concurrency and settlement remain fail-closed even after the semantic catalog is complete.

Catalog completion must not be withheld solely because runtime integration is unimplemented; likewise catalog completion does not authorize a runtime adapter.

## Authority boundary

Mobstein remains authority for its entities, resurrection/surgery mechanics, workstations, progression and internal state. Black Arcana may catalog exact public/provider-exposed identities and later observe supported final state through real contracts, but it must not reconstruct Mobstein internals, create a second resurrection/surgery engine or synthesize provider outcomes when no safe hook exists.
