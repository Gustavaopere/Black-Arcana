# Curios and modifier hooks — Apothic Attributes 2.10.1

## Curios activation

Curios is optional in source metadata. The main provider only initializes `CuriosCompat` when mod id `curios` is loaded. The current physical pack includes Curios `9.5.1+1.21.1`, so this optional path is eligible to activate.

## What the Curios bridge owns

`CuriosCompat`:

- registers a modifier-source extractor used to identify item modifier sources in the Attributes GUI;
- listens to `CurioAttributeModifierEvent` at high priority;
- bridges eligible Curios modifiers into the provider's `StackAttributeModifiersEvent` abstraction;
- resolves a Curios type only when a matching provider `CurioEquipmentSlot` has been registered;
- expects a matching `EntitySlotGroup` for full base-modifier round-trip behavior.

Apothic does not turn every Curios slot into a provider equipment slot automatically. The source explicitly requires registration of compatible slot/group objects by an interested mod.

## `CurioEquipmentSlot`

This provider record implements `EntityEquipmentSlot` by querying Curios inventory for one named Curios type and exposing its stacks through the provider slot abstraction.

This is an attribute/equipment composition hook, not a casting, progression or resource hook.

## `StackAttributeModifiersEvent`

The event fires when item-stack attribute modifiers are queried and may run on logical server or client. It can:

- inspect defaults;
- add modifiers;
- remove modifiers;
- replace modifiers;
- remove conditionally;
- clear modifiers;
- build the resulting `StackAttributeModifiers` value.

The event is used by the provider's vanilla item-modifier bridge and optional Curios bridge.

## Black Arcana boundary

Black Arcana already owns a bounded Curios snapshot path for its own resistance/hazard facts. Do not replace that path with Apothic GUI/modifier-source scanning and do not add a second per-tick Curios scan.

If a future BA integration deliberately consumes Apothic attributes, it must use a verified API/boundary and preserve attribute ownership. No Curios slot, Apothic slot group or `StackAttributeModifiersEvent` should be treated as BA cast authority.
