# Simply Swords — 1.70.2-1.21.1

Status: `⚠️ PARTIAL / PHYSICAL IDENTITY CLOSED / RELEASE-CORRELATED SOURCE CHECKPOINT / LOWER_BOUND 66 PLAYER-INVOKED ACTION ROOTS / LEGACY NON-OPTED INVENTORY + DEPLOYED REACHABILITY OPEN / +0 STRICT`

## Current physical authority

- sibling checkpoint: `neoforge-rpg-skilltree@51d590653d927538f23ba6f1643576dc6cc49859`;
- physical row: `#503`;
- JAR: `simplyswords-neoforge-1.70.2-1.21.1.jar`;
- mod id: `simplyswords`;
- runtime: `1.70.2-1.21.1`;
- physical SHA-1: `05b074ff774467f1fe9fb5592151b7845c321cbc`;
- sibling dossier publisher anchor: CurseForge File `8746001`, Simply Swords `1.70.2-1.21.1`.

Official file:
`https://www.curseforge.com/minecraft/mc-mods/simply-swords/files/8746001`

The publisher changelog for 1.70.2 names three changes:

- Epic Fight crash fix;
- Lootr loot-injection/pity fix;
- Simplified Chinese localization update.

Those runtime regression concerns are separate from semantic action counting.

## Release-correlated source authority

Official repository:

`https://github.com/Sweenus/SimplySwords`

Primary release-correlated checkpoint:

`Sweenus/SimplySwords@c82eeaf4479543a728340b9763ab445c9c9d4c0d`

This commit is the **Epic Fight crash fix named by the 1.70.2 publisher changelog**. It follows the source commit for the Lootr injection/pity fix (`91edb6e...`) and the localization update/merge already present on the branch. Therefore it is a stronger release-line anchor than an arbitrary moving-branch snapshot.

A later same-day cross-check:

`Sweenus/SimplySwords@359a8031b1a3243d1a3b013dbaa0cbba70ea8278`

declares `mod_version=1.70.2-1.21.1` and retains the **same 62 ACTIVE root IDs and the same four player-use Runic action families**. It adds one passive companion definition relative to the release-correlated fix checkpoint; that passive delta does not affect the semantic lower bound.

Neither checkpoint is claimed to be byte-identical to the physical CurseForge JAR.

## Canonical semantic metric boundary

The semantic ledger counts discrete provider-owned supernatural **player actions**. It does not count:

- items or weapon totals;
- passive gear/proc frameworks;
- status effects;
- weapon implicits triggered by hit/damage;
- Forge/UI/processes;
- loot/pity state;
- Awakening levels by themselves;
- downstream entities/projectiles/effects/events of one action.

That boundary is applied before arithmetic.

## 62 release-line registered active Unique ability roots

At the release-correlated checkpoint, `SimplySwords.init()` calls `BuiltinUniqueAbilities.register()`.

That registration path installs the built-in block and then `Phase2UniqueAbilities` through `Phase10UniqueAbilities`.

At `c82eeaf...` the source registers:

- **121 total `UniqueAbilityDefinition` roots**;
- **62 `ACTIVE` roots**;
- **59 `PASSIVE` roots**.

At the later version-declared cross-check `359a8031...`, the ACTIVE set remains exactly **62** while one additional passive companion brings PASSIVE to 60.

The provider's modifier API treats a `UniqueAbilityDefinition` as the root identity and lifecycle/events as children of that root. Therefore downstream HIT/FINISH/event identifiers do not create extra semantic objects.

ACTIVE subtotal by block at the release-correlated checkpoint:

| Block | ACTIVE | PASSIVE |
|---|---:|---:|
| Builtin | 2 | 3 |
| Phase 2 | 6 | 4 |
| Phase 3 | 7 | 5 |
| Phase 4 | 3 | 3 |
| Phase 5 | 6 | 5 |
| Phase 6 | 7 | 6 |
| Phase 7 | 4 | 6 |
| Phase 8 | 7 | 11 |
| Phase 9 | 13 | 8 |
| Phase 10 | 7 | 8 |
| **Total** | **62** | **59** |

The passive definitions are provider behavior but are **excluded** from the semantic-magic action count.

## Four countable Runic action families

`GemPowerRegistry` contains many Runic/Runefused/Nether power IDs, but the semantic metric does not count trigger-only powers.

