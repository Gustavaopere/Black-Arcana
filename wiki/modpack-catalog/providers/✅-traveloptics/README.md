# T.O Magic n' Extras 4.4.0.1-1.21.1 — 33/33 current spell identities cataloged

**Current physical-JAR intake override (2026-10-08):** the exact `7b74816e...` bytes have now been inspected directly; **33/33 current registered spell IDs** are confirmed, and the two loot codec suppliers point to their respective modifier classes. The old raw-JAR-unavailable premises below are historical. Blackout survival, deployed runtime/serializer observation and Aqua cross-provider coexistence remain open; strict stays **+0**. See [`PHYSICAL-JAR-DIRECT-AUDIT-2026-10-08.md`](PHYSICAL-JAR-DIRECT-AUDIT-2026-10-08.md).

## Status

`✅ CATALOG COMPLETE (33/33) / ⚠️ RUNTIME AND SURVIVAL QA OPEN / CURRENT PHYSICAL JAR DIRECTLY INSPECTED / EXACT-CURRENT 33 REGISTERED SPELL IDS / DISTINCT LOOT CODEC SUPPLIER REFERENCES / BLACKOUT SURVIVAL + IN-PROCESS CODEC IDENTITY + AQUA AUTHORITY OPEN / STRICT +0`

Current physical status: **INSTALLED / CATALOG COMPLETE / RUNTIME GATES OPEN**. Current sibling authority rechecked at `neoforge-rpg-skilltree@de80b186357cad20ba5b81892a8682777e96e35a` (Traveloptics dossier blob `394abc11401526a4d2e6db5bd9af39bbc962e572`): `PROJECT-INSTRUCTIONS/modlist/modlist.md` row **#550** and `PROJECT-INSTRUCTIONS/modlist/Addons + Adventure and RPG + Armor, Tools, and Weapons + Magic + Mobs/✅-to-magic-n-extras v4.4.0.1-1.21.1.md` both record `traveloptics-4.4.0.1-1.21.1.jar`, mod id `traveloptics`, runtime `4.4.0.1-1.21.1`, SHA-1 `7b74816e89cc15dd0b5a31d9ea1e456024e8fae4`. This current physical authority supersedes older claims that Traveloptics was absent. Project Library physical inventories now provide direct SHA-1 corroboration as early as **22/08/2026**, followed by **08/09/2026** and **16/09/2026**, each recording the same `7b74816e...` bytes under the same filename.

The Phase 2BS publisher-artifact audit remains canonical evidence for File `6342780`. A later physical-fingerprint checkpoint proves the 2026-09-16 on-disk bytes differ (`OTHER_VERIFIED`). A separate 2026-08-18 Project Library CurseForge snapshot records the same filename in project/file `1046916 / 6342780`, publisher SHA-1 `380849...`, with `isModified=true`; because that metadata predates the later physical SHA-1, it is historical context and **does not identify the provenance of the September `7b74816e...` artifact**. Traveloptics is an active **✅ fully inventoried provider (33/33)**; deployment, survival availability and runtime remain **⚠️ conditional**, not historical-only.

## Current installed authority

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

Current sibling physical authority fingerprints the installed filename at SHA-1 `7b74816e89cc15dd0b5a31d9ea1e456024e8fae4`, independently matching Project Library physical inventories captured on **2026-08-22**, **2026-09-08** and **2026-09-16**. This differs from both exact publisher File `6342780` SHA-1 `3808493ce45cdfeb6408e85578adecf13df698e8` and known patch File `8861368` SHA-1 `680fa679d8ea2419a79571f455436367222f6f9d`. Physical disposition remains **`OTHER_VERIFIED`** and current provenance remains unidentified. The older 2026-08-18 `minecraftinstance.json` snapshot records a File-6342780 slot with `isModified=true`, but cannot prove that the later September bytes descend from that earlier state. The 33-ID File-6342780 inventory was a publisher-only baseline at that historical checkpoint. The later direct 2026-10-08 audit independently confirmed the **same exact-current physical set of 33 registered IDs**. See [`PHYSICAL-4.4.0.1-FINGERPRINT-CHECKPOINT.md`](PHYSICAL-4.4.0.1-FINGERPRINT-CHECKPOINT.md).

