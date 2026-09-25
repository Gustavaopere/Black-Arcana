# Iron's Apothic — 2.2.2

Status: `CURRENT PHYSICAL COMPONENT / EXACT SOURCE-PINNED MAGIC BRIDGE / 7 CUSTOM AFFIX CODECS / 140 AFFIX DATA DEFINITIONS / 48 SPELL-TRIGGER OR IMBUED SPELL AFFIX DEFINITIONS / 24 GEM DEFINITIONS / ZERO PROVIDER-OWNED SPELL REGISTRATIONS / +0 STRICT SPELL-SEMANTIC / RUNTIME QA FAIL-CLOSED`

## Current physical identity

The current sibling authority at `neoforge-rpg-skilltree@c3de5878d69a7a6b4441606ef2b9e96a61a8f2e9` preserves the certified row:

- physical/index row: **#339**;
- project: **Apotheosis x Iron's Spellbooks Compat / Iron's Apothic**;
- JAR: `irons_apothic-2.2.2.jar`;
- mod id: `irons_apothic`;
- runtime version: `2.2.2`;
- Minecraft: 1.21.1 / NeoForge.

Certified sibling dossier:

`PROJECT-INSTRUCTIONS/modlist/Adventure and RPG + Armor, Tools, and Weapons + Magic/✅-irons-apothic v2.2.2.md`

The current sibling dossier does not preserve an independent installed-JAR digest, so no byte-for-byte physical ↔ source/release equality is claimed.

## Exact source pin

Official source:

`muon-rw/Apotheosis-Irons-Spells@c5d501219cc9bbbfb8c69acc08bebac76983d1c1`

The exact commit message is `2.2.2`. Its `gradle.properties` declares:

- `mod_id=irons_apothic`;
- `mod_version=2.2.2`;
- Minecraft `1.21.1`;
- NeoForge development baseline `21.1.235`;
- Apotheosis `8.6.0`;
- Apothic Enchanting `1.6.0`;
- Apothic Spawners `1.4.0`;
- Apothic Attributes `2.10.0`;
- Iron's Spells `1.21.1-3.16.2`;
- Iron's Lib `1.21.1-2.1.0`;
- Curios `9.5.1+1.21.1`.

The assembled pack is newer on several providers, including Apotheosis 8.8.0 and Iron's Spells 3.16.3, so runtime compatibility remains a separate gate.

## Classification

Canonical catalog classification:

`MAGIC BRIDGE / AFFIX + GEM SUPPORT SYSTEM / EXTERNAL-SPELL TRIGGER OVERLAY`

Iron's Apothic does not own a second spell registry. It extends Apotheosis/Apothic affixes and gems so they can inspect, modify or trigger spells owned by Iron's and installed spell addons.

## Registry and data surface

At the exact 2.2.2 source pin, `IronsApothic.commonSetup` registers **7 custom Apotheosis affix codecs**:

1. `attribute`;
2. `spell_effect`;
3. `magic_telepathic`;
4. `spell_level`;
5. `spell_trigger`;
6. `imbued_spell_trigger`;
7. `mana_cost`.

The exact source tree contains:

- **140** JSON affix definitions under `data/irons_apothic/affixes/**`;
- **48** spell-trigger / imbued-spell affix definitions under explicit `spell` or `imbued` resource paths;
- **24** gem definitions under `data/irons_apothic/gems/**`;
- **25** school-family resource groups, including Geo in 2.2.2.

See `SOURCE-2.2.2-MAGIC-SURFACE.md` for the bounded resource inventory.

## Spell ownership

The source imports and resolves Iron's `SpellRegistry`, `SchoolRegistry` and `AbstractSpell` for affix codecs and triggered casting.

`SpellTriggerAffix` decodes a spell holder from Iron's `SpellRegistry.REGISTRY`. `SpellCastUtil` executes the resolved external `AbstractSpell` through Iron's server-side casting state with `CastSource.COMMAND`.

No provider-owned `DeferredRegister`/spell registrar or independent `AbstractSpell` registration surface is present in the exact source tree.

Therefore:

- the 48 spell-oriented affix definitions are **not 48 new spells**;
- they reference or trigger spell identities owned by Iron's and other providers;
- Iron's Apothic contributes **+0 independent spell identities** to the strict semantic spell numerator.

## 2.2.2 delta

The certified sibling dossier and exact source pin establish the current line's addon compatibility changes:

- Geo school affixes are present for GTBC's Geomancy;
- `quaking_jasper` is present as an external gem definition;
- older Sand compatibility was removed for current Cataclysm Spellbooks compatibility;
- Harmonic/Guardian Angel integration was removed after the corresponding provider change.

The exact 2.2.2 source still contains some historical resource files such as `harmonic_geode` and `school_spirit/harmonic.json`; file presence alone is not treated as proof that removed integration is reachable in the current runtime. Runtime/data loading remains fail-closed where provider conditions matter.

## Authority boundary

- **Iron's Spells** owns spell identities, schools, mana, base casting and spell cooldown semantics.
- **Apotheosis/Apothic** owns affix/gem/reforging mechanics and affix settlement.
- **Iron's Apothic** owns the bridge codecs, filters, affix-triggered casts, magic-specific loot categories and gem/affix data.
- **Black Arcana** must not duplicate the same triggered casts, school bonuses, mana-cost modifiers, spell-level modifiers or magic-loot routing as new spells.
- **RPG Skill Tree** remains authority for progression, attributes, Mastery, perks and gates through verified contracts only.

## Exactly-once and recursion risk

The exact source contains an explicit recursion guard in `SpellTriggerAffix` for spell-triggered affix execution. This is useful provider evidence, but it is not a blanket assembled-pack guarantee.

Runtime QA still must verify:

- one affix trigger produces at most one intended external cast;
- the triggered cast does not generate an uncontrolled proc loop across other mods;
- mana-free affix casts remain mana-free only under the provider contract;
- affix cooldown state is not duplicated or shared across wrong entities;
- target rewriting does not select the wrong entity;
- spell/heal/damage callbacks do not settle twice;
- Curios/equipment modifiers clean up correctly.

## Runtime fail-closed boundary

Still unresolved for the assembled pack:

- physical JAR digest ↔ source/release byte equality;
- exact loaded datapack/resource set after pack overrides;
- provider optional-integration resolution;
- numerical affix/gem balance;
- recursive cross-mod proc behavior;
- FakePlayer/automation paths;
- dedicated-server and multiplayer lifecycle;
- persistence/relog/restart behavior;
- complete compatibility with Iron's 3.16.3 and Apotheosis 8.8.0.

## Result

**✅ Cataloged.**

Catalog closure is source-pinned for the 2.2.2 magic bridge surface:

- 7/7 custom affix codecs identified;
- 140 affix JSON definitions bounded;
- 48 spell/imbued spell affix definitions inventoried;
- 24 gem definitions bounded;
- provider-owned spell registrations: **0**;
- strict spell-semantic delta: **+0**.

This is a catalog closure, not an assembled-pack runtime compatibility PASS.
