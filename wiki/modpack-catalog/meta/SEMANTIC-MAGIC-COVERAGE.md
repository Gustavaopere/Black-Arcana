# Semantic Magic Coverage Ledger

## Purpose

This file is the reconstructible ledger for the user-facing semantic-magic coverage metric. It is deliberately separate from the provider-component closure metric in [`CATALOG-COVERAGE-CURRENT.md`](./CATALOG-COVERAGE-CURRENT.md).

A semantic magic object is one discrete provider-owned magical action identity that belongs to one of these classes:

- standalone spell;
- Ars glyph/spell-part primitive;
- ritual/rite;
- equivalent discrete supernatural player action when the provider uses an action/focus model instead of a spell registry.

The ledger does **not** count provider/JAR totals, schools by themselves, items, gear, familiars, affixes, machines, effects/statuses, resource entries, ordinary recipes/processes, classification tags, proxy registry slots, aliases, physicalization of an already-owned spell, arbitrary Ars spell compositions, or downstream consequences of one causal cast/action.

A provider-native identity is counted once under its semantic owner. Bridge/compat behavior does not mint a second spell identity merely because it observes, modifies, transports or physicalizes an existing provider action.

## Physical and repository anchor

- Minecraft: **1.21.1**
- NeoForge: **21.1.248**
- physical modlist: **595 top-level entries**
- physical modlist SHA-1: `7aaece7acbfb07ba4d0c66029042f36c50d046f0`
- reconstruction base: `main@4f3dab1a4801393873f9d4b7857782fcf6298e56`
- base post-merge validation: Black Arcana CI **#2349**, attempt 2 GREEN on the exact base SHA
- Phase 2BE canonicalized at `main@cce7f51794e4e65b0d97511eb55f710afc6e02f0`: PR #189 exact HEAD `e787699d25b283b8040cd179f605143e8ee396de` passed Black Arcana CI **#2483**; the merge SHA passed Black Arcana CI **#2484 attempt 2** GREEN after attempt 1 ended on an external `code.redspace.io` read timeout before compilation/tests
- Phase 2BM component closure is validated at `main@f2cdfe7b79d500540c281d70a76e8b6e3a77d311`: PR #210 exact HEAD `1b8d5d5761569f8ef1f3a32b7ece84cfb6ce6df6` passed Black Arcana CI **#2543**; the merge SHA passed exact-SHA post-merge CI **#2544** / run `34713268914` and published canonical QA artifact `10303624842` (`sha256:f4ff7ce2fac582f435f037f3a8dd29469df25d8889b895b0c168c2b0d6da0719`)
- Phase 2BN component closure is validated at `main@c1c422b5ec72fe4308104f04282732d6c2f2bbc1`: PR #212 exact HEAD `c4facc0286dab0b522bf2b09c5812ffdd935bd5d` passed Black Arcana CI **#2553** / run `34720437808`; the merge SHA passed exact-SHA post-merge CI **#2554** / run `34720646567` and published canonical QA artifact `10306246238` (`sha256:a63f42f6746cc62e435e6a1c541daaed973b0b56d3dcc566cbc7cf4e9fa57e96`)
- Phase 2BO evidence is validated at `main@34a5fd495da744800b32b051e38c6473c6f5ea15`: PR #214 exact corrected HEAD `d3a92c31d7ac5b38183224ef28c6737e721fc758` passed Black Arcana CI **#2564** / run `34723967662`; the merge SHA passed exact-SHA post-merge CI **#2565** / run `34724351805` and published canonical QA artifact `10307207453` (`sha256:50b94c3efc207dfd143a10367cf234473ede7dbbc1f36b9acdd3d3ca1ccc67fa`)
- Phase 2BP evidence is validated at `main@84e9635b446b605140ab349fa2edc51f3462d518`: PR #219 exact reconciled HEAD `6e39a01273b77ba8accf85d49647b6ceff840e8a` passed Black Arcana CI **#2577** / run `34730598682`; the evidence merge SHA passed exact-SHA post-merge CI **#2578** / run `34730783233`.
- Phase 2BQ exact-artifact closure is validated at `main@bc5428b5855e4d5821d5bd901fb591a62ecf3cbe`: NON-MERGE PR #222 audit HEAD `9a3620209e27bb74934c8a9740678b7e59df39c6` passed exact artifact run `34735280002`; durable PR #223 HEAD `0eec58c14e591f6d2c875172bec4e436f8e1d5cb` passed Black Arcana CI **#2618** / run `34735444723`; the exact merge SHA passed post-merge CI **#2622** / run `34735586680` and published canonical QA artifact `10310957237` (`sha256:de930eaba7f0f5730810747050ec500b4d72ed793cfbdce0c8603e3af8d8cc9d`).
- Phase 2BR GTBC's Geomancy Plus closure is validated at `main@4ab4ad990d453938e67f3d2b7cfa878bbe031ef0`: structural audit run `34737230548`, registry reconciliation run `34737352893`, and Geo reachability run `34738729721` are GREEN; durable PR #226 exact merge SHA passed post-merge CI **#2654** / run `34738972649` and published canonical QA artifact `10311522907` (`sha256:c815f684a7a6dec192dd995bb6fbd6784c35faa0b0d21ae39bb9de89b93cec16`).
- Phase 2BS T.O Magic n' Extras partial catalog is validated at `main@0bd1c04460e63a03b6b484b785247e75f6e44178`: durable PR #228 passed exact-head CI #2679 / run `34741531727`; the merge SHA passed exact-SHA post-merge CI #2682 / run `34741699505` and published canonical QA artifact `10311724779` (`sha256:05e28f0dc516e3b51bbd9016a37816cd1854e45caeaa71745189b20297ae3813`). Phase 2BS catalogs 33 exact registered identities but contributes +0 strict and no component closure.
- Phase 2BT Vampire Spells Addon source-pinned zero closure is validated at `main@1c5091807a8773d378c34ffac2e737b5f08b545c`: durable PR #239 closes release/source `0.0.9` as `ZERO_BRIDGE_INFRA`, and exact-SHA post-merge Black Arcana CI run `34795795283` completed GREEN. Phase 2BT contributes +0 strict; the separate shared-ledger reconciliation promotes technical component #67.

The historical chat-only tally is not an authority and is not used as an input to any sum below.

## Evidence states

| State | Meaning | Included in strict counted minimum? |
|---|---|---:|
| `COUNTED_EXACT` | current physical/runtime identity and exact current inventory are directly closed | yes |
| `COUNTED_SOURCE_PINNED` | current semantic inventory is closed at a matching source/version checkpoint; byte-for-byte JAR reproducibility may remain open | yes |
| `COUNTED_RELEASE_BOUNDED` | current/release-bounded evidence closes the semantic count even though implementation internals remain partially unavailable | yes |
| `CONDITIONAL` | registry/action exists, but current config, survival reachability or active eligibility is not closed strongly enough | no |
| `LOWER_BOUND` | current evidence proves at least this many objects, but not the complete current inventory | no |
| `OPEN` | no safe current semantic count can yet be declared | no |
| `ZERO_BRIDGE_INFRA` | audited provider adds no independent object under this metric | zero |
| `ZERO_SEMANTIC_PORTAL_INFRA` | exact portal/compat provider adds no independent spell/glyph/ritual/rite/action identity under this metric | zero |
| `EXCLUDED` | a registry/content entry exists but fails this metric by definition | zero |

`COUNTED_*` is a semantic-inventory confidence state. It is **not** a claim that runtime QA, compatibility QA or every numerical mechanic has passed.

## Phase 2BT — Vampire Spells Addon 0.0.9 source-pinned zero-semantic closure

Official release `1.21.1-0.0.9` and exact source target `xsharov/VampireSpellsAddon@2d36e94e67611a316b7311b11e4574b499025580` close the provider as a compatibility/runtime-policy overlay rather than an independent spell provider. `SpellIds` references Iron's-owned spell/school identities under namespace `irons_spellbooks`; the audited registration path installs Iron's/Vampirism integration listeners and does not register a provider-owned spell, school, ritual or equivalent discrete magical action.

