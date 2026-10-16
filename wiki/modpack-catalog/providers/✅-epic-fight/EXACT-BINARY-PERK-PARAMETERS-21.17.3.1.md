# Epic Fight 21.17.3.1 — exact binary packaged perk parameters (16/10/2026)

**Evidence level (descriptive, not a new registry enum):** exact publisher/physical packaged JSON + compiled symbol presence for **13 pre-existing** core skill IDs. This is **not** behavioral equivalence, a perk hook contract, or adapter/runtime acceptance. Registry disposition remains exactly as established by the separate 43-ID audit.

## Exact artifact and reproducible run

- Sibling physical authority: `neoforge-rpg-skilltree/PROJECT-INSTRUCTIONS/modlist/Adventure and RPG + API and Library + Armor, Tools, and Weapons/✅-epic-fight v21.17.3.1.md`, `modlist(1).txt` #260, `epic-fight-21.17.3.1-mc1.21.1-neoforge.jar`, mod id `epicfight`, Minecraft 1.21.1, NeoForge.
- Publisher CurseForge project/file **405076 / 8175609** fetched from `https://cursemaven.com/curse/maven/epic-fight-mod-405076/8175609/epic-fight-mod-405076-8175609.jar`.
- Installed/publisher SHA-1 **`fb199b7bbea2fc402da28ab586e73f47e32f8fc0`**; exact publisher SHA-256 **`8b882554cf10086398340fbdc741819ee72a801a3adce516c7f4768326a39526`**. Workflow hard-gates **both hashes before reading any skill**.
- Reproducible verifier: [`docs/qa/epicfight_211731_perk_binary.py`](https://github.com/Gustavaopere/Black-Arcana/blob/docs/catalog-perk-causality-20261015/docs/qa/epicfight_211731_perk_binary.py), [GitHub workflow](https://github.com/Gustavaopere/Black-Arcana/blob/docs/catalog-perk-causality-20261015/.github/workflows/epicfight-211731-perk-binary.yml).
- **First run:** [38978906335](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38978906335) `FAILURE` even with both hashes, 9 JSON and other class symbols matching, because the verifier incorrectly looked for event constants in outer `EpicFightEventHooks` rather than inner `EpicFightEventHooks$Entity` and `$Player`. The three false-negative assertions were corrected without dropping the checks.
- **Corrected initial run:** [38979022783](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38979022783), **SUCCESS** on corrected script commit `0c8cc892d60b7e4fb7f78f77ef5b1b8e80ef5734` (run checkout merge ref is distinct). Historical scope: **6/6 synthetic tests PASS; 9/9 packaged JSONs; 12/12 classfile symbols; 0 deviations**; JSON-only artifact `12079209973`.
- **Latest expanded proof:** [38979547368](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38979547368), **SUCCESS** after adding four passives, on script commit `ea272cf44f075c0054eac7e29c219c0c0f2a904b`: **8/8 synthetic tests PASS, 13/13 exact packaged JSONs, 17/17 classfiles with symbols present, 0 deviations**. Bounded JSON-only artifact `12080695954`. Both hashes independently matched again. Neither publisher JAR nor class bytecode is redistributed.

## Precise static facts proven at this gate (13 JSON resources)

| Core registry ID (all previously classified) | Exact packaged resource facts |
|---|---|
| `epicfight:parrying` | `penalizer=0.6`, `parry_window=8` |
| `epicfight:impact_guard` | `penalizer=0.6`, `superior_penalizer=0.2`, `damage_reducer=0.2` |
| `epicfight:swordmaster` | `speed_bonus=30`; `epicfight:stamina_regen` `add_value +0.2`, `epicfight:stamina` `add_value +2` |
| `epicfight:forbidden_strength` | `minecraft:generic.attack_damage` `add_multiplied_total +0.05`; `minecraft:generic.max_health` `add_value +4` |
| `epicfight:technician` | `epicfight:stamina_regen` `add_value +0.4` |
| `epicfight:berserker` | `speed_bonus=0.5`, `damage_bonus=0.3`, `epicfight:stamina` `add_value +6` |
| `epicfight:stamina_pillager` | `regen_rate=30`, `minecraft:generic.attack_damage` `add_multiplied_total +0.1`, `epicfight:stamina` `add_value +3` |
| `epicfight:death_harvest` | `minecraft:generic.attack_damage` `add_multiplied_total +0.15` |
| `epicfight:roll` | `consumption=4` |
| `epicfight:step` | `consumption=3` |
| `epicfight:wrathful_lighting` | `consumption=50` (unit/resource semantics **not** inferred from JSON alone) |
| `epicfight:tsunami` | `consumption=50` |
| `epicfight:everlasting_allegiance` | `consumption=40` |

Data comes from packaged `data/epicfight/skill_parameters/<id>.json`; parser verifies object identity, required scalar values and modifier operation/amount. It does **not** certify that a world's datapack did not override these values.

**Classfile symbol presence** from Java21 `javap -p -c -constants`: `ParryingSkill`, `ImpactGuardSkill`, `SwordmasterSkill`, `ForbiddenStrengthSkill`, `DodgeSkill`, **`TechnicianSkill`, `BerserkerSkill`, `StaminaPillagerSkill`, `DeathHarvestSkill`, `DeathHarvestOrb`**, `WrathfulLightingSkill`, `EverlastingAllegiance`, `EpicFightMovesets`, `EpicFightSkills`, **`EpicFightEventHooks$Entity`**, **`EpicFightEventHooks$Player`**, `SkillContainer`. Checks require names of selected hooks, fields, methods and selector identities. Existence of string/symbol != correct instruction sequence, event ordering, non-cancelled hit, effective attribute adjustment or modification surface for optional perks.

## Counts / status boundaries

- **Exact core registry remains 43/43 dispositioned** (previous exact audit). Three trident innates already counted magical; 40 core skills excluded from magic metric.
- **Exact packaged parameters + compiled symbols at this gate: ✅ 13/43 core skill IDs (30.23%)**. The scope is *limited static binary evidence*; **17 inspected classfiles** include supporting infrastructure/components and **do not** represent 17 extra semantic skill IDs.
- **Aprofundamento source para perks:** as quatro passivas adicionais `technician`, `berserker`, `stamina_pillager`, `death_harvest` são analisadas causalmente na revisão upstream **21.17.3**, não por equivalência completa de bytecode. Agora seus **JSONs empacotados e símbolos compilados** também foram confirmados no JAR **21.17.3.1** (run 38979547368), mas **não** a instrução-por-instrução, event phase ou settlement. Profundidade documental **13/43 (30.23%)**.
- **Global magic semantic floor unchanged:** 1,856 minimum / 1,854 strict, unknown denominator. This proof adds **0** new magical identities.
- **Runtime/adapter/perk acceptance:** ⚠️/⛔ not validated. Stage 06.05 🟡, physical Stage 09 pending. In particular, do not equate `consumption` with committed stamina, mana or cooldown; do not duplicate hit, thunder, trident return, kill proc, dodge or cost.

## Required next proof

Expand structural verification from symbols to **bounded instruction/control-flow fragments** for conditions, sidedness, event subscription and settlement; inspect data overrides in the **assembled 587-entry pack**, validate `stamina` attributes, protection, multiplayer, Arcana/Iron's co-existence, `RPG Skill Tree` real provider contract. Only after this may a perk hook be called SAFE. No Java runtime integration or client test is asserted here.
