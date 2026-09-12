# Somake Spells 1.0.8-fix — exact artifact audit

## Verdict

`EXACT HASH-MATCHED ARTIFACT / 67 CURRENT REGISTRY IDENTITIES / PHYSICAL OPTIONAL GATES SATISFIED / SEMANTIC REACHABILITY CONDITIONAL / +0 STRICT DELTA / ARR CLEAN-ROOM`

This audit closes Somake's exact installed spell-registry identity. It intentionally does **not** promote those identities into the strict semantic numerator because current deployed COMMON configuration and complete object-level survival acquisition/reachability are not available as authoritative evidence.

## Exact physical artifact

- installed JAR: `somakespells-1.0.8-1.21.1-fix.jar`
- mod id/runtime: `somakespells` / `1.0.8`
- CurseForge project/file: `1461634 / 8417850`
- expected physical SHA-1: `b0ad94c1504709662bee2d08700375ccecbb5ec7`
- materialized artifact SHA-1: `b0ad94c1504709662bee2d08700375ccecbb5ec7`
- exact hash match: yes
- license posture: All Rights Reserved / read-only clean-room factual inspection

## Evidence runs

Evidence was isolated in non-merge PR #191.

- initial exact-registry audit: run `34659320633`;
- reachability/resource audit: run `34664093646`, artifact `10288333124`;
- targeted optional/config gate audit: run `34664411845`, artifact `10288675409`, HEAD `397e09e4bfd65f66b82b1b82151915a91c15148d`;
- each audit re-downloads File ID `8417850` and requires the physical SHA-1 before inspection.

## Exact registry topology

`com.somake.somakespells.registries.ModSpells` exposes a `DeferredRegister<AbstractSpell>`. The hash-matched artifact contains:

- **67** typed `DeferredHolder<AbstractSpell, ...>` spell fields;
- **67** unique `DeferredRegister.register(String, Supplier)` spell registrations;
- **67** standalone provider `*Spell` classes;
- no extra provider spell identity is added from localization-only text.

Exact registered IDs:

`combustion`, `ritual_flame`, `damned_demomans`, `eruption`, `fire_blast`, `firestorm_vortex`, `pumpkin_bomb`, `ignis_shield`, `incinerator_slash`, `abyssal_burn`, `fire_orbs`, `abyssal_orbs`, `apocalyptic_burst`, `earthbound`, `submerge`, `tidal_grasp`, `tsunami`, `tidal_dash`, `thunder_cloud`, `water_control`, `water_spear`, `hydro_slash`, `sea_serpent`, `sea_serpent_jet`, `storm_aura`, `water_ball`, `summon_zombie`, `lightning_spear`, `ender_corruption`, `phantom_barrage`, `overgrowth`, `permafrost`, `blessing`, `custodia_caeli`, `blessed_connection`, `guardian_connection`, `cursed_connection`, `blood_rush`, `blood_cut`, `bloody_legacy`, `bloodmark`, `fragmented_requiem`, `rose_secret`, `eldritch_gambit`, `chain_connection`, `evocation_fortitude`, `reverberation`, `slumber_melody`, `resonant_pulse`, `ram_tchum`, `jingle_bell`, `lightning_ball`, `lightning_dance`, `lightning_field`, `lightning_strike`, `lightning_cut`, `lightning_spark`, `lightning_swarm`, `lightning_lash`, `halberd_strike`, `mirror_strike`, `render_rush`, `axe_cleave`, `desert_wrath`, `soul_grab`, `spirit_empowerment`, `symmetry_empowerment`.

These are registry identities, not a claim that package/folder names equal canonical schools or that current numerical mechanics have been reconstructed.

## Optional registration gates

The static registry initializer has six optional-provider-gated registrations.

- `MOWZIE_LOADED = ModList.get().isLoaded("mowziesmobs")` gates `blessed_connection`, `guardian_connection`, `cursed_connection`.
- `ISS_LOADED = MagicFromTheEastCompat.isLoaded()` gates `mirror_strike`, `spirit_empowerment`, `symmetry_empowerment`.
- exact `MagicFromTheEastCompat.isLoaded()` calls `ModList.get().isLoaded("iss_magicfromtheeast")`.

The physical modlist contains `mowziesmobs` 1.8.2 and `iss_magicfromtheeast` 1.1.5. Therefore the current physical provider set satisfies both gates and all **67/67** registry identities are active.

## Spell-lock / usability gate

The exact artifact registers its general spec as `ModConfig.Type.COMMON` at `somakespells/general/common.toml`. `Config.ENABLE_SPELL_LOCK_SYSTEM` is declared under `enableSpellLockSystem` with code default **false**.

Provider behavior established narrowly by signatures/control flow:

- `PlayerSpellMastery.getUnlockedLevel(spellId)` returns `100` when the spell-lock config is false;
- when the config is true, it reads the provider-owned unlocked-level map;
- `MagicBlockHandler.onSpellPreCast` is server-side for non-creative players and cancels the cast when requested spell level exceeds that provider mastery;
- `SpellCommand.register` exists only when spell-lock is enabled and the top-level `/somake` command requires command permission level **2**.

The code default is **not** substituted for deployed pack state. No authoritative copy of `somakespells/general/common.toml` was found in the Black Arcana repository or supplied project files.

## Acquisition/reachability evidence

The artifact packages provider-native progression/acquisition surfaces including tier spellbooks, Grimoires, Upgrade Forge recipes/progression, loot modifiers and item/entity loot resources. Multiple provider spellbooks and runtime handlers refer directly to `ModSpells` identities. This proves real provider acquisition infrastructure, but the audit does not yet close an object-by-object survival path for all 67 spells.

Under `SEMANTIC-MAGIC-COVERAGE.md`, a current registry identity whose effective config/survival reachability is not closed remains `CONDITIONAL`. Therefore:

- exact registry inventory: **67**;
- active registry identities under current physical optional set: **67**;
- strict semantic contribution in Phase 2BF: **+0**;
- canonical global strict minimum remains **874**;
- structural component coverage remains **55/100**.

## Clean-room boundary

The artifact is All Rights Reserved. Retained evidence is limited to hash/metadata, archive/resource and registry IDs, class/member signatures and narrow gate/config control-flow facts needed to determine current identity/eligibility. No implementation body is copied, reconstructed or adapted; no source, texture, model, sound or upstream prose is incorporated into Black Arcana.

This audit does not create a stable Somake API. Any runtime adapter remains fail-closed until a provider-native boundary is proven. Iron's remains host casting/resource/cooldown authority; Somake remains authority for its own spells, charges and provider-specific progression; Black Arcana must not duplicate those runtimes or transfer them to RPG Skill Tree.
