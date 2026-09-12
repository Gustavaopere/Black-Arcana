from pathlib import Path

ROOT = Path('.')


def replace_exact(path: str, old: str, new: str, expected: int = 1) -> None:
    p = ROOT / path
    text = p.read_text()
    count = text.count(old)
    if count != expected:
        raise SystemExit(f'{path}: expected {expected} occurrence(s), found {count}: {old[:120]!r}')
    p.write_text(text.replace(old, new))


# Phase checkpoint: candidate -> canonical final evidence.
checkpoint = 'wiki/modpack-catalog/meta/PHASE2BH-GOETY-3.1.4-EXACT-CHECKPOINT.md'
(ROOT / checkpoint).write_text('''# Phase 2BH — Goety 3.1.4 exact checkpoint

Status: `CANONICAL — DURABLE PR + EXACT POST-MERGE CI GREEN`

Base audited: `main@7d14874e7d477c8ae2b3c8643c1519feea5a90cc`.

Exact physical identity: `goety-3.1.4.jar`, `goety` / `3.1.4`, SHA-1 `a0770e180e4e8b1b87d8fa9c8356e9dbf34d82a7`, CurseForge `586095 / 8689429`, modlist 595 / `7aaece7acbfb07ba4d0c66029042f36c50d046f0`.

Exact catalog evidence came from isolated non-merge PR #197: `34670150370/10290083272`, `34670458172/10290222369`, `34670556329/10290527131`, `34670758163/10289884505`. Discarded harness-failure runs `34670348040` and `34670400350` are not evidence.

Durable PR #198 clean HEAD `d75f82a23b5c977ccc8ec84813bf89c928ffc0ab` passed Black Arcana CI **#2523** / run `34672038273`. It was squash-merged as `4fcc40aaf8149b5511dbd882a5616ee5240cd640`; that exact merge SHA passed Black Arcana CI **#2524** / run `34672222798`, including unit tests, diff sanity, NeoForge build, built-JAR verification, Foundation GameTest, dedicated-server smoke and canonical QA-JAR publication.

Canonical QA artifact: `black-arcana-4fcc40aaf8149b5511dbd882a5616ee5240cd640`, artifact ID `10291461067`, SHA-256 `4f2ccf8be11cdba348c7cd0bdc64e595f6b101257b2b99f80fbe5542fae41ada`.

Canonical disposition: 123 active Focus actions + 238 available distinct non-Focus ritual actions = **+361**; strict semantic minimum **888 → 1249**; provider-component coverage **56/100 → 57/100**, component #57.

Numerical balance, Soul Energy settlement APIs, research, servants/Summon Down, Lichdom, ritual completion hooks, full-modpack runtime QA and Black Arcana adapter seams remain separate fail-closed gates. No runtime/Stage authority changes are part of Phase 2BH.
''')

# Provider exact-artifact audit.
replace_exact(
    'wiki/modpack-catalog/providers/goety/EXACT-3.1.4-ARTIFACT-AUDIT.md',
    'Status: `PHASE 2BH CANDIDATE / EXACT HASH-MATCHED ARTIFACT / CATALOG IDENTITY CLOSED / RUNTIME API QA SEPARATE`',
    'Status: `PHASE 2BH CANONICAL / EXACT HASH-MATCHED ARTIFACT / CATALOG IDENTITY CLOSED / RUNTIME API QA SEPARATE`',
)
replace_exact(
    'wiki/modpack-catalog/providers/goety/EXACT-3.1.4-ARTIFACT-AUDIT.md',
    '- Phase 2BH candidate Goety subtotal: **361**.\n- canonical baseline entering this durable PR: **888 / 56 of 100**; candidate: **1249 / 57 of 100**, component #57.',
    '- Phase 2BH canonical Goety subtotal: **361**.\n- canonical strict minimum after Phase 2BH: **1249 / 57 of 100**, component #57.\n- durable PR #198 HEAD `d75f82a23b5c977ccc8ec84813bf89c928ffc0ab` passed CI #2523; squash merge `4fcc40aaf8149b5511dbd882a5616ee5240cd640` passed exact-SHA post-merge CI #2524 and published canonical QA artifact `10291461067` (`sha256:4f2ccf8be11cdba348c7cd0bdc64e595f6b101257b2b99f80fbe5542fae41ada`).',
)

