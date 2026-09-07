# Malum 1.8.2 — provider catalog

## Status

`EXACT RELEASE 1.8.2 / EXACT VERSION COMMIT IDENTIFIED / PUBLISHER 1.8+1.8.2 CHANGELOG SURFACE VERIFIED / SOURCE-LICENSE CONFLICT BLOCKS IMPLEMENTATION-INTERNAL PROMOTION / EXACT REGISTRY+RUNTIME QA PENDING`

## Installed authority

- provider: **Malum**
- mod id: `malum`
- installed JAR: `malum-1.21.1-1.8.2.jar`
- runtime version: `1.8.2`
- loader/game: NeoForge 1.21.1
- role: `SPIRIT ARCANA / TYPED SPIRIT RESOURCE / SPIRIT RITE / TOTEM / GEAS-PROGRESSION PROVIDER`
- installed ecosystem additions: Gaze `1.1.7.1`; Malum: Vestis; JEI Malum.

The current physical modlist is authoritative for installed identity.

CurseForge independently identifies `malum-1.21.1-1.8.2.jar` as the latest 1.21.1 NeoForge release, published on `2025-12-08`.

## Exact version commit

The official `SammySemicolon/Malum-Mod` history contains commit:

`03b743a37f3eeb0cc7f4364f0730e1f135f78408`

at `2025-12-08T08:23:22Z`.

Its `gradle.properties` declares:

- `minecraft_version=1.21.1`;
- `mod_id=malum`;
- `mod_version=1.8.2`;
- `lodestone_version=1.8.2.523`.

This is strong version-line evidence and lets the audit anchor publisher-authored release/changelog material to the exact installed line.

## License/provenance conflict — implementation source remains blocked

There is a material license inconsistency:

- the public CurseForge project/release surface declares **GNU LGPLv3**;
- the exact `1.8.2` commit's `gradle.properties` declares `mod_license=All Rights Reserved`;
- the repository root at that commit does not expose a root `LICENSE` file that resolves the conflict;
- GitHub repository metadata exposes no license object.

Therefore Black Arcana does **not** promote exact-source implementation internals from this commit into implementable integration contracts. Until the conflict is resolved by an authoritative upstream license statement, the source-code layer is treated as `READABLE VERSION EVIDENCE / IMPLEMENTATION REUSE OR SOURCE-DERIVED SPEC BLOCKED`.

Publisher-authored changelogs and public gameplay documentation may still establish externally documented behavior, but they do not authorize copying code/assets or inventing hidden APIs.

## Provider identity — installed-line facts

Malum is a Spirit Arcana system where spirits are **typed provider resources**, not a generic mana bar. The current project guide and publisher documentation establish:

- spirit harvesting / Spirit Reaping;
- typed spirits used as provider resources and ingredients;
- Spirit Infusion;
- Spirit Focusing;
- Spirit Rites / totem magic;
- Spirit Rite Locus/Anchor behavior in the 1.8 line;
- spirit-powered gear, runes, tools, weapons and curios;
- Encyclopedia Arcana progression;
- Soulbinding as a provider crafting/process vocabulary;
- Geas/Pact/Oath/Authority progression existing in the installed 1.8 line.

Exact registry counts and full registry ids remain separate gates.

## Exact 1.8 publisher changelog — registry and rite architecture

The publisher's `changelogs/1.8.txt`, present at the exact 1.8.2 version commit, states that:

- **Spirit Types** moved to a Deferred Registry;
- spirit registry names now include a mod identifier plus name, explicitly affecting third-party compatibility;
- **Spirit Rites** moved to a Deferred Registry;
- addon rite providers such as Gaze need compatibility updates for that change;
- many Spirit Rites were redone;
- world-affecting rites now use a **Rite Locus** system;
- **Rite Anchors** can define a travel vector for a Rite Locus and different spirits can empower the locus differently;
- **Rite Unwaver** kills/removes an active Rite Locus when found.

This proves those architectural concepts belong to the installed 1.8 generation. It does **not** prove every registry entry currently seen on the later 1.9.0 branch exists unchanged in 1.8.2.

## Geas / Pacts / Oaths / Authorities — confirmed in installed line

The old preparatory catalog classified Geas as possible newer-branch-only content. That is no longer correct.

The publisher's 1.8 changelog explicitly discusses multiple Geas entries, including:

- Pact of the Prospector;
- Pact of the Profane Glutton;
- Pact of the Berserker;
- Pact of Wyrd Reconstruction;
- Pact of the Cloudskipper;
- Oath of the Overkeen Eye;
- Oath of Unmakers Disdain;
- Oath of Unsighted Resistance;
- Authority of the Gleeful Target.

The publisher's **1.8.2** changelog additionally changes:

- Pact of the Lone Druid;
- Pact of the High Priest;
- Pact of the Prospector;
- Pact of the Blastweaver, renamed from Pact of the Pyromaniac.

Therefore:

- `Geas/Pact/Oath/Authority exists in 1.8.2` = **PROVEN**;
- `the later 1.9.0 branch has exactly 34 active entries in the installed 1.8.2 JAR` = **NOT PROVEN**;
- commented-out Bond prototypes from newer source are **not installed-gameplay evidence** and remain excluded.

This is already a strong deduplication constraint for Black Arcana Binding: a feature is not novel merely because it calls a persistent tradeoff a Pact, Geas or Oath.

