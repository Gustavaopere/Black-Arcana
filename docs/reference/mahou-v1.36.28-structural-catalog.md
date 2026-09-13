# Mahou Tsukai 1.21.1 v1.36.28 — Clean-Room Structural Reference Catalog

## Status and boundary

This document is **reference/provenance only**. It does not make Mahou Tsukai a dependency and does not authorize copying its implementation or assets.

Exact artifact audited:

- CurseForge project: `342543`;
- file: `8860405`;
- filename: `mahoutsukai-1.21.1-v1.36.28.jar`;
- metadata mod id: `mahoutsukai`;
- metadata version: `1.21.1-v1.36.28`;
- metadata license: `All Rights Reserved`;
- SHA-1: `9049114ceea69d35e7469838f5a23d2655ebf133`;
- SHA-256: `0f79fcf98680fdba8d4bb96e85f2d715bdd22dfa67906712d8181a99dc075a43`.

The exact-artifact audit ran on isolated non-merge branch `audit/mahou-1.21.1-v1.36.28-exact-artifact`. It retained only cryptographic identity, metadata facts, class/resource paths, localization **keys**, serializer identities/counts and public signatures. It did **not** retain method bodies, recipe ingredients/payloads, localization prose, textures, models, animations, sounds, source reconstruction or binary redistribution.

Mahou Tsukai is absent from the supplied physical modlist. Everything below is a design/reference disposition, never a runtime integration contract.

## Interpretation rules

- Reference names remain in this document only so provenance/disposition is auditable.
- Player-facing implementations use original Black Arcana identity unless a term is generic.
- An exact class/field/localization identity proves presence, not behavior.
- Legacy behavior already documented from public/observable sources in the earlier Black Arcana reference catalog may be reused as specification evidence.
- Newer identities require separate public/observable behavior provenance before implementation if their semantics are not already documented.
- No recipe, staff, scroll, Mahou mana-growth mechanic, self-cutting activation or Mahou asset is imported.

## Complete exact circle/reference identity inventory

The v1.36.28 structural audit identified the following **53 circle/reference identities**. `Disposition` is a planning decision, not implemented state.

