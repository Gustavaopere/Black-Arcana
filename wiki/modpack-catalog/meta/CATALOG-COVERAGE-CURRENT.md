# Current Magic Catalog Coverage

## User-facing semantic magic coverage

The principal percentage reported to the user is the coverage of **semantic magic objects**: spells, glyphs/spell-parts, rituals/rites and equivalent discrete magical actions. Provider count, JAR count, technical proxies, items, gear, familiars, affixes and machines do not substitute for that denominator.

The reconstructible semantic ledger lives in [`SEMANTIC-MAGIC-COVERAGE.md`](./SEMANTIC-MAGIC-COVERAGE.md). Phase 2BL raises the **strict counted minimum to 1316 semantic magic objects** by closing exact Goety Iron 3.1 (+14) and Goety Cataclysm 1.21.1-1.8.2 (+52) inventories without duplicating base-Goety ownership. Phase 2BM then closes Ars Polymorphia 1.0.3 as a source-pinned zero-semantic bridge with **+0**, Phase 2BN closes Ars Sable 1.1.2 as a source-pinned zero-semantic spatial/compat bridge with **+0**, Phase 2BO closes Farmer's Spell 'n Spellbooks 1.0.5.1 with **+6 `COUNTED_SOURCE_PINNED`**, and Phase 2BP closes SnackPirate's Aeromancy Additions 1.2.8 with **+10 `COUNTED_SOURCE_PINNED`**; Phase 2BQ then closes Ars Nouveau: Two-Way Portals 2.0.0 as exact hash-matched `ZERO_SEMANTIC_PORTAL_INFRA` with **+0**; Phase 2BR closes GTBC's Geomancy Plus 1.1.0-1.21.1 at **+12 `COUNTED_RELEASE_BOUNDED`** from the exact publisher-release registry plus provider/host reachability evidence; Phase 2BT closes Vampire Spells Addon 0.0.9 as source-pinned `ZERO_BRIDGE_INFRA` with **+0**. At the Phase 2BT checkpoint the strict minimum remained **1344**. The global denominator is still incomplete and no semantic percentage is declared.

## Structural provider-directory inventory — 27/09/2026

The canonical provider tree now contains **115 top-level provider directories = 100 ✅ + 15 ⚠️**. This count was obtained directly from `wiki/modpack-catalog/providers/` after consolidating the duplicate Vampiric Ageing directory pair that represented the same mod id `vampiricageing`, installed JAR and source pin.

This is a **repository catalog-structure metric only**. It does not regenerate the historical cross-domain component denominator, does not prove that 115 is the unique current physical-provider denominator, and must not be used to derive the semantic-magic percentage. The technical denominator remains `PENDING REBASE`; the semantic denominator remains open.

See [PROVIDER-DIRECTORY-INVENTORY.md](./PROVIDER-DIRECTORY-INVENTORY.md).

## Current reconciliation — 27/09/2026

Presence/version authority is the newest physical Project Library evidence plus newer sibling physical dossiers when they supersede that snapshot. At `neoforge-rpg-skilltree@8c6da384c68a557240522486f070b38edc87eca2`, the current modlist has **84 rows whose category field contains `Magic`**. After ownership normalization and the six newly mapped providers, **84/84** map to Black Arcana provider directories (**71 ✅ + 13 ⚠️**). The previous 67-row snapshot is historical.

The +17 physical-category delta contains eleven providers that were already cataloged and six newly materialized providers: Reliquified L_Ender's Cataclysm, ShadowsZ, Simply Swords: Cataclysm, Simply More, Simply Swords and Waystones. Reliquified L_Ender's Cataclysm 0.1.1 is ✅ `COUNTED_EXACT 7`. The other five new providers remain ⚠️. ShadowsZ 1.1.9 has an exact hash-matched **10-action semantic inventory** but stays +0 strict because effective attunement restriction and Fusion deployment state are not captured. Simply More Alpha 5 now has an exact hash-matched **24-action current-pack denominator** (10 active API + 13 legacy direct-use + 1 shared Mimicry), but stays +0 strict while deployed Awakening/acquisition/Mimicry/config reachability is unresolved. Category reclassification itself does not create semantic objects; the Reliquified +7 comes from its separate exact semantic closure. Current blockers are recorded in [PHYSICAL-MAGIC-RECONCILIATION-2026-09-27.md](./PHYSICAL-MAGIC-RECONCILIATION-2026-09-27.md) and [CONDITIONAL-PROVIDER-CLOSURE.md](./CONDITIONAL-PROVIDER-CLOSURE.md). The global cross-domain set remains larger than this physical-category subtotal.

