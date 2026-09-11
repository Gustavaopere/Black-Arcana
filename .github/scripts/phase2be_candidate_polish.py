from pathlib import Path


def replace_once(path: str, old: str, new: str, label: str) -> None:
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    count = text.count(old)
    assert count == 1, f"{label}: expected exactly one occurrence, found {count}"
    p.write_text(text.replace(old, new, 1), encoding="utf-8")


SEM = "wiki/modpack-catalog/meta/SEMANTIC-MAGIC-COVERAGE.md"
CAT = "wiki/modpack-catalog/meta/CATALOG-COVERAGE-CURRENT.md"
QUEUE = "wiki/modpack-catalog/meta/PROVIDER-AUDIT-QUEUE.md"
CURRENT = "wiki/modpack-catalog/meta/CURRENT-MAGIC-PROVIDERS.md"

replace_once(
    SEM,
    "**874 semantic magic objects are reconstructible after applying the exact Phase 2BE Cataclysm 1.1.13 closure.**\n\nThis is a counted minimum, not the final denominator and not a coverage percentage.",
    "**Phase 2BE candidate strict minimum: 874 semantic magic objects are reconstructible after applying the exact Cataclysm 1.1.13 closure.**\n\nThe canonical `main` baseline entering PR #189 remains **815** until latest-main reconciliation, merge and exact post-merge validation promote this candidate. The semantic denominator remains incomplete, so neither value is a coverage percentage.",
    "semantic candidate framing",
)

replace_once(
    CAT,
    "The reconstructible semantic ledger lives in [`SEMANTIC-MAGIC-COVERAGE.md`](./SEMANTIC-MAGIC-COVERAGE.md). Against the physical 595-entry snapshot it now closes a **strict counted minimum of 874 semantic magic objects** from provider records that meet the ledger's inclusion rule. This is not a final denominator and no percentage is declared: conditional registrations, current publisher lower bounds and providers with open exact inventories remain outside the strict sum.",
    "The reconstructible semantic ledger lives in [`SEMANTIC-MAGIC-COVERAGE.md`](./SEMANTIC-MAGIC-COVERAGE.md). Phase 2BE now reconstructs a **candidate strict counted minimum of 874 semantic magic objects** from provider records that meet the ledger's inclusion rule. The canonical `main` baseline entering PR #189 remains **815** until latest-main reconciliation, merge and exact post-merge validation. The global denominator is still incomplete and no semantic percentage is declared.",
    "coverage candidate semantic framing",
)
replace_once(CAT, "## Canonical recent closure sequence", "## Recent canonical closures and current promotion candidate", "coverage sequence heading")

replace_once(
    QUEUE,
    "A reconstrução Phase 2BE fecha **874 objetos mágicos semânticos** após aplicar o inventário exato Cataclysm 1.1.13. Esse valor ainda é um mínimo contado, não um denominador final e não uma porcentagem global.",
    "A reconstrução Phase 2BE propõe **874 objetos mágicos semânticos** após aplicar o inventário exato Cataclysm 1.1.13. O baseline canônico de `main` que entra no PR #189 permanece **815** até latest-main reconciliation, merge e validação pós-merge exata. O denominador global continua incompleto e nenhuma porcentagem semântica é declarada.",
    "queue candidate semantic framing",
)
replace_once(QUEUE, "- mínimo estrito global: **874**;", "- mínimo estrito Phase 2BE candidato: **874**;", "queue candidate total label")

replace_once(
    CURRENT,
    "O registry exato fecha **59 `AbstractSpell` registrations `COUNTED_EXACT`**: 7 Abyssal, 4 Ender, 1 Evocation, 5 Holy, 11 Fire, 5 Ice, 4 Nature e 22 Technomancy.",
    "O registry exato fecha **59 `AbstractSpell` registrations `COUNTED_EXACT`**. Por implementation package group: 7 Abyssal, 4 Ender, 1 Evocation, 5 Holy, 11 Fire, 5 Ice, 4 Nature e 22 Technomancy; essa distribuição de packages não é promovida automaticamente a uma tabela de escolas/runtime mechanics.",
    "current package-group clarification",
)

for path, needle in [
    (SEM, "canonical `main` baseline entering PR #189 remains **815**"),
    (CAT, "Recent canonical closures and current promotion candidate"),
    (QUEUE, "mínimo estrito Phase 2BE candidato: **874**"),
    (CURRENT, "Por implementation package group"),
]:
    assert needle in Path(path).read_text(encoding="utf-8"), f"sanity missing {needle}"

print("Phase 2BE candidate/canonical wording polish passed")
