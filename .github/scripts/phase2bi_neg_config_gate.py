from pathlib import Path

ROOT = Path('.')
semantic = ROOT / 'wiki/modpack-catalog/meta/SEMANTIC-MAGIC-COVERAGE.md'
provider = ROOT / 'wiki/modpack-catalog/providers/not-enough-glyphs/README.md'
matrix = ROOT / 'wiki/modpack-catalog/providers/not-enough-glyphs/REGISTRATION-MATRIX.md'
checkpoint = ROOT / 'wiki/modpack-catalog/meta/PHASE2BI-NOT-ENOUGH-GLYPHS-CONFIG-GATE.md'


def replace_once(path: Path, old: str, new: str):
    text = path.read_text()
    if old not in text:
        raise SystemExit(f'missing expected text in {path}: {old!r}')
    if text.count(old) != 1:
        raise SystemExit(f'expected exactly one occurrence in {path}: {old!r}')
    path.write_text(text.replace(old, new, 1))

replace_once(
    semantic,
    '| Not Enough Glyphs | 39 | `CONDITIONAL` | current-pack source produces 40 `registerSpell` calls; `momentum` is source-disabled, leaving 39 source-enabled before user/provider config; exact active pack config remains to be reconciled |',
    '| Not Enough Glyphs | 39 | `CONDITIONAL / CONFIG AUTHORITY CLOSED / +0` | current-pack source produces 40 `registerSpell` calls; `momentum` is source-disabled, leaving 39 candidates. Ars Nouveau 5.13.1 registers each spell part as a `SERVER` config at `not_enough_glyphs/<glyph>.toml`; inherited `[general].enabled` defaults true, but the deployed server/world override set is unavailable, so source defaults are not promoted to active-pack facts |'
)
replace_once(
    semantic,
    '1. current-pack config closure for Not Enough Glyphs 4.6.1 and other remaining conditional glyph/action rows;',
    '1. obtain the deployed Not Enough Glyphs/Ars `SERVER` config set (`not_enough_glyphs/<glyph>.toml`, including any world `serverconfig` overrides) and reconcile `[general].enabled` for the 39 candidates; source/default-only evidence is insufficient;'
)

provider_marker = '## Phase 2BI — exact config authority (semantic delta +0)'
if provider_marker not in provider.read_text():
    provider.write_text(provider.read_text().rstrip() + '''\n\n## Phase 2BI — exact config authority (semantic delta +0)\n\nThe remaining 39-glyph semantic blocker is now narrowed to the deployed Ars/NeoForge server-config values rather than an unknown Not Enough Glyphs-specific switch. Exact Ars Nouveau 5.13.1 source at `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` shows that `GlyphRegistry.registerSpell(...)` builds each `AbstractSpellPart` config and registers it as `ModConfig.Type.SERVER` using `<namespace>/<path>.toml`. For NEG-owned IDs the concrete filename family is therefore `not_enough_glyphs/<glyph>.toml`.\n\n`AbstractSpellPart.buildConfig(...)` defines `[general].enabled` with source default `true`, and `isEnabled()` reads that config value. `momentum` remains a separate provider override that returns disabled in NEG source. NeoForge 1.21.1 SERVER configs are server-authoritative/synchronized and may be overridden per world under `world/serverconfig`; consequently the source default is not accepted as the deployed pack state.\n\nNo authoritative deployed NEG glyph-config TOMLs are present in the current project attachments/repository evidence. Phase 2BI therefore changes **neither** metric: strict semantic minimum remains **1249**, and provider-component closure remains **57/100**. A future promotion may count only those of the 39 candidates whose effective deployed `[general].enabled` state is proven true. Runtime/balance/protection QA remains separate.\n''')

