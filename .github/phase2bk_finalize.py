#!/usr/bin/env python3
from pathlib import Path
import re


def read(p):
    return Path(p).read_text(encoding="utf-8")


def write(p, s):
    Path(p).write_text(s, encoding="utf-8")


def one(s, old, new, label):
    n = s.count(old)
    assert n == 1, f"{label}: expected 1 match, got {n}"
    return s.replace(old, new, 1)


def regex1(s, pat, repl, label, flags=0):
    out, n = re.subn(pat, repl, s, count=1, flags=flags)
    assert n == 1, f"{label}: expected 1 match, got {n}"
    return out


# Semantic ledger: zero closure, no strict-total change.
p = "wiki/modpack-catalog/meta/SEMANTIC-MAGIC-COVERAGE.md"
s = read(p)
phase = """## Phase 2BK exact zero closure — Ignis Soulfires: Spellbooks 1.1.0

Exact hash-matched artifact evidence closes Ignis Soulfires: Spellbooks 1.1.0 as `BRIDGE_COMPAT + GEAR_LOOT_SUPPORT` with **0 independent semantic magic objects**. The artifact contains 11 provider classes; its own registry surfaces are one armor-material registry and one five-item equipment registry. Across every provider class, structural inspection finds 0 hits for `AbstractSpell`, `registerSpell`, `SpellRegistry`, `Ritual`, `Rite` or `Ability`; packaged provider data contains equipment tags/recipes rather than a spell/ritual/action registry.

Isolated NON-MERGE PR #203 audited exact HEAD `ed807b77345cde1803767d804e26ea972c41d964`; run `34688273425` was GREEN and published text-only artifact `10296406134` with digest `sha256:5e96a319aea648aadf2c70bdf9b870a26a9503068307befc8a9972bb7b1cd52e`. The ARR JAR itself was not redistributed. Phase 2BK therefore classifies the provider `ZERO_BRIDGE_INFRA`, contributes **+0**, and leaves the strict semantic minimum at **1250**. The provider component itself is now closed, moving the separate technical component metric to **58/100**.

"""
s = one(
    s,
    "## Phase 2BJ semantic promotion — Gaze 1.1.7.1 exact artifact\n",
    phase + "## Phase 2BJ semantic promotion — Gaze 1.1.7.1 exact artifact\n",
    "semantic phase insert",
)
s = regex1(
    s,
    r"^\| \[Ignis Soulfires: Spellbooks\]\([^\n]+$",
    "| [Ignis Soulfires: Spellbooks](../providers/ignis-soulfires-spellbooks/README.md) 1.1.0 | exact hash-matched artifact closes 11 provider classes, one armor-material registry and exactly five equipment items; no spell/ritual/action registry exists | `ZERO_BRIDGE_INFRA / EXACT ARTIFACT CLOSED / +0` | gear/items/passive equipment behavior are excluded by metric definition; exact artifact proves zero independent semantic magic objects |",
    "semantic Ignis row",
    re.M,
)
next_block = """## Next closure order

To converge on a final denominator efficiently, prioritize:

1. Goety Iron 3.1 and Goety Cataclysm 1.21.1-1.8.2 exact semantic inventories without duplicating base-Goety ownership;
2. obtain deployed config evidence for input-blocked conditional rows, especially Not Enough Glyphs 4.6.1 and Gaze 1.1.7.1 Rites;
3. remaining open provider inventories that can materially reduce the denominator blocker.

Phase 3 remains blocked"""
s = regex1(
    s,
    r"## Next closure order\n\n.*?\n\nPhase 3 remains blocked",
    next_block,
    "semantic next order",
    re.S,
)
write(p, s)