Semantic effect of the current reconciliation:

- 27/09 physical-category expansion 67→84: **+0 strict at mapping time**; eleven rows were already represented and six new provider mappings initially entered fail-closed. Reliquified L_Ender's Cataclysm has since closed exact at **+7 strict**, leaving five of those six mappings partial; ShadowsZ is now inventory-exact at 10 but still active-state conditional.

- Companions! 1.3.4: **+9 `COUNTED_SOURCE_PINNED`** Magic Book actions.
- Crystal Chronicles 0.1.3-alpha: **+1 `COUNTED_SOURCE_PINNED`** (`crystal_chronicles:prismatic_portal`).
- Relics 0.12.8: **+41 `COUNTED_EXACT`** — 39 base abilities + 2 owner-scoped synergies.
- Corail Tombstone 9.5.6: **+10 `COUNTED_EXACT`** — six prayers + four Ritual Flute actions; 12 more action families remain config-conditional.
- Ender's Spells and Stuff: Requiem 0.1.7: **+53 `COUNTED_SOURCE_PINNED`**.
- Hexalia 1.3.7: current semantic surface **29 = 23 Nature's Ritual + 6 Celestial Infusion**, a **+4** delta over the previously counted 25.
- Reliquified Ars Nouveau 0.8.1: **+19 `COUNTED_SOURCE_PINNED`**.
- Reliquified Artifacts 1.0.8: **+52 `COUNTED_SOURCE_PINNED`**.
- Reliquified Iron's Spells 'n Spellbooks 0.2.7: **+25 `COUNTED_SOURCE_PINNED`**.
- Reliquified L_Ender's Cataclysm 0.1.1: **+7 `COUNTED_EXACT`** — exact publisher/physical SHA-1 equality plus bounded exact-artifact registry/declaration reconciliation.
- Ars 'n' Spells 3.3.4: **+0 version delta**; five ritual identities remain counted, with current state `COUNTED_RELEASE_BOUNDED`.
- Cataclysm: Spellbooks 1.1.14: **+0 current delta**, retaining 59 already-counted identities with stronger exact evidence.
- Acolyte, Dungeon's Delight, Fantasy Armor, Enchantment Descriptions, A Good Place, Create: Apokinetics, Photon, RunicLib, Immersive Portal Iron's bridge, Iron's Recolor, Spell Actionbar and Specs: **+0 independent semantic objects** under the current metric. The four UI/compat providers are now ✅ cataloged at zero semantic identities; their technical/runtime QA remains separate.
- More Relics 1.7.7-forRelics-0.12.8-1.0 is now **✅ `COUNTED_EXACT` / +61 strict** after NON-MERGE exact-artifact audit #409 hash-matched File `8859015` and closed 61 owner-scoped ability roots. Traveloptics 4.4.0.1-1.21.1 remains current **⚠️ / +0 strict pending closure**; its old 33-spell publisher baseline is not promoted into the exact current physical numerator.
- Ozymandias Sundries physical 0.0.5 / embedded metadata 0.0.1 is now **✅ `COUNTED_EXACT` / +2 strict** after exact-artifact run `36286741917` hash-matched File `6978561`; the exact registrar has two unconditional registrations (`levitate`, `lightning_warp`), zero initializer branches and zero packaged Iron's spell-config override paths. Unregistered spell classes/localization residue are excluded.
- Mowzie's Mobs 1.8.2 is now **⚠️ / +10 `COUNTED_EXACT` strict + 1 `CONDITIONAL`** after exact-artifact run `36288758348` hash-matched File `7760267`; the exact active array has 13 player-ability slots. Ten independent powers are strict-counted, `tunneling` remains config-conditional on deployed `enableTunneling`, `hit_boulder` and `backstab` are technical/subaction slots, and four declared ids are inactive.
- Ice And Fire Community Edition 2.1.2 is now **⚠️ / +8 `COUNTED_EXACT` strict + 1 `CONDITIONAL`**. Exact reachability run `36323035696` closes seven provider-data routes; exact current-pack NeoForge 21.1.250 runtime audit `36327488231` closes Dread Lich Staff inherited equipment-drop reachability. Ghost Sword has exact acquisition but deployed `tools.phantasmalBladeAbility` remains unresolved.
- Mowzie's Cataclysm 1.2.2, Pickable Orbs 1.21.1-1.0.0, IronSable X Wind's Spellbooks 1.0.0, Iron's Gems 'n Jewelry 1.21.1-2.0.2 and Integrated Villages 1.3.3+1.21.1-neoforge are now **✅ exact zero-semantic closures / +0 strict each**. Their exact artifacts respectively close locator Eyes, pickup-effect entities, an existing-spell physics bridge, equipment proc payloads and worldgen/structure integration without minting independent player magic identities.
- Somake 1.0.9 remains **⚠️ / +0 strict** with 83/83 current registrations structurally closed but deployed config/reachability open.
- Iron's Spellbooks KubeJS and KubeJS Ars Nouveau have **+0 fixed built-in identities**, while current pack-script mutation/registration inventories remain open.

