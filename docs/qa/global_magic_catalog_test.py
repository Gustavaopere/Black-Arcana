#!/usr/bin/env python3
"""Documentation-only checks for the canonical magic-provider catalog index."""
from __future__ import annotations
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROVIDERS = ROOT / "wiki" / "modpack-catalog" / "providers"
GLOBAL = ROOT / "wiki" / "modpack-catalog" / "meta" / "CATALOGO-GLOBAL-MAGIAS.md"
TUNES = PROVIDERS / "✅-tunes-n-tomes"
INDEX_PATTERN = re.compile(
    r"^\| \x60(?P<slug>[^\x60]+)\x60 \| ✅ \| "
    r"\[README\]\(\.\./providers/✅-(?P=slug)/README\.md\)"
    r" \| (?P<scope>Dentro do inventário global|Fora do escopo específico) \|$",
    re.MULTILINE,
)
CARD_PATTERN = re.compile(r"^### (?P<ordinal>\d{2}) (?P<spell>.+)$", re.MULTILINE)
LINK_PATTERN = re.compile(
    r"^\| (?P<ordinal>\d+) \| (?P<spell>[^|]+) \| "
    r"\[Ficha \d{2}\]\(#(?P<anchor>[^)]+)\) \| Publicador / release-bounded \|$",
    re.MULTILINE,
)


class GlobalMagicCatalogTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.index = GLOBAL.read_text(encoding="utf-8")
        cls.actual = {
            p.name[2:] for p in PROVIDERS.iterdir()
            if p.is_dir() and p.name.startswith("✅-")
        }
        cls.rows = [m.groupdict() for m in INDEX_PATTERN.finditer(cls.index)]
        cls.cards = (TUNES / "SPELL-CARDS-1.1.0-HOTFIX.md").read_text(encoding="utf-8")
        cls.readme = (TUNES / "README.md").read_text(encoding="utf-8")

    def test_all_provider_directories_are_uniquely_indexed(self):
        listed = [row["slug"] for row in self.rows]
        self.assertEqual(len(listed), len(set(listed)), "duplicate provider index row")
        self.assertEqual(self.actual, set(listed), "missing or stale provider rows")
        for row in self.rows:
            self.assertTrue(
                (PROVIDERS / ("✅-" + row["slug"]) / "README.md").is_file(),
                row["slug"],
            )

    def test_out_of_scope_is_exactly_two_mod_bases(self):
        excluded = {
            row["slug"] for row in self.rows
            if row["scope"] == "Fora do escopo específico"
        }
        self.assertEqual({"deeper-and-darker", "traveloptics"}, excluded)
        self.assertIn("deeper-and-darker-spellbooks", self.actual)

    def test_tunes_cards_match_all_publisher_named_roster_entries(self):
        roster_section = self.readme.split(
            "## Current publisher roster — 16 semantic spell identities", 1
        )[1].split("\n## ", 1)[0]
        names = re.findall(r"^\d+\. (.+)$", roster_section, re.MULTILINE)
        cards = [m.groupdict() for m in CARD_PATTERN.finditer(self.cards)]
        self.assertEqual(len(names), len(set(names)))
        self.assertEqual(names, [row["spell"] for row in cards])
        self.assertEqual(
            [f"{i:02d}" for i in range(1, len(names) + 1)],
            [row["ordinal"] for row in cards],
        )
        self.assertEqual(16, len(cards))

    def test_tunes_index_links_resolve_to_each_spell_heading(self):
        links = [m.groupdict() for m in LINK_PATTERN.finditer(self.cards)]
        self.assertEqual(16, len(links))
        for i, link in enumerate(links, 1):
            self.assertEqual(i, int(link["ordinal"]))
            expected = (
                f"{i:02d}-" +
                re.sub(r"[^a-z0-9 ]", "", link["spell"].lower()).replace(" ", "-")
            )
            self.assertEqual(expected, link["anchor"])

    def test_current_status_does_not_promote_runtime(self):
        self.assertIn("164/164 diretórios", self.index)
        self.assertIn("97/97 dossiês", self.index)
        self.assertIn("denominador semântico final permanece aberto", self.index)
        self.assertIn("COUNTED_RELEASE_BOUNDED", self.cards)
        self.assertIn("não verificados", self.cards)


if __name__ == "__main__":
    unittest.main()
