# Ars Delight 2.2.2 — mixins, config, networking and optional compatibility

Status: `SOURCE SURFACE CLOSED / CURRENT-HOST CLASSLOADING+RUNTIME QA OPEN`

## Declared mixins — 3

`arsdelight.mixins.json` is required, Java 21, defaultRequire 1, and declares three common mixins:

1. `AddItemModifierAccessor`
   - targets Farmer's Delight `AddItemModifier`;
   - exposes its constructor through a Mixin invoker for provider global-loot generation/runtime serialization support.

2. `DrygmyTileMixin`
   - targets Ars Nouveau `DrygmyTile.generateItems`;
   - wraps `ANFakePlayer.getPlayer(ServerLevel)` to install a provider-selected adjacent pedestal tool;
   - tail injection removes the fake-player main-hand item.

3. `EffectInfuseMixin`
   - targets Ars Nouveau `EffectInfuse.getPotionData`;
   - can replace potion data from a provider Jelly context attachment.

These are implementation couplings, not Black Arcana integration APIs. The two Ars-targeting mixins require exact current-host validation against Ars 5.13.1.

## Drygmy tool contract

The provider scans the six adjacent directions around the Drygmy block position. On the first adjacent Ars `ArcanePedestalTile` holding a non-stackable item:

- either copies the exact stack or creates the item's plain default instance according to config;
- equips the Ars fake player main hand;
- optionally damages the original pedestal stack by configured cost;
- removes the fake-player item at method tail.

Server defaults:

- `drygmyFarmingToolPlainCopy = false`;
- `drygmyFarmingDamageTool = 2`.

Shared fake-player lifecycle, exceptional exits and compatibility with current Ars internals require runtime testing; they are not promoted to defects from source inspection alone.

## Config surface

### Client

The source Client config class is empty/plain.

### Common

- `enableThirstCompat = true`.

### Server

- `maxShieldingAbsorption = 8.0`, range 2..100;
- `wildenSpellDamageBonus = 0.2`, range 0..1;
- `wildenMaxManaBonus = 0.2`, range 0..1;
- `wildenManaRegenBonus = 0.2`, range 0..1;
- `drygmyFarmingToolPlainCopy = false`;
- `drygmyFarmingDamageTool = 2`, range 0..10000.

The exact installed generated config values/files have not been read in Phase 2Y.

## Provider-owned networking

`ArsDelight` constructs an L2 `PacketHandler` field with protocol/version `1`, but the exact 2.2.2 source tree contains no dedicated Ars Delight network package or provider packet/payload registration surface identified by this audit.

Therefore Phase 2Y does **not** claim a runtime payload count beyond “none identified in exact source”. JAR/runtime inspection remains the binary gate.

## Optional compatibility

### Ars Elemental — physically present

Source gates optional Jelly/content registration on `ModList.isLoaded(ArsElemental.MODID)`. It also registers `ElementalCompat` on the NeoForge event bus. Current physical version is 0.7.10.1.

Source behavior includes Flashpine content and a `SpellDamageEvent.Post` lightning-lure path. Runtime compatibility with the exact current Ars Elemental version remains pending.

### Archwood Good — not found top-level

Source gates its optional Jelly/content registration on `ModList.isLoaded(ArchwoodGood.MODID)`. No top-level Archwood Good JAR was found in the current physical modlist checkpoint. Absence must remain classloading-safe.

### Diet — not found top-level

Source has Diet tag-generation compatibility, but no top-level Diet JAR was found in the current physical checkpoint.

### Thirst — current provider differs from source build artifact

Source imports `dev.ghen.thirst.Thirst` and `RegisterThirstValueEvent`, gates registration on `Thirst.ID`, and enables the bridge by Common config. The source build references a historical Thirst Was Taken Curse artifact.

The physical pack currently contains Thirst Was Reclaimed 1.21.1-3.0.4 with mod id `thirst`. Mod-id continuity is insufficient evidence that the same Java packages/events remain binary-compatible. This integration is fail-closed for exact behavior until runtime/classpath validation.

### Cuisine Delight — physically present

`ADConfigGen` emits Cuisine Delight ingredient/transform config data using provider foods/effects. Current physical Cuisine Delight is 1.2.10. Source build referenced 1.2.1+1. Generated-data compatibility with 1.2.10 remains a runtime/datapack validation item.