The strict reconstructible semantic minimum is therefore **1684**. The semantic denominator and the global cross-domain technical denominator remain incomplete; no percentage is declared.

## Current provider override — Hazen N Stuff 1.4.0.14

The sibling physical re-audit at `neoforge-rpg-skilltree@7028524829b5589ee377cd980aa8298cf95cf5c7` certifies `hazennstuff-1.4.0.14.jar` / mod id `hazennstuff` / runtime `1.4.0.14` / physical SHA-1 `3be20bacb44c1923348ab6f61b685eec6aacfdcd`. Exact public source pin `Hazentouvel/Hazen_N_Stuff@5fcaf39cf399609f6c1c87d14f8d4807098c9cce` declares the same provider version and closes **38 active Iron's spell registrations**. The same release localization has 41 root spell keys: `brimstone_hellblast` and `supernova` have no active registry entry, while `reign_of_tyros` has a source class/localization root but its registration line is commented; all three are excluded. Registry-level source inspection finds no conditional registration/config/mod-presence branch around the 38 active identities. Thirty-five spells inherit host/default crafting gates; Golden Shower, Night's Edge Strike and Scorching Slash have provider-specific inventory gates whose required provider items have exact release crafting paths. Custom Cosmic/Radiance/Shadow/Hydro focus routing is also source-reconciled against the current HazentouveLib 1.0.9 / Ace's Spell Utils infrastructure. Therefore Hazen contributes **+38 `COUNTED_SOURCE_PINNED`**, raising the strict reconstructible minimum at that checkpoint from **1344 to 1382**. Runtime compatibility remains fail-closed.

The old technical `68/100` component ratio is now a **historical checkpoint**, not a current denominator claim: the 22/09 sibling physical re-audit has surfaced magic components not represented in that older 100-component baseline. Hazen closes the next known provider component, but the denominator must be regenerated from the current physical modlist before another fraction or percentage is published. See [Hazen N Stuff](../providers/%E2%9C%85-hazen-n-stuff/README.md) and [its source-pinned inventory](../providers/%E2%9C%85-hazen-n-stuff/SOURCE-1.4.0.14-SPELL-INVENTORY.md).

## Current provider override — Create: Wizardry 1.21.1-0.5.1-pre1

The current sibling physical index at `neoforge-rpg-skilltree@7028524829b5589ee377cd980aa8298cf95cf5c7` certifies physical row **#166** as `create_wizardry-1.21.1-0.5.1-pre1.jar` / mod id `create_wizardry` / runtime `1.21.1-0.5.1-pre1`. Exact official public source pin `TTZPlayz/Create-Wizardry@9c4e53aad0ee9477187487443b597b77ef06f323` declares the same version line. No independent installed-JAR hash is retained for this row, so byte equality is not claimed.

