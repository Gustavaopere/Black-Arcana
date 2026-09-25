# Current Magic Catalog Coverage

## User-facing semantic magic coverage

The principal percentage reported to the user is the coverage of **semantic magic objects**: spells, glyphs/spell-parts, rituals/rites and equivalent discrete magical actions. Provider count, JAR count, technical proxies, items, gear, familiars, affixes and machines do not substitute for that denominator.

The reconstructible semantic ledger lives in [`SEMANTIC-MAGIC-COVERAGE.md`](./SEMANTIC-MAGIC-COVERAGE.md). Phase 2BL raises the **strict counted minimum to 1316 semantic magic objects** by closing exact Goety Iron 3.1 (+14) and Goety Cataclysm 1.21.1-1.8.2 (+52) inventories without duplicating base-Goety ownership. Phase 2BM then closes Ars Polymorphia 1.0.3 as a source-pinned zero-semantic bridge with **+0**, Phase 2BN closes Ars Sable 1.1.2 as a source-pinned zero-semantic spatial/compat bridge with **+0**, Phase 2BO closes Farmer's Spell 'n Spellbooks 1.0.5.1 with **+6 `COUNTED_SOURCE_PINNED`**, and Phase 2BP closes SnackPirate's Aeromancy Additions 1.2.8 with **+10 `COUNTED_SOURCE_PINNED`**; Phase 2BQ then closes Ars Nouveau: Two-Way Portals 2.0.0 as exact hash-matched `ZERO_SEMANTIC_PORTAL_INFRA` with **+0**; Phase 2BR closes GTBC's Geomancy Plus 1.1.0-1.21.1 at **+12 `COUNTED_RELEASE_BOUNDED`** from the exact publisher-release registry plus provider/host reachability evidence; Phase 2BT closes Vampire Spells Addon 0.0.9 as source-pinned `ZERO_BRIDGE_INFRA` with **+0**. At the Phase 2BT checkpoint the strict minimum remained **1344**. The global denominator is still incomplete and no semantic percentage is declared.

## Current reconciliation — 24/09/2026

Current sibling authority `neoforge-rpg-skilltree@e3689bbc04ba54be1612a13c242496330e99df06` preserves 587 top-level entries. The current category layout contains **45 physical rows whose category path contains `Magic`**; all map to catalog provider directories after ownership-name normalization: **40 ✅ cataloged / 5 ⚠️ partial-conditioned**. Gaze remains a global ⚠️ magic provider but is currently categorized under `Addons/`, so it is outside this physical-category subtotal.

Semantic effect of the current reconciliation:

- Acolyte 1.0.3: **+0** — consumes Iron's-owned spell identities.
- Companions! 1.3.4: **+9 `COUNTED_SOURCE_PINNED`** Magic Book actions.
- Crystal Chronicles 0.1.3-alpha: **+1 `COUNTED_SOURCE_PINNED`** (`crystal_chronicles:prismatic_portal`).
- Dungeon's Delight 1.5.1, Fantasy Armor 1.2.4, Enchantment Descriptions 21.1.11 and A Good Place 1.2.5: **+0** each after explicit zero-semantic classification.
- Create: Apokinetics 1.0.6: **+0** — exact physical SHA equals audited publisher File 8790422; exact-binary bounded scan closes zero spell/glyph/ritual surface while runtime/economy QA remains fail-closed.
- Cataclysm: Spellbooks 1.1.14: retains **59** already-counted spell identities; physical SHA-1 equals audited publisher File 8847070, strengthening evidence to `COUNTED_EXACT` with **+0 current delta**.
- Corail Tombstone 9.5.6 and Relics 0.12.8: provider magic confirmed but exact final discrete-action cardinality remains pending.
- Somake 1.0.9 remains conditional and contributes **+0 strict** until its current exact registry/reachability gates close.

The strict reconstructible semantic minimum is therefore **1392** (`1382 + 9 + 1`). The semantic denominator and the cross-domain technical denominator remain incomplete; no percentage is declared.

## Current provider override — Hazen N Stuff 1.4.0.14

The sibling physical re-audit at `neoforge-rpg-skilltree@278b427023136d7c43d85dc188d0eac1ac85ef3a` certifies `hazennstuff-1.4.0.14.jar` / mod id `hazennstuff` / runtime `1.4.0.14` / physical SHA-1 `3be20bacb44c1923348ab6f61b685eec6aacfdcd`. Exact public source pin `Hazentouvel/Hazen_N_Stuff@5fcaf39cf399609f6c1c87d14f8d4807098c9cce` declares the same provider version and closes **38 active Iron's spell registrations**. The same release localization has 41 root spell keys: `brimstone_hellblast` and `supernova` have no active registry entry, while `reign_of_tyros` has a source class/localization root but its registration line is commented; all three are excluded. Registry-level source inspection finds no conditional registration/config/mod-presence branch around the 38 active identities. Thirty-five spells inherit host/default crafting gates; Golden Shower, Night's Edge Strike and Scorching Slash have provider-specific inventory gates whose required provider items have exact release crafting paths. Custom Cosmic/Radiance/Shadow/Hydro focus routing is also source-reconciled against the current HazentouveLib 1.0.9 / Ace's Spell Utils infrastructure. Therefore Hazen contributes **+38 `COUNTED_SOURCE_PINNED`**, raising the strict reconstructible minimum at that checkpoint from **1344 to 1382**. Runtime compatibility remains fail-closed.

The old technical `68/100` component ratio is now a **historical checkpoint**, not a current denominator claim: the 22/09 sibling physical re-audit has surfaced magic components not represented in that older 100-component baseline. Hazen closes the next known provider component, but the denominator must be regenerated from the current physical modlist before another fraction or percentage is published. See [Hazen N Stuff](../providers/%E2%9C%85-hazen-n-stuff/README.md) and [its source-pinned inventory](../providers/%E2%9C%85-hazen-n-stuff/SOURCE-1.4.0.14-SPELL-INVENTORY.md).

## Current provider override — Create: Wizardry 1.21.1-0.5.1-pre1

The current sibling physical index at `neoforge-rpg-skilltree@4767f5c637c02c6d91ccb43a86ea1539f42a2e9b` certifies physical row **#166** as `create_wizardry-1.21.1-0.5.1-pre1.jar` / mod id `create_wizardry` / runtime `1.21.1-0.5.1-pre1`. Exact official public source pin `TTZPlayz/Create-Wizardry@9c4e53aad0ee9477187487443b597b77ef06f323` declares the same version line. No independent installed-JAR hash is retained for this row, so byte equality is not claimed.

Bounded source inspection closes the semantic ownership question: no provider spell registry/resource surface is present, while Blaze Caster and Mana Siphon consume existing Iron's spell/mana contracts. Create: Wizardry is therefore **✅ cataloged** as `ZERO_SEMANTIC_HOST_SPELL_AUTOMATION` with **+0** independent semantic magic objects. At that provider checkpoint, the strict reconstructible minimum remained **1382**. Runtime automation/resource settlement remains fail-closed. See [Create: Wizardry](../providers/%E2%9C%85-create-wizardry/README.md) and [its source-pinned magic-surface audit](../providers/%E2%9C%85-create-wizardry/SOURCE-1.21.1-0.5.1-PRE1-MAGIC-SURFACE.md).


## Current provider override — Iron's Apothic 2.2.2

The current sibling certified row at `neoforge-rpg-skilltree@c3de5878d69a7a6b4441606ef2b9e96a61a8f2e9` records `irons_apothic-2.2.2.jar` / mod id `irons_apothic` / runtime `2.2.2` at row #339. Exact official source pin `muon-rw/Apotheosis-Irons-Spells@c5d501219cc9bbbfb8c69acc08bebac76983d1c1` declares the same version and closes the provider's magic surface as a bridge over Iron's and Apotheosis/Apothic.

