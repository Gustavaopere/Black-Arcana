#!/usr/bin/env python3
"""Check the five operational pending items against their evidence inventories."""
from __future__ import annotations
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
META = ROOT / "wiki/modpack-catalog/meta"
QA = ROOT / "docs/qa"


class MagicPendencyStatusTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.status = (META / "PENDENCIAS-MAGICAS-ATUAIS.md").read_text(encoding="utf-8")
        cls.cross = (META / "AUDITORIA-CROSS-DOMAIN-2026-10-08.md").read_text(encoding="utf-8")
        cls.binary = (META / "REVALIDACAO-BINARIA-39-PROVIDERS-2026-10-08.md").read_text(encoding="utf-8")
        cls.conditional = (META / "CONDITIONAL-PROVIDER-CLOSURE.md").read_text(encoding="utf-8")
        cls.stage = (QA / "ritual-veil-anchor-activation-design-gate-2026-10-08.md").read_text(encoding="utf-8")

    def test_exactly_five_named_status_rows(self):
        rows = re.findall(r"^\| (Identificar|Comprovar|Verificar|Atualizar|Concluir)[^|]*\|", self.status, re.MULTILINE)
        self.assertEqual(["Identificar", "Comprovar", "Verificar", "Atualizar", "Concluir"], rows)
        for flag in ("🟡", "⚠️", "✅", "⛔"):
            self.assertIn(flag, self.status)

    def test_cross_domain_triage_is_not_false_global_closure(self):
        section = self.cross.split("## Candidatos lexicais, estado por linha física", 1)[1].split(
            "## Onze casos", 1
        )[0]
        rows = [line for line in section.splitlines() if re.match(r"^\| #\d{3} \|", line)]
        self.assertEqual(46, len(rows))
        self.assertEqual(35, sum("✅ Catálogo existente" in line for line in rows))
        self.assertEqual(11, sum("⚠️ Dossiê físico revisado" in line for line in rows))
        self.assertIn("**489**", self.cross)
        self.assertIn("**96**", self.cross)
        self.assertIn("**347**", self.cross)
        self.assertIn("489/489 nomes físicos", self.status)
        self.assertIn("**não executado na instância real**", self.status)

    def test_39_non_binary_exact_provider_rows_are_explicit(self):
        section = self.binary.split("|---|---|---:|---|---|", 1)[1].split(
            "\n## Requisitos mínimos", 1
        )[0]
        rows = re.findall(r"^\| \[[^\]]+\]\([^)]+\) \|", section, re.MULTILINE)
        self.assertEqual(39, len(rows))
        self.assertIn("0/39", self.binary)
        self.assertIn("não executado neste lote", self.binary)

    def test_conditional_routes_point_to_current_green_folders(self):
        self.assertNotIn("../providers/⚠️-", self.conditional)
        self.assertIn("0 CATALOG-OPEN DIRECTORIES", self.conditional)
        section = self.conditional.split("## Current deployed-evidence routes", 1)[1].split(
            "\n## ", 1
        )[0]
        rows = [line for line in section.splitlines() if line.startswith("| ")
                and not line.startswith("| Provider")]
        self.assertEqual(14, len(rows))

    def test_ritual_stays_explicitly_blocked(self):
        self.assertIn("⛔ SEM INGRESSO CANÔNICO", self.stage)
        self.assertIn("RitualEngine.start(", self.stage)
        self.assertIn("não uma implementação", self.stage)


if __name__ == "__main__":
    unittest.main()
