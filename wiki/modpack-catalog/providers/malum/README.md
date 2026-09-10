# Malum 1.8.2 — provider catalog

## Status

`RELEASE 1.8.2 / RELEASE-BOUNDED CORE REGISTRY INVENTORY CLOSED / SPECIAL RITES PLAYER-FACING PROVEN / WHOLE-INTERVAL PATH HISTORY VERIFIED / PUBLISHER 1.8+1.8.2 CHANGELOG SURFACE VERIFIED / SOURCE-LICENSE CONFLICT BLOCKS IMPLEMENTATION-INTERNAL PROMOTION / RUNTIME/API QA PENDING`

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

## 1.8.2 release interval

The official `SammySemicolon/Malum-Mod` `1.21.1` history gives a bounded source interval for the installed version line:

- `f56691e56e591a6d8d1859ff119e749375e14d61` is the first observed checkpoint whose `gradle.properties` declares `mod_version=1.8.2`;
- its parent `966177b14b7f922bc12a135e34d1609cdb1eac7c` still declares `mod_version=1.8.1`;
- `03b743a37f3eeb0cc7f4364f0730e1f135f78408` is the last observed `1.8.2` checkpoint before the next version transition;
- its child `e875523840285212940aacb75627637909380175` declares `mod_version=1.8.3`.

Endpoint equality alone is not used to establish the inventory or the supporting semantic evidence. Path-history queries were run across the complete observed `1.8.2` window for the registry paths used below and for the player-facing progression path used to classify the two special rites:

- `MalumSpiritRiteTypes.java` — **0 commits** touch the path after entry into the 1.8.2 window and before the 1.8.3 transition;
- `MalumSpiritRiteEffectTypes.java` — **0 commits** touch the path in that interval; this is supporting deduplication evidence, not a fourth additive semantic inventory;
- `MalumSpiritTypes.java` — **0 commits** touch the path in that interval;
- `MalumGeasEffectTypes.java` — the path is touched at `f56691e...`, the initial 1.8.2 checkpoint itself, and has **no later commit** before the 1.8.3 transition;
- `client/screen/codex/entries/TotemMagicEntries.java` — **0 commits** touch the path in that interval; the blob remains `d0ba29e52abcd1f26cfa92f20951c4981ae3c661` at both endpoints.

Therefore there is no intervening registry or progression-entry edit-and-revert hidden by equal endpoint blobs on these stable paths. `CodexLangDatagen.java` is not treated as endpoint-stable: it is touched at exactly five checkpoints in the window (`f56691e...`, `3fb3c77...`, `a634061...`, `5a578eb...`, `fbcc606...`), and all five snapshots were checked for the two dedicated special-rite entries and their player-facing activation/presentation evidence.

The `1.8.2` checkpoints also declare:

- `minecraft_version=1.21.1`;
- `mod_id=malum`;
- `mod_version=1.8.2`;
- `lodestone_version=1.8.2.523`.

## License/provenance conflict — implementation source remains blocked

There is a material license inconsistency:

- the public CurseForge project/release surface declares **GNU LGPLv3**;
- the exact `1.8.2` source line's `gradle.properties` declares `mod_license=All Rights Reserved`;
- the repository root at those checkpoints does not expose a root `LICENSE` file that resolves the conflict;
- GitHub repository metadata exposes no license object.

Therefore Black Arcana does **not** promote source implementation internals from this line into implementable integration contracts. Until the conflict is resolved by an authoritative upstream license statement, the source-code layer is treated as `READABLE VERSION/FACTUAL CATALOG EVIDENCE / IMPLEMENTATION REUSE OR SOURCE-DERIVED SPEC BLOCKED`.

Publisher-authored changelogs and public gameplay documentation may still establish externally documented behavior. Read-only source inspection in this audit is limited to factual names, counts, path history, immutable blob identity, player-facing progression/recipe-page presence and deduplication for provenance/semantic accounting. It does not authorize copying algorithms, method bodies, assets, upstream prose or hidden integration behavior.

