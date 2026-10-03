# Pufferfish's Skills — 0.19.0

Status: `✅ CATALOGED / EXACT PHYSICAL=PUBLISHER ARTIFACT / ZERO_SEMANTIC_SKILL_TREE_FRAMEWORK / +0 STRICT / RUNTIME-DATAPACK QA SEPARATE`

## Current physical identity

Sibling physical authority: `neoforge-rpg-skilltree` dossier for physical row **#464**.

- JAR: `puffish_skills-0.19.0-1.21-neoforge.jar`;
- mod id: `puffish_skills`;
- runtime: `0.19.0`;
- Minecraft / loader: NeoForge 1.21/1.21.1;
- physical SHA-1: `fa134a526ab2f098559b7d824269ae36aaac32b3`;
- installed causal consumer: Pufferfish's Unofficial Additions 2.2.8.

Pufferfish's Skills is a data-driven skill-tree framework: categories, nodes, connections, points, experience, exchanges, generic rewards, persistence, UI and API. It is not itself a fixed spell/ritual provider.

## Exact artifact closure

NON-MERGE evidence PR **#544** audits the exact current publisher artifact.

- exact-artifact run: `37033574051` — **SUCCESS**;
- evidence artifact: `11238467501`;
- artifact digest: `sha256:ee970728d121ebd403665786bac6e789c41fe1191fa3aefe4ef96ea4e9a65810`;
- CurseForge project/file: `835091 / 8792775`;
- publisher SHA-1: `fa134a526ab2f098559b7d824269ae36aaac32b3`;
- publisher SHA-256: `6dcacba36cc157d7b9889764521564162e06636c65b4b189e67a68684636dfa6`;
- bytes: `649,853`.

The publisher SHA-1 exactly equals the physical pack SHA-1.

See [`EXACT-0.19.0-ARTIFACT-AUDIT.md`](EXACT-0.19.0-ARTIFACT-AUDIT.md).

## Semantic result

The exact JAR contains **426 archive entries / 334 classes / 92 resources**, but **zero `data/puffish_skills/**` provider datapack entries** and **zero packaged provider JSON skill-tree definitions**.

The bounded semantic-path scan finds nine paths, all belonging to criterion/experience infrastructure (`CriterionExperienceSource`, criterion mixins, `SkillsCriteria`) rather than player-owned spell/ritual/action identities.

Built-in reward implementations are generic framework operations:

- Attribute;
- Command;
- Points;
- Scoreboard;
- Tag;
- Dummy/support.

These rewards do not define a provider-owned magical action roster. A datapack or addon may configure a reward that causes an effect or command, but ownership of that configured content remains with the datapack/addon/integration, while Pufferfish's Skills owns framework execution/persistence.

Detailed disposition: [`SEMANTIC-SURFACE-0.19.0.md`](SEMANTIC-SURFACE-0.19.0.md).

## Why `+0` is the correct semantic count

The Black Arcana semantic metric counts fixed provider-owned spells, glyphs/spell-parts, rituals/rites and equivalent discrete supernatural player actions.

Pufferfish's Skills 0.19.0 provides a configurable progression engine. Its exact artifact does **not** package:

- a fixed skill tree under `data/puffish_skills/**`;
- provider-owned spell/ritual/glyph IDs;
- a mana/arcane/summon action registry;
- concrete provider-owned supernatural abilities.

Unlocking a configured skill is progression state, not automatically a magical action. Generic rewards such as Attribute or Command are also not semantic identities until a concrete external tree/addon defines what they do.

Therefore Pufferfish's Skills contributes **`+0 ZERO_SEMANTIC_SKILL_TREE_FRAMEWORK`**.

## Authority and deduplication boundary

Pufferfish's Skills remains authority for:

- category/tree loading and validation;
- points/experience/exchange;
- skill state and exclusive-root behavior;
- generic reward execution;
- persistence/synchronization/UI/API.

Concrete content supplied by another datapack/addon remains owned by that provider. Black Arcana must not count a configured external spell/action twice merely because Pufferfish's Skills unlocks or rewards it.

## Runtime/config QA remains separate

The sibling dossier correctly keeps deployed trees/datapacks fail-closed: JAR presence does not prove a concrete tree is installed. Current-world datapacks may define progression/rewards, and Pufferfish's Unofficial Additions extends the framework.

Those deployed-content questions can affect progression and reachability, but they do not reopen the **provider-owned semantic denominator**, which is closed at zero for the base framework.

The 0.19.1 upstream release is not installed and is not projected onto the current 0.19.0 bytes.

## Result

**✅ Cataloged — `ZERO_SEMANTIC_SKILL_TREE_FRAMEWORK`.**

Strict semantic delta: **+0**.
