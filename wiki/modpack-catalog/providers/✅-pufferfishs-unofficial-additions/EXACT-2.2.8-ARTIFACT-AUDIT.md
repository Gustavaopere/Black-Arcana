# Pufferfish's Unofficial Additions 2.2.8 — exact artifact audit

Status: `EXACT PHYSICAL=PUBLISHER / XP-REWARD BRIDGE SURFACE CLOSED / SEMANTIC DENOMINATOR ZERO`

## Identity gate

- JAR: `pufferfish_unofficial_additions-1.21.1-2.2.8.jar`;
- mod id: `pufferfish_unofficial_additions`;
- runtime: `2.2.8`;
- physical SHA-1: `b273ea691e027b33fb9a19fb966c5f072edfa5c0`.

NON-MERGE PR #547 audits CurseForge project/file `935166 / 7389968`.

Audit evidence:

- run: `37137288035` — SUCCESS;
- artifact: `11277989415`;
- digest: `sha256:277c4c8d88684ab28c67e30b4419bb54a5e875f97f0fde4b95670037e8a5bdcc`;
- publisher SHA-1: `b273ea691e027b33fb9a19fb966c5f072edfa5c0`;
- publisher SHA-256: `2f7831975da0740fd29f9bee775ac9fe43d3650c9d0720e8c4f108241c4092d8`;
- bytes: `52,976`.

Physical/publisher equality is proven by SHA-1.

## Archive inventory

- entries: **46**;
- classes: **27**;
- resources: **19**;
- provider data entries: **0**;
- provider JSON definitions: **0**;
- bounded semantic-path hits: **7**;
- experience/reward-related path hits: **39**.

All seven semantic-path hits belong to the optional Iron's bridge (`Data`, prototypes/events, spell/school conditions and `SpellCastingExperienceSource`). They reference existing Iron's spell/school registries rather than registering new spells.

## Exact extension identities

Direct disassembly closes:

- `spell_casting` — Pufferfish Skills experience source;
- `fishing` — experience source;
- `harvest_crops` — experience source;
- `effect` — configurable reward factory;
- `spell` and `school` calculation/condition surfaces;
- `walk_on_powder_snow` tag-based movement permission hook.

The `spell_casting` data record carries existing Iron's spell/school holder, rarity, mana cost, mana cost per second, cast duration, charge time, cooldown and related values into a calculation prototype. These are observer/calculation inputs.

## Effect reward

The exact reward parses a configured mob effect plus reward type/amplifier/icon/duration-modification data and registers via the Pufferfish Skills Reward API.

Its supported behavior can grant an effect, create effect immunity or modify effect treatment, but the concrete effect identity is configuration-supplied. The addon packages no tree/config JSON that instantiates a fixed semantic action.

## Semantic disposition

Experience sources, calculation conditions/prototypes, configurable reward factories and tag hooks are progression/integration infrastructure.

The exact artifact contains no provider-owned spell registry, ritual/glyph/rite action roster or packaged concrete skill tree.

Result: **`ZERO_SEMANTIC_SKILL_XP_REWARD_BRIDGE / +0 strict`**.

## Clean-room boundary

The durable catalog stores hashes, counts, extension IDs and behavior-level classifications required for ownership/deduplication. It does not redistribute third-party JAR bytes or implementation bodies.
