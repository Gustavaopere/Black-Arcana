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

    def test_gtbcs_spell_cards_match_release_registry_without_minting_extra_spells(self):
        geomancy = PROVIDERS / "✅-gtbcs-geomancy-plus"
        readme = (geomancy / "README.md").read_text(encoding="utf-8")
        roster = readme.split("## Exact semantic spell inventory", 1)[1].split(
            "## Explicit exclusions", 1
        )[0]
        registry = re.findall(
            r"^[|] (Geo|Holy) [|] `([a-z_]+)` [|] `([A-Za-z]+)` [|]$",
            roster,
            re.MULTILINE,
        )
        self.assertEqual(12, len(registry), "expected pinned release inventory")
        self.assertEqual(12, len({identifier for _, identifier, _ in registry}))

        cards = (geomancy / "SPELL-CARDS-1.1.0-1.21.1.md").read_text(encoding="utf-8")
        headings = list(re.finditer(
            r"^### ([0-9]{2}) — `gtbcs_geomancy_plus:([a-z_]+)`$",
            cards,
            re.MULTILINE,
        ))
        self.assertEqual(12, len(headings), "one individual card per registered spell")
        self.assertEqual([f"{i:02d}" for i in range(1, 13)],
                         [match.group(1) for match in headings])
        self.assertEqual(
            {identifier for _, identifier, _ in registry},
            {match.group(2) for match in headings},
            "cards cannot omit or fabricate provider-owned IDs",
        )
        for idx, header in enumerate(headings):
            body = cards[header.end():(
                headings[idx + 1].start() if idx + 1 < len(headings) else len(cards)
            )]
            expected = next(row for row in registry if row[1] == header.group(2))
            school, _identifier, concrete = expected
            self.assertIn(f"- **Família confirmada:** {school}", body)
            self.assertIn(f"- **Classe concreta:** `{concrete}`", body)
            self.assertIn("**Confiança:** `COUNTED_RELEASE_BOUNDED`", body)
        self.assertIn("EarthshatterSpell", cards)
        self.assertIn("Earthquake", cards)
        self.assertIn("Stomp", cards)
        self.assertIn("12/12", cards)
        self.assertIn("sem validação física", cards)

    def test_leyline_cards_match_exact_fourteen_registry_roots(self):
        provider = PROVIDERS / "✅-leyline-spellbooks"
        inventory = (provider / "EXACT-1.0.3-SPELL-INVENTORY.md").read_text(
            encoding="utf-8"
        )
        rows = re.findall(
            r"^\| (\d+) \| \x60([A-Z_]+)\x60 \| \x60([A-Za-z]+)\x60 \| "
            r"\x60leylines:([a-z_]+)\x60 \|$",
            inventory,
            re.MULTILINE,
        )
        self.assertEqual(14, len(rows))
        self.assertEqual([str(i) for i in range(1, 15)], [row[0] for row in rows])
        self.assertEqual(14, len({row[3] for row in rows}))
        all_pages = sorted((provider / "spells").glob("*.md"))
        self.assertEqual(14, len(all_pages), "one page per exact provider spell")

        index = (provider / "SPELL-CARDS-1.0.3.md").read_text(encoding="utf-8")
        self.assertIn("14/14", index)
        self.assertIn("1.851 / 1.849", index)
        self.assertIn("Total semântico neste trabalho: +0", index)
        self.assertIn("⚠️ QA condicionado", index)
        for _n, field, klass, ident in rows:
            slug = "eclipse" if ident == "ley_eclipse" else ident.replace("_", "-")
            path = provider / "spells" / (slug + ".md")
            self.assertTrue(path.is_file(), f"missing individual card {ident}")
            page = path.read_text(encoding="utf-8")
            self.assertIn(f"**Registry ID:** \x60leylines:{ident}\x60", page)
            self.assertIn(f"**Classe exata:** \x60{klass}\x60", page)
            self.assertIn(f"campo \x60{field}\x60", page)
            self.assertIn("COUNTED_EXACT", page)
            self.assertIn(f"(spells/{path.name})", index)
            self.assertIn(f"\x60leylines:{ident}\x60", index)
        readme = (provider / "README.md").read_text(encoding="utf-8")
        self.assertIn("SPELL-CARDS-1.0.3.md", readme)

    def test_monsters_spellbooks_ninety_eight_source_cards(self):
        provider = PROVIDERS / "✅-monsters-spellbooks"
        inventory = (provider / "SPELL-CATALOG.md").read_text(encoding="utf-8")
        recorded = re.findall(
            r"^\| (\d+) \| `([a-z]+)` \| `([A-Z_]+)` \| `([A-Za-z]+)` \| "
            r"`registered in ModSpellRegistry` \|$",
            inventory, re.MULTILINE,
        )
        self.assertEqual(98, len(recorded), "source registry should have 98")
        self.assertEqual([str(i) for i in range(1, 99)],
                         [entry[0] for entry in recorded])
        self.assertEqual(98, len({e[2] for e in recorded}))

        cards = (provider / "SPELL-CARDS-RELEASE-INTERVAL-0.0.16.3.md").read_text(
            encoding="utf-8"
        )
        headings = list(re.finditer(
            r"^### (\d{2}) — `([A-Z_]+)`$", cards, re.MULTILINE
        ))
        self.assertEqual(98, len(headings))
        self.assertEqual(
            [(f"{int(n):02d}", field) for n, _, field, _ in recorded],
            [(m.group(1), m.group(2)) for m in headings],
        )
        expected_families = {
            "blood": 5, "ender": 12, "evocation": 3, "fire": 10,
            "holy": 4, "hydro": 8, "ice": 8, "lightning": 14,
            "nature": 7, "necro": 25, "technomancy": 2,
        }
        for family, count in expected_families.items():
            self.assertEqual(count, sum(1 for _, f, _, _ in recorded if f == family))
        for idx, (_n, family, field, klass) in enumerate(recorded):
            end = (headings[idx + 1].start() if idx + 1 < len(headings)
                   else cards.index("## Exclusões e limites finais"))
            page = cards[headings[idx].end():end]
            self.assertIn(f"**Família organizacional na fonte:** `{family}`", page)
            self.assertIn(f"**Constante em `ModSpellRegistry`:** `{field}`", page)
            self.assertIn(f"**Classe da fonte pública:** `{klass}`", page)
            self.assertIn("**Registry ID físico 0.0.16.3:** `NÃO VERIFICADO`", page)
            self.assertIn("COUNTED_RELEASE_BOUNDED", page)
        self.assertIn("98/98 fichas", cards)
        self.assertIn("**+0 novas identidades**", cards)
        self.assertIn("**NÃO é um build pin exato**", cards)
        self.assertIn("`aero` = **0 registros**", cards)
        self.assertIn("fichas source-observed / ⚠️ registry físico", self.index)
        readme = (provider / "README.md").read_text(encoding="utf-8")
        self.assertIn("SPELL-CARDS-RELEASE-INTERVAL-0.0.16.3.md", readme)

    def test_bloodlines_29_action_cards_keep_source_contract_and_exclusion(self):
        provider = PROVIDERS / "✅-bloodlines"
        source = (provider / "ACTION-CATALOG.md").read_text(encoding="utf-8")
        actions = list(re.finditer(
            r"^## ([^\n]+?) — `bloodlines:([a-z_]+)`$", source, re.MULTILINE
        ))
        self.assertEqual(29, len(actions))
        self.assertEqual(29, len({m.group(2) for m in actions}))
        groups = {"Noble": 5, "Zealot": 4, "Ectotherm": 3,
                  "Bloodknight": 5, "Gravebound": 12}
        index = (provider / "ACTION-CARDS-3.0.9.md").read_text(encoding="utf-8")
        pages = sorted((provider / "actions").glob("*.md"))
        self.assertEqual(29, len(pages))
        checked = {key: 0 for key in groups}
        counted = 0
        excluded = 0
        for match in actions:
            name, ident = match.group(1), match.group(2)
            prev = source[:match.start()]
            group_matches = list(re.finditer(
                r"^# (Noble|Zealot|Ectotherm|Bloodknight|Gravebound) actions$",
                prev, re.MULTILINE,
            ))
            self.assertTrue(group_matches, ident)
            group = group_matches[-1].group(1)
            checked[group] += 1
            slug = ident.replace("_", "-")
            path = provider / "actions" / (slug + ".md")
            self.assertTrue(path.is_file(), ident)
            card = path.read_text(encoding="utf-8")
            self.assertIn(f"# {name} — Bloodlines 3.0.9", card)
            self.assertIn(f"**Registry ID:** `bloodlines:{ident}`", card)
            self.assertIn(f"**Bloodline:** `{group}`", card)
            self.assertIn("IAction", card)
            self.assertIn("ACTION-CATALOG.md", card)
            self.assertIn(f"`bloodlines:{ident}`", index)
            self.assertIn(f"(actions/{slug}.md)", index)
            tail = source[match.end():]
            boundary = re.search(r"^#{1,2} ", tail, re.MULTILINE)
            original = (tail[:boundary.start()] if boundary else tail).strip()
            self.assertIn(original, card,
                          f"source detail drift for bloodlines:{ident}")
            if ident == "gravebound_crit_action":
                self.assertIn("EXCLUDED (+0)", card)
                self.assertIn("SEM AQUISIÇÃO NORMAL COMPROVADA", card)
                excluded += 1
            else:
                self.assertIn("COUNTED_SOURCE_PINNED", card)
                self.assertNotIn("EXCLUDED (+0)", card)
                counted += 1
        self.assertEqual(groups, checked)
        self.assertEqual((28, 1), (counted, excluded))
        self.assertIn("29/29 registros individualizados", index)
        self.assertIn("Materialização de fichas = **+0 identidades novas**", index)
        self.assertIn("ACTION-CARDS-3.0.9.md", self.index)
        self.assertIn("ACTION-CARDS-3.0.9.md",
                      (provider / "README.md").read_text(encoding="utf-8"))
        self.assertIn("ACTION-CARDS-3.0.9.md",
                      (provider / "MAGIAS.md").read_text(encoding="utf-8"))

    def test_goety_exact_123_focus_cards_crosswalk(self):
        provider = PROVIDERS / "✅-goety"
        inventory = (provider / "EXACT-3.1.4-SEMANTIC-INVENTORY.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("## Exact Focus actions — 123", inventory)
        self.assertIn("## Exact non-Focus ritual actions — 238", inventory)
        subset = inventory.split("## Exact Focus actions — 123", 1)[1].split(
            "## Exact non-Focus ritual actions — 238", 1
        )[0]
        registered = re.findall(r"^- `([a-z_]+_focus)`$", subset, re.MULTILINE)
        self.assertEqual(123, len(registered))
        self.assertEqual(123, len(set(registered)))
        self.assertNotIn("empty_focus", registered)
        pages = sorted((provider / "focuses").glob("*-focus.md"))
        self.assertEqual(123, len(pages), "one page per exact 3.1.4 Focus")
        index = (provider / "FOCUS-CARDS-3.1.4.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("123/123", index)
        self.assertIn("**+0 novas identidades semânticas**", index)
        self.assertIn("80 `goety:ritual` / 43 shaped", index)
        self.assertIn("238 rituais não-Focus", index)
        self.assertIn("a0770e180e4e8b1b87d8fa9c8356e9dbf34d82a7", index)
        for ordinal, ident in enumerate(registered, start=1):
            slug = ident.replace("_", "-")
            path = provider / "focuses" / (slug + ".md")
            self.assertTrue(path.is_file(), f"missing Focus {ident}")
            page = path.read_text(encoding="utf-8")
            self.assertIn(f"# Goety 3.1.4 — `{ident}`", page)
            self.assertIn(f"**Identidade de Focus no artefato:** `{ident}`", page)
            self.assertIn(f"**Posição no inventário exato:** {ordinal}/123", page)
            self.assertIn("COUNTED_EXACT", page)
            self.assertIn("**NÃO VERIFICADO nesta ficha**", page)
            self.assertIn("Não é o `empty_focus` proxy", page)
            self.assertIn(f"| {ordinal} | `{ident}` | [Abrir](focuses/{slug}.md) |", index)
        self.assertFalse((provider / "focuses" / "empty-focus.md").exists())
        for filename in ("README.md", "FOCUS-CATALOG.md", "focuses/README.md"):
            self.assertIn("FOCUS-CARDS-3.1.4.md",
                          (provider / filename).read_text(encoding="utf-8"))
        self.assertIn("FOCUS-CARDS-3.1.4.md", self.index)
        self.assertIn("1.851 global / 1.849 no escopo solicitado", index)

    def test_goety_exact_238_nonfocus_ritual_cards(self):
        provider = PROVIDERS / "✅-goety"
        source = (provider / "EXACT-3.1.4-SEMANTIC-INVENTORY.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("## Exact non-Focus ritual actions — 238", source)
        subset = source.split("### Counted ritual identities", 1)[1]
        records = re.findall(
            r"^- `([^`]+\.json)` → `([^`]+)` \(`([A-Z_]+)`, `([a-z_]+)`\)$",
            subset, re.MULTILINE,
        )
        self.assertEqual(238, len(records))
        self.assertEqual(238, len({row[0] for row in records}))
        self.assertEqual(238, len({row[1] for row in records}))
        expected_classes = {
            "OTHER_RITUAL": 123, "CONVERSION_RITUAL": 23,
            "ENCHANT_RITUAL": 37, "LOCATE_RITUAL": 19,
            "SUMMON_RITUAL": 2, "THRALL_SUMMON_RITUAL": 34,
        }
        expected_crafts = {
            "deep": 9, "geoturgy": 15, "animation": 3, "forge": 47,
            "end": 7, "expert_nether": 13, "necroturgy": 36,
            "overgrown": 11, "adept_nether": 8, "magic": 48,
            "storm": 8, "frost": 4, "sky": 9,
            "divination": 19, "sabbath": 1,
        }
        for name, count in expected_classes.items():
            self.assertEqual(count, sum(1 for r in records if r[2] == name))
        for name, count in expected_crafts.items():
            self.assertEqual(count, sum(1 for r in records if r[3] == name))
        cards_root = provider / "rituals" / "cards"
        pages = sorted(cards_root.rglob("*.md"))
        self.assertEqual(238, len(pages))
        index = (provider / "RITUAL-CARDS-3.1.4.md").read_text(
            encoding="utf-8"
        )
        for ordinal, (resource, signature, family, craft) in enumerate(records, 1):
            relative = resource[:-5] + ".md"
            path = cards_root / relative
            self.assertTrue(path.is_file(), resource)
            card = path.read_text(encoding="utf-8")
            self.assertIn(f"# Goety 3.1.4 — ritual `{resource}`", card)
            self.assertIn(f"**Recurso de receita no inventário do JAR:** `{resource}`", card)
            self.assertIn(f"**Assinatura semântica auditada:** `{signature}`", card)
            self.assertIn(f"**Classe de auditoria:** `{family}`", card)
            self.assertIn(f"**Tipo de crafting de ritual:** `{craft}`", card)
            self.assertIn(f"**Posição editorial:** {ordinal}/238", card)
            self.assertIn("COUNTED_EXACT", card)
            self.assertIn("**NÃO VERIFICADO nesta ficha**", card)
            self.assertIn(f"| {ordinal} | [`{resource}`](rituals/cards/{relative}) |", index)
            for label, canonical in (
                ("Inventário semântico exato", "EXACT-3.1.4-SEMANTIC-INVENTORY.md"),
                ("Auditoria de artefato", "EXACT-3.1.4-ARTIFACT-AUDIT.md"),
                ("Integração", "INTEGRATION-RULES.md"),
            ):
                match = re.search(r"\[" + label + r"\]\(([^)]+)\)", card)
                self.assertIsNotNone(match, (resource, label))
                resolved = (path.parent / match.group(1)).resolve()
                self.assertEqual((provider / canonical).resolve(), resolved)
            if "?->" in signature:
                self.assertIn("origem/input não está certificado", card)
            if signature.startswith("RITUAL_PATH:"):
                self.assertIn("não um resultado ou entity registry ID", card)
        self.assertIn("**238** assinaturas são únicas", index)
        self.assertIn("**+0 novas identidades**", index)
        self.assertIn("**342** recursos", index)
        self.assertIn("**83** recursos", index)
        self.assertIn("**17** rituais", index)
        for filename in ("README.md", "rituals/README.md"):
            self.assertIn("RITUAL-CARDS-3.1.4.md",
                          (provider / filename).read_text(encoding="utf-8"))
        self.assertIn("RITUAL-CARDS-3.1.4.md", self.index)

    def test_goety_cataclysm_28_exact_focus_cards_with_24_ritual_gap(self):
        provider = PROVIDERS / "✅-goety-cataclysm"
        readme = (provider / "README.md").read_text(encoding="utf-8")
        source = readme.split(
            "O provider registra exatamente **28 Focuses próprios**:", 1
        )[1].split("Todos os 28 possuem caminho de aquisição", 1)[0]
        holders = re.findall(r"`([A-Z_]+_FOCUS)`", source)
        self.assertEqual(28, len(holders))
        self.assertEqual(28, len(set(holders)))
        card_files = sorted((provider / "focuses").glob("*.md"))
        self.assertEqual(28, len(card_files))
        index = (provider / "FOCUS-CARDS-1.21.1-1.8.2.md").read_text(
            encoding="utf-8"
        )
        for ordinal, holder in enumerate(holders, 1):
            rel = holder.lower().replace("_", "-") + ".md"
            page = provider / "focuses" / rel
            self.assertTrue(page.is_file(), holder)
            card = page.read_text(encoding="utf-8")
            self.assertIn(f"# Goety Cataclysm 1.21.1-1.8.2 — `{holder}`", card)
            self.assertIn(f"**Focus holder observado:** `{holder}`", card)
            self.assertIn(f"**Posição na lista exata:** {ordinal}/28", card)
            self.assertIn("COUNTED_EXACT", card)
            self.assertIn("**+0 novas identidades**", card)
            self.assertIn("**NÃO VERIFICADO nesta ficha**", card)
            self.assertIn("Qual dessas duas vias pertence a este Focus individual", card)
            self.assertIn(
                f"| {ordinal} | `{holder}` | [Abrir](focuses/{rel}) |",
                index,
            )
            self.assertIn("../EXACT-1.21.1-1.8.2-ARTIFACT-AUDIT.md", card)
        self.assertIn("28/28 fichas", index)
        self.assertIn("**10 conversões + 13 summons/thralls + 1 fabricator**", index)
        self.assertIn("0/24 fichas nominais", index)
        self.assertIn("24 rituais de *aquisição*", index)
        self.assertIn("**+0 novas identidades semânticas**", index)
        self.assertIn("4e3052a082200371b36e1a88fdce05e294d82757", index)
        self.assertIn("52 objetos mágicos", index)
        self.assertIn("FOCUS-CARDS-1.21.1-1.8.2.md", readme)
        self.assertIn("FOCUS-CARDS-1.21.1-1.8.2.md", self.index)
        tech = (provider / "TECHNICAL-AUDIT.md").read_text(encoding="utf-8")
        self.assertIn("## Adendo de autoridade — evidência posterior", tech)
        self.assertIn("24 rituais não-Focus distintos", tech)
        artifact = (provider / "EXACT-1.21.1-1.8.2-ARTIFACT-AUDIT.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("28 addon-owned Focus holders", artifact)
        self.assertIn("24 non-Focus rituals remain", artifact)
        self.assertIn("10 conversion, 13 summon/thrall, 1 fabricator", artifact)

    def test_current_status_does_not_promote_runtime(self):
        self.assertIn("164/164 diretórios", self.index)
        self.assertIn("97/97 dossiês", self.index)
        self.assertIn("denominador semântico final permanece aberto", self.index)
        self.assertIn("COUNTED_RELEASE_BOUNDED", self.cards)
        self.assertIn("não verificados", self.cards)


if __name__ == "__main__":
    unittest.main()
