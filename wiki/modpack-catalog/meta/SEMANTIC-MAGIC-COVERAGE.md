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
- reconstruction base: `main@1ef4d7f9c363bf8b37dd6ae8bf305f7750b6cedc`
- base post-merge validation: Black Arcana CI **#2340**, GREEN

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

**729 semantic magic objects are currently reconstructible from canonical provider records.**

This is a counted minimum, not the final denominator and not a coverage percentage. Providers with `LOWER_BOUND`, `CONDITIONAL` or `OPEN` state remain outside this sum until their current inventory/eligibility is reconciled.

Arithmetic cross-check by provider family:

- Ars ecosystem: **199**;
- Iron's ecosystem and spell-content addons: **434**;
- Eidolon: Repraised: **42**;
- Vampirism/Bloodlines/Werewolves supernatural action layer: **54**;
- total: `199 + 434 + 42 + 54 = 729`.

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
| [Asterism Arcanum](../providers/asterism-arcanum/README.md) | current installed line | 10 | `COUNTED_SOURCE_PINNED` | 10 survival spell identities; `astral_gateway` is tracked separately as conditional |
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
| [Eidolon: Repraised](../providers/eidolon-repraised/README.md) | 0.5.0.2 | 42 | `COUNTED_SOURCE_PINNED` | 18 normal/player-facing chants + 24 official ritual recipes; `undead_lure` empty cast and `basic_incense` dummy excluded; chant conversions are not extra spells |
| [Vampirism](../providers/vampirism/README.md) | 1.10.13 | 19 | `COUNTED_SOURCE_PINNED` | 14 Vampire + 3 Hunter + 2 shared Lord registered player actions; counted as provider-native discrete supernatural actions, not Iron's spells |
| [Bloodlines](../providers/bloodlines/README.md) | 3.0.9 | 28 | `COUNTED_SOURCE_PINNED` | 29 action registrations minus Sorcerous Strike, whose survival reachability is unproven and is therefore conditional |
| [Werewolves](../providers/werewolves/README.md) | 2.0.3.3 | 7 | `COUNTED_SOURCE_PINNED` | 3 player form actions + Howling + Rage + Sense + Fear; Leap is conditional and Hide Name is presentation-only |
| **Strict total** |  | **729** |  |  |

## Conditional objects excluded from the strict total

| Provider | Quantity | State | Reason |
|---|---:|---|---|
| Asterism Arcanum | 1 | `CONDITIONAL` | `astral_gateway` is registered but documented creative-only/unfinished |
| Bloodlines | 1 | `CONDITIONAL` | `gravebound_crit_action` / Sorcerous Strike is registered, but survival-tree reachability is unproven |
| Werewolves | 1 | `CONDITIONAL` | `leap` is registered but hidden from the normal selector and current reachability through its enabling path remains unproven |
| Not Enough Glyphs | 39 | `CONDITIONAL` | current-pack source produces 40 `registerSpell` calls; `momentum` is source-disabled, leaving 39 source-enabled before user/provider config; exact active pack config remains to be reconciled |

The four real Ars Elemental primitives referenced by Not Enough Glyphs are not NEG-owned registrations and are already counted under Ars Elemental. Historical fallback namespaces do not create a second owner when the real provider is present.

## Explicit zero / non-duplicating providers

The following audited providers add **0** independent semantic objects under this metric:

- [Ars Creo](../providers/ars-creo/README.md) — Create/Ars bridge, no own glyph registry;
- [Ars Elemancy](../providers/ars-elemancy/README.md) — equipment specialization, empty glyph registration;
- [Ars Polymorphia](../providers/ars-polymorphia/README.md) — compatibility/progression only;
- [FamiliarsLib](../providers/familiarslib/README.md) — familiar framework; historical Sound content removed from the 1.7 line;
- [Soul Fire'd](../providers/soul-fire-d/README.md) — fire/enchantment content, 0 spells/glyphs/rituals;
- [Vampire Spells Addon](../providers/vampire-spells-addon/README.md) — resource/behavior overlay over Iron's + Vampirism, no own spell set;
- [Toxony](../providers/toxony/README.md) — harmful effects, oils, mutagens and alchemy state are provider content but are not spells/rituals/discrete action-registry identities under the current metric;
- IronSable's ten physicalized base Iron's spells — already owned/countable under Iron's;
- Ars 'n' Spells `ars_cross_*` proxy registry pool — proxies, not eight semantic rituals/spells;
- Ars Zero copied disabled AOE/Amplifier compatibility variants — not unique active glyph capabilities;
- Werewolves `hide_name` — client presentation identity, not a gameplay magic object.

## Lower bounds and open denominator blockers

These rows are deliberately **not additive to 729** until their exact/current inventory and deduplication state meet the inclusion rule.

| Provider | Current evidence | State | Why excluded from strict sum |
|---|---|---|---|
| [Cataclysm: Spellbooks](../providers/cataclysm-spellbooks/README.md) 1.1.13 | current publisher says **65 new spells**; public source baseline 1.1.11 contains 34 registrations | `LOWER_BOUND / OPEN CURRENT REGISTRY` | exact 1.1.13 names/IDs are not available; cannot perform one-object ownership/dedup verification |
| [Goety](../providers/goety/README.md) 3.1.4 | current official documentation inventories **110 base Focuses** and provider model states that the Focus determines the spell | `LOWER_BOUND / OPEN JAR RECONCILIATION` | exact 3.1.4 Focus/JAR reconciliation remains pending; 13 ritual *types* are categories and are not blindly counted as 13 rites |
| [Leyline Spellbooks](../providers/leyline-spellbooks/README.md) 1.0.3 | **9** publisher-named signature spells followed by “and more” | `LOWER_BOUND` | nine is explicitly not a complete registry count |
| [Somake Spells](../providers/somake-spells/README.md) 1.0.8-fix | publisher states **over 50 spells** | `LOWER_BOUND / OPEN CURRENT REGISTRY` | complete current registry, IDs and Aqua/T.O authority under the physical dual-installed stack remain unresolved |
| [Gaze](../providers/gaze/README.md) 1.1.7.1 | publisher states **2 Geas** plus a new set of Rites | `LOWER_BOUND / OPEN` | rite registry and complete IDs/names are not published; exact source/JAR extraction pending |
| [Ignis Soulfires: Spellbooks](../providers/ignis-soulfires-spellbooks/README.md) 1.1.0 | exact installed artifact exists; public/source material found only for divergent 1.0.0 | `OPEN` | no safe 1.1.0 granular inventory |
| [Malum](../providers/malum/README.md) 1.8.2 | Spirit Rites and Geas/Pact/Oath/Authority systems are proven in the installed line | `OPEN` | exact 1.8.2 rite and Geas inventories remain unreconciled; later-branch counts are not imported |
| [Hexalia](../providers/hexalia/README.md) physical 1.3.6 / runtime metadata 1.3.5 | source-pinned 1.3.6 has 19 player-facing Nature's Ritual entries and 6 Celestial Infusions, plus brews/processing/mutations/Censer systems | `OPEN SCOPE / VERSION RECONCILIATION` | filename/runtime mismatch remains; ordinary recipes/processes must not be inflated into semantic magic objects before scope normalization |
| Alshanex's Familiars 4.0.3 | exact physical 4.0.3 present; 4.0 removed Sound and moved it to Tunes 'n Tomes; current line contains at least Switcheroo and Fire Fist evidence | `OPEN` | complete 4.0.3 spell/ritual inventory is not yet closed; historical Sound prose is stale for current ownership |
| Tunes 'n Tomes 1.1.0-HOTFIX | physically installed and owns Sound content moved out of the Familiars/FamiliarsLib lineage | `OPEN` | exact current inventory has not yet been reconstructed into a canonical provider record on this ledger pass |
| [Goety Cataclysm](../providers/goety-cataclysm/README.md) 1.21.1-1.8.2 | exact installed release; public semantic surface proves addon spells/abilities exist | `OPEN` | complete Focus/spell/ritual inventory unavailable for current build |
| [Goety Iron](../providers/goety-iron/README.md) 3.1 | exact installed release; servant/focus/ritual bridge publicly established | `OPEN / BRIDGE-BOUNDED` | public servant list is not a spell inventory; focus/ritual registry totals are unverified |

Other provider directories that have not yet been normalized into a semantic-object row also remain outside the denominator. Absence from the strict table is never interpreted as zero without an explicit zero disposition.

## Important interpretation rules

1. **729 is not “729 / unknown”.** It is a reconstructible counted minimum while the denominator remains open.
2. Do not divide 729 by the 100 provider-component denominator. `52/100` and semantic-magic coverage answer different questions.
3. Do not add public lower bounds to 729 and call the result complete. Lower-bound providers can contain unenumerated objects, aliases, removed entries or cross-provider proxies that require object-level reconciliation.
4. A registered technical slot can still be excluded when the provider itself proves it is dummy, presentation-only, disabled, proxy-only or unreachable in the current survival path.
5. Runtime/config QA remains distinct from semantic inventory closure. A source-pinned object may be countable while numerical settlement or compatibility remains fail-closed.
6. Semantic similarity does not transfer authority. Two different provider spells may overlap mechanically and still remain distinct provider-owned objects; deduplication prevents double ownership/processing, not factual erasure of existing content.
7. Black Arcana's own proposed/implemented spells do not backfill missing provider evidence and do not reduce the provider denominator by assumption.

## Next closure order

To converge on a final denominator efficiently, prioritize:

1. exact current inventory for `cataclysm_spellbooks` 1.1.13;
2. exact current inventory for `somakespells` 1.0.8-fix;
3. exact current inventory for `leylines` 1.0.3;
4. exact Gaze 1.1.7.1 rites/Geas inventory;
5. Alshanex's Familiars 4.0.3 + Tunes 'n Tomes ownership reconciliation;
6. Goety 3.1.4 Focus/JAR and ritual-identity reconciliation;
7. Malum 1.8.2 rites/Geas inventory;
8. Hexalia semantic-scope/version normalization;
9. current-pack config/reachability closure for conditional action/glyph rows.

Phase 3 remains blocked until the semantic denominator is reconstructible and provider/capability deduplication proves real Black Arcana gaps.