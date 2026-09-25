# Somake Spells — current physical 1.0.9 / historical exact 1.0.8-fix audit

Status: `⚠️ CURRENT PHYSICAL 1.0.9 / PHYSICAL SHA-1 = EXACT PUBLISHER FILE 8867079 / EXACT 83-ID REGISTRY / CURRENT MOD-COMPOSITION REGISTRATION OUTCOME 83/83 / SPELL-LOCK DEFAULT FALSE / DEPLOYED HOST+LOCK CONFIG + SURVIVAL REACHABILITY OPEN / CONDITIONAL +0 / FAIL-CLOSED`

## Current installed identity — 1.0.9

Current sibling modlist authority rechecked at `Gustavaopere/neoforge-rpg-skilltree@af648d441441dde929cd49c5e18509347f06f09a` preserves the 1.0.9 physical line and supersedes the former 1.0.8-fix physical-line claim:

- JAR: `somakespells-1.0.9-1.21.1.jar`
- Mod id: `somakespells`
- Runtime: `1.0.9`
- Minecraft / loader: `1.21.1` / NeoForge
- Physical SHA-1: `171841ac9f802be9309ecc166c1d972ac6d404c0` — captured by the hash-bearing physical modlist checkpoint dated 2026-09-16 and equal to exact CurseForge File `8867079`
- CurseForge Project ID: `1461634`
- Exact File ID: `8867079`
- File date/type: `2026-09-12`, Release
- Curse Maven: `curse.maven:somake-spells-irons-spells-addon-1461634:8867079`
- Publisher: TeenLe
- License: `All Rights Reserved`
- Exact public source revision: **not located**
- Provider class: `SPELL PROVIDER / CONTENT + PROGRESSION ADDON`
- Casting substrate: Iron's Spells 'n Spellbooks

The previous exact physical SHA-1 `b0ad94c1504709662bee2d08700375ccecbb5ec7`, File ID `8417850` and 67-registry audit apply to **1.0.8-fix only**. They remain historical checkpoint evidence and must not be presented as the current 1.0.9 registry.

See [`CURRENT-1.0.9-REVALIDATION-CHECKLIST.md`](CURRENT-1.0.9-REVALIDATION-CHECKLIST.md) and [`PHYSICAL-1.0.9-FINGERPRINT-CHECKPOINT.md`](PHYSICAL-1.0.9-FINGERPRINT-CHECKPOINT.md).

## Historical Phase 2BF exact-artifact reconciliation — 1.0.8-fix

Phase 2AI correctly stopped at the publisher evidence ceiling. Phase 2BF supersedes only that technical ceiling by materializing the exact CurseForge/Curse Maven File ID `8417850` and requiring SHA-1 equality with the physical modlist: `b0ad94c1504709662bee2d08700375ccecbb5ec7`.

For the historical 1.0.8-fix artifact, clean-room inspection closed that artifact's spell registry at **67 provider registrations**: 67 `DeferredHolder<AbstractSpell, ...>` fields, 67 unique `DeferredRegister.register(String, Supplier)` spell IDs and 67 standalone provider `*Spell` classes. Six registrations are optional-provider gated: three by `ModList.isLoaded("mowziesmobs")` and three by `MagicFromTheEastCompat.isLoaded()`, whose exact implementation tests `ModList.isLoaded("iss_magicfromtheeast")`. At that historical checkpoint, both mod IDs were physically present, so all **67/67 registry identities were active under the then-current optional-provider set**. This statement does not prove the 1.0.9 registry.

That historical audit closed 1.0.8-fix registry identity, not 1.0.9 registry identity and not semantic reachability. Somake registers `enableSpellLockSystem` as a `COMMON` config in `somakespells/general/common.toml`; its code default is `false`, and `PlayerSpellMastery.getUnlockedLevel()` returns `100` while disabled. When enabled, the provider's `/somake` command surface is permission-level 2 and the pre-cast path can reject unlearned spell levels. The deployed pack's actual COMMON config value is not present in the repository or supplied project files, and complete object-level survival acquisition/reachability is not yet proven. Under the canonical ledger rule, the 67 identities therefore remain `CONDITIONAL` and contribute **+0** to the strict semantic sum.

See [`EXACT-1.0.8-FIX-ARTIFACT-AUDIT.md`](EXACT-1.0.8-FIX-ARTIFACT-AUDIT.md) and [`../../meta/PHASE2BF-SOMAKE-1.0.8-FIX-EXACT-CHECKPOINT.md`](../../meta/PHASE2BF-SOMAKE-1.0.8-FIX-EXACT-CHECKPOINT.md).