# Provider README.
replace_exact(
    'wiki/modpack-catalog/providers/goety/README.md',
    '`PHASE 2BH CANDIDATE / EXACT 3.1.4 ARTIFACT IDENTITY + SEMANTIC INVENTORY CLOSED / RUNTIME API QA PENDING`',
    '`PHASE 2BH CANONICAL / EXACT 3.1.4 ARTIFACT IDENTITY + SEMANTIC INVENTORY CLOSED / RUNTIME API QA PENDING`',
)
replace_exact(
    'wiki/modpack-catalog/providers/goety/README.md',
    '## Phase 2BH exact-artifact closure candidate\n\nExact PR #197 evidence supersedes source-only uncertainty for catalog identity: **123 active Focus actions + 238 available distinct non-Focus ritual actions = 361**. Candidate totals are **1249 semantic objects / 57 of 100 components** from canonical baseline 888 / 56. These values remain candidate until durable merge + exact post-merge CI. See `EXACT-3.1.4-ARTIFACT-AUDIT.md` and `EXACT-3.1.4-SEMANTIC-INVENTORY.md`. Runtime/API/balance and provider-owned Soul Energy/research/servant/Lichdom settlement remain fail-closed.',
    '## Phase 2BH exact-artifact closure — canonical\n\nExact PR #197 evidence supersedes source-only uncertainty for catalog identity: **123 active Focus actions + 238 available distinct non-Focus ritual actions = 361**. Durable PR #198 HEAD `d75f82a23b5c977ccc8ec84813bf89c928ffc0ab` passed CI #2523; squash merge `4fcc40aaf8149b5511dbd882a5616ee5240cd640` passed exact-SHA post-merge CI #2524 and published canonical QA artifact `10291461067` with SHA-256 `4f2ccf8be11cdba348c7cd0bdc64e595f6b101257b2b99f80fbe5542fae41ada`. Canonical totals are now **1249 semantic objects / 57 of 100 components**. See `EXACT-3.1.4-ARTIFACT-AUDIT.md` and `EXACT-3.1.4-SEMANTIC-INVENTORY.md`. Runtime/API/balance and provider-owned Soul Energy/research/servant/Lichdom settlement remain fail-closed.',
)
replace_exact(
    'wiki/modpack-catalog/providers/goety/README.md',
    'Canonical baseline entering Phase 2BH is **888 / 56 of 100**. The exact 3.1.4 artifact proposes Goety as `COUNTED_EXACT` with **361**, producing candidate **1249 / 57 of 100**. Canonical promotion still requires durable merge and exact post-merge CI. Runtime integration remains fail-closed until provider boundaries are separately proven.',
    'Phase 2BH canonically counts Goety as `COUNTED_EXACT` with **361** semantic objects, yielding strict minimum **1249 / 57 of 100** after durable PR #198 and exact post-merge CI #2524. Runtime integration remains fail-closed until provider boundaries are separately proven.',
)

