# Awakening

Status: `SOURCE-PINNED 5.13.1 / ENTITY-WORLD CONVERSION RITUAL`

- Registry id: `ars_nouveau:ritual_awakening`
- Class: `RitualAwakening`
- Exact release checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Provider-native modes

### Bookwyrm Charm mode

If any consumed item is a `WritableBookItem`, the ritual enters Bookwyrm mode. Once per 20 server ticks it compares progress with the total count of consumed writable books and emits one `BOOKWYRM_CHARM` for each progress slot until that total is reached, then finishes.

### Awakening mode

Without writable books, after progress exceeds `5` the ritual searches positions within Manhattan bounds `(3,1,3)` around the brazier.

For each candidate position it performs provider DFS searches capped at `350` matching blocks for four Archwood families:

- Blazing;
- Flourishing;
- Vexing;
- Cascading.

A matching tree requires at least `50` connected provider log/leaf blocks. When found, the ritual destroys the returned component through Ars' safe-destroy helper and selects the corresponding Weald Walker entity.

A nearby Budding Amethyst is a separate conversion route: that block is replaced with air and an Amethyst Golem is selected.

After a valid target is resolved, the ritual spawns the selected LivingEntity at the converted location and finishes.

## World-safety boundary

This class does not expose the same explicit `destroyRespectsClaim(...)` preflight seen in some other Ars world-effect paths; it delegates tree removal to `destroyBlockSafelyWithoutSound` with an Ars fake player. Whether all protection providers are respected in the installed full pack is therefore a **runtime QA item**, not inferred from helper naming.

Black Arcana must not replay these block removals/entity creations. Any independent Black Arcana world conversion remains governed by `WorldEffectPolicy`.

## Authority

Weald Walker/Golem identity, Bookwyrm Charm creation and conversion lifecycle remain Ars Nouveau authority. They are not Black Arcana summons/familiars merely because the ritual creates living magical entities.