Bounded source inspection closes the semantic ownership question: no provider spell registry/resource surface is present, while Blaze Caster and Mana Siphon consume existing Iron's spell/mana contracts. Create: Wizardry is therefore **✅ cataloged** as `ZERO_SEMANTIC_HOST_SPELL_AUTOMATION` with **+0** independent semantic magic objects. At that provider checkpoint, the strict reconstructible minimum remained **1382**. Runtime automation/resource settlement remains fail-closed. See [Create: Wizardry](../providers/%E2%9C%85-create-wizardry/README.md) and [its source-pinned magic-surface audit](../providers/%E2%9C%85-create-wizardry/SOURCE-1.21.1-0.5.1-PRE1-MAGIC-SURFACE.md).


## Current provider override — Iron's Apothic 2.2.2

The current sibling certified row at `neoforge-rpg-skilltree@7028524829b5589ee377cd980aa8298cf95cf5c7` records `irons_apothic-2.2.2.jar` / mod id `irons_apothic` / runtime `2.2.2` at row #339. Exact official source pin `muon-rw/Apotheosis-Irons-Spells@c5d501219cc9bbbfb8c69acc08bebac76983d1c1` declares the same version and closes the provider's magic surface as a bridge over Iron's and Apotheosis/Apothic.

The exact source registers 7 custom affix codecs, contains 140 affix definitions, 48 explicit spell/imbued-spell affix definitions and 24 gem definitions. Spell-trigger codecs resolve external holders from Iron's `SpellRegistry`; no provider-owned spell registry is established. Iron's Apothic is therefore **✅ cataloged** with **+0 independent semantic magic objects**, leaving the strict minimum at **1382** at that provider checkpoint. The current technical denominator remains `PENDING REBASE`, so this closure is not assigned a new `N/100` component fraction. Runtime proc/cooldown/targeting and version-drift QA remain fail-closed.

