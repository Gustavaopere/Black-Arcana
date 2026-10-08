# Reconciliação física do ledger de magia — 2026-10-08

Status: `VERSION/IDENTITY RECONCILIATION COMPLETE FOR CURRENT COUNTED-LEDGER PROVIDERS; NO JAR-BYTE OR DEPLOYMENT CLAIM`

## Authority and procedure

- Sibling index: [PROJECT-INSTRUCTIONS/modlist/modlist.md](https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/de80b186357cad20ba5b81892a8682777e96e35a/PROJECT-INSTRUCTIONS/modlist/modlist.md), `neoforge-rpg-skilltree@de80b186357cad20ba5b81892a8682777e96e35a`.
- Black Arcana base: `main@e4d001e05a1e45a24136e8b6582096e9ea71ceff`.
- Ledger source: [SEMANTIC-MAGIC-COVERAGE.md](SEMANTIC-MAGIC-COVERAGE.md), counted-ledger rows as recorded at the base commit.
- Identity matching uses exact normalized display names or **explicit, checked aliases**; never substring matching. This prevents false matches such as Wind's Spellbooks versus IronSable X Wind's Spellbooks, or Vampirism versus Bloodlines.
- Version test confirms that **every explicitly stated numeric version token** in the ledger line appears in the physical index's runtime/distribution version string or exact JAR filename (including deliberately different distribution/embedded metadata versions). It is a **declared-version consistency check**, not a binary hash, loaded registry or source-build equivalence proof.

## Results

- Physical index: **587 numbered top-level entries**, including modloader (its documented post-snapshot additions and replacement request are not silently promoted to a newer physical dump).
- Counted ledger: **71 named provider rows**, comprising **69 uniquely matched currently installed providers** and **2 historically cataloged providers absent from the certified physical snapshot**.
- **0 declared-version-token conflicts** among the 69 uniquely mapped installed providers.
- **No magic-count change** from this reconciliation. The current user's explicitly scoped minimum remains **1849**. The global repo minimum **1851** includes two counted Deeper and Darker base actions, which are outside this user's requested scope; Traveloptics adds zero to the strict count.
- NeoForge physical modloader is **21.1.250**, index row `#001`; Black Arcana's `gradle.properties` uses **21.1.248** as its compile/dev baseline. This distinction is recorded, **not** treated as a validated incompatibility or license to silently alter the build.

## Exact-current physical crosswalk