## Current public scope

The current publisher page describes Somake as adding **over 50 spells** with emphasis on Lightning, Fire, Aqua and Symmetry, plus Blood/Ender content and elemental `charges`, including addon element integrations.

It also documents a Somake **Aqua School** for 1.21.1, equipment/armor, evolving Grimoires, tier-book progression / Upgrade Forge from the release lineage and a Soul Fire / Infernal Fire ritual progression using Cataclysm's Altar of Ignis.

`50+` is a publisher scale statement, **not** a verified current registry count. The changelog history itself names more Blood content than the current page's simplified `1 Blood` summary would suggest, so school totals are not inferred from marketing prose.

## Historical exact 1.0.8-fix

File ID `8417850` is the historical 1.0.8-fix artifact. It repairs **Symmetry** and **Spirit Elemental Charges**, which were not applying their buffs.

This proves those charge surfaces for the 1.0.8-fix artifact only. It does not establish their current 1.0.9 registry state, internal IDs, formulas, stack rules, persistence or API.

## Catalog files

- [PUBLIC-NAMED-SPELLS.md](PUBLIC-NAMED-SPELLS.md) — spell names explicitly demonstrated by publisher changelogs, with current-line vs historical states;
- [PUBLIC-CHANGELOG-AUDIT.md](PUBLIC-CHANGELOG-AUDIT.md) — release-by-release 1.0.x evidence;
- [PROGRESSION-EQUIPMENT.md](PROGRESSION-EQUIPMENT.md) — books, Grimoires, Upgrade Forge, ritual path and equipment;
- [TECHNICAL-AUDIT.md](TECHNICAL-AUDIT.md) — exact artifact/provenance/dependency/QA boundary;
- [CURRENT-1.0.9-REVALIDATION-CHECKLIST.md](CURRENT-1.0.9-REVALIDATION-CHECKLIST.md) — authoritative current-line closure gates for 1.0.9;
- [EXACT-1.0.9-RESOURCE-AUDIT.md](EXACT-1.0.9-RESOURCE-AUDIT.md) — exact publisher-release hash/metadata/resource evidence for 1.0.9;\n- [EXACT-1.0.9-REGISTRY-AUDIT.md](EXACT-1.0.9-REGISTRY-AUDIT.md) — exact hash-matched physical/release registry closure: 83 declared IDs, +17/-1 delta, current optional-registration topology and host override facts;\n- [EXACT-1.0.9-REGISTRATION-GATE-MAP.md](EXACT-1.0.9-REGISTRATION-GATE-MAP.md) — exact 67 unconditional + 16 optional-provider-gated mapping and current-pack 83/83 registration outcome;\n- [SPELL-CATALOG-1.0.9.md](SPELL-CATALOG-1.0.9.md) — current 83-ID registry inventory; active by current mod composition but not yet strict-counted;
- [EXACT-1.0.8-FIX-ARTIFACT-AUDIT.md](EXACT-1.0.8-FIX-ARTIFACT-AUDIT.md) — historical 1.0.8-fix hash-matched registry/gate/config facts;
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

### Latest explicit provider-stack physical checkpoint

The following presence list is preserved from the latest complete provider-stack physical checkpoint used by this dossier. The sibling's current reorganized certification index is being rebuilt in physical-order batches and is not treated as an absence authority for entries it has not yet reached.

Present at that checkpoint:

- Iron's Spells 'n Spellbooks `1.21.1-3.16.3`;
- L_Ender's Cataclysm `3.33`;
- Apothic Attributes `2.10.1`;
- Magic From the East / `iss_magicfromtheeast` `1.1.5`;
- Born in Chaos `1.7.6`;
- GTBC's Geomancy Plus `1.1.0-1.21.1`;
- Tunes 'n Tomes `1.1.0-HOTFIX`;
- Mowzie's Mobs `1.8.2`;
- T.O Magic n' Extras / `traveloptics` `4.4.0.1-1.21.1`.

Not located at that checkpoint:

- Better Combat.

Exact 1.0.9 clean-room registration-gate audit now closes the current predicate topology rather than carrying forward 1.0.8 assumptions. `ModSpells` caches exactly three registration booleans: `MOWZIE_LOADED` from `ModList.isLoaded("mowziesmobs")`, `ISS_LOADED` from `MagicFromTheEastCompat.isLoaded()`, and `LEGENDARY_MONSTERS_LOADED` from `LegendaryMonstersCompat.isLoaded()`. The exact ID mapping is preserved in [`EXACT-1.0.9-REGISTRATION-GATE-MAP.md`](EXACT-1.0.9-REGISTRATION-GATE-MAP.md).

