# Apprentice's Codex 0.9.7.1 — classfile registry reconciliation

**Checkpoint:** 2026-10-14 · Minecraft 1.21.1 NeoForge · Java 21. **State: 🟡 audit gate prepared; exact physical result pending CI.**

## Authorities

- Black Arcana baseline `main@707a638e54c72eb80ef8b6a373edfd52860697ed`; 83 IDs in `wiki/modpack-catalog/providers/✅-apprentice-codex/README.md`, verified source-level against upstream `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`.
- Sibling modlist `Gustavaopere/neoforge-rpg-skilltree/main@9e6436edb0049a8dcc4e47165db0f6850e5efa68`: `apprentice_codex-0.9.7.1+mc1.21.1.jar` / mod ID `apprenticecodex`. Exact binary SHA-1 `b514315add32b93b0049c8673075627d7ef812e0`, SHA-256 `f0dfab67154f344c02c6fbe561f73456fa46ed9d018fae661dcdf4da95c67fe2`; official CurseForge file 8768955.
- Previous [four narrow classfile predicates](apprentice-codex-binary-audit-2026-10-14.md) **PASS** on exact SHA JAR; **not** a proof of 83 compiled registration sites.

## This new executable gate

Run `python3 docs/qa/apprentice_codex_registry_binary_audit_test.py -v` for synthetic Java 21 tests. The tests check that unrelated string constants do not count, IDs must be unique, unexpected/missing IDs and field remappings fail, and symlink/untrusted JARs are rejected.

The exact-hash CI audit invokes `docs/qa/apprentice_codex_registry_binary_audit.py` only **after** the existing artifact download/hash/NeoForge metadata gates. `javap -c -p` inspects the compiled `jp.aquafactory.apprenticecodex.registry.SpellRegistry` initializer without loading third-party game classes. Each accepted registration must have the concrete instruction sequence:

`ldc "id" → invokedynamic Supplier → invokestatic reg(String,Supplier) → putstatic FIELD`

It reconciles all 83 canonical IDs against 83 distinct compiled registration pairs, expected field name (`id.upper()`), and the corresponding public `DeferredHolder` fields. Any missing/extra/duplicate/remapped ID, unbound field or count mismatch yields `UNPROVEN_OR_MISMATCH` (fail-closed). The report is JSON only; the provider JAR or decompiled content is **not** published.

**Scope limitation:** An `83/83 PASS` (if actually observed in CI) supports only the static registration callsites in the **exact versioned JAR**. It does not certify that all 83 spells were loaded into a running Iron's/NeoForge registry, acquired in Survival, cast successfully, remained enabled in configs, or gained any RPG Skill Tree progression hook. Full method bytecode, world/claim behavior and client/dedicated QA remain separate.

## Preserve hard blockers

- ⚠️ Physical provider-real scenarios `AC-P01` through `AC-P05` in [Stage 09 runbook](apprentice-codex-provider-real-runbook.md) remain **PENDING**.
- ⛔ RPG Skill Tree perks/Mastery adapter without real homologated contract remains blocked. Black Arcana does not take control of external Iron's mana, cast pipeline, or Apprentice's spell effects.
- 🟡 Stage 06.05 remains without promotion; Stage 09 D035 acceptance cannot be inferred from `javap` or a green CI workflow.

**Recording rule:** Add the actual CI run, HEAD SHA, verified counts and evidence artifact only after observing them; do not prematurely mark binary registry PASS.
