# Goety 3.1.4 — provider catalog

## Status

`EXACT RELEASE-PINNED 3.1.4 / OFFICIAL PUBLIC-WIKI INVENTORY: 110 BASE FOCUSES + 12 WANDS/STAFFS + 13 RITUAL TYPES + 10 RESEARCH LINES / EXACT 3.1.4 SOURCE PIN OR JAR-LEVEL RECONCILIATION UNAVAILABLE / RUNTIME QA PENDING`

## Installed authority

- provider: **Goety**
- mod id: `goety`
- installed JAR: `goety-3.1.4.jar`
- runtime version: `3.1.4`
- loader/game: NeoForge 1.21.1
- CurseForge file: `8689429`
- release date: `2026-08-20`
- channel: Release
- project author: Polarice3
- release uploader: Vivideru
- project/release license declared by CurseForge: MIT
- role: `SOUL ENERGY / FOCUS SPELLCASTING / NECROMANCY / SERVANT / RITUAL PROVIDER`
- addons installed separately: Goety Iron `3.1`; Goety Cataclysm `1.21.1-1.8.2`.

The current modlist is authoritative for the installed JAR/runtime identity. CurseForge independently confirms the exact 3.1.4 artifact and release metadata.

## Source/provenance limitation

The official CurseForge project links source to `Polarice3/Goety-2`. The currently public repository exposes only `1.20` and `1.19` branches; it does not expose an auditable `1.21.1`/`3.1.4` branch or tag. The 3.1.4 CurseForge artifact has no additional source archive.

Therefore this catalog deliberately does **not**:

- use the current `1.20` branch as 3.1.4 source authority;
- treat a third-party 1.21.1 fork as the official 3.1.4 source;
- decompile the installed JAR to reconstruct implementation internals;
- infer exact registry IDs, costs or hooks from older source.

Confidence classes:

- installed/release identity: **EXACT**;
- current official Wiki-visible mechanics/inventory: **PUBLIC DOCUMENTATION**;
- exact 3.1.4 implementation/source/API semantics: **UNVERIFIED / FAIL-CLOSED** unless separately evidenced;
- exact runtime behavior in this 612-mod pack: **UNVERIFIED**.

## Provider authority

Goety is a primary supernatural/magic provider with its own:

- Soul Energy economy;
- Focus + Wand/Staff casting model;
- ritual system;
- research progression;
- owned servants and summon lifecycle;
- artifices powered by Soul Energy;
- witchcraft/brewing surface;
- endgame Lichdom transformation.

It is not an Iron's/Ars spell addon. Black Arcana must not reinterpret Goety Focuses as Black Arcana-native spells or Goety Soul Energy as a generic shared soul resource.

## Public official inventory checkpoint

The current official Wiki inventory exposes:

| Surface | Public documentation inventory | Exact 3.1.4 JAR reconciliation |
|---|---:|---|
| Base Focuses | **110** | PENDING |
| Focus categories | **10** — Magic, Necromancy, Geomancy, Frost, Wild, Wind, Storm, Abyss, Nether, Void | PENDING |
| Wands/staffs | **12** | PENDING |
| Ritual types | **13** | PENDING |
| Research lines | **10** | PENDING |
| Main resource | Soul Energy | provider identity publicly confirmed; exact internals pending |
| Endgame transformation | Lichdom | publicly confirmed; exact 3.1.4 internals pending |

The earlier preparatory branch count of 109 Focuses was incorrect: it omitted **Order Focus** from the 25-entry Magic family. The current official Items inventory yields 110 total.

## Core resource — Soul Energy

Official documentation identifies Soul Energy as Goety's main power source. Spells and artifices consume it. The player needs provider storage/access such as a suitable Totem in the hotbar/Charm slot or an active Arca to store/use Soul Energy.

Documented acquisition includes mob kills, with provider-specific generation paths through artifices and, under provider gear/state, servant kills. Soul Energy also participates in provider sustain, including healing compatible servant families and healing a Lich where ordinary regeneration changes.

Black Arcana must not synthesize a second Goety Soul Energy balance from death events. Any future integration must consume/query the provider-owned state through a verified boundary.

## Focus casting model

A Wand/Staff contains a Focus; the Focus determines the spell. The official getting-started flow exposes direct Focus slot selection and a Focus radial menu. The Focus Bag holds eight Focuses and can occupy a Curios Belt slot.

Specialized staffs modify compatible Focus behavior. Those are variants inside the provider cast semantics; Black Arcana must not observe one activation and process it as a second cast.

See [`FOCUS-CATALOG.md`](FOCUS-CATALOG.md) for the complete current public 110-name inventory and confidence rules.

