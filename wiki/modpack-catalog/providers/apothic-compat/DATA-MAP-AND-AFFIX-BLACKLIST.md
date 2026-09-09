# Apothic Compat 2.0.2 — data map and affix blacklist

## Loot-category authority

The exact 1.21.1 source does not register or patch a parallel category system. It contributes to the NeoForge data map owned by Apotheosis at:

`data/apotheosis/data_maps/item/loot_category_overrides.json`

All 13 exact values target `apotheosis:bow`:

| Item ID | Category |
|---|---|
| `alexscaves:raygun` | `apotheosis:bow` |
| `alexscaves:dreadbow` | `apotheosis:bow` |
| `alexsmobs:hemolymph_blaster` | `apotheosis:bow` |
| `alexsmobs:blood_sprayer` | `apotheosis:bow` |
| `born_in_chaos_v1:pumpkinhandgun` | `apotheosis:bow` |
| `cataclysm:cursed_bow` | `apotheosis:bow` |
| `cataclysm:wrath_of_the_desert` | `apotheosis:bow` |
| `cataclysm:void_assault_shoulder_weapon` | `apotheosis:bow` |
| `cataclysm:wither_assault_shoulder_weapon` | `apotheosis:bow` |
| `cataclysm:laser_gatling` | `apotheosis:bow` |
| `undergarden:slingshot` | `apotheosis:bow` |
| `twilightforest:block_and_chain` | `apotheosis:bow` |
| `twilightforest:cube_of_annihilation` | `apotheosis:bow` |

The exact publisher/source rationale is that these ranged/thrown items are not reliably categorized by Apotheosis 8.x's normal item-class/attack-damage predicates. `bow` is used because the relevant Apotheosis affixes hook projectile-hit behavior.

No provider code iterates these 13 entries. Apotheosis loads the data map itself.

## Affix blacklist config

The exact provider config is a manually managed NightConfig file:

`config/apothic_compat-common.toml`

There is exactly one semantic config key:

`affix_blacklist = []`

It accepts an array of `namespace:path` affix IDs. Invalid/non-string entries are skipped with warnings; duplicate IDs collapse through a `LinkedHashSet`.

The stated semantics are:

- prevent selected affixes from future rolling on generated/reforged/traded/gem-applied gear;
- existing items keep affixes already present;
- provider does not remove the affix from the backing registry;
- Apotheosis datapack affix overrides remain provider authority.

## Application algorithm

`AffixBlacklist.apply()`:

1. reads the current blacklist snapshot;
2. if the set is empty, returns `0` without touching the host pool;
3. reads all `AffixRegistry.INSTANCE.getValues()`;
4. if the registry is empty, returns without rewriting it;
5. rebuilds a new `Multimap<AffixType, DynamicHolder<Affix>>`, omitting IDs in the blacklist;
6. catches failures per individual third-party affix so one broken affix does not abort the rebuild;
7. warns for blacklist IDs that matched no registered affix;
8. reflectively obtains the private field named `byType` from `AffixRegistry`;
9. replaces that field on `AffixRegistry.INSTANCE` with the rebuilt map;
10. catches reflection/runtime failure and logs instead of propagating it.

The backing affix registry remains intact.

## Reapplication lifecycle

Blacklist application occurs:

- on `ServerStartedEvent`;
- after a full `OnDatapackSyncEvent`, detected by `event.getPlayer() == null`;
- via the provider reload command.

This exists because Apotheosis rebuilds its affix-by-type pool on datapack reload.

## Reload command behavior

Both command roots require permission level 2:

- `/apothiccompat reload`
- `/ac reload`

The short alias redirects to the same command root.

The reload path tracks file modification time plus a byte-content hash to report no-op edits and returns the count of affixes disabled by the latest apply operation.

## Exact empty-blacklist asymmetry

The exact source has a static behavioral edge case that must not be papered over:

- assume the current `byType` pool has already been filtered by a non-empty provider blacklist;
- edit `affix_blacklist` to `[]`;
- run only `/ac reload`;
- `setBlacklist(empty)` succeeds, but `AffixBlacklist.apply()` immediately returns because the set is empty;
- therefore that method does not reconstruct/restore the already-filtered host `byType` map.

A subsequent lifecycle where Apotheosis itself rebuilds the pool first — normal datapack reload or server restart — restores the full pool before the provider reapplies the now-empty blacklist.

This is recorded as **STATIC QA / RUNTIME REGRESSION REQUIRED**, not as an intended semantic guarantee.

## Black Arcana implications

- item loot categories are Apotheosis authority, not BA spell-domain tags;
- affix blacklist state is not a BA proc/cooldown/cast policy surface;
- BA must not reflect into `AffixRegistry.byType` to implement Arcane Danger, Backlash or magic gating;
- any future interop must use a verified provider/Apotheosis contract and preserve host causal/proc semantics.
