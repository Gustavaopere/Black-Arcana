# Astral Gateway

- Provider: **Asterism Arcanum** (`asterismarcanum`)
- Installed artifact: `asterismarcanum-1.21.1-0.1.0.jar`
- Registry ID: `asterismarcanum:astral_gateway`
- School: `asterismarcanum:astral`
- Rarity: **Legendary**
- Levels: **1**
- Mana: **300**
- Cooldown: **60 s**
- Cast: **LONG**, 40 ticks / 2 s, without cast-time scaling
- Radius: **8**
- Registry state: **active**
- Catalog state: `REGISTERED / CREATIVE-ONLY / UNFINISHED / FAIL-CLOSED`

## Survival boundary

The release language describes Astral Gateway as not fully implemented or craftable and treats it as creative-only. Black Arcana therefore does not approve it for canonical survival progression, perks or new acquisition sources.

There is a static acquisition inconsistency: the spell class does not disable looting, its `DefaultConfig` does not disable crafting, the Astral school keeps Iron's default `allowLooting=true`, and the Astromancer loot table can roll Astral-school scrolls. This means a survival exposure path may exist if no deployed config/datapack blocks it; that effective pack state is not inferred here.

## Runtime boundary

The audited source moves a `ServerPlayer` between the Astral Sea and its return destination. Teleport settlement, destination state and all provider-side effects remain Asterism/Iron's authority; Black Arcana must not duplicate the gateway runtime.

Source: `../NON-SURVIVAL.md` and `../TECHNICAL-AUDIT.md`.
