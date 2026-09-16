# Binding

Status: `SOURCE-PINNED 5.13.1 / FAMILIAR-BINDING RITUAL`

- Registry id: `ars_nouveau:ritual_binding`
- Class: `RitualBinding`
- Completion threshold: `3` progress steps, advanced once per 20 server ticks
- Search radius: `5` blocks
- Exact release checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Provider-native behavior

At completion, Binding scans every entity within radius 5. For each entity it iterates Ars Nouveau's registered `FamiliarRegistry` holders and applies the holder's provider predicate.

When a holder recognizes an entity:

1. the entity is removed with `RemovalReason.DISCARDED`;
2. Ars spawns its visual poof;
3. the holder's `getOutputItem()` is spawned at that entity's location;
4. a provider sound is played;
5. nearby players are rewarded through Ars' familiar advancement trigger.

The ritual then finishes.

The output item is the provider's bound-script/familiar-binding representation; Black Arcana does not own that identity.

## Black Arcana boundary

Binding is the canonical Ars conversion route from eligible familiar entity to provider binding item. Black Arcana must not independently delete the entity, duplicate the output, or interpret a bound script as a Black Arcana familiar contract.

Any bridge to Familiars & Divination must preserve the registered Ars holder identity and provider lifecycle.

## QA

Source behavior is pinned to 5.13.1. Cross-addon familiar holders registered into the same registry and full-pack entity matching remain runtime/registry QA.