The exact source registers 7 custom affix codecs, contains 140 affix definitions, 48 explicit spell/imbued-spell affix definitions and 24 gem definitions. Spell-trigger codecs resolve external holders from Iron's `SpellRegistry`; no provider-owned spell registry is established. Iron's Apothic is therefore **✅ cataloged** with **+0 independent semantic magic objects**, leaving the strict minimum at **1382** at that provider checkpoint. The current technical denominator remains `PENDING REBASE`, so this closure is not assigned a new `N/100` component fraction. Runtime proc/cooldown/targeting and version-drift QA remain fail-closed.

See [Iron's Apothic](../providers/%E2%9C%85-irons-apothic/README.md), [exact source magic-surface inventory](../providers/%E2%9C%85-irons-apothic/SOURCE-2.2.2-MAGIC-SURFACE.md), and the narrow queue/capability overlays.

Phase 2BS — T.O Magic n' Extras / Traveloptics 4.4.0.1-1.21.1 — is a **partial catalog with +0 strict semantic delta and +0 component delta**. Exact publisher file `6342780` closes 33 registered spell identities and excludes 32 residual localization-only roots. `traveloptics:blackout` remains reachability-unresolved under `AbstractUniqueSpell.allowCrafting=false`, and exact `TOLootModifiers` wiring references `KeyLootModifier.CODEC` twice while `UniversalLootModifier.CODEC` is absent from that registration path. Runtime crash is not claimed reproduced. Phase 2BS therefore leaves the strict minimum at **1344** and technical closure at **66/100 at that checkpoint**. See [`../providers/traveloptics/README.md`](../providers/traveloptics/README.md), [`../providers/traveloptics/EXACT-4.4.0.1-ARTIFACT-AUDIT.md`](../providers/traveloptics/EXACT-4.4.0.1-ARTIFACT-AUDIT.md) and [`PHASE2BS-TRAVELOPTICS-4.4.0.1-PARTIAL-CHECKPOINT.md`](./PHASE2BS-TRAVELOPTICS-4.4.0.1-PARTIAL-CHECKPOINT.md).

Phase 2BT — Vampire Spells Addon 0.0.9 — has semantic delta **+0** and closes technical component **#67**. Official release `1.21.1-0.0.9` and exact source target `xsharov/VampireSpellsAddon@2d36e94e67611a316b7311b11e4574b499025580` show a compatibility/runtime-policy overlay over Iron's + Vampirism: spell/school identifiers belong to `irons_spellbooks`, integration is installed through bridge/listener surfaces, and no provider-owned spell, school, ritual or equivalent action registrar is established. PR #239 merged the durable audit as `main@1c5091807a8773d378c34ffac2e737b5f08b545c`, and the exact merge SHA passed Black Arcana CI run `34795795283` GREEN. The strict semantic minimum remains **1344** while technical component closure becomes **67/100**. Runtime bridge behavior, effective config and physical byte equality remain separate fail-closed gates. See [`../providers/vampire-spells-addon/RELEASE-SOURCE-0.0.9-AUDIT.md`](../providers/vampire-spells-addon/RELEASE-SOURCE-0.0.9-AUDIT.md).

Mobstein `5.4.4` is now a durable zero-semantic catalog closure. PR #318 was squash-merged as `main@73cd692ac0f6aa96ee1a6c422f09d0fcc648c8f4`; exact-SHA post-merge Black Arcana CI **#3217** / run `35293505012` completed GREEN, including canonical verification and the Stage 05 companion dedicated-server smoke. Exact physical SHA-1 `3672d88f940ddd474a5429d7066b099cd0ce0c29` plus the successful resource-only clean-room audit closes Mobstein as `ZERO_SEMANTIC_ACTIONS` with **+0** semantic objects. At that historical checkpoint, this shared reconciliation closed technical provider component **#68 / 68 of 100** while the strict semantic minimum remained **1344**. Runtime/API/Sable integration remains fail-closed and is not a catalog blocker.

**Current Somake override — 1.0.9.** The current reorganized sibling modlist checked at `neoforge-rpg-skilltree@cd514bc0456a42ef3f76059c32d9e59d88f1e06b` retains the certified Somake entry `somakespells-1.0.9-1.21.1.jar` / runtime `1.0.9`. Exact CurseForge file `8867079` was resource-audited clean-room at release SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0`; 83 base spell-localization roots each have a matching `.guide` key, but localization is **not** registry proof. The same exact 1.21.1 changelog explicitly names 16 current-line spells (10 Spirit/Evocation, 1 Holy, 1 Sound, 1 Aqua, 3 Blood) and states `Summon Zombie` was replaced by `Summon Drowned`; these are publisher-named semantic provenance, not registry identities or a complete total. The official 1.0.9 changelog also confirms a broad optional-provider gate for Legendary Monsters: its Spirit/Red Soul/items tranche loads only when Legendary Monsters is installed. The latest explicit sibling dossier for `legendary_monsters` records physical `2.2.2` installation at its preserved pack checkpoint, so that broad presence condition is satisfied there; this does **not** establish the exact 1.0.9 spell registry or object-level registration predicates. Black Arcana still lacks physical-pack SHA-1 equality for Somake 1.0.9, exact current registry/predicate closure, and deployed config/host/reachability evidence. Therefore Somake stays **⚠️ conditional / +0**, and all 1.0.8-fix exact-registry text below is historical only.

Phase 2BR has a semantic delta of **+12 `COUNTED_RELEASE_BOUNDED`**: exact publisher release file `7041615` closes twelve unconditional `GGSpells` registrations — ten Geo and two Holy — while `EarthshatterSpell` is present but unregistered and the non-registry adaptation classes add zero provider identities. The repository does not preserve an independent local physical-JAR hash, so this is release-bounded rather than `COUNTED_EXACT`. A dedicated exact-release audit proves all ten registered Geo classes inherit Iron's `allowCrafting`, `isEnabled` and `canBeCraftedBy` host gates; exact Geo focus data plus the canonical Iron's Scroll Forge contract close catalog-level Geo reachability, while exact Umvuthi loot identifiers and the exact file changelog close catalog-level acquisition for `solar_beam` and `solar_storm`. This shared reconciliation raises the strict minimum to **1344** and closes provider component **#66**, while assembled-pack runtime/config/protection behavior remains fail-closed. See [`../providers/gtbcs-geomancy-plus/README.md`](../providers/gtbcs-geomancy-plus/README.md), [`../providers/gtbcs-geomancy-plus/EXACT-1.1.0-ARTIFACT-AUDIT.md`](../providers/gtbcs-geomancy-plus/EXACT-1.1.0-ARTIFACT-AUDIT.md) and [`PHASE2BR-GTBC-GEOMANCY-PLUS-1.1.0-EXACT-CHECKPOINT.md`](./PHASE2BR-GTBC-GEOMANCY-PLUS-1.1.0-EXACT-CHECKPOINT.md).

Phase 2BQ has a semantic delta of **0**: exact hash-matched `ars_two_way_portals-2.0.0.jar` contains portal/compat infrastructure, two provider items, three recipes and seven required mixins, but no independent spell/glyph/ritual/rite/ability registry or semantic resource surface. It is classified `ZERO_SEMANTIC_PORTAL_INFRA`; the strict semantic minimum stays **1332** while this shared reconciliation closes provider component **#65**. Runtime portal lifecycle, effective config, mixin application and assembled-host Immersive behavior remain fail-closed. See [`../providers/ars-two-way-portals/README.md`](../providers/ars-two-way-portals/README.md), [`../providers/ars-two-way-portals/EXACT-2.0.0-ARTIFACT-AUDIT.md`](../providers/ars-two-way-portals/EXACT-2.0.0-ARTIFACT-AUDIT.md) and [`PHASE2BQ-ARS-TWO-WAY-PORTALS-2.0.0-EXACT-CHECKPOINT.md`](./PHASE2BQ-ARS-TWO-WAY-PORTALS-2.0.0-EXACT-CHECKPOINT.md).

Phase 2BP has a semantic delta of **+10 `COUNTED_SOURCE_PINNED`**: physical `aero_additions-1.2.8.jar` / SHA-1 `dee32c9fa84d6e39846608f8f77591ea56f` is reconciled with exact public source pin `snackerpirater/aero-additions@ae282b32d25ad76ef8d01c637ec05566a767ae4c`, which closes exactly ten active unconditional Wind `AbstractSpell` registrations. Five commented-out registrations are excluded. Provider Wind focus data plus the Iron's 3.16.3 Scroll Forge contract close a host-native Breeze Rod catalog acquisition route; provider loot modifiers also add Breeze Rod support to Trial Chamber normal-vault rewards. This closes provider component **#64** while keeping assembled-pack runtime compatibility fail-closed. See [`../providers/aeromancy-additions/README.md`](../providers/aeromancy-additions/README.md) and [`PHASE2BP-AEROMANCY-CHECKPOINT.md`](./PHASE2BP-AEROMANCY-CHECKPOINT.md).

Phase 2BO has a semantic delta of **+6 `COUNTED_SOURCE_PINNED`**: physical `farmers-spell-n-spellbook-1.0.5.1-1.21.1.jar` / SHA-1 `f77355e029af39bbaba3854e10cc087a608351ff` is reconciled with exact public source pin `GLDYM/Farmers-Spell-n-Spellbook@b7cbb40316a9ccbbc2ce2b56b3023647261ce569`, which closes exactly six unconditional Gluttony `AbstractSpell` registrations. Provider Gluttony focus data plus the Iron's 3.16.3 Scroll Forge contract close a host-native catalog acquisition route; generic random scroll loot is not claimed because the school sets `allowLooting=false`. This closes provider component **#63** while keeping current-host runtime compatibility fail-closed. See [`../providers/farmers-spell/README.md`](../providers/farmers-spell/README.md) and [`PHASE2BO-FARMERS-SPELL-CHECKPOINT.md`](./PHASE2BO-FARMERS-SPELL-CHECKPOINT.md).

Phase 2BN has a semantic delta of **0**: exact official source pin `baileyholl/ars-sable@1fd83f3a998e3a41b5a21d0d6529140a0b0a55ba` closes the provider's role as a narrow Ars Nouveau ↔ Sable spatial/sublevel compatibility layer. The exact source has 24 common + 5 client required mixins, protocol registrar version `2`, zero provider-owned payload registrations, and no provider-owned spell/glyph/ritual/school/resource/action registry. This closes provider component **#62** while keeping current-host runtime compatibility fail-closed. See [`../providers/ars-sable/README.md`](../providers/ars-sable/README.md) and [`PHASE2BN-ARS-SABLE-CHECKPOINT.md`](./PHASE2BN-ARS-SABLE-CHECKPOINT.md).

Phase 2BM has a semantic delta of **0**: exact official source pin `Vonr/Ars-Polymorphia@e09b6c9ab434ccbb3232ca47b37ca5666becfb6f` closes the provider's role as an Ars Storage/Crafting Lectern ↔ Polymorph recipe-conflict bridge, without a provider-owned spell, glyph, ritual, school, mana/resource or equivalent magical-action registry. This closes provider component **#61** while keeping current-host runtime compatibility fail-closed. See [`../providers/ars-polymorphia/README.md`](../providers/ars-polymorphia/README.md) and [`PHASE2BM-ARS-POLYMORPHIA-CHECKPOINT.md`](./PHASE2BM-ARS-POLYMORPHIA-CHECKPOINT.md).

Phase 2BK has a semantic delta of **0**: exact hash-matched Ignis Soulfires: Spellbooks 1.1.0 contains only its armor-material/item bridge surfaces and no provider-owned spell, ritual, rite or equivalent action registry. This closes provider component **#58** without changing the semantic numerator. See [`../providers/ignis-soulfires-spellbooks/EXACT-1.1.0-ARTIFACT-AUDIT.md`](../providers/ignis-soulfires-spellbooks/EXACT-1.1.0-ARTIFACT-AUDIT.md).

The latest semantic promotion before Phase 2BL was **Gaze +1**. Exact hash-matched 1.1.7.1 artifact evidence closes one Gaze-owned Iron's standalone spell identity, Soulward Shield, with the optional Iron's provider gate satisfied by the physical pack. The same artifact closes 26 player-facing Spirit Rite identities, but they remain `CONDITIONAL` because the deployed COMMON `disableGazeRites` value is unavailable; two Geas effect types and eight rune items are metric-excluded. See [`../providers/gaze/EXACT-1.1.7.1-ARTIFACT-AUDIT.md`](../providers/gaze/EXACT-1.1.7.1-ARTIFACT-AUDIT.md).

The preceding semantic promotion is **Goety +361**. Exact hash-matched 3.1.4 artifact evidence closes 123 active/acquirable Focus actions and 238 available distinct non-Focus ritual actions after semantic deduplication and physical-provider condition filtering. Runtime/API/balance and provider-owned settlement remain separate fail-closed gates. See [`../providers/goety/EXACT-3.1.4-ARTIFACT-AUDIT.md`](../providers/goety/EXACT-3.1.4-ARTIFACT-AUDIT.md).

The preceding semantic promotion is **Leyline Spellbooks +14**. Exact hash-matched 1.0.3 artifact evidence closes 14 unconditional provider spell registrations; no Leylines-specific spell lock or conditional registration gate is present, while generic Iron's host config remains separate runtime QA. See [`../providers/leyline-spellbooks/EXACT-1.0.3-ARTIFACT-AUDIT.md`](../providers/leyline-spellbooks/EXACT-1.0.3-ARTIFACT-AUDIT.md).

The preceding semantic promotion is **Cataclysm: Spellbooks +59**. Exact hash-matched 1.1.13 artifact evidence closes 59 unconditional provider spell registrations; ten additional root localization identities are not registered in the installed artifact and remain excluded. The generic/current 65-spell publisher scale is not substituted for the physical 1.1.13 registry. See [`../providers/cataclysm-spellbooks/EXACT-1.1.13-ARTIFACT-AUDIT.md`](../providers/cataclysm-spellbooks/EXACT-1.1.13-ARTIFACT-AUDIT.md).

The preceding semantic promotion is **Alshanex's Familiars +18**. Exact hash-matched 4.0.3 artifact evidence closes seven provider-owned spell registrations and eleven packaged custom `alshanex_familiars:ritual_recipe` identities. Sound/Melodic content remains counted only under Tunes n' Tomes, while familiar AI/passives and external Iron's spell casts remain excluded. See [`../providers/alshanex-familiars/EXACT-4.0.3-ARTIFACT-AUDIT.md`](../providers/alshanex-familiars/EXACT-4.0.3-ARTIFACT-AUDIT.md).

The preceding semantic correction is **Werewolves +1**. Exact source pin `TeamLapen/Werewolves@b72635b3e014e406b25bb79adb9d340f7443660b` proves that `LEAP` is an `ActionSkill`, that `SURVIVAL31` grants it, that the node is connected into the generated normal `werewolf_level` tree, and that the provider has a dedicated server-handled Leap input path. Hidden-selector presentation therefore does not make Leap unreachable. Werewolves contributes **8** counted semantic actions rather than 7; `hide_name` remains excluded as presentation-only and the separate `no_leap_cooldown` refinement remains an open modifier-acquisition question rather than a separate semantic action. See [`SEMANTIC-MAGIC-DELTA-WEREWOLVES-LEAP.md`](./SEMANTIC-MAGIC-DELTA-WEREWOLVES-LEAP.md).

Phase 2AY itself has a semantic delta of **0**: GTBC's SpellLib 2.2.0 is publisher-defined shared spell/addon library/API infrastructure and does not establish an independent standalone spell catalog. Its reusable spell/helper, imbuement, Curio, trade, particle, summon and attribute surfaces do not mint semantic spell identities by themselves.

Therefore:

- semantic numerator/denominator delta attributable to Vampire Spells Addon 0.0.9 source-pinned zero closure: **+0**;
- semantic numerator delta from GTBC's Geomancy Plus 1.1.0-1.21.1 release-bounded closure: **+12**;
- semantic numerator/denominator delta attributable to Ars Nouveau: Two-Way Portals 2.0.0 exact closure: **+0**;
- semantic numerator delta from SnackPirate's Aeromancy Additions 1.2.8 source-pinned closure: **+10**;
- semantic numerator delta from Farmer's Spell 'n Spellbooks 1.0.5.1 source-pinned closure: **+6**;
- semantic numerator/denominator delta attributable to Ars Sable 1.1.2: **+0**;
- semantic numerator/denominator delta attributable to Ars Polymorphia 1.0.3: **+0**;
- semantic numerator/denominator delta attributable to Ignis Soulfires: Spellbooks 1.1.0: **+0**;
- semantic numerator delta from Gaze 1.1.7.1 exact closure: **+1**;
- semantic numerator delta from Goety 3.1.4 exact closure: **+361**;
- semantic numerator delta from Leyline Spellbooks 1.0.3 exact closure: **+14**;
- semantic numerator delta from Cataclysm: Spellbooks exact closure: **+59 historical/current retained**; 1.1.14 revalidation changes evidence strength, not the numerator;
- semantic numerator delta from Alshanex's Familiars 4.0.3 exact closure: **+18**;
- semantic numerator delta from the preceding Werewolves correction: **+1**;
- semantic numerator/denominator delta attributable to GTBC's SpellLib: **+0**;
- semantic numerator delta from Companions! 1.3.4 source-pinned closure: **+9**;
- semantic numerator delta from Crystal Chronicles 0.1.3-alpha source-pinned closure: **+1**;
- semantic numerator delta from Goety Iron 3.1 exact closure: **+14**;
- semantic numerator delta from Goety Cataclysm 1.21.1-1.8.2 exact closure: **+52**;
- strict reconstructible semantic minimum: **1392**;
- the global semantic denominator remains incomplete because other providers still have open granular inventories;
- **do not derive a spell/magic percentage from the provider-component metric below**.

The preceding semantic-only promotion was **Malum +26**: whole-interval path history across the observed `1.8.2` source window plus stable endpoint blobs close 26 base-Malum `SpiritRiteType` identities. Release-bounded Codex evidence separately proves that the two special identities, `undirected_rite` and `unchained_rite`, are player-facing rather than sentinel/proxy slots: `TotemMagicEntries.setupEntries(ArcanaProgressionScreen)` adds each as a distinct progression entry backed by its corresponding `RiteHolder`, `SpiritRiteTextPage`, and `SpiritRiteRecipePage`, while every observed `CodexLangDatagen.java` snapshot in the 1.8.2 interval preserves dedicated entries for both. The same release-bounded audit also records 37 active `GeasEffectType` identities and 9 `SpiritArcanaType` resource identities, but those are excluded from the current semantic-action metric by definition. Exact installed-JAR/source equivalence and runtime/API/recipe mechanics remain separate gates. The preceding semantic-only promotion was **Hexalia +25**: 19 player-facing Nature's Ritual identities plus 6 Celestial Infusion identities release-bounded across the observed 1.3.5 metadata / 1.3.6 filename-source boundary. Neither semantic promotion changes the internal provider-component closure metric below.

Phase 2BH is canonical for Goety 3.1.4 from exact hash-matched artifact evidence: **123 active Focus actions + 238 available distinct non-Focus ritual actions = 361**. Durable PR #198 HEAD `d75f82a23b5c977ccc8ec84813bf89c928ffc0ab` passed CI #2523; squash merge `4fcc40aaf8149b5511dbd882a5616ee5240cd640` passed exact-SHA post-merge CI #2524 and published canonical QA artifact `10291461067` with SHA-256 `4f2ccf8be11cdba348c7cd0bdc64e595f6b101257b2b99f80fbe5542fae41ada`. Canonical values are **1249 / 57 of 100**. Runtime/API/balance gates remain separate.

The previous chat-only working tally is not an authority and is not used as an input to the versioned ledger.

## Phase 2BT — Vampire Spells Addon 0.0.9 component #67, source-pinned zero closure

Official release `1.21.1-0.0.9` is correlated to exact source target `xsharov/VampireSpellsAddon@2d36e94e67611a316b7311b11e4574b499025580`. The provider is an Iron's + Vampirism compatibility/runtime-policy overlay: the audited magic IDs are Iron's-owned, provider registration installs bridges/listeners, and no provider-owned spell, school, ritual or equivalent action registrar is established. Semantic disposition is `ZERO_BRIDGE_INFRA`, **+0**.

PR #239 merged the durable audit as `main@1c5091807a8773d378c34ffac2e737b5f08b545c`; exact-SHA post-merge Black Arcana CI run `34795795283` is GREEN. This shared reconciliation therefore closes technical provider component **#67 / 67 of 100** while keeping the strict semantic minimum at **1344**. Exact physical-JAR byte equality, reflective integration contracts, mixin/event ordering, effective serverconfig and live resource/damage/cooldown behavior remain fail-closed runtime QA.

## Phase 2BP — SnackPirate's Aeromancy Additions 1.2.8 component #64, source-pinned spell closure

Physical `aero_additions-1.2.8.jar` / SHA-1 `dee32c9fa84d6e39846608f8f77591ea56f` is reconciled with exact public source `snackerpirater/aero-additions@ae282b32d25ad76ef8d01c637ec05566a767ae4c`. The source-pinned registry closes exactly ten active unconditional Wind spells: `wind_charge`, `updraft`, `airstep`, `asphyxiate`, `feather_fall`, `wind_shield`, `airblast`, `wind_blade`, `flush`, `dash`. Tornado, Thunderclap, Summon Breeze, Telelink and Shapeshift remain excluded because their registration lines are commented out at the audited pin. The Wind school is support taxonomy rather than an eleventh semantic action.

Provider data supplies the Breeze Rod Wind focus route and the Iron's 3.16.3 source-line Scroll Forge contract corroborates host-native catalog reachability. Provider global loot modifiers additionally append Breeze Rod support to the normal Trial Chamber vault reward table. Updraft Tome and Wind Sword embed already-counted provider spells and do not add semantics. The ten spells are therefore `COUNTED_SOURCE_PINNED`, not `COUNTED_EXACT`.

PR #219 exact reconciled HEAD `6e39a01273b77ba8accf85d49647b6ceff840e8a` passed Black Arcana CI #2577 / run `34730598682`; squash evidence merge `84e9635b446b605140ab349fa2edc51f3462d518` passed exact-SHA post-merge CI #2578 / run `34730783233`. Phase 2BP raises the Iron ecosystem subtotal from **548 to 558**, the strict minimum from **1322 to 1332**, and this separate shared-ledger reconciliation promotes provider component **#64 / 64 of 100**.

No assembled-pack runtime compatibility PASS is claimed. Source 1.2.8 targets NeoForge `21.1.228` and Iron's `1.21.1-3.16.1`, while the physical pack uses NeoForge `21.1.248` and Iron's `3.16.3`; the declared Iron's range accepts the physical version, but required mixin application, provider payload behavior, physical Scroll Forge/config behavior, representative casts, persistence/reload and duplicate-processing checks remain direct runtime QA gates.

## Phase 2BO — Farmer's Spell 'n Spellbooks 1.0.5.1 component #63, source-pinned spell closure

Physical `farmers-spell-n-spellbook-1.0.5.1-1.21.1.jar` / SHA-1 `f77355e029af39bbaba3854e10cc087a608351ff` is reconciled with exact public source `GLDYM/Farmers-Spell-n-Spellbook@b7cbb40316a9ccbbc2ce2b56b3023647261ce569`. The source-pinned registry closes exactly six unconditional Gluttony spells: `goodberry`, `phantom_loot`, `seal_coat`, `bad_apple`, `chaos_slash`, `preserve_circle`. The Gluttony school is support taxonomy rather than a seventh semantic action.

Provider data supplies the Gluttony focus route and the Iron's 3.16.3 source-line Scroll Forge contract corroborates host-native catalog reachability; generic random scroll loot is deliberately excluded because the school sets `allowLooting=false`. The six spells are therefore `COUNTED_SOURCE_PINNED`, not `COUNTED_EXACT`.

PR #214 corrected HEAD `d3a92c31d7ac5b38183224ef28c6737e721fc758` passed Black Arcana CI #2564 / run `34723967662`; squash merge `34a5fd495da744800b32b051e38c6473c6f5ea15` passed exact-SHA post-merge CI #2565 / run `34724351805` and published artifact `10307207453` (`sha256:50b94c3efc207dfd143a10367cf234473ede7dbbc1f36b9acdd3d3ca1ccc67fa`). Phase 2BO raises the Iron ecosystem subtotal from **542 to 548**, the strict minimum from **1316 to 1322**, and closes provider component **#63 / 63 of 100**.

Runtime compatibility remains fail-closed: source build targets NeoForge `21.1.238` and Farmer's Delight `1.3.2`, while the physical pack uses NeoForge `21.1.248` and Farmer's Delight `1.3.4`; all seven provider mixins are required. GeckoLib is `4.9.2` on both source build and physical pack by version label, which is not itself a runtime PASS. No provider-owned payload registrations are observed at the exact source pin.

## Phase 2BN — Ars Sable 1.1.2 component #62, source-pinned zero closure

Exact official source `baileyholl/ars-sable@1fd83f3a998e3a41b5a21d0d6529140a0b0a55ba` matches the installed provider version 1.1.2 and closes its technical role as a compatibility/spatial layer between Ars Nouveau and Sable. The exact source exposes 24 common + 5 client required mixins, protocol registrar version `2`, zero provider-owned payload registrations, and no provider-owned spell/glyph/ritual/school/resource/action registry. The semantic delta is therefore **+0** and the strict minimum remains **1316** at that historical checkpoint.

PR #212 exact HEAD `c4facc0286da...` passed Black Arcana CI #2553 / run `34720437808`; squash merge `c1c422b5ec72fe4308104f04282732d6c2f2bbc1` passed exact-SHA post-merge CI #2554 / run `34720646567` and published canonical QA artifact `10306246238` (`sha256:a63f42f6746cc62e435e6a1c541daaed973b0b56d3dcc566cbc7cf4e9fa57e96`). Provider component **#62** is therefore closed. Runtime compatibility remains fail-closed because exact source was built against Sable `1.2.2` while the physical pack uses Sable `2.0.5`, and against Ars Nouveau `5.11.7.1354` while the physical pack uses `5.13.1`; all 29 mixins are required. Exact source metadata declares `LGPLv3` while the root `LICENSE` contains The Unlicense, so no reuse/license conclusion is inferred beyond read-only clean-room factual inspection.

## Phase 2BM — Ars Polymorphia 1.0.3 component #61, source-pinned zero closure

Exact official source `Vonr/Ars-Polymorphia@e09b6c9ab434ccbb3232ca47b37ca5666becfb6f` matches the installed provider version 1.0.3 and closes its technical role as a recipe-conflict bridge for Ars Storage/Crafting Lecterns. The exact source exposes five required mixin/accessor bindings, protocol version `1`, and one provider-owned play-to-server unit payload, while establishing no provider-owned spell/glyph/ritual/school/resource/action registry. The semantic delta is therefore **+0** and the strict minimum remains **1316** at that historical checkpoint.

PR #210 exact HEAD `1b8d5d5761569f8ef1f3a32b7ece84cfb6ce6df6` passed Black Arcana CI #2543; squash merge `f2cdfe7b79d500540c281d70a76e8b6e3a77d311` passed exact-SHA post-merge CI #2544 / run `34713268914` and published canonical QA artifact `10303624842` (`sha256:f4ff7ce2fac582f435f037f3a8dd29469df25d8889b895b0c168c2b0d6da0719`). Provider component **#61** is therefore closed. Runtime compatibility remains fail-closed because exact source requires mod id `polymorph` while the physical pack exposes `polymorph_plus`, source was built against Ars Nouveau `5.4.2.938` while the pack uses `5.13.1`, and source metadata declares `minecraft_version=1.21.1` together with range `[1.21,1.21.1)`.

## Phase 2BL — Goety addon exact closures, components #59 and #60

Exact hash-matched evidence closes **Goety Iron +14** (2 Focus + 12 non-Focus rituals) and **Goety Cataclysm +52** (28 Focus + 24 non-Focus rituals). Acquisition recipes are deduplicated against Focus identities; counted non-Focus rituals have distinct outcomes and no mod-loaded conditions. Narrow registry-gate scans find zero initializer branches and zero config references for Focus registration in both providers.

Phase 2BL therefore moves the strict semantic minimum to **1316** and the separate provider-component metric to **60/100**. NON-MERGE evidence PRs are #205 and #206. Runtime/balance/servant lifecycle and any Black Arcana adapter remain separate fail-closed gates.

## Phase 2BK — Ignis Soulfires: Spellbooks 1.1.0 component #58, exact zero closure

Exact hash-matched artifact evidence closes the provider as `BRIDGE_COMPAT + GEAR_LOOT_SUPPORT`: 11 provider classes, one armor-material registry, one five-item equipment registry, and no provider-owned spell/ritual/action registry. Clean-room structural inspection finds 0 `AbstractSpell`, `registerSpell`, `SpellRegistry`, `Ritual`, `Rite` and `Ability` class hits. Semantic disposition is `ZERO_BRIDGE_INFRA` with **+0**; the strict semantic minimum remains **1250**.

Isolated NON-MERGE PR #203 exact HEAD `ed807b77345cde1803767d804e26ea972c41d964` passed run `34688273425`; text-only evidence artifact `10296406134` has digest `sha256:5e96a319aea648aadf2c70bdf9b870a26a9503068307befc8a9972bb7b1cd52e`. The provider was already an open unit in the reconciled 100-component denominator, so exact closure moves the technical metric to **58/100**. Runtime numerical gear behavior and any future adapter remain separate fail-closed gates.

## Phase 2BJ — Gaze 1.1.7.1 semantic-only exact promotion

Exact hash-matched artifact evidence closes **+1** current semantic object: Gaze-owned Iron's spell Soulward Shield, with the physical Iron's provider gate satisfied. Gaze's 26 exact player-facing Spirit Rites remain configuration-conditional because the deployed COMMON `disableGazeRites` value is unavailable; the two Geas effect types and eight rune items remain excluded by metric definition. Isolated NON-MERGE PR #201 final audit HEAD `2f4ff6536663b1c629a6a5ea92416765bea17b1e` passed evidence run `34676660467` and published artifact `10292013626` (`sha256:fb69f353b672f7c8ec7b470c454d24d1c3110cb996a250076a16d2b053f23f71`).

Phase 2BJ changes the strict semantic minimum to **1250** but does **not** close another provider component; the internal component metric stays **57/100**. Runtime/config/balance and any Black Arcana adapter remain fail-closed.

## Phase 2BH — Goety 3.1.4 component #57, canonical

Exact 3.1.4 artifact identity closes **+361** and component #57. Durable PR #198 clean HEAD `d75f82a23b5c977ccc8ec84813bf89c928ffc0ab` passed Black Arcana CI #2523 / run `34672038273`; squash merge `4fcc40aaf8149b5511dbd882a5616ee5240cd640` passed exact-SHA post-merge CI #2524 / run `34672222798` and published the canonical QA JAR. See `PHASE2BH-GOETY-3.1.4-EXACT-CHECKPOINT.md` and `../providers/goety/EXACT-3.1.4-ARTIFACT-AUDIT.md`. Canonical totals are **1249 / 57/100** at that historical checkpoint.

## Phase 2BG — Leyline Spellbooks 1.0.3 component #56, canonical

Exact hash-matched Leylines 1.0.3 evidence closes 14 unconditional registered spells and removes the provider-specific eligibility blocker; exact Iron's host defaults/scroll behavior corroborate normal reachability while deployed generic host config remains separate runtime QA. Leylines is now **+14 semantic objects**, the Iron subtotal is **541**, the strict minimum is **888**, and provider component **#56 / 56/100** is canonical at that checkpoint.

Durable PR #195 clean HEAD `a9d7b55044230bbb011f7233ffd75d9a8321489b` passed Black Arcana CI **#2503** / run `34668329229`. Squash merge `88f042f68429ff920314a7ec3a6923369edc93fd` passed exact-SHA post-merge CI **#2504** / run `34668535721`, including canonical QA-JAR publication. Numerical balance, complete-modpack runtime QA and any Black Arcana adapter/API seam remain separate fail-closed gates.

## Internal provider-component closure metric

**Historical provider-component checkpoint after the Mobstein 5.4.4 shared reconciliation: 68/100 = 68%. The current denominator is `PENDING REBASE` and this fraction must not be published as current coverage.**

Mobstein 5.4.4 / PR #318 was squash-merged as `73cd692ac0f6aa96ee1a6c422f09d0fcc648c8f4`; exact-SHA post-merge Black Arcana CI **#3217** / run `35293505012` completed GREEN. The provider contributes semantic **+0 `ZERO_SEMANTIC_ACTIONS`** and this shared reconciliation closes technical component **#68**. This is catalog closure, not a runtime/API compatibility PASS.

Phase 2BT / PR #239 was merged as `1c5091807a8773d378c34ffac2e737b5f08b545c`; that exact durable merge SHA passed Black Arcana CI run `34795795283`. The provider contributes semantic **+0 `ZERO_BRIDGE_INFRA`** and this reconciliation closes technical component **#67**. This is catalog closure, not a runtime compatibility PASS.

Phase 2BR / PR #226 was squash-merged as `4ab4ad990d453938e67f3d2b7cfa878bbe031ef0`; that exact durable merge SHA passed post-merge Black Arcana CI **#2654** / run `34738972649`, including unit tests, diff sanity, NeoForge build, built-JAR verification, Foundation GameTest server, dedicated-server smoke and canonical QA artifact `10311522907` (`sha256:c815f684a7a6dec192dd995bb6fbd6784c35faa0b0d21ae39bb9de89b93cec16`). The provider contributes semantic **+12 `COUNTED_RELEASE_BOUNDED`** and this reconciliation closes technical component **#66**.

Phase 2BQ / PR #223 was squash-merged as `bc5428b5855e4d5821d5bd901fb591a62ecf3cbe`; that exact merge SHA passed post-merge Black Arcana CI **#2622** / run `34735586680`, including unit tests, diff sanity, NeoForge build, built-JAR verification, Foundation GameTest server, dedicated-server smoke and canonical QA artifact `10310957237` (`sha256:de930eaba7f0f5730810747050ec500b4d72ed793cfbdce0c8603e3af8d8cc9d`). The provider contributes semantic **+0** and closes technical component **#65** only.

Phase 2BF is now a **historical 1.0.8-fix checkpoint**: its exact-artifact reconciliation closed 67 registrations for that artifact under the then-current optional-provider set, but the current physical provider line has advanced to 1.0.9. The 67-ID result must not be read as the current registry. At the historical checkpoint, the provider remained `CONDITIONAL` because deployed COMMON spell-lock configuration and complete survival reachability were not authoritative; Phase 2BF changed neither metric: **874** strict semantic objects and **55/100** closed provider components.

Phase 2BF / PR #192 was audited at exact clean HEAD `85b15aec9faf395cef5460d06a17be58ccd16af8`, which passed Black Arcana CI **#2490**. It was squash-merged as `cc4cfc1d740f7714188e25a3586d8b43bb5eb969`; that exact merge SHA passed post-merge Black Arcana CI **#2491**, including unit tests, diff sanity, NeoForge build, built-JAR verification, Foundation GameTest, dedicated-server smoke and canonical QA-JAR publication.

Phase 2BE / PR #189 was audited at exact HEAD `e787699d25b283b8040cd179f605143e8ee396de`, which passed Black Arcana CI **#2483**. It was squash-merged to `main` as `cce7f51794e4e65b0d97511eb55f710afc6e02f0`. Black Arcana CI **#2484 attempt 1** ended before compilation/tests on a transient external read timeout fetching Iron's API from `code.redspace.io`; rerunning the same job on the unchanged merge SHA produced **#2484 attempt 2 GREEN**, including unit tests, diff sanity, NeoForge build, built-JAR verification, Foundation GameTest server, dedicated-server smoke and canonical QA-JAR publication.

Phase 2BD / PR #186 was audited at exact HEAD `acfcff0fca09b3c2f7b4fcf082618a970e1d19c0`, which passed Black Arcana CI **#2464**. It was squash-merged to `main` as `95ec538ff1c34766450393522ce3affe1039d0dd`; that exact merge SHA passed post-merge Black Arcana CI **#2465**, including unit tests, diff sanity, NeoForge build, built-JAR verification, Foundation GameTest server, dedicated-server smoke and canonical QA-JAR publication.

Phase 2AY / PR #175 merged to `main` as `9a4e1cd6a462a278083ab946b5ed054864c3315e` after exact audited HEAD `2260c46261ac9ab99d839f307fd7b4519d38eef2` passed Black Arcana CI **#2420**. The exact merge SHA then passed post-merge Black Arcana CI **#2421**, including unit tests, diff sanity, NeoForge build, built-JAR verification, Foundation GameTest server, dedicated-server smoke and canonical QA-JAR publication.

The historical Phase 2AW nuance remains recorded: its immediate post-merge workflow #2308 failed at Foundation GameTest after unit tests, diff sanity, NeoForge build and JAR verification had passed, while later current-main validation #2334 completed the full gate successfully. This does not change the canonical #51 status of Apotheotic Creation.

The complete pre-Phase-2AX coverage text is preserved byte-for-byte in [`CATALOG-COVERAGE-CURRENT-PRE-PHASE2AX.md`](./CATALOG-COVERAGE-CURRENT-PRE-PHASE2AX.md). Provider-specific evidence lives under `wiki/modpack-catalog/providers/**` plus the corresponding phase checkpoint/capability files.

## Physical anchor

- Minecraft: 1.21.1
- NeoForge: `21.1.248`
- latest physical modlist: **595 top-level entries**
- modlist SHA-1: `7aaece7acbfb07ba4d0c66029042f36c50d046f0`
- jarjar/internal dependencies are not counted as top-level providers

## Current working component denominator

The historical internal operational denominator was **100 magic/cross-domain component units** under the older physical reconciliation. The current denominator is **`PENDING REBASE`** after the sibling physical re-audit surfaced additional magic/cross-domain components:

- 103 historical candidate IDs;
- 5 historically listed candidates now absent: `ars_morph`, `morerelics`, `reliquary`, `vestis`, `woodwalkers_spellbooks`;
- 2 current candidates added beyond the historical baseline: `soul_fire_d`, `reliquified_lenders_cataclysm_new_relics_fix`;
- therefore `103 - 5 + 2 = 100`.

GTBC's SpellLib, GTBC's Geomancy Plus, FamiliarsLib, Farmer's Spell, Aeromancy Additions, Ars Nouveau: Two-Way Portals and Vampire Spells Addon were already members of those 100 component units, so their closure changes the numerator only. The denominator must be reconciled whenever the physical provider set changes.

## Canonical recent closure sequence

| Component | Phase / PR | Provider | Result |
|---:|---|---|---|
| 47 | Phase 2AS / PR #155 | `apothic_compats` | canonical |
| 48 | Phase 2AT / PR #156 | `apothic_spawners` | canonical |
| 49 | Phase 2AU / PR #158 | `apothic_enchanting` | canonical |
| 50 | Phase 2AV / PR #160 | `apotheosis` | canonical |
| 51 | Phase 2AW / PR #161 | `apotheoticcreation` | canonical; historical immediate post-merge GameTest failure superseded by later full current-main GREEN validation |
| 52 | Phase 2AX / PR #166 | `familiarslib` | canonical at `main@4238275d2086a00c6f31960114733d74b8cdb1d8`; post-merge CI #2337 GREEN |
| 53 | Phase 2AY / PR #175 | `gtbcs_spell_lib` | canonical at `main@9a4e1cd6a462a278083ab946b5ed054864c3315e`; post-merge CI #2421 GREEN |
| 54 | Phase 2BD / PR #186 | `alshanex_familiars` | canonical at `main@95ec538ff1c34766450393522ce3affe1039d0dd`; audited HEAD `acfcff0fca09b3c2f7b4fcf082618a970e1d19c0` CI #2464 GREEN; post-merge CI #2465 GREEN |
| 55 | Phase 2BE / PR #189 | `cataclysm_spellbooks` | canonical at `main@cce7f51794e4e65b0d97511eb55f710afc6e02f0`; audited HEAD `e787699d25b283b8040cd179f605143e8ee396de` CI #2483 GREEN; post-merge CI #2484 attempt 2 GREEN |
| 56 | Phase 2BG / PR #195 | `leylines` | canonical at `main@88f042f68429ff920314a7ec3a6923369edc93fd`; audited HEAD `a9d7b55044230bbb011f7233ffd75d9a8321489b` CI #2503 GREEN; post-merge CI #2504 GREEN |
| 57 | Phase 2BH / PR #198 | `goety` | canonical at `main@4fcc40aaf8149b5511dbd882a5616ee5240cd640`; audited HEAD `d75f82a23b5c977ccc8ec84813bf89c928ffc0ab` CI #2523 GREEN; post-merge CI #2524 GREEN; QA artifact `10291461067` |
| 58 | Phase 2BK | `ignissoulfires_spellbooks` | exact hash-matched 1.1.0 gear/bridge closure; `ZERO_BRIDGE_INFRA`; semantic +0; evidence PR #203 / run `34688273425` |
| 59 | Phase 2BL / PR #207 | `goetyiron` | canonical; exact-artifact semantic +14 closure |
| 60 | Phase 2BL / PR #207 | `goety_cataclysm` | canonical; exact-artifact semantic +52 closure |
| 61 | Phase 2BM / PR #210 | `ars_polymorphia` | canonical at `main@f2cdfe7b79d500540c281d70a76e8b6e3a77d311`; source-pinned `ZERO_SEMANTIC_BRIDGE`; semantic +0; post-merge CI #2544 GREEN |
| 62 | Phase 2BN / PR #212 | `ars_sable` | canonical at `main@c1c422b5ec72fe4308104f04282732d6c2f2bbc1`; source-pinned zero-semantic spatial/compat bridge; post-merge CI #2554 GREEN; runtime host QA fail-closed |
| 63 | Phase 2BO / PR #214 | `farmers_spell` | source-pinned +6 semantic closure; evidence merge `main@34a5fd495da744800b32b051e38c6473c6f5ea15`; post-merge CI #2565 GREEN; runtime host QA fail-closed |
| 64 | Phase 2BP / PR #219 | `aero_additions` | source-pinned +10 semantic closure; evidence merge `main@84e9635b446b605140ab349fa2edc51f3462d518`; post-merge CI #2578 GREEN; runtime host QA fail-closed; promoted by the separate shared-ledger reconciliation |
| 65 | Phase 2BQ / PR #223 | `ars_two_way_portals` | exact hash-matched `ZERO_SEMANTIC_PORTAL_INFRA`; semantic +0; durable merge `main@bc5428b5855e4d5821d5bd901fb591a62ecf3cbe`; post-merge CI #2622 GREEN; QA artifact `10310957237`; runtime host QA fail-closed; canonical |
| 66 | Phase 2BR / PR #226 | `gtbcs_geomancy_plus` | `COUNTED_RELEASE_BOUNDED`; exact publisher file `7041615` closes 12 registrations (10 Geo + 2 Holy); Geo host-gate inheritance and focus reachability audited; Holy Umvuthi acquisition evidenced; durable merge `main@4ab4ad990d453938e67f3d2b7cfa878bbe031ef0`; post-merge CI #2654 GREEN; QA artifact `10311522907`; runtime host QA fail-closed; canonical |
| 67 | Phase 2BT / PR #239 + shared reconciliation | `vampire_spells_addon` | source-pinned `ZERO_BRIDGE_INFRA`; semantic +0; durable audit merge `main@1c5091807a8773d378c34ffac2e737b5f08b545c`; exact post-merge CI run `34795795283` GREEN; runtime bridge QA fail-closed; promoted by this shared-ledger reconciliation |
| 68 | Mobstein closure / PR #318 + shared reconciliation | `mobstein` | exact physical SHA-1 `3672d88f940ddd474a5429d7066b099cd0ce0c29`; resource-only clean-room closure `ZERO_SEMANTIC_ACTIONS`; semantic +0; durable merge `main@73cd692ac0f6aa96ee1a6c422f09d0fcc648c8f4`; exact post-merge CI #3217 / run `35293505012` GREEN; runtime/API/Sable integration fail-closed |

Components #1–#46 remain part of the same canonical numerator and are preserved by prior cumulative snapshots/provider records.

## Phase 2BE — Cataclysm: Spellbooks 1.1.13 component #55, canonical

Phase 2BE closes the physically installed spell identity inventory to exact artifact evidence:

- exact JAR `cataclysm_spellbooks-1.1.13-1.21.jar` / SHA-1 `4af8348cc77bbff2ab7057c1fac26a5ab0a5b6a2`;
- isolated non-merge PR #188 materialized exact File ID `8792628` and hash-matched the physical artifact;
- 59 `Supplier<AbstractSpell>` fields, 59 `registerSpell(...)` calls, 59 spell-class instantiations and 0 conditional branches in the exact registry initializer;
- exact group distribution: 7 Abyssal + 4 Ender + 1 Evocation + 5 Holy + 11 Fire + 5 Ice + 4 Nature + 22 Technomancy = **59**;
- ten additional root localization keys have no current registered spell identity and remain excluded;
- semantic delta: **+59**, yielding strict counted minimum **874** and Iron ecosystem subtotal **527**;
- the generic/current publisher scale of 65 spells is not substituted for the installed 1.1.13 registry;
- numerical mechanics, acquisition, runtime QA and future integration seams remain separate/fail-closed;
- clean-room audit retained only factual identity/registry/resource evidence and copied no upstream implementation or assets.

See [`PHASE2BE-CATACLYSM-SPELLBOOKS-1.1.13-EXACT-CHECKPOINT.md`](./PHASE2BE-CATACLYSM-SPELLBOOKS-1.1.13-EXACT-CHECKPOINT.md).

## Phase 2BD — Alshanex's Familiars 4.0.3 component #54

Phase 2BD closes the current provider identity inventory against the exact physical artifact:

- exact JAR `alshanex_familiars-1.21.1_v4.0.3.jar` / SHA-1 `e5051c2385a426d05bf203ba8081a23d891f6686`;
- isolated Curse Maven download of exact File ID `8675568` hash-matched the physical artifact;
- 7 provider-owned spell registrations closed from exact registry/member/literal evidence;
- 11 packaged custom `alshanex_familiars:ritual_recipe` identities closed from exact structured resources;
- semantic delta: **+18**, strict counted minimum **815**;
- Sound/Melodic content remains owned/counted under Tunes n' Tomes and is not duplicated;
- runtime QA, numerical mechanics and future familiar adapter seams remain separately pending/fail-closed;
- clean-room audit retained only factual identity/registry/resource evidence and copied no upstream implementation or assets.

See [`PHASE2BD-ALSHANEX-4.0.3-EXACT-CHECKPOINT.md`](./PHASE2BD-ALSHANEX-4.0.3-EXACT-CHECKPOINT.md).

## Phase 2AY — GTBC's SpellLib 2.2.0 component #53, canonical

Phase 2AY closes the physically installed shared spell/addon library to the strongest current publisher evidence:

- physical artifact `gtbcs_spell_lib-2.2.0-1.21.1.jar`, mod id `gtbcs_spell_lib`, version `2.2.0`, physical SHA-1 `36cce8ab3117e89ae992a84a566d596709db2ffe`;
- exact CurseForge project/file `1194714 / 8824651` for the installed 2.2.0 line;
- publisher documentation defines SpellLib as reusable library/API infrastructure rather than standalone gameplay content;
- exact 2.2.0 release notes add Healing Received, Damage Taken and Summon Health attributes;
- reusable `AdvancedSpell`, imbuement, Curio, trade, particle and summon facilities are infrastructure consumed by addons and do not prove independent spell identities;
- semantic magic delta: **0**;
- no JAR decompilation or source copying was used; unsupported internal/API signatures remain fail-closed.

Iron's and consuming addons retain authority for their concrete spell/casting identities. Black Arcana retains authority for its own canonical casting, costs, targeting/effects, cooldowns/charges, hazards, rituals, Corruption, Strain, Arcane Danger, Backlash and WorldEffectPolicy.

## Phase 2AX — FamiliarsLib 1.7.1 component #52, canonical

Phase 2AX closes the installed familiar-framework library to the strongest currently available evidence:

- physical artifact `familiarslib-1.21.1-1.7.1.jar`, mod id `familiarslib`, runtime `1.21.1-1.7`, SHA-1 `7fa3f3116e35c12456425ae195924ced33fcc2eb`;
- CurseForge project/file `1316458 / 8059464`, release 2026-05-08 for NeoForge / Minecraft 1.21.1;
- official source repository `Alshanex/FamiliarsLib`;
- strongest release-correlated source commit `56561e7fd474fbd5c5166c1ac96f235faae156ab`, same date and same familiar-bed bug-fix intent as the 1.7.1 publisher changelog;
- correlated source tree `9d39b4751b9e52874f66cf2187afab239d00b251`, recursive `truncated=false`;
- source metadata declares Minecraft 1.21.1, NeoForge development baseline 21.1.90, Iron's `1.21.1-3.15.5`, Curios 9.2.2, mod version `1.21.1-1.7`;
- source owns serializable player-familiar attachment state and familiar lifecycle/storage/summon transport;
- `PayloadHandler` registers 17 optional payload handlers, split 9 play-to-server and 8 play-to-client;
- the tree contains spellcasting-familiar abstractions and Iron's spell classification tags, but no provider-owned spell registry or `data/familiarslib/spells/**` content;
- the 1.7 publisher changelog states that Sound-school content was removed and moved to Tunes n' Tomes;
- consequently FamiliarsLib contributes **0 independent semantic spell/magic objects** to the user-facing metric.

## Exactness and license boundary

FamiliarsLib's source commit is release-correlated, not cryptographically tied to the installed binary: no matching release tag or reproducible-build proof was established. Do not call it an exact source-to-JAR pin. Its observed license surfaces disagree, so no reuse conclusion is inferred. GTBC's SpellLib is treated conservatively as publisher/physical factual evidence only. Clean-room policy remains read-only factual inspection: no provider code/assets/text are copied or adapted.

## Black Arcana integration disposition

FamiliarsLib remains authority for its own familiar attachment/lifecycle/networking framework. Iron's remains authority for the external spells referenced by FamiliarsLib tags and casting interoperability. GTBC's SpellLib remains authority for its library facilities. Black Arcana remains authority for its own canonical magic runtime.

Stage 07.07 Borrowed Sight must not accept FamiliarsLib entities by thematic inference or generic tameable detection. A future bridge requires a verified provider-native ownership seam behind a dedicated adapter, with server-side revalidation and fail-closed behavior. Phase 2AX does **not** add that adapter, and Phase 2AY adds no runtime integration.

## Partial providers still receive zero component points

Examples remain:

- `not_enough_glyphs` — current physical line is 4.6.2; exact 4.6.2 source preserves the 4.6.1 registration and Momentum blobs byte-for-byte, so the existing 40-registration / 39-source-enabled matrix remains current. Those 39 candidates remain config-conditional because deployed SERVER overrides are unavailable;
- `somakespells` — current physical line is 1.0.9; the exact 1.0.8-fix 67-ID registry audit is historical only. Exact release/resource evidence for 1.0.9 is bounded, but physical byte equality, current registry, optional registration gates and survival/config reachability remain open;
- `gaze` — exact registry identity is closed, but 26 Spirit Rites remain conditional on the unavailable deployed COMMON `disableGazeRites` value.

These partials are also reasons the global semantic spell/magic denominator remains open. Their current conditional/open evidence is tracked explicitly in [`SEMANTIC-MAGIC-COVERAGE.md`](./SEMANTIC-MAGIC-COVERAGE.md) rather than being silently added to the strict semantic count.

## Update rule

After each provider closure:

1. re-read physical modlist and current `main`;
2. reconcile concurrent PR/branch ownership;
3. close the provider to the strongest exact evidence available;
4. preserve physical/publisher/source/license evidence layers when they differ;
5. keep semantic magic-object coverage separate from provider-component closure;
6. merge only after latest-main reconciliation and CI GREEN on the exact reconciled HEAD;
7. increment the canonical component numerator only after merge and post-merge main confirmation;
8. change either denominator only when evidence for that metric changes.

Phase 3 remains blocked until provider catalog/deduplication establishes real Black Arcana gaps and the semantic magic denominator is reconstructible.
