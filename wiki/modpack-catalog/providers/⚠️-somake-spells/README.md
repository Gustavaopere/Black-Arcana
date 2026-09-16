# Somake Spells 1.0.8-fix

Status: `EXACT HASH-MATCHED 1.0.8-FIX ARTIFACT / 67 CURRENT REGISTRY IDENTITIES CLOSED UNDER PHYSICAL OPTIONAL SET / SURVIVAL REACHABILITY + EFFECTIVE COMMON CONFIG UNVERIFIED / CONDITIONAL +0 / FAIL-CLOSED`

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

## Phase 2BF exact-artifact reconciliation

Phase 2AI correctly stopped at the publisher evidence ceiling. Phase 2BF supersedes only that technical ceiling by materializing the exact CurseForge/Curse Maven File ID `8417850` and requiring SHA-1 equality with the physical modlist: `b0ad94c1504709662bee2d08700375ccecbb5ec7`.

Clean-room inspection closes the current spell registry at **67 provider registrations**: 67 `DeferredHolder<AbstractSpell, ...>` fields, 67 unique `DeferredRegister.register(String, Supplier)` spell IDs and 67 standalone provider `*Spell` classes. Six registrations are optional-provider gated: three by `ModList.isLoaded("mowziesmobs")` and three by `MagicFromTheEastCompat.isLoaded()`, whose exact implementation tests `ModList.isLoaded("iss_magicfromtheeast")`. Both mod IDs are physically present, so all **67/67 registry identities are active under the current physical optional-provider set**.

That closes registry identity, not semantic reachability. Somake registers `enableSpellLockSystem` as a `COMMON` config in `somakespells/general/common.toml`; its code default is `false`, and `PlayerSpellMastery.getUnlockedLevel()` returns `100` while disabled. When enabled, the provider's `/somake` command surface is permission-level 2 and the pre-cast path can reject unlearned spell levels. The deployed pack's actual COMMON config value is not present in the repository or supplied project files, and complete object-level survival acquisition/reachability is not yet proven. Under the canonical ledger rule, the 67 identities therefore remain `CONDITIONAL` and contribute **+0** to the strict semantic sum.

See [`EXACT-1.0.8-FIX-ARTIFACT-AUDIT.md`](EXACT-1.0.8-FIX-ARTIFACT-AUDIT.md) and [`../../meta/PHASE2BF-SOMAKE-1.0.8-FIX-EXACT-CHECKPOINT.md`](../../meta/PHASE2BF-SOMAKE-1.0.8-FIX-EXACT-CHECKPOINT.md).

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
- [EXACT-1.0.8-FIX-ARTIFACT-AUDIT.md](EXACT-1.0.8-FIX-ARTIFACT-AUDIT.md) — hash-matched registry/gate/config facts from the installed binary;
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

Presence alone is not generally enough to prove an optional integration path. For the six conditionally registered Somake spells, however, the exact 1.0.8-fix bytecode closes the predicates themselves: `mowziesmobs` gates Blessed/Guardian/Cursed Connection and `iss_magicfromtheeast` gates Mirror Strike/Spirit Empowerment/Symmetry Empowerment. Both predicates are true under the current physical modlist, so those six registrations join the 61 unconditional registrations for 67/67 current registry identities. Runtime behavior, acquisition and config-dependent usability remain separate.

## Aqua / T.O Magic coexistence

Somake states that Aqua was created to cover the absence of Aqua/T.O Magic on 1.21.1 and that its Aqua content would migrate if T.O Magic officially updated.

The current pack does contain `traveloptics-4.4.0.1-1.21.1.jar`, but the T.O Magic publisher currently labels that 1.21.1 build **`DEPRECATED DONT USE Alpha-4.4.0.1-1.21.1`**.

Therefore Somake Aqua and the T.O Magic alpha are both physically present, but the historical migration statement does **not** prove that authority migrated to this deprecated alpha. Duplicate school/registry/runtime interaction is a live QA blocker.

Until runtime/API evidence resolves it, Black Arcana must not select one provider's Aqua identity by assumption or create another Aqua pipeline.

## Publicly named current-line spell evidence

The publisher changelog files remain provenance for names and release semantics, but they no longer define the registry ceiling. The exact 1.0.8-fix artifact now supplies the complete 67-ID registry inventory in `EXACT-1.0.8-FIX-ARTIFACT-AUDIT.md`. Historical naming contradictions remain useful for editorial provenance and must not be substituted for current bytecode-backed IDs, school mechanics or numerical values.

## Authority / deduplication

Somake owns its provider-specific spell semantics, Aqua/Symmetry content it registers, Elemental Charges, tier-book/Grimoire/Upgrade Forge progression, Soul Fire/Infernal Fire ritual progression and item/equipment evolution.

Black Arcana must not create a parallel Somake charge ledger, duplicate provider ritual completion/rewards, write guessed Somake school/spell IDs, duplicate generic Water Control/damage-link/heal-link/blood-zone/fire-vortex mechanics without a material forbidden-magic delta, or transfer Somake runtime authority to RPG Skill Tree.

RPG Skill Tree may provide progression/mastery/perks only through a real contract. It does not own Somake casting/resources or Black Arcana magic runtime.

## Evidence ceiling

- installed identity/hash — `HIGH`, physical modlist + exact artifact hash match;
- exact File ID/release/fix semantics — `HIGH`, publisher;
- exact current spell registry — `HIGH`, 67/67 IDs closed from the hash-matched artifact under the physical optional-provider set;
- exact optional registry predicates — `HIGH`, `mowziesmobs` and `iss_magicfromtheeast`, both physically satisfied;
- `enableSpellLockSystem` code default/path — `HIGH`, default `false`, `COMMON`, `somakespells/general/common.toml`;
- deployed value of that COMMON config — `UNVERIFIED`;
- complete object-level survival acquisition/reachability — `UNVERIFIED / CONDITIONAL`;
- values/formulas/stable integration API/hooks/networking/persistence — `UNVERIFIED / FAIL-CLOSED` except for narrow facts explicitly recorded by the artifact audit;
- Somake↔T.O Aqua authority on the current dual-installed stack — `RUNTIME QA REQUIRED`.

The ARR artifact was inspected only to retain factual hash/metadata, resource/registry identities, class/member signatures and narrow control-flow/config predicates needed for catalog interoperability. No implementation body, source reconstruction, asset, model, sound or upstream prose is copied/adapted or treated as reusable material.