# T.O Magic n' Extras 4.4.0.1-1.21.1 — exact-release partial semantic closure

## Status

`HISTORICAL PHASE 2BS CHECKPOINT / NO CURRENT STATUS-PREFIXED PHYSICAL ROW / LEGACY EXPORT DOSSIER RETAINED / FORMER PHYSICAL OTHER_VERIFIED SHA-1 / 33-ID PUBLISHER-BASELINE REGISTRY / STRICT +0 HISTORICAL`

Current physical status: **NO CURRENT STATUS-PREFIXED/CATEGORIZED PHYSICAL ROW / NOT A CURRENT PROVIDER BLOCKER** at sibling `neoforge-rpg-skilltree@76cf13e7d1110116f67c290eaa15891888279fc1`. A legacy uncategorized export dossier remains under `PROJECT-INSTRUCTIONS/modlist/to-magic-n-extras.md` and explicitly uses the older 595-mod physical snapshot.

The former Phase 2BS state remains **⚠️ partial/conditioned historical evidence** for the old 4.4.0.1 line. It is retained for provenance and future reintroduction audits, not counted as an unresolved provider in the current pack.

## Historical installed authority

- provider: **T.O Magic n' Extras**
- mod id: `traveloptics`
- physical version line: `4.4.0.1-1.21.1`
- installed filename observed by the physical-pack evidence: `traveloptics-4.4.0.1-1.21.1.jar`
- Minecraft / loader: Minecraft `1.21.1`, NeoForge `[21.1.0,)`
- CurseForge project / exact file: `1046916 / 6342780`
- Curse Maven: `curse.maven:to-tweaks-irons-spells-1046916:6342780`
- exact publisher-release SHA-1: `3808493ce45cdfeb6408e85578adecf13df698e8`
- exact publisher-release SHA-256: `0372b4b8593288726fb0d6e8cdb86202a87677d0c2dafeb96cab50bf057ec298`
- publisher license: **All Rights Reserved**
- required artifact dependencies declared by the exact JAR: Iron's Spells 'n Spellbooks `[1.21.1-3.10.0,)`, L_Ender's Cataclysm `[2.60.,)`, Apothic Attributes `[2.6.1,)`

Historical sibling checkpoint `neoforge-rpg-skilltree@4d9710dc0c9bf17e1fdaef29e48d843de80288d0` recorded `traveloptics-4.4.0.1-1.21.1.jar`. A later hash-bearing Project physical checkpoint dated 2026-09-16 fingerprinted that installed filename at SHA-1 `7b74816e89cc15dd0b5a31d9ea1e456024e8fae4`. Current sibling `neoforge-rpg-skilltree@76cf13e7d1110116f67c290eaa15891888279fc1` contains no current status-prefixed/categorized Traveloptics physical row; the remaining uncategorized `to-magic-n-extras.md` file is an older 595-mod export dossier, so those physical statements are historical rather than current. That value differs from both exact publisher File `6342780` SHA-1 `3808493ce45cdfeb6408e85578adecf13df698e8` and known patch File `8861368` SHA-1 `680fa679d8ea2419a79571f455436367222f6f9d`. Physical disposition is therefore `OTHER_VERIFIED`: the installed bytes are a third artifact/repack/replacement whose content delta is not yet materialized. The 33-ID File-6342780 inventory remains an exact publisher baseline, **not** an exact-current-physical registry claim. See [`PHYSICAL-4.4.0.1-FINGERPRINT-CHECKPOINT.md`](PHYSICAL-4.4.0.1-FINGERPRINT-CHECKPOINT.md).

## Publisher release boundary

The exact CurseForge file is explicitly published as a deprecated alpha for 1.21.1. Its file notes state that only part of the 1.21 content was ported, that Cataclysm-based spells/some items were among the ported surfaces, that the ported spells are intended to be obtainable in survival, and that Alex's Caves content is absent from this build.