See [Iron's Apothic](../providers/%E2%9C%85-irons-apothic/README.md), [exact source magic-surface inventory](../providers/%E2%9C%85-irons-apothic/SOURCE-2.2.2-MAGIC-SURFACE.md), and the narrow queue/capability overlays.

Phase 2BS — T.O Magic n' Extras / Traveloptics 4.4.0.1-1.21.1 — remains the historical publisher-artifact audit: exact File `6342780` closes 33 registered spell identities and excludes 32 residual localization-only roots, with `blackout` reachability unresolved and suspicious loot-modifier codec wiring. Newer physical Project Library authority now confirms Traveloptics is **currently installed** at the same version line with SHA-1 `7b74816e89cc15dd0b5a31d9ea1e456024e8fae4`; that digest differs from both the audited publisher alpha and known patch artifact, so the provider is current **⚠️ `OTHER_VERIFIED` / +0 strict** until the installed bytes/current registry are closed. See [`../providers/⚠️-traveloptics/README.md`](../providers/⚠️-traveloptics/README.md).

Phase 2BT — Vampire Spells Addon 0.0.9 — has semantic delta **+0** and closes technical component **#67**. Official release `1.21.1-0.0.9` and exact source target `xsharov/VampireSpellsAddon@2d36e94e67611a316b7311b11e4574b499025580` show a compatibility/runtime-policy overlay over Iron's + Vampirism: spell/school identifiers belong to `irons_spellbooks`, integration is installed through bridge/listener surfaces, and no provider-owned spell, school, ritual or equivalent action registrar is established. PR #239 merged the durable audit as `main@1c5091807a8773d378c34ffac2e737b5f08b545c`, and the exact merge SHA passed Black Arcana CI run `34795795283` GREEN. The strict semantic minimum remains **1344** while technical component closure becomes **67/100**. Runtime bridge behavior, effective config and physical byte equality remain separate fail-closed gates. See [`../providers/✅-vampire-spells-addon/RELEASE-SOURCE-0.0.9-AUDIT.md`](../providers/✅-vampire-spells-addon/RELEASE-SOURCE-0.0.9-AUDIT.md).

Mobstein `5.4.4` is now a durable zero-semantic catalog closure. PR #318 was squash-merged as `main@73cd692ac0f6aa96ee1a6c422f09d0fcc648c8f4`; exact-SHA post-merge Black Arcana CI **#3217** / run `35293505012` completed GREEN, including canonical verification and the Stage 05 companion dedicated-server smoke. Exact physical SHA-1 `3672d88f940ddd474a5429d7066b099cd0ce0c29` plus the successful resource-only clean-room audit closes Mobstein as `ZERO_SEMANTIC_ACTIONS` with **+0** semantic objects. At that historical checkpoint, this shared reconciliation closed technical provider component **#68 / 68 of 100** while the strict semantic minimum remained **1344**. Runtime/API/Sable integration remains fail-closed and is not a catalog blocker.

**Current Somake override — 1.0.9.** Current sibling authority `neoforge-rpg-skilltree@7028524829b5589ee377cd980aa8298cf95cf5c7` retains `somakespells-1.0.9-1.21.1.jar` / runtime `1.0.9`. Physical Project Library SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0` equals exact publisher CurseForge File `8867079`, so physical↔publisher equality is closed. Exact clean-room structural evidence closes **83 unique registry IDs**, **67 unconditional + 16 optional-provider-gated** registrations, and the object-level gate map. The current pack contains Mowzie's Mobs, ISS: Magic From The East and Legendary Monsters, so Somake's own registration predicates admit **83/83** declared IDs. Exact provider code default for `enableSpellLockSystem` is `false`. PR #393 additionally materialized all **83 current IDs** as individual cards under `registry-1.0.9/`.

This does **not** promote Somake into the strict numerator. Effective deployed Iron's `enabled` / `allow_crafting`, the deployed Somake `enableSpellLockSystem` value and survival acquisition/reachability remain unavailable as authoritative current-pack facts. Somake therefore stays **⚠️ conditional / +0**, with registry identity/composition no longer open. Historical 1.0.8-fix registry text below remains historical only.

Phase 2BR has a semantic delta of **+12 `COUNTED_RELEASE_BOUNDED`**: exact publisher release file `7041615` closes twelve unconditional `GGSpells` registrations — ten Geo and two Holy — while `EarthshatterSpell` is present but unregistered and the non-registry adaptation classes add zero provider identities. The repository does not preserve an independent local physical-JAR hash, so this is release-bounded rather than `COUNTED_EXACT`. A dedicated exact-release audit proves all ten registered Geo classes inherit Iron's `allowCrafting`, `isEnabled` and `canBeCraftedBy` host gates; exact Geo focus data plus the canonical Iron's Scroll Forge contract close catalog-level Geo reachability, while exact Umvuthi loot identifiers and the exact file changelog close catalog-level acquisition for `solar_beam` and `solar_storm`. This shared reconciliation raises the strict minimum to **1344** and closes provider component **#66**, while assembled-pack runtime/config/protection behavior remains fail-closed. See [`../providers/✅-gtbcs-geomancy-plus/README.md`](../providers/✅-gtbcs-geomancy-plus/README.md), [`../providers/✅-gtbcs-geomancy-plus/EXACT-1.1.0-ARTIFACT-AUDIT.md`](../providers/✅-gtbcs-geomancy-plus/EXACT-1.1.0-ARTIFACT-AUDIT.md) and [`PHASE2BR-GTBC-GEOMANCY-PLUS-1.1.0-EXACT-CHECKPOINT.md`](./PHASE2BR-GTBC-GEOMANCY-PLUS-1.1.0-EXACT-CHECKPOINT.md).

Phase 2BQ has a semantic delta of **0**: exact hash-matched `ars_two_way_portals-2.0.0.jar` contains portal/compat infrastructure, two provider items, three recipes and seven required mixins, but no independent spell/glyph/ritual/rite/ability registry or semantic resource surface. It is classified `ZERO_SEMANTIC_PORTAL_INFRA`; the strict semantic minimum stays **1332** while this shared reconciliation closes provider component **#65**. Runtime portal lifecycle, effective config, mixin application and assembled-host Immersive behavior remain fail-closed. See [`../providers/✅-ars-two-way-portals/README.md`](../providers/✅-ars-two-way-portals/README.md), [`../providers/✅-ars-two-way-portals/EXACT-2.0.0-ARTIFACT-AUDIT.md`](../providers/✅-ars-two-way-portals/EXACT-2.0.0-ARTIFACT-AUDIT.md) and [`PHASE2BQ-ARS-TWO-WAY-PORTALS-2.0.0-EXACT-CHECKPOINT.md`](./PHASE2BQ-ARS-TWO-WAY-PORTALS-2.0.0-EXACT-CHECKPOINT.md).

Phase 2BP has a semantic delta of **+10 `COUNTED_SOURCE_PINNED`**: physical `aero_additions-1.2.8.jar` / SHA-1 `dee32c9fa84d6e39846608f8f77591ea56f` is reconciled with exact public source pin `snackerpirater/aero-additions@ae282b32d25ad76ef8d01c637ec05566a767ae4c`, which closes exactly ten active unconditional Wind `AbstractSpell` registrations. Five commented-out registrations are excluded. Provider Wind focus data plus the Iron's 3.16.3 Scroll Forge contract close a host-native Breeze Rod catalog acquisition route; provider loot modifiers also add Breeze Rod support to Trial Chamber normal-vault rewards. This closes provider component **#64** while keeping assembled-pack runtime compatibility fail-closed. See [`../providers/✅-aeromancy-additions/README.md`](../providers/✅-aeromancy-additions/README.md) and [`PHASE2BP-AEROMANCY-CHECKPOINT.md`](./PHASE2BP-AEROMANCY-CHECKPOINT.md).

Phase 2BO has a semantic delta of **+6 `COUNTED_SOURCE_PINNED`**: physical `farmers-spell-n-spellbook-1.0.5.1-1.21.1.jar` / SHA-1 `f77355e029af39bbaba3854e10cc087a608351ff` is reconciled with exact public source pin `GLDYM/Farmers-Spell-n-Spellbook@b7cbb40316a9ccbbc2ce2b56b3023647261ce569`, which closes exactly six unconditional Gluttony `AbstractSpell` registrations. Provider Gluttony focus data plus the Iron's 3.16.3 Scroll Forge contract close a host-native catalog acquisition route; generic random scroll loot is not claimed because the school sets `allowLooting=false`. This closes provider component **#63** while keeping current-host runtime compatibility fail-closed. See [`../providers/✅-farmers-spell/README.md`](../providers/✅-farmers-spell/README.md) and [`PHASE2BO-FARMERS-SPELL-CHECKPOINT.md`](./PHASE2BO-FARMERS-SPELL-CHECKPOINT.md).

Phase 2BN has a semantic delta of **0**: exact official source pin `baileyholl/ars-sable@1fd83f3a998e3a41b5a21d0d6529140a0b0a55ba` closes the provider's role as a narrow Ars Nouveau ↔ Sable spatial/sublevel compatibility layer. The exact source has 24 common + 5 client required mixins, protocol registrar version `2`, zero provider-owned payload registrations, and no provider-owned spell/glyph/ritual/school/resource/action registry. This closes provider component **#62** while keeping current-host runtime compatibility fail-closed. See [`../providers/✅-ars-sable/README.md`](../providers/✅-ars-sable/README.md) and [`PHASE2BN-ARS-SABLE-CHECKPOINT.md`](./PHASE2BN-ARS-SABLE-CHECKPOINT.md).

Phase 2BM has a semantic delta of **0**: exact official source pin `Vonr/Ars-Polymorphia@e09b6c9ab434ccbb3232ca47b37ca5666becfb6f` closes the provider's role as an Ars Storage/Crafting Lectern ↔ Polymorph recipe-conflict bridge, without a provider-owned spell, glyph, ritual, school, mana/resource or equivalent magical-action registry. This closes provider component **#61** while keeping current-host runtime compatibility fail-closed. See [`../providers/✅-ars-polymorphia/README.md`](../providers/✅-ars-polymorphia/README.md) and [`PHASE2BM-ARS-POLYMORPHIA-CHECKPOINT.md`](./PHASE2BM-ARS-POLYMORPHIA-CHECKPOINT.md).

Phase 2BK has a semantic delta of **0**: exact hash-matched Ignis Soulfires: Spellbooks 1.1.0 contains only its armor-material/item bridge surfaces and no provider-owned spell, ritual, rite or equivalent action registry. This closes provider component **#58** without changing the semantic numerator. See [`../providers/✅-ignis-soulfires-spellbooks/EXACT-1.1.0-ARTIFACT-AUDIT.md`](../providers/✅-ignis-soulfires-spellbooks/EXACT-1.1.0-ARTIFACT-AUDIT.md).

The latest semantic promotion before Phase 2BL was **Gaze +1**. Exact hash-matched 1.1.7.1 artifact evidence closes one Gaze-owned Iron's standalone spell identity, Soulward Shield, with the optional Iron's provider gate satisfied by the physical pack. The same artifact closes 26 player-facing Spirit Rite identities, but they remain `CONDITIONAL` because the deployed COMMON `disableGazeRites` value is unavailable; two Geas effect types and eight rune items are metric-excluded. See [`../providers/⚠️-gaze/EXACT-1.1.7.1-ARTIFACT-AUDIT.md`](../providers/⚠️-gaze/EXACT-1.1.7.1-ARTIFACT-AUDIT.md).

The preceding semantic promotion is **Goety +361**. Exact hash-matched 3.1.4 artifact evidence closes 123 active/acquirable Focus actions and 238 available distinct non-Focus ritual actions after semantic deduplication and physical-provider condition filtering. Runtime/API/balance and provider-owned settlement remain separate fail-closed gates. See [`../providers/✅-goety/EXACT-3.1.4-ARTIFACT-AUDIT.md`](../providers/✅-goety/EXACT-3.1.4-ARTIFACT-AUDIT.md).

The preceding semantic promotion is **Leyline Spellbooks +14**. Exact hash-matched 1.0.3 artifact evidence closes 14 unconditional provider spell registrations; no Leylines-specific spell lock or conditional registration gate is present, while generic Iron's host config remains separate runtime QA. See [`../providers/✅-leyline-spellbooks/EXACT-1.0.3-ARTIFACT-AUDIT.md`](../providers/✅-leyline-spellbooks/EXACT-1.0.3-ARTIFACT-AUDIT.md).

The preceding semantic promotion is **Cataclysm: Spellbooks +59**. Exact hash-matched 1.1.13 artifact evidence closes 59 unconditional provider spell registrations; ten additional root localization identities are not registered in the installed artifact and remain excluded. The generic/current 65-spell publisher scale is not substituted for the physical 1.1.13 registry. See [`../providers/✅-cataclysm-spellbooks/EXACT-1.1.13-ARTIFACT-AUDIT.md`](../providers/✅-cataclysm-spellbooks/EXACT-1.1.13-ARTIFACT-AUDIT.md).

The preceding semantic promotion is **Alshanex's Familiars +18**. Exact hash-matched 4.0.3 artifact evidence closes seven provider-owned spell registrations and eleven packaged custom `alshanex_familiars:ritual_recipe` identities. Sound/Melodic content remains counted only under Tunes n' Tomes, while familiar AI/passives and external Iron's spell casts remain excluded. See [`../providers/✅-alshanex-familiars/EXACT-4.0.3-ARTIFACT-AUDIT.md`](../providers/✅-alshanex-familiars/EXACT-4.0.3-ARTIFACT-AUDIT.md).

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
- semantic numerator delta from Relics 0.12.8 exact ability/synergy closure: **+41**;
- semantic numerator delta from Goety Iron 3.1 exact closure: **+14**;
- semantic numerator delta from Goety Cataclysm 1.21.1-1.8.2 exact closure: **+52**;
- semantic numerator delta from Ender's Spells and Stuff: Requiem 0.1.7 source-pinned closure: **+53**;
- semantic numerator delta from Hexalia 1.3.7 current release-source reconciliation: **+4**;
- semantic numerator delta from Reliquified Ars Nouveau 0.8.1 source-pinned closure: **+19**;
- semantic numerator delta from Reliquified Artifacts 1.0.8 source-pinned closure: **+52**;
- semantic numerator delta from Reliquified Iron's Spells 'n Spellbooks 0.2.7 source-pinned closure: **+25**;
- semantic numerator delta from More Relics 1.7.7-forRelics-0.12.8-1.0 exact-artifact ability closure: **+61 `COUNTED_EXACT`**;
- semantic numerator delta from Ozymandias Sundries physical 0.0.5 exact-artifact closure: **+2 `COUNTED_EXACT`**;
- semantic numerator delta from Mowzie's Mobs 1.8.2 exact-artifact closure: **+10 `COUNTED_EXACT`**; one additional Tunneling power remains conditional;
- semantic numerator delta from Ice And Fire CE 2.1.2 exact-artifact/current-runtime reachability closure: **+8 `COUNTED_EXACT`**; only Ghost Sword remains conditional;
- semantic numerator/denominator delta currently attributable to current-physical Traveloptics: **+0 strict pending installed-byte registry closure**;
- semantic numerator delta from Reliquified L_Ender's Cataclysm 0.1.1 exact-artifact closure: **+7 `COUNTED_EXACT`**;
- strict reconstructible semantic minimum: **1684**;
- the global semantic denominator remains incomplete because other providers still have open granular inventories;
- **do not derive a spell/magic percentage from the provider-component metric below**.

The preceding semantic-only promotion was **Malum +26**: whole-interval path history across the observed `1.8.2` source window plus stable endpoint blobs close 26 base-Malum `SpiritRiteType` identities. Release-bounded Codex evidence separately proves the two special identities player-facing; Geas/resource/effect registries remain metric-excluded. Hexalia's earlier 1.3.6 checkpoint contributed **25**, but the current 1.3.7 release-source audit expands that same provider surface to **29** with four additional Nature's Ritual identities. These semantic promotions do not by themselves close the global provider-component denominator.

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

Exact 3.1.4 artifact identity closes **+361** and component #57. Durable PR #198 clean HEAD `d75f82a23b5c977ccc8ec84813bf89c928ffc0ab` passed Black Arcana CI #2523 / run `34672038273`; squash merge `4fcc40aaf8149b5511dbd882a5616ee5240cd640` passed exact-SHA post-merge CI #2524 / run `34672222798` and published the canonical QA JAR. See `PHASE2BH-GOETY-3.1.4-EXACT-CHECKPOINT.md` and `../providers/✅-goety/EXACT-3.1.4-ARTIFACT-AUDIT.md`. Canonical totals are **1249 / 57/100** at that historical checkpoint.

## Phase 2BG — Leyline Spellbooks 1.0.3 component #56, canonical

Exact hash-matched Leylines 1.0.3 evidence closes 14 unconditional registered spells and removes the provider-specific eligibility blocker; exact Iron's host defaults/scroll behavior corroborate normal reachability while deployed generic host config remains separate runtime QA. Leylines is now **+14 semantic objects**, the Iron subtotal is **541**, the strict minimum is **888**, and provider component **#56 / 56/100** is canonical at that checkpoint.

Durable PR #195 clean HEAD `a9d7b55044230bbb011f7233ffd75d9a8321489b` passed Black Arcana CI **#2503** / run `34668329229`. Squash merge `88f042f68429ff920314a7ec3a6923369edc93fd` passed exact-SHA post-merge CI **#2504** / run `34668535721`, including canonical QA-JAR publication. Numerical balance, complete-modpack runtime QA and any Black Arcana adapter/API seam remain separate fail-closed gates.

## Internal provider-component closure metric

**Historical provider-component checkpoint after the Mobstein 5.4.4 shared reconciliation: 68/100 = 68%. The current denominator is `PENDING REBASE` and this fraction must not be published as current coverage.**