The current sibling T.O Magic n' Extras dossier now independently confirms the physical row and the same SHA-1. It is presence/fingerprint authority; the *subsequent direct-JAR audit* establishes exact-current registry identity. The publisher-to-physical provenance and numeric/mechanics delta remain separate, not yet reconciled.

### Physical-lineage chronology correction — updated 2026-10-04

The earliest direct physical hash capture is now **2026-08-22**: Project Library inventory `fcb79de3-0e3e-41af-8136-cd524859f71c.txt` records `traveloptics-4.4.0.1-1.21.1.jar` at SHA-1 `7b74816e89cc15dd0b5a31d9ea1e456024e8fae4` and fingerprint `4254006126`. The 2026-09-08 and 2026-09-16 inventories repeat the same values. Therefore this custom/repacked artifact was present in the assembled instance **well before** public patch File `8861368` was uploaded on 2026-09-12.

The retained August sequence is now bounded more tightly: repeated assembled boots on 16/08 fail inside Traveloptics `RegisterEvent` with duplicate `KeyLootModifier` codec registration; a canonical-name JAR and a separately named generated `fixed-keyloot.jar` are retained on 17/08; about 73 seconds after the retained `fixed-keyloot.jar` timestamp, the immediately following preserved NeoForge process discovers `traveloptics-4.4.0.1-1.21.1.jar` from the real instance `mods` directory and progresses through Traveloptics initialization into provider resource reload; CurseForge reports the canonical slot `isModified=true` on 18/08; the runtime analyzer observes the same 33 spell IDs on 19/08; and the current `7b74816e...` hash is directly captured on 22/08. The first-hash-day runtime bridge is now stronger than the prior >=25/33 checkpoint: targeted 2026-10-06 retrieval finds direct Additional Attributes registration lines for the eight previously unsurfaced IDs, so the retained 22/08 log family positively observes **all 33/33 publisher-baseline Traveloptics spell IDs**, including `traveloptics:blackout`.

This is strong historical local-modification/current-line correlation evidence, but it was **not** a byte bridge or exact-set proof on 22/08: the processes did not embed the JAR hash, file immutability was unproven and positive 33/33 inclusion did not rule out extra IDs. The direct 2026-10-08 physical-JAR registry inspection subsequently closed the exact 33-ID set on the matching bytes. See [`RUNTIME-2026-08-17-POST-REPAIR-CORRELATION.md`](RUNTIME-2026-08-17-POST-REPAIR-CORRELATION.md) and [`RUNTIME-2026-08-22-FIRST-HASH-REGISTRY-CORRELATION.md`](RUNTIME-2026-08-22-FIRST-HASH-REGISTRY-CORRELATION.md).

This chronology rules out “the pack simply downloaded File `8861368` and later renamed it” as provenance for `7b74816e...`. The chronology **alone** did not prove which code changes produced those bytes or their spell registry identity. The direct physical-JAR audit of 2026-10-08 closes the **exact-current 33-ID registry** independently, while provenance and constructed codec-instance/runtime evidence remain fail-closed.

A Project Library assembled-runtime checkpoint from **2026-08-19** further narrows that delta: NeoForge discovered the same nominal `traveloptics-4.4.0.1-1.21.1.jar`, and a bounded runtime-analyzer extraction produced exactly the same **33 unique spell IDs** as the publisher baseline, including `traveloptics:blackout`, with no additional Traveloptics spell identity before the analyzer advanced to the next provider namespace. The log does not record the JAR SHA-1, so this is **historical modified-runtime 33/33 evidence**, not proof that September SHA-1 `7b74816e...` is registry-identical.

Temporary NON-MERGE PR **#474** adds another bounded negative result. Its clean-room run `36649716927` reconstructed common one-entry archive replacements using the known patch's changed `TOLootModifiers.class`; none matched current SHA-1 `7b74816e...`, and none matched the recorded size of the Aug-17 Library `fixed-keyloot.jar`. This makes “the current JAR is merely one of those straightforward repacks” unsupported, but still does not identify the current bytes. See [`PHYSICAL-4.4.0.1-FINGERPRINT-CHECKPOINT.md`](PHYSICAL-4.4.0.1-FINGERPRINT-CHECKPOINT.md).

