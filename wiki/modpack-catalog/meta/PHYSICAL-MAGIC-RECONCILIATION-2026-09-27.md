# Physical Magic Reconciliation — 2026-09-27

Status: `84/84 CURRENT PHYSICAL MAGIC ROWS MAPPED / 71 ✅ + 13 ⚠️ / STRICT SEMANTIC MINIMUM 1684`

## Authority

- Black Arcana base: `main@99e56bfa174969d538331f2fc40b2211b5b79b2a`
- sibling physical/modlist authority: `neoforge-rpg-skilltree@ac23fc1c67937deeffe982ae971c21d4f3561bc5`
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
| 479 | Reliquified L_Ender's Cataclysm | ✅ `COUNTED_RELEASE_BOUNDED`; 5 relic owners / 7 ability roots / +7 strict |
| 500 | ShadowsZ | ⚠️ new canonical mapping; 3 named Umbral spells are a lower bound, complete action inventory open |
| 501 | Simply Swords: Cataclysm | ⚠️ new canonical mapping; 4 documented current-release ability families, exact-current completeness open |
| 502 | Simply More | ⚠️ new canonical mapping; Alpha-5 unique/implicit ability inventory open |
| 503 | Simply Swords | ⚠️ new canonical mapping; Runic/Unique/implicit action inventory open |
| 564 | Waystones | ⚠️ new canonical mapping; semantic classification of provider teleport network remains open |

## Current physical-Magic status

After this reconciliation:

- physical `Magic` rows: **84**;
- mapped into Black Arcana: **84/84**;
- ✅ cataloged: **71**;
- ⚠️ partial / conditioned: **13**;
- ❌ unmapped/not cataloged: **0**;
- 🟡 active implementation: **0**;
- ⛔ blocked by total absence of evidence: **0**.

The thirteen ⚠️ rows in this physical-category subtotal are the previous eight category-Magic partials plus five of the six providers newly mapped above. Reliquified L_Ender's Cataclysm has since been promoted to ✅. Cross-domain partial providers such as Gaze and Traveloptics remain relevant to the global catalog even when they are outside this physical-category subtotal.

## Semantic effect

The category reclassification itself adds **no strict semantic objects**. The eleven reclassified rows with existing provider catalogs were already represented in the semantic ledger, so their movement into the sibling `Magic` category cannot be counted again.

A subsequent release-bounded closure promotes Reliquified L_Ender's Cataclysm 0.1.1 by **+7 strict**. Public initial-release source closes five relic owners and seven ability roots; the publisher 0.1.1 delta is compatibility-only for OctoLib 0.6, and later 0.2/WIP branch relics are excluded.

The remaining five newly mapped providers stay fail-closed:

- ShadowsZ: at least three Umbral spells are named, but the complete current spell/action inventory is not closed;
- Simply Swords: Cataclysm: four current-release ability families are documented, but exact installed completeness is not yet proven;
- Simply More: item/Unique totals do not equal action totals, and the installed Alpha line explicitly contains rework/incomplete functionality;
- Simply Swords: weapon/item/Runic infrastructure does not itself prove the count of discrete supernatural player actions;
- Waystones: physical `Magic` classification does not by itself establish a countable spell/ritual/action identity.

Therefore the strict reconstructible minimum is now **1684**.

## Structural provider-tree effect

Six new top-level partial provider directories are added to the prior canonical 109-directory tree:

- prior: **109 = 99 ✅ + 10 ⚠️**;
- current: **115 = 100 ✅ + 15 ⚠️**.

This is a structural count, not a global semantic denominator.

## Next closure queue

The six new providers should be closed in physical order unless stronger current evidence appears elsewhere:

1. ShadowsZ 1.1.9;
2. Simply Swords: Cataclysm 1.0.2;
3. Simply More 1.3.0 Alpha 5;
4. Simply Swords 1.70.2;
5. Waystones 21.1.45.

Do not re-audit the eleven already-cataloged reclassified providers unless their physical/source line changes.