| # | Reference identity | Black Arcana disposition | Preferred host / authority | Behavior evidence gate |
|---:|---|---|---|---|
| 1 | Alarm Boundary | `REUSE_EXISTING_BA` / ward-field concept | BA field/runtime; Eidolon presentation optional | legacy public/observable catalog |
| 2 | Displacement Boundary | `REUSE_EXISTING_BA` | Stage 07.04 Space & Displacement | legacy public/observable catalog |
| 3 | Tangible Boundary | `REUSE_EXISTING_BA` or merge into ward/domain field | BA field/runtime | legacy public/observable catalog |
| 4 | Gravity Boundary | `BA_NATIVE_NEW` only if still distinct after Stage 07 audit | BA bounded field; Iron's presentation optional | legacy public/observable catalog |
| 5 | Raise Enclosure | `REUSE_EXISTING_BA` / field shelter if justified | BA world-safe field; Eidolon presentation optional | legacy public/observable catalog |
| 6 | Drain Life Boundary | `REUSE_EXISTING_BA` | Stage 07.01 `Sanguine Harvest`; 07.08 blood composition | legacy public/observable catalog |
| 7 | Contract | `RITUAL_UNLOCK` / merge with reviewed bargain contract | Stage 06 BA ritual; Eidolon presentation optional | legacy public/observable catalog |
| 8 | Strengthening | `REUSE_EXISTING_BA` / Projection & Arsenal strengthening | Stage 07.03; provider-native equipment hooks where proven | legacy public/observable catalog |
| 9 | Projection | `REUSE_EXISTING_BA` | Stage 07.03 Projection & Arsenal | legacy public/observable catalog |
| 10 | Reality Marble | `REUSE_EXISTING_BA` | Stage 07.06 Forbidden Domains under D032 | legacy public/observable catalog |
| 11 | Treasury Projection | `REUSE_EXISTING_BA` / merge | Stage 07.03 Projection & Arsenal | legacy public/observable catalog |
| 12 | Weapon Shooter | `REUSE_EXISTING_BA` / merge | Stage 07.03; Iron's host if safe | legacy public/observable catalog |
| 13 | Power Consolidation | `REUSE_EXISTING_BA` / bounded strengthening progression | Stage 07.03 + Stage 08 balance | legacy public/observable catalog |
| 14 | Proximity Projection | `REUSE_EXISTING_BA` | Stage 07.03 / 07.04 depending final semantic split | legacy public/observable catalog |
| 15 | Catalyst Exchange | `PROVIDER_NATIVE_FIRST` or `DROP_OR_MERGE` | Ars/Eidolon/Malum resource systems only through real contracts | legacy public/observable catalog |
| 16 | Durability Exchange | `PROVIDER_NATIVE_FIRST` or bounded BA cost strategy | provider-native item cost first | legacy public/observable catalog |
| 17 | Damage Exchange | `BA_NATIVE_NEW` only if distinct from canonical Blood Price/cost models | BA canonical cost transaction | legacy public/observable catalog |
| 18 | Chronal Exchange | `DROP_OR_MERGE` unless safe bounded time fantasy survives review | BA world safety required; no global time abuse | legacy public/observable catalog |
| 19 | Alchemical Exchange | `PROVIDER_NATIVE_FIRST` | Ars/Eidolon/Malum native transformations first | legacy public/observable catalog |
| 20 | Immunity Exchange | `BA_NATIVE_NEW` only as bounded conditional defense | BA server state; Iron's presentation optional | legacy public/observable catalog |
| 21 | Scrying | `REUSE_EXISTING_BA` | Stage 07.07 Noetic/Divination after completion | legacy public/observable catalog |
| 22 | Projectile Displacement | `REUSE_EXISTING_BA` | Stage 07.04; Iron's projectile host optional | legacy public/observable catalog |
| 23 | Protective Displacement | `REUSE_EXISTING_BA` | Stage 07.04 safe displacement | legacy public/observable catalog |
| 24 | Equivalent Displacement | `REUSE_EXISTING_BA` or merge | Stage 07.04 | legacy public/observable catalog |
| 25 | Ordered Displacement | `REUSE_EXISTING_BA` / bounded chain displacement | Stage 07.04 | legacy public/observable catalog |
| 26 | Mental Displacement | `REUSE_EXISTING_BA` | Stage 07.07 Astral Severance only after end-to-end completion | legacy public/observable catalog |
| 27 | Ascension | `PROVIDER_NATIVE_FIRST` / merge into displacement utility | Ars native utility or Stage 07.04 if distinct | legacy public/observable catalog |
| 28 | Mystic Eyes | `REUSE_EXISTING_BA` / divination umbrella | Stage 07.07 | legacy public/observable catalog |
| 29 | Prediction | `REUSE_EXISTING_BA` / divination umbrella | Stage 07.07 | legacy/public behavior must match adopted scope |
| 30 | Death Collection | `REUSE_EXISTING_BA` | Stage 07.02 Souls & Death / Mortal Ledger family | legacy public/observable catalog |
| 31 | Reversion Eyes | `REUSE_EXISTING_BA` or provider-native cleanse | Stage 07.07 + Iron's/Ars effect hooks if proven | legacy public/observable catalog |
| 32 | Black Flame | `REUSE_EXISTING_BA` | Stage 07.05 Black Flame | legacy public/observable catalog |
| 33 | Fay Sight | `REUSE_EXISTING_BA` / divination | Stage 07.07 | legacy public/observable catalog |
| 34 | Familiars Garden | `REUSE_EXISTING_BA` / merge | Stage 07.07 familiar substrate; provider host only if safe | legacy public/observable catalog |
| 35 | Swap Familiar | `REUSE_EXISTING_BA` / familiar command | Stage 07.07 | legacy public/observable catalog |
| 36 | Recall Familiar | `REUSE_EXISTING_BA` / familiar command | Stage 07.07 | legacy public/observable catalog |
| 37 | Summon Familiar | `REUSE_EXISTING_BA` / familiar lifecycle | Stage 07.07; Goety only if exact ownership hook selected | legacy public/observable catalog |
| 38 | Butterfly Effect | `PENDING_BEHAVIOR_PROVENANCE` | no provider assigned until semantics are proven | exact identity proven; behavior requires source check |
| 39 | Insight | `REUSE_EXISTING_BA` / divination inspection if justified | Stage 07.07 | legacy public/observable catalog |
| 40 | Possess Entity | `BA_NATIVE_NEW` only under strict agency/identity safety | BA server authority; optional provider presentation | exact identity proven; adopted behavior requires reviewed provenance/policy |
| 41 | Rho Aias | `PROVIDER_HOSTED_BA_AUTHORITY` / original barrier | Iron's preferred combat presentation; BA safety/semantics | legacy public/observable catalog; reference name not player-facing |
| 42 | Mystic Staff | `DROP_ITEM_SURFACE / REEXPRESS_BEHAVIOR` | no universal staff; active powers routed individually | legacy public/observable catalog |
| 43 | Spatial Disorientation | `PROVIDER_HOSTED_BA_AUTHORITY` or `REUSE_EXISTING_BA` | Stage 07.04; Iron's host if safe | legacy public/observable catalog |
| 44 | Borrowed Authority | `BA_NATIVE_NEW` or merge into dangerous projection/arsenal effect | BA authority; Iron's presentation optional | legacy public/observable catalog |
| 45 | Damage Replication | `BA_NATIVE_NEW` only with bounded stored-damage ledger | BA canonical combat/danger state | legacy public/observable catalog |
| 46 | Cup of Heaven | `RITUAL_UNLOCK` / bounded debuff-domain concept if retained | Stage 06 ritual + BA field/domain | legacy public/observable catalog; reference name replaced |
| 47 | Retribution | `BA_NATIVE_NEW` or merge with Blood/Curses exchange | BA canonical transaction | legacy public/observable catalog |
| 48 | Presence Concealment | `PENDING_BEHAVIOR_PROVENANCE` then likely divination/stealth disposition | Stage 07.07 / provider-native stealth only if exact | exact identity proven; behavior must be reverified |
| 49 | Gandr | `PENDING_BEHAVIOR_PROVENANCE` then likely fixed active combat spell | Iron's preferred host if adopted | exact identity proven; behavior must be reverified |
| 50 | Fallen Down | `PROVIDER_HOSTED_BA_AUTHORITY + RITUAL_UNLOCK` -> original **Ruinous Zenith** | Stage 06 unlock; Iron's preferred cast host; BA world/hazard authority | exact identity + public behavior provenance required before implementation |
| 51 | Geas | `BA_NATIVE_NEW + RITUAL_UNLOCK` only with strict agency/PvP policy | Stage 06 BA ritual; Eidolon presentation optional | exact identity proven; behavior must be reverified |
| 52 | Probability Alter | `PENDING_BEHAVIOR_PROVENANCE` | BA only if bounded deterministic hook exists | exact identity proven; behavior must be reverified |
| 53 | Selective Displacement | `REUSE_EXISTING_BA` if observable semantics fit Stage 07.04 | Stage 07.04 | exact identity proven; behavior must be reverified |

