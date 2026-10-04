# T.O Magic n' Extras 4.4.0.1-1.21.1 — exact publisher artifact audit

Status: `NON-SOURCE CLEAN-ROOM EVIDENCE / EXACT CURSEFORGE FILE 6342780 / 33 REGISTRY IDENTITIES / PARTIAL REACHABILITY / RUNTIME RISK FAIL-CLOSED`

## Artifact identity

- CurseForge project: `1046916`
- exact file: `6342780`
- version: `4.4.0.1-1.21.1`
- mod id: `traveloptics`
- display name: `T.O Magic n' Extras`
- license: `All Rights Reserved`
- exact release SHA-1: `3808493ce45cdfeb6408e85578adecf13df698e8`
- exact release SHA-256: `0372b4b8593288726fb0d6e8cdb86202a87677d0c2dafeb96cab50bf057ec298`
- Curse Maven: `curse.maven:to-tweaks-irons-spells-1046916:6342780`

The current physical-JAR SHA-1 is independently preserved by the sibling modlist and Project Library evidence as `7b74816e89cc15dd0b5a31d9ea1e456024e8fae4`, and it differs from the exact publisher release SHA-1 `3808493ce45cdfeb6408e85578adecf13df698e8`. This artifact is therefore an exact publisher-release witness aligned to the installed version line, not a hash-matched current-physical witness; the exact current bytes/provenance and registry delta remain unavailable.

## Declared dependency facts

Exact `META-INF/neoforge.mods.toml` declares:

- NeoForge `[21.1.0,)`;
- Minecraft `[1.21.1,1.22)`;
- Iron's Spells 'n Spellbooks `[1.21.1-3.10.0,)`;
- L_Ender's Cataclysm `[2.60.,)`;
- Apothic Attributes `[2.6.1,)`.

These declarations are metadata facts only; they do not prove assembled-pack compatibility.

## Clean-room audit sequence

### Exact artifact structure

Audit branch: `audit/traveloptics-4.4.0.1-exact-artifact`.

Run `34740821956` completed GREEN after downloading Curse Maven file `6342780` and hard-requiring SHA-1 `3808493ce45cdfeb6408e85578adecf13df698e8`.

Artifact:

- ID `10312358984`;
- name `traveloptics-4.4.0.1-exact-artifact-audit`;
- digest `sha256:2a38dcb75bbdb844ce3371a0b9afcf556c0f99b8ce5793442bf34ad8b5bc28b0`.

Retained facts include metadata, hashes, class/type/signature identities, aggregate registry/config facts, localization keys and structured resource paths only.

### Focused registry reconciliation

Run `34740904391` completed GREEN.

Artifact:

- ID `10312645516`;
- name `traveloptics-4.4.0.1-registry-reconciliation`;
- digest `sha256:e6d7e908acfb96328285b4f8ca7504d13ca43f02cc07703d0e04c203fcbbfa11`.

It closed:

- provider class count: `250`;
- provider `AbstractSpell` descendants: `35`;
- exact spell registry class: `com.gametechbc.traveloptics.init.TOSpells`;
- registry `registerSpell(...)` calls: `33`;
- static-initializer branch opcodes: `0`.

### 33/33 semantic reconciliation

Run `34741045570` completed GREEN.

Artifact:

- ID `10311499946`;
- name `traveloptics-4.4.0.1-semantic-reconciliation`;
- digest `sha256:acbcc86f961d603608794f922a26106ab85f1a7479636596ba75dff3fefe8b00`.

Hard assertions required:

- 33 unique `Supplier<AbstractSpell>` fields;
- 33 registry calls;
- zero registry branches;
- 33 unique concrete spell classes;
- 33 unique field -> class mappings;
- 33 unique class -> `traveloptics:<id>` mappings;
- every registered ID has a root localization key.

The artifact also contains 32 additional root localization spell IDs that are absent from the exact registry. Those are retained only as evidence of stale/residual content and are excluded from semantic counting.

### Runtime-risk reconciliation

The initial assertion assumed both provider abstract spell bases were non-craftable and intentionally failed when exact bytecode instead proved `AbstractWeaponSpell.allowCrafting() = true`. The harness was corrected rather than treating that failure as provider evidence.

Corrected run `34741368134` completed GREEN on audit HEAD `3dbe6d1f0dc25104a86283ae04e0cfd3365b4998`.

Artifact:

- ID `10312730434`;
- name `traveloptics-4.4.0.1-runtime-risk-reconciliation`;
- digest `sha256:55c933137fabb4f32b90ca7fae08f89c799392b72e63f7de1682edac58cd15da`.

Exact constant results:

- `AbstractUniqueSpell.allowCrafting() = false`;
- `AbstractWeaponSpell.allowCrafting() = true`.

Exact selected provider references:

- `BLACKOUT_SPELL`: zero provider-owned class references outside `TOSpells`;
- `CURSED_BLAST_SPELL`: referenced by `CursedWraithbladeItem` construction;
- `GYRO_SLASH_SPELL`: referenced by Infernal Devastator item variants and the Gyro Slash projectile path.

Exact `TOLootModifiers` structural facts:

- `key_loot` registry name reference count: `1`;
- `universal_loot` registry name reference count: `1`;
- `KeyLootModifier.CODEC` reference count: `2`;
- `UniversalLootModifier.CODEC` reference count: `0`.

This audit records wiring facts only. It does not claim a reproduced NeoForge registry crash.

## Exact field -> class -> ID inventory

| Registry field | Concrete class | Exact registry ID |
|---|---|---|
| `BLOOD_HOWL_SPELL` | `BloodHowlSpell` | `traveloptics:blood_howl` |
| `ABYSSAL_BLAST_SPELL` | `AbyssalBlastSpell` | `traveloptics:abyssal_blast` |
| `BLACKOUT_SPELL` | `BlackoutSpell` | `traveloptics:blackout` |
| `PSYCHIC_BOLT_SPELL` | `PsychicBoltSpell` | `traveloptics:psychic_bolt` |
| `REVERSAL_SPELL` | `ReversalSpell` | `traveloptics:reversal` |
| `SPECTRAL_BLINK` | `SpectralBlinkSpell` | `traveloptics:spectral_blink` |
| `ETERNAL_SENTINEL_SPELL` | `EternalSentinelSpell` | `traveloptics:eternal_sentinel` |
| `ORBITAL_VOID_SPELL` | `OrbitalVoidSpell` | `traveloptics:orbital_void` |
| `CURSED_MINEFIELD_SPELL` | `CursedMinefieldSpell` | `traveloptics:cursed_minefield` |
| `VOID_ERUPTION_SPELL` | `VoidEruptionSpell` | `traveloptics:void_eruption` |
| `VORTEX_PUNCH_SPELL` | `VortexPunchSpell` | `traveloptics:vortex_punch` |
| `ASTRAL_SENSE_SPELL` | `AstralSenseSpell` | `traveloptics:astral_sense` |
| `ASHEN_BREATH_SPELL` | `AshenBreathSpell` | `traveloptics:ashen_breath` |
| `LINGERING_STRAIN` | `LingeringStrainSpell` | `traveloptics:lingering_strain` |
| `IGNITED_ONSLAUGHT_SPELL` | `IgnitedOnslaughtSpell` | `traveloptics:ignited_onslaught` |
| `BURNING_JUDGEMENT_SPELL` | `BurningJudgmentSpell` | `traveloptics:burning_judgment` |
| `METEOR_STORM_SPELL` | `MeteorStormSpell` | `traveloptics:meteor_storm` |
| `LAVAL_BOMB_SPELL` | `LavaBombSpell` | `traveloptics:lava_bomb` |
| `GYRO_SLASH_SPELL` | `GyroSlashSpell` | `traveloptics:gyro_slash` |
| `NULLFLARE_SPELL` | `NullflareSpell` | `traveloptics:nullflare` |
| `SUMMON_DESERT_DWELLERS_SPELL` | `SummonDesertDwellers` | `traveloptics:summon_desert_dwellers` |
| `SWORD_OF_THE_ANCIENTS_SPELL` | `SwordOfTheAncientsSpell` | `traveloptics:sword_of_the_ancients` |
| `AXE_OF_THE_DOOMED_SPELL` | `AxeOfTheDoomedSpell` | `traveloptics:axe_of_the_doomed` |
| `CURSED_REVENANTS_SPELL` | `CursedRevenantsSpell` | `traveloptics:cursed_revenants` |
| `DESPAIR_SPELL` | `DespairSpell` | `traveloptics:despair` |
| `HALBERD_HORIZON_SPELL` | `HalberdHorizonSpell` | `traveloptics:halberd_horizon` |
| `CURSED_BLAST_SPELL` | `CursedBlastSpell` | `traveloptics:cursed_blast` |
| `MECHANIZED_PREDATORS_SPELL` | `MechanizedPredatorSpell` | `traveloptics:mechanized_predator` |
| `RAPID_LASER_SPELL` | `RapidLaserSpell` | `traveloptics:rapid_laser` |
| `DEATH_LASER_SPELL` | `DeathLaserSpell` | `traveloptics:death_laser` |
| `EM_PULSE_SPELL` | `EmPulse` | `traveloptics:em_pulse` |
| `AERIAL_COLLAPSE_SPELL` | `AerialCollapseSpell` | `traveloptics:aerial_collapse` |
| `STELE_CASCADE_SPELL` | `SteleCascadeSpell` | `traveloptics:stele_cascade` |

## Provider gate ancestry

The 33 registrations split as follows:

