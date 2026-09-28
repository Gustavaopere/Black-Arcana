# Physical Magic Reconciliation — 2026-09-27

Status: `84/84 CURRENT PHYSICAL MAGIC ROWS MAPPED / 71 ✅ + 13 ⚠️ / STRICT SEMANTIC MINIMUM 1684`

## Authority

- Black Arcana base before this closure: `main@49873930b2948b7d5ddf8f0417138dcebffec6ca`
- sibling physical/modlist authority: `neoforge-rpg-skilltree@7028524829b5589ee377cd980aa8298cf95cf5c7`
- source table: `PROJECT-INSTRUCTIONS/modlist/modlist.md`
- category rule: a row belongs to this subtotal only when the **category field** contains the exact category `Magic`; the word "Magic" in a display name is not sufficient.

The prior Black Arcana snapshot had 67 physical `Magic` rows. The current sibling category table has **84**, a delta of **+17** reclassified/current rows.

## Delta reconciliation

| Physical row | Provider | Black Arcana disposition |
|---:|---|---|
| 214 | Deeper and Darker: Spellbooks | ✅ existing canonical provider |
| 220 | Discerning The Eldritch | ✅ existing canonical provider |
| 221 | Dis-Enchanting Table | ✅ existing canonical provider; zero semantic action ownership already closed |
| 225 | Dreamless Spells and Spellbooks | ✅ existing canonical provider |
| 232 | Dynamic RPG Resource Bars | ✅ existing canonical provider; presentation/zero-semantic closure already present |
| 324 | Ignis Soulfires: Spellbooks | ✅ existing canonical provider; zero bridge/gear semantic closure already present |
| 329 | Immersive Portal - Iron's Spells addon | ✅ existing canonical provider; +0 independent semantic identities |
| 472 | Iron's Spells Recolor | ✅ existing canonical provider; +0 independent semantic identities |
| 476 | Reliquified Ars Nouveau | ✅ existing canonical provider; +19 strict already owned in ledger |
| 477 | Reliquified Artifacts | ✅ existing canonical provider; +52 strict already owned in ledger |
| 478 | Reliquified Iron's Spells 'n Spellbooks | ✅ existing canonical provider; +25 strict already owned in ledger |
| 479 | Reliquified L_Ender's Cataclysm | ✅ exact publisher/physical SHA-1 equality plus bounded exact-artifact audit close 5 registered relic owners / 7 owner-scoped ability roots and exact-current loot routes for all five owners; `COUNTED_EXACT +7` |
| 500 | ShadowsZ | ⚠️ exact physical/publisher SHA-1 equality + exact-artifact audit close **10 semantic identities**; all player powers remain attunement-gated by effective `shadowszRestrictPowers`, and Fusion additionally depends on deployed `fusionEnabled`; +0 strict until those values are captured |
| 501 | Simply Swords: Cataclysm | ⚠️ exact-version source inventory closed at 4 abilities; deployed STARTUP config decides current active subset |
| 502 | Simply More | ⚠️ Alpha-5 semantic lower bound 9 player-invoked active roots; passive/proc surfaces and implicits excluded; legacy active inventory open |
| 503 | Simply Swords | ⚠️ release-correlated source lower bound 66: 62 ACTIVE Unique roots + 4 player-use Runic actions; passive/proc/implicit surfaces excluded; legacy/reachability open |
| 564 | Waystones | ⚠️ exact-version source lower bound 3: one deduplicated Warp/Teleport root + Warp Portal Conjuration + Twinbound Link; setup-action classification remains open |

## Current physical-Magic status

After this reconciliation:

- physical `Magic` rows: **84**;
- mapped into Black Arcana: **84/84**;
- ✅ cataloged: **71**;
- ⚠️ partial / conditioned: **13**;
- ❌ unmapped/not cataloged: **0**;
- 🟡 active implementation: **0**;
- ⛔ blocked by total absence of evidence: **0**.

The thirteen ⚠️ rows in this physical-category subtotal are the previous eight category-Magic partials plus the five still-partial providers newly mapped above. Reliquified L_Ender's Cataclysm #479 is now ✅ exact-cataloged. Cross-domain partial providers such as Gaze and Traveloptics remain relevant to the global catalog even when they are outside this physical-category subtotal.

## Semantic effect

This reconciliation now adds **+7 strict semantic objects** from the exact-current Reliquified L_Ender's Cataclysm 0.1.1 closure.

The eleven reclassified rows with existing provider catalogs were already represented in the semantic ledger, so their movement into the sibling `Magic` category cannot be counted again.

Reliquified L_Ender's Cataclysm is no longer fail-closed at the catalog denominator: exact publisher bytes match the physical SHA-1, and bounded audit run `36416011761` closes exactly five registered relic owners and seven owner-scoped `AbilityData.builder(...)` roots. It contributes **+7 `COUNTED_EXACT`**.

The remaining five newly mapped providers stay fail-closed:

- ShadowsZ: exact hash-matched 1.1.9 artifact evidence closes the complete semantic inventory at 10 identities; strict remains +0 because all powers are attunement-gated by the effective `shadowszRestrictPowers` world rule and Fusion additionally depends on deployed `fusionEnabled`;
- Simply Swords: Cataclysm: exact-version release-correlated source closes four semantic abilities, but deployed STARTUP config can suppress their active surface and remains uncaptured;
- Simply More: release-correlated Alpha-5 source establishes a 9-action semantic lower bound from player-invoked active roots; passive/proc surfaces and implicits are excluded while legacy/rework/no-function active uniques and Mimicry remain unclassified;
- Simply Swords: release-correlated source establishes a 66-action semantic lower bound from 62 registered ACTIVE Unique roots plus 4 player-use Runic action families; passive definitions, 17 implicits and trigger-only Gem Powers are excluded while legacy/non-opted active paths and deployed reachability remain open;
- Waystones: exact 21.1.45 source establishes a 3-action lower bound from one provider-native Warp/Teleport root, Warp Portal Conjuration and Twinbound Link; activation, Blank Scroll binding and Warp Plate shard attunement remain classification-open, while passive/downstream/bridge infrastructure is excluded;

Therefore the strict reconstructible minimum is now **1684**.

## Structural provider-tree effect

Six new top-level partial provider directories are added to the prior canonical 109-directory tree:

- prior: **109 = 99 ✅ + 10 ⚠️**;
- current: **115 = 100 ✅ + 15 ⚠️**.

This is a structural count, not a global semantic denominator.

## Next closure queue

The five still-partial new providers remain in the closure queue and should be closed in physical order unless stronger current evidence appears elsewhere:

1. ShadowsZ 1.1.9 — capture effective `shadowszRestrictPowers` and deployed `fusionEnabled`; exact 10-root inventory is already closed;
2. Simply Swords: Cataclysm 1.0.2 deployed config;
3. Simply More 1.3.0 Alpha 5;
4. Simply Swords 1.70.2;
5. Waystones 21.1.45.

Do not re-audit the eleven already-cataloged reclassified providers unless their physical/source line changes.