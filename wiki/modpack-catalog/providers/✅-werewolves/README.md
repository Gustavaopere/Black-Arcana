# Werewolves 2.0.3.3 — provider catalog

## Status

`SOURCE-PINNED 2.0.3.3 / FACTION+FORMS+LEVELING+SKILLS+ACTIONS+EFFECTS+LORD+MINIONS INVENTORIED / STATIC MISMATCHES RECORDED / RUNTIME QA PENDING`

## Installed authority

- Minecraft: NeoForge 1.21.1 pack line.
- Installed JAR: `Werewolves-1.21-2.0.3.3.jar`.
- Runtime version in current modlist: `2.0.3.3`.
- Exact source authority: `TeamLapen/Werewolves@b72635b3e014e406b25bb79adb9d340f7443660b`.
- Source license at that exact revision: GNU LGPL v3.
- Black Arcana provenance records: `docs/provenance/REFERENCE_LEDGER.md`, `SOURCES.md`, `THIRD_PARTY_NOTICES.md`.
- That source declares `major_version=2`, `minor_version=3`, `patch_version=3` and Vampirism range `[1.10.0-beta.2,1.11.0)`, compatible with installed Vampirism 1.10.13.

The source audit is read-only evidence for this compatibility/catalog layer. No Werewolves code or assets are copied/adapted into Black Arcana by these documents.

## Provider role

Werewolves is not a spellbook provider and does not expose a mana school. It is a Vampirism-native supernatural faction provider with its own transformation/forms, bite pipeline, level progression, skill trees, actions, effects, Lord progression, refinements, minions, faction village/world content and weaknesses.

Black Arcana must model these capabilities as provider-native supernatural mechanics, not flatten them into generic mana spells or duplicate progression.

## Exact source inventory

| Surface | Exact source-level inventory |
|---|---:|
| Playable faction | 1 — Werewolf |
| Normal faction levels | 1–14 |
| Lord levels | 1–5 |
| Registered player actions | 9 |
| Registered Werewolves skills | 38, including normal/Lord roots |
| Own skills connected to generated normal tree | 33 |
| Own skills connected to generated Lord tree | 3 |
| Host Vampirism Lord skills referenced by Werewolves Lord tree | 3 |
| Registered own skills without normal generated-tree reachability proven | 2 — `resistance`, `sixth_sense` |
| Runtime forms registered by `WerewolfForm` | 5 — `none`, `human`, `beast`, `beast4l`, `survivalist` |
| Player form actions | 3 — Human, Beast, Survivalist |
| Werewolves mob effects | 8 |
| Werewolves-owned refinements | 13 |
| Werewolves tasks | 14 |
| Werewolves-owned minion task | 1 |
| Reused Vampirism minion tasks | 4 |
| Custom attributes | 4 |
| Overworld supernatural biome | `werewolves:werewolf_heaven`, display name Werewolf Forest |

`beast4l` is a provider form used by Alpha Werewolf entities; no player form action registers it.

## Canonical documentation

- [ACTION-FORM-CATALOG.md](ACTION-FORM-CATALOG.md) — actions, forms, transformation-time and bite semantics.
- [SKILL-TREE-CATALOG.md](SKILL-TREE-CATALOG.md) — registry, generated tree topology, reachability and skill effects.
- [PROGRESSION.md](PROGRESSION.md) — levels 1–14, Stone Altar and Lord 1–5 tasks.
- [EFFECTS-COMBAT.md](EFFECTS-COMBAT.md) — infection/cure, silver, wolfsbane, bleeding, stun, defenses and custom attributes.
- [MINIONS-REFINEMENTS.md](MINIONS-REFINEMENTS.md) — minion system, tasks and refinements.
- [TECHNICAL-AUDIT.md](TECHNICAL-AUDIT.md) — exact source authority, static mismatches and QA queue.
- [INTEGRATION-RULES.md](INTEGRATION-RULES.md) — Black Arcana contract.

## Critical authority boundaries

1. **Faction authority:** Vampirism `FactionPlayerHandler` + Werewolves faction registration own joining/leaving and levels.
2. **Transformation authority:** `WerewolfFormAction`, `WerewolfPlayer`, provider permissions and form state own transformation lifecycle.
3. **Level authority:** Werewolf `LevelHandler` + Stone Altar own normal progression; Vampirism task/Lord infrastructure owns Lord progression.
4. **Skill authority:** Vampirism skill registries/handlers carry Werewolves skill state and generated configured trees.
5. **Bite authority:** Werewolves owns `bite_damage`, bite cooldown/state, bite damage source, post-hit status and infection.
6. **Weakness authority:** Silver/Wolfsbane effects and provider damage handling own the intended vulnerabilities.
7. **Minion authority:** Vampirism minion infrastructure plus Werewolves minion data/tasks own Lord servants.
8. **Refinement authority:** Vampirism refinement framework carries Werewolves-owned refinement IDs/sets.

## World terminology correction

The source key is `werewolves:werewolf_heaven`, but the English display name is **Werewolf Forest** and generated tags include it in `minecraft:is_overworld`. Treat it as an Overworld biome, not a separate Werewolf Heaven dimension.

## Runtime QA still required

Source catalog completion is not runtime confirmation. Dedicated-server/in-pack QA remains required for transformation state, Epic Fight rendering/animation, skill-tree unlocks, Stone Altar settlement, bite/infection, silver/wolfsbane, action timing, minions, worldgen and the static mismatches recorded in `TECHNICAL-AUDIT.md`.