Temporary NON-MERGE PR **#648** then expands the surgical one-entry reconstruction family to **164** outputs, varying Info-ZIP update strategy, extra fields, compression levels, plausible replacement timestamps and JDK `jar uf`. Dedicated run `37317446376` succeeds with **0/164** matches for current SHA-1 `7b74816e...`, **0/164** matches for physical fingerprint `4254006126`, and **0/164** matches for the retained `fixed-keyloot.jar` size **18,393,641**. The closest family is 81 bytes smaller. This is stronger negative lineage evidence, not artifact identification. See [`EXPANDED-SURGICAL-REPACK-AUDIT.md`](EXPANDED-SURGICAL-REPACK-AUDIT.md).

A 2026-10-05 public-provenance boundary additionally found no indexed origin for the exact `7b74816e...` SHA-1, fingerprint `4254006126`, retained `fixed-keyloot` filename, or a public user-repository build/provenance trail. This is negative discovery evidence only; it does not prove private/local origin. The historical Gate-1 missing-byte requirement has since been satisfied by the 2026-10-08 exact physical upload; patch provenance is still not established and is not a prerequisite for the now-closed 33-ID inventory. See [`PUBLIC-PROVENANCE-SEARCH-BOUNDARY-2026-10-05.md`](PUBLIC-PROVENANCE-SEARCH-BOUNDARY-2026-10-05.md).

A second September correlation is now canonical: the 08/09 physical dump at ~12:05 UTC records SHA-1 `7b74816e...`, and `debug(9).log` from the same CurseForge instance starts the relevant assembled boot roughly 14 minutes later. That boot creates `TravelopticsMod`, loads both Traveloptics configs and subscribes provider handlers; bounded full-log search finds no `Adding duplicate value` and no `Mod loading issue for:`. The later crash is a `shine.mixins.json:ProgramMixin` shader-injection failure, not Traveloptics registration. This is strong contemporaneous runtime-init evidence for the September physical line, but the process does not embed the JAR SHA and does not enumerate the spell registry. See [`RUNTIME-2026-09-08-PHYSICAL-CORRELATION.md`](RUNTIME-2026-09-08-PHYSICAL-CORRELATION.md).

## Publisher release boundary

The exact CurseForge file is explicitly published as a deprecated alpha for 1.21.1. Its file notes state that only part of the 1.21 content was ported, that Cataclysm-based spells/some items were among the ported surfaces, that the ported spells are intended to be obtainable in survival, and that Alex's Caves content is absent from this build.

Those publisher statements are release-line context, not a registry inventory. The exact JAR still carries localization roots for content not registered by this 1.21.1 alpha, so marketing text and translation keys are never projected backward into the current registry.

### Publisher semantic context — non-strict

The current official CurseForge project page also publishes behavioral descriptions for entries that correlate with all **33** exact-alpha registry identities. Those descriptions are now captured only as short clean-room paraphrases in [`PUBLISHER-SEMANTIC-CONTEXT.md`](PUBLISHER-SEMANTIC-CONTEXT.md).

This is an editorial/catalog layer, not exact-version runtime evidence: the project page is living documentation and also describes content absent from File `6342780`. Registry IDs, schools, provider gates and exact loot anchors therefore remain controlled by the exact-artifact audit. Display-label drift on the living page is never allowed to rename or add registry identities. Seven explicitly stated thresholds/timings/conditions are retained only as publisher-only version-conditioned context; they are not promoted to exact-alpha/current-physical balance facts.

The semantic/mechanics layers do **not** change the provider disposition: current physical bytes remain `OTHER_VERIFIED` *relative to the publisher*, but the exact-current 33-ID registry is now directly established. Publisher numeric/stat parity, `blackout` reachability, in-process serializer identity and full-pack runtime remain unresolved; strict contribution remains **+0**.

