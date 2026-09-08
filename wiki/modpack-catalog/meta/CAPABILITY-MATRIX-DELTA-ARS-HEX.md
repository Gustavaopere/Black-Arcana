# Capability Matrix Delta — Ars Hex 5.0.4b

Status: `SOURCE-PINNED PROVIDER DELTA / RUNTIME QA PENDING`

| Capability | Current Ars Hex coverage | Black Arcana consequence |
|---|---|---|
| Malum-backed soul damage | Soul Shatter is an Ars Tier-II damage effect using Malum Voodoo damage and Necromancy while Ars Elemental is loaded | generic “Malum soul damage through an Ars glyph” is occupied; BA soul mechanics remain valid only with distinct BA-owned causal contracts |
| Ars→Iron elemental damage bridge | Ars damage is multiplied from mapped Iron school power/resistance in `SpellDamageEvent.Pre` | do not apply Iron school power/resistance a second time to the same Ars damage event |
| Ars Elemental armor→Iron attributes | `IElementalArmor` pieces receive mapped Iron school-power modifiers | do not mirror these provider attributes into a second BA/RPG equipment bonus path |
| General Iron spell-power merge | optional source toggle applies Iron general spell-power multiplier to Ars damage | treat as provider-owned compatibility; source target-vs-caster observation remains QA, not a BA correction hook |
| Ars thread→Malum Soul Ward | Soul Ward Thread adds Malum capacity/integrity attributes | no duplicate Soul Ward ledger or BA shadow-stat |
| Ars thread→Malum Spirit Spoils | Spirit Spoils Thread adds Malum spirit-spoil attribute | no second spirit-drop proc/reward settlement on the same kill |
| Ars thread→Lodestone magic proficiency | Magic Proficiency Thread adds Lodestone magic-proficiency attribute | generic cross-provider magic-damage stat projection is already occupied |
| Malum scythe as Ars caster | Enchanter's Scythe prepends Touch, runs an Ars resolver on hit and integrates Malum boomerang/Reactive paths | do not replay weapon-hit casts or count child resolver work as a second user cast |
| Necromancy mana discount | scythe discounts 20% of each Necromancy part's casting cost, rounded up after summing | Ars mana discount remains Ars/provider-owned; no parallel BA mana discount ledger |
| Iron particle wrapping | 5 Ars particle types wrap Iron particle providers | presentation compatibility creates no BA gameplay authority |
| Hexerei broom/brush bridge | source can register broom/brush/entity/particle integration, but Hexerei is absent from current pack | dormant source does not occupy current-runtime capability and must not be used as evidence of active behavior |
| Damage/item/block tag unification | datagen source intends cross-provider tags, but committed generated tree lacks those tag files | do not treat intended datagen as installed authority until physical JAR packaging is verified |

## Semantic disposition

Ars Hex primarily occupies **cross-provider unification**, not a standalone spell school. Its strongest deduplication consequence is that the modpack already has a provider-native path for Ars damage/equipment to consume Iron's/Malum/Lodestone semantics.

Black Arcana should not build a second universal “magic unifier” that reprocesses the same hits, attributes, spirit rewards or on-hit casts. A Black Arcana integration remains valid only when a real boundary exposes a BA-owned concern — e.g. Arcane Danger snapshotting, Corruption/Strain consequences or BA progression gates — without replaying provider settlement.

## Authority/dedup rules

- Ars mana/casting/glyph/perk state settles through Ars once.
- Malum spirit/Soul Ward/Voodoo/scythe semantics settle through Malum/provider paths once.
- Iron school/general spell attributes settle through Iron's/provider paths once.
- Lodestone Magic Proficiency remains Lodestone-owned.
- RPG Skill Tree may gate or provide its own progression contract; it must not become authority for Ars Hex damage/resource execution.
- Black Arcana may observe provider outcomes only through a real boundary and must preserve causal identity/deduplication.