# Provider technical audit.
replace_exact(
    'wiki/modpack-catalog/providers/goety/TECHNICAL-AUDIT.md',
    'Status: `PHASE 2BH CANDIDATE / EXACT 3.1.4 ARTIFACT REGISTRY + SEMANTIC INVENTORY CLOSED / RUNTIME/API QA PENDING`',
    'Status: `PHASE 2BH CANONICAL / EXACT 3.1.4 ARTIFACT REGISTRY + SEMANTIC INVENTORY CLOSED / RUNTIME/API QA PENDING`',
)
replace_exact(
    'wiki/modpack-catalog/providers/goety/TECHNICAL-AUDIT.md',
    '## Phase 2BH exact-artifact closure candidate\n\nExact hash-matched artifact evidence closes **123 active Focus actions + 238 available distinct non-Focus rituals = 361** for catalog identity. This does not claim source-to-binary equivalence and does not authorize inference of numerical mechanics, Soul Energy settlement, servant/research/Lichdom hooks or stable APIs.',
    '## Phase 2BH exact-artifact closure — canonical\n\nExact hash-matched artifact evidence closes **123 active Focus actions + 238 available distinct non-Focus rituals = 361** for catalog identity. Durable PR #198 HEAD `d75f82a23b5c977ccc8ec84813bf89c928ffc0ab` passed CI #2523; squash merge `4fcc40aaf8149b5511dbd882a5616ee5240cd640` passed exact-SHA post-merge CI #2524 and published canonical QA artifact `10291461067` (`sha256:4f2ccf8be11cdba348c7cd0bdc64e595f6b101257b2b99f80fbe5542fae41ada`). This does not claim source-to-binary equivalence and does not authorize inference of numerical mechanics, Soul Energy settlement, servant/research/Lichdom hooks or stable APIs.',
)
replace_exact(
    'wiki/modpack-catalog/providers/goety/TECHNICAL-AUDIT.md',
    'Phase 2BH proposes Goety as `COUNTED_EXACT` for **361** semantic objects. Canonical baseline is **888**; candidate strict minimum is **1249** pending durable merge + exact post-merge CI.',
    'Phase 2BH canonically counts Goety as `COUNTED_EXACT` for **361** semantic objects. The strict semantic minimum is now **1249** after durable merge + exact post-merge CI.',
)
replace_exact(
    'wiki/modpack-catalog/providers/goety/TECHNICAL-AUDIT.md',
    '| exact 3.1.4 semantic Focus inventory | CANDIDATE `COUNTED_EXACT`: 123 active/acquirable Focus actions |',
    '| exact 3.1.4 semantic Focus inventory | `COUNTED_EXACT`: 123 active/acquirable Focus actions |',
)
replace_exact(
    'wiki/modpack-catalog/providers/goety/TECHNICAL-AUDIT.md',
    '| exact 3.1.4 ritual identity inventory | EXACT ARTIFACT: 342 resources; candidate 238 available distinct non-Focus semantic rituals |',
    '| exact 3.1.4 ritual identity inventory | `COUNTED_EXACT`: 342 resources audited; 238 available distinct non-Focus semantic rituals after deduplication/condition filtering |',
)
replace_exact(
    'wiki/modpack-catalog/providers/goety/TECHNICAL-AUDIT.md',
    '`OPEN CURRENT REGISTRY / EXACT 3.1.4 JAR-SOURCE RECONCILIATION PENDING`.',
    '`COUNTED_EXACT CATALOG IDENTITY / RUNTIME API QA PENDING`.',
)

