# Capability Matrix Delta — Goety base provider

Status: `AUTHORITATIVE GOETY OVERLAY / EXACT 3.1.4 MECHANICS FAIL-CLOSED`

## Scope and precedence

Until `wiki/modpack-catalog/CAPABILITY-MATRIX.md` is regenerated integrally, this file supersedes **only the Goety-specific evidence clauses** in that matrix. It does not change any other provider row, Black Arcana Phase 3 decision, or provider authority boundary.

The purpose of this overlay is to prevent the historical 110-name Wiki list from being read as Goety's complete current registry while preserving the valid player-facing behavior evidence already documented there.

## Evidence anchor

Installed authority:

- mod id: `goety`;
- physical JAR: `goety-3.1.4.jar`;
- runtime version: `3.1.4`;
- physical SHA-1: `a0770e180e4e8b1b87d8fa9c8356e9dbf34d82a7`;
- Minecraft 1.21.1 / NeoForge `21.1.248`.

Public current-line source evidence:

- `Vivideru/Goety-3@4230e3bce2842779a6667ae6e5bfef8f53a27541` — Goety `3.1.0`;
- `Vivideru/Goety-3@6c41a04f2d712097c4461f969a6bb8ee277149ef` — Goety `3.1.1`;
- audited file: `src/main/java/com/Polarice3/Goety/common/items/ModItems.java`;
- stable blob at both checkpoints: `db3c63b366803e2d46aa4a996b5bb0f358437a7f`;
- **123 active Focus item registrations** across the audited public interval.

Category counts in that registry are Magic 26, Necromancy 11, Geomancy 11, Frost 9, Wild 12, Wind 9, Storm 11, Abyss 9, Nether 11 and Void 14.

The legacy official Wiki remains a **110-name documentary subset**. The source-only identities omitted from that list are `illuminate_focus`, `earth_punch_focus`, `smack_stone_focus`, `ministrous_focus`, `carrion_focus`, `razor_wind_focus`, `surging_focus`, `sprightly_focus`, `thunderstorm_focus`, `water_whip_focus`, `hogging_focus`, `stellar_focus` and `void_flash_focus`.

No exact public source/tag matching installed `3.1.4` has been established. Registry membership in 3.1.0/3.1.1 therefore does not establish exact 3.1.4 behavior, reachability, cost, cooldown, targeting, settlement, API hooks or independent semantic eligibility.

## Matrix interpretation

| Capability family / clause | Authoritative Goety interpretation |
|---|---|
| Healing / regeneration / life transfer | The prior Wiki-visible `Soul Heal` and `Leeching` names remain valid documentary overlap. Treat them as behavior/name evidence only at the level already documented; do not read the 110-name list as the complete current registry or infer exact 3.1.4 mechanics. |
| Teleport / portals / displacement | The prior Wiki-visible Void names such as Recall, End Walk, Blink and Banish remain documentary overlap. The audited public source has **14 Void Focus registrations versus 12 Wiki names**, including source-only `stellar_focus` and `void_flash_focus`; their semantics are not inferred from identifiers. |
| Telekinesis / forced movement / gravity | `Telekinesis Focus` remains documentary overlap. The current-line registry strengthens provider-presence evidence but does not close exact 3.1.4 telekinesis mechanics. |
| Summons / familiars / servants | Goety remains the authority for its servant/summon lifecycle and Summon Down semantics. The 123-item Focus registry is not an ownership/lifecycle API and does not justify a generic Black Arcana familiar bridge. |
| Soul / spirit / death economy | Soul Energy remains Goety-owned. The source-registry reconciliation adds no permission to synthesize, mirror or settle a second Goety resource. Any integration still requires a verified provider-native seam. |
| Fire / infernal / soul fire | The ten Wiki-documented Nether Focus names remain valid overlap evidence. The audited public source has **11 Nether Focus registrations**, adding registry-only `hogging_focus`; no behavior is inferred from that source-only identifier. |
| Shields / wards / barriers | `Iron Hide` and `Bulwark` remain documentary overlap; exact 3.1.4 mechanics remain unverified. |
| Order / seals / imposed laws | `Order Focus` remains a verified Wiki-visible name, including the historical 109→110 Wiki correction. Its name still does not prove an imposed-law mechanic, and the source-registry reconciliation does not change that conclusion. |
| Transformation / alternate body state | Lichdom remains a publicly documented Goety-owned transformation. Exact 3.1.4 state/lifecycle/API semantics remain unverified. |
| Spell containers / cross-engine casting | Focus + Wand/Staff remains a provider-native casting-container model, not a cross-engine bridge. Registry enumeration does not change causal ownership or casting settlement. |
| Broad elemental/control/summon overlap | The 123-registration category distribution is current-line factual evidence that Goety's catalog is broader than the 110-name Wiki subset. It is a deduplication signal only until exact/current behavior and reachability are reconciled. |

## Semantic and Phase 3 result

This reconciliation contributes **+0** to the strict semantic magic-object denominator. The reconstructible minimum remains **796**.

Reasons:

- exact installed 3.1.4 JAR↔source equivalence is open;
- item registration alone does not prove player-facing/survival reachability as a discrete action;
- source-only IDs have not been behaviorally deduplicated;
- ritual categories are not treated as discrete ritual identities;
- no stable exact 3.1.4 integration API/event boundary has been established.

Every affected capability row remains `BLOCKED` for Phase 3 until its real semantic gap and required provider boundary are proven. Goety retains authority over Soul Energy, Focus casting, servants, rituals, progression and provider-owned settlement.

## Clean-room boundary

The audited `ModItems.java` path is under upstream `src/main/java/com/Polarice3/`, covered by the MIT scope stated in `Vivideru/Goety-3/LICENSE.txt`. The same upstream license file marks additions under `src/main/java/com/Vivideru/` All Rights Reserved unless separately stated.

Black Arcana uses the audited source read-only for factual identifiers, counts, version/blob provenance and deduplication evidence. No Goety implementation, assets, text, models or sounds are copied or adapted, and the mixed-license repository is not reclassified wholesale as MIT.
