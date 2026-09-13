# Ars Nouveau: Two-Way Portals 2.0.0 — exact artifact catalog

## Status

`EXACT HASH-MATCHED 2.0.0 ARTIFACT / NEOFORGE 1.21.1 / PORTAL+COMPAT INFRASTRUCTURE / 2 ITEMS / 3 RECIPES / 7 REQUIRED MIXINS / ZERO SPELL-GLYPH-RITUAL-RITE-ABILITY SURFACE / ZERO_SEMANTIC_PORTAL_INFRA / COMPONENT #65 CANDIDATE / RUNTIME QA FAIL-CLOSED`

## Installed identity

Current physical-pack authority:

- provider: **Ars Nouveau: Two-Way Portals**;
- mod id: `ars_two_way_portals`;
- installed JAR: `ars_two_way_portals-2.0.0.jar`;
- runtime version: `2.0.0`;
- physical SHA-1: `233846fc30667893c5f36a719da576d5eed43f5c`;
- physical CurseForge hash: `683033210`;
- CurseForge project/file: `1599062 / 8515817`;
- publisher file: release, NeoForge, Minecraft 1.21.1, uploaded 2026-07-26;
- publisher license: LGPLv3.

Phase 2BQ exact-artifact audit run `34735280002` materialized CurseForge file `8515817` and hard-required SHA-1 equality with the physical pack. The downloaded artifact matched exactly and produced SHA-256 `616a07c0510ca7222698d90e365ae0c70b7a7c3d1f296acada8f5354a7be4166`.

Text-only clean-room evidence artifact: `10311071402`, digest `sha256:908bad67ee1d98aa0da19ec90750dfeb0636c8ff7c211367e30217b7e593a898`.

## Exact 2.0.0 structural inventory

The exact JAR contains:

- **25** provider classes;
- one provider item `DeferredRegister.Items` surface;
- exactly **2** provider `DeferredItem` members:
  - `DOUBLE_SIDED_STABLE_WARP_SCROLL` → `DoubleSidedStableWarpScroll`;
  - `PORTAL_NULLIFY_SCROLL` → `PortalNullifyScroll`;
- exactly **3** provider recipe resources:
  - `double_sided_stable_warp_scroll.json`;
  - `portal_nullify_scroll.json`;
  - `reset_double_sided_stable_warp_scroll.json`;
- exactly **1** mixin config, `ars_two_way_portals.mixins.json`;
- exactly **7 required common mixins** with `defaultRequire=1`:
  - `BlockUtilMixin`;
  - `EffectBreakMixin`;
  - `EffectLaunchMixin`;
  - `EffectLeapFrameMixin`;
  - `PortalBlockMixin`;
  - `PortalTileMixin`;
  - `StableWarpScrollMixin`.

The exact `DoubleSidedStableWarpScroll` extends Ars Nouveau `StableWarpScroll`. Exact class signatures also establish provider-owned portal-pair, regular-portal, nullification, cooldown, frame-hook and optional Immersive integration services.

## Exact semantic disposition

The exact 2.0.0 artifact has:

- `AbstractSpell` class hits: **0**;
- `AbstractGlyph` class hits: **0**;
- `SpellRegistry` class hits: **0**;
- `registerSpell` class hits: **0**;
- Ritual class hits: **0**;
- Rite class hits: **0**;
- Ability class hits: **0**;
- spell/glyph/ritual/rite/ability resource paths: **0**.

Under the current semantic-magic metric, the two scroll items, their recipes and portal lifecycle infrastructure are not independent spells, glyphs, rituals, rites or equivalent provider-owned cast actions. Phase 2BQ therefore assigns:

`ZERO_SEMANTIC_PORTAL_INFRA` / semantic delta **+0**.

The strict reconstructible semantic minimum remains **1332**. This provider may close a technical component without increasing the semantic numerator.

## Exact dependency boundary

Exact `neoforge.mods.toml` declares:

- NeoForge `[21.1.243,)` — physical pack `21.1.248` satisfies the declared range;
- Minecraft `[1.21.1,1.21.2)` — physical pack is 1.21.1;
- Ars Nouveau `[5.12.1,6.0.0)` — physical pack uses 5.13.1;
- optional `immersive_portals_core [6.0.7,7.0.0)`.

This resolves the old Phase 2Z source-baseline uncertainty about the optional mod id: exact 2.0.0 targets `immersive_portals_core`, not the old 1.3.4 source gate `immersive_portals`. The physical pack's previously reconciled Immersive surface exposes `immersive_portals_core` 6.0.7, matching the exact declared lower bound.

Dependency-range satisfaction is not a runtime PASS.

## Publisher-described gameplay surface

The exact release/project documentation establishes the intended user-facing role:

- permanent linked two-way Ars portal pairs from the Double-Sided Stable Warp Scroll;
- vertical/horizontal and cross-dimension pairing;
- regular Ars portal mode with a three-second re-entry cooldown;
- optional seamless Immersive mode;
- Dominion Wand pair rotation/gravity behavior;
- one-endpoint Portal Nullify Scroll behavior;
- reset recipe for a configured double-sided scroll;
- a 1.21.1 release note replacing the older Silk Touch-specific frame replacement statement with Ars Weave-block behavior.

These statements describe provider behavior and acquisition surfaces. They do not create semantic spell identities under the current metric.

## Runtime QA boundary

Still fail-closed until directly exercised on the assembled physical host:

- client/full-pack boot with all seven required mixins applied;
- exact current config values for the four Boolean feature surfaces exposed by `PortalConfig`;
- regular versus Immersive pair creation under the installed optional stack;
- pair persistence across chunk unload/reload, reconnect and server restart;
- cross-dimension endpoint lifecycle;
- exactly-once regular cooldown behavior across multi-block portal faces;
- one-endpoint nullification and ordinary pair teardown;
- frame mutation/Weave behavior under the current Ars build;
- Dominion Wand rotation/gravity interop;
- duplicate-processing and claim/world-safety behavior.

No Black Arcana runtime adapter is promoted by this catalog closure.

## Authority boundary

Ars Nouveau owns the base warp scroll, portal block/tile and warp primitives. Two-Way Portals owns its pair lifecycle, provider items, cooldown/nullification/frame behavior and optional Immersive bridge. Immersive Portals remains authority for its portal entities/engine when that integration is active.

Black Arcana must not duplicate provider portal state, cooldown, teleport settlement, pair destruction or optional portal-engine behavior. BA-owned world mutation continues to obey its own `WorldEffectPolicy` and server-authoritative safety contracts.

## Provenance / clean-room

The official public repository still exposes the **1.3.4 / Minecraft 1.20.1 / Forge** source line, not an exact 2.0.0 source pin. Phase 2BQ therefore treats the exact hash-matched JAR as binary authority and uses the public older source only as historical architecture context where explicitly labeled.

Evidence retained from the exact JAR is limited to cryptographic identity, metadata/dependency ranges, archive/resource paths, mixin configuration, class/member/type signatures and narrow indicator presence. No implementation bodies or assets are copied/adapted into Black Arcana.
