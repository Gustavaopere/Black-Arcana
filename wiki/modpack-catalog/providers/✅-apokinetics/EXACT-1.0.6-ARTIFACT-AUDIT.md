# Create: Apokinetics 1.0.6 — Exact Artifact Audit

Status: `COUNTED_EXACT_ZERO / ZERO_SEMANTIC_MACHINE_AUGMENT / CLEAN-ROOM FACTUAL BINARY AUDIT`

## Identity

Physical authority: `neoforge-rpg-skilltree@e3689bbc04ba54be1612a13c242496330e99df06`

- JAR: `apokinetics-1.0.6.jar`;
- mod id: `apokinetics`;
- runtime: `1.0.6`;
- physical SHA-1: `8af4fc7fb17f4d60ead9d0c098d0650d6fdefa68`.

Publisher artifact:

- CurseForge project: `1606442`;
- File ID: `8790422`;
- Curse Maven: `curse.maven:apokinetics-1606442:8790422`;
- exact downloaded size: **1,323,324 bytes**;
- SHA-1: `8af4fc7fb17f4d60ead9d0c098d0650d6fdefa68`;
- SHA-256: `ca4f24cec8f5c9b5126989967498bb4857225a062f183e54000f17a4ca2a74fb`.

Result: **installed physical SHA-1 exactly matches the audited publisher file**.

## NON-MERGE audit evidence

Temporary audit checkpoint:

- branch: `feat/audit-apokinetics-1.0.6-non-merge-2026-09-24`;
- commit: `7871abf34e6443d7944afd5315dd5f196825125f`;
- workflow run: `36079263855`;
- step: `Temporary Apokinetics 1.0.6 exact binary semantic audit NON-MERGE`: **SUCCESS**;
- `verify`: **SUCCESS**;
- `stage05_qa_companion_smoke`: **SUCCESS**.

Temporary workflow/script changes are audit scaffolding only and are not part of the durable catalog delivery.

## Archive facts

Exact top-level artifact:

- class entries: **273**;
- provider-namespace class entries: **273**;
- provider resource entries: **120**;
- embedded JarJar JARs: **0**.

Provider class namespace observed:

`com/fishguy129/apokinetics/`

Metadata mod IDs observed:

`apokinetics, apotheosis, create, curios, jade, jei, minecraft, neoforge`.

Selected resource buckets:

| Bucket | Count |
|---|---:|
| `data/apokinetics/gems` | 13 |
| `data/apokinetics/loot_table` | 4 |
| `data/apokinetics/recipe` | 30 |
| `data/apokinetics/tags` | 6 |
| `assets/apokinetics/blockstates` | 3 |
| `assets/apokinetics/lang` | 2 |
| `assets/apokinetics/models` | 23 |
| `assets/apokinetics/textures` | 37 |

The 13 `gems` resource paths are an archive count, not a semantic-action count. The publisher-facing gameplay capability ledger remains 12 Machine Gem types.

## Semantic negative evidence

The exact artifact scan returned:

| Check | Result |
|---|---:|
| provider class paths matching spell/glyph/ritual/rite | 0 |
| provider resource paths matching spell/glyph/ritual/rite | 0 |
| provider classfile semantic UTF-8 token hits | 0 |
| known external magic API reference hits | 0 |

Classfile tokens searched included bounded spell/glyph/ritual signatures such as `AbstractSpell`, `SpellRegistry`, `registerSpell`, `SpellData`, `SchoolRegistry`, `SpellPart`, `GlyphRegistry`, ritual recipe and rite holder signatures.

Known external magic reference checks covered the provider-facing namespaces/signatures relevant to Iron's Spells, Ars Nouveau, Malum, Eidolon and Goety-style spell/rite surfaces.

This is evidence for absence of a provider-owned spell/glyph/ritual surface in the exact installed artifact. It is not a claim that Apokinetics lacks machine effects, modifiers or augmentation logic.

## Semantic conclusion

The exact artifact is classified:

`ZERO_SEMANTIC_MACHINE_AUGMENT`

The 12 documented Machine Gems and related sockets/Rotation/Pylon/tools are magic-relevant support/augmentation capabilities, not independent spell/glyph/ritual action identities under the Black Arcana metric.

Strict semantic delta:

**+0**

## Clean-room / provenance

The artifact is All Rights Reserved.

The temporary audit retained only:

- cryptographic hashes;
- file size;
- archive paths/counts;
- metadata mod IDs;
- bounded classfile reference-string facts.

The JAR was stored only in temporary CI storage and discarded. No decompilation, implementation reconstruction, code reuse or asset extraction is part of this durable evidence.
