# Capability Matrix Delta — Ars Technica 2.7.6

Status: `SOURCE-PINNED PROVIDER DELTA / RUNTIME QA PENDING`

| Capability | Current Ars Technica coverage | Black Arcana consequence |
|---|---|---|
| Create-style magical processing | Carve, Pack, Polish, Obliterate, Press, Fuse, Whirl, Apply plus provider processing entities | generic “cast a spell to perform Create processing” is already occupied; future BA candidates need a real mechanical delta |
| Magical logistics / insertion | Insert moves item entities into nearby valid containers/handlers; Split changes distribution | generic spell-based item insertion/logistics is not a gap |
| Consumable/fluid remote use | Telefeast consumes or forwards eligible item/fluid-derived consumables | generic remote eat/drink/potion extraction is not a gap |
| Heat-tier processing | Press/Fuse consume Smelt/Superheat context for heated/superheated Create processing | generic magical heated/superheated recipe execution is not a gap |
| Fan processing | Whirl maps Water/Flare/Smelt/Hex to Washing/Smoking/Blasting/Haunting | generic spell-powered fan-processing variants are occupied |
| Source → kinetic conversion | Source Motor consumes Ars Source and generates Create rotation/stress capacity | no second BA Source/SU converter or parallel energy ledger |
| Source relay cadence | Precise Relay changes Ars relay scheduling; Runic/Arcane Wrench conversion preserves Ars Source-machine state | cooldown customization is provider-owned, not a BA Source-network role |
| Rune cadence | provider mixin gives Ars runes persistent custom charge ticks | generic configurable Ars rune delay is already occupied |
| Automated spell processing | Transmutation Turret consumes Source and executes an Ars turret spell with provider resolver/focus semantics | no second turret settlement/cast pipeline |
| Processing focus / Fortune | Transmutation Focus adds Fortune, speeds/capacity provider processing and doubles eligible sub-100% Crush outputs | no duplicate generic yield/Fortune proc around the same Ars/Create event |
| Technomancy armor | 3× four-piece sets, Manipulation mana discount, mana/regen, school-power modifiers and Ars perk slots | equipment/progression overlap must preserve Ars perk/mana authority |
| Pressure/backtank | `thread_pressure` + persistent `air` component are exposed as Create backtank air | no BA pressure/air mirror for this capability |
| Schematicannon acceleration | nearby complete set/tagged Curio accelerates Create cannon cooldown while preserving machine lifecycle | generic technomancer proximity speed buff overlaps; never replay cannon ticks/material use |
| Arcane wrench interoperability | old Runic Spanner aliases/migrates to Create wrench + provider component; wrench adapts Ars runes/relays/turrets/jars/pedestals | do not create a second canonical wrench merely for presentation |
| Provider fluid world output | Fuse can fill nearby handlers then place bounded result-fluid blocks under provider config | provider mutation stays provider-owned; BA destructive/world effects still require `WorldEffectPolicy` |
| Compound spell UI | client mixins expose active/possible Create processing modes and valid subsequent glyphs | presentation is not gameplay authority and does not create a BA composition engine gap |

## Semantic disposition

Ars Technica materially narrows the remaining Black Arcana design space around **technomancy**. Darker aesthetics, different particles, or renaming Create-like processing cannot justify duplication.

A Black Arcana candidate in this area remains viable only if it demonstrates a gameplay identity that the installed Ars Technica/Create/Ars ecosystem does not already provide — for example a Black Arcana-specific hazard/Corruption/Strain/world-safety mechanic whose causal behavior is genuinely distinct rather than a wrapper around the provider recipe.

## Authority/dedup rules

- Ars mana/Source settles through Ars/provider paths once.
- Create recipes, kinetic stress and machine material use settle through Create/provider paths once.
- Provider child processing entities and child resolvers remain descendants of one causal provider cast.
- Pressure/backtank is one provider reserve, not a second Black Arcana resource.
- Black Arcana may observe safe provider outcomes for its own canonical systems only through a real boundary; observation must not replay output, cost, damage or item/fluid transfer.