# Semantic ledger.
replace_exact(
    'wiki/modpack-catalog/meta/SEMANTIC-MAGIC-COVERAGE.md',
    '## Phase 2BH candidate — Goety 3.1.4\n\nCanonical baseline entering this PR remains **888 semantic magic objects / 56 of 100 provider components**. Exact hash-matched 3.1.4 evidence closes **123 active Focus actions + 238 available distinct non-Focus ritual actions = +361**. Phase 2BH proposes candidate strict minimum **1249** and candidate component **#57 / 57 of 100**. These values do not become canonical until durable merge + exact post-merge CI. Runtime/API/balance QA remains separate.',
    '## Phase 2BH canonical — Goety 3.1.4\n\nExact hash-matched 3.1.4 evidence closes **123 active Focus actions + 238 available distinct non-Focus ritual actions = +361**. Durable PR #198 clean HEAD `d75f82a23b5c977ccc8ec84813bf89c928ffc0ab` passed Black Arcana CI **#2523** / run `34672038273`; squash merge `4fcc40aaf8149b5511dbd882a5616ee5240cd640` passed exact-SHA post-merge CI **#2524** / run `34672222798`, including canonical QA-JAR publication. Goety is therefore `COUNTED_EXACT` with **361**, the strict minimum is **1249**, and component **#57 / 57 of 100** is canonical. Runtime/API/balance QA remains separate.',
)
replace_exact(
    'wiki/modpack-catalog/meta/SEMANTIC-MAGIC-COVERAGE.md',
    '**888 semantic magic objects are currently reconstructible from canonical provider records after Phase 2BG.**',
    '**1249 semantic magic objects are currently reconstructible from canonical provider records after Phase 2BH.**',
)
replace_exact(
    'wiki/modpack-catalog/meta/SEMANTIC-MAGIC-COVERAGE.md',
    '- Malum Spirit Rite layer: **26**;\n- total: `199 + 541 + 42 + 55 + 25 + 26 = 888`.',
    '- Malum Spirit Rite layer: **26**;\n- Goety Focus + ritual layer: **361**;\n- total: `199 + 541 + 42 + 55 + 25 + 26 + 361 = 1249`.',
)
replace_exact(
    'wiki/modpack-catalog/meta/SEMANTIC-MAGIC-COVERAGE.md',
    '| [Leyline Spellbooks](../providers/leyline-spellbooks/README.md) | 1.0.3 | 14 | `COUNTED_EXACT` | exact hash-matched JAR closes 14 unconditional `AbstractSpell` registrations; no provider-specific spell lock/conditional registration gate is present; generic Iron\'s host config remains separate runtime QA |\n| [Eidolon: Repraised](../providers/eidolon-repraised/README.md)',
    '| [Leyline Spellbooks](../providers/leyline-spellbooks/README.md) | 1.0.3 | 14 | `COUNTED_EXACT` | exact hash-matched JAR closes 14 unconditional `AbstractSpell` registrations; no provider-specific spell lock/conditional registration gate is present; generic Iron\'s host config remains separate runtime QA |\n| [Goety](../providers/goety/README.md) | 3.1.4 | 361 | `COUNTED_EXACT` | exact hash-matched JAR closes 123 active/acquirable Focus actions + 238 available distinct non-Focus ritual actions after semantic deduplication and physical-provider condition filtering; runtime/API/balance QA remains separate |\n| [Eidolon: Repraised](../providers/eidolon-repraised/README.md)',
)
replace_exact(
    'wiki/modpack-catalog/meta/SEMANTIC-MAGIC-COVERAGE.md',
    '| **Strict total** |  | **888** |  |  |',
    '| **Strict total** |  | **1249** |  |  |',
)
replace_exact(
    'wiki/modpack-catalog/meta/SEMANTIC-MAGIC-COVERAGE.md',
    'Bloodlines remains **28 counted actions**; after later provider closures, the global strict total is **888**.',
    'Bloodlines remains **28 counted actions**; after later provider closures, the global strict total is **1249**.',
)
replace_exact(
    'wiki/modpack-catalog/meta/SEMANTIC-MAGIC-COVERAGE.md',
    'These rows are deliberately **not additive to 888** until their exact/current inventory and deduplication state meet the inclusion rule.',
    'These rows are deliberately **not additive to 1249** until their exact/current inventory and deduplication state meet the inclusion rule.',
)
replace_exact(
    'wiki/modpack-catalog/meta/SEMANTIC-MAGIC-COVERAGE.md',
    '1. **888 is not “888 / unknown”.** It is a reconstructible counted minimum while the denominator remains open.\n2. Do not divide 888 by the 100 provider-component denominator. The current component target is `56/100`; provider-component coverage and semantic-magic coverage answer different questions.\n3. Do not add public lower bounds to 888 and call the result complete.',
    '1. **1249 is not “1249 / unknown”.** It is a reconstructible counted minimum while the denominator remains open.\n2. Do not divide 1249 by the 100 provider-component denominator. The current component target is `57/100`; provider-component coverage and semantic-magic coverage answer different questions.\n3. Do not add public lower bounds to 1249 and call the result complete.',
)
replace_exact(
    'wiki/modpack-catalog/meta/SEMANTIC-MAGIC-COVERAGE.md',
    '1. Goety 3.1.4 exact JAR/source reconciliation, Focus semantic reachability/deduplication and discrete ritual-identity inventory;\n2. current-pack config closure for Not Enough Glyphs 4.6.1 and other remaining conditional glyph/action rows;\n3. exact Gaze 1.1.7.1 rites/Geas inventory only when materially new exact evidence becomes available;\n4. exact Ignis Soulfires: Spellbooks 1.1.0 semantic registry inventory;\n5. remaining open provider inventories that can materially reduce the denominator blocker.',
    '1. current-pack config closure for Not Enough Glyphs 4.6.1 and other remaining conditional glyph/action rows;\n2. exact Gaze 1.1.7.1 rites/Geas inventory only when materially new exact evidence becomes available;\n3. exact Ignis Soulfires: Spellbooks 1.1.0 semantic registry inventory;\n4. Goety Iron 3.1 and Goety Cataclysm 1.21.1-1.8.2 exact semantic inventories without duplicating base-Goety ownership;\n5. remaining open provider inventories that can materially reduce the denominator blocker.',
)