Those publisher statements are release-line context, not a registry inventory. The exact JAR still carries localization roots for content not registered by this 1.21.1 alpha, so marketing text and translation keys are never projected backward into the current registry.

## Exact registry closure

Clean-room inspection of exact file `6342780` closes `com.gametechbc.traveloptics.init.TOSpells` at:

- **33** unique `Supplier<AbstractSpell>` registration fields;
- **33** `registerSpell(...)` calls;
- **0** branch opcodes in the registry static initializer;
- **33** unique concrete provider spell classes instantiated by that initializer;
- **33** unique `traveloptics:<id>` registry identities mapped field -> class -> ID;
- **65** root `spell.traveloptics.<id>` localization identities, of which **32 are residual/unregistered** in this exact alpha and add **0**.

The two additional `AbstractSpell` descendants are provider base classes, `AbstractUniqueSpell` and `AbstractWeaponSpell`; they are not standalone registrations.

### Registered spell identities — 33

Blood:

- `traveloptics:blood_howl`

Eldritch:

- `traveloptics:abyssal_blast`
- `traveloptics:blackout`
- `traveloptics:psychic_bolt`
- `traveloptics:reversal`
- `traveloptics:spectral_blink`

Ender:

- `traveloptics:eternal_sentinel`
- `traveloptics:orbital_void`
- `traveloptics:cursed_minefield`
- `traveloptics:void_eruption`
- `traveloptics:vortex_punch`
- `traveloptics:astral_sense`

Evocation:

- `traveloptics:ashen_breath`
- `traveloptics:lingering_strain`

Fire:

- `traveloptics:ignited_onslaught`
- `traveloptics:burning_judgment`
- `traveloptics:meteor_storm`
- `traveloptics:lava_bomb`
- `traveloptics:gyro_slash`

Holy:

- `traveloptics:nullflare`
- `traveloptics:summon_desert_dwellers`
- `traveloptics:sword_of_the_ancients`

Ice:

- `traveloptics:axe_of_the_doomed`
- `traveloptics:cursed_revenants`
- `traveloptics:despair`
- `traveloptics:halberd_horizon`
- `traveloptics:cursed_blast`

Lightning:

- `traveloptics:mechanized_predator`
- `traveloptics:rapid_laser`
- `traveloptics:death_laser`
- `traveloptics:em_pulse`

Nature:

- `traveloptics:aerial_collapse`
- `traveloptics:stele_cascade`

The exact field/class mapping is preserved in [`EXACT-4.4.0.1-ARTIFACT-AUDIT.md`](EXACT-4.4.0.1-ARTIFACT-AUDIT.md).

## Residual localization identities — excluded

The following 32 root localization IDs exist in the exact alpha but are absent from its exact spell registry and therefore contribute **+0**:

`annihilation`, `aqua_missiles`, `berserker`, `bubble_spray`, `call_forth_the_dead_king`, `coral_barrage`, `dawns_favor`, `earthshatter`, `echo_of_the_abyss`, `eek`, `extinction`, `flood_slash`, `floodgate`, `hydroshot`, `jet_steam`, `magnetron_deployment`, `nocturnal_swarm`, `primal_pack`, `primordial_steed`, `rainfall`, `shadowed_miasma`, `solar_flare`, `sticky_steed_summon`, `sunbeam`, `tectonic_rift`, `the_forgotten_beast`, `tidal_grasp`, `tsunami`, `vigor_siphon`, `violent_skreech`, `void_devourer`, `vortex_of_the_deep`.

This exclusion is important because the publisher itself describes the 1.21.1 line as only partially ported.

## Craftability and acquisition evidence

Provider-owned ancestry divides the 33 registrations into three relevant groups:

- 21 registrations do not declare a provider-owned `allowCrafting`, `isEnabled` or `canBeCraftedBy` override and inherit Iron's host gates;
- 10 registrations inherit `AbstractUniqueSpell.allowCrafting() = false`;
- 2 registrations inherit `AbstractWeaponSpell.allowCrafting() = true`: `cursed_blast` and `gyro_slash`.