| Counted provider | Physical index | Installed top-level JAR | Physical declared version | Ledger version / provenance |
|---|---:|---|---|---|
| Ars Nouveau | #047 | `ars_nouveau-1.21.1-5.13.1.jar` | 5.13.1 | 5.13.1 |
| StarbuncleMania | #527 | `starbunclemania-1.21.1-1.5.8.jar` | 1.5.8 | 1.5.8 |
| Ars Additions | #040 | `ars_additions-1.21.1-21.3.0.jar` | 1.21.1-21.3.0 | 21.3.0 |
| Ars Controle | #041 | `ars_controle-1.21.1-1.6.16.jar` | 1.21.1-1.6.16 | 1.6.16 |
| Ars Technica | #050 | `ars_technica-1.21.1-2.7.6.jar` | 2.7.6 | 2.7.6 |
| Ars Hex | #045 | `ars_hex-1.21.1-5.0.4b.jar` | 5.0.4b | 5.0.4b |
| Ars Zero | #052 | `ars_zero-1.21.1-2.0.2.jar` | 2.0.2 | 2.0.2 |
| Ars Elemental | #044 | `ars_elemental-1.21.1-0.7.10.1.jar` | 0.7.10.1 | 0.7.10.1 |
| Ars 'n' Spells | #046 | `ars_n_spells-3.3.4.jar` | 3.3.4 | 3.3.4 |
| Iron's Spells 'n Spellbooks | #342 | `irons_spellbooks-1.21.1-3.16.3.jar` | 1.21.1-3.16.3 | 3.16.3 |
| Apprentice's Codex | #038 | `apprentice_codex-0.9.7.1+mc1.21.1.jar` | 0.9.7.1 | 0.9.7.1 |
| Asterism Arcanum | #056 | `asterismarcanum-1.21.1-0.1.0.jar` | 1.21.1-0.1.0 | 1.21.1-0.1.0 |
| Backported Spellbooks | #063 | `backportedspellbooks-0.1.2.jar` | 0.1.2 (distribuição/filename); metadata runtime 0.1.0 | physical 0.1.2 / embedded 0.1.0 |
| Deeper & Darker Spellbooks | #214 | `darkermagic-1.3.3-1.21.1-ver.b.jar` | 1.3.3-1.21.1 | 1.3.3 Version B |
| Discerning The Eldritch | #220 | `discerning_the_eldritch-1.4.4-1.21.jar` | 1.4.4-1.21 | 1.4.4 |
| Dreamless Spells | #225 | `dreamless_spells-1.1.9.jar` | 1.1.9 | 1.1.9 |
| GTBC's Geomancy Plus | #309 | `gtbcs_geomancy_plus-1.1.0-1.21.1.jar` | 1.1.0-1.21.1 | 1.1.0-1.21.1 |
| Farmer's Spell 'n Spellbooks | #275 | `farmers-spell-n-spellbook-1.0.5.1-1.21.1.jar` | 1.0.5.1-1.21.1 | 1.0.5.1-1.21.1 |
| SnackPirate's Aeromancy Additions | #009 | `aero_additions-1.2.8.jar` | 1.2.8 | 1.2.8 |
| Hazen N Stuff | #312 | `hazennstuff-1.4.0.14.jar` | 1.4.0.14 | 1.4.0.14 |
| Ender's Spells and Stuff: Requiem | #265 | `ess_requiem-0.1.7.jar` | 0.1.7 | 0.1.7 |
| Fire's Ender Expansion | #281 | `firesenderexpansion-2.4.1.jar` | 2.4.1 | 2.4.1 |
| IronSable | #344 | `ironsable-1.2.0.jar` | 1.2.0 | 1.2.0 |
| ISS: Magic From The East | #346 | `iss_magicfromtheeast-1.1.5.jar` | 1.1.5 | 1.1.5 |
| Legendary Spellbooks | #372 | `legendary_spellbooks-1.21.1+neo-0.3.2.jar` | 0.3.2 | 0.3.2 |
| Monsters & Spellbooks | #406 | `monsterspellbooks-0.0.16.3.jar` | 0.0.16.3 | 0.0.16.3 |
| Paladin Spells | #432 | `paladin_spells-1.21.1-1.1.1.jar` | 1.21.1-1.1.1 | 1.1.1 |
| Wind's Spellbooks | #571 | `wind_spellbooks-1.0.5.jar` | 1.0.5 | 1.0.5 |
| Ypsilon's Fundamentalism | #575 | `ypfundamentals-1.1.7.1.jar` | 1.1.7.1 | 1.1.7.1 |
| Tunes n' Tomes | #552 | `tunes_n_tomes-1.1.0-HOTFIX.jar` | 1.1.0-HOTFIX | 1.1.0-HOTFIX |
| Alshanex's Familiars | #023 | `alshanex_familiars-1.21.1_v4.0.3.jar` | 1.21.1_v4.0.3 | 4.0.3 |
| Companions! | #104 | `companions-neoforge-1.21.1-1.3.4.jar` | 1.3.4 | 1.3.4 |
| Crystal Chronicles | #208 | `crystal_chronicles-0.1.3-alpha.jar` | 0.1.3-alpha | 0.1.3-alpha |
| Cataclysm: Spellbooks | #087 | `cataclysm_spellbooks-1.1.14-1.21.jar` | 1.1.14-1.21 | 1.1.14 |
| Leyline Spellbooks | #373 | `leylines-1.0.3.jar` | 1.0.3 | 1.0.3 |
| Ozymandias Sundries | #431 | `ozymandias_sundries-0.0.5.jar` | 0.0.5 (distribuição/publicação); metadata interna 0.0.1 | physical 0.0.5 / embedded 0.0.1 |
| Gaze | #300 | `gaze-1.1.7.1.jar` | 1.1.7.1 | 1.1.7.1 |
| Relics | #474 | `relics-1.21.1-0.12.8.jar` | 0.12.8 | 0.12.8 |
| More Relics | #408 | `morerelics-1.7.7-forRelics-0.12.8-1.0-1.21.1.jar` | 1.7.7-forRelics-0.12.8-1.0 | 1.7.7-forRelics-0.12.8-1.0 |
| Mowzie's Mobs | #411 | `mowziesmobs-1.21.1-1.8.2.jar` | 1.8.2 | 1.8.2 |
| Ice And Fire CE | #316 | `iceandfire-2.1.2.jar` | 2.1.2 | 2.1.2 |
| L_Ender's Cataclysm | #368 | `L_Ender's Cataclysm 1.21.1-3.33.jar` | 3.33 | 3.33 |
| BetterEnd: New Dawn | #071 | `BetterEnd-21.0.34.jar` | 21.0.34 | 21.0.34 |
| Weapons of Miracles | #568 | `WeaponsOfMiracles-2.0.178.jar` | 2.0.178 | 2.0.178 |
| Epic Fight | #260 | `epic-fight-21.17.3.1-mc1.21.1-neoforge.jar` | 21.17.3.1 | 21.17.3.1 |
| Born in Chaos | #084 | `born_in_chaos_[Neoforge]_1.21.1_1.7.6.jar` | 1.7.6 | 1.7.6 |
| Bosses'Rise | #079 | `block_factorys_bosses-2.1.2-neo-1.21.1.jar` | 2.1.2 | 2.1.2 |
| Portable Hole | #452 | `PortableHole-v21.1.0-1.21.1-NeoForge.jar` | 21.1.0 | 21.1.0 |
| Legendary Monsters | #371 | `legendary_monsters-2.2.2 MC 1.21.1.jar` | 2.2.2 (distribuição); metadata interna 1.21.1 | 2.2.2 |
| Alex's Caves Continued | #019 | `alexscaves-1.0.10-neoforge+1.21.1.jar` | 1.0.10 | 1.0.10 |
| Alex's Mobs Continued | #021 | `alexsmobs-2.1.13-neoforge+1.21.1.jar` | 2.1.13 | 2.1.13 |
| Ice And Fire: Dread Land | #318 | `iceandfire_dreadland-0.1.2.jar` | 0.1.2 | 0.1.2 |
| Bosses of Mass Destruction | #082 | `BOMD-NeoForge-1.21-1.3.3.jar` | 1.3.3 | 1.3.3 |
| Cataclysm: Ignis Soulfires | #323 | `ignissoulfires-1.8.0.jar` | 1.8.0 | 1.8.0 |
| Reliquified Ars Nouveau | #476 | `reliquified_ars_nouveau-1.21.1-0.8.1.jar` | 0.8.1 | 0.8.1 |
| Reliquified Artifacts | #477 | `reliquified_artifacts-1.21.1-1.0.8.jar` | 1.0.8 | 1.0.8 |
| Reliquified Iron's Spells 'n Spellbooks | #478 | `reliquified_irons_spells_and_spellbooks-1.21.1-0.2.7.jar` | 0.2.7 | 0.2.7 |
| Reliquified L_Ender's Cataclysm | #479 | `reliquified_lenders_cataclysm-1.21.1-0.1.1.jar` | 0.1.1 | 0.1.1 |
| Waystones | #564 | `waystones-neoforge-1.21.1-21.1.45.jar` | 21.1.45 | 21.1.45 |
| Corail Tombstone | #544 | `tombstone-neoforge-1.21.1-9.5.6.jar` | 9.5.6 | 9.5.6 |
| Goety | #305 | `goety-3.1.4.jar` | 3.1.4 | 3.1.4 |
| Goety Iron | #307 | `GoetyIron-1.21.1-NeoForge-3.1.jar` | 3.1 | 3.1 |
| Goety Cataclysm | #306 | `goety_cataclysm-1.21.1-1.8.2.jar` | 1.21.1-1.8.2 | 1.21.1-1.8.2 |
| Eidolon: Repraised | #246 | `eidolon_repraised-1.21.1-0.5.0.2.jar` | 0.5.0.2 | 0.5.0.2 |
| Vampirism | #558 | `Vampirism-1.21-1.10.13.jar` | 1.10.13 | 1.10.13 |
| Bloodlines | #081 | `bloodlines-1.21-3.0.9.jar` | 1.21-3.0.9 | 3.0.9 |
| Werewolves | #570 | `Werewolves-1.21-2.0.3.3.jar` | 2.0.3.3 | 2.0.3.3 |
| Hexalia | #314 | `hexalia-neoforge-1.3.7.jar` | 1.3.7 | 1.3.7 |
| Malum | #389 | `malum-1.21.1-1.8.2.jar` | 1.8.2 | 1.8.2 |

## Historical catalogs excluded from current physical sum

| Provider | Prior catalog version | Current physically mapped row | Disposition |
|---|---|---|---|
| Ars Morph | 2.0.0 | None | `CURRENT_PHYSICAL_ABSENT`, +0 current strict |
| Woodwalkers SpellBooks | 0.3.1-BETA | None | `CURRENT_PHYSICAL_ABSENT`, +0 current strict |

## Boundaries and remaining work

1. **Version present does not mean source or binary exactness**. `COUNTED_SOURCE_PINNED` and `COUNTED_RELEASE_BOUNDED` records keep their declared evidentiary class. Do not upgrade them to `COUNTED_EXACT` because a matching JAR name exists.
2. **Config/reachability does not become PASS**. Somake, Not Enough Glyphs, Gaze, Simply Swords, ShadowsZ and the other conditional provider rows still require deployed effective config/survival evidence.
3. The index is the latest certified snapshot; it includes post-snapshot changes as **editorial notes** only. No full physical rescan was performed in this reconciliation.
4. This crosswalk is anchored to the explicit dated git SHAs above; changes in either repository require regeneration and exact diff comparison rather than a silent carry-forward.
5. The full strict semantic denominator remains unknown. No percentage or 100% semantic-coverage claim is justified.
