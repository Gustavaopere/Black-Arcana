# Traveloptics Blackout — bounded versioned acquisition-surface audit

Status: `DIRECT IRON'S CONSTRUCTION/LOOKUP SURFACES NEGATIVE / REVIEWED GENERIC ITEM+REWARD CANDIDATES NON-ACQUISITIVE / DYNAMIC+EXTERNAL+CURRENT-PHYSICAL ROUTES UNRESOLVED / FAIL-CLOSED`

## Purpose

This checkpoint narrows Gate 3 for `traveloptics:blackout` beyond the previously audited literal, `SpellFilter` / `RandomizeSpellFunction`, global-loot-modifier, progression and script/resource surfaces.

The bounded question is:

> Do the current versioned Black Arcana or RPG Skill Tree `src/main` trees directly use the pinned Iron's 3.16.3 APIs/components that construct spell-bearing scroll/imbued containers, or common direct item/command delivery primitives that resolve into a Blackout acquisition route?

For the exact mechanisms audited below, **no Blackout acquisition route is present**.

This is not a proof that every conceivable Java/data route is absent.

## Authority pins

Black Arcana:

- repository: `Gustavaopere/Black-Arcana`;
- audited main: `da8a5c1806c863e91b7ff5383c62761538236f52`.

RPG Skill Tree:

- repository: `Gustavaopere/neoforge-rpg-skilltree`;
- audited sibling: `de80b186357cad20ba5b81892a8682777e96e35a`.

Iron's host API context:

- current host line: `1.21.1-3.16.3`;
- source pin already used by the Traveloptics dossier: `iron431/irons-spells-n-spellbooks@e4056af90302d37eb1739f5ff05020b020e6e252`;
- relevant direct construction surfaces include `ISpellContainer.createScrollContainer`, `createImbuedContainer`, mutable `addSpellAtIndex` / `addSpell`, `ISpellContainer.set`, `ComponentRegistry.SPELL_CONTAINER`, and scroll/spell registry lookup identities.

## Reproducible audit packet

Temporary NON-MERGE PR: **#654**.

Authoritative v2:

- audit HEAD: `561bfc82b0bb81c13fb1f84df768e5420e081b12`;
- workflow run: `37340830240` — **SUCCESS**;
- job: `111867158851`;
- report internal SHA-256: `77b26e07d1ba624618ccb1ff86cfc91db53b1206aec9cb6167d5202ce3c2359a`;
- text artifact: `11357878274`;
- artifact digest: `sha256:4b60a06e4e9da8261aaddf1128a046c1ba218814d817c8270338b62a865ab1c6`.

The first #654 run is superseded because it scanned selected text extensions under resources. v2 scans every file under both pinned `src/main/resources` trees as a byte blob decoded only for bounded ASCII-token matching.

## Complete pinned `src/main` coverage

| Repository | Java files audited | Resource blobs audited |
|---|---:|---:|
| Black Arcana | 482 | 22 |
| RPG Skill Tree | 1,144 | 724 |

The Java scan retained only occurrence counts and matching paths. The resource scan retained only occurrence counts and matching paths. No source bodies were retained by the audit artifact.

## Direct Iron's spell/scroll materialization surfaces

Across **both** pinned repositories, every audited direct Iron's construction/lookup token returned **0 occurrences**:

| Surface | Black Arcana | RPG Skill Tree |
|---|---:|---:|
| `ISpellContainer.createScrollContainer(...)` | 0 | 0 |
| `ISpellContainer.createImbuedContainer(...)` | 0 | 0 |
| `ISpellContainer.set(...)` | 0 | 0 |
| `.addSpellAtIndex(...)` | 0 | 0 |
| `.addSpell(...)` | 0 | 0 |
| `ComponentRegistry.SPELL_CONTAINER` | 0 | 0 |
| `ItemRegistry.SCROLL` | 0 | 0 |
| `SpellDataRegistryHolder` | 0 | 0 |
| `new SpellData(...)` | 0 | 0 |
| `SpellRegistry.getSpell(...)` | 0 | 0 |

This excludes those **specific direct versioned construction/lookup paths** as a project-owned route that could synthesize a Blackout scroll/spell container without naming Blackout literally.

## Versioned runtime resources

Across all audited `src/main/resources` blobs in both repositories:

- `traveloptics:blackout`: **0**;
- `traveloptics`: **0**;
- `irons_spellbooks:scroll`: **0**;
- `irons_spellbooks:spell_container`: **0**;
- generic `spell_container` token: **0**.

This extends the earlier JSON-only/resource-specific checks to the complete pinned resource trees.

It does not inspect user/world datapacks, external KubeJS folders, third-party mod resources or the current physical Traveloptics JAR.

## Generic delivery candidates — Black Arcana

The bounded generic primitive scan found:

