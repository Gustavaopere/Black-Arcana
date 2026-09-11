# Semantic Magic Coverage Ledger

## Purpose

This file is the reconstructible ledger for the user-facing semantic-magic coverage metric. It is deliberately separate from the provider-component closure metric in [`CATALOG-COVERAGE-CURRENT.md`](./CATALOG-COVERAGE-CURRENT.md).

A semantic magic object is one discrete provider-owned magical action identity that belongs to one of these classes:

- standalone spell;
- Ars glyph/spell-part primitive;
- ritual/rite;
- equivalent discrete supernatural player action when the provider uses an action/focus model instead of a spell registry.

The ledger does **not** count provider/JAR totals, schools by themselves, items, gear, familiars, affixes, machines, effects/statuses, resource entries, ordinary recipes/processes, classification tags, proxy registry slots, aliases, physicalization of an already-owned spell, arbitrary Ars spell compositions, or downstream consequences of one causal cast/action.

A provider-native identity is counted once under its semantic owner. Bridge/compat behavior does not mint a second spell identity merely because it observes, modifies, transports or physicalizes an existing provider action.

## Physical and repository anchor

- Minecraft: **1.21.1**
- NeoForge: **21.1.248**
- physical modlist: **595 top-level entries**
- physical modlist SHA-1: `7aaece7acbfb07ba4d0c66029042f36c50d046f0`
- reconstruction base: `main@4f3dab1a4801393873f9d4b7857782fcf6298e56`
- base post-merge validation: Black Arcana CI **#2349**, attempt 2 GREEN on the exact base SHA
- Phase 2BE canonicalized at `main@cce7f51794e4e65b0d97511eb55f710afc6e02f0`: PR #189 exact HEAD `e787699d25b283b8040cd179f605143e8ee396de` passed Black Arcana CI **#2483**; the merge SHA passed Black Arcana CI **#2484 attempt 2** GREEN after attempt 1 ended on an external `code.redspace.io` read timeout before compilation/tests

The historical chat-only tally is not an authority and is not used as an input to any sum below.

## Evidence states

| State | Meaning | Included in strict counted minimum? |
|---|---|---:|
| `COUNTED_EXACT` | current physical/runtime identity and exact current inventory are directly closed | yes |
| `COUNTED_SOURCE_PINNED` | current semantic inventory is closed at a matching source/version checkpoint; byte-for-byte JAR reproducibility may remain open | yes |
| `COUNTED_RELEASE_BOUNDED` | current/release-bounded evidence closes the semantic count even though implementation internals remain partially unavailable | yes |
| `CONDITIONAL` | registry/action exists, but current config, survival reachability or active eligibility is not closed strongly enough | no |
| `LOWER_BOUND` | current evidence proves at least this many objects, but not the complete current inventory | no |
| `OPEN` | no safe current semantic count can yet be declared | no |
| `ZERO_BRIDGE_INFRA` | audited provider adds no independent object under this metric | zero |
| `EXCLUDED` | a registry/content entry exists but fails this metric by definition | zero |

`COUNTED_*` is a semantic-inventory confidence state. It is **not** a claim that runtime QA, compatibility QA or every numerical mechanic has passed.

## Strict reconstructible counted minimum

**874 semantic magic objects are currently reconstructible from canonical provider records after Phase 2BE.**

This is a counted minimum, not the final denominator and not a coverage percentage. Providers with `LOWER_BOUND`, `CONDITIONAL` or `OPEN` state remain outside this sum until their current inventory/eligibility is reconciled.

Arithmetic cross-check by provider family:

- Ars ecosystem: **199**;
- Iron's ecosystem and spell-content addons: **527**;
- Eidolon: Repraised: **42**;
- Vampirism/Bloodlines/Werewolves supernatural action layer: **55**;
- Hexalia ritual/infusion layer: **25**;
- Malum Spirit Rite layer: **26**;
- total: `199 + 527 + 42 + 55 + 25 + 26 = 874`.

### Counted ledger