A bounded clean-room accessor audit closes **37 exact File-only resolved bounded accessor outputs across 24/33 spells** for publisher File `6342780`: 29 no-entity values plus 8 LivingEntity-signature values proven entity-unused before evaluation. A separate direct-delegate audit plus the current Iron's 3.16.3 source contract closes **7 host-resolved effective-cast-time results**, expanding numeric accessor/bridge coverage to **28/33** spell identities while keeping the 37 File-only denominator unchanged. Audit #658 now dependency-classifies **all 34/34 `ENTITY_SLOT_READ` numeric accessors**: 24 depend on the entity only through host `getSpellPower(int, Entity)`, 9 summon-damage accessors additionally depend on Iron's `SUMMON_DAMAGE` attribute surface, and `aerial_collapse#getDamage` adds `Math.min(float,float)`. The methods remain numerically entity/config dependent. Thus **33/33 identities have at least one bounded accessor result, host bridge or dependency contract**, not 33/33 numeric closure. See [`EXACT-4.4.0.1-SCALAR-ACCESSORS.md`](EXACT-4.4.0.1-SCALAR-ACCESSORS.md), [`EXACT-4.4.0.1-LIVINGENTITY-ACCESSORS.md`](EXACT-4.4.0.1-LIVINGENTITY-ACCESSORS.md), [`EXACT-4.4.0.1-CURRENT-HOST-EFFECTIVE-CAST-BRIDGE.md`](EXACT-4.4.0.1-CURRENT-HOST-EFFECTIVE-CAST-BRIDGE.md) and [`EXACT-4.4.0.1-ALL-ENTITY-DEPENDENCY-MAP.md`](EXACT-4.4.0.1-ALL-ENTITY-DEPENDENCY-MAP.md). None of these results is projected to current physical SHA-1 `7b74816e...`.

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

## Exact publisher mechanics baseline

A bounded clean-room audit of exact CurseForge File `6342780` now closes the default/raw host-input mechanics baseline for all **33/33** registered spell classes:

- base mana;
- mana per level;
- base spell-power input;
- spell-power per level input;
- cast-time field in ticks;
- cast type;
- max level;
- minimum rarity;
- default cooldown seconds.

Authority: temporary NON-MERGE PR **#599**, authoritative HEAD `6789b859c3b617e1174e9b0e5ff6df48d2a993b3`, workflow run `37236187715` **SUCCESS**, artifact `11315159450`, digest `sha256:7001221a307d3a81ba8ef8b41a0dba29a059a2fbaf6b756fc2db0edb26996eb9`.

These values are exact for publisher File `6342780` only. They are not projected to current physical SHA-1 `7b74816e...`. Spell-power fields are host inputs, not final damage formulas; effective config/multipliers and spell-specific range/radius/duration/PvP/boss behavior remain separate evidence questions.

See [`EXACT-4.4.0.1-MECHANICS-BASELINE.md`](EXACT-4.4.0.1-MECHANICS-BASELINE.md).

## Craftability and acquisition evidence

Provider-owned ancestry divides the 33 registrations into three relevant groups:

- 21 registrations are outside the Unique/Weapon provider bases. Exact-alpha probes now establish **0/21** direct `DefaultConfig.setAllowCrafting(...)` calls, **0/21** direct `setDeprecated(...)` calls, **0** direct `DefaultConfig.allowCrafting`/`enabled` writes, and **0/21** concrete `isEnabled()` / `canBeCraftedBy(Player)` overrides. Under current Iron's `1.21.1-3.16.3`, `DefaultConfig.allowCrafting=true`, `DefaultConfig.enabled=true`, and both generic config parameters default true. These 21 are therefore **host/publisher-default craftable + enabled**, while effective Scroll Forge eligibility remains conditioned by active server/datapack/global config, compatible focus/school selection and player-specific learning where applicable;
- 10 registrations inherit `AbstractUniqueSpell.allowCrafting() = false`;
- 2 registrations inherit `AbstractWeaponSpell.allowCrafting() = true`: `cursed_blast` and `gyro_slash`.

See [`HOST-CRAFTABILITY-3.16.3-CHECKPOINT.md`](HOST-CRAFTABILITY-3.16.3-CHECKPOINT.md) and [`HOST-ENABLED-3.16.3-CHECKPOINT.md`](HOST-ENABLED-3.16.3-CHECKPOINT.md). Default craftability/enabled closure is narrower than effective Scroll Forge eligibility and does not establish unconditional survival acquisition.

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