At the same release-correlated checkpoint, only four causal power families implement the explicit player input hook `use(...)` and are reached through `GemPowerComponent.use(...)` from `RunicSwordItem.use(...)`:

1. `simplyswords:immolation`;
2. `simplyswords:momentum`;
3. `simplyswords:throwing`;
4. `simplyswords:ward`.

`greater_momentum` uses the same `MomentumPower` causal action with a stronger tier and is not counted as a second semantic action.

Runic action subtotal: **4**.

Other power classes observed at this release-line checkpoint are driven by `postHit`, `onSwing` or `inventoryTick` and are treated as equipment/proc/passive mechanics under the current metric.

## Weapon implicits are excluded

`WeaponImplicitRegistry.registerBuiltins()` registers **17** built-in implicit identities at the release-correlated checkpoint.

Their contract is limited to:

- damage modification;
- on-hit handling;
- incoming-damage cancellation.

They are equipment/proc behavior, not discrete player-invoked supernatural actions, and contribute **+0 semantic objects**.

## Current lower bound

`62 active Unique roots + 4 player-use Runic action families = 66`.

Therefore the current provider state is:

**LOWER_BOUND 66 / +0 STRICT**.

## Why 66 is not the final denominator

The provider's exact-line developer documentation states that existing abilities which do not opt into the `UniqueAbilityApi` continue to use the older `UniqueWeaponActiveAbility` contract.

Therefore the 62 registered `ACTIVE` definitions are a strong positive inventory, but **not proof that every player-invoked Unique ability in 1.70.2 is represented in that registry**.

The complete denominator remains open for:

- legacy/non-opted `UniqueWeaponActiveAbility` actions;
- any secondary-action path not represented by a registered active definition;
- disabled/config-gated content;
- Awakening unlock/reachability;
- exact current loot/survival acquisition where it changes practical reachability;
- direct-stack versus natural-drop Awakening state;
- addon deduplication against Simply More, Simply Swords: Cataclysm and other consumers.

## Config / Awakening boundary

`UniqueWeaponActiveAbility` checks `AwakeningApi.isAbilityUnlocked(stack)` before normal player activation.

The 1.70.x line is also config-breaking/save-sensitive. Source defaults are not treated as proof of the deployed pack's effective ability subset.

For that reason the 66 identities remain outside the strict global sum until complete active-action inventory and deployed reachability are closed.

## Ownership / integration boundary

Simply Swords remains authority for:

- base weapon types;
- Unique ability state;
- Runic Powers;
- weapon implicits;
- Runic Forge;
- Awakening;
- gem/tablet components;
- loot/pity state.

Addons may extend these systems but must not duplicate base-provider action identities or state.

Black Arcana must not duplicate provider damage/proc settlement, active ability lifecycle, cooldown/resource charging, Awakening, Runic state or loot/pity authority.

RPG Skill Tree remains sibling authority only for progression, attributes, Mastery, perks and gates through verified contracts.

## Clean-room / license note

Source license on the audited line: **Timefall Development License 1.2**.

The license permits use as a library/integration but prohibits bundling/publishing/distributing copies absent the stated permissions. Black Arcana retains only factual version/registry/behavior/contract information needed for cataloging and interoperability; no upstream implementation body or asset is copied.

## Closure gate

Promote Simply Swords beyond `LOWER_BOUND 66 / +0 STRICT` only after:

1. every legacy/non-opted player-invoked Unique action is enumerated and deduplicated;
2. secondary input paths are reconciled with registered active definitions;
3. disabled/config-gated active actions are classified;
4. deployed Awakening/reachability evidence is captured where it changes the active subset;
5. Runic powers remain separated into player-use actions versus proc/passive mechanics;
6. addon identities are deduplicated against the base provider;
7. the physical SHA-1 remains the cataloged 1.70.2 artifact.

Runtime Epic Fight/Lootr regression QA, Runic Forge transactions, persistence and save migration remain separate from semantic inventory closure.

## Result

**⚠️ Partial — release-correlated lower bound 66.**

Countable lower bound:

- **62** release-line registered `ACTIVE` Unique ability roots;
- **4** player-invoked Runic action families.

Documented but excluded:

- **59** PASSIVE definitions at the release-correlated fix checkpoint;
- one additional passive companion at the later version-declared cross-check;
- **17** weapon implicits;
- trigger-only/proc Gem Powers.

Strict global delta: **+0** until remaining legacy/non-opted active actions and deployed reachability are closed.