## 1.8.2 publisher changes with integration relevance

The exact `1.8.2` changelog documents several behavior changes relevant to external systems:

- the healing rite now triggers only when healing would have an effect;
- Spellwoven Sprites break blocks as if the player did it and fire `BlockDropsEvent` with the breaker listed as the player;
- Belt of the Prospector grants a documented chance to obtain Avarice from collecting valuables;
- Avarice changes fortune chance and can stack to a documented cap;
- multiple Geas were rebalanced/renamed in 1.8.2.

For Black Arcana/RPG causality, the Spellwoven Sprite note is particularly important: publisher documentation explicitly attributes the block-break event to the player. That still requires runtime/provider integration QA before using it as a mastery source, but it is stronger than inferring player authorship from a servant simply being nearby.

## Typed spirit-resource authority

A Malum spirit is not interchangeable with:

- Goety Soul Energy;
- Eidolon Soul capability/Soul Shards;
- Gravebound Souls;
- Iron's mana;
- Vampirism blood;
- Black Arcana Blood Reservoir mB;
- Black Arcana Infernal Lava mB;
- Toxony toxicity/affinity;
- generic XP or health.

At minimum, the installed release line publicly demonstrates typed spirit recipe semantics, including `malum:earthen` in 1.8.2 datapack/issue evidence. The full installed 1.8.2 Spirit Type registry remains pending and must not be replaced with the later 1.9.0 nine-type list until independently confirmed.

## Black Arcana 07.02 boundary

Black Arcana already uses the correct authority posture for Malum:

- real Malum spirit resources are provider-owned;
- automatic generic `death -> Malum spirit` harvesting is **fail-closed** when no verified causal/value hook proves the exact generated spirit identity/count;
- Black Arcana must not synthesize a second spirit economy from generic death events;
- read/consume/refund operations must use a verified provider boundary and preserve exactly-once settlement.

The Phase 2 catalog must not weaken that existing runtime safety decision merely because an exact 1.8.2 version commit was found.

## Spirit Rites and world effects

Malum Spirit Rites are persistent area/world effects rather than ordinary instant spell casts. The 1.8 changelog proves a Rite Locus model for world-affecting rites.

Consequences:

- do not map a Rite Locus tick to repeated Black Arcana casts;
- do not award mastery per tick merely because an area effect remains active;
- do not reapply world mutation through Black Arcana `WorldEffectPolicy` after Malum already performed a provider-owned mutation;
- if Black Arcana initiates a cross-provider operation, both the provider contract and Black Arcana world-safety admission must be preserved without double-processing.

The full 1.8.2 rite registry, recipes, ranges, durations and locus budgets remain pending.

## Geas collision with Binding / Pact design

Malum already proves first-class Geas/Pact/Oath/Authority gameplay in the installed line. Therefore Arcana Vincular must not degenerate into a second generic pact-buff system.

Its remaining viable delta is the previously approved architecture around:

- typed persistent relationships;
- explicit external resource authorities;
- transactional reserve/commit/refund;
- consent/ownership/protection;
- lifecycle and recursion prevention;
- cross-provider routing without collapsing provider resources.

A name change is not a semantic gap.

## Sacred / Infernal overlap

Later branch evidence shows Sacred/Infernal spirit terminology, but the complete installed 1.8.2 spirit registry has not yet been reconciled. Do not promote all later spirit names to installed coverage merely because the overall typed-spirit system is proven.

The safe separation remains:

- Malum spirits = typed Spirit Arcana resources/reagents;
- Divine/Celestial = Holy/miracle/theurgy domain if a distinct gap survives provider audit;
- Black Arcana Infernal Lava = proposed Nether-bound external fluid/reservoir authority, not a renamed Malum spirit.

## Installed addon boundaries

### Gaze 1.1.7.1

Separate Malum ecosystem addon. The 1.8 changelog explicitly notes that rite addons such as Gaze had to adapt to the Deferred Registry change, reinforcing that Gaze-provided rites must not be counted as base Malum content.

### Malum: Vestis

Separate equipment/vanity extension. Classify capability-by-capability rather than assuming new spell authority.

### JEI Malum

UI/recipe support, not a magic authority.

## Exact gates still open

1. reconcile the full installed 1.8.2 Spirit Type registry without relying on later 1.9.0-only source;
2. reconcile the exact installed 1.8.2 Spirit Rite registry and rite recipes/effects;
3. enumerate the complete installed 1.8.2 Geas/Pact/Oath/Authority set and acquisition model;
4. enumerate installed 1.8.2 Soulbinding/Infusion/Focusing recipes where relevant to deduplication;
5. identify a safe public integration boundary for spirit query/consume/refund and spirit-reaping causality;
6. validate Rite Locus/world-effect lifecycle and dedup semantics in runtime;
7. validate Spellwoven Sprite player-attributed block breaking in the exact modpack before RPG mastery consumes it;
8. reconcile the upstream license conflict before source-code internals inform implementable Black Arcana specs;
9. catalog Gaze/Vestis deltas separately.

## Phase 3 gate

Malum-related new design remains `BLOCKED` until enough of the exact 1.8.2 provider surface is reconciled to distinguish true gaps from renames/partial overlaps.

Finding the exact version commit does **not** by itself authorize source-internal integration.