`traveloptics:blackout` is the unresolved current-pack exception. It inherits `AbstractUniqueSpell.allowCrafting() = false`; a focused exact-alpha generic-loot audit additionally proves `allowLooting() = false`, 23 explicit random-spell filters with no Blackout entry, no forced Eldritch filter, no provider code reference to host `SpellFilter` / `RandomizeSpellFunction`, and no `BLACKOUT_SPELL` reference outside `TOSpells`. Thus File `6342780` has neither a direct structured acquisition anchor nor a provider-owned built-in generic loot path for Blackout. Retained-evidence and versioned-tree audits found no literal/object-specific route, no preserved Library KubeJS/datapack source, no named `SpellFilter` / `RandomizeSpellFunction` route, and no Blackout route in the inspected GLM/progression/script/resource surfaces. A later full-`src/main` bounded audit additionally found zero uses of the audited direct Iron's spell-container/scroll construction APIs across Black Arcana + RPG Skill Tree and no Traveloptics/Blackout/scroll/container resource token; reviewed generic item/reward candidates likewise do not materialize Blackout. This still does **not** exclude reflection/encoded/dynamic versioned logic, assembled external KubeJS/datapack/other-mod surfaces, or current physical Traveloptics content. See [`BLACKOUT-GENERIC-LOOT-EXCLUSION.md`](BLACKOUT-GENERIC-LOOT-EXCLUSION.md), [`BLACKOUT-EXTERNAL-ROUTE-RETAINED-EVIDENCE-CHECKPOINT.md`](BLACKOUT-EXTERNAL-ROUTE-RETAINED-EVIDENCE-CHECKPOINT.md), [`BLACKOUT-VERSIONED-GENERIC-ROUTE-AUDIT.md`](BLACKOUT-VERSIONED-GENERIC-ROUTE-AUDIT.md) and [`BLACKOUT-VERSIONED-ACQUISITION-SURFACE-AUDIT.md`](BLACKOUT-VERSIONED-ACQUISITION-SURFACE-AUDIT.md).

The current broad project description documents a Dead King → Blackout route for the full project, while official 1.20.1 File `6010839` introduced `Blackout`, `Call Forth The Dead King` and `Enraged Dead King` together. Exact alpha File `6342780`, however, does not register `call_forth_the_dead_king` and exposes no Enraged Dead King structured loot/resource route in its audited 41 loot JSON surfaces. The broad/full-line route is therefore **versioned context, not 1.21.1 acquisition proof**. See [`BLACKOUT-VERSIONED-ACQUISITION-BOUNDARY.md`](BLACKOUT-VERSIONED-ACQUISITION-BOUNDARY.md).

Result: complete object-level survival reachability for all 33 registrations is **not closed**.

## Historical publisher loot-registry defect and remaining current runtime gate

A focused clean-room audit independently inspected `com.gametechbc.traveloptics.loot.TOLootModifiers` in exact file `6342780` and found:

- registry name `key_loot`: present once;
- registry name `universal_loot`: present once;
- `KeyLootModifier.CODEC`: referenced **twice** by the registry setup;
- `UniversalLootModifier.CODEC`: referenced **zero** times by that setup.

This is an exact structural fact from the publisher JAR. Project Library crash reports from 2026-08-16 independently reproduce the matching assembled-pack failure under the canonical Traveloptics filename: `RegisterEvent` aborts with `Adding duplicate value ... to registry` for a `KeyLootModifier` codec. Those processes are hash-unbound and therefore do not prove exact publisher-byte identity or current `7b74816e...` behavior. A third-party compatibility patch published later describes the same wiring as a registry-startup defect and changes the universal entry to `UniversalLootModifier.CODEC`; that external patch is not treated as upstream authority. See [`RUNTIME-2026-08-16-LOOT-CODEC-CRASH.md`](RUNTIME-2026-08-16-LOOT-CODEC-CRASH.md).

A later clean-room binary-diff checkpoint fingerprints exact patch File `1690333 / 8861368` at SHA-1 `680fa679d8ea2419a79571f455436367222f6f9d`. Original and patch both contain 1339 ZIP entries; the patch adds/removes none and changes exactly one entry, `com/gametechbc/traveloptics/loot/TOLootModifiers.class`, with zero non-class resource changes. This independently proves the patch's binary scope, while the specific codec semantic fix remains attributed to the patch publisher. Physical deployment and assembled-pack startup remain unverified. See [`PATCH-8861368-BINARY-DIFF.md`](PATCH-8861368-BINARY-DIFF.md).

A bounded Project Library search on 2026-10-05 found no preserved post-repair direct observation of both `traveloptics:key_loot` and `traveloptics:universal_loot` serializer values, and no `distinct_codec_instances=true` probe row. Historical duplicate-`KeyLootModifier` failures remain positive evidence; search misses are not absence evidence. Gate 2 therefore still requires the canonical physical-pack registry probe rather than further generic log searching. See [`GATE2-PRESERVED-LOG-SEARCH-BOUNDARY-2026-10-05.md`](GATE2-PRESERVED-LOG-SEARCH-BOUNDARY-2026-10-05.md).

