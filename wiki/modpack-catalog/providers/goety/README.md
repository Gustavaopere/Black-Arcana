# Goety 3.1.4 — provider catalog

## Status

`OPEN CURRENT REGISTRY / EXACT 3.1.4 JAR-SOURCE RECONCILIATION PENDING / RUNTIME QA PENDING`

## Installed authority

- provider: **Goety**
- mod id: `goety`
- installed JAR: `goety-3.1.4.jar`
- runtime version: `3.1.4`
- loader/game: NeoForge 1.21.1
- physical JAR SHA-1: `a0770e180e4e8b1b87d8fa9c8356e9dbf34d82a7`
- CurseForge file: `8689429`
- release date: `2026-08-20`
- channel: Release
- project author: Polarice3
- release uploader: Vivideru
- project/release license declared by CurseForge: MIT
- role: `SOUL ENERGY / FOCUS SPELLCASTING / NECROMANCY / SERVANT / RITUAL PROVIDER`
- addons installed separately: Goety Iron `3.1`; Goety Cataclysm `1.21.1-1.8.2`.

The current physical modlist is authoritative for installed JAR/runtime identity. CurseForge independently confirms the public 3.1.4 release identity. Neither surface proves source-to-binary equivalence.

## Source/provenance reconciliation

The previous catalog statement that no public Goety source exists for Minecraft 1.21.1 is stale.

