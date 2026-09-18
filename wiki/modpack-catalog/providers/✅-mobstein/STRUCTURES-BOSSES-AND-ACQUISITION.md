# Mobstein 5.4.4 — structures, bosses, syringes and acquisition

## Evidence status

`PUBLISHER PUBLIC GUIDE / EXACT 5.4.4 RELEASE / INTERNAL LOOT+REGISTRY IDS UNVERIFIED / RUNTIME QA PENDING`

## Guidebook and acquisition identity

The publisher presents the **Mobstein Guidebook** as the starting reference for the provider's systems. Progression then branches through physical remains, anatomical components, specialist machines, syringes and world structures.

This is a provider-owned acquisition graph. A compatibility layer must not short-circuit it merely because Black Arcana has its own rituals or resurrection-adjacent capabilities.

## Syringe family

### Empty Syringe

Base container/input for the provider's syringe workflows. Exact recipe remains outside this public-only checkpoint unless explicitly documented by the publisher.

### Reviver Syringe

Publisher-documented roles:

- revives compatible mobs;
- explicitly cannot revive Resurrected Warden or Frankenstein Resucited/Golem;
- clicking the skeleton in Witherstein Ruins is the documented activation step for Witherstein.

This item is therefore both a resurrection tool and a boss-awakening gate. Black Arcana must not reinterpret it as a generic soul-restoration item.

### Mobstenio Blood Syringe

Publisher-documented role:

- revives Dr. Mobstenio at Frankenstein Castle.

Its identity is specific to Mobstenio progression and does not imply a generic blood-resource API.

### Lightningbolt Syringe

Publisher-documented role:

- enables compatible stretcher resurrection during daytime, bypassing the ordinary night timing requirement through a provider-native item route.

### Suspicious Syringe

Publisher-documented role:

- thrown at Igor while using the Igor Table/Station workflow;
- multiple throws may be required;
- current public guide states a maximum of four;
- produces random failed-experiment outcomes under provider rules.

Exact probabilities and RNG behavior remain unverified.

## Frankenstein Castle

Publisher-documented world structure:

- associated with swamp generation;
- primary lore/progression structure;
- location for Dr. Mobstenio content;
- associated with failed experiments 062 and 097 in the public guide.

Black Arcana should treat structure discovery and contained entities/items as Mobstein-owned world progression. No structure scan, forced chunk loading or duplicate spawn should be introduced for convenience.

## Witherstein Ruins

Publisher-documented world structure:

- associated with jungle generation;
- contains the skeleton used to awaken Witherstein;
- interaction with the Reviver Syringe starts the boss path.

Exact structure identifier, biome placement algorithm and generation frequency are not inferred.

## Old Ruins

Publisher documentation describes an **Old Ruins** jungle structure containing essential provider items/progression material.

Exact loot-table contents are not promoted beyond what the public guide explicitly states.

## Dr. Mobstenio

Publisher-documented progression:

- found in Frankenstein Castle;
- revived using Mobstenio Blood Syringe;
- tamed with Wither Spores obtained after the Witherstein encounter according to the guide;
- after revival, the guide describes wandering behavior and states that he cannot follow in the normal companion manner.

This is a named NPC/provider progression chain. Black Arcana must not duplicate or take ownership of Mobstenio state.

## Igor

Acquisition/activation summary:

- Igor is summoned from the Igor Spawner;
- not tameable;
- requires proximity to Igor Table/Station for the failed-experiment workflow;
- Suspicious Syringes are the provider interaction item;
- experiments 062 and 097 are excluded from the ordinary Igor random pool in the current public guide.

## Witherstein

The public guide documents a three-stage boss encounter:

1. locate the skeleton in the center of Witherstein Ruins;
2. use Reviver Syringe to revive/awaken Witherstein;
3. progress through three boss stages;
4. the later two stages spawn many Wither Skeletons.

The publisher also comments on imperfect flying/attack behavior. That qualitative note is not converted into an AI contract.

Witherstein is a provider-owned boss and resurrection-triggered encounter. Black Arcana should not double-award spell/mastery credit for the awakening itself unless a future causal contract explicitly maps that progression milestone.

## Acquisition and progression authority

The documented Mobstein chain combines:

- body/anatomical harvesting;
- organ extraction;
- machine crafting/use;
- stretch resurrection;
- syringes;
- tame items;
- world structures;
- named NPCs;
- boss progression;
- Igor random experiments.

Black Arcana integrations should preserve these gates. In particular:

- no global structure scan;
- no forced chunk loading;
- no bypass of provider tame requirements;
- no client-authored claim that a resurrection/boss event happened;
- no generic recreation of Reviver/Lightningbolt/Mobstenio/Suspicious syringe semantics;
- no synthetic registry IDs or event names based on documentation labels.

## Current exact-version gaps

Still `UNVERIFIED` at this public-only checkpoint:

- exact structure registry IDs;
- structure spawn weights/frequency;
- exact loot-table IDs/weights;
- exact boss health/damage values;
- exact syringe item registry IDs and recipes;
- resurrection timing implementation beyond publisher-visible approximately-15-second wording;
- server event hooks suitable for third-party causal credit;
- Sable interaction inside structures/machines;
- full-modpack runtime compatibility.