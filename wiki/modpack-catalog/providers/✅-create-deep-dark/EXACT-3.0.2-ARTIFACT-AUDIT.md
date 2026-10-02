# Create: Deep Dark 3.0.2 — exact artifact audit

Status: `EXACT PHYSICAL=PUBLISHER / FULL CLASS-ACTION SURFACE CLOSED`

## Identity gate

- physical JAR: `create_deep_dark-3.0.2-neoforge-1.21.1.jar`;
- mod id: `create_deep_dark`;
- runtime: `3.0.2`;
- physical SHA-1: `41a8c7f2f096555355214c55031ade1a84ef4058`;
- CurseForge project/file: `1020173 / 7624342`.

NON-MERGE PR #532 run `37015531955` succeeded with exact physical/publisher equality.

- audit HEAD: `cec3a766719667b7608ac6d05fc472a12f267867`;
- evidence artifact: `11230180765`;
- artifact digest: `sha256:de65ecba1b51068eb1c48e46594654e6bea468edd66c530ae0725f97632b3ebb`;
- publisher SHA-256: `7e1fe63771b9a586a6f5740cb4dbc653e0d7a44f17538db67ad6ce843362112b`;
- bytes: `254,417`.

## Bounded archive inventory

- archive entries: **181**;
- classes: **37**;
- resources: **144**;
- provider data paths: **35**.

Keyword counts over archive paths:

`spell=0 · magic=0 · ritual=0 · ability=0 · mana=0 · arcane=0 · glyph=0 · teleport=0 · summon=0 · portal=0`

Positive semantic-adjacent path counts are Echo/Sculk/Warden/effect-related and were inspected directly rather than treated as magic by name.

## Exhaustive player-action signature scan

Every provider class was disassembled and every class signature was checked for:

`use · useOn · releaseUsing · onUseTick · finishUsingItem · interactLivingEntity · hurtEnemy · inventoryTick · onArmorTick · onItemUseFirst`

Result: **zero matching provider class overrides**.

This is the strongest denominator fact for this provider: its supernatural-looking effects are not exposed through a dedicated player activation surface.

## Exact effect seams

### Echo armor

`EchoArmorEffectProcedure` is wired to `EntityTickEvent.Pre`. It verifies all four provider Echo armor pieces, reads provider config and refreshes vanilla Resistance/Strength effects on the wearer server-side.

Disposition: passive equipment state.

### Echo sword

`EchoSwordEffectProcedure` is wired to `LivingIncomingDamageEvent`. It checks the attack source entity's main-hand item for the Echo Sword and applies Weakness/Darkness to the victim, with provider config controlling amplifier strength.

Disposition: reactive/on-hit weapon proc.

### Molten Echo

`MoltenEchoCollisionProcedure` applies Darkness and ignition on fluid collision.

Disposition: environmental hazard/fluid effect.

### Warden/progression

The provider contains Warden death/progression handling plus exact recipes/advancements for Echo materials and equipment. These are progression/economy surfaces rather than player magic actions.

## Exact data disposition

The bounded data scan includes 24 semantic-adjacent JSON documents, consisting of advancement, loot, Create processing, smithing and Echo-related recipe/tag surfaces. No provider spell/ritual/action registry is present.

## Semantic result

- standalone spell/glyph/ritual/ability roots: **0**;
- player-invoked supernatural action roots: **0**;
- passive full-set armor effect family: **EXCLUDED**;
- Echo Sword on-hit debuff family: **EXCLUDED**;
- Molten Echo collision effect: **EXCLUDED**;
- Warden/recipe/trade/progression surfaces: **EXCLUDED**.

Disposition: **`ZERO_SEMANTIC_PASSIVE_ECHO_GEAR_PROCESSING`**.

## Clean-room boundary

The durable catalog retains only identifiers, hashes, counts and behavior-level classifications required for semantic cataloging. It does not redistribute the JAR, source bodies, assets or localization prose.
