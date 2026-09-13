# Ars Nouveau: Two-Way Portals 2.0.0 — exact-artifact audit

## Evidence identity

- audit branch: `audit/ars-two-way-portals-2.0.0-exact-artifact`;
- evidence PR: #222 — **NON-MERGE**;
- audited HEAD: `9a3620209e27bb74934c8a9740678b7e59df39c6`;
- audit workflow run: `34735280002` — GREEN;
- text-only evidence artifact: `10311071402`;
- artifact digest: `sha256:908bad67ee1d98aa0da19ec90750dfeb0636c8ff7c211367e30217b7e593a898`;
- publisher artifact SHA-256 observed by the audit: `616a07c0510ca7222698d90e365ae0c70b7a7c3d1f296acada8f5354a7be4166`.

## Hash gate

The workflow downloaded CurseForge project/file `1599062 / 8515817` and refused to proceed unless the downloaded SHA-1 exactly equaled the physical-pack authority:

`233846fc30667893c5f36a719da576d5eed43f5c`

The gate passed. The audited publisher artifact is therefore the exact installed binary identity for this catalog purpose.

## Exact metadata

`META-INF/neoforge.mods.toml` establishes:

- mod id `ars_two_way_portals`;
- version `2.0.0`;
- license `LGPL-3.0-or-later`;
- environment BOTH;
- required NeoForge `[21.1.243,)`;
- required Minecraft `[1.21.1,1.21.2)`;
- required Ars Nouveau `[5.12.1,6.0.0)`;
- optional Immersive Portals mod id `immersive_portals_core` `[6.0.7,7.0.0)`;
- mixin config `ars_two_way_portals.mixins.json`.

The exact metadata resolves the historical 1.3.4-source uncertainty about the optional Immersive mod id.

## Exact structural summary

| Surface | Exact result |
|---|---:|
| provider classes | 25 |
| provider item register surfaces | 1 |
| provider item members | 2 |
| provider recipe resources | 3 |
| mixin configs | 1 |
| required common mixins | 7 |
| semantic spell/glyph/ritual/rite/ability resource paths | 0 |

The exact item members exposed by signatures are `DOUBLE_SIDED_STABLE_WARP_SCROLL` and `PORTAL_NULLIFY_SCROLL`. The exact recipe-resource paths are `double_sided_stable_warp_scroll`, `portal_nullify_scroll` and `reset_double_sided_stable_warp_scroll` under the provider recipe namespace.

## Exact mixin footprint

`ars_two_way_portals.mixins.json` is `required=true`, Java 21, `defaultRequire=1`, with:

1. `BlockUtilMixin`;
2. `EffectBreakMixin`;
3. `EffectLaunchMixin`;
4. `EffectLeapFrameMixin`;
5. `PortalBlockMixin`;
6. `PortalTileMixin`;
7. `StableWarpScrollMixin`.

This proves the exact 2.0.0 mixin inventory. It does not prove successful application on the assembled pack; that remains runtime QA.

## Semantic-registry exclusion evidence

Narrow constant-pool/class indicators on the exact artifact produced:

| Indicator | Classes hit |
|---|---:|
| `AbstractSpell` | 0 |
| `AbstractGlyph` | 0 |
| `SpellRegistry` | 0 |
| `registerSpell` | 0 |
| `Ritual` | 0 |
| `Rite` | 0 |
| `Ability` | 0 |

Archive-path inspection also found zero spell/glyph/ritual/rite/ability semantic resource paths.

By contrast, exact artifact indicators and signatures do show Ars `PortalTile`, `PortalBlock`, `StableWarpScroll`, provider pair/nullification/cooldown/frame services, and both `immersive_portals`-text and `immersive_portals_core`-text references. Exact metadata determines the actual optional dependency id as `immersive_portals_core`.

## Classification

The exact artifact supports:

- primary classification: `BRIDGE_COMPAT` / portal infrastructure;
- secondary content: provider items + recipes;
- semantic classification: `ZERO_SEMANTIC_PORTAL_INFRA`;
- semantic delta: **+0**.

The provider alters Ars warp/portal behavior but does not establish an independent spell/glyph/ritual/rite/ability registry. Item and recipe surfaces are not separately counted as semantic magic objects under the current ledger definition.

## Runtime fail-closed boundary

Not proven by this exact structural audit:

- successful application of all required mixins on the full pack;
- effective deployed provider config values;
- live pair creation/teleport/nullification/rotation behavior;
- save/reload/restart/chunk lifecycle;
- optional Immersive behavior on the assembled host;
- current frame mutation path and Weave semantics;
- multiplayer isolation, duplicate processing and world-protection interop.

No runtime PASS or Black Arcana adapter is inferred.

## Clean-room boundary

The JAR is not committed or redistributed. Durable evidence records only hashes, metadata/dependency ranges, class/resource paths, mixin configuration, signatures, counts and narrow indicator presence. No method bodies, assets, localization prose, models or sounds are copied/adapted.
