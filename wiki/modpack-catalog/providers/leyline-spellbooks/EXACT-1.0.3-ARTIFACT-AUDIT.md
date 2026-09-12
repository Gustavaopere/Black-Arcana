# Leyline Spellbooks 1.0.3 — exact installed-artifact audit

## Scope

This checkpoint closes factual identity, registry and player-reachability evidence for the physically installed `leylines-1.0.3.jar`. It is a clean-room catalog audit, not a source reconstruction or runtime adapter specification.

## Physical authority

- Minecraft: `1.21.1`
- NeoForge: `21.1.248`
- JAR: `leylines-1.0.3.jar`
- mod id/runtime: `leylines` / `1.0.3`
- CurseForge project/file: `1636676 / 8565076`
- physical/audit SHA-1: `dfa6908731f432905caaaa1e53b4aedeaa26ed59`
- license: `All Rights Reserved`

The temporary evidence PR is #194 and must not be merged. Its hash-gated audits are:

- primary exact-artifact audit: run `34666436710`, artifact `10289437099`;
- targeted reachability audit: run `34666652534`, artifact `10289292617`;
- school/loot-gate audit: run `34667641655`, artifact `10289184487`.

Every audit required the downloaded File ID `8565076` artifact to match the physical SHA-1 before inspection.

## Exact spell registry

The exact JAR exposes one provider spell registry class, `dev.semeth.leylines.registry.LeySpellRegistry`, with one `DeferredRegister<AbstractSpell>` and fourteen `Supplier<AbstractSpell>` fields. Its static initializer constructs and registers fourteen spell classes with no conditional registration branches.

Therefore the installed 1.0.3 registry is **14 current provider spell identities**, not the public nine-name lower bound.

See [`EXACT-1.0.3-SPELL-INVENTORY.md`](./EXACT-1.0.3-SPELL-INVENTORY.md) for the identity table.

## Reachability / active-eligibility evidence

The exact artifact also closes the provider-specific gates that prevented the previous semantic promotion:

- no Somake-style spell-lock or provider registration enable/disable gate was found for the fourteen spells;
- each spell supplies an Iron's `DefaultConfig` for the Ley school and none of the fourteen overrides `allowLooting()` or `isEnabled()`;
- the exact Ley school is `leylines:ley` and uses Iron's seven-argument `SchoolType` constructor;
- on exact Iron's 3.16.3 source authority (`iron431/irons-spells-n-spellbooks@e4056af90302d37eb1739f5ff05020b020e6e252`), that constructor sets `requiresLearning=false` and `allowLooting=true`;
- Iron's `DefaultConfig` defaults spell enablement to true; no Leylines spell in this inventory calls the deprecated/disable path observed by the filtered audit;
- Iron's `SpellFilter` without an explicit filter enumerates enabled spells and admits spells whose school allows looting;
- Iron's `RandomizeSpellFunction` defaults to that empty filter;
- exact Iron's survival loot tables, including catacombs wall loot, use `randomize_spell` without a school/spell filter;
- Leylines additionally appends a dedicated level-1 `leylines:charge_leyline` scroll to several Iron's chest/entity loot tables.

This establishes that there is no provider-specific lock comparable to Somake and corroborates the ordinary Iron's host path. Under the ledger's existing `COUNTED_EXACT` precedent for unconditional Iron's-addon registries, that removes the Leylines-specific blocker to semantic counting. It does **not** substitute code defaults for an unmaterialized deployed generic Iron's per-spell config, nor prove every numerical mechanic, assembled-pack drop probability or Black Arcana integration hook.

## Exact progression/resource facts

The exact 1.0.3 archive contains provider progression resources for:

- `leylines:ley_crystal`;
- `leylines:leyline_codex`;
- `leylines:ley_staff`;
- recipe resources for the codex and staff;
- advancements for obtaining the crystal/codex/staff, charging a pillar and clearing a rift;
- `leylines:leyline_codex` as a provider spell-container item;
- encounter reward code referencing the provider codex;
- `leylines:ley` school and its Ley Crystal focus tag.

These facts improve progression identity/reachability documentation. Exact assembled-pack loot probabilities, economy tuning and runtime persistence/network ownership remain separate QA/API questions.

## Authority boundary

Provider-native first remains mandatory:

- Iron's owns its generic casting, mana, scroll and spell-container substrate;
- Leyline Spellbooks owns the fourteen spell identities, Ley school, Leyline progression/content, portal/anchor semantics and pillar/rift encounter lifecycle;
- Black Arcana owns its own casting, costs, cooldowns/charges, Corruption, Strain, Arcane Danger, hazards, rituals and world-safety runtime.

Black Arcana must not create a second Leyline spell registry, scroll acquisition system, charge ledger, portal pair, recall-anchor store, pillar progression or rift state machine. A future adapter requires a stable exact-version provider/API seam and fails closed otherwise.

## Clean-room boundary

Leyline Spellbooks is All Rights Reserved. The isolated binary audit retained only cryptographic identity, metadata/resource identifiers, class/member signatures, registry counts/IDs, narrow branch/default-constructor facts and structured acquisition/progression references. No implementation bodies are copied or reconstructed, and no upstream assets, models, sounds or prose are imported into Black Arcana.

## Disposition

For Phase 2BG, the exact installed unconditional spell inventory is canonically `COUNTED_EXACT` under the same registry-level precedent used by other exact Iron's-addon closures: **+14 semantic magic objects**. Durable PR #195 clean HEAD `a9d7b55044230bbb011f7233ffd75d9a8321489b` passed CI #2503; squash merge `88f042f68429ff920314a7ec3a6923369edc93fd` passed exact-SHA post-merge CI #2504. The canonical repository totals are now **888 semantic objects / 56 of 100 provider components**.
