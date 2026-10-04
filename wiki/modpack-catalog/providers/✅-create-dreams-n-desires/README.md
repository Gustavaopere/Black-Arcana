# Create: Dreams n' Desires — 2.3a-BETA

Status: `✅ CATALOGED / EXACT PHYSICAL=PUBLISHER ARTIFACT / ZERO_SEMANTIC_CREATE_AUTOMATION_TOOLS_CONTENT / +0 STRICT / RUNTIME QA SEPARATE`

## Current physical identity

- sibling physical row: **#223**;
- JAR: `DnDesires-1.21.1-2.3a-BETA.jar`;
- mod id: `dndesires`;
- runtime: `2.3a-BETA`;
- Minecraft / loader: 1.21.1 / NeoForge;
- physical SHA-1: `72635119b4bcc49b050c50d6cbb1abb02bb3982a`.

Create: Dreams n' Desires is a broad Create addon for machines, logistics, kinetic equipment, tools, food and related content. Exact-current inspection does not expose a provider-owned spell, ritual, glyph, mana, arcane, teleport or portal action roster.

## Exact publisher-artifact closure

NON-MERGE evidence PR **#560** audits Modrinth project/version `JmybsfWs / bqMxf6Ua` (same 2.3a-BETA release line as CurseForge project/file `864781 / 8037481`) and hard-gates the downloaded artifact against the physical pack fingerprint.

- audit HEAD: `0eb6d0c454305c69fecf3ffb099dad094425e2c8`;
- exact-artifact run: `37168676372` — **SUCCESS**;
- evidence artifact: `11290453324`;
- evidence digest: `sha256:5be20be6f160b129ba71df82959761592d6f787f3c67680eb635ca81211f76a3`;
- publisher SHA-1: `72635119b4bcc49b050c50d6cbb1abb02bb3982a`;
- publisher SHA-256: `d3f7f2384e8327c81671f2d48df15a0bba98ef04b727a430079cfc9145a7a379`;
- bytes: `1,249,099`.

The publisher SHA-1 exactly equals the current physical pack SHA-1.

See [`EXACT-2.3a-BETA-ARTIFACT-AUDIT.md`](EXACT-2.3a-BETA-ARTIFACT-AUDIT.md).

## Exact semantic inventory

The exact artifact contains:

- **1,363** archive entries;
- **227** classes;
- **1,136** non-class resources;
- **457** `data/dndesires/**` paths;
- **233** provider recipes;
- **82** provider loot-table paths;
- **114** provider advancement paths;
- **27** provider tag paths.

Bounded semantic-name inventory is zero for spell, magic, ritual, mana, arcane, glyph, summon, soul, teleport and portal.

The audit reports `ability=1` only because `durability` contains the substring `ability`; the exact hit is `data/minecraft/tags/item/enchantable/durability.json`. The four `enchant` hits are the vanilla `data/minecraft/tags/item/enchantable/**` tags used by tools, not provider-owned enchantment definitions.

## Complete player-interaction surface

Exhaustive signature indexing finds exactly eight classes with the bounded player-interaction methods used by this audit:

1. `SpudSentryBlock` — owner/ammo/config interaction for a kinetic automated potato sentry;
2. `StirlingEngineBlock` — opens/forwards the attached furnace container;
3. `SmartHopperBlock` — inventory/logistics configuration;
4. `MilkshakeItem` — ordinary drink completion/container return;
5. `GatlingBreakerItem` — powered ranged block-breaking tool using Create zapper-beam presentation;
6. `HandheldSawItem` — axe/tree-cutting tool interaction;
7. `BurstPackageItem` — Create package/logistics behavior; contained spawn eggs can settle through vanilla SpawnEgg semantics when the package opens;
8. `DispenserBlockMixin` — wrench/placement interaction compatibility.

The provider also owns Handheld Drill excavation/vein-mining behavior, but that is block-break/tool lifecycle rather than a cast/use root.

Spud Sentry firing is automated kinetic equipment behavior using Create potato-projectile infrastructure. It is not a player-selected summon or spell.

## Semantic disposition

**`ZERO_SEMANTIC_CREATE_AUTOMATION_TOOLS_CONTENT` / +0 strict.**

Detailed disposition: [`SEMANTIC-SURFACE-DISPOSITION.md`](SEMANTIC-SURFACE-DISPOSITION.md).

Milkshake potion effects, tool enchantability, kinetic machines, package contents, sentry projectiles and automation state remain food/tool/equipment/logistics/processing mechanics. They do not mint independent Black Arcana magic identities.

## Authority boundary

Create remains authority for base kinetics, contraption, package and potato-cannon infrastructure. D&D owns its machines, items, food, processing, sentry behavior and adapters. Black Arcana catalogs this surface but must not reinterpret technological/tool interactions as spells.

## Runtime QA remains separate

Catalog closure does not assert assembled-pack runtime PASS. Smart Hopper concurrency, fluids, Golden Mixer, Spud Sentry targeting, tools, Sable/contraption state, packets and Create version compatibility remain runtime/integration QA.

## Result

**✅ Cataloged — zero provider-owned semantic magic objects.**

Strict semantic delta: **+0**.
