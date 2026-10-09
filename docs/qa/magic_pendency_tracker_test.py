#!/usr/bin/env python3
"""Check the five operational pending items against their evidence inventories."""
from __future__ import annotations
import json
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
        cls.other = (META / "AUDITORIA-OTHER-2026-10-09.md").read_text(encoding="utf-8")
        cls.sixth = (META / "AUDITORIA-OTHER-LOTE-6-2026-10-09.md").read_text(encoding="utf-8")
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

    def test_third_pass_doc_triage_keeps_individual_registry_proof_open(self):
        section = self.cross.split(
            "## Terceiro ciclo — dez dossiês cross-domain adicionais", 1
        )[1].split("## Quarto ciclo — vinte dossiês cross-domain adicionais", 1)[0]
        ids = re.findall(r"^\| #(\d{3}) \|", section, re.MULTILINE)
        self.assertEqual(
            ["071", "074", "084", "193", "260", "321", "371", "433", "452", "568"],
            ids,
        )
        self.assertIn("**28 dossiês**", section)
        self.assertIn("11 candidatos `LEXICAL_NAME`", section)
        self.assertIn("17 de `RPG_GEAR_MOBS_DIMENSIONS`", section)
        self.assertIn("**79**", section)
        self.assertIn("0/489 JARs", section)
        self.assertIn("0 novas identidades mágicas certificadas", section)
        self.assertIn("**289 dossiês**", self.status)
        self.assertIn("auditoria binária não executada", self.status)

    def test_fourth_pass_manifest_disjoint_and_not_binary_proof(self):
        section = self.cross.split(
            "## Quarto ciclo — vinte dossiês cross-domain adicionais", 1
        )[1].split("## Quinto ciclo — vinte e cinco dossiês cross-domain adicionais", 1)[0]
        ids = [int(x) for x in re.findall(r"^\| #(\d{3}) \|", section, re.MULTILINE)]
        self.assertEqual(
            [96, 102, 125, 147, 153, 175, 206, 223, 262, 263,
             269, 290, 415, 418, 426, 460, 516, 560, 578, 580],
            ids,
        )
        self.assertEqual(20, len(set(ids)))
        prior_category = {121, 334, 404, 395, 320, 335, 464, 71, 74, 84,
                          193, 260, 321, 371, 433, 452, 568}
        self.assertFalse(prior_category.intersection(ids))
        manifest = json.loads(
            (QA / "nonmagic_physical_manifest_2026-10-08.json").read_text(encoding="utf-8")
        )
        rows = {row["physical_number"]: row for row in manifest["rows"]}
        self.assertEqual(489, len(rows))
        self.assertEqual(96, sum(
            row["triage_group"] == "RPG_GEAR_MOBS_DIMENSIONS"
            for row in rows.values()
        ))
        self.assertTrue(all(
            rows[number]["triage_group"] == "RPG_GEAR_MOBS_DIMENSIONS"
            for number in ids
        ))
        self.assertIn("**48 dossiês individuais**", section)
        self.assertIn("**37/96**", section)
        self.assertIn("**59/96**", section)
        self.assertIn("**0/489 JARs inspecionados na instância", section)
        self.assertIn("**0 novas magias promovidas**", section)
        self.assertIn("**289 dossiês**", self.status)
        self.assertIn("auditoria binária não executada", self.status)
        self.assertIn("0 novas provas binary-exact", self.status)

    def test_fifth_pass_disjoint_and_denominator_open(self):
        section = self.cross.split(
            "## Quinto ciclo — vinte e cinco dossiês cross-domain adicionais", 1
        )[1].split("## Sexto ciclo — trinta e quatro dossiês cross-domain adicionais", 1)[0]
        ids = [int(x) for x in re.findall(r"^\| #(\d{3}) \|", section, re.MULTILINE)]
        expected = [
            17, 27, 28, 62, 73, 89, 93, 116, 117, 133, 140, 145, 146,
            154, 159, 163, 174, 177, 189, 198, 211, 238, 239, 240, 243,
        ]
        self.assertEqual(expected, ids)
        self.assertEqual(25, len(set(ids)))

        second = {121, 334, 404, 395, 320, 335, 464}
        third = {71, 74, 84, 193, 260, 321, 371, 433, 452, 568}
        fourth = {96, 102, 125, 147, 153, 175, 206, 223, 262,
                  263, 269, 290, 415, 418, 426, 460, 516, 560, 578, 580}
        all_reviewed = second | third | fourth | set(ids)
        self.assertEqual(62, len(all_reviewed))
        self.assertFalse((second | third | fourth).intersection(ids))

        manifest = json.loads(
            (QA / "nonmagic_physical_manifest_2026-10-08.json").read_text(encoding="utf-8")
        )
        rows = {x["physical_number"]: x for x in manifest["rows"]}
        self.assertEqual(489, len(rows))
        self.assertEqual(96, sum(x["triage_group"] == "RPG_GEAR_MOBS_DIMENSIONS"
                                 for x in rows.values()))
        self.assertTrue(all(
            rows[n]["triage_group"] == "RPG_GEAR_MOBS_DIMENSIONS"
            for n in all_reviewed
        ))
        self.assertEqual(34, 96 - len(all_reviewed))

        self.assertIn("**73 dossiês individuais**", section)
        self.assertIn("**62/96**", section)
        self.assertIn("**34/96**", section)
        self.assertIn("**0/489 JARs", section)
        self.assertIn("0 novos spell/ritual IDs certificados", section)
        self.assertIn("**289 dossiês**", self.status)
        self.assertIn("auditoria binária não executada", self.status)
        self.assertIn("0 novas provas binary-exact", self.status)

    def test_sixth_pass_finishes_category_dossiers_without_binary_promotion(self):
        section = self.cross.split(
            "## Sexto ciclo — trinta e quatro dossiês cross-domain adicionais", 1
        )[1].split("## Candidatos lexicais, estado por linha física", 1)[0]
        matches = list(re.finditer(
            r"^\| #(\d{3}) \| \[[^\]]+\]\((https://[^)]+)\) \|",
            section, re.MULTILINE,
        ))
        ids = [int(m.group(1)) for m in matches]
        expected = [
            252, 254, 255, 282, 292, 332, 354, 356, 369, 379, 380,
            385, 390, 413, 421, 422, 423, 424, 459, 463, 506, 507,
            523, 541, 546, 549, 561, 577, 579, 581, 582, 583, 584, 586,
        ]
        self.assertEqual(expected, ids)
        self.assertEqual(34, len(set(ids)))
        sibling_pin = (
            "Gustavaopere/neoforge-rpg-skilltree/blob/"
            "de80b186357cad20ba5b81892a8682777e96e35a/"
            "PROJECT-INSTRUCTIONS/modlist/"
        )
        self.assertTrue(all(sibling_pin in m.group(2) for m in matches))

        manifest = json.loads(
            (QA / "nonmagic_physical_manifest_2026-10-08.json").read_text(encoding="utf-8")
        )
        category = {
            x["physical_number"] for x in manifest["rows"]
            if x["triage_group"] == "RPG_GEAR_MOBS_DIMENSIONS"
        }
        self.assertEqual(96, len(category))
        prior = {
            121, 334, 404, 395, 320, 335, 464,
            71, 74, 84, 193, 260, 321, 371, 433, 452, 568,
            96, 102, 125, 147, 153, 175, 206, 223, 262, 263, 269,
            290, 415, 418, 426, 460, 516, 560, 578, 580,
            17, 27, 28, 62, 73, 89, 93, 116, 117, 133, 140, 145,
            146, 154, 159, 163, 174, 177, 189, 198, 211, 238, 239,
            240, 243,
        }
        self.assertEqual(62, len(prior))
        self.assertFalse(prior.intersection(ids))
        self.assertEqual(category, prior | set(ids))

        self.assertIn("**96/96**", section)
        self.assertIn("**107 dossiês individuais**", section)
        self.assertIn("**347/347 JARs sem revisão", section)
        self.assertIn("**0/489 JARs", section)
        self.assertIn("0 novas magias certificadas", section)
        self.assertIn("**289 dossiês**", self.status)
        self.assertIn("142/142 candidatos priorizados", self.status)
        self.assertIn("auditoria binária não executada", self.status)
        self.assertIn("0 novas provas binary-exact", self.status)

    def test_other_first_pass_dossiers_are_manifest_pinned_not_spell_proof(self):
        section = self.other.split(
            "## Primeiro lote — 32 dossiês individuais do grupo ", 1
        )[1].split("## Limites de autoridade e próximos gates", 1)[0]
        rows = list(re.finditer(
            r"^\| #(\d{3}) \| \[[^\]]+\]\((https://[^)]+)\) \|",
            section, re.MULTILINE,
        ))
        ids = [int(m.group(1)) for m in rows]
        expected = [
            12, 16, 66, 76, 105, 106, 118, 124, 127, 132, 136,
            151, 164, 172, 194, 196, 197, 200, 203, 218, 242, 244,
            267, 286, 348, 434, 514, 531, 533, 542, 543, 551,
        ]
        self.assertEqual(expected, ids)
        self.assertEqual(32, len(set(ids)))

        sibling_prefix = (
            "https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/"
            "de80b186357cad20ba5b81892a8682777e96e35a/"
            "PROJECT-INSTRUCTIONS/modlist/"
        )
        self.assertTrue(all(m.group(2).startswith(sibling_prefix) for m in rows))

        manifest = json.loads(
            (QA / "nonmagic_physical_manifest_2026-10-08.json").read_text(encoding="utf-8")
        )
        all_rows = {r["physical_number"]: r for r in manifest["rows"]}
        other = {n for n, row in all_rows.items()
                 if row["triage_group"] == "OTHER"}
        self.assertEqual(347, len(other))
        self.assertTrue(set(ids).issubset(other))
        self.assertEqual(315, len(other - set(ids)))

        self.assertIn("**32/347 `OTHER` lidos individualmente**", self.other)
        self.assertIn("**315/347 `OTHER` ainda sem revisão individual**", self.other)
        self.assertIn("**139 dossiês cross-domain individualmente revisados**", self.other)
        self.assertIn("**0/489 JARs", self.other)
        self.assertIn("0 novas identidades de spell certificadas", self.other)
        self.assertIn("**289 dossiês**", self.status)
        self.assertIn("165/347 sem leitura individual", self.status)
        self.assertIn("auditoria binária não executada", self.status)
        self.assertIn("AUDITORIA-OTHER-2026-10-09.md", self.cross)
        self.assertIn("0 novas provas binary-exact", self.status)

    def test_other_second_pass_dossiers_are_disjoint_and_not_registry_proof(self):
        first = self.other.split(
            "## Primeiro lote — 32 dossiês individuais do grupo", 1
        )[1].split("## Limites de autoridade e próximos gates", 1)[0]
        section = self.other.split(
            "## Segundo lote — trinta dossiês adicionais do grupo", 1
        )[1].split("### Reconciliação e portas abertas no segundo lote", 1)[0]
        pattern = r"^\| #(\d{3}) \| \[[^\]]+\]\((https://[^)]+)\) \|"
        first_ids = [int(x) for x in re.findall(
            r"^\| #(\d{3}) \|", first, re.MULTILINE
        )]
        matches = list(re.finditer(pattern, section, re.MULTILINE))
        ids = [int(m.group(1)) for m in matches]
        self.assertEqual(32, len(first_ids))
        self.assertEqual(30, len(ids))
        self.assertEqual(30, len(set(ids)))
        self.assertFalse(set(first_ids).intersection(ids))
        self.assertEqual([
            5, 7, 10, 11, 13, 14, 15, 19, 20, 26, 65, 86, 130, 143,
            179, 212, 241, 259, 308, 341, 362, 363, 364, 365, 378,
            386, 388, 427, 439, 453,
        ], ids)
        sibling = (
            "https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/"
            "de80b186357cad20ba5b81892a8682777e96e35a/"
            "PROJECT-INSTRUCTIONS/modlist/"
        )
        self.assertTrue(all(m.group(2).startswith(sibling) for m in matches))
        manifest = json.loads(
            (QA / "nonmagic_physical_manifest_2026-10-08.json").read_text(encoding="utf-8")
        )
        other = {x["physical_number"] for x in manifest["rows"]
                 if x["triage_group"] == "OTHER"}
        self.assertEqual(347, len(other))
        self.assertTrue((set(first_ids) | set(ids)).issubset(other))
        self.assertEqual(62, len(set(first_ids) | set(ids)))
        self.assertEqual(285, len(other - set(first_ids) - set(ids)))

        self.assertIn("**62/347 dossiês individualmente lidos**", self.other)
        self.assertIn("**285/347 ainda sem leitura individual**", self.other)
        self.assertIn("**169** dossiês", self.other)
        self.assertIn("0 novas identidades de spell certificadas", self.other)
        self.assertIn("0/489 JARs", self.other)
        self.assertIn("**289 dossiês**", self.status)
        self.assertIn("165/347 sem leitura individual", self.status)
        self.assertIn("182/347", self.cross)
        self.assertIn("**289 dossiês individuais**", (
            META / "CATALOGO-GLOBAL-MAGIAS.md"
        ).read_text(encoding="utf-8"))
        self.assertIn("0 novas provas binary-exact", self.status)

    def test_other_third_pass_completes_92_documentary_dossiers_without_registry_proof(self):
        pattern = r"^\| #(\d{3}) \| \[.+?\]\((https://[^)]+)\) \|"
        first = self.other.split(
            "## Primeiro lote — 32 dossiês individuais do grupo", 1
        )[1].split("## Limites de autoridade e próximos gates", 1)[0]
        second = self.other.split(
            "## Segundo lote — trinta dossiês adicionais do grupo", 1
        )[1].split("### Reconciliação e portas abertas no segundo lote", 1)[0]
        third = self.other.split(
            "## Terceiro lote — trinta dossiês adicionais do grupo", 1
        )[1].split("### Reconciliação e gates do terceiro lote", 1)[0]

        old_ids = [int(m.group(1)) for section in (first, second)
                   for m in re.finditer(pattern, section, re.MULTILINE)]
        rows = list(re.finditer(pattern, third, re.MULTILINE))
        ids = [int(m.group(1)) for m in rows]
        expected = [
            6, 8, 18, 22, 25, 37, 59, 60, 68, 83,
            94, 112, 123, 135, 155, 161, 181, 199, 298, 350,
            375, 384, 405, 428, 67, 75, 77, 85, 90, 95,
        ]
        self.assertEqual(expected, ids)
        self.assertEqual(62, len(old_ids))
        self.assertEqual(30, len(set(ids)))
        self.assertFalse(set(old_ids).intersection(ids))
        self.assertEqual(92, len(set(old_ids) | set(ids)))

        sibling = (
            "https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/"
            "de80b186357cad20ba5b81892a8682777e96e35a/"
            "PROJECT-INSTRUCTIONS/modlist/"
        )
        self.assertTrue(all(m.group(2).startswith(sibling) for m in rows))
        manifest = json.loads(
            (QA / "nonmagic_physical_manifest_2026-10-08.json").read_text(encoding="utf-8")
        )
        other = {m["physical_number"] for m in manifest["rows"]
                 if m["triage_group"] == "OTHER"}
        self.assertEqual(347, len(other))
        reviewed = set(old_ids) | set(ids)
        self.assertTrue(reviewed.issubset(other))
        self.assertEqual(255, len(other - reviewed))

        self.assertIn("92/347 dossiês", self.other)
        self.assertIn("**255/347 ainda sem leitura individual**", self.other)
        self.assertIn("**199 dossiês cross-domain individualmente revisados**", self.other)
        self.assertIn("0 novas identidades de spell certificadas", self.other)
        self.assertIn("0/489 JARs", self.other)
        self.assertIn("**289 dossiês**", self.status)
        self.assertIn("165/347 sem leitura individual", self.status)
        self.assertIn("182/347", self.cross)
        self.assertIn("**289 dossiês individuais**", (
            META / "CATALOGO-GLOBAL-MAGIAS.md"
        ).read_text(encoding="utf-8"))
        self.assertIn("0 novas provas binary-exact", self.status)

    def test_other_fourth_pass_is_unique_and_preserves_real_registry_gates(self):
        pattern = r"^\| #(\d{3}) \| \[.+?\]\((https://[^)]+)\) \|"
        anchors = [
            ("## Primeiro lote — 32 dossiês individuais do grupo",
             "## Limites de autoridade e próximos gates"),
            ("## Segundo lote — trinta dossiês adicionais do grupo",
             "### Reconciliação e portas abertas no segundo lote"),
            ("## Terceiro lote — trinta dossiês adicionais do grupo",
             "### Reconciliação e gates do terceiro lote"),
            ("## Quarto lote — trinta dossiês adicionais do grupo",
             "### Contagem e gates do quarto lote"),
        ]
        sections = [self.other.split(start, 1)[1].split(end, 1)[0]
                    for start, end in anchors]
        matches = [list(re.finditer(pattern, s, re.MULTILINE))
                   for s in sections]
        ids = [[int(m.group(1)) for m in batch] for batch in matches]
        self.assertEqual([32, 30, 30, 30], [len(batch) for batch in ids])
        expected = [
            119, 122, 131, 148, 150, 156, 157, 162, 165, 167,
            169, 170, 171, 187, 192, 205, 226, 227, 228, 229,
            230, 231, 234, 235, 236, 261, 264, 302, 367, 387,
        ]
        self.assertEqual(expected, ids[3])
        all_ids = [n for batch in ids for n in batch]
        self.assertEqual(122, len(all_ids))
        self.assertEqual(122, len(set(all_ids)))

        prefix = (
            "https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/"
            "de80b186357cad20ba5b81892a8682777e96e35a/"
            "PROJECT-INSTRUCTIONS/modlist/"
        )
        self.assertTrue(all(m.group(2).startswith(prefix)
                            for batch in matches for m in batch))
        manifest = json.loads(
            (QA / "nonmagic_physical_manifest_2026-10-08.json").read_text(encoding="utf-8")
        )
        other = {row["physical_number"] for row in manifest["rows"]
                 if row["triage_group"] == "OTHER"}
        self.assertEqual(347, len(other))
        self.assertTrue(set(all_ids).issubset(other))
        self.assertEqual(225, len(other - set(all_ids)))

        self.assertIn("122/347 dossiês", self.other)
        self.assertIn("**225/347 ainda sem leitura individual**", self.other)
        self.assertIn("**229 dossiês cross-domain individualmente revisados**", self.other)
        self.assertIn("0 novos spell/ritual IDs certificados", self.other)
        self.assertIn("0/489 JARs", self.other)
        self.assertIn("**289 dossiês**", self.status)
        self.assertIn("165/347 sem leitura individual", self.status)
        self.assertIn("182/347", self.cross)
        self.assertIn("**289 dossiês individuais**", (
            META / "CATALOGO-GLOBAL-MAGIAS.md"
        ).read_text(encoding="utf-8"))
        self.assertIn("0 novas provas binary-exact", self.status)

    def test_other_fifth_pass_152_unique_pinned_dossiers_and_no_magic_promotion(self):
        pattern = r"^\| #(\d{3}) \| \[.+?\]\((https://[^)]+)\) \|"
        anchors = [
            ("## Primeiro lote — 32 dossiês individuais do grupo",
             "## Limites de autoridade e próximos gates"),
            ("## Segundo lote — trinta dossiês adicionais do grupo",
             "### Reconciliação e portas abertas no segundo lote"),
            ("## Terceiro lote — trinta dossiês adicionais do grupo",
             "### Reconciliação e gates do terceiro lote"),
            ("## Quarto lote — trinta dossiês adicionais do grupo",
             "### Contagem e gates do quarto lote"),
            ("## Quinto lote — trinta dossiês adicionais do grupo",
             "### Contagem e gates do quinto lote"),
        ]
        sections = [self.other.split(a, 1)[1].split(b, 1)[0]
                    for a, b in anchors]
        matches = [list(re.finditer(pattern, s, re.MULTILINE))
                   for s in sections]
        groups = [[int(m.group(1)) for m in group] for group in matches]
        self.assertEqual([32, 30, 30, 30, 30], [len(g) for g in groups])
        self.assertEqual([
            109, 111, 115, 126, 128, 129, 134, 137, 138, 139,
            142, 144, 152, 158, 160, 168, 173, 178, 185, 186,
            188, 190, 191, 195, 201, 202, 204, 207, 209, 210,
        ], groups[4])
        all_ids = [n for g in groups for n in g]
        self.assertEqual(152, len(all_ids))
        self.assertEqual(152, len(set(all_ids)))

        sibling = (
            "https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/"
            "de80b186357cad20ba5b81892a8682777e96e35a/"
            "PROJECT-INSTRUCTIONS/modlist/"
        )
        self.assertTrue(all(m.group(2).startswith(sibling)
                            for g in matches for m in g))
        manifest = json.loads(
            (QA / "nonmagic_physical_manifest_2026-10-08.json").read_text(encoding="utf-8")
        )
        other = {r["physical_number"] for r in manifest["rows"]
                 if r["triage_group"] == "OTHER"}
        self.assertEqual(347, len(other))
        self.assertTrue(set(all_ids).issubset(other))
        self.assertEqual(195, len(other - set(all_ids)))

        self.assertIn("152/347 dossiês", self.other)
        self.assertIn("**195/347 ainda sem leitura individual**", self.other)
        self.assertIn("**259 dossiês cross-domain individualmente revisados**", self.other)
        self.assertIn("0 novos spell/ritual IDs certificados", self.other)
        self.assertIn("0/489 JARs", self.other)
        self.assertIn("**289 dossiês**", self.status)
        self.assertIn("165/347 sem leitura individual", self.status)
        self.assertIn("182/347", self.cross)
        self.assertIn("**289 dossiês individuais**", (
            META / "CATALOGO-GLOBAL-MAGIAS.md"
        ).read_text(encoding="utf-8"))
        self.assertIn("0 novas provas binary-exact", self.status)

    def test_other_sixth_pass_disjoint_source_pinned_and_not_binary_proof(self):
        anchors = re.findall(
            r"^\\| #(\\d{3}) \\| \\[.+?\\]\\((https://[^)]+)\\) \\|",
            self.sixth, re.MULTILINE,
        )
        expected = [
            24, 39, 57, 58, 61, 64, 69, 70, 72, 78, 80, 92, 98,
            99, 101, 103, 107, 108, 110, 113, 114, 176, 180,
            213, 217, 224, 233, 237, 247, 248,
        ]
        found = [int(n) for n, _ in anchors]
        self.assertEqual(expected, found)
        sibling_prefix = (
            "https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/"
            "de80b186357cad20ba5b81892a8682777e96e35a/"
        )
        self.assertTrue(all(url.startswith(sibling_prefix) for _, url in anchors))
        previous = {int(n) for n in re.findall(
            r"^\\| #(\\d{3}) \\|", self.other, re.MULTILINE,
        )}
        self.assertEqual(152, len(previous))
        self.assertTrue(previous.isdisjoint(found))
        manifest = json.loads(
            (QA / "nonmagic_physical_manifest_2026-10-08.json").read_text(encoding="utf-8")
        )
        other = {r["physical_number"] for r in manifest["rows"]
                 if r["triage_group"] == "OTHER"}
        self.assertEqual(347, len(other))
        self.assertTrue(set(found).issubset(other))
        self.assertEqual(182, len(previous | set(found)))
        self.assertEqual(165, len(other - previous - set(found)))
        self.assertIn("**182/347**", self.sixth)
        self.assertIn("**289** dossiês", self.sixth)
        self.assertIn("0/489 JARs", self.sixth)
        self.assertIn("nenhuma", self.sixth.lower())

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
