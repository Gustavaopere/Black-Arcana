# Physical Magic Reconciliation — 2026-09-27

Status: `84/84 CURRENT PHYSICAL MAGIC ROWS MAPPED / 70 ✅ + 14 ⚠️ / STRICT SEMANTIC MINIMUM UNCHANGED 1677`

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
| 479 | Reliquified L_Ender's Cataclysm | ⚠️ lower bound improved to 7 ability roots across 5 baseline relic owners; complete current 0.1.1 denominator open |
| 500 | ShadowsZ | ⚠️ new canonical mapping; 3 named Umbral spells are a lower bound, complete action inventory open |
| 501 | Simply Swords: Cataclysm | ⚠️ new canonical mapping; 4 documented current-release ability families, exact-current completeness open |
| 502 | Simply More | ⚠️ new canonical mapping; Alpha-5 unique/implicit ability inventory open |
| 503 | Simply Swords | ⚠️ new canonical mapping; Runic/Unique/implicit action inventory open |
| 564 | Waystones | ⚠️ new canonical mapping; semantic classification of provider teleport network remains open |

## Current physical-Magic status

After this reconciliation:

- physical `Magic` rows: **84**;
- mapped into Black Arcana: **84/84**;
- ✅ cataloged: **70**;
- ⚠️ partial / conditioned: **14**;
- ❌ unmapped/not cataloged: **0**;
- 🟡 active implementation: **0**;
- ⛔ blocked by total absence of evidence: **0**.

The fourteen ⚠️ rows in this physical-category subtotal are the previous eight category-Magic partials plus the six providers newly mapped above. Cross-domain partial providers such as Gaze and Traveloptics remain relevant to the global catalog even when they are outside this physical-category subtotal.

## Semantic effect

This reconciliation adds **no strict semantic objects**.

The eleven reclassified rows with existing provider catalogs were already represented in the semantic ledger, so their movement into the sibling `Magic` category cannot be counted again.

The six newly mapped providers are deliberately fail-closed:

- Reliquified L_Ender's Cataclysm: public 0.1 release-day source proves 5 baseline relic owners / 7 ability roots and the current-pack compatibility-transform log corroborates the same 5 loaded classes; complete 0.1.1 discrete-action cardinality is still not proven;
- ShadowsZ: at least three Umbral spells are named, but the complete current spell/action inventory is not closed;
- Simply Swords: Cataclysm: four current-release ability families are documented, but exact installed completeness is not yet proven;
- Simply More: item/Unique totals do not equal action totals, and the installed Alpha line explicitly contains rework/incomplete functionality;
- Simply Swords: weapon/item/Runic infrastructure does not itself prove the count of discrete supernatural player actions;
- Waystones: physical `Magic` classification does not by itself establish a countable spell/ritual/action identity.

Therefore the strict reconstructible minimum remains **1677**.

## Structural provider-tree effect

Six new top-level partial provider directories are added to the prior canonical 109-directory tree:

- prior: **109 = 99 ✅ + 10 ⚠️**;
- current: **115 = 99 ✅ + 16 ⚠️**.

This is a structural count, not a global semantic denominator.

## Next closure queue

The six new providers remain in the closure queue and should be closed in physical order unless stronger current evidence appears elsewhere:

1. Reliquified L_Ender's Cataclysm 0.1.1;
2. ShadowsZ 1.1.9;
3. Simply Swords: Cataclysm 1.0.2;
4. Simply More 1.3.0 Alpha 5;
5. Simply Swords 1.70.2;
6. Waystones 21.1.45.

Do not re-audit the eleven already-cataloged reclassified providers unless their physical/source line changes.
