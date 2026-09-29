# Simply Swords — 1.70.2-1.21.1

Status: `✅ CATALOGED / EXACT HASH-MATCHED ACTION DENOMINATOR 66 / DEPLOYED AWAKENING-CONFIG-REACHABILITY OPEN / +0 STRICT`

## Current physical authority

- sibling checkpoint: `neoforge-rpg-skilltree@a826e7773c79fd07d9afe40ace224ff83923c76e`;
- physical row: `#503`;
- JAR: `simplyswords-neoforge-1.70.2-1.21.1.jar`;
- mod id: `simplyswords`;
- runtime: `1.70.2-1.21.1`;
- physical SHA-1: `05b074ff774467f1fe9fb5592151b7845c321cbc`;
- publisher file: CurseForge File `8746001`.

The current sibling still records row #503 with the same JAR/version and `Magic` category.

## Exact artifact evidence

Non-merge evidence PR #448 materializes CurseForge File `8746001` through the exact Curse Maven coordinate and hard-gates SHA-1 equality against the current physical artifact.

Final bounded audit:

- audit PR: `#448`;
- audit branch SHA: `dd7f5450b93f4f6004a3f73b53b121898349d459`;
- audit workflow run: `36524073819` — **SUCCESS**;
- exact downloaded SHA-1: `05b074ff774467f1fe9fb5592151b7845c321cbc`;
- exact metadata: `simplyswords` / `1.70.2-1.21.1`;
- provider top-level classes: **666**;
- exact `UniqueAbilityDefinition` fields: **121**;
- exact registered concrete custom-item classes referenced by `ItemsRegistry`: **54**;
- exact registered classes whose provider inheritance chain implements `UniqueWeaponActiveAbility`: **51**;
- exact registered Secondary classes: **2**;
- unregistered concrete Active classes: **0**;
- unregistered concrete Secondary classes: **0**.

The audit retains only factual archive/class/interface/member/call-target facts required for denominator closure. Full disassembly and implementation bodies are not retained.

See [`EXACT-1.70.2-ARTIFACT-ACTION-AUDIT.md`](EXACT-1.70.2-ARTIFACT-ACTION-AUDIT.md).

## Release-correlated source authority

Official source repository: `Sweenus/SimplySwords`.

Two source checkpoints remain controlling for semantic classification:

- `c82eeaf4479543a728340b9763ab445c9c9d4c0d` — the Epic Fight crash fix named by the publisher's 1.70.2 changelog, after the listed Lootr fix and localization update;
- `359a8031b1a3243d1a3b013dbaa0cbba70ea8278` — later same-day cross-check explicitly declaring `mod_version=1.70.2-1.21.1`.

The later checkpoint preserves the same **62 ACTIVE** root IDs and the same four player-use Runic action families. It adds only one passive companion definition relative to the primary release-correlated checkpoint.

## Exact semantic denominator

The Black Arcana semantic metric counts discrete provider-owned supernatural **player actions**. It excludes passive/proc behavior, equipment containers, downstream lifecycle events/entities/effects, Awakening levels by themselves and infrastructure.

### 62 ACTIVE Unique roots

The release-correlated source closes **121** `UniqueAbilityDefinition` roots at the primary checkpoint:

- **62 ACTIVE**;
- **59 PASSIVE**.

The version-declared cross-check preserves the same 62 ACTIVE roots and has 60 PASSIVE roots.

The exact JAR independently contains **121 `UniqueAbilityDefinition` fields**, while the exact registered Active class set matches the version-declared source class set used for the 1.70.2 line. This removes the prior concern that an unenumerated legacy Active class existed outside the audited surface.

### Four player-use Runic action families

Exactly four Runic/Gem Power families have a causal player `use(...)` action on the audited release line:

1. `simplyswords:immolation`;
2. `simplyswords:momentum` — `greater_momentum` is the same action family at a stronger tier;
3. `simplyswords:throwing`;
4. `simplyswords:ward`.

Trigger-only/proc Runic powers remain excluded.

### Residual legacy/secondary surfaces add zero roots

The exact artifact narrows every residual registered player-action-shaped surface to four cases:

- `StormscaleSwordItem#startPlayerSecondaryAbility`;
- `WraithmawSwordItem#startPlayerSecondaryAbility`;
- `RighteousRelicSwordItem#use`;
- `TaintedRelicSwordItem#use`.

The exact JAR call-target audit closes them:

- Stormscale Secondary calls `StormscaleLightningRodManager.tryReactivate(...)` — a continuation/reactivation of the already-counted Stormscale Active root;
- Wraithmaw Secondary calls `WraithmawAbilityManager.tryDetonate(...)` — a continuation/detonation of the already-counted Wraithmaw Active root;
- Righteous Relic `use` delegates directly to `UniqueSwordItem.use(...)`;
- Tainted Relic `use` delegates directly to `UniqueSwordItem.use(...)`.