# Current coverage summary.
replace_exact(
    'wiki/modpack-catalog/meta/CATALOG-COVERAGE-CURRENT.md',
    'The reconstructible semantic ledger lives in [`SEMANTIC-MAGIC-COVERAGE.md`](./SEMANTIC-MAGIC-COVERAGE.md). Phase 2BG canonically closes a **strict counted minimum of 888 semantic magic objects** from provider records that meet the ledger\'s inclusion rule.',
    'The reconstructible semantic ledger lives in [`SEMANTIC-MAGIC-COVERAGE.md`](./SEMANTIC-MAGIC-COVERAGE.md). Phase 2BH canonically closes a **strict counted minimum of 1249 semantic magic objects** from provider records that meet the ledger\'s inclusion rule.',
)
replace_exact(
    'wiki/modpack-catalog/meta/CATALOG-COVERAGE-CURRENT.md',
    'The latest semantic promotion is **Leyline Spellbooks +14**. Exact hash-matched 1.0.3 artifact evidence closes 14 unconditional provider spell registrations; no Leylines-specific spell lock or conditional registration gate is present, while generic Iron\'s host config remains separate runtime QA. See [`../providers/leyline-spellbooks/EXACT-1.0.3-ARTIFACT-AUDIT.md`](../providers/leyline-spellbooks/EXACT-1.0.3-ARTIFACT-AUDIT.md).',
    'The latest semantic promotion is **Goety +361**. Exact hash-matched 3.1.4 artifact evidence closes 123 active/acquirable Focus actions and 238 available distinct non-Focus ritual actions after semantic deduplication and physical-provider condition filtering. Runtime/API/balance and provider-owned settlement remain separate fail-closed gates. See [`../providers/goety/EXACT-3.1.4-ARTIFACT-AUDIT.md`](../providers/goety/EXACT-3.1.4-ARTIFACT-AUDIT.md).\n\nThe preceding semantic promotion is **Leyline Spellbooks +14**. Exact hash-matched 1.0.3 artifact evidence closes 14 unconditional provider spell registrations; no Leylines-specific spell lock or conditional registration gate is present, while generic Iron\'s host config remains separate runtime QA. See [`../providers/leyline-spellbooks/EXACT-1.0.3-ARTIFACT-AUDIT.md`](../providers/leyline-spellbooks/EXACT-1.0.3-ARTIFACT-AUDIT.md).',
)
replace_exact(
    'wiki/modpack-catalog/meta/CATALOG-COVERAGE-CURRENT.md',
    'Therefore:\n\n- semantic numerator delta from Leyline Spellbooks 1.0.3 exact closure: **+14**;',
    'Therefore:\n\n- semantic numerator delta from Goety 3.1.4 exact closure: **+361**;\n- semantic numerator delta from Leyline Spellbooks 1.0.3 exact closure: **+14**;',
)
replace_exact(
    'wiki/modpack-catalog/meta/CATALOG-COVERAGE-CURRENT.md',
    '- strict reconstructible semantic minimum: **888**;',
    '- strict reconstructible semantic minimum: **1249**;',
)
replace_exact(
    'wiki/modpack-catalog/meta/CATALOG-COVERAGE-CURRENT.md',
    'Phase 2BH now has a **durable promotion candidate** for Goety 3.1.4 from exact hash-matched artifact evidence: **123 active Focus actions + 238 available distinct non-Focus ritual actions = 361**. Canonical values remain **888 / 56 of 100** until durable merge + exact post-merge CI; candidate values are **1249 / 57 of 100**. Runtime/API/balance gates remain separate.',
    'Phase 2BH is canonical for Goety 3.1.4 from exact hash-matched artifact evidence: **123 active Focus actions + 238 available distinct non-Focus ritual actions = 361**. Durable PR #198 HEAD `d75f82a23b5c977ccc8ec84813bf89c928ffc0ab` passed CI #2523; squash merge `4fcc40aaf8149b5511dbd882a5616ee5240cd640` passed exact-SHA post-merge CI #2524 and published canonical QA artifact `10291461067` with SHA-256 `4f2ccf8be11cdba348c7cd0bdc64e595f6b101257b2b99f80fbe5542fae41ada`. Canonical values are **1249 / 57 of 100**. Runtime/API/balance gates remain separate.',
)
replace_exact(
    'wiki/modpack-catalog/meta/CATALOG-COVERAGE-CURRENT.md',
    '## Phase 2BH promotion candidate — Goety 3.1.4\n\nExact 3.1.4 artifact identity closes candidate **+361** and candidate component #57. See `PHASE2BH-GOETY-3.1.4-EXACT-CHECKPOINT.md` and `../providers/goety/EXACT-3.1.4-ARTIFACT-AUDIT.md`. Canonical baseline remains 888 / 56/100 pending promotion.',
    '## Phase 2BH — Goety 3.1.4 component #57, canonical\n\nExact 3.1.4 artifact identity closes **+361** and component #57. Durable PR #198 clean HEAD `d75f82a23b5c977ccc8ec84813bf89c928ffc0ab` passed Black Arcana CI #2523 / run `34672038273`; squash merge `4fcc40aaf8149b5511dbd882a5616ee5240cd640` passed exact-SHA post-merge CI #2524 / run `34672222798` and published the canonical QA JAR. See `PHASE2BH-GOETY-3.1.4-EXACT-CHECKPOINT.md` and `../providers/goety/EXACT-3.1.4-ARTIFACT-AUDIT.md`. Canonical totals are **1249 / 57/100**.',
)
replace_exact(
    'wiki/modpack-catalog/meta/CATALOG-COVERAGE-CURRENT.md',
    '**Canonical provider-component coverage after Phase 2BG: 56/100 = 56%.**',
    '**Canonical provider-component coverage after Phase 2BH: 57/100 = 57%.**',
)
replace_exact(
    'wiki/modpack-catalog/meta/CATALOG-COVERAGE-CURRENT.md',
    '| 56 | Phase 2BG / PR #195 | `leylines` | canonical at `main@88f042f68429ff920314a7ec3a6923369edc93fd`; audited HEAD `a9d7b55044230bbb011f7233ffd75d9a8321489b` CI #2503 GREEN; post-merge CI #2504 GREEN |',
    '| 56 | Phase 2BG / PR #195 | `leylines` | canonical at `main@88f042f68429ff920314a7ec3a6923369edc93fd`; audited HEAD `a9d7b55044230bbb011f7233ffd75d9a8321489b` CI #2503 GREEN; post-merge CI #2504 GREEN |\n| 57 | Phase 2BH / PR #198 | `goety` | canonical at `main@4fcc40aaf8149b5511dbd882a5616ee5240cd640`; audited HEAD `d75f82a23b5c977ccc8ec84813bf89c928ffc0ab` CI #2523 GREEN; post-merge CI #2524 GREEN; QA artifact `10291461067` |',
)

