# Effects, potions and brewing — Apothic Attributes 2.10.1

## Provider mob effects

### Bleeding

- harmful;
- applies every 40 ticks;
- damage amount: `1 + amplifier`;
- exact source uses `apothic_attributes:bleeding` damage source with last-attacker context.

### Detonation

- harmful;
- source triggers only when effect duration reaches 1 tick;
- reads remaining fire ticks, clears them and deals `(1 + amplifier) * fireTicks / 14` damage;
- emits flame particles and dragon-fireball explosion sound;
- exact 2.10.1 source call uses `ALObjects.DamageTypes.BLEEDING` in `hurt(...)`, despite a separate registered/tagged `DamageTypes.DETONATION` key;
- source contains a TODO noting it would ideally trigger on removal rather than only the last tick.

This discrepancy is retained literally. The catalog does not silently substitute the registered detonation damage key for the call observed in source.

### Grievous

- harmful;
- adds `-0.4` to `healing_received` through provider attribute-modifier semantics.

### Ancient Knowledge (`knowledge`)

- beneficial;
- modifies `experience_gained` with `ADD_MULTIPLIED_TOTAL`;
- magnitude function: `knowledgeMultiplier * (amplifier + 1)`;
- `knowledgeMultiplier` defaults to 4.0 and is server-synced to clients.

### Sundering

- harmful marker effect;
- runtime is injected through `LivingEntityMixin` rather than an effect tick.

### Vitality

- beneficial;
- adds `+0.2` to `healing_received` through provider attribute-modifier semantics.

### Flying

- beneficial;
- adds +1 to NeoForge `CREATIVE_FLIGHT` with provider modifier id `apothic_attributes:flying`;
- provider explicitly applies that modifier at amplifier 0.

## Potions — 31

The central registry provides 31 potion variants across Resistance, Absorption, Haste, Fatigue, Wither, Sundering, Knowledge, Vitality, Grievous, Levitation and Flying families. Exact IDs are listed in `REGISTRY-AND-CONTENT-SURFACE.md`.

## Brewing mixes — 37

`MiscDatagen.genPotionRecipes()` generates 37 `brewing_mixes` entries. The graph includes:

- Awkward -> Resistance via Shulker Shell;
- Resistance <-> Sundering inversion paths and long/strong variants;
- Awkward -> Absorption via Golden Apple;
- Awkward -> Haste via Mushroom Stew;
- Haste <-> Fatigue inversion paths and long/strong variants;
- Awkward -> Wither via Wither Skeleton Skull;
- Awkward -> Knowledge via Experience Bottle;
- Awkward -> Vitality via Sweet Berries;
- Vitality <-> Grievous inversion paths and long/strong variants;
- Slow Falling -> Levitation via Fermented Spider Eye;
- Levitation -> Flying via Popped Chorus Fruit;
- Flying -> Long Flying -> Extra Long Flying via Redstone.

Brewing recipes are provider content/data. Black Arcana should not clone them as BA rituals or spells merely because some effects overlap thematically.