# Coverage current: strict semantic total stays 1250; technical component becomes 58/100.
p = "wiki/modpack-catalog/meta/CATALOG-COVERAGE-CURRENT.md"
s = read(p)
s = one(
    s,
    "The reconstructible semantic ledger lives in [`SEMANTIC-MAGIC-COVERAGE.md`](./SEMANTIC-MAGIC-COVERAGE.md). Phase 2BJ raises the **strict counted minimum to 1250 semantic magic objects** from provider records that meet the ledger's inclusion rule. The global denominator is still incomplete and no semantic percentage is declared.",
    "The reconstructible semantic ledger lives in [`SEMANTIC-MAGIC-COVERAGE.md`](./SEMANTIC-MAGIC-COVERAGE.md). Phase 2BK keeps the **strict counted minimum at 1250 semantic magic objects** while closing Ignis Soulfires: Spellbooks 1.1.0 as an exact zero-semantic bridge/gear provider. The global denominator is still incomplete and no semantic percentage is declared.",
    "coverage top",
)
marker = "The latest semantic promotion is **Gaze +1**."
assert s.count(marker) == 1
extra = "Phase 2BK has a semantic delta of **0**: exact hash-matched Ignis Soulfires: Spellbooks 1.1.0 contains only its armor-material/item bridge surfaces and no provider-owned spell, ritual, rite or equivalent action registry. This closes provider component **#58** without changing the semantic numerator. See [`../providers/ignis-soulfires-spellbooks/EXACT-1.1.0-ARTIFACT-AUDIT.md`](../providers/ignis-soulfires-spellbooks/EXACT-1.1.0-ARTIFACT-AUDIT.md).\n\n"
s = s.replace(marker, extra + marker, 1)
s = one(
    s,
    "Therefore:\n\n- semantic numerator delta from Gaze 1.1.7.1 exact closure: **+1**;",
    "Therefore:\n\n- semantic numerator/denominator delta attributable to Ignis Soulfires: Spellbooks 1.1.0: **+0**;\n- semantic numerator delta from Gaze 1.1.7.1 exact closure: **+1**;",
    "coverage therefore",
)
section = """## Phase 2BK — Ignis Soulfires: Spellbooks 1.1.0 component #58, exact zero closure

Exact hash-matched artifact evidence closes the provider as `BRIDGE_COMPAT + GEAR_LOOT_SUPPORT`: 11 provider classes, one armor-material registry, one five-item equipment registry, and no provider-owned spell/ritual/action registry. Clean-room structural inspection finds 0 `AbstractSpell`, `registerSpell`, `SpellRegistry`, `Ritual`, `Rite` and `Ability` class hits. Semantic disposition is `ZERO_BRIDGE_INFRA` with **+0**; the strict semantic minimum remains **1250**.

Isolated NON-MERGE PR #203 exact HEAD `ed807b77345cde1803767d804e26ea972c41d964` passed run `34688273425`; text-only evidence artifact `10296406134` has digest `sha256:5e96a319aea648aadf2c70bdf9b870a26a9503068307befc8a9972bb7b1cd52e`. The provider was already an open unit in the reconciled 100-component denominator, so exact closure moves the technical metric to **58/100**. Runtime numerical gear behavior and any future adapter remain separate fail-closed gates.

"""
s = one(
    s,
    "## Phase 2BJ — Gaze 1.1.7.1 semantic-only exact promotion\n",
    section + "## Phase 2BJ — Gaze 1.1.7.1 semantic-only exact promotion\n",
    "coverage phase section",
)
s = one(
    s,
    "**Canonical provider-component coverage after Phase 2BH: 57/100 = 57%.**",
    "**Canonical provider-component coverage after Phase 2BK: 58/100 = 58%.**",
    "coverage component headline",
)
row = "| 57 | Phase 2BH / PR #198 | `goety` | canonical at `main@4fcc40aaf8149b5511dbd882a5616ee5240cd640`; audited HEAD `d75f82a23b5c977ccc8ec84813bf89c928ffc0ab` CI #2523 GREEN; post-merge CI #2524 GREEN; QA artifact `10291461067` |"
assert s.count(row) == 1
s = s.replace(
    row,
    row + "\n| 58 | Phase 2BK | `ignissoulfires_spellbooks` | exact hash-matched 1.1.0 gear/bridge closure; `ZERO_BRIDGE_INFRA`; semantic +0; evidence PR #203 / run `34688273425` |",
    1,
)
write(p, s)