The public repository [`Vivideru/Goety-3`](https://github.com/Vivideru/Goety-3) is the current 1.21.1+ source line. Two audited checkpoints establish the strongest source evidence available here:

- `4230e3bce2842779a6667ae6e5bfef8f53a27541` — `gradle.properties` declares Minecraft `1.21.1` and Goety `3.1.0`;
- `6c41a04f2d712097c4461f969a6bb8ee277149ef` — latest audited public checkpoint, `gradle.properties` declares Goety `3.1.1`.

No public tag/source checkpoint corresponding to distributed `3.1.2` or the installed `3.1.4` has been established. Therefore the public tree is **current-line factual registry evidence**, not an exact 3.1.4 source pin.

The audited registry file is:

`src/main/java/com/Polarice3/Goety/common/items/ModItems.java`

It has blob `db3c63b366803e2d46aa4a996b5bb0f358437a7f` at both audited 3.1.0 and 3.1.1 checkpoints. Read-only factual inspection closes **123 active Focus item registrations** in that public source interval:

| Source category | Registered Focus items |
|---|---:|
| Magic | 26 |
| Necromancy | 11 |
| Geomancy | 11 |
| Frost | 9 |
| Wild | 12 |
| Wind | 9 |
| Storm | 11 |
| Abyss | 9 |
| Nether | 11 |
| Void | 14 |
| **Total** | **123** |

Ordinary spell-bearing registrations directly instantiate Goety spell objects through `MagicFocus(new ...Spell())`, and the public 3.1.1 tree independently exposes provider-native acquisition recipes under `src/main/resources/data/goety/recipe/focus/` for a broad set of Focus identities. Compatibility recipe variants are acquisition alternatives, not extra semantic spells.

This materially strengthens the public-source evidence that these are real provider casting/acquisition objects rather than a name-only inventory. It still does **not** establish that the installed 3.1.4 JAR contains exactly 123 Focuses, that every registration is survival-reachable, or that all 123 are independently countable semantic magic objects under Black Arcana's denominator. Exact 3.1.4 JAR/source reconciliation and object-level deduplication remain open.

## License boundary

`Vivideru/Goety-3/LICENSE.txt` is mixed-license. The audited license text states that original code under `src/main/java/com/Polarice3/` is MIT, while additions under `src/main/java/com/Vivideru/` are All Rights Reserved unless specifically stated otherwise.

`ModItems.java` is inside the `com/Polarice3` scope. Black Arcana uses it read-only for factual identifiers, counts and blob/version provenance only. This does not make the whole upstream tree MIT and does not authorize copying implementation, assets, text, models or sounds.

Therefore this catalog deliberately does **not**:

- call the 3.1.0/3.1.1 source tree exact 3.1.4 authority;
- infer 3.1.4 registry/API internals beyond evidence that is independently current;
- copy or adapt upstream implementation;
- convert Focus item registrations directly into Black Arcana semantic-count additions;
- decompile the installed JAR as a shortcut around missing exact-source evidence.

Confidence classes:

- installed/release identity: **EXACT**;
- public 1.21.1 source-line registry at 3.1.0/3.1.1: **CURRENT-LINE FACTUAL EVIDENCE**;
- public 3.1.1 Focus construction/acquisition evidence: **CURRENT-LINE FACTUAL EVIDENCE**;
- legacy official Wiki inventory: **PUBLIC DOCUMENTATION SUBSET**;
- exact 3.1.4 implementation/source/API semantics: **UNVERIFIED / FAIL-CLOSED** unless separately evidenced;
- exact runtime behavior in the physical pack: **UNVERIFIED**.

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

## Inventory evidence checkpoint

The legacy official Wiki list contains **110 named base Focuses** across the same ten families. The public 1.21.1 source registry already contains **123 active Focus item registrations**, so the 110-name Wiki list is not a complete authoritative registry for the current 1.21.1 source line.

The 13 source-registered Focus identities omitted from that legacy 110-name list are:

- `illuminate_focus`
- `earth_punch_focus`
- `smack_stone_focus`
- `ministrous_focus`
- `carrion_focus`
- `razor_wind_focus`
- `surging_focus`
- `sprightly_focus`
- `thunderstorm_focus`
- `water_whip_focus`
- `hogging_focus`
- `stellar_focus`
- `void_flash_focus`

Other public documentation surfaces remain useful as documentary evidence, but are not silently promoted to exact 3.1.4 registries:

| Surface | Current evidence | Exact 3.1.4 reconciliation |
|---|---|---|
| Base Focuses | 123 active item registrations in public 3.1.0/3.1.1 registry; spell-bearing entries wrap concrete provider spell objects; broad provider-native recipe surface exists in 3.1.1; legacy Wiki names 110 | PENDING |
| Focus categories | 10 — Magic, Necromancy, Geomancy, Frost, Wild, Wind, Storm, Abyss, Nether, Void | PENDING |
| Wands/staffs | 12 in public documentation | PENDING |
| Ritual types | 13 public categories | PENDING at ritual-identity level |
| Research lines | 10 public lines | PENDING |
| Main resource | Soul Energy | provider identity publicly confirmed; exact internals pending |
| Endgame transformation | Lichdom | publicly confirmed; exact 3.1.4 internals pending |

See [`FOCUS-CATALOG.md`](FOCUS-CATALOG.md) for the registry/Wiki reconciliation and confidence rules.

## Core resource — Soul Energy

Official documentation identifies Soul Energy as Goety's main power source. Spells and artifices consume it. The player needs provider storage/access such as a suitable Totem in the hotbar/Charm slot or an active Arca to store/use Soul Energy.

Documented acquisition includes mob kills, with provider-specific generation paths through artifices and, under provider gear/state, servant kills. Soul Energy also participates in provider sustain, including healing compatible servant families and healing a Lich where ordinary regeneration changes.

Black Arcana must not synthesize a second Goety Soul Energy balance from death events. Any future integration must consume/query provider-owned state through a verified boundary.

## Focus casting model

A Wand/Staff contains a Focus; the Focus determines the spell. Public documentation exposes Focus slot selection and a Focus radial menu. The Focus Bag holds eight Focuses and can occupy a Curios Belt slot.

Specialized staffs modify compatible Focus behavior. Those are variants inside provider cast semantics; Black Arcana must not observe one activation and process it as a second cast.

The public 3.1.1 source adds stronger identity evidence: ordinary Focus registrations directly wrap concrete Goety spell objects, and many Focus identities have provider-native acquisition recipes. This narrows the reachability blocker but does not remove the exact-version gate. Installed 3.1.4 registry/acquisition equivalence remains unproven.

## Ritual model

Public documentation describes the Dark Altar as the centerpiece of most rituals, fed Soul Energy through the Cursed Cage/storage chain. Publicly documented ritual behavior includes crafting provider items, summoning or transforming creatures, environmental/structural conditions, pedestal ingredients, sacrifices within the altar area and living conversion targets.

The Wiki lists 13 ritual **types**: Animation, Forge, Geoturgy, Magic, Necroturgy, Deep, Frost, Sky, Storm, Adept Nether, Expert Nether, End and Sabbath. Those are categories, not evidence of exactly 13 discrete ritual identities.

Ritual cost, sacrifice/conversion identity and completion settlement remain Goety-owned, and exact ritual recipes/registries for 3.1.4 remain pending.

## Research/progression

Research Scrolls unlock provider rituals and servant/content gates. The public Research page lists ten named lines: Ravaging, Warred, Buried, Front, Haunting, Mistral, Floral, Bygone, Terminus and Forbidden.

Terminus depends on Warred in the public progression. Forbidden gates Nameless/Lich content when the corresponding provider config requirement is enabled.

Black Arcana must not grant an advanced Goety Focus/ritual merely because the player has a semantically similar school or mastery elsewhere.

## Servants

Goety is a major servant authority. Public documentation describes servants as owned/summoned mobs that do not attack their owners and respond to owner combat relationships. Many Focus summons also apply **Summon Down**: later summoning while it is active increases spell Soul Energy cost and weakens subsequent summons; the public documentation states a stack ceiling of Summon Down V.

Different servant families have provider gear-dependent persistence/healing rules. Servant ownership, persistence, summon caps, lifespan, healing and Summon Down semantics remain provider-native.

Consequences:

- a Goety servant is not automatically a generic Black Arcana familiar;
- owner, persistence, summon cap and lifespan must not be bypassed through Binding;
- Soul Energy healing must not be paid twice;
- servant kills must not generate a second guessed Soul Energy reward.

## Witchcraft overlap

The public inventory exposes Goety witchcraft/preparation tools including Taglock Kit, Waystone, Cauldron Ladle, Brew, Splash Brew, Lingering Brew, Gas Brew and Refuse Bottle.

This is a direct deduplication constraint for future Black Arcana witchcraft/sympathetic-magic work. Before creating a true-name/hair/blood/personal-object targeting token, the Goety Taglock semantics must be audited. If Goety already provides the required identity evidence, Black Arcana should integrate rather than clone it under another name.

## Infernal/Nether overlap

The legacy public base inventory already includes a substantial Nether family: Fireball, Lava Bomb, Bombardment, Meteor Shower, Magma Bomb, Fire Blast, Flame Strike, Wither Skull, Ghastly and Blazing, while the public source registry adds further current-line registry evidence beyond that 110-name documentary subset.

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

## Domain-overlap rule

Goety's public surfaces span witchcraft/preparation, necromancy, summoning, elemental families, utility/control and Void/Nether magic. These are direct deduplication constraints for future Black Arcana design, but semantic similarity does not transfer provider authority and does not by itself erase a Black Arcana concept.

A future Black Arcana feature must prove a provider-independent delta and a safe integration boundary instead of cloning Goety mechanics under another name.

## Installed addon boundary

Goety Iron `3.1` and Goety Cataclysm `1.21.1-1.8.2` are separate installed providers. Their Focuses/effects are not folded into the base Goety registry count and remain cataloged under their own provider folders.

## Documents

- [`FOCUS-CATALOG.md`](FOCUS-CATALOG.md) — public 1.21.1 source-registry reconciliation against the legacy Wiki list.
- [`RITUALS-PROGRESSION.md`](RITUALS-PROGRESSION.md) — ritual types, research, Soul Energy and Lichdom public contracts.
- [`TECHNICAL-AUDIT.md`](TECHNICAL-AUDIT.md) — exact release/source/provenance limits and QA queue.
- [`INTEGRATION-RULES.md`](INTEGRATION-RULES.md) — Black Arcana provider authority, settlement and deduplication contract.

## Semantic denominator and Phase 3 gate

The strict reconstructible semantic total remains **797**. Goety contributes **+0 at this reconciliation checkpoint** because the exact installed 3.1.4 registry/acquisition surface is not reconciled and object-level semantic deduplication remains open. Public 3.1.1 source now proves stronger spell-bearing Focus construction and broad provider-native acquisition evidence, but it is not exact 3.1.4 authority.

Goety-related Black Arcana implementation remains `BLOCKED` until the relevant installed 3.1.4 behavior and addon surfaces are reconciled sufficiently to prove a real semantic gap and any required provider boundary.

Do not promote this provider to `SOURCE-PINNED 3.1.4`, `JAR 123/123`, or a counted semantic state without new exact/current evidence.
