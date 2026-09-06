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
- **07.05 Black Flame** — implemented in PR #54 from canonical `main@0e508b646b602beefd136bf9602945e247b2a524`; current technical implementation is bounded/protected and the last clean implementation-head workflow `34004647369` (#1118) passed JUnit, diff sanity, NeoForge build, JAR inspection, all **92/92 required GameTests** and dedicated-server smoke on `6e021ef28ebb450a84a7dff7fa8a545f52a90389`. The plan remains without `✅` until PR #54 is merged and exact-SHA post-merge `main` validation succeeds. Real-modpack/provider/manual host acceptance remains deferred under D031.
- **07.06–07.07** — pending. 07.06 must not start automatically from PR #54.

Historical stacked Stage 07 branches/PR #22 are reviewed source material only and are not canonical integration ancestry. Each later domain must start from the latest canonical `main` after its predecessor is promoted.

The stage may be split into sequential domain branches if the review surface becomes too large; 07.01 established that pattern and 07.02–07.05 preserve the same isolation discipline.
