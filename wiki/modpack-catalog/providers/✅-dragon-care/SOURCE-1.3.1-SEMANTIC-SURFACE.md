# Dragon Care 1.3.1 — semantic surface audit

Status: `VERSION-DECLARED OFFICIAL SOURCE / CURRENT PHYSICAL IDENTITY KNOWN / ZERO_SEMANTIC_HUSBANDRY_SUPPORT`

## Authority inputs

Physical sibling authority:

- `Ice and Fire - Dragon Care-1.3.1 - 1.21.1v.jar`;
- mod id `dragoncare`;
- runtime `1.3.1 - 1.21.1v`;
- SHA-1 `6366af9408839a7fc1a50d3751902f772ec62fce`.

Official source/feature authority:

- repository: `OrionTheDragon/DragonCare`;
- NeoForge module: `Addon`;
- module version declaration: `1.3.1 - 1.21.1v`;
- Minecraft line: `1.21.1`.

No claim is made that a source build or public distribution is byte-identical to the installed JAR.

## Registration surface

The official 1.21.1 module's root registration path is bounded to the provider's normal content/support registries:

- blocks;
- items and creative tabs;
- effects;
- sounds;
- global loot modifier serializers;
- data components;
- recipe conditions;
- common configuration.

The provider package is organized around client/command/compat/config/dragon-phone/effect/event/item/loot/mechanics/mixin/network/recipe/sound/taming/worldgen concerns. No provider-owned spell, glyph, ritual, rite or semantic-action registry family is established by this surface.

## Behavior-level reconciliation

Official feature documentation closes the principal player-facing systems:

| Surface | Catalog disposition | Reason |
|---|---|---|
| Bond / affection rewards | `EXCLUDED_PASSIVE` | progression grants passive buffs/effects rather than a selected supernatural action |
| Blood syringe | `EXCLUDED_HUSBANDRY_ITEM_INTERACTION` | non-lethal resource extraction |
| Scale shears | `EXCLUDED_HUSBANDRY_ITEM_INTERACTION` | non-lethal resource extraction |
| Dragon painkiller / feeding / treatment | `EXCLUDED_HUSBANDRY_TREATMENT` | care/state interaction |
| Dragon Brush QTE | `EXCLUDED_HUSBANDRY_QTE` | cleaning minigame/state settlement |
| Dragon Phone | `EXCLUDED_TRACKING_UI` | owner-linked tracking/HUD utility |
| Ash Poisoning | `EXCLUDED_STATUS_EFFECT` | environmental hazard/effect state |
| Ash Sensor | `EXCLUDED_DETECTOR_DEVICE` | manual/automatic environmental scanning |
| Mysterious Tablets | `EXCLUDED_CONSUMABLE_TREATMENT` | detox consumable |
| Dragon Fruit | `EXCLUDED_FARMING` | crop/food content |
| structures/worldgen/loot | `EXCLUDED_SUPPORT_CONTENT` | acquisition/world content, not player magic actions |

## Passive-buff boundary

The official feature description explicitly characterizes high-affection rewards as passive buffs, including Resistance, Regeneration, Strength and max-health bonuses. Passive stat/effect rewards are not converted into discrete spells by the Black Arcana semantic metric.

## Host-creature boundary

Dragon Care's relationship to Ice And Fire CE does not transfer ownership of host dragon breath, combat, taming or other Ice And Fire actions. Those remain host-provider behavior and are deduplicated against the already cataloged Ice And Fire CE surface.

## Result

`ZERO_SEMANTIC_HUSBANDRY_SUPPORT / +0 STRICT`.

The current provider denominator is semantically closed at zero independent magic identities. Runtime/binary-equality questions remain separate and fail-closed.
