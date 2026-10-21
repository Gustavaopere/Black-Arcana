# Apprentice's Codex 0.9.7.1 — exact-JAR bytecode evidence gate

**Opened:** 2026-10-14 · Black Arcana baseline `main@7309c2caa2a985d47a586f7973ca808287b52cea` · Minecraft 1.21.1 / NeoForge / Java 21. This is a **read-only provider audit**, not a new runtime, perk, adapter or Stage 06.05 promotion.

## Physical identity and source

- Installed item #38 in `Gustavaopere/neoforge-rpg-skilltree/main@3fbc5779fb13110698c8be01f527f7277bcc7790`: `apprentice_codex-0.9.7.1+mc1.21.1.jar`, `apprenticecodex`, expected SHA-1 `b514315add32b93b0049c8673075627d7ef812e0`.
- [CurseForge file 8768955](https://www.curseforge.com/minecraft/mc-mods/apprentices-codex/files/8768955): exact 1.21.1 NeoForge artifact, uploaded 2026-08-30. A CDN retrieval without SHA equality is **not** acceptable evidence.
- Source declared 0.9.7.1: `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`. Source identity/83 spell entries were catalogued in PRs #803–805; compiled method equality remains a separate claim.

## Executable narrow bytecode checks

Run `python3 docs/qa/apprentice_codex_binary_audit_test.py -v` for isolated synthetic Java 21 fixtures. **A test PASS proves the collector works on fixtures only.**

The GitHub workflow `.github/workflows/apprentice-codex-binary-audit.yml` fetches the exact CurseForge file number through a candidate CDN URL, first requires the recorded SHA-1, checks NeoForge mod metadata and exact class names, then performs read-only `javap -c -p`. It publishes a narrow JSON report, **not** a third-party JAR or its disassembly.

| Code-derived hypothesis | Class/method inspected | Required opcode/call pattern |
|---|---|---|
| Arcane Beam damage runs on nonzero remainder `tickCount % 5`, apparently 4/5 ticks (despite comment 1/5) | `ArcaneBeamEntity.tick` | `irem → ifeq → damageHitTarget` |
| Unite Luna's antimagia converts the missile to an amplified explosion instead of benign dispel | `UniteLunaMoonEntity.onAntiMagic` / `explodeByAntiMagic` | `explodeByAntiMagic` call, literal `3.0f`, `applyBurstDamage` |
| Palette Shift cancels the next spell's precast on successful affinity reception | `PaletteShiftReceptionEvent.onSpellPreCast` | `applyPastelAffinity` and `setCanceled` calls |
| Mana Mending compares an in-memory ItemStack reference | `ManaMending$ManaMendingCastData.matchesTarget` | `targetStack` and `if_acmpne` / `if_acmpeq` |

**Interpretation:** `PASS` supports only these bytecode shapes. `UNPROVEN_OR_MISMATCH` is an unresolved shape mismatch, not proof the provider is broken. A missing URL, mismatched hash, missing mod metadata or missing class returns fail-closed. The report records SHA-256, SHA-1, byte count, and named narrow predicates. Neither a workflow run nor synthetic fixtures certify full source/JAR equivalence.

## Remaining validation debt

⚠️ **PENDING:** physical modpack startup, mixin/classloader transforms, actual server configs, Arcane Beam DPS/tick cadence, Counterspell impacts/PvP and claims, Palette Shift cost/cancel order, Mana Mending swap/restart, network, reload, dedicated and Survival. A classfile check does not substitute for these tests.

⛔ **BLOCKED:** RPG Skill Tree Mastery/perk adapter without a homologated contract. Black Arcana owns its own runtime, not a second Iron's/Apprentice's cast, mana charge, damage, item repair or XP economy. Stage 06.05 stays unpromoted and Stage 09 retains D035 physical QA obligations.

## Local reproduction

With an independently acquired JAR matching the installed SHA:

~~~bash
python3 docs/qa/apprentice_codex_binary_audit.py \
  --jar '/path/to/apprentice_codex-0.9.7.1+mc1.21.1.jar' \
  --output build/apprentice-codex-binary-audit/evidence.json
~~~

Record real GitHub Actions run IDs, digest and all four narrow results **only after they have been observed**. Do not infer a result from workflow configuration alone.

## Evidência executada — exact-JAR run #38567741062 (2026-10-14)

- [GitHub Actions read-only audit](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38567741062) — **SUCCESS** no job `exact_jar_bytecode`; coleta do CurseForge file 8768955 e `sha1sum --check` aprovadas. Este é um run na branch/PR #806, não teste em modpack.
- JAR: `apprentice_codex-0.9.7.1+mc1.21.1.jar` · **9,945,619 bytes** · SHA-1 `b514315add32b93b0049c8673075627d7ef812e0` · SHA-256 `f0dfab67154f344c02c6fbe561f73456fa46ed9d018fae661dcdf4da95c67fe2`.
- `beam_remainder_nonzero_damage_path`: **PASS**; `moon_antimagic_triggers_boosted_burst`: **PASS**; `palette_precast_cancels_event`: **PASS**; `mending_itemstack_reference_identity`: **PASS**. São **quatro padrões em classfiles exatos**, não certificação da equivalência source/JAR completa.
- Artefato JSON restrito do workflow: `apprentice-codex-binary-report-cd4f091822bd61207749d08d65b1a3214ffb47d4` (artifact ID `11895504113`), sem JAR/código upstream. O source-level das outras 79 magias não é promovido automaticamente a bytecode-audited.
- ⚠️ Continua **PENDING** a validação provider-native em jogo, classloader/mixins, config, efeitos reais e Stage 09. ⛔ Não existe adapter de perks/Mastery homologado com RPG Skill Tree; Stage 06.05 não é promovido.