## Decorative/projector identity

The exact artifact also exposes a Mahoujin/projector block identity. Black Arcana does **not** reuse its assets or remote/projector behavior. The corresponding desired fantasy is handled by Stage 07A.06 as an original local data-driven sigil/mandala presentation layer.

## Behavior-bearing item reference inventory

The exact artifact contains reference item identities including, among others, weapon/staff/mystic-code surfaces such as Caliburn, Clarent, Morgan, Rhongomyniad, Ripper, Replica, Rule Breaker, William-related content, Treasury Projection Gauntlet, Explosion Staff and Spatial Staff.

These items are **not** imported. The user requirement explicitly excludes Mahou recipes, staves and scrolls. If any item contains a distinct valuable observable mechanic, that behavior is catalogued separately from public/observable evidence and re-expressed as an original Black Arcana spell/ritual/progression concept or deliberately dropped/merged.

A class/signature identity alone is not enough to claim how any of these items behaves.

## Current high-level consolidation against Black Arcana

Large parts of the reference inventory are already represented by canonical Black Arcana domains and should not be rebuilt:

- life drain / blood theft -> Stage 07.01 Blood & Curses;
- death avoidance/resurrection -> Stage 07.02 Souls & Death;
- weapon projection/arsenal -> Stage 07.03 Projection & Arsenal;
- displacement -> Stage 07.04 Space & Displacement;
- spreading black-fire fantasy -> Stage 07.05 Black Flame;
- bounded arena/domain fantasy -> Stage 07.06 Forbidden Domains;
- familiar/divination/astral viewing -> Stage 07.07 after completion;
- blood storage/vampiric sustenance -> Stage 07.08 after implementation.

Stage 07A therefore focuses on polarity, fusion, metamagic, original presentation and the small set of genuinely distinct reference fantasies that survive deduplication.

## Clean-room adoption checklist

Before implementing any row:

1. public/observable behavior source recorded;
2. original Black Arcana identity assigned;
3. duplication check against current `main` completed;
4. provider authority/hook verified against exact physical version;
5. cost/cooldown/target/scaling/progression/world/boss-PvP/config/test specification written;
6. polarity/source/agency semantics written;
7. no Mahou asset/code/text/recipe/item implementation required;
8. deterministic tests designed before implementation.

Anything failing this checklist remains reference-only/fail-closed.