## Release-bounded core registry inventory

Whole-interval path history plus endpoint blob equality closes three provider-owned inventory registries for factual accounting across the observed `1.8.2` line. One additional Rite-effect registry is release-bounded only as supporting deduplication evidence and contributes no extra semantic-action identities. Player-facing progression evidence is handled separately so registry membership alone does not determine semantic eligibility.

### Spirit Rite types — 26 registered identities

`MalumSpiritRiteTypes.java` has blob SHA `2b9e4e5445733dee4ed205e4331d55c93ac86028` at both `f56691e...` and `03b743a...`, with no intervening path commit during the 1.8.2 window.

It contains **26 active base-Malum `SpiritRiteType` registrations**:

- special Arcane rites: `undirected_rite`, `unchained_rite`;
- Sacred: `rite_of_healing`, `rite_of_nourishment`, `rite_of_nurturing`, `rite_of_lust`;
- Wicked: `rite_of_harming`, `rite_of_empowerment`, `rite_of_culling`, `rite_of_rending`;
- Aerial: `rite_of_the_howling_gale`, `rite_of_the_sky_tether`, `rite_of_gravity`, `rite_of_ascension`;
- Aqueous: `rite_of_the_flowing_grasp`, `rite_of_the_good_tides`, `rite_of_soaking`, `rite_of_sapping`;
- Earthen: `rite_of_the_stone_ward`, `rite_of_the_oaken_might`, `rite_of_creation`, `rite_of_destruction`;
- Infernal: `rite_of_the_burning_fervor`, `rite_of_the_fiery_embrace`, `rite_of_smelting`, `rite_of_quickening`.

The supporting `MalumSpiritRiteEffectTypes.java` has blob SHA `e5fd8854c12783e4503475ccaf461c3a19c2a0b0` at both `f56691e...` and `03b743a...`, with no path commit anywhere in the observed 1.8.2 window. It registers separate `undirected_rite_effect` and `unchained_rite_effect` effect identities. This establishes that the two corresponding `SpiritRiteType` registrations do not share one effect identity; the effect registry itself contributes **0** additional semantic objects.

#### Player-facing eligibility of `undirected_rite` and `unchained_rite`

Registry separation is not used by itself to count the two special rites. Exact `1.8.2` `TotemMagicEntries.java` adds `undirected_rite` and `unchained_rite` separately to `ArcanaProgressionScreen`. Each entry uses its corresponding `RiteHolder` in both a `SpiritRiteTextPage` and a `SpiritRiteRecipePage`; the Unchained entry additionally exposes Unchained Transmutation content. The file has blob `d0ba29e52abcd1f26cfa92f20951c4981ae3c661` at both release-window endpoints and **zero path commits** inside the observed `1.8.2` interval.

As a second check, all five snapshots of `CodexLangDatagen.java` that exist in the release window preserve dedicated player-facing entries for both special rites. The Undirected entry consistently includes activation guidance requiring five runes. These observations prove player-facing rite reachability/presentation across the release line rather than mere technical registry existence.

Therefore both special IDs satisfy the ledger's ritual/rite semantic class and are counted once each. This evidence does **not** close exact recipe contents, numerical requirements, runtime execution mechanics or source/JAR byte equivalence.

For the semantic-magic ledger, the full **26 rites are additive**. Effects, recipe pages themselves and downstream locus/transmutation consequences do not create extra semantic objects.

### Geas effect types — 37 active registered identities, non-additive

`MalumGeasEffectTypes.java` has blob SHA `2aef164fcedae891b2c6805f2edbd8ee48cffbfe` at both ends of the `1.8.2` interval. Its only path touch in that interval is the initial `f56691e...` checkpoint; there is no later change before 1.8.3.

It contains **37 active `GeasEffectType` registrations**:

- 28 Pacts;
- 6 Oaths;
- 2 Authorities;
- 1 Creed.

Two proposed Bond registrations and `authority_of_crushing_melancholy` are commented out in the release-bounded source and are excluded.

These 37 entries are **not additive** to the current semantic-magic total. The ledger excludes effects/statuses and counts discrete magical action identities; Malum's Geas registry is an effect/progression registry rather than a spell/rite/action registry. The exact inventory is still important for collision/deduplication analysis against Black Arcana Binding/Pact design.

### Spirit types — 9 registered resource/type identities, non-additive

`MalumSpiritTypes.java` has blob SHA `fa772479f0f73131dabf33d9342299c7e20405e1` at both ends of the `1.8.2` interval, with no intervening path commit.

It contains **9 registered `SpiritArcanaType` identities**:

- `sacred`;
- `wicked`;
- `arcane`;
- `eldritch`;
- `aerial`;
- `aqueous`;
- `earthen`;
- `infernal`;
- `umbral`.

These are typed provider resource identities and therefore contribute **0** to the semantic-magic action total.

This closure is deliberately narrow: the three registry inventories above are release-bounded factual evidence only; the supporting Rite-effect registry is used only for deduplication; and the Codex/progression sources are used only to prove semantic reachability of the two special rites. It does not promote source-internal APIs or implementation behavior into Black Arcana contracts.

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

The base Spirit Rite, Geas and Spirit Type registry counts are now release-bounded for `1.8.2`; the two special rites also have release-bounded player-facing progression evidence. Runtime mechanics, acquisition paths, recipe contents and safe integration boundaries remain separate gates.

## Exact 1.8 publisher changelog — registry and rite architecture

The publisher's `changelogs/1.8.txt`, present inside the `1.8.2` release interval, states that:

- **Spirit Types** moved to a Deferred Registry;
- spirit registry names now include a mod identifier plus name, explicitly affecting third-party compatibility;
- **Spirit Rites** moved to a Deferred Registry;
- addon rite providers such as Gaze need compatibility updates for that change;
- many Spirit Rites were redone;
- world-affecting rites now use a **Rite Locus** system;
- **Rite Anchors** can define a travel vector for a Rite Locus and different spirits can empower the locus differently;
- **Rite Unwaver** kills/removes an active Rite Locus when found.

This proves those architectural concepts belong to the installed 1.8 generation. It does **not** turn source implementation internals into an integration API.

## Geas / Pacts / Oaths / Authorities — release-bounded in installed line

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

Release-bounded registry evidence now closes the installed `1.8.2` inventory at **37 active Geas effect-type identities**. Commented Bond prototypes and the commented Authority are not active installed-line registry evidence and remain excluded.

This is a strong deduplication constraint for Black Arcana Binding: a feature is not novel merely because it calls a persistent tradeoff a Pact, Geas or Oath. The 37 Geas entries remain outside the semantic-action total because the metric excludes effect/progression identities.

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

The release-bounded `1.8.2` registry closes the provider's nine base spirit-type identities as `sacred`, `wicked`, `arcane`, `eldritch`, `aerial`, `aqueous`, `earthen`, `infernal` and `umbral`. This does not imply that Black Arcana may synthesize, substitute, consume or refund them without a verified provider boundary.

## Black Arcana 07.02 boundary

Black Arcana already uses the correct authority posture for Malum:

- real Malum spirit resources are provider-owned;
- automatic generic `death -> Malum spirit` harvesting is **fail-closed** when no verified causal/value hook proves the exact generated spirit identity/count;
- Black Arcana must not synthesize a second spirit economy from generic death events;
- read/consume/refund operations must use a verified provider boundary and preserve exactly-once settlement.

The Phase 2 catalog must not weaken that existing runtime safety decision merely because the `1.8.2` semantic inventories are now release-bounded.

## Spirit Rites and world effects