# Current provider inventory.
p = "wiki/modpack-catalog/meta/CURRENT-MAGIC-PROVIDERS.md"
s = read(p)
s = one(
    s,
    "O denominador interno corrente do catálogo foi reconciliado para **100 componentes mágicos/cross-domain**, dos quais **57 estão canônicos** após Phase 2BH / PR #198. Esse 57/100 é uma métrica técnica de fechamento de componentes e **não** é a porcentagem de spells/magias.",
    "O denominador interno corrente do catálogo permanece **100 componentes mágicos/cross-domain**; Phase 2BK fecha `ignissoulfires_spellbooks` como componente **#58**, portanto **58 estão canônicos**. Esse 58/100 é uma métrica técnica de fechamento de componentes e **não** é a porcentagem de spells/magias.",
    "providers component current",
)
cp = """## Checkpoint Ignis Soulfires: Spellbooks — Phase 2BK exact zero closure

O artefato físico `ignissoulfires_spellbooks-1.1.0.jar` / SHA-1 `dcde77db35b6de3562b4e6de0025746eaf68f119` foi materializado do File ID CurseForge exato `8620663` e hash-matched em NON-MERGE PR #203. O JAR possui 11 classes próprias; seus registries são um armor material e exatamente cinco equipment items. Não há `AbstractSpell`, `registerSpell`, `SpellRegistry`, `Ritual`, `Rite` ou `Ability` nas classes do provider, nem spell/ritual/action data registry empacotado.

A classificação exata é `BRIDGE_COMPAT + GEAR_LOOT_SUPPORT`; semanticamente é `ZERO_BRIDGE_INFRA`, **+0** objetos. O mínimo estrito permanece **1250**. Como o provider já era uma unidade aberta do denominador técnico de 100 componentes, seu fechamento exato torna-o componente **#58 / 58/100**. Evidência: audit HEAD `ed807b77345cde1803767d804e26ea972c41d964`, run `34688273425`, text-only artifact `10296406134`. Runtime gear/balance e qualquer adapter Black Arcana continuam fail-closed.

"""
s = one(
    s,
    "## Checkpoint Gaze — Phase 2BJ exact-artifact semantic promotion\n",
    cp + "## Checkpoint Gaze — Phase 2BJ exact-artifact semantic promotion\n",
    "providers checkpoint insert",
)
write(p, s)

# Provider audit queue.
p = "wiki/modpack-catalog/meta/PROVIDER-AUDIT-QUEUE.md"
s = read(p)
s = regex1(
    s,
    r"- `main` canônica após Phase 2BI / PR #200: `21d63c58a2ad6cd19f4f68131bb39e4b39bdd1c2`;.*",
    "- base canônica considerada para Phase 2BK: `main@fa14b75bf08482031e4fabbc779d30d295e22c5e`; esse SHA contém Phase 2BJ / PR #202 e passou exact-SHA post-merge CI #2531, incluindo canonical QA-JAR publication;",
    "queue authority",
    re.M,
)
s = one(
    s,
    "A reconstrução canônica candidata da Phase 2BJ fecha **1250 objetos mágicos semânticos** após a promoção exata de Soulward Shield/Gaze. O denominador global continua incompleto e nenhuma porcentagem semântica é declarada.",
    "A reconstrução canônica após Phase 2BJ fecha **1250 objetos mágicos semânticos**. Phase 2BK fecha Ignis Soulfires: Spellbooks em **+0** por evidência exata, portanto o mínimo continua **1250**. O denominador global continua incompleto e nenhuma porcentagem semântica é declarada.",
    "queue semantic current",
)
s = one(
    s,
    "- delta semântico Gaze 1.1.7.1 Phase 2BJ: **+1**;",
    "- delta semântico Ignis Soulfires: Spellbooks 1.1.0 Phase 2BK: **+0** (`ZERO_BRIDGE_INFRA` exact-artifact);\n- delta semântico Gaze 1.1.7.1 Phase 2BJ: **+1**;",
    "queue delta",
)
s = one(
    s,
    "- mínimo estrito global candidato após Phase 2BJ: **1250**;",
    "- mínimo estrito global após Phase 2BK: **1250**;",
    "queue total",
)
s = one(
    s,
    "- cobertura canônica de componentes após Phase 2BH: **57/100 = 57%**; componente #57 fechado pelo PR #198 com CI #2523 no HEAD limpo e CI #2524 no merge SHA exato.",
    "- cobertura de componentes após o fechamento Phase 2BK: **58/100 = 58%**; `ignissoulfires_spellbooks` é componente #58 por exact-artifact closure, sem delta semântico.",
    "queue component current",
)
s = one(
    s,
    "O valor 57/100 nunca substitui a métrica semântica de magias.",
    "O valor 58/100 nunca substitui a métrica semântica de magias.",
    "queue warning",
)
qsection = """## Phase 2BK — Ignis Soulfires: Spellbooks 1.1.0 — componente #58 / semantic +0

| Mod ID | Artefato físico | Estado |
|---|---|---|
| `ignissoulfires_spellbooks` | `ignissoulfires_spellbooks-1.1.0.jar` | EXACT HASH-MATCHED ARTIFACT / BRIDGE_COMPAT + GEAR_LOOT_SUPPORT / 11 PROVIDER CLASSES / ARMOR MATERIAL + 5 ITEMS / NO SPELL-RITUAL-ACTION REGISTRY / ZERO_BRIDGE_INFRA / +0 SEMANTIC / COMPONENT #58 |

Evidence: physical/audit SHA-1 `dcde77db35b6de3562b4e6de0025746eaf68f119`; CurseForge project/file `1572171 / 8620663`; NON-MERGE PR #203; audit HEAD `ed807b77345cde1803767d804e26ea972c41d964`; run `34688273425` GREEN; text-only artifact `10296406134`, digest `sha256:5e96a319aea648aadf2c70bdf9b870a26a9503068307befc8a9972bb7b1cd52e`. ARR JAR not redistributed. Runtime gear values/ABI and any Black Arcana adapter remain fail-closed.

"""
s = one(
    s,
    "## Phase 2BH — Goety 3.1.4 — componente #57 canônico\n",
    qsection + "## Phase 2BH — Goety 3.1.4 — componente #57 canônico\n",
    "queue phase insert",
)
write(p, s)