# Current provider inventory summary.
replace_exact(
    'wiki/modpack-catalog/meta/CURRENT-MAGIC-PROVIDERS.md',
    'O denominador interno corrente do catálogo foi reconciliado para **100 componentes mágicos/cross-domain**, dos quais **56 estão canônicos** após Phase 2BG / PR #195. Esse 56/100 é uma métrica técnica de fechamento de componentes e **não** é a porcentagem de spells/magias.',
    'O denominador interno corrente do catálogo foi reconciliado para **100 componentes mágicos/cross-domain**, dos quais **57 estão canônicos** após Phase 2BH / PR #198. Esse 57/100 é uma métrica técnica de fechamento de componentes e **não** é a porcentagem de spells/magias.',
)
replace_exact(
    'wiki/modpack-catalog/meta/CURRENT-MAGIC-PROVIDERS.md',
    '## Checkpoint Goety — Phase 2BH exact candidate\n\nExact `goety-3.1.4.jar` evidence closes **123 active Focus actions + 238 available distinct non-Focus ritual actions = +361**. Candidate totals: **1249 semantic objects / 57 of 100 components**; canonical values remain 888 / 56 until durable merge + exact post-merge CI. Runtime/API/provider settlement remains fail-closed.',
    '## Checkpoint Goety — Phase 2BH canonical\n\nExact `goety-3.1.4.jar` evidence closes **123 active Focus actions + 238 available distinct non-Focus ritual actions = +361**. Durable PR #198 HEAD `d75f82a23b5c977ccc8ec84813bf89c928ffc0ab` passed CI #2523; squash merge `4fcc40aaf8149b5511dbd882a5616ee5240cd640` passed exact-SHA post-merge CI #2524 and published QA artifact `10291461067` with SHA-256 `4f2ccf8be11cdba348c7cd0bdc64e595f6b101257b2b99f80fbe5542fae41ada`. Canonical totals are **1249 semantic objects / 57 of 100 components**. Runtime/API/provider settlement remains fail-closed.',
)