The current pack contains all three required providers — Mowzie's Mobs, ISS: Magic From The East and Legendary Monsters — so the current mod-composition registration outcome is **83/83 declared Somake spell IDs active by registration predicate**. This closes registration composition only. It does not establish effective Iron's `enabled` / `allow_crafting`, deployed Somake spell-lock state or survival acquisition.

## Aqua / T.O Magic coexistence

Somake states that Aqua was created to cover the absence of Aqua/T.O Magic on 1.21.1 and that its Aqua content would migrate if T.O Magic officially updated.

At the same explicit physical checkpoint, the pack contains `traveloptics-4.4.0.1-1.21.1.jar`; the T.O Magic publisher labels that 1.21.1 build **`DEPRECATED DONT USE Alpha-4.4.0.1-1.21.1`**.

Therefore Somake Aqua and the T.O Magic alpha were both physically present at that checkpoint, but the historical migration statement does **not** prove that authority migrated to this deprecated alpha. Duplicate school/registry/runtime interaction is a live QA blocker.

Until runtime/API evidence resolves it, Black Arcana must not select one provider's Aqua identity by assumption or create another Aqua pipeline.

## Publicly named current-line spell evidence

The exact 1.0.9 File `8867079` changelog explicitly publishes **16 spell names** in its **New Spells** section: ten Spirit/Evocation, one Holy, one Sound, one Aqua and three Blood. These names and publisher-level semantics are materialized separately in [`CURRENT-1.0.9-PUBLIC-NAMED-SPELLS.md`](CURRENT-1.0.9-PUBLIC-NAMED-SPELLS.md).

That ledger remains naming/semantic provenance only. Registry identity is now closed separately by the exact 1.0.9 structural audit at **83 declared IDs**; publisher names/localization still do not establish school mechanics, active deployed registration, host enablement or survival reachability.

## Authority / deduplication

Somake owns its provider-specific spell semantics, Aqua/Symmetry content it registers, Elemental Charges, tier-book/Grimoire/Upgrade Forge progression, Soul Fire/Infernal Fire ritual progression and item/equipment evolution.

Black Arcana must not create a parallel Somake charge ledger, duplicate provider ritual completion/rewards, write guessed Somake school/spell IDs, duplicate generic Water Control/damage-link/heal-link/blood-zone/fire-vortex mechanics without a material forbidden-magic delta, or transfer Somake runtime authority to RPG Skill Tree.

RPG Skill Tree may provide progression/mastery/perks only through a real contract. It does not own Somake casting/resources or Black Arcana magic runtime.

## Evidence ceiling

- current installed filename/runtime — `HIGH`, sibling modlist identifies `somakespells-1.0.9-1.21.1.jar` / runtime `1.0.9`;
- exact 1.0.9 publisher release identity/hash — `HIGH`, File `8867079` / SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0`;
- current physical-pack byte equality to that release — `HIGH / HASH-MATCHED`: physical SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0` equals exact File `8867079`; this closes artifact equality but not the assembled active subset, config or reachability;
- exact current 1.0.9 physical/release registry declaration — `HIGH / HASH-MATCHED`: 83 fields + 83 register calls + 83 unique IDs + 83 top-level spell classes;
- exact current 1.0.9 optional-registration mapping — `HIGH / EXACT-BINARY`: 67 unconditional IDs + 16 unique conditional IDs gated only by Mowzie's Mobs, ISS: Magic From The East and/or Legendary Monsters;
- current-pack registration outcome — `HIGH / COMPOSITION-CLOSED`: all three registration-gate providers are physically installed, therefore 83/83 declared IDs satisfy Somake's own registration predicates in the current pack;
- `enableSpellLockSystem` symbol + `somakespells/general/common.toml` path + code default — `CURRENT 1.0.9 REVALIDATED`; exact boolean default is `false`, while the effective deployed value remains open;
- deployed value of the relevant current COMMON config — `UNVERIFIED`;
- complete object-level survival acquisition/reachability — `UNVERIFIED / CONDITIONAL`;
- values/formulas/stable integration API/hooks/networking/persistence — `UNVERIFIED / FAIL-CLOSED` except for narrow facts explicitly recorded by the artifact audit;
- Somake↔T.O Aqua authority on the current dual-installed stack — `RUNTIME QA REQUIRED`.

The ARR artifact was inspected only to retain factual hash/metadata, resource/registry identities, class/member signatures and narrow control-flow/config predicates needed for catalog interoperability. No implementation body, source reconstruction, asset, model, sound or upstream prose is copied/adapted or treated as reusable material.