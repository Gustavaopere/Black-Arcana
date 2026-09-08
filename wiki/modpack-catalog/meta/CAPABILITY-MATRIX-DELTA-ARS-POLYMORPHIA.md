# Capability Matrix Delta — Ars Polymorphia 1.0.3

Status: `EXACT SOURCE-PINNED / NON-SPELL COMPAT PROVIDER`

| Capability | Exact evidence | Black Arcana consequence |
|---|---|---|
| Ars Storage/Crafting Lectern recipe-conflict selection | exact 1.0.3 source injects into `CraftingLecternTile.onCraftingMatrixChanged(UUID)` and feeds matching server recipes into Polymorph player recipe data/sync | capability is occupied by Ars + Polymorph adapter; BA must not create another resolver for the same terminal |
| Player-specific conflicting recipe choice | exact source indexes the Ars lectern crafting inventory by player UUID and reads Polymorph player recipe data | do not mirror selection into BA state or globalize it across players |
| Client recipe selector in Ars Crafting Terminal | exact client mixin creates Polymorph `RecipesWidget` after terminal init | client UI is presentation only; BA must not interpret widget state as authoritative craft settlement |
| Server-side selection settlement | provider serverbound payload requires Ars CraftingTerminalMenu/Lectern and re-resolves the current valid recipe through Polymorph before assigning Ars `currentRecipe` | no second recipe validation or execution path is needed in BA |
| Provider networking | exactly one provider-owned play-to-server payload, `ars_polymorphia:reset_crafting_result`, protocol `1` | BA should observe final craft outcomes rather than replay reset/selection packets |
| Spell/glyph/ritual/resource content | none registered in exact 1.0.3 source tree | no spell-school/domain gap is consumed; provider is cataloged only because it touches the magic ecosystem |

## Current-host compatibility status

Exact source declares required dependency `polymorph` `[1.0.7,)`, but the physical top-level pack exposes `polymorph_plus` 1.3.1+1.21.1. Exact source also targeted Ars Nouveau 5.4.2.938 while the physical pack uses 5.13.1.

These are concrete runtime-compatibility gates. Phase 2AA does not infer successful dependency substitution or mixin compatibility from naming/theme alone.

## Semantic disposition

Ars Polymorphia does not overlap Black Arcana casting, hazards, Corruption, Strain, Arcane Danger, rituals or spell-domain authority. Its overlap is purely operational around recipe selection in an Ars terminal.

Therefore:

- keep Ars as terminal/craft authority;
- keep Polymorph-compatible provider as conflict-selection authority;
- keep Ars Polymorphia as adapter only;
- Black Arcana remains a read-only observer if any progression feature later cares about resulting crafts.