# Provider audit queue.
replace_exact(
    'wiki/modpack-catalog/meta/PROVIDER-AUDIT-QUEUE.md',
    '- `main` canônica após Phase 2BG durable / PR #195: `88f042f68429ff920314a7ec3a6923369edc93fd`; HEAD limpo `a9d7b55044230bbb011f7233ffd75d9a8321489b` passou CI #2503 e o exact-SHA post-merge CI #2504 ficou GREEN, incluindo canonical QA-JAR publication;',
    '- `main` canônica após Phase 2BH durable / PR #198: `4fcc40aaf8149b5511dbd882a5616ee5240cd640`; HEAD limpo `d75f82a23b5c977ccc8ec84813bf89c928ffc0ab` passou CI #2523 e o exact-SHA post-merge CI #2524 ficou GREEN, incluindo canonical QA-JAR publication;',
)
replace_exact(
    'wiki/modpack-catalog/meta/PROVIDER-AUDIT-QUEUE.md',
    'A reconstrução canônica após Phase 2BG fecha **888 objetos mágicos semânticos** com a promoção exata de Leyline Spellbooks 1.0.3.',
    'A reconstrução canônica após Phase 2BH fecha **1249 objetos mágicos semânticos** com a promoção exata de Goety 3.1.4.',
)
replace_exact(
    'wiki/modpack-catalog/meta/PROVIDER-AUDIT-QUEUE.md',
    '- delta semântico Leyline Spellbooks 1.0.3 Phase 2BG: **+14** (`14 exact unconditional registry identities`);\n- mínimo estrito global canônico: **888**;',
    '- delta semântico Leyline Spellbooks 1.0.3 Phase 2BG: **+14** (`14 exact unconditional registry identities`);\n- delta semântico Goety 3.1.4 Phase 2BH: **+361** (`123 active Focus + 238 available distinct non-Focus rituals`);\n- mínimo estrito global canônico: **1249**;',
)
replace_exact(
    'wiki/modpack-catalog/meta/PROVIDER-AUDIT-QUEUE.md',
    '- cobertura canônica de componentes após Phase 2BG: **56/100 = 56%**; componente #56 fechado pelo PR #195 com CI #2503 no HEAD limpo e CI #2504 no merge SHA exato.\n\nO valor 56/100 nunca substitui a métrica semântica de magias.\n\n## Phase 2BH — Goety 3.1.4 — candidate component #57\n\nExact evidence PR #197 closes **123 Focus + 238 non-Focus rituals = +361 candidate semantic objects**. Accepted run/artifact pairs: `34670150370/10290083272`, `34670458172/10290222369`, `34670556329/10290527131`, `34670758163/10289884505`. Canonical baseline remains **888 / 56/100**; candidate **1249 / 57/100**.',
    '- cobertura canônica de componentes após Phase 2BH: **57/100 = 57%**; componente #57 fechado pelo PR #198 com CI #2523 no HEAD limpo e CI #2524 no merge SHA exato.\n\nO valor 57/100 nunca substitui a métrica semântica de magias.\n\n## Phase 2BH — Goety 3.1.4 — componente #57 canônico\n\nExact evidence PR #197 closes **123 Focus + 238 non-Focus rituals = +361 semantic objects**. Accepted run/artifact pairs: `34670150370/10290083272`, `34670458172/10290222369`, `34670556329/10290527131`, `34670758163/10289884505`. Durable PR #198 clean HEAD `d75f82a23b5c977ccc8ec84813bf89c928ffc0ab` passed CI #2523; squash merge `4fcc40aaf8149b5511dbd882a5616ee5240cd640` passed exact-SHA post-merge CI #2524. Canonical QA artifact: `10291461067`, SHA-256 `4f2ccf8be11cdba348c7cd0bdc64e595f6b101257b2b99f80fbe5542fae41ada`. Canonical totals are **1249 / 57/100**.',
)

