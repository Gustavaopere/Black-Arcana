# Deeper and Darker — 1.4.1

Status: `⚠️ PARTIAL / PUBLIC 1.4.1 BASELINE CLOSED / PHYSICAL JAR DIFFERS FROM ALL OFFICIAL PUBLISHERS / 3 SUPERNATURAL ACTION ROOTS IN PUBLIC BASELINE / +0 STRICT`

## Current physical identity

Current sibling physical authority records:

- row: **#215**;
- JAR: `deeperdarker-neoforge-1.21.1-1.4.1.jar`;
- mod id: `deeperdarker`;
- runtime: `1.4.1`;
- physical SHA-1: `83f7edd0a8516b2767c2cda7a3b2402f9e290d88`.

The mod is cross-domain: its sibling category is dimension/worldgen/mobs rather than `Magic`, but its player-facing surface includes supernatural portal, staff and Soul Elytra actions.

## Publisher mismatch — blocker

NON-MERGE PR **#517** tested every relevant official 1.4.1 distribution path:

- GitHub release `v1.4.1`;
- Modrinth version `TuD0Zvi3`;
- CurseForge File `8201775`.

All three official paths resolve to the same public artifact:

- SHA-1: `b6094adde68bd4b909bc75c64901e1f3fb99ad8f`;
- SHA-256: `eee3f51222b0bcc714def002ff089ac9e131d3cae4575b542fd0a7dd101fe0af`;
- bytes: `3,906,057`.

That artifact does **not** equal the physical pack fingerprint `83f7edd0...`. The pack JAR is therefore `OTHER_VERIFIED` relative to the official public release and cannot inherit the public semantic denominator as exact-current.

Publisher-baseline audit run **#4 / `36959073485`** completed successfully and produced evidence artifact `11206937200` with digest `sha256:b103afe2dd4b52780acf54682ddcca4b6df484df9ad9cf7accd218e443fb8b1f`.

See [`PUBLIC-1.4.1-BASELINE-AUDIT.md`](PUBLIC-1.4.1-BASELINE-AUDIT.md).

## Public 1.4.1 supernatural baseline

The public release closes three discrete player-owned supernatural actions:

1. **Otherside Portal Activation** — Heart of the Deep used on a valid reinforced-deepslate portal frame invokes provider portal creation;
2. **Sonorous Staff Sonic Boom** — deliberate charged staff release emits the provider sonic-boom damage/knockback action;
3. **Soul Elytra Boost** — dedicated client keybind sends `soul_elytra_boost` to the server; when eligible, the provider supplies a firework-style flight boost and applies its cooldown.

Detailed cards: [`actions/PUBLIC-BASELINE-ACTIONS.md`](actions/PUBLIC-BASELINE-ACTIONS.md).

## Exclusions from the semantic baseline

The exhaustive public-release activation audit also observes player interaction surfaces that do not create separate semantic magic identities:

- Ancient Compass — structure locator state;
- Sculk Transmitter / transmit keybind — remote container/block interaction utility;
- Soul Elytra item tick — presentation/cooldown state, separate from the active boost packet;
- Warden Armor — passive blindness/darkness suppression;
- boats and Lily Flower — ordinary placement;
- portal traversal after portal creation — consequence of the portal action, not a second spell;
- Sonorous Staff enchantments Volume/Reverberation — modifiers of the same staff action, not separate actions.

## Acquisition baseline

Public 1.4.1 provider data closes baseline acquisition:

- `deeperdarker:heart_of_the_deep` is added to the vanilla Warden loot table by a provider loot modifier;
- `deeperdarker:sonorous_staff` has a provider shaped recipe using Heart of the Deep, Soul Crystal and Sculk Bone;
- Soul Elytra is provider equipment; exact current-pack acquisition is not projected from the public release because the physical JAR differs.

## Strict accounting

Because the physical JAR is not byte-equivalent to any official public 1.4.1 artifact and is not attached for direct inspection:

- public baseline roots: **3**;
- exact-current physical roots: **UNKNOWN**;
- strict semantic contribution: **+0**;
- folder state: **⚠️ partial/conditioned**.

Even the public Soul Elytra Boost has an additional provider config gate: `soulElytraCooldown == -1` disables the boost. That config condition is subordinate to the larger physical-artifact blocker.

## Closure requirement

Promote this provider only after one of these evidence paths closes the installed bytes:

- direct access to the physical `deeperdarker-neoforge-1.21.1-1.4.1.jar`; or
- a publisher/repository artifact whose SHA-1 exactly equals `83f7edd0a8516b2767c2cda7a3b2402f9e290d88`.

Until then, do not add the three public-release actions to the strict global numerator and do not assume the physical JAR has exactly the same registrations/control flow.