| Provider | Installed/current line | Count | State | Semantic basis |
|---|---|---:|---|---|
| [Ars Nouveau](../providers/ars-nouveau/README.md) | 5.13.1 | 109 | `COUNTED_SOURCE_PINNED` | 5 Forms + 13 Augments + 67 Effects + 24 rituals; arbitrary composed chains excluded |
| [Ars Additions](../providers/ars-additions/README.md) | 21.3.0 | 5 | `COUNTED_SOURCE_PINNED` | 3 glyphs + 2 rituals |
| [Ars Controle](../providers/ars-controle/README.md) | 1.6.15 | 9 | `COUNTED_SOURCE_PINNED` | 1 effect + 8 filters/spell parts |
| [Ars Technica](../providers/ars-technica/README.md) | 2.7.6 | 11 | `COUNTED_SOURCE_PINNED` | 11/11 registered spell parts |
| [Ars Hex](../providers/ars-hex/README.md) | 5.0.4b | 1 | `COUNTED_SOURCE_PINNED` | one current Malum-backed registered glyph under the physical provider set |
| [Ars Zero](../providers/ars-zero/README.md) | 2.0.2 | 12 | `COUNTED_RELEASE_BOUNDED` | 12 current unique glyph capabilities; disabled copied AOE/Amplifier variants excluded |
| [Ars Elemental](../providers/ars-elemental/README.md) | 0.7.10.1 | 47 | `COUNTED_SOURCE_PINNED` | 39 production spell parts + 8 rituals |
| [Ars 'n' Spells](../providers/ars-n-spells/README.md) | 3.3.2 | 5 | `COUNTED_SOURCE_PINNED` | 5 ritual identities; eight `ars_cross_*` proxy slots contribute zero |
| [Iron's Spells 'n Spellbooks](../providers/irons-spells/README.md) | 3.16.3 | 110 | `COUNTED_EXACT` | 110/110 active spell registry entries; deprecated Cloud of Regeneration excluded |
| [Apprentice's Codex](../providers/apprentice-codex/README.md) | 0.9.7.1 | 83 | `COUNTED_SOURCE_PINNED` | exact 83-spell registry inventory |
| [Asterism Arcanum](../providers/asterism-arcanum/README.md) | 1.21.1-0.1.0 | 10 | `COUNTED_SOURCE_PINNED` | 10 survival spell identities; `astral_gateway` is tracked separately as conditional |
| [Backported Spellbooks](../providers/backported-spellbooks/README.md) | physical 0.1.2 / embedded 0.1.0 | 6 | `COUNTED_RELEASE_BOUNDED` | release-day official source ceiling registers six standalone Iron's spells |
| [Deeper & Darker Spellbooks](../providers/deeper-and-darker-spellbooks/README.md) | 1.3.3 Version B | 4 | `COUNTED_RELEASE_BOUNDED` | 4 current provider spell identities |
| [Discerning The Eldritch](../providers/discerning-the-eldritch/README.md) | 1.4.4 | 22 | `COUNTED_SOURCE_PINNED` | 22/22 registered spells, including its ritual-school spell registrations once |
| [Dreamless Spells](../providers/dreamless-spells/README.md) | 1.1.9 | 4 | `COUNTED_SOURCE_PINNED` | 4 current registered spells |
| [Fire's Ender Expansion](../providers/fires-ender-expansion/README.md) | 2.4.1 | 11 | `COUNTED_SOURCE_PINNED` | 11/11 active spells |
| [IronSable](../providers/ironsable/README.md) | 1.2.0 | 7 | `COUNTED_RELEASE_BOUNDED` | 7 provider-owned new spells; 10 physicalized existing Iron's spells add zero identities |
| [ISS: Magic From The East](../providers/iss-magic-from-the-east/README.md) | 1.1.5 | 22 | `COUNTED_SOURCE_PINNED` | 11 Symmetry + 11 Spirit spells |
| [Legendary Spellbooks](../providers/legendary-spellbooks/README.md) | 0.3.2 | 30 | `COUNTED_SOURCE_PINNED` | 30 current provider spell identities |
| [Monsters & Spellbooks](../providers/monsters-spellbooks/README.md) | 0.0.16.3 | 98 | `COUNTED_RELEASE_BOUNDED` | release-interval evidence closes a stable 98-spell semantic inventory |
| [Paladin Spells](../providers/paladin-spells/README.md) | 1.1.1 | 5 | `COUNTED_SOURCE_PINNED` | 5/5 Holy spells |
| [Wind's Spellbooks](../providers/winds-spellbooks/README.md) | 1.0.5 | 7 | `COUNTED_RELEASE_BOUNDED` | 7/7 publisher/runtime-observed Wind spells |
| [Ypsilon's Fundamentalism](../providers/ypsilons-fundamentalism/README.md) | 1.1.7.1 | 15 | `COUNTED_SOURCE_PINNED` | 15/15 active spell registrations; commented prototypes excluded |
| [Tunes n' Tomes](../providers/tunes-n-tomes/README.md) | 1.1.0-HOTFIX | 16 | `COUNTED_RELEASE_BOUNDED` | current publisher Melodic roster enumerates 16 spells; migrated Sound ownership is not duplicated under Alshanex/FamiliarsLib |
| [Alshanex's Familiars](../providers/alshanex-familiars/README.md) | 4.0.3 | 18 | `COUNTED_EXACT` | exact hash-matched JAR closes 7 provider-owned spell registrations + 11 packaged `alshanex_familiars:ritual_recipe` identities; migrated Sound/Tunes content and external familiar casts are excluded |
| [Cataclysm: Spellbooks](../providers/cataclysm-spellbooks/README.md) | 1.1.13 | 59 | `COUNTED_EXACT` | exact hash-matched JAR closes 59 unconditional `AbstractSpell` registrations; 10 additional root localization keys are unregistered in 1.1.13 and excluded |
| [Eidolon: Repraised](../providers/eidolon-repraised/README.md) | 0.5.0.2 | 42 | `COUNTED_SOURCE_PINNED` | 18 normal/player-facing chants + 24 official ritual recipes; `undead_lure` empty cast and `basic_incense` dummy excluded; chant conversions are not extra spells |
| [Vampirism](../providers/vampirism/README.md) | 1.10.13 | 19 | `COUNTED_SOURCE_PINNED` | 14 Vampire + 3 Hunter + 2 shared Lord registered player actions; counted as provider-native discrete supernatural actions, not Iron's spells |
| [Bloodlines](../providers/bloodlines/README.md) | 3.0.9 | 28 | `COUNTED_SOURCE_PINNED` | 29 action registrations minus Sorcerous Strike; exact source registers its action/skill/node/config but omits the node from the configured Gravebound tree and from all rank-default grants, so it is not normally survival-reachable in this build |
| [Werewolves](../providers/werewolves/README.md) | 2.0.3.3 | 8 | `COUNTED_SOURCE_PINNED` | 3 player form actions + Howling + Rage + Sense + Fear + Leap; exact source proves Leap's survival-tree node and dedicated server input path; Hide Name remains presentation-only |
| [Hexalia](../providers/hexalia/README.md) | physical filename 1.3.6 / runtime metadata 1.3.5 | 25 | `COUNTED_RELEASE_BOUNDED` | 19 player-facing Nature's Ritual identities + 6 Celestial Infusion identities; mutation, Mortar & Pestle, Small Cauldron/brews, Censer, idols and equipment remain excluded by metric scope |
| [Malum](../providers/malum/README.md) | 1.8.2 | 26 | `COUNTED_RELEASE_BOUNDED` | release-bounded registry evidence closes 26 base `SpiritRiteType` identities; exact release-bounded `TotemMagicEntries` separately places both special Arcane rites in `ArcanaProgressionScreen` with `SpiritRiteRecipePage`, proving they are player-facing rites rather than proxy slots; 37 Geas effect types and 9 spirit resource/type identities remain excluded |
| **Strict total** |  | **874** |  |  |

### Bloodlines 3.0.9 Sorcerous Strike reachability closure

Exact installed-line source at `TheDrOfDoctoring/bloodlines@c8fd517d204d09dfcb9a544c17d7df87755eaa5c` registers Sorcerous Strike as `gravebound_crit_action`, registers the corresponding `BloodlineActionSkill`, creates a `gravebound_sorcerous_strike` skill node, and exposes its balance config. Those facts establish that the implementation exists; they do not establish normal player acquisition.

The same exact source closes the missing reachability question: the generated configured Gravebound tree does not include `gravebound_sorcerous_strike`, and `HunterBloodlinesConfig.graveboundDefaults` grants only the four Gravebound rank nodes by default. Repository-wide inspection finds no provider-native alternate grant dedicated to Sorcerous Strike; generic Bloodline task/command surfaces add perk points rather than directly granting this skill. `SkillHandlerMixin` only adds Bloodlines-specific cost/rank/default checks around Vampirism skill enabling and does not create a second acquisition path.

Therefore Sorcerous Strike is classified `EXCLUDED` for the current semantic denominator as a registered/generated but not normally survival-reachable action in the exact 3.0.9 provider build. This statement does not claim that an operator command or externally modified datapack could never force-enable it; those are outside normal current-provider survival reachability. Bloodlines remains **28 counted actions**; after later provider closures, the global strict total is **874**.

### Werewolves 2.0.3.3 Leap correction

The previous ledger left `werewolves:leap` conditional because the action is hidden from the generic selector and its enabling path had not yet been reconstructed. Exact source at `TeamLapen/Werewolves@b72635b3e014e406b25bb79adb9d340f7443660b` closes that path: `ModSkills.LEAP` is an `ActionSkill` bound to `ModActions.LEAP`; node `SURVIVAL31` grants that skill; `SkillTreeProvider` connects `SURVIVAL31` into the normal `werewolf_level` tree; and the server handles the dedicated Leap input by delegating to the provider-owned action handler. Therefore hidden-selector presentation does not make Leap unreachable. The separate `no_leap_cooldown` refinement remains reachability-unproven and is not a separate semantic action. See [`SEMANTIC-MAGIC-DELTA-WEREWOLVES-LEAP.md`](./SEMANTIC-MAGIC-DELTA-WEREWOLVES-LEAP.md).

### Alshanex's Familiars 4.0.3 exact-artifact closure

Phase 2BD materialized CurseForge File ID `8675568` through Curse Maven in an isolated audit and required SHA-1 `e5051c2385a426d05bf203ba8081a23d891f6686` to match the physical modlist before inspection. The exact JAR closes seven unconditional provider-owned `AbstractSpell` registrations and eleven packaged JSON resources of custom type `alshanex_familiars:ritual_recipe`. These are discrete spell/ritual identities under this ledger, for **+18**.

The seven spells are `summon_shadows`, `ice_age`, `ice_chamber`, `megido`, `fire_fist`, `end_mayhem` and `switcheroo`. The eleven rituals are the five familiar-shard rituals (`archmage`, `druid`, `frostling`, `hunter`, `lightning_mage`), `summoner_shard`, four magic power/resistance tier rituals and `truth_mirror`. Exact numerical mechanics and runtime QA remain separate gates.

The 4.0 ownership migration remains controlling: Sound/Melodic content belongs to Tunes n' Tomes and is not counted again under Alshanex. Familiar AI/passives and casts of externally owned Iron's spells also add zero identities. Clean-room inspection retained only factual IDs/counts/signatures and structured resource facts; no upstream implementation/assets were copied or adapted. See [`../providers/alshanex-familiars/EXACT-4.0.3-ARTIFACT-AUDIT.md`](../providers/alshanex-familiars/EXACT-4.0.3-ARTIFACT-AUDIT.md).

### Cataclysm: Spellbooks 1.1.13 exact-artifact closure

Phase 2BE materialized CurseForge File ID `8792628` through Curse Maven in isolated non-merge PR #188 and required SHA-1 `4af8348cc77bbff2ab7057c1fac26a5ab0a5b6a2` to match the physical modlist before factual inspection. The exact `SpellRegistries` static initializer closes **59** `registerSpell(...)` calls, **59** provider spell-class instantiations, **59** spell-field assignments and **0** conditional branches. Field/class/root-ID reconciliation closes **59 unique current spell identities**, for **+59**.

The exact implementation-package distribution is 7 Abyssal, 4 Ender, 1 Evocation, 5 Holy, 11 Fire, 5 Ice, 4 Nature and 22 Technomancy. The exact English localization has 69 root spell keys, but ten are not registered current spell IDs/classes and are excluded as translation-only/WIP-or-residual evidence: `conjure_abyssal_gnawer`, `conjure_clawdian`, `conjure_coral_golem`, `conjure_coralssus`, `cryopiercer`, `final_rend`, `hemorrhaging_impact`, `parting_shot`, `quick_strike`, `scorched_earth`.

The generic/current publisher project page advertises 65 spells, but that project-scale claim is not substituted for the physically installed 1.1.13 registry; a newer 1.1.14 beta also exists after the installed file. Exact numerical mechanics, acquisition and runtime/API integration remain separate gates. See [`../providers/cataclysm-spellbooks/EXACT-1.1.13-ARTIFACT-AUDIT.md`](../providers/cataclysm-spellbooks/EXACT-1.1.13-ARTIFACT-AUDIT.md) and [`../providers/cataclysm-spellbooks/EXACT-1.1.13-SPELL-INVENTORY.md`](../providers/cataclysm-spellbooks/EXACT-1.1.13-SPELL-INVENTORY.md).

### Hexalia release-boundary reconciliation

Hexalia remains an explicit physical/source identity mismatch: the installed file is `hexalia-neoforge-1.3.6.jar`, while its runtime metadata reports `1.3.5`. That prevents an exact installed-JAR/source-equivalence claim, but it no longer blocks this narrow semantic count.

The official source commit `ef34896fc1a2a02da46b49a46ca78ca236bdc2dc` (`Update 1.3.5`) declares `mod_version=1.3.5`; its immediate release successor `4952c65233bf31e9f0d3e55ff76be7fa1007ee3d` (`Release Hexalia 1.3.6`) declares `mod_version=1.3.6`. Comparing those checkpoints shows no Nature's Ritual or Celestial Infusion recipe JSON added, removed or modified. The official 1.3.5 publisher changelog also records restoration of the Galeberries Celestial Infusion recipe, so the six-infusion inventory is already present on the 1.3.5 release line.

Therefore the intersection relevant to this metric is stable across the observed `1.3.5` metadata / `1.3.6` filename-source boundary: **19 player-facing Nature's Rituals + 6 Celestial Infusions = 25**. The debug Nature's Ritual is excluded. Exact installed-binary equivalence, runtime mechanics and provider API/hook QA remain open independently.

### Malum 1.8.2 release-boundary reconciliation

The physical instance identifies `malum-1.21.1-1.8.2.jar` / runtime `1.8.2`. The official `SammySemicolon/Malum-Mod` `1.21.1` history bounds the matching version line between `f56691e56e591a6d8d1859ff119e749375e14d61`, whose parent still declares `1.8.1`, and `03b743a37f3eeb0cc7f4364f0730e1f135f78408`, whose child advances to `1.8.3`.

Endpoint blob equality is not used alone. Path-history queries over the complete observed 1.8.2 window show:

- `MalumSpiritRiteTypes.java` — no commit touches the path after entry into the window and before the 1.8.3 transition;
- `MalumSpiritRiteEffectTypes.java` — no commit touches the path in that interval; supporting deduplication evidence only;
- `MalumSpiritTypes.java` — no commit touches the path in that interval;
- `MalumGeasEffectTypes.java` — the path is touched at the initial `f56691e...` checkpoint and has no later commit before the transition;
- `client/screen/codex/entries/TotemMagicEntries.java` — no commit touches the path in that interval.

The stable endpoint blobs are:

- `MalumSpiritRiteTypes.java` → `2b9e4e5445733dee4ed205e4331d55c93ac86028`, with **26 active base-Malum rite registrations**;
- `MalumSpiritRiteEffectTypes.java` → `e5fd8854c12783e4503475ccaf461c3a19c2a0b0`, used only to distinguish the two special rite/effect identities and adding **0** semantic objects;
- `MalumGeasEffectTypes.java` → `2aef164fcedae891b2c6805f2edbd8ee48cffbfe`, with **37 active Geas effect-type registrations**; two proposed Bonds and one Authority are commented out;
- `MalumSpiritTypes.java` → `fa772479f0f73131dabf33d9342299c7e20405e1`, with **9 spirit resource/type registrations**;
- `TotemMagicEntries.java` → `d0ba29e52abcd1f26cfa92f20951c4981ae3c661` at both endpoints.

The semantic eligibility of `undirected_rite` and `unchained_rite` is not inferred from registry membership. Exact `TotemMagicEntries.setupEntries(ArcanaProgressionScreen)` adds both as separate progression entries, each with its corresponding `RiteHolder` represented by a `SpiritRiteTextPage` and a `SpiritRiteRecipePage`; Unchained additionally exposes transmutation content. Because the progression file is unchanged throughout the observed `1.8.2` interval, this player-facing surface is release-bounded rather than a single-checkpoint observation.

`CodexLangDatagen.java` is touched at exactly five checkpoints during the same interval — `f56691e...`, `3fb3c77...`, `a634061...`, `5a578eb...` and `fbcc606...`. Every snapshot preserves dedicated entries for the two special rites, and the Undirected entry preserves activation guidance using five runes. This is supporting player-facing/reachability evidence; upstream prose is not copied into Black Arcana.

Therefore all **26 `SpiritRiteType` identities** satisfy the counted ritual/rite class for this ledger, including the two special Arcane rites. The Geas registry is an effect/progression registry, the Spirit Type registry is a resource/type registry, and Rite-effect entries are effects; all are explicitly outside the counted semantic-action classes. Gaze-provided rites are not included in the base Malum 26.

This is `COUNTED_RELEASE_BOUNDED`, not an exact installed-JAR/source-equivalence claim. Exact recipe contents, numerical mechanics, runtime lifecycle and provider API contracts remain open. The upstream licensing inconsistency documented in the Malum provider catalog continues to block promotion of source implementation internals into Black Arcana integration contracts.

## Conditional objects excluded from the strict total

| Provider | Quantity | State | Reason |
|---|---:|---|---|
| Asterism Arcanum | 1 | `CONDITIONAL` | `astral_gateway` is registered but documented creative-only/unfinished |
| Not Enough Glyphs | 39 | `CONDITIONAL` | current-pack source produces 40 `registerSpell` calls; `momentum` is source-disabled, leaving 39 source-enabled before user/provider config; exact active pack config remains to be reconciled |

The four real Ars Elemental primitives referenced by Not Enough Glyphs are not NEG-owned registrations and are already counted under Ars Elemental. Historical fallback namespaces do not create a second owner when the real provider is present.

## Explicit zero / non-duplicating providers

The following audited providers add **0** independent semantic objects under this metric:

- [Ars Creo](../providers/ars-creo/README.md) — Create/Ars bridge, no own glyph registry;
- [Ars Elemancy](../providers/ars-elemancy/README.md) — equipment specialization, empty glyph registration;
- [Ars Polymorphia](../providers/ars-polymorphia/README.md) — compatibility/progression only;
- [FamiliarsLib](../providers/familiarslib/README.md) — familiar framework; historical Sound content removed from the 1.7 line;
- [GTBC's SpellLib](../providers/gtbcs-spelllib/README.md) — shared spell/addon library infrastructure; publisher surface establishes no standalone gameplay/spell catalog in 2.2.0;
- [Soul Fire'd](../providers/soul-fire-d/README.md) — fire/enchantment content, 0 spells/glyphs/rituals;
- [Vampire Spells Addon](../providers/vampire-spells-addon/README.md) — resource/behavior overlay over Iron's + Vampirism, no own spell set;
- [Toxony](../providers/toxony/README.md) — harmful effects, oils, mutagens and alchemy state are provider content but are not spells/rituals/discrete action-registry identities under the current metric;
- Bloodlines `gravebound_crit_action` / Sorcerous Strike — registered implementation, but exact 3.0.9 configured tree and rank defaults provide no normal survival acquisition path;
- IronSable's ten physicalized base Iron's spells — already owned/countable under Iron's;
- Ars 'n' Spells `ars_cross_*` proxy registry pool — proxies, not eight semantic rituals/spells;
- Ars Zero copied disabled AOE/Amplifier compatibility variants — not unique active glyph capabilities;
- Werewolves `hide_name` — client presentation identity, not a gameplay magic object.

## Lower bounds and open denominator blockers

These rows are deliberately **not additive to 874** until their exact/current inventory and deduplication state meet the inclusion rule.

| Provider | Current evidence | State | Why excluded from strict sum |
|---|---|---|---|
| [Goety](../providers/goety/README.md) 3.1.4 | public 1.21.1 source line registers **123 active Focus items** in `ModItems.java`, stable at audited 3.1.0/3.1.1 checkpoints; the legacy Wiki 110-name list omits 13 of those registry identities | `OPEN CURRENT REGISTRY / EXACT 3.1.4 JAR-SOURCE RECONCILIATION PENDING` | exact installed 3.1.4 registry equivalence, player-facing semantic reachability/object-level deduplication and discrete ritual identities remain pending; item registration alone is not blindly counted as one semantic action |
| [Leyline Spellbooks](../providers/leyline-spellbooks/README.md) 1.0.3 | **9** publisher-named signature spells followed by “and more” | `LOWER_BOUND` | nine is explicitly not a complete registry count |
| [Somake Spells](../providers/somake-spells/README.md) 1.0.8-fix | publisher states **over 50 spells** | `LOWER_BOUND / OPEN CURRENT REGISTRY` | complete current registry, IDs and Aqua/T.O authority under the physical dual-installed stack remain unresolved |
| [Gaze](../providers/gaze/README.md) 1.1.7.1 | publisher states **2 Geas** plus a new set of Rites | `LOWER_BOUND / OPEN` | rite registry and complete IDs/names are not published; exact source/JAR extraction pending |
| [Ignis Soulfires: Spellbooks](../providers/ignis-soulfires-spellbooks/README.md) 1.1.0 | exact installed artifact and exact official CurseForge release are pinned (`project 1572171`, file `8620663`); publisher explicitly describes a Souled Ignitium Wizard Armor compatibility scope, while exact source/registry remains unavailable | `OPEN` | no safe 1.1.0 semantic registry inventory; publisher armor scope does not prove absence of spell/ritual registrations |
| [Goety Cataclysm](../providers/goety-cataclysm/README.md) 1.21.1-1.8.2 | exact installed release; public semantic surface proves addon spells/abilities exist | `OPEN` | complete Focus/spell/ritual inventory unavailable for current build |
| [Goety Iron](../providers/goety-iron/README.md) 3.1 | exact installed release; servant/focus/ritual bridge publicly established | `OPEN / BRIDGE-BOUNDED` | public servant list is not a spell inventory; focus/ritual registry totals are unverified |

Other provider directories that have not yet been normalized into a semantic-object row also remain outside the denominator. Absence from the strict table is never interpreted as zero without an explicit zero disposition.

## Important interpretation rules

1. **874 is not “874 / unknown”.** It is a reconstructible counted minimum while the denominator remains open.
2. Do not divide 874 by the 100 provider-component denominator. The Phase 2BE component target is `55/100`; provider-component coverage and semantic-magic coverage answer different questions.
3. Do not add public lower bounds to 874 and call the result complete. Lower-bound providers can contain unenumerated objects, aliases, removed entries or cross-provider proxies that require object-level reconciliation.
4. A registered technical slot can still be excluded when the provider itself proves it is dummy, presentation-only, disabled, proxy-only or unreachable in the current survival path.
5. Runtime/config QA remains distinct from semantic inventory closure. A source-pinned or release-bounded object may be countable while numerical settlement or compatibility remains fail-closed.
6. Semantic similarity does not transfer authority. Two different provider spells may overlap mechanically and still remain distinct provider-owned objects; deduplication prevents double ownership/processing, not factual erasure of existing content.
7. Black Arcana's own proposed/implemented spells do not backfill missing provider evidence and do not reduce the provider denominator by assumption.

## Next closure order

To converge on a final denominator efficiently, prioritize:

1. exact current inventory for `somakespells` 1.0.8-fix;
2. exact current inventory for `leylines` 1.0.3;
3. exact Gaze 1.1.7.1 rites/Geas inventory when materially new exact evidence becomes available;
4. Goety 3.1.4 exact JAR/source reconciliation, Focus semantic reachability/deduplication and discrete ritual-identity inventory;
5. current-pack config closure for the remaining conditional glyph/action rows.

Phase 3 remains blocked until the semantic denominator is reconstructible and provider/capability deduplication proves real Black Arcana gaps.