Nine of the ten non-craftable Unique spells have direct exact structured loot references in the JAR:

- `abyssal_blast` — Leviathan loot;
- `axe_of_the_doomed` — Aptrgangr loot;
- `burning_judgment` — Ignis loot;
- `eternal_sentinel` — Ender Golem loot;
- `halberd_horizon` — Maledictus loot;
- `ignited_onslaught` — Ignited Berserker / Ignited Revenant loot;
- `mechanized_predator` — Prowler / Watcher loot;
- `summon_desert_dwellers` — Koboleton / Wadjet loot;
- `sword_of_the_ancients` — Kobolediator loot.

`traveloptics:blackout` is the unresolved exception. It inherits `AbstractUniqueSpell.allowCrafting() = false`, has no direct structured-data reference in the exact artifact, and the focused class-reference audit found no provider-owned reference to `TOSpells.BLACKOUT_SPELL` outside `TOSpells` itself. The publisher's generic statement that ported spells are obtainable in survival is not specific enough to manufacture an object-level Blackout route.

The current broad project description documents a Dead King → Blackout route for the full project, while official 1.20.1 File `6010839` introduced `Blackout`, `Call Forth The Dead King` and `Enraged Dead King` together. Exact alpha File `6342780`, however, does not register `call_forth_the_dead_king` and exposes no Enraged Dead King structured loot/resource route in its audited 41 loot JSON surfaces. The broad/full-line route is therefore **versioned context, not 1.21.1 acquisition proof**. See [`BLACKOUT-VERSIONED-ACQUISITION-BOUNDARY.md`](BLACKOUT-VERSIONED-ACQUISITION-BOUNDARY.md).

Result: complete object-level survival reachability for all 33 registrations is **not closed**.

## Exact loot-registry structural risk

A focused clean-room audit independently inspected `com.gametechbc.traveloptics.loot.TOLootModifiers` in exact file `6342780` and found:

- registry name `key_loot`: present once;
- registry name `universal_loot`: present once;
- `KeyLootModifier.CODEC`: referenced **twice** by the registry setup;
- `UniversalLootModifier.CODEC`: referenced **zero** times by that setup.

This is an exact structural fact from the publisher JAR. A third-party compatibility patch published later describes the same wiring as a registry-startup defect and changes the universal entry to `UniversalLootModifier.CODEC`; that external patch is not treated as upstream authority and Phase 2BS does **not** claim to have reproduced its reported crash.

A later clean-room binary-diff checkpoint fingerprints exact patch File `1690333 / 8861368` at SHA-1 `680fa679d8ea2419a79571f455436367222f6f9d`. Original and patch both contain 1339 ZIP entries; the patch adds/removes none and changes exactly one entry, `com/gametechbc/traveloptics/loot/TOLootModifiers.class`, with zero non-class resource changes. This independently proves the patch's binary scope, while the specific codec semantic fix remains attributed to the patch publisher. Physical deployment and assembled-pack startup remain unverified. See [`PATCH-8861368-BINARY-DIFF.md`](PATCH-8861368-BINARY-DIFF.md).

The structural mismatch is nevertheless sufficient to keep current-pack runtime promotion fail-closed until one of these is proven:

1. the physical pack actually carries a verified patch/replacement that changes this wiring; or
2. the exact unpatched physical artifact successfully initializes in an authoritative assembled-pack/runtime test despite the structural risk.

Neither proof is currently present in repository evidence.

## Semantic accounting

Phase 2BS disposition:

- 33 exact registered spell identities in publisher File `6342780`: **cataloged as release baseline**; current physical `OTHER_VERIFIED` bytes require re-audit before those 33 are claimed exact for the installed artifact;
- 32 residual localization-only IDs: **excluded +0**;
- `traveloptics:blackout`: survival reachability unresolved under its non-craftable Unique gate;
- exact publisher artifact: structural `TOLootModifiers` codec-wiring risk unresolved at runtime;
- semantic contribution to strict global minimum: **+0**;
- provider component closure: **no new component**;
- global strict minimum remains **1344**;
- technical component closure remains **66/100**.

