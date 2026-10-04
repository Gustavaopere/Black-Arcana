# Create: Dreams n' Desires 2.3a-BETA — exact artifact audit

Status: `EXACT PHYSICAL=PUBLISHER / ZERO PROVIDER-OWNED MAGIC-ACTION ROSTER`

## Identity gate

- physical JAR: `DnDesires-1.21.1-2.3a-BETA.jar`;
- mod id: `dndesires`;
- runtime: `2.3a-BETA`;
- physical SHA-1: `72635119b4bcc49b050c50d6cbb1abb02bb3982a`.

NON-MERGE PR #560 downloads Modrinth `JmybsfWs / bqMxf6Ua` and fails unless its SHA-1 equals the physical fingerprint. The release corresponds to CurseForge `864781 / 8037481`.

- audit HEAD: `0eb6d0c454305c69fecf3ffb099dad094425e2c8`;
- run: `37168676372` — SUCCESS;
- artifact: `11290453324`;
- digest: `sha256:5be20be6f160b129ba71df82959761592d6f787f3c67680eb635ca81211f76a3`;
- publisher SHA-1: `72635119b4bcc49b050c50d6cbb1abb02bb3982a`;
- publisher SHA-256: `d3f7f2384e8327c81671f2d48df15a0bba98ef04b727a430079cfc9145a7a379`;
- bytes: `1,249,099`.

Result: exact publisher/physical equality is proven.

## Archive inventory

- entries: **1,363**;
- classes: **227**;
- resources: **1,136**;
- provider-data paths: **457**;
- recipes: **233**;
- loot-table paths: **82**;
- advancement paths: **114**;
- tag paths: **27**.

Semantic-name path counts:

- spell 0;
- magic 0;
- ritual 0;
- ability 1 — false positive from `durability` substring;
- mana 0;
- arcane 0;
- glyph 0;
- summon 0;
- soul 0;
- teleport 0;
- portal 0;
- enchant 4 — vanilla `enchantable` tag paths;
- charm 0;
- sentry 23;
- effect 0.

Exact `ability`/`enchant` path inspection resolves only:

- `data/minecraft/tags/item/enchantable/durability.json`;
- `data/minecraft/tags/item/enchantable/mining.json`;
- `data/minecraft/tags/item/enchantable/mining_loot.json`;
- the parent `enchantable/` directory.

No provider enchantment definition or provider magic-action registry follows from these paths.

## Exhaustive bounded activation index

The audit scans every class signature and finds eight classes on the bounded interaction method set:

- `SpudSentryBlock` — `useWithoutItem`;
- `StirlingEngineBlock` — `useWithoutItem`;
- `SmartHopperBlock` — `useWithoutItem`;
- `MilkshakeItem` — `finishUsingItem`;
- `GatlingBreakerItem` — `use`, `releaseUsing`, `onUseTick`, `inventoryTick`;
- `HandheldSawItem` — `useOn`;
- `BurstPackageItem` — `use`, `useOn`, `releaseUsing`, `inventoryTick`;
- `DispenserBlockMixin` — `useWithoutItem`.

Bytecode disposition:

- Spud Sentry interaction establishes owner/ammo/config state; autonomous firing creates Create potato projectiles from inserted ammo;
- Stirling Engine interaction opens the attached furnace container;
- Smart Hopper is inventory/logistics behavior;
- Milkshake consumption delegates normal food/drink settlement and returns a glass bottle;
- Gatling Breaker raycasts and destroys blocks as a powered tool;
- Handheld Saw delegates axe/tool/tree-cutting behavior;
- Burst Package inherits Create package logistics; its special spawn-egg handling delegates entity creation from contained vanilla SpawnEgg items rather than defining a provider summon identity;
- Dispenser mixin only adjusts wrench/placement interaction.

Handheld Drill is separately visible in provider content and acquisition data; its excavation/vein-mining behavior is tool/block-break lifecycle and therefore outside the magic-action metric.

## Data/acquisition surface

The exact provider data closes crafting/processing progression for Handheld Drill, Handheld Saw, Spud Sentry, Gatling Breaker and the broader automation catalog. Acquisition evidence does not convert these technological/tool surfaces into supernatural identities.

## Semantic disposition

`ZERO_SEMANTIC_CREATE_AUTOMATION_TOOLS_CONTENT / +0 strict`.

Food/status effects, existing enchantment tags, projectile settlement, package contents and kinetic machinery are not independent spells/rituals/glyphs/abilities under the catalog metric.

## Clean-room boundary

The durable catalog retains hashes, counts, IDs, method categories and behavior-level classifications required for denominator work. It does not redistribute JAR bytes, implementation bodies or assets.
