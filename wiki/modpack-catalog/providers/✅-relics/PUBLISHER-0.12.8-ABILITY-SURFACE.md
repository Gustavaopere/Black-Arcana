# Relics 0.12.8 — publisher/current-doc cross-check

Status: `DOCUMENTARY CROSS-CHECK / SUPERSEDED FOR CARDINALITY BY EXACT ARTIFACT AUDIT`

## Evidence boundary

Physical authority:

`neoforge-rpg-skilltree@5751321657cea41e77ec7c2be7f191e11c9b68a7`

Exact publisher file:

`https://www.curseforge.com/minecraft/mc-mods/relics-mod/files/8158315`

Current official documentation:

`https://www.shatterbyte.com/docs/mods/relics/`

This file preserves documentary naming/behavior context. Exact cardinality and exact current identity roots are controlled by [`EXACT-0.12.8-ABILITY-INVENTORY.md`](EXACT-0.12.8-ABILITY-INVENTORY.md).

## Version correlation

The exact 0.12.8 publisher changelog adds Shield of Retaliation.

Current official docs include Shield of Retaliation in the 20-relic base roster. The documentation is therefore useful for human-readable behavior/name cross-checking, but it is not used as the immutable count authority.

## Exact-artifact supersession

The clean-room exact artifact audit closes:

- 20 base relic item classes;
- 39 exact base ability roots;
- 2 exact owner-scoped synergy roots;
- physical/publisher SHA-1 equality.

Therefore the older documentary `PENDING` cardinality is superseded.

## Naming boundary

Publisher/docs may use human-readable names that differ from exact internal ids. Examples include documentation concepts such as Teleportation, Transgression, Electric Discharge or Lunar Phase, while the exact artifact roots use ids such as `blink`, `rewind`, `shock` and `phase`.

For deduplication and counting, exact owner-scoped artifact identities prevail. Documentation remains useful for high-level semantics only.

## Rank/mode boundary

The following do not mint additional identities by default:

- enabled/disabled modes;
- lunar mode selection;
- rank modifiers;
- quality/stat scaling;
- rank-unlocked numerical refinements.

Synergies are a separate first-class provider surface and are inventoried separately from base abilities.

## Result

Documentary surface: retained as cross-check.

Exact current semantic count: **41 `COUNTED_EXACT` provider powers**, controlled by the exact artifact inventory.
