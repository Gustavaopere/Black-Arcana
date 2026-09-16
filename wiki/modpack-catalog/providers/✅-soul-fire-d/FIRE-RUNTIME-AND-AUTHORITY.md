# Soul Fire'd 6.1.0 — fire runtime and authority

This file records the exact installed/source-visible Soul Fire surface while keeping the generic custom-fire framework under its actual 6.x provider, Prometheus.

## Authority migration

Historical Soul Fire'd versions exposed their own fire API. That is not the installed architecture.

For the 6.x line, publisher documentation says the API moved to Prometheus. Exact 6.1.0 source confirms this mechanically: Soul Fire'd imports and calls Prometheus `Fire`, `FireManager` and `FireRegistrar` instead of defining a second generic fire manager.

Black Arcana consequence: do not build an integration against historical Soul Fire'd API assumptions. A provider boundary for generic fire typing must be verified against the physical **Prometheus 1.2.5** contract.

## Exact physical provider stack

| Component | Physical version | Role in this boundary |
|---|---:|---|
| Soul Fire'd | 6.1.0 | Soul Fire content/registration, enchantments and acquisition |
| Prometheus | 1.2.5 | generic Fire API/runtime/component registration |
| Cobweb | 1.4.0 | registration/static-data-pack support used by this line |
| NeoForge | 21.1.248 | loader/runtime |

Exact Soul Fire'd source metadata asks for Prometheus 1.2.5 and Cobweb 1.4.0. The physical pack matches both exactly. Its NeoForge metadata requires `[21.0,)`, satisfied by 21.1.248.

## Exact Soul Fire registration

Soul Fire'd's `FireRegistry` aliases:

- `SOUL_FIRE_TYPE = FireManager.SOUL_FIRE_TYPE`.

Exact Prometheus 1.2.5 defines that type as:

- `minecraft:soul`.

Soul Fire'd then calls Prometheus's fire builder with:

- default components;
- vanilla Soul Fire flame particle;
- light `10`;
- damage `2`.

It finally asks Prometheus `FireRegistrar` to register the associated fire charge.

This split matters:

- the **definition values and request to instantiate Soul Fire content** are Soul Fire'd's responsibility;
- the **generic builder, component model, registry helpers, dynamic tags and fire runtime** are Prometheus's responsibility.

## Associated Soul Fire Charge

The exact source contains the item/model/recipe resource family for `minecraft:soul_fire_charge`, and the recipe result names that ID explicitly.

Recipe:

- 1 gunpowder;
- 1 ghast tear;
- 1 coal **or** charcoal;
- output: 16 `minecraft:soul_fire_charge`.

Exact Prometheus `FireRegistrar.registerFireCharge(...)`:

- derives the component item ID from the fire type;
- registers it in the fire type's namespace;
- adds the resulting item to `minecraft:creeper_igniters` through Prometheus's dynamic data pack;
- owns the generic registration helper.

For `minecraft:soul`, this resolves consistently with Soul Fire'd's exact resource/recipe ID `minecraft:soul_fire_charge`.

## Mixins

Two mixin config files are declared by NeoForge metadata because the multi-loader project carries common and NeoForge mixin manifests.

Both exact 6.1.0 manifests contain:

- `mixins: []`;
- `client: []`;
- `server: []`.

Therefore current exact mixin count is **0**. The presence of config filenames in physical metadata is not evidence of active mixin hooks.

## Causality and hazard safety

Soul Fire'd/Prometheus fire state is external provider state. Black Arcana must preserve causal identity:

1. BA decides and validates its own cast/hazard through the canonical server pipeline;
2. BA applies `WorldEffectPolicy` and its own bounded world-effect budgets where world mutation is involved;
3. only then may an integration request provider-native Soul Fire behavior through a verified boundary, if such a bridge is intentionally designed;
4. provider fire damage/enchantment effects remain provider events, not retroactively BA cast authority.

Do not let a generic entity-on-fire callback become a second BA spell pipeline.

## Backlash / proc boundary

Soul Fire'd's enchantments can ignite entities through Prometheus effects. This does not authorize Black Arcana Backlash to trigger normal offensive enchantment/proc chains.

The canonical Backlash invariant remains unchanged: Backlash is not a normal offensive proc source. Any future damage-source interoperability must preserve this causality rather than manufacturing a provider-enchantment attack context.

## RPG Skill Tree boundary

RPG Skill Tree may provide progression or attributes only through a real sibling contract. It does not own Soul Fire, Prometheus fire registration, provider enchantment effects, BA hazard state or BA casting.

## Runtime QA backlog

The following remain runtime QA rather than source-catalog assumptions:

- physical full-pack entity ignition/damage ordering;
- interactions with other mods modifying fire, damage or enchantment events;
- cross-dimension/relog fire-state behavior if relevant to Prometheus runtime;
- dedicated multiplayer synchronization of visual/functional Soul Fire state;
- provider updates that alter Prometheus fire API semantics or move authority again.
