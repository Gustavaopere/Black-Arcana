# Somake Spells 1.0.8-fix

Status: `EXACT-ARTIFACT-PINNED / PUBLISHER 50+ SCALE / PUBLIC CHANGELOG CATALOG ADVANCED / COMPLETE REGISTRY+API PENDING / FAIL-CLOSED`

## Installed identity

- JAR: `somakespells-1.0.8-1.21.1-fix.jar`
- Mod id: `somakespells`
- Runtime: `1.0.8`
- Minecraft / loader: `1.21.1` / NeoForge
- Physical SHA-1: `b0ad94c1504709662bee2d08700375ccecbb5ec7`
- CurseForge Project ID: `1461634`
- Exact File ID: `8417850`
- File date/type: `2026-07-12`, Release
- Curse Maven: `curse.maven:somake-spells-irons-spells-addon-1461634:8417850`
- Publisher: TeenLe
- License: `All Rights Reserved`
- Exact public source revision: **not located**
- Provider class: `SPELL PROVIDER / CONTENT + PROGRESSION ADDON`
- Casting substrate: Iron's Spells 'n Spellbooks

Physical modlist evidence is authoritative for installed filename/mod id/runtime/hash. Publisher release metadata confirms the exact 1.0.8-fix line.

## Current public scope

The current publisher page describes Somake as adding **over 50 spells** with emphasis on Lightning, Fire, Aqua and Symmetry, plus Blood/Ender content and elemental `charges`, including addon element integrations.

It also documents a Somake **Aqua School** for 1.21.1, equipment/armor, evolving Grimoires, tier-book progression / Upgrade Forge from the release lineage and a Soul Fire / Infernal Fire ritual progression using Cataclysm's Altar of Ignis.

`50+` is a publisher scale statement, **not** a verified current registry count. The changelog history itself names more Blood content than the current page's simplified `1 Blood` summary would suggest, so school totals are not inferred from marketing prose.

## Exact installed fix

File ID `8417850` is a small fix over 1.0.8. It repairs **Symmetry** and **Spirit Elemental Charges**, which were not applying their buffs.

This proves those charge surfaces in the installed release line, but does not publish their internal IDs, formulas, stack rules, persistence or API.

## Catalog files

- [PUBLIC-NAMED-SPELLS.md](PUBLIC-NAMED-SPELLS.md) — spell names explicitly demonstrated by publisher changelogs, with current-line vs historical states;
- [PUBLIC-CHANGELOG-AUDIT.md](PUBLIC-CHANGELOG-AUDIT.md) — release-by-release 1.0.x evidence;
- [PROGRESSION-EQUIPMENT.md](PROGRESSION-EQUIPMENT.md) — books, Grimoires, Upgrade Forge, ritual path and equipment;
- [TECHNICAL-AUDIT.md](TECHNICAL-AUDIT.md) — exact artifact/provenance/dependency/QA boundary;
- [INTEGRATION-RULES.md](INTEGRATION-RULES.md) — Black Arcana authority and fail-closed rules.

School directories already present in this provider tree remain organizational placeholders until exact current membership can be proven. Historical changelog school labels do not justify manufacturing a complete school-first registry.

## Publisher compatibility — 1.21.1

Current description:

- L_Ender's Cataclysm — required;
- Apothic Attributes — required;
- Magic From the East — optional;
- Born in Chaos — optional;
- Geomancy Plus — optional;
- Tunes 'n Tomes — optional.

The 1.0.8 changelog explicitly says Magic From the East and Born in Chaos are **no longer mandatory**, which prevails over stale/generic relation metadata.

### Current physical pack

Present:

- Iron's Spells 'n Spellbooks `1.21.1-3.16.3`;
- L_Ender's Cataclysm `3.33`;
- Apothic Attributes `2.10.1`;
- Magic From the East / `iss_magicfromtheeast` `1.1.5`;
- Born in Chaos `1.7.6`;
- GTBC's Geomancy Plus `1.1.0-1.21.1`;
- Tunes 'n Tomes `1.1.0-HOTFIX`;
- Mowzie's Mobs `1.8.2`;
- T.O Magic n' Extras / `traveloptics` `4.4.0.1-1.21.1`.

Not located in the physical modlist:

- Better Combat.

Presence satisfies a compatibility precondition only; it is not evidence that every optional integration path is runtime-active. Because Magic From the East is physically present, the publisher-described **Symmetry integration path is eligible**; exact active spells/IDs still require runtime/config evidence.

## Aqua / T.O Magic coexistence

Somake states that Aqua was created to cover the absence of Aqua/T.O Magic on 1.21.1 and that its Aqua content would migrate if T.O Magic officially updated.

The current pack does contain `traveloptics-4.4.0.1-1.21.1.jar`, but the T.O Magic publisher currently labels that 1.21.1 build **`DEPRECATED DONT USE Alpha-4.4.0.1-1.21.1`**.

Therefore Somake Aqua and the T.O Magic alpha are both physically present, but the historical migration statement does **not** prove that authority migrated to this deprecated alpha. Duplicate school/registry/runtime interaction is a live QA blocker.

Until runtime/API evidence resolves it, Black Arcana must not select one provider's Aqua identity by assumption or create another Aqua pipeline.

## Publicly named current-line spell evidence

1.0.8 directly adds/references Ritual Flame, Custodia Caeli, Bloody Legacy, Fragmented Requiem, The Rose's Secret, Jingle Bell, Chain Connection (moved to Aqua), Fire Orbs (rework) and Ignis Shield (rework).

1.0.7 publicly introduced Guardian/Blessed/Cursed Connection, Bloodmark, Water Control and Firestorm Vortex. Those older names remain separately marked `CURRENT REGISTRY UNVERIFIED` unless 1.0.8 re-confirms them.

1.0.6 explicitly removed Tsunami and renamed Tidal Grasp/Dash to Ceraunus Grasp/Dash.

See the dedicated inventory for exact evidence posture. None of these names imply registry IDs or values.

## Authority / deduplication

Somake owns its provider-specific spell semantics, Aqua/Symmetry content it registers, Elemental Charges, tier-book/Grimoire/Upgrade Forge progression, Soul Fire/Infernal Fire ritual progression and item/equipment evolution.

Black Arcana must not create a parallel Somake charge ledger, duplicate provider ritual completion/rewards, write guessed Somake school/spell IDs, duplicate generic Water Control/damage-link/heal-link/blood-zone/fire-vortex mechanics without a material forbidden-magic delta, or transfer Somake runtime authority to RPG Skill Tree.

RPG Skill Tree may provide progression/mastery/perks only through a real contract. It does not own Somake casting/resources or Black Arcana magic runtime.

## Evidence ceiling

- installed identity/hash — `HIGH`, physical modlist;
- exact File ID/release/fix semantics — `HIGH`, publisher;
- 50+ scale / Aqua / equipment / compatibility — `HIGH` at public feature level;
- changelog names/semantics — `HIGH` for the release in which they are stated;
- exact current complete spell list — `UNVERIFIED`;
- registry IDs/classes/values/config defaults/acquisition/API/hooks/networking/persistence — `UNVERIFIED / FAIL-CLOSED`;
- Somake↔T.O Aqua authority on the current dual-installed stack — `RUNTIME QA REQUIRED`.

No source code or bytecode implementation details are treated as reusable material.