- **21** inherit Iron's host gate methods with no provider-owned `allowCrafting`, `isEnabled` or `canBeCraftedBy` declaration found along provider ancestry;
- **10** inherit provider `AbstractUniqueSpell.allowCrafting() = false`;
- **2** inherit provider `AbstractWeaponSpell.allowCrafting() = true`.

A follow-up clean-room probe on exact File `6342780` (temporary NON-MERGE PR **#588**, HEAD `992d798b2edeb0861655f19dd5cda65b7cb13905`, run `37211319887` SUCCESS, text artifact `11306413411`, digest `sha256:2d8f4c16d4a315b52fea0a571c551d3ee6a8dedee472fbced3a44331938edab8`) checked only the 21 concrete classes in the first group for direct `DefaultConfig.setAllowCrafting(boolean)` calls. Result: **21 ABSENT / 0 FALSE / 0 TRUE / 0 UNKNOWN**.

Current physical Iron's Spellbooks is `1.21.1-3.16.3` (SHA-1 `017fd8140c477f9ae602cf95594f1c23bef1d6e3`). Its exact public source pin `iron431/irons-spells-n-spellbooks@e4056af90302d37eb1739f5ff05020b020e6e252` identifies the same `mod_version=1.21.1-3.16.3` and establishes: `DefaultConfig.allowCrafting = true`; generic `SpellConfigParameter.ALLOW_CRAFTING = true`; `AbstractSpell.allowCrafting()` resolves the configured parameter; and `canBeCraftedBy(player)` independently applies the learning gate.

Therefore those **21** exact-alpha registrations are **host-default Scroll Forge eligible under the current Iron's 3.16.3 contract**, while effective deployed craftability remains config/learning-conditioned. This does not by itself close object-level survival reachability. See `HOST-CRAFTABILITY-3.16.3-CHECKPOINT.md`.

The ten Unique registrations are:

`abyssal_blast`, `axe_of_the_doomed`, `blackout`, `burning_judgment`, `eternal_sentinel`, `halberd_horizon`, `ignited_onslaught`, `mechanized_predator`, `summon_desert_dwellers`, `sword_of_the_ancients`.

The two Weapon registrations are:

`cursed_blast`, `gyro_slash`.

## Structured acquisition evidence

Exact resource scanning finds 41 loot/loot-modifier JSON resources and zero recipe JSON resources. Nine of the ten non-craftable Unique registrations have direct exact structured loot references:

| Unique spell | Exact structured acquisition anchor |
|---|---|
| `abyssal_blast` | Leviathan loot |
| `axe_of_the_doomed` | Aptrgangr loot |
| `burning_judgment` | Ignis loot |
| `eternal_sentinel` | Ender Golem loot |
| `halberd_horizon` | Maledictus loot |
| `ignited_onslaught` | Ignited Berserker / Ignited Revenant loot |
| `mechanized_predator` | Prowler / Watcher loot |
| `summon_desert_dwellers` | Koboleton / Wadjet loot |
| `sword_of_the_ancients` | Kobolediator loot |

`blackout` has no structured-data reference in the exact JAR and no provider-owned field reference outside the registry itself. That does not prove impossibility, but it leaves exact object-level survival reachability unresolved.

The single `data/traveloptics/tags/item/aqua_focus.json` resource is not evidence of active Aqua spell registrations: no Aqua spell appears among the exact 33 registrations in this alpha.

## Config evidence

`com.gametechbc.traveloptics.config.SpellsConfig` exists. The exact audit observed configuration fields for spell behavior, damage/block interaction, summon limits, spellbook slots/power/mana and related balance surfaces. No per-spell registry enable/disable gate was found in the exact registry path.

Config presence therefore does not condition whether the 33 `TOSpells` registrations exist; runtime behavior and balance remain separate QA.

## Mixin / runtime surface

The JAR contains one mixin configuration, `traveloptics.mixins.json`. Phase 2BS does not infer compatibility or safety from its presence.

The publisher labels file `6342780` a deprecated alpha. Separately, a later third-party patch reports a registry initialization problem at `TOLootModifiers` and describes changing the universal loot codec reference. The clean-room audit independently confirms the exact original JAR's two-name/two-Key-codec/zero-Universal-codec structure, but no assembled-pack crash was reproduced in this checkpoint.

Therefore runtime remains fail-closed.

## Metric disposition

- exact registry identities reconstructed: `33`;
- residual localization roots excluded: `32`;
- strict semantic delta: `+0` while reachability/runtime blockers remain;
- component delta: `+0`;
- current global strict minimum remains `1344`;
- current technical closure remains `66/100`.

## Clean-room retention rule

The exact ARR binary was inspected read-only. Retained evidence is limited to cryptographic hashes, metadata/dependencies, class/type/member/registry identities, aggregate control-flow facts, constant boolean gate outcomes, and structured resource/reference identities needed for interoperability and catalog accounting.

No implementation bodies, upstream source reconstruction, binary redistribution, assets, localization prose, recipe/loot payload bodies, models or sounds are preserved or adapted.