# SOURCES provenance: insert exact ARR artifact row after Cataclysm: Spellbooks.
p = "SOURCES.md"
s = read(p)
new_source = "| [Ignis Soulfires: Spellbooks `1.1.0`](https://www.curseforge.com/minecraft/mc-mods/ignis-soulfires-spellbooks) | exact installed-artifact read-only catalog audit; CurseForge project/file `1572171 / 8620663`, physical/audit SHA-1 `dcde77db35b6de3562b4e6de0025746eaf68f119`; exact artifact closes the provider as armor/material compatibility gear with zero independent semantic magic objects | `REFERENCE_ONLY / COMPATIBILITY_TARGET / ARR`; NON-MERGE PR #203 materialized and hash-matched the exact publisher file, retaining only cryptographic identity, metadata/resource paths, class/member/type signatures and registry type/count facts. No implementation bodies, recipe ingredient payloads, localization prose, textures/models/animations/sounds are copied/adapted; the JAR is not redistributed; runtime gear/API semantics remain fail-closed |"
s = regex1(
    s,
    r"(^\| \[Cataclysm: Spellbooks `1\.1\.13`\].*$)",
    lambda m: m.group(1) + "\n" + new_source,
    "sources Ignis insert",
    re.M,
)
write(p, s)

# Third-party notices: exact ARR compatibility target.
p = "THIRD_PARTY_NOTICES.md"
s = read(p)
s = s.replace(
    "## Dependency / compatibility evidence — through 2026-09-11",
    "## Dependency / compatibility evidence — through 2026-09-12",
    1,
)
new_notice = "| Ignis Soulfires: Spellbooks | installed `1.1.0`; JAR `ignissoulfires_spellbooks-1.1.0.jar`; CurseForge project/file `1572171 / 8620663`; physical/audit SHA-1 `dcde77db35b6de3562b4e6de0025746eaf68f119`; exact audit proves one armor-material registry and five equipment items with no provider spell/ritual/action registry | `REFERENCE_ONLY / COMPATIBILITY_TARGET` exact-artifact factual audit for authority/deduplication and zero-semantic classification | project and exact artifact metadata are **All Rights Reserved**. Binary inspection was restricted to cryptographic identity, factual metadata/resource paths, class/member/type signatures and narrow registry type/count facts; no implementation bodies/source reconstruction, recipe ingredient payloads, localization prose, textures/models/animations/sounds are copied/adapted. The JAR is not redistributed; any stronger derivation is `PERMISSION_REQUIRED`/`REVIEW_REQUIRED` |"
s = regex1(
    s,
    r"(^\| Cataclysm: Spellbooks \|.*$)",
    lambda m: m.group(1) + "\n" + new_notice,
    "notices Ignis insert",
    re.M,
)
write(p, s)
