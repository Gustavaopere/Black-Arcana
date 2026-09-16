# IronSable 1.2.0 — technical audit

## Evidence hierarchy

1. Current modlist: `ironsable-1.2.0.jar`, runtime `1.2.0`.
2. Notion audit entry: installed 1.2.0 physics bridge.
3. Exact CurseForge release: project `1625528`, file `8598255`, NeoForge 1.21.1.
4. Official Modrinth/CurseForge description: seven new spells, ten physicalized existing spells, acquisition rules and qualitative physics contracts.
5. Historical runtime logs from this pack: all seven `spell/ironsable/*` IDs observed registered.
6. Linked GitHub issue repository `emariduble-cmd/IronSable`: no mod source tree; therefore no source-code authority is claimed.

## Inventory closure

Runtime-observed IronSable spell IDs:

- `ironsable:maelstrom`
- `ironsable:tempests_grasp`
- `ironsable:gyroscopic_spin`
- `ironsable:downburst`
- `ironsable:stasis_lock`
- `ironsable:kinetic_barrier`
- `ironsable:elastic_tether`

This matches the official 1.2.0 statement of seven new spells. Inventory is therefore closed at **7/7** even though bytecode is not yet extracted.

## Conditional school classification

The exact 1.2.0 changelog says Tempest's Grasp, Downburst and Maelstrom use the Wind school when Wind's Spellbooks is installed. The current modlist contains `wind_spellbooks-1.0.5.jar`, so that condition is active in this pack.

The public evidence consulted does not identify the schools of Gyroscopic Spin, Stasis Lock, Kinetic Barrier or Elastic Tether. They stay `NÃO VERIFICADO`; no school is inferred from effect theme.

## Physicalized base spells

IronSable extends Telekinesis, Gust, Sonic Boom, Shockwave, Black Hole, Gravity Fissure, Stomp, Blizzard, Earthquake and Raise Hell with Sable-ship behavior. The provider explicitly states that their damage, mana and cooldowns are untouched. Their normal spell stats remain owned by Iron's Spells.

See [PHYSICALIZED-BASE-SPELLS.md](PHYSICALIZED-BASE-SPELLS.md).

## Authority and deduplication

IronSable is authoritative for translating a supported spell's kinetic intent into Sable ship/object physics. A Black Arcana integration must not add a second generic knockback, teleport, rotation or velocity mutation after IronSable has already handled that cast.

Fail closed if the exact 1.2.0 physics hook cannot be proven. A generic entity knockback fallback is not semantically equivalent to moving a Sable ship/sublevel and can double force, bypass mass rules, or desynchronize server/client state.

## Public physics API

Release 1.2.0 advertises a public physics API for companion mods. Existence is confirmed, but exact package names, classes, methods, event ordering, ownership semantics and thread/side expectations are **NÃO VERIFICADO** because neither public source nor extracted 1.2.0 bytecode is available in this audit.

No Black Arcana implementation should compile against guessed API symbols.

## Runtime QA matrix

- dedicated-server authority for force/rotation/freeze/tether operations;
- one cast -> one physics application per target ship;
- ship mass/capacity behavior, especially Telekinesis;
- self-ship and allied-player behavior for Downburst/Kinetic Barrier;
- terrain anchoring semantics for Elastic Tether;
- channel cancellation and cleanup for Stasis Lock/Gyroscopic Spin/Kinetic Barrier;
- target invalidation/removal/chunk unload while a spell is active;
- Sable sublevel coordinate transforms and moving frames;
- cross-dimension/chunk transitions;
- coexistence with other Sable bridges and Create Aeronautics;
- Wind school binding with Wind's Spellbooks 1.0.5 present;
- optional Raise Hell hot-air-balloon inflation path;
- exact spell configs: levels, rarity, mana, cooldown, cast type/timing, range, caps and formulas.

## Historical compat warning

Old debug logs also mention a distinct `ironssablecompat` mixin identity. That historical compatibility component must not be silently merged with the current top-level `ironsable` identity. Presence/JAR authority is the current modlist, which contains `ironsable-1.2.0.jar`.

## Status

`CATALOG COMPLETE 7/7 / EXACT RELEASE PINNED / BYTECODE + LIVE PHYSICS QA PENDING`