The attached current physical JAR now directly establishes distinct **supplier references** (`key_loot -> KeyLootModifier.CODEC` and `universal_loot -> UniversalLootModifier.CODEC`), unlike the historical publisher wiring. This supersedes the earlier *current-wiring-unknown* premise, not the runtime blocker. Only an in-process schema-4 observation of distinct constructed codec instances, both registrations and successful same-artifact startup can close the remaining serializer/runtime gate. No such authoritative current-instance observation is present.

## Semantic accounting — current physical override and historical Phase 2BS

Phase 2BS historical disposition, superseded where expressly noted below:

- 33 publisher-registered spell identities: **release baseline**, independently confirmed as the same **33/33 exact-current physical registered IDs** by the 2026-10-08 direct-JAR audit;
- 32 residual localization-only IDs: **excluded +0**;
- `traveloptics:blackout`: exact-alpha provider direct/generic loot routes excluded; current-pack survival reachability remains unresolved;
- exact publisher mechanics baseline: 33/33 registered spells closed for raw/default host inputs; current-physical stat equality unverified;
- exact publisher File-only bounded scalar accessors: 37 resolved outputs across 24 spells; LivingEntity-bearing surface classified at 15 ENTITY_UNUSED / 34 ENTITY_SLOT_READ, with 8 File-only values plus 7 exact direct-delegate relations; current Iron's 3.16.3 host resolves those seven effective-cast delegates, bringing numeric accessor/bridge coverage to 28/33 spell identities; audit #658 dependency-classifies all 34/34 entity-reading methods into 24 host-spell-power-only + 9 `SUMMON_DAMAGE`-augmented + 1 spell-power+`Math.min`, so identity-level accessor/bridge/dependency coverage is 33/33 while numeric closure stays 28/33; current-physical equality remains unverified;
- exact publisher artifact: structural `TOLootModifiers` defect is corroborated by historical assembled-runtime reproduction; current physical `7b74816e...` supplier references are distinct, while constructed codec object identity and process-bound startup remain unresolved;
- semantic contribution to strict global minimum: **+0**;
- provider component closure: **no new component**;
- strict minimum at the historical Phase 2BS checkpoint remained **1344**; after direct physical-JAR intake PR #697 the current catalog-wide strict reconstructible minimum is **1851** (Deeper and Darker +2; Traveloptics +0);
- technical component closure at the historical Phase 2BS checkpoint remained **66/100**; the current cross-domain technical denominator is **`PENDING REBASE`**.

`66/100` is a technical component metric, not a spell-coverage percentage.

## Runtime / authority boundary

T.O Magic remains owner of its provider spell identities, items, loot modifiers and addon-specific mechanics. Iron's remains owner of the host spell/casting substrate. Black Arcana does not create duplicate spell identities, replace provider acquisition, silently repair provider registries at runtime, or infer missing Alpha content from translations.

RPG Skill Tree remains only a sibling/provider of progression, attributes, Mastery, perks and gates through verified contracts; it does not own T.O Magic casting or Black Arcana runtime.

Somake 1.0.9 and Traveloptics 4.4.0.1 are both physically present in the current modlist checkpoint, so the Aqua coexistence/authority blocker is **current**. Black Arcana must not select, suppress, alias or merge an Aqua authority by assumption; coexistence must be demonstrated from provider/runtime evidence.

## Evidence ceiling

