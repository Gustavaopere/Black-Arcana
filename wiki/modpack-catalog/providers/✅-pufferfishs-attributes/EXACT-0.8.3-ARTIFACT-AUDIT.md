# Pufferfish's Attributes 0.8.3 — exact artifact audit

Status: `EXACT PHYSICAL=PUBLISHER / 42 ATTRIBUTE IDS / SEMANTIC DENOMINATOR ZERO`

## Identity gate

Current physical authority:

- `puffish_attributes-0.8.3-1.21-neoforge.jar`;
- mod id `puffish_attributes`;
- runtime `0.8.3`;
- SHA-1 `9e6a87f790fc9281ea2685f8d4f6435d0d7c6d1f`.

NON-MERGE PR #546 downloads CurseForge File `991341 / 8610466` and fails before inspection unless its SHA-1 equals the physical fingerprint.

Audit evidence:

- run: `37137133861` — SUCCESS;
- artifact: `11278014339`;
- digest: `sha256:a0c3a257f169e2fea76ebf3f8b40643df650aa6f43bfeec638724c824ff13e99`;
- publisher SHA-1: `9e6a87f790fc9281ea2685f8d4f6435d0d7c6d1f`;
- publisher SHA-256: `b21c165e033360e112eb2c3426437e1ba4ebf70f971535b72b1b1891d04c87f0`;
- bytes: `235,542`.

## Exact archive inventory

- entries: **71**;
- classes: **32**;
- resources: **39**;
- provider data paths: **4**;
- attribute-named paths: **58**;
- bounded semantic-path hits: **1**.

The one semantic-path hit is `net/puffish/attributesmod/mixin/HungerManagerMixin.class`. It is a regex false positive caused by the substring `mana` inside `Manager`, not evidence of a mana subsystem.

Provider data is limited to attribute-tag infrastructure under `data/puffish_attributes/tags/attribute/` plus compatibility tagging.

## Exact attribute inventory

Exact localization/registry inspection closes **42 attribute IDs**. No separate skill/action registry is present.

The inventory includes `magic_damage`, `magic_resistance` and `magic_resistance_shred`; these are numeric attribute semantics, not casts or spell identities.

## Semantic disposition

The exact JAR contains no provider-owned spell, ritual, rite, glyph, summon, teleport or equivalent discrete supernatural player-action roster.

Attribute modification is a numerical/stat layer consumed by other systems. The concrete action remains owned by the equipment/skill/spell/effect provider that triggers or applies it.

Result: **`ZERO_SEMANTIC_ATTRIBUTE_FRAMEWORK / +0 strict`**.

## Clean-room boundary

The durable catalog retains hashes, counts, attribute identifiers and behavior-level classification. No third-party JAR bytes or implementation bodies are committed.
