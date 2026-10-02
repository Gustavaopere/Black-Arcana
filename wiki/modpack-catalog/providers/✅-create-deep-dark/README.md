# Create: Deep Dark — 3.0.2

Status: `✅ CATALOGED / EXACT PHYSICAL=PUBLISHER ARTIFACT / ZERO_SEMANTIC_PASSIVE_ECHO_GEAR_PROCESSING / +0 STRICT / RUNTIME QA SEPARATE`

## Current physical identity

- sibling physical row: **#141**;
- JAR: `create_deep_dark-3.0.2-neoforge-1.21.1.jar`;
- mod id: `create_deep_dark`;
- runtime: `3.0.2`;
- physical SHA-1: `41a8c7f2f096555355214c55031ade1a84ef4058`.

Create: Deep Dark is cross-domain for the magic catalog because it adds supernatural-looking Echo gear/effects, but exact inspection is required before treating those effects as standalone magic actions.

## Exact publisher-artifact closure

NON-MERGE evidence PR **#532** audits CurseForge project/file `1020173 / 7624342` and hard-gates the publisher artifact against the physical fingerprint.

- audit HEAD: `cec3a766719667b7608ac6d05fc472a12f267867`;
- exact-artifact run: `37015531955` — **SUCCESS**;
- evidence artifact: `11230180765`;
- evidence digest: `sha256:de65ecba1b51068eb1c48e46594654e6bea468edd66c530ae0725f97632b3ebb`;
- publisher SHA-1: `41a8c7f2f096555355214c55031ade1a84ef4058`;
- publisher SHA-256: `7e1fe63771b9a586a6f5740cb4dbc653e0d7a44f17538db67ad6ce843362112b`;
- bytes: `254,417`.

The publisher SHA-1 exactly equals the physical pack SHA-1.

See [`EXACT-3.0.2-ARTIFACT-AUDIT.md`](EXACT-3.0.2-ARTIFACT-AUDIT.md).

## Exact semantic inventory

The exact artifact contains:

- **181** archive entries;
- **37** classes;
- **144** non-class resources;
- **35** `data/create_deep_dark/**` paths.

Archive keyword inventory closes zero provider surfaces named as spell/magic/ritual/ability/mana/arcane/glyph/teleport/summon/portal.

More importantly, exhaustive method-signature inspection across all 37 classes finds **zero** overrides in the player-action set `use`, `useOn`, `releaseUsing`, `onUseTick`, `finishUsingItem`, `interactLivingEntity`, `hurtEnemy`, `inventoryTick`, `onArmorTick`, or `onItemUseFirst`.

## Echo armor

`EchoArmorEffectProcedure` is an entity-tick subscriber. It checks the complete Echo armor set and refreshes Resistance/Strength server-side. The config can change effect strength.

This is equipment/passive state, not a discrete cast or ritual. The four armor pieces do not become four magic identities.

## Echo sword

`EchoSwordEffectProcedure` runs from `LivingIncomingDamageEvent`. When the attacker holds the Echo Sword, the victim receives Weakness and Darkness according to provider config.

This is an on-hit weapon proc attached to an ordinary melee attack. It is not counted as a separate spell/action root.

## Molten Echo

`MoltenEchoCollisionProcedure` applies Darkness and ignites a living entity colliding with the provider fluid. This is environmental/fluid behavior and does not create a player-owned magic identity.

## Warden, recipes and progression

The exact provider data closes Create processing, smithing, advancement and progression surfaces around Echo:

- Echo armor/sword smithing;
- Echo Cake and Molten Echo processing;
- Sculk Flour/XP processing;
- Echo Upgrade template progression;
- Warden-related progression/loot handling.

These are recipes, loot/economy and progression surfaces, not spells/glyphs/rituals.

Detailed classification: [`SEMANTIC-SURFACE-DISPOSITION.md`](SEMANTIC-SURFACE-DISPOSITION.md).

## Authority boundary

Create: Deep Dark remains authority for Echo materials, armor/sword effects, provider config, Warden additions, recipes, fluids, trades and progression. Create remains authority for its processing/heat systems; Minecraft remains authority for base Warden/Deep Dark mechanics.

Black Arcana records the semantic disposition only and must not reapply Echo buffs/debuffs, duplicate loot, or create a parallel superheat/processing path.

## Result

**✅ Cataloged — `ZERO_SEMANTIC_PASSIVE_ECHO_GEAR_PROCESSING`.**

Strict semantic delta: **+0**.