Therefore these four surfaces create **0 additional semantic roots**.

The exact artifact also proves:

- the registered Active class set matches the version-declared source set;
- the registered Secondary class set is exactly Stormscale + Wraithmaw;
- the registered non-Active direct-`use` set is exactly Righteous Relic + Tainted Relic;
- there are no unregistered concrete Active or Secondary classes in the exact artifact.

## Denominator arithmetic

`62 ACTIVE Unique roots + 4 player-use Runic roots + 0 residual legacy/secondary roots = 66`.

Current provider semantic inventory:

**EXACT ACTION DENOMINATOR 66 / +0 STRICT**.

The former `LOWER_BOUND 66` state is superseded. The identity/action denominator is closed; only deployed reachability remains open.

## Fichas canônicas

As 66 raízes exatas estão materializadas objeto-a-objeto em [ACTION-CARDS-1.70.2.md](ACTION-CARDS-1.70.2.md): 62 ACTIVE Unique roots e 4 famílias Runic de uso explícito. As fichas preservam o denominador e mantêm o strict fail-closed até a evidência implantada de reachability.

## Passive and non-action surfaces excluded

These remain provider behavior but do not add player-action identities:

- 59 PASSIVE definitions at the primary release-correlated checkpoint;
- one additional passive companion at the later version-declared checkpoint;
- 17 Weapon Implicits;
- trigger-only/proc Gem Powers;
- hit/incoming-damage hooks;
- Awakening progression state;
- Runic Forge/loot/pity/config UI infrastructure;
- downstream projectiles/entities/effects of one counted action.

## Deployed reachability remains open

`UniqueWeaponActiveAbility` activation is gated by `AwakeningApi.isAbilityUnlocked(stack)`, and the 1.70.x line is config/save-sensitive.

The following are still required before strict promotion:

1. authoritative deployed Awakening/unlock state for current obtainable stacks/forms;
2. current survival acquisition/reformation paths where they affect which of the 66 identities are practically reachable;
3. effective deployed config/datapack/script suppression affecting player availability;
4. exact compat-provider presence/gates where a source-defined root is conditionally materialized, including Dreadtide/Eldritch End if applicable;
5. final addon ownership/reachability reconciliation where base-provider and addon surfaces can overlap operationally.

Source defaults are not substituted for deployed state.

### Bounded deployed-evidence route

The read-only provider catalog collector now has a bounded Simply Swords 1.70.2 route.

It first fingerprints:

`simplyswords-neoforge-1.70.2-1.21.1.jar`

against the canonical physical/publisher SHA-1:

`05b074ff774467f1fe9fb5592151b7845c321cbc`.

The release-line source checkpoint `359a8031b1a3243d1a3b013dbaa0cbba70ea8278`
declares Fzzy Config `0.7.6+1.21`, `GeneralConfig` id
`simplyswords:general` and `LootConfig` id `simplyswords:loot`.
Fzzy Config 0.7.6 derives the default folder/name from the config identifier and
uses TOML by default, so the collector is bounded to:

- `config/simplyswords/general.toml` → `enableUniqueWeaponAwakening`;
- `config/simplyswords/loot.toml` → `enableLootDrops`,
  `runicLootTableWeight`, `uniqueLootTableWeight`,
  `enableContainedRemnants`, `disabledUniqueWeaponLoot` and
  `uniqueLootTableOptions`.

Missing files/keys, duplicate observations, invalid booleans/numbers and invalid
resource locations remain explicit fail-closed states. No unrelated config values
are retained.

This route closes only a bounded part of deployed reachability. It does **not**
prove per-stack Awakening level/unlock state, complete acquisition/reformation,
compat-dependent materialization, or addon ownership.

See [DEPLOYED-REACHABILITY-CHECKLIST.md](DEPLOYED-REACHABILITY-CHECKLIST.md).

## Ownership / integration boundary

Simply Swords remains authority for Unique abilities, Runic Powers, Weapon Implicits, Runic Forge, Awakening, gem/tablet components and loot/pity state.

Black Arcana must not duplicate provider activation, cooldown/resource charging, Awakening, proc settlement, Runic state or loot/pity authority.

RPG Skill Tree remains sibling authority only for progression, attributes, Mastery, perks and gates through verified contracts.

## Clean-room / license

The audited source line declares the Timefall Development License 1.2. Black Arcana retains only factual metadata, IDs, class/interface/member structure, bounded call-target facts and behavior-level semantics needed for cataloging/interoperability. No upstream implementation body or protected asset is copied.

## Result

**✅ Cataloged — exact action denominator closed at 66 and all 66 roots are materialized object-by-object.**

- exact current action denominator: **66**;
- strict semantic contribution: **+0**;
- remaining runtime/reachability gate: deployed Awakening/config/acquisition/compat reachability;
- runtime Epic Fight/Lootr regression QA, persistence, Runic Forge transactions and save migration remain separate from semantic inventory closure.