- player `.addItem(...)`: **0**;
- `.spawnAtLocation(...)`: **0**;
- command-dispatch primitive: **0**;
- `CommandSourceStack`: **0**;
- inventory `.add(...)`: **1**;
- entity/player `.drop(...)`: **1**;
- `new ItemStack(...)`: **16 occurrences across 6 paths**.

Direct review resolves the production candidates:

- `NeoForgeMalumSpiritInventoryAccess` creates/refunds only Malum `<affinity>_spirit` items and may return a failed refund through the player's inventory/drop path;
- `CuriosEquipmentSnapshotAdapter`, `MinecraftEchoArmamentRuntime`, `MinecraftNoeticObservationRuntime` and `MinecraftStandardEquipmentSnapshotAdapter` read existing item identities/equipment; they do not grant provider spells;
- the remaining `new ItemStack(...)` paths are Black Arcana GameTest classes.

The Black Arcana Iron's integration itself was also checked semantically:

- `IronsSpellRegistryBridge` registers only Black Arcana's own `irons_integration_probe`;
- `IronsSyntheticContent` installs the Black Arcana-owned synthetic probe definition/cooldown/runtime;
- neither is a provider-scroll acquisition route.

## Generic delivery candidates — RPG Skill Tree

The bounded generic primitive scan found:

- player `.addItem(...)`: **0**;
- inventory `.add(...)`: **0**;
- `.spawnAtLocation(...)`: **0**;
- entity/player `.drop(...)`: **0**;
- command-dispatch primitive: **0**;
- `CommandSourceStack`: **5 occurrences**, all in `VolcanoAdminCommands`;
- `new ItemStack(...)`: **11 occurrences across 7 paths**.

Direct review resolves the production candidates:

- six `new ItemStack(...)` paths are GameTest classes;
- `CompendiumStaticPreviewRegistryResolver` constructs a block-as-item stack for static UI preview and does not grant it to a player/world;
- `GoetyProgressionEvents`, `MalumProgressionEvents`, `RuntimeFloraCatalogCollector`, Curios/pressure runtime and the sustain runtime read existing registry/item state rather than creating Iron's scrolls;
- `VolcanoAdminCommands` defines its own volcano administration command surface; the repository-wide command-dispatch token count is zero, so it is not a generic nested command executor.

The reward/progression candidates were separately checked:

- `CompendiumDiscoveryRewardBridge` rejects every reward kind except `CHARACTER_XP`;
- `BossRewardDefinition` contains only `id` + integer `points`;
- `RewardRiskLootModifier` delegates to `EntityRewardLootRuntime`, which transforms already-generated loot rather than selecting a new provider item/spell identity;
- `IronsCitizenMagicBridge` accepts/casts existing `SpellData`; it does not construct a scroll or grant a spell.

## What this establishes

For Black Arcana `da8a5c18...` and RPG Skill Tree `de80b186...`:

- exact/literal Blackout project-owned route — already **NOT FOUND** by the prior checkpoint;
- named `SpellFilter` / `RandomizeSpellFunction` route — already **NOT FOUND**;
- direct Iron's spell-container/scroll construction APIs listed above — **NOT USED** in either pinned `src/main/java` tree;
- direct resource identities for Traveloptics/Blackout/Iron's scroll/spell-container — **NOT PRESENT** in either pinned `src/main/resources` tree;
- reviewed project-owned generic item/reward candidates — **NO BLACKOUT ACQUISITION ROUTE IDENTIFIED**.

This materially narrows the versioned project-owned exception space left open by the previous audit.

## What this does not establish

This audit does **not** prove universal absence of every acquisition-capable Java/data path.

Still unresolved:

- reflection, method handles, encoded names or other dynamic invocation not containing the audited tokens;
- arbitrary custom logic that could encode an equivalent spell-bearing item without the named Iron's APIs/tokens;
- assembled external KubeJS/server/startup scripts outside these repositories;
- user/world datapacks or command blocks;
- other installed mods;
- current physical Traveloptics SHA-1 `7b74816e89cc15dd0b5a31d9ea1e456024e8fae4`;
- live current-world survival acquisition.

Therefore Gate 3 remains **OPEN**.

## Gate 3 consequence

Blackout can now be classified more narrowly as:

`REGISTERED / UNIQUE / NON-CRAFTABLE / NON-LOOTABLE IN EXACT ALPHA / PROVIDER BUILT-IN ROUTES EXCLUDED / NAMED FILTER ROUTES NEGATIVE / AUDITED DIRECT VERSIONED SPELL-CONSTRUCTION + ITEM-DELIVERY SURFACES NEGATIVE / DYNAMIC + ASSEMBLED EXTERNAL + CURRENT-PHYSICAL ROUTES UNVERIFIED`.

No acquisition route is synthesized by Black Arcana.

No semantic count changes.

Traveloptics remains **⚠️ partial/conditioned / strict +0**.
