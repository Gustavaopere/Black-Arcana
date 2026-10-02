# Bosses of Mass Destruction 1.3.3 — exact artifact audit

Status: `EXACT PHYSICAL=PUBLISHER / PLAYER-ACTIVATION SURFACE CLOSED`

## Identity gate

Current physical sibling dossier:

- `BOMD-NeoForge-1.21-1.3.3.jar`;
- mod id `bosses_of_mass_destruction`;
- SHA-1 `446ff63afb858ad49149d24b72541739de83d38d`.

NON-MERGE PR #515 downloads CurseForge project/file `941573 / 8448640` and fails before semantic inspection unless publisher SHA-1 equals the physical fingerprint.

Audit evidence:

- HEAD: `f29e3dbadd76b729f9cba826f56516c644f1bfa2`;
- run: `36955037836` — SUCCESS;
- artifact: `11206056202`;
- digest: `sha256:3b756714d059e5459273a9840ae33ef9a0f2d3f432adb98f51e1719c0f48e2f1`;
- publisher SHA-1: `446ff63afb858ad49149d24b72541739de83d38d`;
- publisher SHA-256: `93da8753a00229e41c5ed399e6cf849737e7bd9b4109d5d8e4ad3a20136deb82`;
- bytes: `1,952,017`.

Result: exact publisher/physical equality is proven.

## Bounded archive inventory

- archive entries: **763**;
- classes: **287**;
- resources: **476**;
- provider data paths: **94**;
- top-level item classes selected by bounded audit: **13**;
- top-level block classes selected by bounded audit: **20**.

No third-party JAR bytes are committed to Black Arcana.

## Exhaustive direct player-activation index

Whole-artifact signature scanning finds direct item activation only on:

1. `BrimstoneNectarItem` — `use`;
2. `ChargedEnderPearlItem` — `use`;
3. `EarthdiveSpear` — `use`, `releaseUsing`, `onUseTick`;
4. `SoulStarItem` — `use`, `useOn`.

A fifth semantic root is provided by `ObsidilithSummonBlock` through the exact Ender Eye mixin path; it intercepts vanilla Eye of Ender `useOn` on the provider summon frame.

## Exact action/control findings

### Soul Star

`SoulStarItem.useOn` checks a provider Chiseled Stone Altar, consumes the Soul Star, marks altars lit and schedules Lich spawning once the required altar network is filled. The separate `use` branch launches a locator entity toward the Lich tower structure; that locator branch is excluded from semantic magic counting.

Exact `LichConfig$SummonMechanic` bytecode defaults `isEnabled = true` and `numEntitiesKilledToDropSoulStar = 50`. NeoForge death-event handling reads `summonMechanic.isEnabled` before granting Soul Star progress/drop behavior. Because the deployed effective config is unavailable, normal Soul Star production is fail-closed as conditional.

### Obsidilith

`ObsidilithSummonBlock` accepts an Eye of Ender on the provider `obsidilith_end_frame`, consumes the eye server-side, replaces the summon frame after a timed event and creates/adds the Obsidilith entity. Exact artifact data packages the Obsidilith arena worldgen/structure surface. No exact 1.3.3 binary config field was found that disables this summon action.

### Charged Ender Pearl

The exact item use launches `ChargedEnderPearlEntity`. On collision the provider teleports the owner to the impact point, resets fall distance, applies Resistance and Slow Falling, applies nearby knockback, synchronizes impact effects and discards the projectile.

Exact recipe: Void Thorn + Ender Pearl + Ancient Anima. Ancient Anima appears in exact Lich entity loot. Because the normal Lich path depends on the unresolved Soul Star summon config, this action is retained as `CONDITIONAL` for strict accounting.

### Earthdive Spear

Charged use/release delegates to provider `WallTeleport` and attempts short-range teleport through solid geometry. Exact localization independently identifies the behavior as short-range teleport through solid blocks.

Exact recipe: Obsidian Heart + Void Thorn + Stick. Exact provider data gives Obsidian Heart in the Obsidilith arena chest and Void Thorn in Void Blossom entity loot. Exact `VoidBlossomSummonBlockEntity` automatically spawns Void Blossom when a player approaches within its arena range; this automatic spawn is not itself a counted player action.

### Brimstone Nectar

Exact `use` resolves nearby eligible BOMD structures, schedules provider structure-repair operations, applies cooldown/effects, consumes one item outside creative mode and records item use.

Exact recipe is shapeless Netherite Scrap + Dragon's Breath + Ghast Tear, so normal catalog-level acquisition does not depend on another BOMD boss/config gate.

## Exact data reachability

Packaged exact data additionally closes:

- `charged_ender_pearl` recipe;
- `earthdive_spear` recipe;
- `brimstone_nectar` recipe;
- Obsidilith arena chest containing Obsidian Heart;
- Lich entity loot containing Ancient Anima;
- Void Blossom entity loot containing Void Thorn;
- Lich tower, Obsidilith arena and Void Blossom worldgen/structure resources.

## Semantic disposition

- Obsidilith Summoning — `COUNTED_EXACT`;
- Earthdive Wall Teleport — `COUNTED_EXACT`;
- Brimstone Structure Restoration — `COUNTED_EXACT`;
- Night Lich Summoning — `CONDITIONAL` on deployed Lich summon-mechanic state;
- Charged Ender Pearl Teleport — `CONDITIONAL` because normal owner acquisition inherits the Lich/Ancient Anima reachability gate.

Total supernatural roots: **5**.

Strict contribution: **+3**.

## Exclusions

Excluded from the semantic count:

- Soul Star locator launch;
- automatic Void Blossom proximity spawn;
- boss AI/projectiles;
- passive Levitation Block / Mob Ward / Monolith environmental behavior;
- structure blocks/runes/arena machinery;
- consumables/materials as objects;
- particles, sounds, scheduler phases and downstream hit/effect events.

## Clean-room boundary

The durable catalog retains identifiers, hashes, counts, bounded call-target/control-flow facts, recipe/loot reachability and semantic classification. It does not redistribute upstream JAR bytes, source implementation bodies, assets or localization beyond minimal identity labels.
