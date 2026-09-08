# Ars Two-Way Portals — mixin, frame and Immersive boundaries

Status: `1.3.4 BASELINE IMPLEMENTATION CATALOGED / 2.0.0 EXACT MIXINS UNKNOWN`

## Baseline mixins — 7

The public 1.3.4 `ars_two_way_portals.mixins.json` is required and declares:

1. `BlockUtilMixin`
2. `EffectBreakMixin`
3. `EffectLaunchMixin`
4. `EffectLeapFrameMixin`
5. `PortalBlockMixin`
6. `PortalTileMixin`
7. `StableWarpScrollMixin`

It targets Java 17-era Forge/Ars internals. The physical 2.0.0 JAR merely confirms a mixin config named `ars_two_way_portals.mixins.json`; Phase 2Z does not claim that the exact list/targets survived the NeoForge 1.21.1 port.

## Historical frame hooks

The 1.3.4 baseline:

- intercepts Ars `EffectBreak` + Extract and `BlockUtil.breakExtraBlock` to protect a tracked frame removal;
- blocks Ars `EffectLaunch` from moving a tracked frame;
- redirects `EffectLeap` so a tracked frame block can be removed without immediately collapsing the pair;
- bypasses normal PortalBlock neighbor-shape collapse for linked regular portals;
- uses temporary protected-removal sets/maps to distinguish intended frame mutation from pair destruction.

### 2.0.0 release-specific correction

The publisher explicitly says that for the 1.21.1 release, the old Silk Touch frame-removal/replacement function was replaced by Ars Nouveau **Weave blocks**. The same project description still contains older generic text mentioning Leap/Silk Touch/Break+Extract.

Phase 2Z therefore does not project the seven old frame mixins onto the installed version. Exact 2.0.0 binary inspection must determine which historical hooks survived, changed or disappeared.

## Optional Immersive Portals baseline

The 1.3.4 source imports `qouteall.imm_ptl` APIs and, when old mod id `immersive_portals` is loaded, can:

- convert accepted Ars portal geometry into Immersive `Portal` entities;
- derive a canonical transform and complete a bi-way bi-faced portal set;
- assign a provider pair tag;
- persist frame geometry on portal entity data;
- remove overlapping Ars PortalBlocks after conversion;
- validate tracked frames on a periodic server tick;
- handle Dominion Wand rotation and gravity-transform state;
- destroy/nullify provider-owned Immersive portal pairs/endpoints through the integration layer.

The baseline frame validator iterates loaded levels/entities every 10 server ticks looking at provider-tagged portal entities. This is a performance-sensitive historical implementation detail and requires exact 2.0.0/runtime validation; Black Arcana must not reproduce it as a generic global scan.

## Current physical Immersive boundary

The pack's current top-level entry is:

- file: `Immersive-Aeronautics1.1.4-1.21.1-NeoForge.jar`;
- exposed mod id: `immersive_portals_core`;
- displayed provider: Immersive Portals;
- version: `6.0.7`.

It also contains `immersive_portals_true_immersion` 2.0.4 as another top-level addon.

The old source gate `ModList.isLoaded("immersive_portals")` does not match the current top-level mod id. This does **not** prove the installed 2.0.0 bridge is broken, because its exact port source/binary has not been inspected. It is a concrete compatibility QA gate.

## Black Arcana boundary

- Do not depend directly on these mixins as a stable API.
- Do not perform a second teleport after Ars/Two-Way/Immersive accepted movement.
- Do not mirror provider pair tags, frame state or cooldown into BA persistence.
- BA-owned block/portal mutation still routes through `WorldEffectPolicy` and Stage 07.04 destination safety.
- Provider frame mutation behavior does not authorize BA to bypass claims/protection/world-border checks.
- Missing compatible optional integration => fail closed rather than fabricating a portal-engine fallback.
