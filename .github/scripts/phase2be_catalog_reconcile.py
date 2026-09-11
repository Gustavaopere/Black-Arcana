from pathlib import Path


def read(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    Path(path).write_text(text, encoding="utf-8")


def replace_once(path: str, old: str, new: str, label: str) -> None:
    text = read(path)
    count = text.count(old)
    assert count == 1, f"{label}: expected exactly one occurrence, found {count}"
    write(path, text.replace(old, new, 1))


def remove_line_starting(path: str, prefix: str, label: str) -> None:
    text = read(path)
    lines = text.splitlines(keepends=True)
    hits = [i for i, line in enumerate(lines) if line.startswith(prefix)]
    assert len(hits) == 1, f"{label}: expected exactly one line, found {len(hits)}"
    del lines[hits[0]]
    write(path, "".join(lines))


def assert_contains(path: str, needle: str, label: str) -> None:
    assert needle in read(path), f"{label}: missing {needle!r}"


SEM = "wiki/modpack-catalog/meta/SEMANTIC-MAGIC-COVERAGE.md"
CAT = "wiki/modpack-catalog/meta/CATALOG-COVERAGE-CURRENT.md"
QUEUE = "wiki/modpack-catalog/meta/PROVIDER-AUDIT-QUEUE.md"
CURRENT = "wiki/modpack-catalog/meta/CURRENT-MAGIC-PROVIDERS.md"
SOURCES = "SOURCES.md"
NOTICES = "THIRD_PARTY_NOTICES.md"

# --- Semantic ledger ---
replace_once(
    SEM,
    "- latest provider-component canonicalization base: `main@95ec538ff1c34766450393522ce3affe1039d0dd`, with post-merge Black Arcana CI **#2465** GREEN",
    "- latest completed catalog baseline entering Phase 2BE: `main@c5a46a622351b6d9157b4620ca5386889c7bd5f3`, with Black Arcana CI **#2467** GREEN after the Phase 2BD final-evidence reconciliation",
    "semantic baseline anchor",
)
replace_once(
    SEM,
    "**815 semantic magic objects are currently reconstructible from canonical provider records.**",
    "**874 semantic magic objects are reconstructible after applying the exact Phase 2BE Cataclysm 1.1.13 closure.**",
    "semantic headline",
)
replace_once(SEM, "- Iron's ecosystem and spell-content addons: **468**;", "- Iron's ecosystem and spell-content addons: **527**;", "semantic iron subtotal")
replace_once(SEM, "- total: `199 + 468 + 42 + 55 + 25 + 26 = 815`.", "- total: `199 + 527 + 42 + 55 + 25 + 26 = 874`.", "semantic arithmetic")

alshanex_row = "| [Alshanex's Familiars](../providers/alshanex-familiars/README.md) | 4.0.3 | 18 | `COUNTED_EXACT` | exact hash-matched JAR closes 7 provider-owned spell registrations + 11 packaged `alshanex_familiars:ritual_recipe` identities; migrated Sound/Tunes content and external familiar casts are excluded |"
cat_row = "| [Cataclysm: Spellbooks](../providers/cataclysm-spellbooks/README.md) | 1.1.13 | 59 | `COUNTED_EXACT` | exact hash-matched JAR closes 59 unconditional `AbstractSpell` registrations; 10 additional root localization keys are unregistered in 1.1.13 and excluded |"
replace_once(SEM, alshanex_row + "\n", alshanex_row + "\n" + cat_row + "\n", "semantic Cataclysm row insertion")
replace_once(SEM, "| **Strict total** |  | **815** |  |  |", "| **Strict total** |  | **874** |  |  |", "semantic strict total")
replace_once(
    SEM,
    "Bloodlines remains **28 counted actions**, and the strict total remains **815**.",
    "Bloodlines remains **28 counted actions**; after later provider closures, the global strict total is **874**.",
    "Bloodlines stale global total",
)

cat_section = """### Cataclysm: Spellbooks 1.1.13 exact-artifact closure

Phase 2BE materialized CurseForge File ID `8792628` through Curse Maven in isolated non-merge PR #188 and required SHA-1 `4af8348cc77bbff2ab7057c1fac26a5ab0a5b6a2` to match the physical modlist before factual inspection. The exact `SpellRegistries` static initializer closes **59** `registerSpell(...)` calls, **59** provider spell-class instantiations, **59** spell-field assignments and **0** conditional branches. Field/class/root-ID reconciliation closes **59 unique current spell identities**, for **+59**.

The exact implementation-package distribution is 7 Abyssal, 4 Ender, 1 Evocation, 5 Holy, 11 Fire, 5 Ice, 4 Nature and 22 Technomancy. The exact English localization has 69 root spell keys, but ten are not registered current spell IDs/classes and are excluded as translation-only/WIP-or-residual evidence: `conjure_abyssal_gnawer`, `conjure_clawdian`, `conjure_coral_golem`, `conjure_coralssus`, `cryopiercer`, `final_rend`, `hemorrhaging_impact`, `parting_shot`, `quick_strike`, `scorched_earth`.

The generic/current publisher project page advertises 65 spells, but that project-scale claim is not substituted for the physically installed 1.1.13 registry; a newer 1.1.14 beta also exists after the installed file. Exact numerical mechanics, acquisition and runtime/API integration remain separate gates. See [`../providers/cataclysm-spellbooks/EXACT-1.1.13-ARTIFACT-AUDIT.md`](../providers/cataclysm-spellbooks/EXACT-1.1.13-ARTIFACT-AUDIT.md) and [`../providers/cataclysm-spellbooks/EXACT-1.1.13-SPELL-INVENTORY.md`](../providers/cataclysm-spellbooks/EXACT-1.1.13-SPELL-INVENTORY.md).

"""
replace_once(SEM, "### Hexalia release-boundary reconciliation\n", cat_section + "### Hexalia release-boundary reconciliation\n", "semantic Cataclysm closure section")
replace_once(SEM, "These rows are deliberately **not additive to 815** until their exact/current inventory and deduplication state meet the inclusion rule.", "These rows are deliberately **not additive to 874** until their exact/current inventory and deduplication state meet the inclusion rule.", "semantic open-blocker total")
remove_line_starting(SEM, "| [Cataclysm: Spellbooks](../providers/cataclysm-spellbooks/README.md) 1.1.13 |", "remove Cataclysm open row")
replace_once(SEM, "1. **815 is not “815 / unknown”.** It is a reconstructible counted minimum while the denominator remains open.", "1. **874 is not “874 / unknown”.** It is a reconstructible counted minimum while the denominator remains open.", "semantic interpretation 1")
replace_once(SEM, "2. Do not divide 815 by the 100 provider-component denominator. `54/100` and semantic-magic coverage answer different questions.", "2. Do not divide 874 by the 100 provider-component denominator. The Phase 2BE component target is `55/100`; provider-component coverage and semantic-magic coverage answer different questions.", "semantic interpretation 2")
replace_once(SEM, "3. Do not add public lower bounds to 815 and call the result complete.", "3. Do not add public lower bounds to 874 and call the result complete.", "semantic interpretation 3")
old_next = """1. exact current inventory for `cataclysm_spellbooks` 1.1.13;
2. exact current inventory for `somakespells` 1.0.8-fix;
3. exact current inventory for `leylines` 1.0.3;
4. exact Gaze 1.1.7.1 rites/Geas inventory;
5. Goety 3.1.4 exact JAR/source reconciliation, Focus semantic reachability/deduplication and discrete ritual-identity inventory;
6. current-pack config closure for the remaining conditional glyph/action rows."""
new_next = """1. exact current inventory for `somakespells` 1.0.8-fix;
2. exact current inventory for `leylines` 1.0.3;
3. exact Gaze 1.1.7.1 rites/Geas inventory when materially new exact evidence becomes available;
4. Goety 3.1.4 exact JAR/source reconciliation, Focus semantic reachability/deduplication and discrete ritual-identity inventory;
5. current-pack config closure for the remaining conditional glyph/action rows."""
replace_once(SEM, old_next, new_next, "semantic next closure order")

# --- Coverage summary ---
replace_once(
    CAT,
    "a **strict counted minimum of 815 semantic magic objects**",
    "a **strict counted minimum of 874 semantic magic objects**",
    "coverage strict minimum",
)
old_latest = "The latest semantic promotion is **Alshanex's Familiars +18**. Exact hash-matched 4.0.3 artifact evidence closes seven provider-owned spell registrations and eleven packaged custom `alshanex_familiars:ritual_recipe` identities. Sound/Melodic content remains counted only under Tunes n' Tomes, while familiar AI/passives and external Iron's spell casts remain excluded. See [`../providers/alshanex-familiars/EXACT-4.0.3-ARTIFACT-AUDIT.md`](../providers/alshanex-familiars/EXACT-4.0.3-ARTIFACT-AUDIT.md)."
new_latest = "The latest semantic promotion proposed by Phase 2BE is **Cataclysm: Spellbooks +59**. Exact hash-matched 1.1.13 artifact evidence closes 59 unconditional provider spell registrations; ten additional root localization identities are not registered in the installed artifact and remain excluded. The generic/current 65-spell publisher scale is not substituted for the physical 1.1.13 registry. See [`../providers/cataclysm-spellbooks/EXACT-1.1.13-ARTIFACT-AUDIT.md`](../providers/cataclysm-spellbooks/EXACT-1.1.13-ARTIFACT-AUDIT.md).\n\nThe preceding semantic promotion is **Alshanex's Familiars +18**. Exact hash-matched 4.0.3 artifact evidence closes seven provider-owned spell registrations and eleven packaged custom `alshanex_familiars:ritual_recipe` identities. Sound/Melodic content remains counted only under Tunes n' Tomes, while familiar AI/passives and external Iron's spell casts remain excluded. See [`../providers/alshanex-familiars/EXACT-4.0.3-ARTIFACT-AUDIT.md`](../providers/alshanex-familiars/EXACT-4.0.3-ARTIFACT-AUDIT.md)."
replace_once(CAT, old_latest, new_latest, "coverage latest promotion")
replace_once(CAT, "- semantic numerator delta from Alshanex's Familiars 4.0.3 exact closure: **+18**;", "- semantic numerator delta from Cataclysm: Spellbooks 1.1.13 exact closure: **+59**;\n- semantic numerator delta from Alshanex's Familiars 4.0.3 exact closure: **+18**;", "coverage delta Cataclysm")
replace_once(CAT, "- strict reconstructible semantic minimum: **815**;", "- strict reconstructible semantic minimum: **874**;", "coverage total")
replace_once(CAT, "enter the strict **815** minimum at this checkpoint.", "enter the strict **874** minimum at this checkpoint.", "coverage Goety stale total")
replace_once(CAT, "**Canonical provider-component coverage after Phase 2BD: 54/100 = 54%.**", "**Phase 2BE promotion target: 55/100 = 55%. Component #55 remains candidate on PR #189 until merge, latest-main reconciliation and exact post-merge validation.**", "coverage component target")
row54 = "| 54 | Phase 2BD / PR #186 | `alshanex_familiars` | canonical at `main@95ec538ff1c34766450393522ce3affe1039d0dd`; audited HEAD `acfcff0fca09b3c2f7b4fcf082618a970e1d19c0` CI #2464 GREEN; post-merge CI #2465 GREEN |"
row55 = "| 55 | Phase 2BE / PR #189 | `cataclysm_spellbooks` | exact 1.1.13 59-spell identity closure; candidate until merge/latest-main reconciliation and post-merge validation |"
replace_once(CAT, row54 + "\n", row55 + "\n" + row54 + "\n", "coverage #55 row")
phase2be = """## Phase 2BE — Cataclysm: Spellbooks 1.1.13 component #55 candidate

Phase 2BE closes the physically installed spell identity inventory to exact artifact evidence:

- exact JAR `cataclysm_spellbooks-1.1.13-1.21.jar` / SHA-1 `4af8348cc77bbff2ab7057c1fac26a5ab0a5b6a2`;
- isolated non-merge PR #188 materialized exact File ID `8792628` and hash-matched the physical artifact;
- 59 `Supplier<AbstractSpell>` fields, 59 `registerSpell(...)` calls, 59 spell-class instantiations and 0 conditional branches in the exact registry initializer;
- exact group distribution: 7 Abyssal + 4 Ender + 1 Evocation + 5 Holy + 11 Fire + 5 Ice + 4 Nature + 22 Technomancy = **59**;
- ten additional root localization keys have no current registered spell identity and remain excluded;
- semantic delta: **+59**, yielding strict counted minimum **874** and Iron ecosystem subtotal **527**;
- the generic/current publisher scale of 65 spells is not substituted for the installed 1.1.13 registry;
- numerical mechanics, acquisition, runtime QA and future integration seams remain separate/fail-closed;
- clean-room audit retained only factual identity/registry/resource evidence and copied no upstream implementation or assets.

See [`PHASE2BE-CATACLYSM-SPELLBOOKS-1.1.13-EXACT-CHECKPOINT.md`](./PHASE2BE-CATACLYSM-SPELLBOOKS-1.1.13-EXACT-CHECKPOINT.md).

"""
replace_once(CAT, "## Phase 2BD — Alshanex's Familiars 4.0.3 component #54\n", phase2be + "## Phase 2BD — Alshanex's Familiars 4.0.3 component #54\n", "coverage Phase2BE section")
remove_line_starting(CAT, "- `cataclysm_spellbooks` — installed 1.1.13 remains ahead of the exact public source baseline already audited;", "coverage remove Cataclysm partial")

# --- Provider audit queue ---
replace_once(
    QUEUE,
    "- `main` canônica após Phase 2BD / PR #186: `95ec538ff1c34766450393522ce3affe1039d0dd`; post-merge Black Arcana CI #2465 GREEN;",
    "- base auditada para Phase 2BE: `main@c5a46a622351b6d9157b4620ca5386889c7bd5f3`; Phase 2BD final-evidence reconciliation CI #2467 GREEN; fechamento Cataclysm proposto por PR #189;",
    "queue authority anchor",
)
replace_once(QUEUE, "A reconstrução estrita fecha agora **815 objetos mágicos semânticos**.", "A reconstrução Phase 2BE fecha **874 objetos mágicos semânticos** após aplicar o inventário exato Cataclysm 1.1.13.", "queue semantic headline")
replace_once(QUEUE, "- delta semântico Alshanex 4.0.3: **+18**;", "- delta semântico Alshanex 4.0.3: **+18**;\n- delta semântico Cataclysm: Spellbooks 1.1.13: **+59**;", "queue Cataclysm delta")
replace_once(QUEUE, "- mínimo estrito global: **815**;", "- mínimo estrito global: **874**;", "queue semantic total")
replace_once(QUEUE, "- cobertura canônica de componentes após Phase 2BD: **54/100 = 54%**.", "- cobertura-alvo após promoção Phase 2BE: **55/100 = 55%**; componente #55 permanece candidato no PR #189 até merge e validação pós-merge.", "queue component target")
replace_once(QUEUE, "O valor 54/100 nunca substitui a métrica semântica de magias.", "O valor 55/100 nunca substitui a métrica semântica de magias.", "queue component interpretation")
phase2be_queue = """## Phase 2BE — Cataclysm: Spellbooks 1.1.13 — componente #55 candidato

| Mod ID | Artefato físico | Estado |
|---|---|---|
| `cataclysm_spellbooks` | `cataclysm_spellbooks-1.1.13-1.21.jar` | EXACT PHYSICAL / EXACT CURSEFORGE FILE / EXACT HASH-MATCHED ARTIFACT AUDIT / 59 REGISTERED SPELL IDENTITIES / 10 TRANSLATION-ONLY ROOT KEYS EXCLUDED / +59 SEMANTIC MAGICS / #55 CANDIDATE |

### Evidence boundary

- physical SHA-1 `4af8348cc77bbff2ab7057c1fac26a5ab0a5b6a2`;
- CurseForge project/file `1099461 / 8792628`;
- isolated non-merge PR #188 primary run/artifact `34656614109 / 10285687158`;
- constructor-ID disambiguation run/artifact `34656814496 / 10285756485`;
- exact registry: 59 `Supplier<AbstractSpell>` fields, 59 `registerSpell` calls, 59 class instantiations, 0 conditional branches;
- exact group distribution: 7 Abyssal, 4 Ender, 1 Evocation, 5 Holy, 11 Fire, 5 Ice, 4 Nature, 22 Technomancy;
- ten extra root localization keys are unregistered and excluded;
- publisher generic/current 65-spell scale is not substituted for physical 1.1.13;
- no upstream implementation/assets copied or adapted; balance/acquisition/runtime/API seams remain fail-closed where not separately proven.

"""
replace_once(QUEUE, "## Phase 2BD — Alshanex's Familiars 4.0.3 — componente #54\n", phase2be_queue + "## Phase 2BD — Alshanex's Familiars 4.0.3 — componente #54\n", "queue Phase2BE section")
row54q = "| 54 | 2BD / #186 | `alshanex_familiars` | CANÔNICO em `main@95ec538f...`; HEAD auditado CI #2464 GREEN; CI pós-merge #2465 GREEN |"
row55q = "| 55 | 2BE / #189 | `cataclysm_spellbooks` | 59/59 exact 1.1.13 spell inventory closure; candidato até merge/latest-main + CI pós-merge |"
replace_once(QUEUE, row54q + "\n", row55q + "\n" + row54q + "\n", "queue #55 row")
remove_line_starting(QUEUE, "- `cataclysm_spellbooks` 1.1.13 — publisher atual informa 65 spells, mas registry exato atual permanece aberto;", "queue remove Cataclysm priority")

# --- Current provider inventory ---
replace_once(CURRENT, "dos quais **54 estão canônicos** após Phase 2BD / PR #186. Esse 54/100", "dos quais **54 estão canônicos** na base que entra em Phase 2BE; o fechamento Cataclysm propõe o componente #55 via PR #189. O alvo 55/100", "current component candidate")
cat_checkpoint = """## Checkpoint Cataclysm: Spellbooks — Phase 2BE

O artefato físico `cataclysm_spellbooks-1.1.13-1.21.jar` / SHA-1 `4af8348cc77bbff2ab7057c1fac26a5ab0a5b6a2` foi materializado pelo File ID exato `8792628` em auditoria isolada e bateu criptograficamente com a modlist. O registry exato fecha **59 `AbstractSpell` registrations `COUNTED_EXACT`**: 7 Abyssal, 4 Ender, 1 Evocation, 5 Holy, 11 Fire, 5 Ice, 4 Nature e 22 Technomancy.

O `en_us` contém 69 root spell keys, mas dez não possuem identidade registrada no 1.1.13 e ficam excluídos como translation-only/WIP-or-residual. O claim genérico/current do publisher de 65 spells não substitui o registry físico instalado; existe inclusive uma 1.1.14 beta posterior ao arquivo do pack.

Esse fechamento é de identidade/contagem. Balance numérico, acquisition, runtime QA e qualquer seam futuro Black Arcana↔Cataclysm Spellbooks continuam separados e fail-closed até evidência provider-native segura.

"""
replace_once(CURRENT, "## Checkpoint Alshanex's Familiars — Phase 2BD\n", cat_checkpoint + "## Checkpoint Alshanex's Familiars — Phase 2BD\n", "current Cataclysm checkpoint")
replace_once(CURRENT, "após o fechamento exato de Alshanex 4.0.3, o mínimo semântico estrito global é **815**", "após aplicar o fechamento exato Phase 2BE de Cataclysm: Spellbooks 1.1.13, o mínimo semântico estrito global proposto é **874**", "current Goety global total")

# --- Provenance ---
old_source_row = "| [Cataclysm: Spellbooks `1.1.13`](https://www.curseforge.com/minecraft/mc-mods/cataclysm-spellbooks/files/8792628) | exact installed-artifact identity + publisher-current provider-scale audit; separate read-only public `1.1.11`-labelled source baseline at `AceTheEldritchKing/Cataclysm_Spellbooks_1.21.1@82a0af71f051058fe515c8b1cb9168e7f972f41c` for historical semantic/deduplication evidence | `REFERENCE_ONLY / COMPATIBILITY_TARGET / CURRENT-SOURCE MISMATCH / LICENSE REVIEW REQUIRED`; installed 1.1.13 is Beta and the linked public source still declares 1.1.11. Current CurseForge and `TEMPLATE_LICENSE.txt` identify PolyForm Shield 1.0.0 while the source `gradle.properties` declares All Rights Reserved. No code/assets are copied/adapted; exact current registries/API remain fail-closed until the 1.1.13 artifact or matching source is inspectable |"
new_source_row = "| [Cataclysm: Spellbooks `1.1.13`](https://www.curseforge.com/minecraft/mc-mods/cataclysm-spellbooks/files/8792628) | exact installed-artifact read-only catalog audit; SHA-1 `4af8348cc77bbff2ab7057c1fac26a5ab0a5b6a2`; 59 current provider spell registrations closed for semantic inventory/deduplication; separate public `1.1.11` source baseline retained only for historical comparison | `REFERENCE_ONLY / COMPATIBILITY_TARGET / CURRENT-SOURCE MISMATCH / LICENSE REVIEW REQUIRED`; current CurseForge and `TEMPLATE_LICENSE.txt` identify PolyForm Shield 1.0.0 while public-source `gradle.properties` declares All Rights Reserved. Exact binary inspection retained only hash/metadata, resource/localization IDs, class/member signatures, filtered root-ID literals and narrow registry/constructor facts. No implementation bodies/source reconstruction/assets/models/sounds/upstream prose are copied/adapted; numerical mechanics, acquisition and runtime/API integration remain fail-closed where not separately proven |"
replace_once(SOURCES, old_source_row, new_source_row, "SOURCES Cataclysm row")

old_notice_row = "| Cataclysm: Spellbooks | installed `1.1.13-1.21`; JAR `cataclysm_spellbooks-1.1.13-1.21.jar`; CurseForge File ID `8792628`; separate public source baseline `AceTheEldritchKing/Cataclysm_Spellbooks_1.21.1@82a0af71f051058fe515c8b1cb9168e7f972f41c` still declares `1.1.11-1.21` | `REFERENCE_ONLY / COMPATIBILITY_TARGET` exact-artifact identity/current publisher-scale audit plus read-only stale-source semantic baseline for deduplication | current CurseForge and source `TEMPLATE_LICENSE.txt` identify PolyForm Shield 1.0.0, while source `gradle.properties` declares `All Rights Reserved`; source metadata is therefore not treated as a derivation grant. PolyForm Shield also contains a noncompete restriction. No code/assets are copied/adapted; matching 1.1.13 source/registry/API remains `REVIEW_REQUIRED` and fail-closed |"
new_notice_row = "| Cataclysm: Spellbooks | installed `1.1.13-1.21`; JAR `cataclysm_spellbooks-1.1.13-1.21.jar`; CurseForge File ID `8792628`; physical/audit SHA-1 `4af8348cc77bbff2ab7057c1fac26a5ab0a5b6a2`; separate public source baseline still declares `1.1.11-1.21` | `REFERENCE_ONLY / COMPATIBILITY_TARGET` exact-artifact factual audit closing 59 current registered spell identities for catalog/deduplication while preserving the stale public source only as historical evidence | current CurseForge and source `TEMPLATE_LICENSE.txt` identify PolyForm Shield 1.0.0, while public-source `gradle.properties` declares `All Rights Reserved`; neither surface is treated as a derivation grant. Exact binary inspection was restricted to hash/metadata, archive/resource/localization IDs, class/member signatures, filtered root-ID literals and narrow registry/constructor facts. No implementation body/source reconstruction/assets/models/sounds/upstream prose are copied/adapted; exact numerical mechanics, acquisition and runtime/API integration remain `REVIEW_REQUIRED`/fail-closed |"
replace_once(NOTICES, old_notice_row, new_notice_row, "THIRD_PARTY_NOTICES Cataclysm row")

# --- Sanity checks ---
assert_contains(SEM, "| [Cataclysm: Spellbooks](../providers/cataclysm-spellbooks/README.md) | 1.1.13 | 59 | `COUNTED_EXACT` |", "semantic Cataclysm counted row")
assert_contains(SEM, "**874 semantic magic objects", "semantic 874 headline")
assert_contains(SEM, "199 + 527 + 42 + 55 + 25 + 26 = 874", "semantic arithmetic sanity")
assert "LOWER_BOUND / OPEN CURRENT REGISTRY` | exact 1.1.13" not in read(SEM), "Cataclysm open semantic row survived"
assert_contains(CAT, "Phase 2BE promotion target: 55/100 = 55%", "coverage 55 target")
assert_contains(QUEUE, "Cataclysm: Spellbooks 1.1.13: **+59**", "queue Cataclysm delta sanity")
assert_contains(CURRENT, "59 `AbstractSpell` registrations `COUNTED_EXACT`", "current Cataclysm checkpoint sanity")
assert_contains(SOURCES, "59 current provider spell registrations", "source provenance sanity")
assert_contains(NOTICES, "closing 59 current registered spell identities", "notice provenance sanity")

print("Phase 2BE catalog reconciliation assertions passed")