# Sanity gates for the intended promotion.
checks = {
    'wiki/modpack-catalog/meta/SEMANTIC-MAGIC-COVERAGE.md': ['**1249 semantic magic objects', '| [Goety](../providers/goety/README.md) | 3.1.4 | 361 | `COUNTED_EXACT`', '| **Strict total** |  | **1249**'],
    'wiki/modpack-catalog/meta/CATALOG-COVERAGE-CURRENT.md': ['Phase 2BH canonically closes', '**Canonical provider-component coverage after Phase 2BH: 57/100 = 57%.**', '| 57 | Phase 2BH / PR #198 | `goety` |'],
    'wiki/modpack-catalog/meta/CURRENT-MAGIC-PROVIDERS.md': ['**57 estão canônicos**', '## Checkpoint Goety — Phase 2BH canonical'],
    'wiki/modpack-catalog/meta/PROVIDER-AUDIT-QUEUE.md': ['**1249 objetos mágicos semânticos**', 'componente #57 canônico'],
}
for path, needles in checks.items():
    text = (ROOT / path).read_text()
    for needle in needles:
        if needle not in text:
            raise SystemExit(f'{path}: missing postcondition {needle!r}')

print('Phase 2BH final-evidence reconciliation prepared: canonical 1249 / 57 of 100')
