# Protection Pixel — 2.2.1

Status: `✅ CATALOGED / EXACT PHYSICAL=PUBLISHER ARTIFACT / ZERO_SEMANTIC_TECH_GEAR / +0 STRICT / RUNTIME QA SEPARATE`

## Current physical identity

Current sibling authority:

- physical row: **#460**;
- JAR: `protection_pixel-2.2.1-neoforge-1.21.1.jar`;
- mod id: `protection_pixel`;
- runtime: `2.2.1`;
- Minecraft / loader: 1.21.1 / NeoForge;
- physical SHA-1: `c35da610425f735eea4d027ad159c88de6ec6e3f`.

Protection Pixel is cross-domain only because it exposes player-facing equipment abilities. The exact installed artifact is a Create-steampunk equipment/device addon, not a spell/ritual provider.

## Exact publisher-artifact closure

NON-MERGE evidence PR **#520** audits CurseForge project/file `1023409 / 7549821` and hard-gates publisher bytes against the physical pack fingerprint.

- audit HEAD: `4c3168f33c2d702e19f97534436e26bb93faa10c`;
- exact-artifact run: `36962672381` — **SUCCESS**;
- evidence artifact: `11208357031`;
- evidence digest: `sha256:0005d0954a20bf8b2aa8f06192c8f0ab8df12da8dbdfc435e173a1b673f8cc62`;
- publisher SHA-1: `c35da610425f735eea4d027ad159c88de6ec6e3f`;
- publisher SHA-256: `a496e6263a0c2cd4341f05a1a71085e467cfe85b453a6aef1c38f614b61129f4`;
- bytes: `2,608,196`.

The publisher SHA-1 exactly equals the current physical sibling SHA-1.

See [`EXACT-2.2.1-ARTIFACT-AUDIT.md`](EXACT-2.2.1-ARTIFACT-AUDIT.md).

## Exact provider surface

The exact JAR contains:

- **1,292** archive entries;
- **659** classes, all under the Protection Pixel provider package;
- **222** procedure classes;
- **104** item classes;
- **13** input/network classes;
- **111** `data/protection_pixel/**` paths;
- three explicit key mappings: Armor Table Trigger, Wing Fly and Fly Forward;
- Create-integrated crafting/processing and equipment/device acquisition routes.

The provider has active gadgets such as Cannon Arm, Hook Cannon, Heat Pulse Thruster, Maneuvering/Evasion Wing, Blood Dialysis Device and many armor-piece effects. These are documented in [`TECH-ACTION-SURFACE.md`](TECH-ACTION-SURFACE.md).

## Semantic-magic disposition

Exact archive/resource inspection finds **no provider-owned spell, ritual, rite, glyph, mana, arcane, wizard/sorcery or magic-action registry/resource surface**.

The only superficially related archive hit is vanilla-style enchantability support (`data/minecraft/tags/item/enchantable/**`) plus ordinary item names such as Netherite sheets. That does not create provider magic identities.

Protection Pixel abilities are explicitly technological/equipment-mediated:

- artillery shells and hook launchers;
- steam/heat propulsion and jet/wing movement;
- drones and magnetic equipment effects;
- force-field-style shielding;
- armor sensors, debuffs, stat modifiers and proc effects;
- blood-dialysis/medical equipment behavior;
- reactor, water, flare-rod and armor-platform support infrastructure.

Under the Black Arcana semantic metric, these are equipment/gadget actions, passives/procs, locomotion or technological weapon operations. They are not standalone spells/glyphs/rituals or equivalent supernatural player-action identities.

## Result

**✅ Cataloged — `ZERO_SEMANTIC_TECH_GEAR`.**

- provider-owned semantic magic identities: **0**;
- strict semantic delta: **+0**;
- provider directory is complete at catalog level;
- runtime/equipment QA remains separate.

## Authority boundary

Protection Pixel remains authority for equipment state, reactor/fuel/water support, device inputs, cooldowns, projectiles, drones, armor modifiers, armor plates and Create integration. Black Arcana does not reinterpret these technological mechanics as magic and must not replay their costs/effects.