matrix_marker = '## Phase 2BI config gate'
if matrix_marker not in matrix.read_text():
    matrix.write_text(matrix.read_text().rstrip() + '''\n\n## Phase 2BI config gate\n\nThe matrix's 39 `source-enabled` rows are **not yet active-pack counted rows**. Exact Ars Nouveau 5.13.1 source proves the controlling config contract:\n\n- `GlyphRegistry.registerSpell(part)` calls `part.buildConfig(...)`;\n- the resulting spec is registered as `ModConfig.Type.SERVER`;\n- the explicit filename is `<namespace>/<path>.toml`, yielding `not_enough_glyphs/<glyph>.toml` for NEG IDs;\n- base `AbstractSpellPart` defines `[general].enabled = true` as a source default and `isEnabled()` reads that value;\n- NEG `momentum` remains explicitly disabled by its own override.\n\nBecause NeoForge SERVER configs can be overridden per world and the deployed server/world config set is not available in authoritative project material, the 39 rows stay `CONDITIONAL`. Source defaults are not substituted for deployed state. Semantic delta: **+0**; strict total: **1249**.\n''')

if checkpoint.exists():
    raise SystemExit(f'{checkpoint} already exists')
checkpoint.write_text('''# Phase 2BI — Not Enough Glyphs 4.6.1 config-authority checkpoint\n\nStatus: `CONFIG AUTHORITY CLOSED / DEPLOYED VALUES MISSING / SEMANTIC DELTA +0`\n\nBase audited: `main@75558c92150506cce9f9b98b8f1ae29e4c128e62`.\n\n## Physical/provider anchor\n\n- installed JAR: `not_enough_glyphs-1.21.1-4.6.1.jar`;\n- mod id/version: `not_enough_glyphs` / `4.6.1`;\n- physical SHA-1: `e5fd04b7c40d6d5a9aea5d6356f3eb628941fca4`;\n- embedded Sauce: `0.0.42.89`;\n- Minecraft 1.21.1 / NeoForge `21.1.248`;\n- physical modlist: 595 top-level entries, SHA-1 `7aaece7acbfb07ba4d0c66029042f36c50d046f0`.\n\nPhase 2AF already closed the current-pack registration matrix: 40 NEG registrations, with `momentum` source-disabled and 39 remaining source-enabled candidates before external/user configuration. The stale Phase 2AD/2AF branches are ancestors of current `main` and contain no unmerged work.\n\n## Exact config authority\n\nExact Ars Nouveau 5.13.1 source checkpoint `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` supplies the host contract used by NEG glyphs:\n\n1. `GlyphRegistry.registerSpell(AbstractSpellPart)` invokes `part.buildConfig(...)`.\n2. It registers that per-glyph spec as `ModConfig.Type.SERVER`.\n3. It supplies filename `<namespace>/<path>.toml`; NEG glyphs therefore use `not_enough_glyphs/<glyph>.toml`.\n4. Base `AbstractSpellPart.buildConfig(...)` defines `general.enabled` with source default `true`.\n5. Base `isEnabled()` returns the resolved `ENABLED` config value.\n6. NEG `momentum` independently overrides `isEnabled()` to false and remains excluded.\n\nNeoForge 1.21.1 documents `SERVER` configs as server-authoritative/synchronized and allows per-world overrides in `<server_folder>/world/serverconfig`. Therefore the effective semantic gate is the deployed config set, including any world override; a code default cannot substitute for it.\n\n## Evidence availability\n\nThe current uploaded/project material contains the physical modlist and provider/source documentation but no authoritative deployed `not_enough_glyphs/*.toml` server/world config set. Repository search likewise does not expose those deployed files.\n\nConsequently Phase 2BI **does not promote the 39 candidates**. Canonical values remain:\n\n- strict reconstructible semantic minimum: **1249**;\n- provider-component coverage: **57/100**;\n- Not Enough Glyphs conditional semantic candidates: **39**.\n\n## Required evidence for promotion\n\nObtain the effective server configuration for all 39 candidate NEG IDs, including any per-world override. Reconcile `general.enabled` per glyph. Only proven-enabled rows may enter the strict semantic ledger; disabled rows remain excluded. If no valid explicit config exists for a row, the runtime fallback/default must be demonstrated from the actual deployed environment rather than inferred solely from source.\n\nThis checkpoint changes no Black Arcana runtime authority, Ars/NEG ownership, mana/casting settlement, or provider-component count.\n''')

# Validation
sem = semantic.read_text()
assert 'CONDITIONAL / CONFIG AUTHORITY CLOSED / +0' in sem
assert '**1249**' in sem
assert '**57/100**' in provider.read_text()
assert checkpoint.exists()
print('Phase 2BI config-authority documentation reconciled; semantic/component totals unchanged.')
