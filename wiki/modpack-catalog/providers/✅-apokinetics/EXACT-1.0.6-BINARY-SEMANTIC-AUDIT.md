# Create: Apokinetics 1.0.6 — exact binary semantic audit

Status: `EXACT HASH-MATCHED PHYSICAL/PUBLISHER ARTIFACT / CLEAN-ROOM FACTUAL INVENTORY / ZERO SPELL-GLYPH-RITUAL SURFACE OBSERVED`

## Provenance

Physical pack fingerprint:

- `apokinetics-1.0.6.jar`;
- SHA-1 `8af4fc7fb17f4d60ead9d0c098d0650d6fdefa68`.

Publisher artifact:

- CurseForge project `1606442`;
- file `8790422`;
- Curse Maven coordinate `curse.maven:apokinetics-1606442:8790422`.

NON-MERGE audit checkpoint:

- Black Arcana commit `7871abf34e6443d7944afd5315dd5f196825125f`;
- CI run `36079263855`;
- exact binary semantic audit step: SUCCESS.

The temporary workflow/script are audit-only and are not merged into the durable catalog.

## Cryptographic equality

Observed exact publisher artifact:

- bytes: `1,323,324`;
- SHA-1: `8af4fc7fb17f4d60ead9d0c098d0650d6fdefa68`;
- SHA-256: `ca4f24cec8f5c9b5126989967498bb4857225a062f183e54000f17a4ca2a74fb`.

Physical SHA-1 = publisher-artifact SHA-1:

**true**

## Structural inventory

Exact artifact:

- total classes: **273**;
- provider classes: **273**;
- provider resources: **120**;
- embedded jar-in-jar libraries: **0**.

Observed dependency mod IDs from NeoForge metadata:

- `apokinetics`;
- `apotheosis`;
- `create`;
- `curios`;
- `jade`;
- `jei`;
- `minecraft`;
- `neoforge`.

No Iron's, Ars Nouveau, Malum, Eidolon or Goety dependency/reference surface was observed by the bounded audit.

## Semantic probes

The audit searched exact provider class/resource paths and provider classfile byte strings for spell/glyph/ritual/rite contracts and known external magic APIs.

Results:

| Probe | Hits |
|---|---:|
| semantic class paths | 0 |
| semantic resource paths | 0 |
| semantic classfile tokens | 0 |
| known magic API references | 0 |

The script was fail-fast: any positive result in those four families would have failed the audit and required manual review.

## Resource shape

Observed provider resource buckets include:

- `data/apokinetics/gems`: 13 resources;
- recipes: 30;
- loot tables: 4;
- tags: 6;
- assets for models, textures, lang and blockstates.

This resource shape is consistent with the publisher-documented machine/gem/tool system rather than an unlisted spell/glyph/ritual data surface.

## Clean-room boundary

Retained evidence is limited to cryptographic digests, archive paths/counts, metadata dependency IDs, class/resource names and bounded classfile token/reference presence needed for interoperability/catalog classification.

No implementation body, assets, models, textures, sounds or proprietary source reconstruction are copied into Black Arcana.

## Conclusion

For the exact physical 1.0.6 artifact:

- no provider spell registry/resource/API surface was observed;
- no provider glyph/spell-part registry/resource/API surface was observed;
- no provider ritual/rite registry/resource/API surface was observed;
- the documented Machine Gem/table/pylon/socket/tool surface remains support/augmentation content.

Catalog semantic delta: **+0**.

This closes the previous catalog-only blocker `SPELL-REGISTRY ABSENCE UNVERIFIED`. Runtime/config/economy/compatibility QA remains fail-closed.
