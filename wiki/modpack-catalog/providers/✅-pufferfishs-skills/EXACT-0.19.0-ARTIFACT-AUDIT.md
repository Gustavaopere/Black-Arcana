# Pufferfish's Skills 0.19.0 — exact artifact audit

Status: `EXACT PHYSICAL=PUBLISHER / BASE FRAMEWORK SEMANTIC DENOMINATOR CLOSED AT ZERO`

## Identity gate

Current physical authority identifies:

- `puffish_skills-0.19.0-1.21-neoforge.jar`;
- mod id `puffish_skills`;
- runtime `0.19.0`;
- SHA-1 `fa134a526ab2f098559b7d824269ae36aaac32b3`.

NON-MERGE PR #544 downloads CurseForge File `835091 / 8792775` and verifies equality before semantic inspection.

Audit evidence:

- run: `37033574051` — SUCCESS;
- artifact: `11238467501`;
- artifact digest: `sha256:ee970728d121ebd403665786bac6e789c41fe1191fa3aefe4ef96ea4e9a65810`;
- publisher SHA-1: `fa134a526ab2f098559b7d824269ae36aaac32b3`;
- publisher SHA-256: `6dcacba36cc157d7b9889764521564162e06636c65b4b189e67a68684636dfa6`;
- bytes: `649,853`.

Result: exact physical/publisher byte identity is proven by SHA-1.

## Archive inventory

- archive entries: **426**;
- classes: **334**;
- resources: **92**;
- `data/puffish_skills/**` entries: **0**;
- packaged valid provider JSON definitions under that namespace: **0**;
- invalid provider JSON definitions: **0**.

## Semantic-like path audit

The bounded scan reports **9 semantic-like paths**. All nine are infrastructure around criteria/experience:

- `CriterionExperienceSource` and its data class;
- advancement/criterion mixins;
- `SkillsCriteria` and `SkillUnlockedCriterion`.

They are not player-selected supernatural action identities.

The broader skill-path inventory is dominated by framework/API/config/UI/network/persistence classes such as `Category`, `Skill`, `Exchange`, `Experience`, `Reward`, `SkillsAPI`, tree config, commands and synchronization.

## Reward implementation audit

Exact built-in reward classes include:

- `AttributeReward`;
- `CommandReward`;
- `PointsReward`;
- `ScoreboardReward`;
- `TagReward`;
- `DummyReward`.

These are generic execution primitives. They can be parameterized by external skill-tree data but do not form a fixed provider-owned action roster.

## Negative semantic closure

The exact artifact contains no provider datapack tree and no fixed registry/resource surface for spell, magic, ritual, mana, arcane, glyph, summon or equivalent provider-owned supernatural actions.

A `Skill` object in this framework is a progression node/state container. It is not automatically a spell. The concrete consequence of unlocking a skill is defined through external configuration/addons/rewards.

Therefore the base provider semantic denominator is **0**.

## CI note

The exact audit workflow succeeded. The parallel repository CI run #4124 failed during Gradle unit-test setup because configuration-cache serialization of `:compileJava` failed; provider catalog collector Python tests passed, and the failure occurred independently of the artifact-audit evidence. No runtime/build PASS is inferred from this audit.

## Clean-room boundary

The durable catalog retains hashes, counts, class/resource names and behavior-level classification necessary to identify the provider surface. No third-party JAR bytes or implementation bodies are committed.
