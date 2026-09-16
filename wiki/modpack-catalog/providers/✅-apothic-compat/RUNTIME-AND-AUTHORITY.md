# Apothic Compat 2.0.2 — runtime and authority

## Initialization/runtime shape

Exact entry point: `@Mod("apothic_compat")`.

The constructor registers the mod instance on `NeoForge.EVENT_BUS`. The exact source has three subscribed runtime hooks:

1. `RegisterCommandsEvent`
   - registers `/apothiccompat reload`;
   - registers `/ac` as a permission-level-2 redirect.
2. `ServerStartedEvent`
   - loads the provider config;
   - reapplies the affix blacklist after the host affix registry is available.
3. `OnDatapackSyncEvent`
   - re-runs blacklist application only for full sync/reload (`getPlayer() == null`);
   - ignores per-player sync because it does not rebuild the host pool.

Loot-category overrides themselves are not handled by those events. They are data consumed by Apotheosis.

## Runtime metadata

Exact NeoForge metadata declares:

- loader `javafml`, loader range `[4,)`;
- Minecraft `[1.21.1,1.22)`;
- NeoForge `[21.1.0,)`;
- required Apotheosis `[8.5,9)`;
- `displayTest="IGNORE_SERVER_VERSION"`;
- license `MIT`.

The source/readme identifies the 1.21.1 build as server-side. The provider data map and blacklist execute server-side; Apotheosis remains responsible for syncing its category state to clients.

## Exact dependency/version boundary

Exact build baselines:

- NeoForge 21.1.230;
- Apotheosis 8.5.4;
- Placebo 9.9.1;
- Apothic Attributes 2.9.1.

Physical pack:

- NeoForge 21.1.248;
- Apotheosis 8.8.0;
- Placebo 9.9.2;
- Apothic Attributes 2.10.1.

The declared Apotheosis dependency range includes physical 8.8.0, but the blacklist reaches the host private field name `AffixRegistry.byType` through reflection. A declared semantic version range is not proof that this private field remains identical. Therefore full-pack runtime blacklist QA stays fail-closed.

## Failure behavior

The exact blacklist implementation is deliberately bounded around several failure cases:

- empty provider blacklist: no reflective rewrite;
- empty host affix registry: skip instead of overwriting host pool with empty state;
- a third-party affix throws during `id()`/`definition()`: skip that affix and continue the rebuild;
- unknown configured IDs: warn and skip;
- reflective field access/write fails: warn and return 0 rather than throwing the failure outward.

This reduces blast radius but does not convert the private reflection seam into a stable public API.

## Authority table

| Surface | Authority |
|---|---|
| loot-category registry/data-map type and category semantics | Apotheosis |
| category synchronization | Apotheosis |
| 13 contributed item overrides | Apothic Compat data |
| affix identities/definitions/backing registry | Apotheosis + owning addon namespace |
| provider config file and selected blacklist IDs | Apothic Compat |
| provider reconstruction/filter of the host `byType` pool | Apothic Compat compatibility runtime over Apotheosis internals |
| BA casts/costs/targeting/cooldowns/charges | Black Arcana |
| BA Corruption/Strain/Arcane Danger/Backlash | Black Arcana |
| destructive BA world changes | Black Arcana `WorldEffectPolicy` |
| progression/Mastery/perks | RPG Skill Tree through real contracts only |

## Deduplication rules

Black Arcana must not:

- create a second loot-category override for the same 13 items merely to make magic affixes work;
- treat `apotheosis:bow` as a BA spell-domain classification;
- use Apothic Compat's reflection seam as BA's generic way to suppress proc families;
- assume an affix blacklist constitutes server-authoritative BA cooldown/cast prevention;
- deliberately route Backlash through normal offensive affix procs;
- transfer Black Arcana's magic authority to Apotheosis, Apothic Compat or RPG Skill Tree.

If a future BA feature needs to suppress or classify provider affixes, a current supported provider-native API/data contract must be proven first. The private `byType` reflection used by this compatibility mod is evidence of this provider's own implementation, not an endorsed BA extension contract.