- current physical presence/version/hash from Project modlist: `HIGH`;
- 2026-08-19 modified assembled-runtime 33/33 spell-ID set: `HIGH FOR THAT HISTORICAL SNAPSHOT / HASH-UNBOUND TO CURRENT PHYSICAL`;
- sibling status-prefix/categorization absence: `NON-AUTHORITATIVE FOR PHYSICAL PRESENCE`;
- exact publisher file identity/hashes: `HIGH`;
- exact 33 registration identities: `HIGH`;
- exact File-6342780 bounded scalar accessors (37 File-only resolved values; 49 LivingEntity-bearing methods classified): `HIGH FOR FILE-LOCAL RAW RETURN VALUES / UNITS+FINAL FORMULAS SEPARATE`;
- seven File-6342780 direct effective-cast delegates + current Iron's 3.16.3 `getCastTime` bridge: `HIGH FOR THE PINNED PROVIDER+HOST COMBINATION / NOT CURRENT-PHYSICAL TRAVELOPTICS PROOF`;
- all 34 entity-reading accessor dependency classifications: `HIGH FOR MEMBER/CONTROL-FLOW DEPENDENCY / 24 HOST-SPELL-POWER ONLY + 9 SUMMON_DAMAGE AUGMENTED + 1 SPELL-POWER+MATH.MIN / NUMERIC OUTPUTS REMAIN ENTITY+CONFIG CONDITIONAL`;
- exclusion of 32 residual localization roots: `HIGH`;
- provider Unique/Weapon `allowCrafting` constants: `HIGH`;
- 21 remaining exact-alpha concrete classes with no direct `DefaultConfig.setAllowCrafting(...)`: `HIGH`;
- current Iron's 3.16.3 host default craftability contract: `HIGH / SOURCE-PINNED`;
- effective deployed craftability for those 21 after server/datapack config + player learning: `CONDITIONAL`;
- nine exact Unique-spell loot routes: `HIGH`;
- `blackout` File-6342780 provider loot route: `EXCLUDED — DIRECT + GENERIC`;
- `blackout` actual current-pack survival route: `UNVERIFIED / FAIL-CLOSED`;
- `TOLootModifiers` codec reference wiring: `HIGH` structural fact;
- actual registry-startup failure in the assembled pack: `REPRODUCED HISTORICALLY / 2026-08-16 / PROCESS HASH UNBOUND`; current `7b74816e...` serializer-object state remains unverified;
- physical deployment of exact patch File `8861368`: `DISPROVED BY HASH`;
- byte identity with the common one-entry repack variants tested in PR #474: `DISPROVED`;
- provenance/content of the actual `7b74816e...` replacement: `AUGUST LINEAGE NARROWED / ENTRY-LEVEL DELTA UNVERIFIED`;
- complete-modpack runtime compatibility: `UNVERIFIED / FAIL-CLOSED`.

## Clean-room boundary

The artifact is All Rights Reserved. Inspection retained only hashes, metadata/dependency declarations, class/type/member identities, exact registry IDs, aggregate control-flow facts, constant host-gate outcomes, structured identifier/path references and narrow registry-reference facts required for catalog interoperability.

No method bodies, source reconstruction, localization prose, recipe/loot payloads, assets, models, sounds or binary redistribution are retained or adapted.

## Remaining gates

Traveloptics is currently installed and remains blocked on a finite current-pack closure set:

1. capture the assembled-instance schema-4 registry probe with both constructed codec identities distinct and the exact FML-loaded current-JAR fingerprint; physical `TOLootModifiers` supplier references are already inspected;
2. close `traveloptics:blackout` normal-survival acquisition using actual deployed Iron's settings and KubeJS/datapack/loot/quest routes, not publisher descriptions or source defaults;
3. close Somake Aqua ↔ Traveloptics cross-provider identity/authority and deduplication using actual assembled-stack evidence;
4. complete provider-native runtime acceptance without conflating registry/serializer smoke with gameplay QA.

The **33 exact-current physical registered identities are cataloged 33/33**, but contribute **+0 strict** pending the current-pack reachability/runtime gates. The semantic global minimum remains **1851** independently of Traveloptics.

## Audit anchors

- exact-artifact run `34740821956`, artifact `10312358984`, digest `sha256:2a38dcb75bbdb844ce3371a0b9afcf556c0f99b8ce5793442bf34ad8b5bc28b0`;
- focused registry run `34740904391`, artifact `10312645516`, digest `sha256:e6d7e908acfb96328285b4f8ca7504d13ca43f02cc07703d0e04c203fcbbfa11`;
- semantic 33/33 reconciliation run `34741045570`, artifact `10311499946`, digest `sha256:acbcc86f961d603608794f922a26106ab85f1a7479636596ba75dff3fefe8b00`;
- runtime-risk reconciliation run `34741368134`, artifact `10312730434`, digest `sha256:55c933137fabb4f32b90ca7fae08f89c799392b72e63f7de1682edac58cd15da`.
