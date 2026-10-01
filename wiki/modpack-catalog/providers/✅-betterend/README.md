# BetterEnd: New Dawn — 21.0.34

Status: `✅ CATALOGED / EXACT PHYSICAL=PUBLISHER ARTIFACT / 48 INFUSION RITUAL IDENTITIES + 1 ETERNAL PORTAL RITUAL / 49 COUNTED_EXACT / RUNTIME QA SEPARATE`

## Current physical identity

Current sibling authority: `neoforge-rpg-skilltree@682a62c13c38215691be24361ffd303abb32dc01`.

Certified dossier:

`PROJECT-INSTRUCTIONS/modlist/Biomes + Cosmetic + Mobs + Structures + World Gen/✅-betterend-new-dawn v21.0.34.md`

- physical row: **#71**;
- JAR: `BetterEnd-21.0.34.jar`;
- mod id: `betterend`;
- runtime: `21.0.34`;
- Minecraft / loader: 1.21.1 / NeoForge;
- physical SHA-1: `149b73179ea63bf777315a7c850b2eba65c554bd`.

BetterEnd is cross-domain for the magic catalog: its sibling category is worldgen/biomes/structures rather than `Magic`, but the exact installed artifact owns a real ritual system.

## Exact publisher-artifact closure

NON-MERGE evidence PR **#497** audits the exact current publisher artifact and hard-gates it against the physical pack fingerprint.

- final ritual-seam audit HEAD: `f296d3fde0ebb01a85a4b6aa7e3f46a0c5dbaa92`;
- exact-artifact run: `36901757754` — **SUCCESS**;
- evidence artifact: `11182076262`;
- evidence digest: `sha256:9e7b92ddea636bb52349df6ab865a3efb7c12646ad1f4fa256ffb6561c4e1dce`;
- CurseForge project/file: `1422294 / 8610367`;
- publisher SHA-1: `149b73179ea63bf777315a7c850b2eba65c554bd`;
- publisher SHA-256: `45befc75466153f2f62d8c17a790b58ce794a4216ea152fc21190aa9dc40a440`;
- bytes: `97,673,585`.

The publisher SHA-1 exactly equals the current physical sibling SHA-1.

The exact artifact contains **10,430 archive entries / 682 classes / 9,748 non-class resources / 3,146 provider data paths**. The bounded audit found **48 unique `betterend:infusion` recipe IDs**, zero invalid recipe JSONs and exact Eternal Ritual control/reachability surfaces.

See [`EXACT-21.0.34-ARTIFACT-AUDIT.md`](EXACT-21.0.34-ARTIFACT-AUDIT.md).

## Semantic ritual inventory

BetterEnd 21.0.34 contributes **49 provider-owned ritual identities** under the Black Arcana semantic metric:

- **48 Infusion Ritual recipe identities** — exact packaged `betterend:infusion` recipes executed by the provider `InfusionRitual` lifecycle;
- **1 Eternal Portal Ritual** — the provider-owned pedestal/frame ritual that validates a complete structure and activates an Eternal Portal.

Detailed catalogs:

- [`rituals/INFUSION-RITUAL-CATALOG.md`](rituals/INFUSION-RITUAL-CATALOG.md)
- [`rituals/ETERNAL-PORTAL-RITUAL.md`](rituals/ETERNAL-PORTAL-RITUAL.md)

This follows the catalog precedent already used for recipe-defined provider rituals such as Hexalia Nature's Ritual and Celestial Infusion: each distinct ritual recipe ID is one semantic ritual identity when the provider ritual engine selects and settles that recipe. Ordinary crafting/process recipes remain excluded.

## Infusion Ritual — 48 exact identities

The exact JAR registers a dedicated `betterend:infusion` recipe type and the provider `InfusionRitual` resolves one active recipe from that type, tracks its infusion duration and settles its assembled result back to the Infusion Pedestal.

The packaged set is exactly **48 unique recipe IDs**:

- **39** enchanted-book infusion identities;
- **9** BetterEnd material/equipment transformations.

All 48 are explicitly materialized in the infusion catalog. Duplicate output item `minecraft:enchanted_book` does not collapse distinct ritual recipes because each recipe ID resolves a different enchantment identity.

## Eternal Portal Ritual — 1 exact identity

The exact artifact separately exposes `EternalRitual`, `EternalPedestal`, `EternalPedestalEntity` and `EndPortals`.

The exact control flow establishes one provider-owned ritual identity: accepted portal-key items activate the Eternal Pedestals; the linked ritual validates the frame/pedestal structure; matching active pedestals resolve a portal ID; then the server activates or generates the corresponding portal.

`config/betterend/portals.json` parameterizes portal destination, key item and color. It does **not** mint one semantic ritual per destination: all configured entries use the same Eternal Ritual causal action. The loader guarantees a non-empty portal mapping by regenerating its default when the file is absent, malformed at the top level or contains an empty portal array. The exact default maps `betterend:eternal_crystal` to the Overworld.

The exact JAR also packages the Eternal Portal structure/worldgen resources and `betterend:eternal_crystal` as one of the 48 Infusion Ritual recipes. Exact deployed portal-map contents remain runtime/config QA; they do not change the closed ritual denominator.

## Metric exclusions

BetterEnd contains a large amount of magical-looking content that is not a separate semantic action identity under this metric: ordinary crafting/process recipes, passive equipment/enchantment effects, worldgen/biome content, portal aftermath, particles, visual hints and synchronization.

Only the 48 ritual recipe identities and the one Eternal Portal activation identity are counted.

## Authority boundary

BetterEnd remains authority for Infusion Ritual matching/timing/consumption/output, pedestal state, Eternal Ritual structure validation/portal settlement and portal destination/key configuration. Black Arcana catalogs these identities but must not introduce a second BetterEnd ritual engine or double-settle the same provider ritual.

## Runtime QA remains separate

Catalog closure does not assert assembled-pack runtime PASS. Remaining QA includes exact deployed `betterend/portals.json`, complete-modpack pedestal interaction, multiplayer synchronization, portal/world lifecycle, protection/worldgen coexistence and provider dependencies BCLib/WorldWeaver/WunderLib.

## Result

**✅ Cataloged — `COUNTED_EXACT`.**

Current BetterEnd 21.0.34 semantic inventory: **49 exact-current ritual identities**.

Strict semantic delta: **+49**.