`66/100` is a technical component metric, not a spell-coverage percentage.

## Runtime / authority boundary

T.O Magic remains owner of its provider spell identities, items, loot modifiers and addon-specific mechanics. Iron's remains owner of the host spell/casting substrate. Black Arcana does not create duplicate spell identities, replace provider acquisition, silently repair provider registries at runtime, or infer missing Alpha content from translations.

RPG Skill Tree remains only a sibling/provider of progression, attributes, Mastery, perks and gates through verified contracts; it does not own T.O Magic casting or Black Arcana runtime.

At the historical Phase 2BS checkpoint, Somake Aqua and this deprecated T.O alpha were both physically present, so Aqua authority could not be selected by assumption. Current sibling `76cf13e7d1110116f67c290eaa15891888279fc1` has no current certified/status-prefixed Traveloptics physical row; the legacy export dossier does not establish current installation. That specific dual-installed coexistence blocker is therefore **not current** unless Traveloptics is reintroduced into the physical pack.

## Evidence ceiling

- historical physical presence/version line: `HIGH`;
- current sibling physical-row presence: `ABSENT / NO STATUS-PREFIXED OR CATEGORIZED CURRENT ROW`; legacy uncategorized export dossier retained;
- exact publisher file identity/hashes: `HIGH`;
- exact 33 registration identities: `HIGH`;
- exclusion of 32 residual localization roots: `HIGH`;
- provider `allowCrafting` constants: `HIGH`;
- nine exact Unique-spell loot routes: `HIGH`;
- `blackout` object-level survival route: `UNVERIFIED / FAIL-CLOSED`;
- `TOLootModifiers` codec reference wiring: `HIGH` structural fact;
- actual registry-startup failure in the assembled pack: `NOT REPRODUCED`;
- physical deployment of any third-party patch: `UNVERIFIED`;
- complete-modpack runtime compatibility: `UNVERIFIED / FAIL-CLOSED`.

## Clean-room boundary

The artifact is All Rights Reserved. Inspection retained only hashes, metadata/dependency declarations, class/type/member identities, exact registry IDs, aggregate control-flow facts, constant host-gate outcomes, structured identifier/path references and narrow registry-reference facts required for catalog interoperability.

No method bodies, source reconstruction, localization prose, recipe/loot payloads, assets, models, sounds or binary redistribution are retained or adapted.

## Remaining gates

There is no current-pack promotion gate while Traveloptics has no current certified/status-prefixed physical row. If the provider is reintroduced, the audit must restart from the new physical artifact rather than inheriting the old alpha as current authority. At that time, re-evaluate:

1. exact physical artifact identity/hash and registry;
2. `TOLootModifiers` wiring/runtime initialization;
3. `traveloptics:blackout` object-level survival reachability;
4. any Somake Aqua ↔ T.O Aqua coexistence actually present in the reintroduced stack.

Until reintroduction, this dossier is historical provenance only.

## Audit anchors

- exact-artifact run `34740821956`, artifact `10312358984`, digest `sha256:2a38dcb75bbdb844ce3371a0b9afcf556c0f99b8ce5793442bf34ad8b5bc28b0`;
- focused registry run `34740904391`, artifact `10312645516`, digest `sha256:e6d7e908acfb96328285b4f8ca7504d13ca43f02cc07703d0e04c203fcbbfa11`;
- semantic 33/33 reconciliation run `34741045570`, artifact `10311499946`, digest `sha256:acbcc86f961d603608794f922a26106ab85f1a7479636596ba75dff3fefe8b00`;
- runtime-risk reconciliation run `34741368134`, artifact `10312730434`, digest `sha256:55c933137fabb4f32b90ca7fae08f89c799392b72e63f7de1682edac58cd15da`.
