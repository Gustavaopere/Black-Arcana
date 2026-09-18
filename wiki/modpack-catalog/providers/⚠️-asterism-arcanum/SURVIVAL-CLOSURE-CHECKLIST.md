# Asterism Arcanum 0.1.0 — Astral Gateway Survival Closure Checklist

Status: `REGISTRY 11 EXACT / 10 SURVIVAL COUNTED / ASTRAL GATEWAY DEFAULT HOST LOOT-ELIGIBLE / DEPLOYED IRON'S SPELL CONFIG UNVERIFIED / PROVIDER REMAINS CONDITIONAL`

## Purpose

Asterism Arcanum 0.1.0 already has a closed registry inventory:

- 11 registered spells in `ASARSpellRegistry`;
- 10 publisher-supported survival spells already cataloged and counted;
- 1 additional active registration, `asterismarcanum:astral_gateway`, documented by the release/lang surface as creative-only, unfinished and not intended to be craftable;
- `TrailblazeSpell` exists in source but its registration is commented and is therefore not a runtime spell for 0.1.0.

The remaining catalog blocker is not spell identity. It is the effective **survival reachability** of Astral Gateway in the assembled pack.

## Exact conditional identity

| Spell | Registry | Publisher/release disposition | Effective pack reachability | Current catalog disposition |
|---|---|---|---|---|
| `asterismarcanum:astral_gateway` | `EXACT / ACTIVE` | `CREATIVE-ONLY / UNFINISHED / NOT INTENDED CRAFTABLE` | `NÃO VERIFICADO` | `CONDITIONAL / OUTSIDE STRICT COUNT` |

Known source-backed spell metadata already cataloged separately:

- school: `asterismarcanum:astral`;
- rarity: Legendary;
- level: 1;
- mana: 300;
- cooldown: 60 s;
- LONG cast, 40 ticks / 2 s;
- radius: 8.

Those values do not resolve survival availability.

## Exact host-default survival path now proven

Exact Asterism 0.1.0 source plus exact Iron's 3.16.3 source closes the static host semantics more tightly:

1. `AstralGatewaySpell` is actively registered as `asterismarcanum:astral_gateway`;
2. it is Legendary, but Iron's `RandomizeSpellFunction` does **not** use loot `quality` to filter rarity;
3. the Astromancer `quality 0.25..0.85` range is applied only after spell selection to calculate spell level;
4. Legendary spells remain eligible in the weighted selection pool with weight `4`;
5. Astromancer loot filters by school `asterismarcanum:astral`;
6. Iron's school-filter path requires only effective `spell.isEnabled()` and `spell.allowLooting()`;
7. `AstralGatewaySpell` does not override either method;
8. Asterism constructs the Astral school through the Iron's seven-argument `SchoolType` constructor, whose exact 3.16.3 defaults are `requiresLearning=false` and `allowLooting=true`;
9. `AstralGatewaySpell` does not explicitly disable `allow_crafting`, whose Iron's host default is `true`.

Therefore the **default provider-native path is positively loot-eligible and craft-eligible**. The remaining uncertainty is not rarity/quality behavior. It is whether the actual assembled pack overrides the spell's effective Iron's config.

See [`IRONS-3.16.3-HOST-LOOT-ELIGIBILITY.md`](IRONS-3.16.3-HOST-LOOT-ELIGIBILITY.md).

Static defaults still cannot substitute for deployed configuration/datapack state.

## Required authoritative evidence

Close this gate using at least one authoritative current-pack path:

### Gate A — deployed Iron's spell configuration/datapack evidence

Capture the actual deployed Iron's spell configuration and relevant datapack state for the current pack/world.

Exact Iron's 3.16.3 config targets are:

- per-spell local file: `/config/irons_spellbooks_spell_config/asterismarcanum/astral_gateway.json`;
- global fallback file: `/config/irons_spellbooks_spell_config/global_config.json`;
- datapack override: `/data/asterismarcanum/irons_spellbooks_spell_config/astral_gateway.json`.

Resolve at minimum:

- effective `irons_spellbooks:enabled`;
- effective `irons_spellbooks:school`;
- effective `irons_spellbooks:allow_crafting`;
- any global/datapack value that overrides those fields.

For the Astromancer loot path, no separate per-spell `allow_looting` config exists in exact Iron's 3.16.3: `AbstractSpell.allowLooting()` delegates to the effective school's `allowLooting` flag. The Astral school source default is `true`.

A deployed `enabled=false`, a school override away from `asterismarcanum:astral`, or another authoritative provider/datapack suppression can close the loot path negatively. If no such override exists, the exact host semantics above establish a provider-native default loot path.

Do not infer deployed values from source defaults.

### Gate B — real-pack acquisition observation

On the actual assembled pack, exercise the provider-native survival acquisition paths relevant to Astral spells, including:

- Astromancer Astral-scroll loot generation;
- Scroll Forge / normal spell crafting eligibility where applicable;
- any other provider-native survival source exposed by the installed configuration.

Record whether Astral Gateway is reachable without commands/creative intervention.

A positive observation must identify the provider-native path. A negative observation is only conclusive when the tested path and deployed gate state are sufficiently bounded; a small random sample of loot is not proof of exclusion.

## Acceptance branches

### A. Gateway is authoritatively excluded from survival

If deployed config/datapack evidence or a deterministic provider-native gate proves Astral Gateway cannot enter survival acquisition:

- keep `astral_gateway` cataloged as an exact non-survival registration;
- keep it outside the strict survival semantic count;
- the remaining provider prefix may be reconsidered independently of unrelated runtime QA, because runtime compatibility issues are not catalog status by themselves.

### B. Gateway is authoritatively survival-reachable

If the actual pack exposes Astral Gateway through a provider-native survival path:

- reclassify its catalog reachability accordingly;
- update the strict semantic ledger only after the exact active survival state is reconciled with the global counting rule;
- do not interpret reachability as proof that the unfinished runtime is safe or supported;
- do not create any additional Black Arcana acquisition source.

### C. Effective state remains unavailable

Keep Asterism Arcanum at `⚠️ Parcial / condicionado` and keep Astral Gateway outside the strict count.

## Already closed — do not redo

- installed artifact identity `asterismarcanum-1.21.1-0.1.0.jar`;
- exact source pin `BirdieVibes/Asterism-Arcanum@f1738c7813a85d31a6da10e6c9f2dbce18d2b583`;
- registry size 11;
- 10/10 ordinary survival spell identities and individual cards;
- Astral Gateway exact registry ID and individual card;
- Trailblaze exclusion because its registration is commented;
- Astral school identity and source-backed school membership;
- Astromancer randomized Astral-scroll loot pipeline;
- provider-native settlement boundaries for all cataloged spells.

## Separate runtime QA — not this catalog gate

The existing technical audit records runtime questions for Celestial Tether, Silvery Barbs, Starcutter, Starfire, Star Swarm, Luminous Beam and Summon Lunar Moth. Those remain runtime/provider QA and must not be used as a reason to invent a second settlement path.

This checklist resolves only the **survival classification of `asterismarcanum:astral_gateway`**.

## Authority boundary

Asterism/Iron's remain authority for Astral spell registration, acquisition, teleport settlement, damage, summons and configuration. Black Arcana may catalog and observe supported final state, but must not recreate Astral Gateway, force-enable it, synthesize a loot source or compensate for provider bugs.