## Ritual model

Official documentation describes the Dark Altar as the centerpiece of most rituals, fed Soul Energy through the Cursed Cage/storage chain. Rituals can:

- craft provider items;
- summon creatures;
- transform creatures;
- require environmental/structural conditions;
- require pedestal ingredients;
- require sacrifices within the altar area;
- require living conversion targets.

The official Wiki lists 13 ritual types: Animation, Forge, Geoturgy, Magic, Necroturgy, Deep, Frost, Sky, Storm, Adept Nether, Expert Nether, End and Sabbath.

Ritual cost, sacrifice/conversion identity and completion settlement remain Goety-owned.

## Research/progression

Research Scrolls unlock provider rituals and servant/content gates. The public Research page lists ten named lines:

1. Ravaging
2. Warred
3. Buried
4. Front
5. Haunting
6. Mistral
7. Floral
8. Bygone
9. Terminus
10. Forbidden

Terminus depends on Warred in the public progression. Forbidden gates Nameless/Lich content when the corresponding provider config requirement is enabled.

Black Arcana must not grant an advanced Goety Focus/ritual merely because the player has a semantically similar school or mastery elsewhere.

## Servants

Goety is a major servant authority. Official documentation defines servants as owned/summoned mobs that do not attack owners and respond to owner combat relationships. Many Focus summons also apply **Summon Down**: later summoning while it is active increases spell Soul Energy cost and weakens subsequent summons; the public documentation states a stack ceiling of Summon Down V.

Different servant families have provider gear-dependent persistence/healing rules. These lifecycles must remain provider-native.

Consequences:

- a Goety servant is not automatically a generic Black Arcana familiar;
- owner, persistence, summon cap and lifespan must not be bypassed through Binding;
- Soul Energy healing must not be paid twice;
- servant kills must not generate a second guessed Soul Energy reward.

## Witchcraft overlap

The official public inventory exposes Goety witchcraft/preparation tools including Taglock Kit, Waystone, Cauldron Ladle, Brew, Splash Brew, Lingering Brew, Gas Brew and Refuse Bottle.

This is a direct deduplication constraint for future Black Arcana witchcraft/sympathetic-magic work. Before creating a true-name/hair/blood/personal-object targeting token, the Goety Taglock semantics must be audited. If Goety already provides the required identity evidence, Black Arcana should integrate rather than clone it under another name.

## Infernal/Nether overlap

The public base inventory already includes a substantial Nether family: Fireball, Lava Bomb, Bombardment, Meteor Shower, Magma Bomb, Fire Blast, Flame Strike, Wither Skull, Ghastly and Blazing.

Therefore a future Black Arcana Infernal domain cannot be justified as merely stronger Nether/fire magic. Its proposed provider-independent delta must survive comparison with Goety, Iron's Fire, Cataclysm/Ignis and Soulfire providers.

## Soul/death overlap

Goety already covers death-derived Soul Energy, soul-powered casting/artifices, necromancy, owned servants and soul-based sustain. This sharply constrains any generic Black Arcana `soul mana` concept.

Goety Soul Energy remains distinct from:

- Malum spirits;
- Eidolon Soul capability/Soul Shards;
- Gravebound Souls/Phylactery;
- Vampirism blood;
- Black Arcana resources.

No conversion exists merely because the concepts share a soul/death theme.

## Installed addon boundary

### Goety Iron 3.1

Separate bridge/provider between Goety and Iron's. It can alter spell/servant integration and must be cataloged separately rather than counted inside the base Focus list.

### Goety Cataclysm 1.21.1-1.8.2

Separate content addon integrating Cataclysm themes/entities/powers into Goety. The current official Wiki page lists its own Focus families; those are addon-owned and are not included in the base 110-Focus inventory.

## Documents

- [`FOCUS-CATALOG.md`](FOCUS-CATALOG.md) — current official public base Focus inventory and individual verified examples.
- [`RITUALS-PROGRESSION.md`](RITUALS-PROGRESSION.md) — ritual types, research, Soul Energy and Lichdom public contracts.
- [`TECHNICAL-AUDIT.md`](TECHNICAL-AUDIT.md) — exact release/source/provenance limits and QA queue.
- [`INTEGRATION-RULES.md`](INTEGRATION-RULES.md) — Black Arcana provider authority, settlement and deduplication contract.

## Phase 3 gate

Goety-related Black Arcana implementation remains `BLOCKED` until the relevant installed 3.1.4 behavior and addon surfaces are reconciled sufficiently to prove a real semantic gap.

Do not promote this provider to `SOURCE-PINNED 3.1.4` or claim `JAR 110/110` unless exact evidence closes those separate gates.