Phase 2BT is therefore `ZERO_BRIDGE_INFRA` and contributes **+0 semantic magic objects**. The strict reconstructible minimum remains **1344**. PR #239 merged the durable audit as `main@1c5091807a8773d378c34ffac2e737b5f08b545c`, whose exact post-merge Black Arcana CI run `34795795283` is GREEN. The shared reconciliation promotes only the separate technical provider-component metric to **#67 / 67 of 100**. Physical-JAR byte equality, reflective bridge resolution, mixin/event ordering, effective serverconfig and live resource/damage/cooldown settlement remain runtime QA and are not inferred from this catalog closure.

## Phase 2BS — T.O Magic n' Extras / Traveloptics 4.4.0.1-1.21.1 historical partial catalog

Historical publisher file `6342780` closes **33 unique registered `traveloptics:<id>` spell identities**, 33 field→class→ID mappings and zero registry initializer branches for that audited release. Current sibling `neoforge-rpg-skilltree@76cf13e7d1110116f67c290eaa15891888279fc1` contains no current status-prefixed/categorized Traveloptics physical row. It retains only a legacy uncategorized `modlist/to-magic-n-extras.md` export bound to the older 595-mod snapshot, so the Phase 2BS row is provenance only and is not a current denominator/blocker. The same exact alpha carries 32 additional root localization spell IDs that are not registered and are excluded. Provider ancestry proves `AbstractUniqueSpell.allowCrafting() = false` and `AbstractWeaponSpell.allowCrafting() = true`; nine of ten Unique registrations have direct structured loot anchors, while `traveloptics:blackout` remains object-level survival-unresolved.

A focused exact-artifact audit also proves a runtime-risk wiring fact: `TOLootModifiers` registers both `key_loot` and `universal_loot`, while `KeyLootModifier.CODEC` is referenced twice and `UniversalLootModifier.CODEC` zero times. Black Arcana does not claim the reported runtime crash is reproduced, but runtime viability remains fail-closed. Consequently all 33 registry identities remain catalog inventory rather than a strict counted promotion: Phase 2BS contributes **+0 strict**, the reconstructible minimum stays **1344**, and technical component closure stays **66/100 at that checkpoint**.

## Phase 2BR — GTBC's Geomancy Plus 1.1.0-1.21.1 release-bounded spell closure

The exact publisher release artifact for file `7041615` closes **12 unconditional provider-owned `GGSpells` registrations**: ten Geo (`chunker`, `dripstone_bolt`, `eroding_boulder`, `fissure`, `geo_conductor`, `petrivise`, `pillar_of_the_resounding_earth`, `seismic_surf`, `tremor_spike`, `tremor_step`) and two Holy (`solar_beam`, `solar_storm`). `EarthshatterSpell` exists in the artifact but is unregistered and excluded; `EarthquakeMixin` and `StormSpellMixin` are non-registry adaptation classes and add zero provider identities.

The repository does not preserve an independent cryptographic hash of the local physical GTBC Geomancy Plus JAR. The exact publisher-release artifact is aligned to the installed mod-id/version line, so the correct evidence state is **`COUNTED_RELEASE_BOUNDED`**, not `COUNTED_EXACT`. Registry reconciliation records 12 fields, 12 `registerSpell(...)` calls, zero initializer branches, zero registry config refs and zero registry mod-gate refs. A separate exact-release audit proves all ten registered Geo classes directly inherit Iron's `AbstractSpell` and do not override `allowCrafting`, `isEnabled` or `canBeCraftedBy`; exact Geo focus data plus the canonical Iron's Scroll Forge contract close catalog-level Geo reachability. Exact Umvuthi loot identifiers and the exact release changelog close catalog-level acquisition for the two Holy spells. Deployed generic host config and full assembled-pack behavior remain separate runtime QA.

Phase 2BR therefore contributes **+12 `COUNTED_RELEASE_BOUNDED`** semantic magic objects. The Iron's ecosystem subtotal becomes **570**, the strict reconstructible minimum becomes **1344**, and provider component **#66 / 66 of 100** is promoted separately by this shared reconciliation. Runtime compatibility, terrain/protection settlement, Mowzie integration, live loot, multiplayer/reload and numerical balance remain fail-closed.

## Phase 2BQ — Ars Nouveau: Two-Way Portals 2.0.0 exact zero-semantic portal closure

Exact hash-matched artifact evidence closes physical `ars_two_way_portals-2.0.0.jar` / SHA-1 `233846fc30667893c5f36a719da576d5eed43f5c` as portal/compat infrastructure rather than an independent spell provider. NON-MERGE PR #222 materialized exact CurseForge file `8515817`; the exact JAR contains 25 provider classes, two provider item members, three recipe resources and seven required common mixins. Structural inspection found zero hits for `AbstractSpell`, `AbstractGlyph`, `SpellRegistry`, `registerSpell`, Ritual, Rite or Ability, and zero semantic spell/glyph/ritual/rite/ability resource paths.

Phase 2BQ therefore contributes **+0 semantic magic objects** as `ZERO_SEMANTIC_PORTAL_INFRA` and leaves the strict reconstructible minimum at **1332**, while this shared reconciliation separately closes provider component **#65 / 65 of 100**. Exact metadata declares required NeoForge `[21.1.243,)`, Ars Nouveau `[5.12.1,6.0.0)`, and optional `immersive_portals_core [6.0.7,7.0.0)`; declared-range satisfaction is not an assembled-runtime PASS. Portal lifecycle, effective config, mixin application, persistence, optional Immersive behavior, frame/Weave mutation and multiplayer/protection behavior remain fail-closed.

## Phase 2BP — SnackPirate's Aeromancy Additions 1.2.8 source-pinned spell closure

The physical provider `aero_additions-1.2.8.jar` / SHA-1 `dee32c9fa84d6e39846608f8f77591ea56f` is reconciled with exact public source `snackerpirater/aero-additions@ae282b32d25ad76ef8d01c637ec05566a767ae4c`, whose complete recursive tree closes version 1.2.8. The source registry contains exactly ten active unconditional Iron's `AbstractSpell` identities: `wind_charge`, `updraft`, `airstep`, `asphyxiate`, `feather_fall`, `wind_shield`, `airblast`, `wind_blade`, `flush` and `dash`.

Five additional spell classes/prototypes — Tornado, Thunderclap, Summon Breeze, Telelink and Shapeshift — have commented-out `registerSpell(...)` lines at the audited pin and are excluded. The Wind school itself is taxonomy rather than an eleventh semantic action. Provider Wind focus data plus the Iron's 3.16.3 Scroll Forge contract close a catalog-level host-native route through `minecraft:breeze_rod`; provider loot modifiers also add Breeze Rod support to Trial Chamber normal-vault rewards. Updraft Tome and Wind Sword embed already-counted provider spells and add zero extra semantic identities.

Phase 2BP therefore contributes **+10 `COUNTED_SOURCE_PINNED`** semantic magic objects. The Iron's ecosystem subtotal becomes **558**, and the strict reconstructible minimum becomes **1332**. Provider component **#64 / 64 of 100** is promoted separately by this shared catalog reconciliation. No assembled-pack runtime PASS is claimed: current-pack client/server boot, required mixins, payload behavior, physical Scroll Forge/config behavior and representative casts remain direct QA gates.

## Phase 2BO — Farmer's Spell 'n Spellbooks 1.0.5.1 source-pinned spell closure

The physical provider `farmers-spell-n-spellbook-1.0.5.1-1.21.1.jar` / SHA-1 `f77355e029af39bbaba3854e10cc087a608351ff` is reconciled with exact public source `GLDYM/Farmers-Spell-n-Spellbook@b7cbb40316a9ccbbc2ce2b56b3023647261ce569`, whose signed version-bump commit closes the `1.0.5.1-1.21.1` source line. The source registry contains exactly six unconditional provider-owned Iron's `AbstractSpell` identities under the Gluttony school: `goodberry`, `phantom_loot`, `seal_coat`, `bad_apple`, `chaos_slash` and `preserve_circle`.