Malum Spirit Rites are persistent area/world effects rather than ordinary instant spell casts. The 1.8 changelog proves a Rite Locus model for world-affecting rites.

The base `1.8.2` rite registry is release-bounded at **26 registered rite identities**, and exact progression/Codex evidence proves the two special Arcane entries are player-facing rather than registry-only proxies. That closes the semantic count, but not the full execution contract.

Consequences:

- do not map a Rite Locus tick to repeated Black Arcana casts;
- do not award mastery per tick merely because an area effect remains active;
- do not reapply world mutation through Black Arcana `WorldEffectPolicy` after Malum already performed a provider-owned mutation;
- if Black Arcana initiates a cross-provider operation, both the provider contract and Black Arcana world-safety admission must be preserved without double-processing.

Rite recipe contents, ranges, durations, locus budgets and exact runtime lifecycle remain pending.

## Geas collision with Binding / Pact design

Malum proves first-class Geas/Pact/Oath/Authority gameplay in the installed line, with the active `1.8.2` registry release-bounded at 37 entries. Therefore Arcana Vincular must not degenerate into a second generic pact-buff system.

Its remaining viable delta is the previously approved architecture around:

- typed persistent relationships;
- explicit external resource authorities;
- transactional reserve/commit/refund;
- consent/ownership/protection;
- lifecycle and recursion prevention;
- cross-provider routing without collapsing provider resources.

A name change is not a semantic gap.

## Sacred / Infernal overlap

The release-bounded `1.8.2` Spirit Type registry directly proves both `sacred` and `infernal` among Malum's nine typed spirits.

That narrows naming/design freedom but does not collapse authorities:

- Malum spirits = typed Spirit Arcana resources/reagents;
- Divine/Celestial = Holy/miracle/theurgy domain only if a distinct gap survives provider audit;
- Black Arcana Infernal Lava = proposed Nether-bound external fluid/reservoir authority, not a renamed Malum spirit.

## Installed addon boundaries

### Gaze 1.1.7.1

Separate Malum ecosystem addon. The 1.8 changelog explicitly notes that rite addons such as Gaze had to adapt to the Deferred Registry change, reinforcing that Gaze-provided rites must not be counted as base Malum content.

### Malum: Vestis

Separate equipment/vanity extension. Classify capability-by-capability rather than assuming new spell authority.

### JEI Malum

UI/recipe support, not a magic authority.

## Exact gates still open

1. establish byte-for-byte source/JAR equivalence or extract the exact installed JAR registry only if later runtime QA requires that stronger proof; this is no longer required for the narrow semantic count;
2. reconcile Spirit Rite recipe contents, ranges, durations, locus budgets and exact runtime lifecycle; player-facing recipe-page presence for the two special rites is already proven but does not close those mechanics;
3. reconcile Geas acquisition/lifecycle mechanics where needed for design collision analysis; the 37-entry active registry count itself is closed;
4. enumerate installed `1.8.2` Soulbinding/Infusion/Focusing recipes where relevant to deduplication;
5. identify a safe public integration boundary for spirit query/consume/refund and spirit-reaping causality;
6. validate Rite Locus/world-effect lifecycle and dedup semantics in runtime;
7. validate Spellwoven Sprite player-attributed block breaking in the exact modpack before RPG mastery consumes it;
8. reconcile the upstream license conflict before source-code internals inform implementable Black Arcana specs;
9. catalog Gaze/Vestis deltas separately.

## Phase 3 gate

Malum is no longer an open blocker for the **narrow semantic-action count**: its 26 base rite identities are release-bounded, and the two special Arcane rites have release-bounded player-facing progression evidence, so all 26 can enter the reconstructible minimum.

Malum-dependent runtime implementation and any design that requires source-internal APIs, exact execution mechanics or provider resource mutation remain `BLOCKED / FAIL-CLOSED` until the corresponding gates above are resolved. The overall Phase 3 gate remains blocked by other provider inventories and the still-open denominator.