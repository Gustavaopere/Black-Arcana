# 07 — Spell Domains

Implement the approved Stage 01 catalog using the frozen core, integration, safety, UX and ritual contracts.

## Rule for every spell
Specification must state: fantasy, host integration, invocation, target rules, resource cost, cooldown, scaling equation, progression gate, world-effect mode, boss/PvP behavior, config surface, tests and provenance link.

## Domains
- Blood & Curses
- Souls & Death
- Projection & Arsenal
- Space & Displacement
- Black Flame
- Forbidden Domains
- Familiars & Divination

## Implementation state

Stage 07 is being promoted as sequential domain-scoped work to keep review and validation surfaces bounded.

- **07.01 Blood & Curses** — canonical on `main` via PR #45; automated branch and post-merge validation are GREEN. Final real-modpack/manual acceptance remains deferred under D031.
- **07.02 Souls & Death** — canonical on `main` via PR #47 at merge `998186beed3522a0821a7dbb911f5e31cd6a9e1d`; exact-SHA post-merge workflow `33981437469` passed JUnit, diff sanity, NeoForge build, JAR inspection, all 40 required GameTests, dedicated-server smoke and canonical QA artifact publication. Provider-native Malum death-to-spirit harvesting and player-specific Eidolon unlock remain explicitly fail-closed where verified hooks lack the required causal/value or caster-identity contracts. Final real-modpack/manual host acceptance remains deferred under D031.
- **07.03 Projection & Arsenal** — canonical on `main` via PR #50 at merge `8631c614e7e319a46ab6b29fe7ab33b3903fc2ef`. Final PR-head workflow `33991180861` (#992) passed JUnit, diff sanity, NeoForge build, JAR inspection, all 58 required GameTests and dedicated-server smoke. Exact-SHA post-merge workflow `33991393657` (#993) passed the same complete pipeline and published canonical QA artifact `black-arcana-8631c614e7e319a46ab6b29fe7ab33b3903fc2ef`. The implementation remains isolated from 07.04: Rift Blades uses canonical Stage 04 world-safety primitives without importing `content/space`. Real-modpack/provider host acceptance remains deferred and is not inferred as PASS.
- **07.04 Space & Displacement** — canonical on `main` via PR #52 at merge `a567419f1cccd3a33db95402fcb267c0ad79bc67`. Final PR-head workflow `33997420003` passed JUnit, diff sanity, NeoForge build, JAR inspection, all required GameTests and dedicated-server smoke on `f74bf5b15e3178392a2ea52d3f00969ac6288ea2`. Exact-SHA post-merge workflow `33997767668` passed the complete pipeline, including all 77 required GameTests, dedicated-server smoke and canonical QA artifact publication. Canonical artifact: `black-arcana-a567419f1cccd3a33db95402fcb267c0ad79bc67`, artifact ID `9978600971`, SHA-256 `c4343f5764d76d6b5310dc446ff1bfbb9359b17ccf74898e615743010259dc1e`. Real-modpack/provider/manual host acceptance remains deferred under D031 and is not inferred as PASS.
- **07.05 Black Flame** — canonical on `main` via PR #54 at runtime merge `f57f2547977e48ac2bbd3bb912371913784ea1ba`. Final exact PR head `bf23cfc805dc6fe01ec7bed009f15e2f6e217ec9` passed workflow `34006367929` (#1142); exact-SHA post-merge workflow `34006704333` (#1143) passed JUnit, diff sanity, NeoForge build, JAR inspection, the complete required GameTest suite, dedicated-server smoke and main-only canonical QA artifact publication. Canonical artifact: `black-arcana-f57f2547977e48ac2bbd3bb912371913784ea1ba`, artifact ID `9981201760`, SHA-256 `7c462656d5d99b59cd9d49a4ecdd4e44272ee2a294fc192a53ecfd0b63cf5a47`. Both P1 review threads were resolved before merge. Real-modpack/provider/manual host acceptance remains deferred under D031 and is not inferred as PASS.
- **07.06 Forbidden Domains** — canonical on `main` via PR #59 at runtime merge `836623d39d3060de1b8830000c43d493305cd740`. Final exact PR head `b560a1a0e4d2679d101008526d87de6a8a3b4325` passed push workflow `34036461398` (#1187) and PR workflow `34036463695` (#1188). Exact-SHA post-merge workflow `34036992474` (#1189) passed JUnit, diff sanity, NeoForge build, built-JAR verification, all **95 required GameTests**, dedicated-server smoke and canonical artifact publication. Canonical artifact: `black-arcana-836623d39d3060de1b8830000c43d493305cd740`, artifact ID `9990520844`, SHA-256 `e77666b5768a51193597c65f1f0be4547c5e5723fa51a1a36d41c5354e8b1ebe`. D032 freezes the implementation to bounded localized in-world fields in already-loaded dimensions: no temporary dimensions, force-loading, inventory cloning or arbitrary terrain mutation. Start/capture admission reuses canonical Stage 04 protection/world-effect authority and Stage 07.04 safe-destination recovery; unknown state fails closed. Concrete Arsenal/Soul/Blood provider-native Forbidden Domain effects remain unspecified/fail-closed rather than being invented. Real-modpack/provider/manual host acceptance remains deferred under D031 and is not inferred as PASS.
- **07.07 Familiars & Divination** — pending. It must not start automatically from the 07.06 promotion.

Historical stacked Stage 07 branches/PR #22 are reviewed source material only and are not canonical integration ancestry. Each later domain must start from the latest canonical `main` after its predecessor is promoted.

The stage may be split into sequential domain branches if the review surface becomes too large; 07.01 established that pattern and 07.02–07.06 preserve the same isolation discipline.