The Gluttony school itself is taxonomy rather than a seventh semantic action. Generic random Iron's scroll loot is not used as reachability proof because the school sets `allowLooting=false`; provider data instead supplies a Gluttony focus (`#minecraft:foods` plus `farmers_spell:foodgeist_seasoning`), and the Iron's 3.16.3 source-line Scroll Forge contract supplies the host-native focus-to-school/spell route. No provider override of `allowCrafting`, `isEnabled` or `canBeCraftedBy` was found for the six spell classes. This closes catalog-level reachability while leaving assembled-pack runtime QA separate.

Phase 2BO therefore contributes **+6 `COUNTED_SOURCE_PINNED`** semantic magic objects. The Iron's ecosystem subtotal becomes **548**, and the strict reconstructible minimum becomes **1322**. Provider component **#63 / 63 of 100** is promoted separately by the shared catalog reconciliation. Runtime compatibility remains fail-closed: source build NeoForge `21.1.238` and Farmer's Delight `1.3.2` differ from physical NeoForge `21.1.248` and Farmer's Delight `1.3.4`; all seven provider mixins are required. GeckoLib is `4.9.2` on both source build and physical pack by version label, which is not itself a runtime PASS.

## Phase 2BN — Ars Sable 1.1.2 source-pinned zero-semantic spatial bridge

Exact official source `baileyholl/ars-sable@1fd83f3a998e3a41b5a21d0d6529140a0b0a55ba` matches the physically installed provider version `1.1.2` and closes the provider's technical role as Ars Nouveau ↔ Sable spatial/sublevel compatibility infrastructure. The exact source establishes 24 common + 5 client required mixins, protocol registrar version `2`, zero provider-owned payload registrations, and no provider-owned spell, glyph, ritual, school, mana/resource or equivalent independent magical-action registry.

Phase 2BN therefore contributes **+0 semantic magic objects** and leaves the strict reconstructible minimum at **1316** at that historical checkpoint, while separately closing provider component **#62 / 62 of 100**. This is a source-pinned technical/catalog closure, not a runtime compatibility PASS: exact source was built against Sable `1.2.2` while the physical pack uses `2.0.5`, and against Ars Nouveau `5.11.7.1354` while the pack uses `5.13.1`; all 29 mixins are required. The source metadata/root license surfaces also conflict (`LGPLv3` metadata vs The Unlicense root file), so clean-room factual inspection does not infer reuse rights.

## Phase 2BM — Ars Polymorphia 1.0.3 source-pinned zero-semantic bridge

Exact official source `Vonr/Ars-Polymorphia@e09b6c9ab434ccbb3232ca47b37ca5666becfb6f` matches the physically installed provider version `1.0.3` and closes the provider's technical role as an Ars Storage/Crafting Lectern ↔ Polymorph recipe-conflict bridge. The exact source establishes five required mixin/accessor bindings, protocol version `1`, one provider-owned play-to-server unit payload, and no provider-owned spell, glyph, ritual, school, mana/resource or equivalent independent magical-action registry.

Phase 2BM therefore contributes **+0 semantic magic objects** and leaves the strict reconstructible minimum at **1316** at the later post-2BL baseline, while separately closing provider component **#61 / 61 of 100**. This is a source-pinned technical/catalog closure, not a runtime compatibility PASS: exact source requires mod id `polymorph` while the physical pack exposes `polymorph_plus` `1.3.1+1.21.1`; source was built against Ars Nouveau `5.4.2.938` while the pack uses `5.13.1`; and source metadata declares `minecraft_version=1.21.1` together with `minecraft_version_range=[1.21,1.21.1)`. Current-host runtime behavior remains fail-closed.

## Phase 2BL — Goety Iron 3.1 + Goety Cataclysm 1.21.1-1.8.2

Exact hash-matched artifact evidence closes both remaining Goety addon rows without duplicating base-Goety ownership. Goety Iron contributes **2 Focus + 12 distinct non-Focus rituals = +14**. Goety Cataclysm contributes **28 Focus + 24 distinct non-Focus rituals = +52**. Focus-acquisition recipes are deduplicated against the Focus identities themselves. Targeted scans find no mod-loaded conditions on the counted non-Focus rituals, while registry initializers have zero conditional branches and zero config references; no enable/disable-like registration gate was found.

Evidence is isolated in NON-MERGE PRs #205 and #206. Phase 2BL therefore adds **+66 `COUNTED_EXACT`**, moving the strict reconstructible minimum from **1250 to 1316** and, separately, closing provider components **#59 and #60**. Runtime/balance/servant-lifecycle QA remains separate and fail-closed.

## Phase 2BK exact zero closure — Ignis Soulfires: Spellbooks 1.1.0

Exact hash-matched artifact evidence closes Ignis Soulfires: Spellbooks 1.1.0 as `BRIDGE_COMPAT + GEAR_LOOT_SUPPORT` with **0 independent semantic magic objects**. The artifact contains 11 provider classes; its own registry surfaces are one armor-material registry and one five-item equipment registry. Across every provider class, structural inspection finds 0 hits for `AbstractSpell`, `registerSpell`, `SpellRegistry`, `Ritual`, `Rite` or `Ability`; packaged provider data contains equipment tags/recipes rather than a spell/ritual/action registry.

Isolated NON-MERGE PR #203 audited exact HEAD `ed807b77345cde1803767d804e26ea972c41d964`; run `34688273425` was GREEN and published text-only artifact `10296406134` with digest `sha256:5e96a319aea648aadf2c70bdf9b870a26a9503068307befc8a9972bb7b1cd52e`. The ARR JAR itself was not redistributed. Phase 2BK therefore classifies the provider `ZERO_BRIDGE_INFRA`, contributes **+0**, and leaves the strict semantic minimum at **1250**. The provider component itself is now closed, moving the separate technical component metric to **58/100**.

## Phase 2BJ semantic promotion — Gaze 1.1.7.1 exact artifact

Exact hash-matched Gaze 1.1.7.1 evidence closes one current Gaze-owned Iron's standalone spell identity, **Soulward Shield**, whose optional `irons_spellbooks` provider gate is satisfied by the physical pack. The same exact artifact closes 26 player-facing Gaze Spirit Rite identities, but their registration is suppressed when the resolved COMMON config `disableGazeRites=true`; the deployed value is unavailable, so those 26 remain `CONDITIONAL`. Two Gaze `GeasEffectType` identities and eight rune items remain excluded by the existing metric definition.

Isolated NON-MERGE PR #201 audited exact HEAD `2f4ff6536663b1c629a6a5ea92416765bea17b1e`; final evidence run `34676660467` was GREEN and published artifact `10292013626` with digest `sha256:fb69f353b672f7c8ec7b470c454d24d1c3110cb996a250076a16d2b053f23f71`. Phase 2BJ therefore contributes **+1 `COUNTED_EXACT`**, moves the Iron's ecosystem subtotal to **542**, and moves the strict reconstructible minimum to **1250**. Gaze remains an open provider component, so component coverage stays **57/100**. Runtime/config/balance and provider-owned settlement remain separate fail-closed gates.

## Phase 2BH canonical — Goety 3.1.4

Exact hash-matched 3.1.4 evidence closes **123 active Focus actions + 238 available distinct non-Focus ritual actions = +361**. Durable PR #198 clean HEAD `d75f82a23b5c977ccc8ec84813bf89c928ffc0ab` passed Black Arcana CI **#2523** / run `34672038273`; squash merge `4fcc40aaf8149b5511dbd882a5616ee5240cd640` passed exact-SHA post-merge CI **#2524** / run `34672222798`, including canonical QA-JAR publication. Goety is therefore `COUNTED_EXACT` with **361**, the strict minimum is **1249**, and component **#57 / 57 of 100** is canonical. Runtime/API/balance QA remains separate.

## Phase 2BG canonical — Leyline Spellbooks 1.0.3

Exact hash-matched 1.0.3 artifact evidence closes **14 unconditional Leyline spell identities**. No Leylines-specific spell lock or conditional registration gate is present, and exact Iron's 3.16.3 school/default/scroll evidence corroborates ordinary host reachability; deployed generic host config remains separate runtime QA rather than a reason to reinterpret the exact registry. Leylines is therefore `COUNTED_EXACT` with **+14**.

