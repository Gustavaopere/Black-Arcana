# Create: Cold Sweat — 1.1.2

Status: `✅ CATALOGED / EXACT PHYSICAL=PUBLISHER ARTIFACT / ZERO_SEMANTIC_CREATE_THERMAL_BRIDGE / +0 STRICT / RUNTIME QA SEPARATE`

## Current physical identity

Current sibling physical authority:

- physical row: **#136**;
- JAR: `create_cold_sweat-1.1.2.jar`;
- mod id: `create_cold_sweat`;
- runtime: `1.1.2`;
- Minecraft / loader: 1.21.1 / NeoForge;
- physical SHA-1: `58326378dac966d664ae827dcc76e4b3a284d747`.

Create: Cold Sweat is a bridge between Create and Cold Sweat. It translates Create blocks/fluids/kinetics into Cold Sweat temperature inputs; it is not a second body-temperature system and does not expose a standalone spell/ritual/action roster.

## Exact publisher-artifact closure

NON-MERGE evidence PR **#566** audits CurseForge project/file `1184450 / 7214552` and hard-gates publisher bytes against the physical fingerprint.

- audit HEAD: `6095f4ac2be04a369227461d2aac5c1fac7bb547`;
- exact-artifact run: `37172185334` — **SUCCESS**;
- evidence artifact: `11291667207`;
- evidence digest: `sha256:c4a0294e4f54ef3c7944ff3429947c0458055cb506a137561b0e82c6407299b5`;
- publisher SHA-1: `58326378dac966d664ae827dcc76e4b3a284d747`;
- publisher SHA-256: `7b9260cef82a343e68c7fdbbfd8a955c1cf3bdf1f52b09989ca7971e3cce1224`;
- bytes: `214,958`.

The publisher SHA-1 exactly equals the installed physical SHA-1.

See [`EXACT-1.1.2-ARTIFACT-AUDIT.md`](EXACT-1.1.2-ARTIFACT-AUDIT.md).

## Exact provider surface

The exact artifact contains:

- **51** archive entries;
- **19** classes;
- **32** resources;
- **19** `data/create_cold_sweat/**` paths;
- **0** archive paths matching the audit's spell/magic/ritual/rite/ability/mana/arcane/glyph/summon/teleport/portal/soul/curse semantic token set;
- **44** temperature/Create bridge paths;
- **13** provider JSON resources.

The complete class set consists of block-temperature registration/configuration, thermal block effects for Blaze Burners, Boilers, Encased Fans, fluid containers, pipes/pumps and Steam Engines, plus datagen and helper utilities.

## Semantic-magic disposition

The exact JAR exposes no provider-owned item/cast/keybind/network action surface. Its runtime hook is Cold Sweat's `BlockTempRegisterEvent` and related block-temperature APIs.

Provider data contains fluid-temperature definitions and tags for Create thermal blocks. Exact bytecode resolves the active behavior to:

- registering Create blocks as Cold Sweat `BlockTemp` sources;
- configurable Blaze Burner temperatures;
- Boiler heat calculation;
- Encased Fan cooling/temperature propagation;
- fluid/container temperatures;
- pipe/pump thermal behavior;
- Steam Engine effects;
- config/datagen support.

These are environmental/thermal bridge mechanics. They are not spells, glyphs, rituals, rites or equivalent discrete supernatural player actions.

## Result

**✅ Cataloged — `ZERO_SEMANTIC_CREATE_THERMAL_BRIDGE`.**

- provider-owned semantic magic identities: **0**;
- strict semantic delta: **+0**;
- provider catalog denominator: closed;
- assembled-pack Create/Cold Sweat runtime QA: separate.

## Authority boundary

Cold Sweat remains authority for body/environment temperature settlement; Create remains authority for Create machines/fluids/kinetics. Create: Cold Sweat translates those surfaces. Black Arcana must not create a second thermal ledger or reinterpret bridge temperature effects as magic actions.
