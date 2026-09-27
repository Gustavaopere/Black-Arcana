# Mowzie's Cataclysm — 1.2.2

Status: `✅ CATALOGED / EXACT PHYSICAL=PUBLISHER ARTIFACT / ZERO_SEMANTIC_LOCATOR_BRIDGE / +0 STRICT / RUNTIME QA SEPARATE`

## Physical identity

- JAR: `mowzies_cataclysm-1.2.2.jar`;
- mod id: `mowzies_cataclysm`;
- runtime: `1.2.2`;
- Minecraft / loader: 1.21.1 / NeoForge;
- physical SHA-1: `0dff3e849155ca343d1a500f5b9ca2b54ffa692d`;
- CurseForge project/file: `1128348 / 8196282`.

Exact run `36291915300` hash-matched the publisher artifact to the physical pack JAR.

## Exact semantic boundary

The exact artifact contains four provider item classes:

- `FrostmawEyeItem`;
- `SunEyeItem`;
- `TongbiEyeItem`;
- `WroughtEyeItem`.

Its provider data namespace contains exactly four Eye recipes and four structure-location tags. English localization exposes **Eye of Frost**, **Eye of Sunbird**, **Eye of Sculptor** and **Eye of Wrought**.

The same artifact contains **0** spell/ritual/rite/ability-like paths and **0** such class names. The four Eyes are locator/exploration items bridging Cataclysm-style Eye navigation to Mowzie's Mobs structures; they are not independent player magic actions under the Black Arcana metric.

**Semantic contribution: +0 — `ZERO_SEMANTIC_LOCATOR_BRIDGE`.**

See [exact audit](EXACT-1.2.2-ZERO-SEMANTIC-AUDIT.md).

## Authority / runtime boundary

Mowzie's Mobs remains owner of its bosses/powers. This addon owns the locator items and their structure-tag routing. Integrated/worldgen changes can still affect whether those locators resolve correctly; that is runtime QA, not a new spell identity.

## Result

**✅ Cataloged.** Four exact locator Eyes, zero independent semantic magic actions.