Durable PR #195 clean HEAD `a9d7b55044230bbb011f7233ffd75d9a8321489b` passed Black Arcana CI **#2503** / run `34668329229`. It was squash-merged as `88f042f68429ff920314a7ec3a6923369edc93fd`; that exact merge SHA passed Black Arcana CI **#2504** / run `34668535721`, including unit tests, diff sanity, NeoForge build, built-JAR verification, Foundation GameTest, dedicated-server smoke and canonical QA-JAR publication. The canonical Iron-ecosystem subtotal is now **541** and the strict semantic minimum is **888** (`199 + 541 + 42 + 55 + 25 + 26`). The global denominator remains incomplete, so no semantic percentage is declared.

## Hazen N Stuff 1.4.0.14 source-pinned spell closure

The current sibling physical re-audit certifies `hazennstuff-1.4.0.14.jar` / mod id `hazennstuff` / runtime `1.4.0.14` / physical SHA-1 `3be20bacb44c1923348ab6f61b685eec6aacfdcd`. Exact release-correlated source `Hazentouvel/Hazen_N_Stuff@5fcaf39cf399609f6c1c87d14f8d4807098c9cce` declares the same version and its sole spell registry contains **38 active Iron's `AbstractSpell` registrations**.

The same exact localization exposes 41 root spell keys. `brimstone_hellblast` and `supernova` have no active registry entry; `reign_of_tyros` has a source class/localization root but its `registerSpell(...)` line is commented. Those three are excluded. Three of the 38 active spells inherit provider-specific inventory craft gates with source-pinned provider-owned acquisition paths; the remaining 35 use the host/default craftability path at the provider source level. Custom Cosmic/Radiance/Shadow/Hydro focus routing is catalog-reconciled against HazentouveLib/Ace's Spell Utils, while assembled-pack runtime and deployed host config remain fail-closed.

Hazen therefore contributes **+38 `COUNTED_SOURCE_PINNED`** semantic spell identities. Later `1.21.1` branch additions such as `coruscated_discharge` are not projected backward into the pinned 1.4.0.14 release.

## Create: Wizardry 1.21.1-0.5.1-pre1 source-pinned zero-semantic closure

Current sibling physical authority `neoforge-rpg-skilltree@4767f5c637c02c6d91ccb43a86ea1539f42a2e9b` certifies `create_wizardry-1.21.1-0.5.1-pre1.jar` at physical row #166. Official source pin `TTZPlayz/Create-Wizardry@9c4e53aad0ee9477187487443b597b77ef06f323` declares the same provider version.

The source pin has 75 Java files and 328 resource files, but no provider-owned spell resource namespace and no `registerSpell`, `SpellRegistry`, `DeferredRegister<AbstractSpell>`, `Registries.SPELL`, `SPELLS.register` or `spell.create_wizardry` identity surface. Blaze Caster reads host `SpellData`/`AbstractSpell` and invokes existing Iron's spell casts; Mana Siphon and the provider's two mob effects modify mana/casting conditions. These are automation/resource/policy surfaces, not new provider-owned spell identities.

Create: Wizardry is therefore `ZERO_SEMANTIC_HOST_SPELL_AUTOMATION` and contributes **+0 semantic magic objects**. The strict reconstructible minimum remains **1382** on this base. Source-build byte equality to the installed JAR and all assembled-pack automation/resource settlement remain runtime QA rather than semantic-count gates.

## Iron's Apothic 2.2.2 source-pinned zero-semantic closure

Current sibling authority `neoforge-rpg-skilltree@c3de5878d69a7a6b4441606ef2b9e96a61a8f2e9` certifies `irons_apothic-2.2.2.jar` at row #339. Exact official source `muon-rw/Apotheosis-Irons-Spells@c5d501219cc9bbbfb8c69acc08bebac76983d1c1` declares the same provider version.

The exact source registers seven custom Apotheosis affix codecs and contains 140 affix JSON definitions, including 48 explicit spell/imbued-spell trigger definitions, plus 24 gem definitions. Those resources consume Iron's `SpellRegistry`, `SchoolRegistry`, `AbstractSpell` and casting state; no independent provider-owned spell registrar is present. The 48 spell-oriented affixes therefore reference, trigger or modify spells owned by Iron's or its addons instead of minting 48 new spell identities.

Iron's Apothic is consequently a source-pinned magic bridge/support closure with **+0 independent semantic magic objects**. The strict reconstructible minimum remains **1382**. Installed-JAR byte equality and assembled-pack affix/cooldown/target/proc behavior remain runtime QA, not semantic-count evidence.

## Current 24/09/2026 reconciliation

Current sibling authority `neoforge-rpg-skilltree@76cf13e7d1110116f67c290eaa15891888279fc1` preserves the status-prefixed current provider lines used here; Traveloptics has no current certified physical row, while its uncategorized legacy export remains provenance only.

Current semantic deltas since the 1382 checkpoint:

- Acolyte 1.0.3: **+0** — no provider-owned spell registry; observed spell references remain Iron's-owned.
- Companions! 1.3.4: **+9 `COUNTED_SOURCE_PINNED`** provider-owned Magic Book actions with source-level survival routes.
- Crystal Chronicles 0.1.3-alpha: **+1 `COUNTED_SOURCE_PINNED`** — `crystal_chronicles:prismatic_portal`.
- Dungeon's Delight 1.5.1: **+0** — mob effects, enchantments, food/cooking and item systems are metric-excluded support surfaces.
- Fantasy Armor 1.2.4: **+0** — passive gear/MobEffect surface, no spell/ritual/active-action registry.
- Enchantment Descriptions 21.1.11: **+0** — client presentation only.
- A Good Place 1.2.5: **+0** — client placement-animation presentation only.
- Create: Apokinetics 1.0.6: **+0** — exact physical/publisher artifact equality plus bounded clean-room exact-binary scan closes zero spell/glyph/ritual surface; Machine Gems remain support/augmentation capabilities.
- Relics 0.12.8: **+41 `COUNTED_EXACT`** — exact physical/publisher artifact equality; 39 base ability roots + 2 distinct owner-scoped synergy roots; rank/mode variants are not extra identities.
- Cataclysm: Spellbooks 1.1.14: **+0 delta** — retains the already counted 59 identities; physical SHA-1 `568d798862a61a374ab1e55dcddf5b2e3326b8b5` equals audited publisher File 8847070 and the registry class is byte-identical to the exact 1.1.13 control, so current evidence is `COUNTED_EXACT`.
- Corail Tombstone 9.5.6: **+10 `COUNTED_RELEASE_BOUNDED`** — six prayer identities + four Ritual Flute actions are release-exact/reachability-bounded; provider remains **⚠️ partial/conditioned** because additional config-sensitive castable magic-item actions are still unresolved.
- Ender's Spells and Stuff: Requiem 0.1.7: **+53 `COUNTED_SOURCE_PINNED`** — exact release-correlated source closes 58 current registered roots under the present provider set; five implementation/residual roots are excluded, leaving 53 provider-owned player-facing semantic actions.
- Somake 1.0.9 remains **CONDITIONAL / +0 strict**; physical SHA-1 equality to exact publisher File `8867079`, the exact 83-ID registry, the 67-unconditional + 16-optional registration-gate map, current-composition admission of **83/83**, and 83 individual current cards are closed. Only effective deployed Iron's/provider config and survival reachability remain semantic-count blockers.

Therefore the strict reconstructible minimum becomes **1496**. This remains a minimum, not a final denominator or percentage.

## Strict reconstructible counted minimum

**1496 semantic magic objects are currently reconstructible from canonical provider records after Companions (+9), Crystal Chronicles (+1), Relics (+41), Corail Tombstone (+10) and Ender's Spells and Stuff: Requiem (+53) promotions.**

This is a counted minimum, not the final denominator and not a coverage percentage. Providers with `LOWER_BOUND`, `CONDITIONAL` or `OPEN` state remain outside this sum until their current inventory/eligibility is reconciled.

Arithmetic cross-check by provider family:

- Ars ecosystem: **199**;
- Iron's ecosystem and spell-content addons: **662**;
- Companions provider-owned Magic Books: **9**;
- Relics provider-owned ability/synergy layer: **41**;
- Corail Tombstone counted prayer/Ritual-Flute layer: **10**;
- Eidolon: Repraised: **42**;
- Vampirism/Bloodlines/Werewolves supernatural action layer: **55**;
- Hexalia ritual/infusion layer: **25**;
- Malum Spirit Rite layer: **26**;
- Goety base Focus + ritual layer: **361**;
- Goety Iron Focus + ritual layer: **14**;
- Goety Cataclysm Focus + ritual layer: **52**;
- total: `199 + 662 + 9 + 41 + 10 + 42 + 55 + 25 + 26 + 361 + 14 + 52 = 1496`.

### Counted ledger

| Provider | Installed/current line | Count | State | Semantic basis |
|---|---|---:|---|---|
| [Ars Nouveau](../providers/ars-nouveau/README.md) | 5.13.1 | 109 | `COUNTED_SOURCE_PINNED` | 5 Forms + 13 Augments + 67 Effects + 24 rituals; arbitrary composed chains excluded |
| [Ars Additions](../providers/ars-additions/README.md) | 21.3.0 | 5 | `COUNTED_SOURCE_PINNED` | 3 glyphs + 2 rituals |
| [Ars Controle](../providers/ars-controle/README.md) | 1.6.16 | 9 | `COUNTED_SOURCE_PINNED` | 1 effect + 8 filters/spell parts; 1.6.15→1.6.16 registry source is blob-identical |
| [Ars Technica](../providers/ars-technica/README.md) | 2.7.6 | 11 | `COUNTED_SOURCE_PINNED` | 11/11 registered spell parts |
| [Ars Hex](../providers/ars-hex/README.md) | 5.0.4b | 1 | `COUNTED_SOURCE_PINNED` | one current Malum-backed registered glyph under the physical provider set |
| [Ars Zero](../providers/ars-zero/README.md) | 2.0.2 | 12 | `COUNTED_RELEASE_BOUNDED` | 12 current unique glyph capabilities; disabled copied AOE/Amplifier variants excluded |
| [Ars Elemental](../providers/ars-elemental/README.md) | 0.7.10.1 | 47 | `COUNTED_SOURCE_PINNED` | 39 production spell parts + 8 rituals |
| [Ars 'n' Spells](../providers/ars-n-spells/README.md) | 3.3.2 | 5 | `COUNTED_SOURCE_PINNED` | 5 ritual identities; eight `ars_cross_*` proxy slots contribute zero |
| [Iron's Spells 'n Spellbooks](../providers/irons-spells/README.md) | 3.16.3 | 110 | `COUNTED_EXACT` | 110/110 active spell registry entries; deprecated Cloud of Regeneration excluded |
| [Apprentice's Codex](../providers/apprentice-codex/README.md) | 0.9.7.1 | 83 | `COUNTED_SOURCE_PINNED` | exact 83-spell registry inventory |
| [Asterism Arcanum](../providers/⚠️-asterism-arcanum/README.md) | 1.21.1-0.1.0 | 10 | `COUNTED_EXACT` | physical SHA-1 equals exact publisher File 8157080; exact binary registrar references all 11 expected spell classes, while publisher lists 10 normal survival spells and `astral_gateway` remains separately conditional/creative-only |
| [Backported Spellbooks](../providers/backported-spellbooks/README.md) | physical 0.1.2 / embedded 0.1.0 | 6 | `COUNTED_RELEASE_BOUNDED` | release-day official source ceiling registers six standalone Iron's spells |
| [Deeper & Darker Spellbooks](../providers/deeper-and-darker-spellbooks/README.md) | 1.3.3 Version B | 4 | `COUNTED_RELEASE_BOUNDED` | 4 current provider spell identities |
| [Discerning The Eldritch](../providers/discerning-the-eldritch/README.md) | 1.4.4 | 22 | `COUNTED_SOURCE_PINNED` | 22/22 registered spells, including its ritual-school spell registrations once |
| [Dreamless Spells](../providers/dreamless-spells/README.md) | 1.1.9 | 4 | `COUNTED_SOURCE_PINNED` | 4 current registered spells |
| [GTBC's Geomancy Plus](../providers/gtbcs-geomancy-plus/README.md) | 1.1.0-1.21.1 | 12 | `COUNTED_RELEASE_BOUNDED` | exact publisher file `7041615` closes 12 unconditional provider-owned registrations (10 Geo + 2 Holy); Geo host-gate inheritance + focus/Scroll Forge route and Holy Umvuthi acquisition close catalog reachability; independent local physical-JAR hash is unavailable; assembled-host runtime QA remains separate |
| [Farmer's Spell 'n Spellbooks](../providers/farmers-spell/README.md) | 1.0.5.1-1.21.1 | 6 | `COUNTED_SOURCE_PINNED` | exact 1.0.5.1 source pin closes six unconditional Gluttony spell registrations; provider/host-native Scroll Forge focus route closes catalog reachability while current-host runtime QA remains separate |
| [SnackPirate's Aeromancy Additions](../providers/aeromancy-additions/README.md) | 1.2.8 | 10 | `COUNTED_SOURCE_PINNED` | exact 1.2.8 source pin closes ten active unconditional Wind spell registrations; five commented registrations are excluded; Breeze Rod Wind focus + Iron's Scroll Forge contract close catalog reachability while current-host runtime QA remains separate |
| [Hazen N Stuff](../providers/✅-hazen-n-stuff/README.md) | 1.4.0.14 | 38 | `COUNTED_SOURCE_PINNED` | exact release-correlated source pin closes 38 active spell registrations; `brimstone_hellblast` and `supernova` are unregistered localization roots and `reign_of_tyros` has a commented registration; special craft gates/focus routes are catalog-reconciled while assembled-host runtime QA remains separate |
| [Ender's Spells and Stuff: Requiem](../providers/✅-enders-spells-and-stuff-requiem/README.md) | 0.1.7 | 53 | `COUNTED_SOURCE_PINNED` | exact 0.1.7 release-correlated source closes 58 current registered roots with DTE present; five implementation/residual roots are excluded, leaving 53 provider-owned player-facing semantic actions |
| [Fire's Ender Expansion](../providers/fires-ender-expansion/README.md) | 2.4.1 | 11 | `COUNTED_SOURCE_PINNED` | 11/11 active spells |
| [IronSable](../providers/ironsable/README.md) | 1.2.0 | 7 | `COUNTED_RELEASE_BOUNDED` | 7 provider-owned new spells; 10 physicalized existing Iron's spells add zero identities |
| [ISS: Magic From The East](../providers/iss-magic-from-the-east/README.md) | 1.1.5 | 22 | `COUNTED_SOURCE_PINNED` | 11 Symmetry + 11 Spirit spells |
| [Legendary Spellbooks](../providers/legendary-spellbooks/README.md) | 0.3.2 | 30 | `COUNTED_SOURCE_PINNED` | 30 current provider spell identities |
| [Monsters & Spellbooks](../providers/monsters-spellbooks/README.md) | 0.0.16.3 | 98 | `COUNTED_RELEASE_BOUNDED` | release-interval evidence closes a stable 98-spell semantic inventory |
| [Paladin Spells](../providers/paladin-spells/README.md) | 1.1.1 | 5 | `COUNTED_SOURCE_PINNED` | 5/5 Holy spells |
| [Wind's Spellbooks](../providers/winds-spellbooks/README.md) | 1.0.5 | 7 | `COUNTED_RELEASE_BOUNDED` | 7/7 publisher/runtime-observed Wind spells |
| [Ypsilon's Fundamentalism](../providers/ypsilons-fundamentalism/README.md) | 1.1.7.1 | 15 | `COUNTED_SOURCE_PINNED` | 15/15 active spell registrations; commented prototypes excluded |
| [Tunes n' Tomes](../providers/tunes-n-tomes/README.md) | 1.1.0-HOTFIX | 16 | `COUNTED_RELEASE_BOUNDED` | current publisher Melodic roster enumerates 16 spells; migrated Sound ownership is not duplicated under Alshanex/FamiliarsLib |
| [Alshanex's Familiars](../providers/alshanex-familiars/README.md) | 4.0.3 | 18 | `COUNTED_EXACT` | exact hash-matched JAR closes 7 provider-owned spell registrations + 11 packaged `alshanex_familiars:ritual_recipe` identities; migrated Sound/Tunes content and external familiar casts are excluded |
| [Companions!](../providers/✅-companions/README.md) | 1.3.4 | 9 | `COUNTED_SOURCE_PINNED` | nine direct/unconditional Magic Book action identities; source-level survival routes closed; Soul Mage reuse deduplicated |
| [Crystal Chronicles](../providers/✅-crystal-chronicles/README.md) | 0.1.3-alpha | 1 | `COUNTED_SOURCE_PINNED` | exactly one provider-owned Iron's spell registration, `crystal_chronicles:prismatic_portal`; physical SHA is known but source-build byte equivalence is not claimed |
| [Cataclysm: Spellbooks](../providers/cataclysm-spellbooks/README.md) | 1.1.14 | 59 | `COUNTED_EXACT` | physical SHA-1 equals audited publisher File 8847070; 1.1.14 registry class is byte-identical to the exact 1.1.13 control, preserving 59 registered identities; 10 residual root localization keys remain excluded |
| [Leyline Spellbooks](../providers/leyline-spellbooks/README.md) | 1.0.3 | 14 | `COUNTED_EXACT` | exact hash-matched JAR closes 14 unconditional `AbstractSpell` registrations; no provider-specific spell lock/conditional registration gate is present; generic Iron's host config remains separate runtime QA |
| [Gaze](../providers/gaze/README.md) | 1.1.7.1 | 1 | `COUNTED_EXACT` | exact hash-matched artifact closes one Gaze-owned Iron's `AbstractSpell`, Soulward Shield; physical Iron's satisfies the provider gate; 26 Spirit Rites remain config-conditional and 2 Geas + 8 rune items are metric-excluded |
| [Relics](../providers/✅-relics/README.md) | 0.12.8 | 41 | `COUNTED_EXACT` | exact physical/publisher artifact equality closes 39 owner-scoped base abilities + 2 distinct owner-scoped synergies; modes/rank modifiers and relic items add zero extra identities; runtime/config QA remains separate |
| [Corail Tombstone](../providers/⚠️-corail-tombstone/README.md) | 9.5.6 | 10 | `COUNTED_RELEASE_BOUNDED` | exact publisher artifact closes 6 prayer + 4 Ritual Flute action identities; publisher `Silent Bound` wording is provenance-only while exact artifact identity is `Silent Bond`; additional config-sensitive castable magic-item actions remain conditional |
| [Goety](../providers/goety/README.md) | 3.1.4 | 361 | `COUNTED_EXACT` | exact hash-matched JAR closes 123 active/acquirable Focus actions + 238 available distinct non-Focus ritual actions after semantic deduplication and physical-provider condition filtering; runtime/API/balance QA remains separate |
| [Goety Iron](../providers/goety-iron/README.md) | 3.1 | 14 | `COUNTED_EXACT` | exact hash-matched JAR closes 2 unconditional addon-owned Focus identities + 12 distinct non-Focus rituals; 2 Focus-acquisition rituals deduplicated; no base-Goety semantic duplicates |
| [Goety Cataclysm](../providers/goety-cataclysm/README.md) | 1.21.1-1.8.2 | 52 | `COUNTED_EXACT` | exact hash-matched JAR closes 28 unconditional addon-owned Focus identities + 24 distinct non-Focus rituals; 24 Focus-acquisition rituals deduplicated; no base-Goety semantic duplicates |
| [Eidolon: Repraised](../providers/eidolon-repraised/README.md) | 0.5.0.2 | 42 | `COUNTED_SOURCE_PINNED` | 18 normal/player-facing chants + 24 official ritual recipes; `undead_lure` empty cast and `basic_incense` dummy excluded; chant conversions are not extra spells |
| [Vampirism](../providers/vampirism/README.md) | 1.10.13 | 19 | `COUNTED_SOURCE_PINNED` | 14 Vampire + 3 Hunter + 2 shared Lord registered player actions; counted as provider-native discrete supernatural actions, not Iron's spells |
| [Bloodlines](../providers/bloodlines/README.md) | 3.0.9 | 28 | `COUNTED_SOURCE_PINNED` | 29 action registrations minus Sorcerous Strike; exact source registers its action/skill/node/config but omits the node from the configured Gravebound tree and from all rank-default grants, so it is not normally survival-reachable in this build |
| [Werewolves](../providers/werewolves/README.md) | 2.0.3.3 | 8 | `COUNTED_SOURCE_PINNED` | 3 player form actions + Howling + Rage + Sense + Fear + Leap; exact source proves Leap's survival-tree node and dedicated server input path; Hide Name remains presentation-only |
| [Hexalia](../providers/hexalia/README.md) | physical filename 1.3.6 / runtime metadata 1.3.5 | 25 | `COUNTED_RELEASE_BOUNDED` | 19 player-facing Nature's Ritual identities + 6 Celestial Infusion identities; mutation, Mortar & Pestle, Small Cauldron/brews, Censer, idols and equipment remain excluded by metric scope |
| [Malum](../providers/malum/README.md) | 1.8.2 | 26 | `COUNTED_RELEASE_BOUNDED` | release-bounded registry evidence closes 26 base `SpiritRiteType` identities; exact release-bounded `TotemMagicEntries` separately places both special Arcane rites in `ArcanaProgressionScreen` with `SpiritRiteRecipePage`, proving they are player-facing rites rather than proxy slots; 37 Geas effect types and 9 spirit resource/type identities remain excluded |
| **Strict total** |  | **1496** |  |  |

### Bloodlines 3.0.9 Sorcerous Strike reachability closure

Exact installed-line source at `TheDrOfDoctoring/bloodlines@c8fd517d204d09dfcb9a544c17d7df87755eaa5c` registers Sorcerous Strike as `gravebound_crit_action`, registers the corresponding `BloodlineActionSkill`, creates a `gravebound_sorcerous_strike` skill node, and exposes its balance config. Those facts establish that the implementation exists; they do not establish normal player acquisition.

The same exact source closes the missing reachability question: the generated configured Gravebound tree does not include `gravebound_sorcerous_strike`, and `HunterBloodlinesConfig.graveboundDefaults` grants only the four Gravebound rank nodes by default. Repository-wide inspection finds no provider-native alternate grant dedicated to Sorcerous Strike; generic Bloodline task/command surfaces add perk points rather than directly granting this skill. `SkillHandlerMixin` only adds Bloodlines-specific cost/rank/default checks around Vampirism skill enabling and does not create a second acquisition path.

Therefore Sorcerous Strike is classified `EXCLUDED` for the current semantic denominator as a registered/generated but not normally survival-reachable action in the exact 3.0.9 provider build. This statement does not claim that an operator command or externally modified datapack could never force-enable it; those are outside normal current-provider survival reachability. Bloodlines remains **28 counted actions**; after Phase 2BL, the global strict total was **1316**.

### Werewolves 2.0.3.3 Leap correction

The previous ledger left `werewolves:leap` conditional because the action is hidden from the generic selector and its enabling path had not yet been reconstructed. Exact source at `TeamLapen/Werewolves@b72635b3e014e406b25bb79adb9d340f7443660b` closes that path: `ModSkills.LEAP` is an `ActionSkill` bound to `ModActions.LEAP`; node `SURVIVAL31` grants that skill; `SkillTreeProvider` connects `SURVIVAL31` into the normal `werewolf_level` tree; and the server handles the dedicated Leap input by delegating to the provider-owned action handler. Therefore hidden-selector presentation does not make Leap unreachable. The separate `no_leap_cooldown` refinement remains reachability-unproven and is not a separate semantic action. See [`SEMANTIC-MAGIC-DELTA-WEREWOLVES-LEAP.md`](./SEMANTIC-MAGIC-DELTA-WEREWOLVES-LEAP.md).

### Alshanex's Familiars 4.0.3 exact-artifact closure

Phase 2BD materialized CurseForge File ID `8675568` through Curse Maven in an isolated audit and required SHA-1 `e5051c2385a426d05bf203ba8081a23d891f6686` to match the physical modlist before inspection. The exact JAR closes seven unconditional provider-owned `AbstractSpell` registrations and eleven packaged JSON resources of custom type `alshanex_familiars:ritual_recipe`. These are discrete spell/ritual identities under this ledger, for **+18**.

The seven spells are `summon_shadows`, `ice_age`, `ice_chamber`, `megido`, `fire_fist`, `end_mayhem` and `switcheroo`. The eleven rituals are the five familiar-shard rituals (`archmage`, `druid`, `frostling`, `hunter`, `lightning_mage`), `summoner_shard`, four magic power/resistance tier rituals and `truth_mirror`. Exact numerical mechanics and runtime QA remain separate gates.

The 4.0 ownership migration remains controlling: Sound/Melodic content belongs to Tunes n' Tomes and is not counted again under Alshanex. Familiar AI/passives and casts of externally owned Iron's spells also add zero identities. Clean-room inspection retained only factual IDs/counts/signatures and structured resource facts; no upstream implementation/assets were copied or adapted. See [`../providers/alshanex-familiars/EXACT-4.0.3-ARTIFACT-AUDIT.md`](../providers/alshanex-familiars/EXACT-4.0.3-ARTIFACT-AUDIT.md).

### Cataclysm: Spellbooks 1.1.13 exact-artifact closure

Phase 2BE materialized CurseForge File ID `8792628` through Curse Maven in isolated non-merge PR #188 and required SHA-1 `4af8348cc77bbff2ab7057c1fac26a5ab0a5b6a2` to match the physical modlist before factual inspection. The exact `SpellRegistries` static initializer closes **59** `registerSpell(...)` calls, **59** provider spell-class instantiations, **59** spell-field assignments and **0** conditional branches. Field/class/root-ID reconciliation closes **59 unique current spell identities**, for **+59**.

The exact implementation-package distribution is 7 Abyssal, 4 Ender, 1 Evocation, 5 Holy, 11 Fire, 5 Ice, 4 Nature and 22 Technomancy. The exact English localization has 69 root spell keys, but ten are not registered current spell IDs/classes and are excluded as translation-only/WIP-or-residual evidence: `conjure_abyssal_gnawer`, `conjure_clawdian`, `conjure_coral_golem`, `conjure_coralssus`, `cryopiercer`, `final_rend`, `hemorrhaging_impact`, `parting_shot`, `quick_strike`, `scorched_earth`.

The generic/current publisher project page advertises 65 spells, but that project-scale claim is not substituted for the physically installed 1.1.13 registry; a newer 1.1.14 beta also exists after the installed file. Exact numerical mechanics, acquisition and runtime/API integration remain separate gates. See [`../providers/cataclysm-spellbooks/EXACT-1.1.13-ARTIFACT-AUDIT.md`](../providers/cataclysm-spellbooks/EXACT-1.1.13-ARTIFACT-AUDIT.md) and [`../providers/cataclysm-spellbooks/EXACT-1.1.13-SPELL-INVENTORY.md`](../providers/cataclysm-spellbooks/EXACT-1.1.13-SPELL-INVENTORY.md).

### Hexalia release-boundary reconciliation

Hexalia remains an explicit physical/source identity mismatch: the installed file is `hexalia-neoforge-1.3.6.jar`, while its runtime metadata reports `1.3.5`. That prevents an exact installed-JAR/source-equivalence claim, but it no longer blocks this narrow semantic count.

The official source commit `ef34896fc1a2a02da46b49a46ca78ca236bdc2dc` (`Update 1.3.5`) declares `mod_version=1.3.5`; its immediate release successor `4952c65233bf31e9f0d3e55ff76be7fa1007ee3d` (`Release Hexalia 1.3.6`) declares `mod_version=1.3.6`. Comparing those checkpoints shows no Nature's Ritual or Celestial Infusion recipe JSON added, removed or modified. The official 1.3.5 publisher changelog also records restoration of the Galeberries Celestial Infusion recipe, so the six-infusion inventory is already present on the 1.3.5 release line.

Therefore the intersection relevant to this metric is stable across the observed `1.3.5` metadata / `1.3.6` filename-source boundary: **19 player-facing Nature's Rituals + 6 Celestial Infusions = 25**. The debug Nature's Ritual is excluded. Exact installed-binary equivalence, runtime mechanics and provider API/hook QA remain open independently.

### Malum 1.8.2 release-boundary reconciliation

The physical instance identifies `malum-1.21.1-1.8.2.jar` / runtime `1.8.2`. The official `SammySemicolon/Malum-Mod` `1.21.1` history bounds the matching version line between `f56691e56e591a6d8d1859ff119e749375e14d61`, whose parent still declares `1.8.1`, and `03b743a37f3eeb0cc7f4364f0730e1f135f78408`, whose child advances to `1.8.3`.

Endpoint blob equality is not used alone. Path-history queries over the complete observed 1.8.2 window show:

- `MalumSpiritRiteTypes.java` — no commit touches the path after entry into the window and before the 1.8.3 transition;
- `MalumSpiritRiteEffectTypes.java` — no commit touches the path in that interval; supporting deduplication evidence only;
- `MalumSpiritTypes.java` — no commit touches the path in that interval;
- `MalumGeasEffectTypes.java` — the path is touched at the initial `f56691e...` checkpoint and has no later commit before the transition;
- `client/screen/codex/entries/TotemMagicEntries.java` — no commit touches the path in that interval.

The stable endpoint blobs are:

- `MalumSpiritRiteTypes.java` → `2b9e4e5445733dee4ed205e4331d55c93ac86028`, with **26 active base-Malum rite registrations**;
- `MalumSpiritRiteEffectTypes.java` → `e5fd8854c12783e4503475ccaf461c3a19c2a0b0`, used only to distinguish the two special rite/effect identities and adding **0** semantic objects;
- `MalumGeasEffectTypes.java` → `2aef164fcedae891b2c6805f2edbd8ee48cffbfe`, with **37 active Geas effect-type registrations**; two proposed Bonds and one Authority are commented out;
- `MalumSpiritTypes.java` → `fa772479f0f73131dabf33d9342299c7e20405e1`, with **9 spirit resource/type registrations**;
- `TotemMagicEntries.java` → `d0ba29e52abcd1f26cfa92f20951c4981ae3c661` at both endpoints.

The semantic eligibility of `undirected_rite` and `unchained_rite` is not inferred from registry membership. Exact `TotemMagicEntries.setupEntries(ArcanaProgressionScreen)` adds both as separate progression entries, each with its corresponding `RiteHolder` represented by a `SpiritRiteTextPage` and a `SpiritRiteRecipePage`; Unchained additionally exposes transmutation content. Because the progression file is unchanged throughout the observed `1.8.2` interval, this player-facing surface is release-bounded rather than a single-checkpoint observation.

`CodexLangDatagen.java` is touched at exactly five checkpoints during the same interval — `f56691e...`, `3fb3c77...`, `a634061...`, `5a578eb...` and `fbcc606...`. Every snapshot preserves dedicated entries for the two special rites, and the Undirected entry preserves activation guidance using five runes. This is supporting player-facing/reachability evidence; upstream prose is not copied into Black Arcana.

Therefore all **26 `SpiritRiteType` identities** satisfy the counted ritual/rite class for this ledger, including the two special Arcane rites. The Geas registry is an effect/progression registry, the Spirit Type registry is a resource/type registry, and Rite-effect entries are effects; all are explicitly outside the counted semantic-action classes. Gaze-provided rites are not included in the base Malum 26.

This is `COUNTED_RELEASE_BOUNDED`, not an exact installed-JAR/source-equivalence claim. Exact recipe contents, numerical mechanics, runtime lifecycle and provider API contracts remain open. The upstream licensing inconsistency documented in the Malum provider catalog continues to block promotion of source implementation internals into Black Arcana integration contracts.

## Conditional objects excluded from the strict total

| Provider | Quantity | State | Reason |
|---|---:|---|---|
| Asterism Arcanum | 1 | `CONDITIONAL` | `astral_gateway` is registered but documented creative-only/unfinished |
| Not Enough Glyphs 4.6.2 | 39 | `CONDITIONAL / CURRENT SOURCE MATRIX RECLOSED / CONFIG AUTHORITY CLOSED / +0` | current 4.6.2 source pin preserves the exact registration and Momentum blobs from 4.6.1, so the current-pack source result remains 40 registrations with `momentum` source-disabled and 39 candidates. Ars Nouveau 5.13.1 registers each spell part as a `SERVER` config at `<namespace>/<path>.toml`; inherited `[general].enabled` defaults true, but the deployed server/world override set is unavailable, so source defaults are not promoted to active-pack facts |

The four real Ars Elemental primitives referenced by Not Enough Glyphs are not NEG-owned registrations and are already counted under Ars Elemental. Historical fallback namespaces do not create a second owner when the real provider is present.

## Explicit zero / non-duplicating providers

The following audited providers add **0** independent semantic objects under this metric:

- [Ars Creo](../providers/ars-creo/README.md) — Create/Ars bridge, no own glyph registry;
- [Ars Elemancy](../providers/ars-elemancy/README.md) — equipment specialization, empty glyph registration;
- [Ars Polymorphia](../providers/ars-polymorphia/README.md) — Phase 2BM source-pinned recipe-conflict bridge; `ZERO_SEMANTIC_BRIDGE`, +0; current-host runtime compatibility remains fail-closed;
- [Ars Sable](../providers/ars-sable/README.md) — Phase 2BN source-pinned spatial/sublevel compatibility bridge; `ZERO_SEMANTIC_BRIDGE`, +0; current-host Sable/Ars mixin compatibility remains fail-closed;
- [FamiliarsLib](../providers/familiarslib/README.md) — familiar framework; historical Sound content removed from the 1.7 line;
- [GTBC's SpellLib](../providers/gtbcs-spelllib/README.md) — shared spell/addon library infrastructure; publisher surface establishes no standalone gameplay/spell catalog in 2.2.0;
- [Soul Fire'd](../providers/soul-fire-d/README.md) — fire/enchantment content, 0 spells/glyphs/rituals;
- [Vampire Spells Addon](../providers/vampire-spells-addon/README.md) — Phase 2BT exact-release source-pinned `ZERO_BRIDGE_INFRA`; +0; modifies Iron's/Vampirism behavior without minting a provider-owned spell/action identity; runtime bridge QA remains fail-closed;
- [Create: Wizardry](../providers/✅-create-wizardry/README.md) — current physical 1.21.1-0.5.1-pre1 source-pinned `ZERO_SEMANTIC_HOST_SPELL_AUTOMATION`; +0; Blaze Caster/Mana Siphon automate or constrain Iron's-owned spell/mana behavior without minting provider-owned spell identities; runtime settlement remains fail-closed;
- [Toxony](../providers/toxony/README.md) — harmful effects, oils, mutagens and alchemy state are provider content but are not spells/rituals/discrete action-registry identities under the current metric;
- [Mobstein](../providers/✅-mobstein/README.md) — exact 5.4.4 physical SHA-1 plus hash-matched resource-only clean-room audit closes the residual boundary as `ZERO_SEMANTIC_ACTIONS`: documented syringes are item interactions and surfaced action-like keybinds are entity/mount controls; **+0** independent semantic magic objects; runtime/API integration remains separately fail-closed;
- [Acolyte](../providers/✅-acolyte/README.md) — exact 1.0.3 release-bounded structural audit finds no provider-owned spell identity; Iron's host spells remain externally owned; **+0**.
- [Dungeon's Delight](../providers/✅-dungeons-delight/README.md) — 1.5.1 source-pinned effects/enchantments/food mechanics with no spell/ritual/action registry; **+0**.
- [Fantasy Armor](../providers/✅-fantasy-armor/README.md) — 1.2.4 source-pinned passive gear/effect magic; **+0**.
- [Enchantment Descriptions](../providers/✅-enchantment-descriptions/README.md) — 21.1.11 client tooltip/localization presentation; **+0**.
- [A Good Place](../providers/✅-a-good-place/README.md) — 1.2.5 client placement-animation presentation; **+0**.
- [Create: Apokinetics](../providers/✅-apokinetics/README.md) — exact hash-matched 1.0.6 machine-augmentation/support closure; bounded binary audit observes no spell/glyph/ritual semantic registry/resource/API surface; **+0**.
- Bloodlines `gravebound_crit_action` / Sorcerous Strike — registered implementation, but exact 3.0.9 configured tree and rank defaults provide no normal survival acquisition path;
- IronSable's ten physicalized base Iron's spells — already owned/countable under Iron's;
- Ars 'n' Spells `ars_cross_*` proxy registry pool — proxies, not eight semantic rituals/spells;
- Ars Zero copied disabled AOE/Amplifier compatibility variants — not unique active glyph capabilities;
- Werewolves `hide_name` — client presentation identity, not a gameplay magic object.

## Lower bounds and open denominator blockers

These rows are deliberately **not additive to 1496** until their exact/current inventory and deduplication state meet the inclusion rule.

| Provider | Current evidence | State | Why excluded from strict sum |
|---|---|---|---|
| [Somake Spells](../providers/⚠️-somake-spells/README.md) 1.0.9 | exact physical SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0` equals publisher File `8867079`; exact physical registry closes **83 unique spell IDs**; exact gate topology is **67 unconditional + 16 optional-provider-gated**; Mowzie's Mobs, ISS and Legendary Monsters are present, so the current composition admits **83/83** registrations; all 83 current identities are materialized under `MAGIC-CARDS-1.0.9.md` / `registry-1.0.9/`; provider code default for `enableSpellLockSystem` is `false` | `CONDITIONAL / EXACT PHYSICAL REGISTRY CLOSED / CURRENT COMPOSITION 83/83 / +0` | effective deployed Iron's `enabled` / `allow_crafting`, deployed Somake `enableSpellLockSystem`, and object-level or bounded-set survival acquisition/reachability remain open; source/default values are not substituted for deployed state |
| [Gaze](../providers/gaze/README.md) 1.1.7.1 rites | exact hash-matched artifact closes **26 player-facing Spirit Rite identities** | `CONDITIONAL / EXACT REGISTRY CLOSED / +0 RITES` | exact provider control flow suppresses the rite surfaces when resolved COMMON config `disableGazeRites=true`; deployed pack value is unavailable, so source default `false` is not substituted |

Other provider directories that have not yet been normalized into a semantic-object row also remain outside the denominator. Absence from the strict table is never interpreted as zero without an explicit zero disposition.

## Important interpretation rules

1. **1496 is not “1496 / unknown”.** It is a reconstructible counted minimum while the denominator remains open.
2. Do not divide 1496 by the historical 100-provider-component denominator. The former `68/100` checkpoint predates the 22/09 physical re-audit and is now `PENDING REBASE`; provider-component coverage and semantic-magic coverage answer different questions.
3. Do not add public lower bounds to 1496 and call the result complete. Lower-bound providers can contain unenumerated objects, aliases, removed entries or cross-provider proxies that require object-level reconciliation.
4. A registered technical slot can still be excluded when the provider itself proves it is dummy, presentation-only, disabled, proxy-only or unreachable in the current survival path.
5. Runtime/config QA remains distinct from semantic inventory closure. A source-pinned or release-bounded object may be countable while numerical settlement or compatibility remains fail-closed.
6. Semantic similarity does not transfer authority. Two different provider spells may overlap mechanically and still remain distinct provider-owned objects; deduplication prevents double ownership/processing, not factual erasure of existing content.
7. Black Arcana's own proposed/implemented spells do not backfill missing provider evidence and do not reduce the provider denominator by assumption.

## Next closure order

To converge on a final denominator efficiently, prioritize:

1. another still-open provider/component for which current/exact evidence can materially reduce inventory or classification uncertainty;
2. obtain deployed config evidence for input-blocked conditional rows, especially Not Enough Glyphs 4.6.2 and Gaze 1.1.7.1 Rites when such evidence becomes available;
3. obtain deployed host/provider config evidence and close Somake 1.0.9 survival reachability; physical↔publisher equality, exact 83-ID registry, exact 67+16 registration-gate mapping, current-composition 83/83 admission and current 83-card materialization are already closed and must not be re-audited as open.

Phase 3 remains blocked until the semantic denominator is reconstructible and provider/capability deduplication proves real Black Arcana gaps.
