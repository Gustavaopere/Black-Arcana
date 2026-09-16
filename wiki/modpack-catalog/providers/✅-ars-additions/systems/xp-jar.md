# XP Jar

Status: `SOURCE-PINNED 21.3.0 / EXECUTION AUDITED / ACQUISITION SOURCE-PINNED / RUNTIME QA PENDING`

Exact source pin: `Jarva/Ars-Additions@91f102a90dc058cf40e4eac5a67a881e48b856b4`.

Registry id: `ars_additions:xp_jar`.

## Acquisition

Enchanting Apparatus recipe in the exact pin:

- reagent: Glass Bottle;
- pedestal items: Ars Nouveau Allow Item Scroll, Furnace, Cobblestone, an item in the coal tag, and Lapis Lazuli.

A shapeless self-clear recipe is also generated.

## Provider-native behavior

XP Jar extends Ars Nouveau `VoidJar`. Before the provider consumes/voids a matching stack amount, `preConsume` converts the voided count into vanilla player experience at a ratio of **1 XP point per 2 consumed items**.

Because odd amounts cannot be represented immediately, the jar stores one-bit-equivalent integer carry state in the persistent/network-synchronized `xp_jar_remainder` component:

- `total = amount + remainder`;
- awarded XP = integer `total / 2`;
- new remainder = `total % 2`.

This is vanilla experience-point award, not Ars mana, Source, RPG Skill Tree XP or Black Arcana progression.

## Black Arcana boundary

Do not convert XP Jar output into Mastery/skill XP automatically and do not run a second item-consumption settlement. Any RPG/Black Arcana progression bridge would require an explicit contract that distinguishes vanilla XP from provider/RPG progression resources.
