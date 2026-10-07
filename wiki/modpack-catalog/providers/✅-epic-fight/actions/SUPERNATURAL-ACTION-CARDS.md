# Epic Fight 21.17.3.1 — supernatural action cards

Status: `3/3 COUNTED_EXACT`

Individual files:

- [Wrathful Lightning](wrathful-lightning.md)
- [Tsunami](tsunami.md)
- [Everlasting Allegiance](everlasting-allegiance.md)

These files materialize the existing three-root denominator and do not change the +3 strict accounting.

These cards represent the three Epic Fight core skill identities that meet the current semantic-magic rule. The vanilla trident/enchantment is the owner/reachability surface; Epic Fight remains authority for the action lifecycle, resource settlement, animation and damage.

## 1. Wrathful Lightning

- skill id: `epicfight:wrathful_lighting`;
- player-facing label: **Wrathful Lightning**;
- owner/reachability: `minecraft:trident` with vanilla **Channeling**;
- trigger: Epic Fight weapon-innate activation through the exact trident moveset;
- semantic settlement: provider animation/control path invokes the server-side `SUMMON_THUNDER` event;
- state: `COUNTED_EXACT`.

The exact registry ID intentionally uses `lighting`; the visible identity is Lightning.

## 2. Tsunami

- skill id: `epicfight:tsunami`;
- owner/reachability: `minecraft:trident` with vanilla **Riptide**;
- trigger: Epic Fight weapon-innate activation through the exact trident moveset;
- semantic settlement: provider Tsunami action uses dedicated animation/particle resources and selects its strengthened form when the server player is in water or rain;
- state: `COUNTED_EXACT`.

Water/rain state modifies the same causal Tsunami identity; it does not create a second spell/action.

## 3. Everlasting Allegiance

- skill id: `epicfight:everlasting_allegiance`;
- owner/reachability: `minecraft:trident` with vanilla **Loyalty**;
- trigger: Epic Fight weapon-innate activation with the provider-tracked thrown trident;
- semantic settlement: provider invokes the thrown-trident `recalledBySkill()` lifecycle and resolves the return path with entity-hit behavior;
- state: `COUNTED_EXACT`.

This is distinct from vanilla Loyalty's automatic passive return because the provider exposes an explicit player skill action and a separate damaging recall lifecycle.

## Exact fallback boundary

On the exact trident moveset, if none of Riptide, Channeling or Loyalty selects the three roots above, Epic Fight returns `epicfight:grasping_spire`. Grasping Spire remains classified as a martial/special weapon technique and is excluded from the semantic-magic numerator.

## Deduplication boundary

- lightning entities/events after Wrathful Lightning are consequences, not extra identities;
- Tsunami particles, sounds, dash distance and strengthened water/rain variant are parameters/consequences;
- repeated hits during Everlasting Allegiance's trident return are one action settlement;
- the vanilla enchantments are selectors/requirements, not new Epic Fight magic objects.

## Result

**3 exact-current provider-owned supernatural player actions.**
