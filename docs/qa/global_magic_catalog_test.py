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
            self.assertIn("**Confiança atual:** `COUNTED_EXACT`", body)
            self.assertIn("sem comprovação de gameplay, config ou Survival", body)
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
            self.assertIn("**Rota de aquisição atribuída:**", card)
            self.assertIn(
                f"| {ordinal} | `{holder}` | [Abrir](focuses/{rel}) |",
                index,
            )
            self.assertIn("../EXACT-1.21.1-1.8.2-ARTIFACT-AUDIT.md", card)
        self.assertIn("28/28 fichas", index)
        self.assertIn("**10 conversões + 13 summons/thralls + 1 fabricator**", index)
        self.assertIn("24/24 fichas nominais", index)
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

    def test_goety_cataclysm_exact_48_recipe_matrix_24_ritual_cards(self):
        provider = PROVIDERS / "✅-goety-cataclysm"
        text = (provider / "RITUAL-INVENTORY-EXACT-1.21.1-1.8.2.md").read_text(
            encoding="utf-8"
        )
        rows = re.findall(
            r"^\| (\d+) \| \x60(data/goety_cataclysm/recipe/[a-z0-9_./]+\.json)\x60 "
            r"\| \x60(goety:[a-z0-9_]+)\x60 \| (.*?) "
            r"\| \x60([a-z0-9_:/]+)\x60 \| \x60\[\]\x60 "
            r"\| \x60(FOCUS_ACQUISITION_DEDUP|COUNTED_EXACT)\x60 \|$",
            text, re.MULTILINE,
        )
        self.assertEqual(48, len(rows))
        self.assertEqual([str(i) for i in range(1, 49)], [r[0] for r in rows])
        self.assertEqual(48, len({r[1] for r in rows}))
        focus = [r for r in rows if r[5] == "FOCUS_ACQUISITION_DEDUP"]
        non = [r for r in rows if r[5] == "COUNTED_EXACT"]
        self.assertEqual(24, len(focus))
        self.assertEqual(24, len(non))
        self.assertEqual(24, len({r[4] for r in non}))
        self.assertEqual(24, len({r[4] for r in focus}))
        self.assertTrue(all(r[2] == "goety:craft" for r in focus))
        self.assertEqual(
            {"goety:convert_tamed": 9, "goety:convert_complete_tamed": 1,
             "goety:summon_tamed": 13, "goety:craft": 1},
            {k: sum(r[2] == k for r in non) for k in {r[2] for r in non}},
        )
        self.assertNotIn("goety:jei_dummy/none", {r[4] for r in rows})
        self.assertTrue(
            all(r[3] == "\x60goety:jei_dummy/none\x60"
                for r in non if r[2] != "goety:craft")
        )
        index = (provider / "RITUAL-CARDS-1.21.1-1.8.2.md").read_text(
            encoding="utf-8"
        )
        pages = sorted((provider / "rituals").glob("*.md"))
        self.assertEqual(24, len(pages))
        for i, (number, path, typ, result, outcome, _) in enumerate(non, 1):
            slug = path.removeprefix("data/goety_cataclysm/recipe/")
            slug = slug.removesuffix(".json").replace("/", "__")
            file = provider / "rituals" / (slug + ".md")
            self.assertTrue(file.is_file(), path)
            card = file.read_text(encoding="utf-8")
            self.assertIn("**Recipe path literal:** \x60" + path + "\x60", card)
            self.assertIn("**Subtipo \x60ritual_type\x60:** \x60" + typ + "\x60", card)
            self.assertIn("**Outcome semântico exato:** \x60" + outcome + "\x60", card)
            self.assertIn("**Posição na lista não-Focus:** " + str(i) + "/24", card)
            self.assertIn("índice no arquivo: " + number + "/48", card)
            self.assertIn("**+0 novas identidades semânticas**", card)
            self.assertIn("COUNTED_EXACT", card)
            self.assertIn("**NÃO VERIFICADOS individualmente:**", card)
            self.assertIn("../RITUAL-INVENTORY-EXACT-1.21.1-1.8.2.md", card)
            self.assertIn(
                f"| {i} | \x60{path}\x60 | \x60{typ}\x60 | \x60{outcome}\x60 "
                f"| [Abrir](rituals/{slug}.md) |", index,
            )
        self.assertIn("✅ 24/24 fichas nominais", index)
        self.assertIn("**+0 novas identidades semânticas**", index)
        self.assertIn("38190078609", text)
        self.assertIn("RITUAL-CARDS-1.21.1-1.8.2.md", self.index)
        self.assertIn("RITUAL-INVENTORY-EXACT-1.21.1-1.8.2.md", self.index)
        readme = (provider / "README.md").read_text(encoding="utf-8")
        owners = readme.split(
            "O provider registra exatamente **28 Focuses próprios**:", 1
        )[1].split("Todos os 28 possuem caminho de aquisição", 1)[0]
        owners = re.findall(r"\x60([A-Z_]+_FOCUS)\x60", owners)
        self.assertEqual(28, len(owners))
        mapped_foci = {r[4] for r in focus}
        inferred = {"AMETHYST_CLUSTER_FOCUS", "ASHEN_BREATH_FOCUS",
                    "VOID_RUNE_FOCUS", "WATER_SPEAR_FOCUS"}
        self.assertEqual(
            inferred, {h for h in owners
                       if "goety_cataclysm:" + h.lower() not in mapped_foci}
        )
        for holder in owners:
            fpath = provider / "focuses" / (
                holder.lower().replace("_", "-") + ".md"
            )
            content = fpath.read_text(encoding="utf-8")
            self.assertIn("**Rota de aquisição atribuída:**", content)
            if holder in inferred:
                self.assertIn("minecraft:crafting_shaped", content)
                self.assertIn("**Rota de aquisição atribuída:** ✅ receita", content)
            else:
                matched = next(r for r in focus if
                    r[4] == "goety_cataclysm:" + holder.lower())
                self.assertIn(matched[1], content)
                self.assertIn("comprovado individualmente", content)
            self.assertIn("../RITUAL-CARDS-1.21.1-1.8.2.md", content)


    def test_goety_cataclysm_182_four_exact_shaped_focus_acquisitions(self):
        provider = PROVIDERS / "✅-goety-cataclysm"
        doc = (provider / "FOCUS-CRAFTING-EXACT-1.21.1-1.8.2.md").read_text(
            encoding="utf-8"
        )
        records = re.findall(
            r"^\| (\d+) \| \x60([A-Z_]+_FOCUS)\x60 "
            r"\| \x60(data/goety_cataclysm/recipe/focus/[a-z0-9_]+\.json)\x60 "
            r"\| \x60(minecraft:crafting_shaped)\x60 "
            r"\| \x60(goety_cataclysm:[a-z0-9_]+)\x60 "
            r"\| (0) \| \x60(FOCUS_ACQUISITION_DEDUP)\x60 \|$",
            doc, re.MULTILINE,
        )
        self.assertEqual(4, len(records))
        self.assertEqual(["1", "2", "3", "4"], [r[0] for r in records])
        expected = {
            "AMETHYST_CLUSTER_FOCUS": "amethyst_cluster_focus",
            "ASHEN_BREATH_FOCUS": "ashen_breath_focus",
            "VOID_RUNE_FOCUS": "void_rune_focus",
            "WATER_SPEAR_FOCUS": "water_spear_focus",
        }
        self.assertEqual(set(expected), {r[1] for r in records})
        self.assertEqual(4, len({r[2] for r in records}))
        self.assertEqual(4, len({r[4] for r in records}))
        for _, holder, path, recipe_type, result_id, conditions, status in records:
            short = expected[holder]
            self.assertEqual(
                "data/goety_cataclysm/recipe/focus/" + short + ".json", path
            )
            self.assertEqual("goety_cataclysm:" + short, result_id)
            self.assertEqual("minecraft:crafting_shaped", recipe_type)
            self.assertEqual("0", conditions)
            self.assertEqual("FOCUS_ACQUISITION_DEDUP", status)
            card = provider / "focuses" / (
                holder.lower().replace("_", "-") + ".md"
            )
            self.assertTrue(card.is_file())
            body = card.read_text(encoding="utf-8")
            self.assertIn("**Rota de aquisição atribuída:**", body)
            self.assertIn("receita \x60minecraft:crafting_shaped\x60", body)
            self.assertIn(path, body)
            self.assertIn(result_id, body)
            self.assertIn(
                "../FOCUS-CRAFTING-EXACT-1.21.1-1.8.2.md", body,
            )
            self.assertNotIn("por exclusão controlada", body)
        self.assertIn("38191990175", doc)
        self.assertIn("4e3052a082200371b36e1a88fdce05e294d82757", doc)
        self.assertIn("**+0 novas identidades semânticas**", doc)
        ritual = (
            provider / "RITUAL-INVENTORY-EXACT-1.21.1-1.8.2.md"
        ).read_text(encoding="utf-8")
        ritual_focus_ids = set(re.findall(
            r"^\| \d+ \| .*? \| \x60(goety_cataclysm:[a-z0-9_]+_focus)\x60 "
            r"\| \x60\[\]\x60 \| \x60FOCUS_ACQUISITION_DEDUP\x60 \|$",
            ritual, re.MULTILINE,
        ))
        self.assertEqual(24, len(ritual_focus_ids))
        shaped_ids = {r[4] for r in records}
        self.assertTrue(shaped_ids.isdisjoint(ritual_focus_ids))
        self.assertEqual(28, len(shaped_ids | ritual_focus_ids))
        readme = (provider / "README.md").read_text(encoding="utf-8")
        holders_section = readme.split(
            "O provider registra exatamente **28 Focuses próprios**:", 1
        )[1].split("Todos os 28 possuem caminho de aquisição", 1)[0]
        holder_ids = {
            "goety_cataclysm:" + h.lower()
            for h in re.findall(r"\x60([A-Z_]+_FOCUS)\x60", holders_section)
        }
        self.assertEqual(holder_ids, shaped_ids | ritual_focus_ids)
        self.assertIn(
            "FOCUS-CRAFTING-EXACT-1.21.1-1.8.2.md", self.index
        )
        self.assertIn(
            "FOCUS-CRAFTING-EXACT-1.21.1-1.8.2.md",
            (provider / "FOCUS-CARDS-1.21.1-1.8.2.md").read_text(
                encoding="utf-8"
            ),
        )

    def test_goety_iron_3_1_focus_cards_and_ritual_evidence_gate(self):
        provider = PROVIDERS / "✅-goety-iron"
        readme = (provider / "README.md").read_text(encoding="utf-8")
        section = readme.split(
            "O provider registra exatamente **2 Focuses próprios**:", 1
        )[1].split("Ambos são superfícies", 1)[0]
        holders = re.findall(r"^- `([A-Z_]+_FOCUS)`$", section, re.MULTILINE)
        self.assertEqual(["FIERY_FOCUS", "TARNISHED_FOCUS"], holders)
        index = (provider / "FOCUS-CARDS-3.1.md").read_text(encoding="utf-8")
        pages = sorted((provider / "focuses").glob("*.md"))
        self.assertEqual(2, len(pages))
        for ordinal, field in enumerate(holders, 1):
            filename = field.lower().replace("_", "-") + ".md"
            path = provider / "focuses" / filename
            self.assertTrue(path.is_file(), field)
            body = path.read_text(encoding="utf-8")
            self.assertIn(f"# Goety Iron 3.1 — `{field}`", body)
            self.assertIn(f"**Focus holder auditado:** `{field}`", body)
            self.assertIn(f"**Ordinal editorial:** {ordinal}/2", body)
            self.assertIn("COUNTED_EXACT", body)
            self.assertIn("**+0 identidades semânticas**", body)
            self.assertIn("**NÃO VERIFICADO**", body)
            self.assertIn("não são inventadas", body)
            self.assertIn(
                f"| {ordinal} | `{field}` | [Abrir](focuses/{filename}) |",
                index,
            )
            self.assertIn("../EXACT-3.1-ARTIFACT-AUDIT.md", body)
        self.assertIn("**✅ 2/2 Focuses", index)
        self.assertIn("**14 recipes `goety:ritual`**", index)
        self.assertIn("**12 restantes**", index)
        self.assertIn("12/12 rituais semanticamente contabilizados", index)
        self.assertIn("12/12 fichas nominais", index)
        self.assertIn("**+0 novas identidades**", index)
        self.assertIn("1.851 global / 1.849 no escopo", index)
        self.assertIn("c8529867e798661ed01fb2948abda23735888fc6", index)
        artifact = (provider / "EXACT-3.1-ARTIFACT-AUDIT.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("2 addon-owned Focus holders", artifact)
        self.assertIn("12 non-Focus rituals remain", artifact)
        self.assertIn("14 packaged `goety:ritual` recipes", artifact)
        self.assertIn("FOCUS-CARDS-3.1.md", readme)
        self.assertIn("FOCUS-CARDS-3.1.md", self.index)
        tech = (provider / "TECHNICAL-AUDIT.md").read_text(encoding="utf-8")
        self.assertIn("## Adendo de autoridade — auditoria hash-matched 3.1", tech)
        sync = (provider / "RELEASE-SYNC-EVIDENCE.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("## Supersession note — exact 3.1 Phase 2BL artifact", sync)

    def test_goety_iron_31_12_exact_ritual_cards_from_source_matrix(self):
        provider = PROVIDERS / "✅-goety-iron"
        matrix = (provider / "RITUAL-INVENTORY-EXACT-3.1.md").read_text(
            encoding="utf-8"
        )
        rows = re.findall(
            r"^\| (\d+) \| \x60(data/goetyiron/recipe/[a-z0-9_]+\.json)\x60 "
            r"\| \x60(goety:[a-z0-9_]+)\x60 \| (.*?) \| "
            r"\x60([a-z0-9_:/]+)\x60 \| \x60\[\]\x60 \| "
            r"\x60(FOCUS_ACQUISITION_DEDUP|COUNTED_EXACT)\x60 \|$",
            matrix, re.MULTILINE,
        )
        self.assertEqual(14, len(rows))
        self.assertEqual([str(i) for i in range(1, 15)], [r[0] for r in rows])
        self.assertEqual(14, len({r[1] for r in rows}))
        self.assertEqual(14, len({r[4] for r in rows}))
        self.assertEqual(2, sum(r[5] == "FOCUS_ACQUISITION_DEDUP" for r in rows))
        exact = [r for r in rows if r[5] == "COUNTED_EXACT"]
        self.assertEqual(12, len(exact))
        self.assertEqual(10, sum(r[2] == "goety:convert_complete_tamed" for r in exact))
        self.assertEqual(2, sum(r[2] == "goety:craft" for r in exact))
        self.assertEqual(
            {"goetyiron:fiery_focus", "goetyiron:tarnished_focus"},
            {r[4] for r in rows if r[5] == "FOCUS_ACQUISITION_DEDUP"},
        )
        self.assertEqual(
            {"goetyiron:hemolytic_ring", "irons_spellbooks:rotten_spell_book"},
            {r[4] for r in exact if r[2] == "goety:craft"},
        )
        self.assertIn("goety:jei_dummy/none", matrix)
        self.assertNotIn(
            "goety:jei_dummy/none", {r[4] for r in rows},
            "JEI dummy must not be semantic outcome",
        )
        index = (provider / "RITUAL-CARDS-3.1.md").read_text(
            encoding="utf-8"
        )
        pages = sorted((provider / "rituals").glob("*.md"))
        self.assertEqual(12, len(pages))
        for ordinal, (_, path, typ, result_ids, dest, _) in enumerate(exact, 1):
            slug = path.split("/")[-1][:-5]
            page = provider / "rituals" / (slug + ".md")
            self.assertTrue(page.is_file(), path)
            card = page.read_text(encoding="utf-8")
            self.assertIn("**Resource path literal:** \x60" + path + "\x60", card)
            self.assertIn("**Recipe type do pacote:** \x60goety:ritual\x60", card)
            self.assertIn("**Campo \x60ritual_type\x60:** \x60" + typ + "\x60", card)
            self.assertIn("**Resultado semântico do ritual:** \x60" + dest + "\x60", card)
            self.assertIn("**Ordinal não-Focus:** " + str(ordinal) + "/12", card)
            self.assertIn("COUNTED_EXACT", card)
            self.assertIn("**+0 novas identidades semânticas**", card)
            self.assertIn("**NÃO VERIFICADOS individualmente**", card)
            self.assertIn("../RITUAL-INVENTORY-EXACT-3.1.md", card)
            self.assertIn("../EXACT-3.1-ARTIFACT-AUDIT.md", card)
            self.assertIn(
                f"| {ordinal} | \x60{slug}\x60 | \x60{typ}\x60 | "
                f"\x60{dest}\x60 | [Abrir](rituals/{slug}.md) |",
                index,
            )
            if typ == "goety:convert_complete_tamed":
                self.assertEqual("\x60goety:jei_dummy/none\x60", result_ids)
                self.assertIn("marcador placeholder", card)
            else:
                self.assertEqual("\x60" + dest + "\x60", result_ids)
        self.assertIn("**✅ 12/12 fichas nominais", index)
        self.assertIn("**+0 novas identidades semânticas**", index)
        self.assertIn("RITUAL-INVENTORY-EXACT-3.1.md", index)
        self.assertIn("38186445480", index)
        for path in ("README.md", "FOCUS-CARDS-3.1.md", "EXACT-3.1-ARTIFACT-AUDIT.md"):
            self.assertIn(
                "RITUAL-CARDS-3.1.md",
                (provider / path).read_text(encoding="utf-8"),
            )
        self.assertIn("RITUAL-CARDS-3.1.md", self.index)
        self.assertIn("RITUAL-INVENTORY-EXACT-3.1.md", self.index)

    def test_ars_zero_twelve_release_bounded_glyph_cards(self):
        provider = PROVIDERS / "✅-ars-zero"
        matrix = (provider / "GLYPH-CATALOG.md").read_text(encoding="utf-8")
        records = re.findall(
            r"^\| ([^|]+) \| ([^|]+) \| ([^|]+) \| ([^|]+) \|$",
            matrix, re.MULTILINE,
        )
        capabilities = [
            (name.strip(), evidence.strip(), role.strip(), bound.strip())
            for name, evidence, role, bound in records
            if name.strip() not in ("Capability", "---")
            and not name.strip().startswith("---")
        ]
        self.assertEqual(12, len(capabilities))
        self.assertEqual(12, len({x[0] for x in capabilities}))
        index = (provider / "GLYPH-CARDS-2.0.2.md").read_text(
            encoding="utf-8"
        )
        pages = sorted((provider / "glyphs").glob("*.md"))
        self.assertEqual(18, len(pages))
        for ordinal, (name, evidence, role, bound) in enumerate(capabilities, 1):
            slug = re.sub(r"^-|-$", "", re.sub(r"[^a-z0-9]+", "-", name.lower()))
            path = provider / "glyphs" / (slug + ".md")
            self.assertTrue(path.is_file(), name)
            text = path.read_text(encoding="utf-8")
            self.assertIn(f"# Ars Zero 2.0.2 — {name}", text)
            self.assertIn(f"**Nome exibido pelo provider:** {name}", text)
            self.assertIn(f"**Evidência corrente na matriz original:** {evidence}", text)
            self.assertIn(f"**Papel semântico publicado:** {role}", text)
            self.assertIn(f"**Fronteira de integração Black Arcana:** {bound}", text)
            self.assertIn(f"**Posição editorial:** {ordinal}/12", text)
            self.assertIn("COUNTED_RELEASE_BOUNDED", text)
            self.assertIn("**+0 novas identidades**", text)
            self.assertIn("`NÃO VERIFICADO`", text)
            self.assertIn(f"| {ordinal} | {name} | {evidence} | [Abrir](glyphs/{slug}.md) |", index)
            self.assertIn("../GLYPH-CATALOG.md", text)
        self.assertIn("12/12 capacidades públicas distintas", index)
        self.assertIn("**+0 novas identidades**", index)
        self.assertIn("**1.851 global / 1.849 no escopo solicitado**", index)
        for ignored in ("AOE II", "AOE III", "Amplifier II", "Amplifier III"):
            self.assertIn(ignored, index)
        self.assertIn("GLYPH-CARDS-2.0.2.md", self.index)
        self.assertIn("GLYPH-CARDS-2.0.2.md",
                      (provider / "README.md").read_text(encoding="utf-8"))


    def test_ars_zero_202_physical_exact_twenty_two_with_six_new_unique(self):
        """22 binary register slots != 22 unique semantic roots."""
        provider = PROVIDERS / "✅-ars-zero"
        dossier = (provider / "EXACT-BINARY-GLYPHS-2.0.2.md").read_text(encoding="utf-8")
        rows = re.findall(
            r"^\| (\d+) \| `(ars_zero:[a-z_]+)` \| `([^`]+)` \| (base|NEW|COPIED) \|$",
            dossier, re.MULTILINE,
        )
        self.assertEqual(22, len(rows))
        self.assertEqual([str(i) for i in range(1, 23)], [r[0] for r in rows])
        self.assertEqual(22, len({r[1] for r in rows}))
        self.assertEqual(18, sum(r[3] != "COPIED" for r in rows))
        self.assertEqual(6, sum(r[3] == "NEW" for r in rows))
        self.assertEqual(4, sum(r[3] == "COPIED" for r in rows))
        self.assertIn("38343776242", dossier)
        self.assertIn("6774561", dossier)
        self.assertIn("ac9b6e6f7a2bd403ee7cdc16023509fde7c4e1d0", dossier)
        expected = {
            "sustain": ("sustain_effect", "SustainEffect"),
            "discard": ("discard_effect", "DiscardEffect"),
            "hollow": ("augment_hollow", "AugmentHollow"),
            "sphere": ("augment_sphere", "AugmentSphere"),
            "cube": ("augment_cube", "AugmentCube"),
            "flatten": ("augment_flatten", "AugmentFlatten"),
        }
        for slug, (glyph_id, cls) in expected.items():
            text = (provider / "glyphs" / f"{slug}.md").read_text(encoding="utf-8")
            self.assertIn(f"ars_zero:{glyph_id}", text)
            self.assertIn(cls, text)
            self.assertIn("COUNTED_EXACT", text)
            self.assertIn("NÃO VERIFICADO", text)
        self.assertEqual(18, len(list((provider / "glyphs").glob("*.md"))))
        matrix = (ROOT / "wiki/modpack-catalog/meta" /
                  "REVALIDACAO-BINARIA-39-PROVIDERS-2026-10-08.md").read_text(encoding="utf-8")
        arszero = next(x for x in matrix.splitlines() if x.startswith("| [Ars Zero]"))
        self.assertIn("| 2.0.2 | 18 | COUNTED_EXACT |", arszero)
        self.assertIn("14/39", matrix)
        self.assertIn("25/39", matrix)
        ledger = (ROOT / "wiki/modpack-catalog/meta" /
                  "SEMANTIC-MAGIC-COVERAGE.md").read_text(encoding="utf-8")
        row = next(x for x in ledger.splitlines() if x.startswith("| [Ars Zero]"))
        self.assertIn("| 2.0.2 | 18 | `COUNTED_EXACT` |", row)
        self.assertIn("1857 global / 1855 scoped", ledger)

    def test_ars_elemental_47_source_pinned_cards(self):
        provider = PROVIDERS / "✅-ars-elemental"
        glyph_source = (provider / "GLYPHS.md").read_text(encoding="utf-8")
        ritual_source = (provider / "RITUALS.md").read_text(encoding="utf-8")
        glyph_index = (provider / "GLYPH-CARDS-0.7.10.1.md").read_text(
            encoding="utf-8"
        )
        ritual_index = (provider / "RITUAL-CARDS-0.7.10.1.md").read_text(
            encoding="utf-8"
        )
        expected_types = (
            ("## Effects — 23", "### Source-behavior notes", 23),
            ("## Cast methods — 2", "## Propagators — 2", 2),
            ("## Propagators — 2", "## Filters — 12", 2),
        )
        names = []
        for start, end, expected in expected_types:
            source = glyph_source.split(start, 1)[1].split(end, 1)[0]
            rows = [line.split("|")[1].strip()
                    for line in source.splitlines()
                    if line.startswith("| ")
                    and not line.startswith("| Glyph")
                    and not line.startswith("|---")]
            self.assertEqual(expected, len(rows), start)
            names.extend(rows)
        pairs_source = glyph_source.split(
            "| Normal / inverted pair |", 1
        )[1].split("Registered ids are", 1)[0]
        pairs = [row.split("|")[1].strip() for row in pairs_source.splitlines()
                 if row.startswith("| ") and not row.startswith("|---")]
        self.assertEqual(6, len(pairs))
        for pair in pairs:
            names.extend(pair.split(" / "))
        registered = re.findall(
            r"`(glyph_[a-z_]+)`",
            glyph_source.split("Registered ids are", 1)[1].split(
                "under namespace", 1
            )[0],
        )
        self.assertEqual(12, len(registered))
        self.assertEqual(39, len(names))
        self.assertEqual(39, len(set(names)))
        glyph_pages = sorted((provider / "glyphs").glob("*.md"))
        self.assertEqual(39, len(glyph_pages))
        for ordinal, name in enumerate(names, 1):
            slug = re.sub(r"(^-|-$)", "", re.sub(r"[^a-z0-9]+", "-", name.lower()))
            page = provider / "glyphs" / (slug + ".md")
            self.assertTrue(page.is_file(), name)
            card = page.read_text(encoding="utf-8")
            self.assertIn(f"# Ars Elemental 0.7.10.1 — {name}", card)
            self.assertIn("COUNTED_SOURCE_PINNED", card)
            self.assertIn("**+0 novas identidades**", card)
            self.assertIn(f"| {ordinal} |", glyph_index)
            self.assertIn(f"(glyphs/{slug}.md)", glyph_index)
            self.assertIn("../GLYPHS.md", card)
            if ordinal <= 27:
                self.assertIn("**ResourceLocation individual:** **NÃO VERIFICADO", card)
            else:
                ident = "glyph_" + name.lower().replace("not ", "not_").replace(" ", "_") + "_filter"
                self.assertIn(ident, registered)
                self.assertIn(f"`ars_elemental:{ident}`", card)
        self.assertIn("MethodCarianPhalanx", glyph_index)
        self.assertIn("frame_skip_recipe=false", glyph_index)
        ritual_ids = re.findall(
            r"^## `(ars_elemental:ritual_[a-z_]+)`$",
            ritual_source, re.MULTILINE,
        )
        self.assertEqual(8, len(ritual_ids))
        self.assertEqual(8, len(set(ritual_ids)))
        ritual_pages = sorted((provider / "rituals" / "cards").glob("*.md"))
        self.assertEqual(8, len(ritual_pages))
        for ordinal, ident in enumerate(ritual_ids, 1):
            slug = ident.split(":")[1]
            path = provider / "rituals" / "cards" / (slug + ".md")
            self.assertTrue(path.is_file(), ident)
            text = path.read_text(encoding="utf-8")
            self.assertIn(f"# Ars Elemental 0.7.10.1 — `{ident}`", text)
            self.assertIn("COUNTED_SOURCE_PINNED", text)
            self.assertIn(f"| {ordinal} | `{ident}` | [Abrir](rituals/cards/{slug}.md) |", ritual_index)
            self.assertIn("../../RITUALS.md", text)
        self.assertIn("50 Ars Source a cada cinco placements", ritual_index)
        self.assertIn("getSourceCost()=0", ritual_index)
        self.assertIn("**+0 novas identidades semânticas**", ritual_index)
        self.assertIn("GLYPH-CARDS-0.7.10.1.md", self.index)
        self.assertIn("RITUAL-CARDS-0.7.10.1.md", self.index)
        readme = (provider / "README.md").read_text(encoding="utf-8")
        self.assertIn("GLYPH-CARDS-0.7.10.1.md", readme)
        self.assertIn("RITUAL-CARDS-0.7.10.1.md", readme)

    def test_ars_hex_one_exact_binary_glyph_card(self):
        provider = PROVIDERS / "✅-ars-hex"
        source = (provider / "GLYPHS.md").read_text(encoding="utf-8")
        registry = (provider / "REGISTRIES.md").read_text(encoding="utf-8")
        readme = (provider / "README.md").read_text(encoding="utf-8")
        index = (provider / "GLYPH-CARDS-5.0.4b.md").read_text(encoding="utf-8")
        pages = sorted((provider / "glyphs").glob("*.md"))
        self.assertEqual(1, len(pages))
        card = (provider / "glyphs" / "soul-shatter.md").read_text(encoding="utf-8")
        self.assertIn("`ars_hex:glyph_soul_shatter`", source)
        self.assertIn("`ars_hex:glyph_soul_shatter`", registry)
        self.assertIn("`ars_hex:glyph_soul_shatter`", card)
        self.assertIn("`ars_hex:glyph_soul_shatter`", index)
        self.assertIn("(glyphs/soul-shatter.md)", index)
        for field in ("Tier II", "Mana base 30", "Amplify +3.0",
                      "limite explícito de Amplify 2", "XP 55", "VOODOO",
                      "malum:wicked_spirit", "malum:soul_stained_steel_sword"):
            self.assertIn(field, card)
        self.assertIn("COUNTED_EXACT", card)
        self.assertIn("**+0 novas identidades**", card)
        self.assertIn("**⚠️ NÃO VERIFICADO no runtime físico:**", card)
        self.assertIn("não implementa fórmula/RNG explícito de spirit-release", card)
        self.assertIn("2354710ea312e2a6e0fbc3eb2dbafb8e06f10cf4", card)
        self.assertIn("Alexthw46/Ars-Unity@b25528adf8c0135585cd6d654582efa147e0a227", card)
        self.assertIn("GLYPH-CARDS-5.0.4b.md", readme)
        self.assertIn("GLYPH-CARDS-5.0.4b.md", self.index)
        self.assertIn("**1.851 global / 1.849 no escopo solicitado**", index)
        self.assertIn("Malum é fisicamente presente", index)
        self.assertIn("Hexerei/Hexcasting são ausentes", index)

    def test_relics_41_exact_owner_scoped_power_cards(self):
        provider = PROVIDERS / "✅-relics"
        source = (provider / "EXACT-0.12.8-ABILITY-INVENTORY.md").read_text(
            encoding="utf-8"
        )
        ability_section = source.split("## 39 exact base ability roots", 1)[1].split(
            "The identity key is owner-scoped", 1
        )[0]
        synergy_section = source.split("## 2 exact synergy roots", 1)[1].split(
            "These are distinct owner-scoped", 1
        )[0]
        pattern = r"^\| (\d+) \| ([a-z_]+) \| ([a-z_]+) \|$"
        abilities = re.findall(pattern, ability_section, re.MULTILINE)
        synergies = re.findall(pattern, synergy_section, re.MULTILINE)
        self.assertEqual(39, len(abilities))
        self.assertEqual(2, len(synergies))
        self.assertEqual(39, len({(o, i) for _, o, i in abilities}))
        self.assertEqual(2, len({(o, i) for _, o, i in synergies}))
        self.assertEqual(20, len({o for _, o, _ in abilities}))
        self.assertEqual({("glitchy_mantle", "electricity"),
                          ("kinetic_belt", "electricity")},
                         {(o, i) for _, o, i in synergies})
        index = (provider / "ABILITY-CARDS-0.12.8.md").read_text(
            encoding="utf-8"
        )
        for label, kind, rows, expected in (
            ("Habilidade", "abilities", abilities, 39),
            ("Sinergia", "synergies", synergies, 2),
        ):
            pages = sorted((provider / kind).rglob("*.md"))
            self.assertEqual(expected, len(pages))
            for num, (owner, ident) in enumerate([(o, i) for _, o, i in rows], 1):
                path = provider / kind / owner / (ident + ".md")
                self.assertTrue(path.is_file(), (kind, owner, ident))
                card = path.read_text(encoding="utf-8")
                self.assertIn(f"# Relics 0.12.8 — {owner} / {ident}", card)
                self.assertIn(f"**Relíquia proprietária:** `{owner}`", card)
                self.assertIn(f"**Chave semântica inequívoca:** `{owner}|{ident}`", card)
                self.assertIn(f"**Ordinal da seção factual:** {num}/{expected}", card)
                self.assertIn("COUNTED_EXACT", card)
                self.assertIn("**+0 novas identidades**", card)
                self.assertIn("**NÃO VERIFICADO**", card)
                self.assertIn("../../EXACT-0.12.8-ABILITY-INVENTORY.md", card)
                self.assertIn(
                    f"| {num} | `{owner}` | `{ident}` | `{owner}|{ident}` | "
                    f"[Abrir]({kind}/{owner}/{ident}.md) |", index
                )
        self.assertIn("**✅ 39/39 habilidades base + 2/2 sinergias", index)
        self.assertIn("**+0 novas identidades**", index)
        self.assertIn("**1.851 global / 1.849 escopo**", index)
        self.assertIn("ABILITY-CARDS-0.12.8.md", self.index)
        self.assertIn("ABILITY-CARDS-0.12.8.md",
                      (provider / "README.md").read_text(encoding="utf-8"))

    def test_hexalia_137_29_ritual_infusion_cards(self):
        provider = PROVIDERS / "✅-hexalia"
        nature = (provider / "rituals" / "NATURES-RITUAL-CATALOG.md").read_text(encoding="utf-8")
        celestial = (provider / "infusions" / "CELESTIAL-INFUSION-CATALOG.md").read_text(encoding="utf-8")
        def recipe_rows(document, size):
            rows = []
            for line in document.splitlines():
                if line.startswith("| `hexalia:"):
                    data = [part.strip() for part in line.split("|")[1:-1]]
                    self.assertEqual(size, len(data), line)
                    rows.append(data)
            return rows
        rituals = recipe_rows(nature, 6)
        infusions = recipe_rows(celestial, 3)
        self.assertEqual((23, 6), (len(rituals), len(infusions)))
        self.assertEqual(29, len({x[0] for x in rituals + infusions}))
        ritual_index = (provider / "NATURES-RITUAL-CARDS-1.3.7.md").read_text(encoding="utf-8")
        infusion_index = (provider / "CELESTIAL-INFUSION-CARDS-1.3.7.md").read_text(encoding="utf-8")
        self.assertEqual(23, len(list((provider / "rituals" / "cards").glob("*.md"))))
        self.assertEqual(6, len(list((provider / "infusions" / "cards").glob("*.md"))))
        for number, (raw, center, offerings, result, timing, soul) in enumerate(rituals, 1):
            recipe_id = raw.strip("`")
            filename = recipe_id.split(":")[1] + ".md"
            path = provider / "rituals" / "cards" / filename
            self.assertTrue(path.is_file(), recipe_id)
            card = path.read_text(encoding="utf-8")
            self.assertIn("**Registry de receita:** `" + recipe_id + "`", card)
            self.assertIn("**Centro no Ritual Table:** " + center, card)
            self.assertIn("**Offerings por Ritual Braziers:** " + offerings, card)
            self.assertIn("**Resultado provider-owned:** " + result, card)
            self.assertIn("**Quantidade de offerings / processamento base:** " + timing, card)
            self.assertIn("**Requer captura de alma:** **" + ("sim" if soul == "yes" else "não") + "**", card)
            self.assertIn("**Ordinal editorial:** " + str(number) + "/23", card)
            self.assertIn("COUNTED_SOURCE_PINNED", card)
            self.assertIn("**+0 novas identidades**", card)
            self.assertIn("../../rituals/NATURES-RITUAL-CATALOG.md", card)
            self.assertIn("[Abrir](rituals/cards/" + filename + ")", ritual_index)
            if soul == "yes":
                self.assertIn("AWAITING_SOUL", card)
                self.assertIn("50 ticks", card)
                self.assertIn("hexalia:athame", card)
            else:
                self.assertIn("não há fase `AWAITING_SOUL`", card)
        for number, (raw, item_in, item_out) in enumerate(infusions, 1):
            recipe_id = raw.strip("`")
            filename = recipe_id.split(":")[1] + ".md"
            path = provider / "infusions" / "cards" / filename
            self.assertTrue(path.is_file(), recipe_id)
            card = path.read_text(encoding="utf-8")
            self.assertIn("**Recipe ID:** `" + recipe_id + "`", card)
            self.assertIn("**Entrada no Ritual Brazier:** " + item_in, card)
            self.assertIn("**Saída substitutiva (1x):** " + item_out, card)
            self.assertIn("**Ordinal editorial:** " + str(number) + "/6", card)
            self.assertIn("COUNTED_SOURCE_PINNED", card)
            self.assertIn("**+0 novas identidades**", card)
            self.assertIn("120 ticks (6 s)", card)
            self.assertIn("**não há exigência `SALTED=true`**", card)
            self.assertIn("../../infusions/CELESTIAL-INFUSION-CATALOG.md", card)
            self.assertIn("[Abrir](infusions/cards/" + filename + ")", infusion_index)
        self.assertIn("✅ 23/23 receitas", ritual_index)
        self.assertIn("✅ 6/6 receitas", infusion_index)
        self.assertIn("**+0 novas identidades semânticas**", infusion_index)
        for filename in ("NATURES-RITUAL-CARDS-1.3.7.md", "CELESTIAL-INFUSION-CARDS-1.3.7.md"):
            self.assertIn(filename, self.index)
            self.assertIn(filename, (provider / "README.md").read_text(encoding="utf-8"))

    def test_betterend_21034_48_infusion_ritual_cards(self):
        provider = PROVIDERS / "✅-betterend"
        source = (provider / "rituals" / "INFUSION-RITUAL-CATALOG.md").read_text(
            encoding="utf-8"
        )
        rows = re.findall(
            r"^\| (\d+) \| `(betterend:[a-z0-9_]+)` "
            r"\| `([a-z0-9_:]+)` \| `COUNTED_EXACT` \|$",
            source, re.MULTILINE,
        )
        self.assertEqual(48, len(rows))
        self.assertEqual([str(i) for i in range(1, 49)], [r[0] for r in rows])
        self.assertEqual(48, len({r[1] for r in rows}))
        self.assertEqual(39, sum(1 for r in rows if r[2] == "minecraft:enchanted_book"))
        self.assertEqual(9, sum(1 for r in rows if r[2] != "minecraft:enchanted_book"))
        self.assertEqual(10, len({r[2] for r in rows}))
        index = (provider / "INFUSION-RITUAL-CARDS-21.0.34.md").read_text(
            encoding="utf-8"
        )
        cards = sorted((provider / "rituals" / "cards").glob("*.md"))
        self.assertEqual(48, len(cards), "must have one card per exact recipe")
        self.assertNotIn("betterend:eternal_portal", [r[1] for r in rows])
        for number, rid, output in rows:
            slug = rid.split(":", 1)[1]
            page = provider / "rituals" / "cards" / (slug + ".md")
            self.assertTrue(page.is_file(), rid)
            body = page.read_text(encoding="utf-8")
            self.assertIn("**Recipe ID:** `" + rid + "`", body)
            self.assertIn("**Recipe type:** `betterend:infusion`", body)
            self.assertIn("**Resultado — item ID:** `" + output + "`", body)
            self.assertIn("**Posição no inventário exato:** " + number + "/48", body)
            self.assertIn("COUNTED_EXACT", body)
            self.assertIn("**+0 novas identidades**", body)
            self.assertIn("**NÃO VERIFICADO individualmente**", body)
            self.assertIn("../INFUSION-RITUAL-CATALOG.md", body)
            self.assertIn("../../EXACT-21.0.34-ARTIFACT-AUDIT.md", body)
            self.assertIn(
                f"| {number} | `{rid}` | `{output}` | "
                f"[Abrir](rituals/cards/{slug}.md) |",
                index,
            )
        self.assertIn("48/48", index)
        self.assertIn("**48** infusões + **1** Eternal Portal Ritual", index)
        self.assertIn("**+0 novas identidades semânticas:**", index)
        self.assertIn("INFUSION-RITUAL-CARDS-21.0.34.md", self.index)
        self.assertIn(
            "INFUSION-RITUAL-CARDS-21.0.34.md",
            (provider / "README.md").read_text(encoding="utf-8"),
        )

    def test_more_relics_177_sixty_one_exact_ability_cards(self):
        provider = PROVIDERS / "✅-more-relics"
        source = (provider / "ABILITY-INVENTORY-EXACT.md").read_text(encoding="utf-8")
        records = re.findall(
            r"^\| \x60([a-z0-9_]+)\x60 \| (\d+) \| ([^|]+) \| ([^|]+) \|$",
            source, re.MULTILINE,
        )
        self.assertEqual(29, len(records), "29 owner roots from exact artifact")
        pairs = []
        for owner, count, roots, route in records:
            abilities = [entry.strip(" \x60") for entry in roots.split(",")]
            self.assertEqual(int(count), len(abilities), owner)
            pairs.extend((owner, ability, route) for ability in abilities)
        self.assertEqual(61, len(pairs))
        self.assertEqual(61, len({(owner, ability) for owner, ability, _ in pairs}))
        self.assertEqual(56, len({ability for _, ability, _ in pairs}))
        for root, cardinality in (("cyberpsychosis", 4), ("blood_bond", 2), ("head_start", 2)):
            self.assertEqual(cardinality, sum(ability == root for _, ability, _ in pairs))
        index = (provider / "ABILITY-CARDS-1.7.7-REL0128.md").read_text(
            encoding="utf-8"
        )
        pages = sorted((provider / "abilities").rglob("*.md"))
        self.assertEqual(61, len(pages), "one card per owner+ability")
        for ordinal, (owner, ability, route) in enumerate(pairs, 1):
            card = provider / "abilities" / owner / (ability + ".md")
            self.assertTrue(card.is_file(), f"missing {owner}/{ability}")
            content = card.read_text(encoding="utf-8")
            self.assertIn(f"**Relíquia owner — root do inventário:** \x60{owner}\x60", content)
            self.assertIn(f"**Ability root:** \x60{ability}\x60", content)
            self.assertIn(f"**Posição editorial:** {ordinal}/61", content)
            self.assertIn("**Registro literal no inventário:** " + route, content)
            self.assertIn("COUNTED_EXACT", content)
            self.assertIn("**+0 novas identidades**", content)
            self.assertIn("**NÃO VERIFICADOS individualmente**", content)
            self.assertIn("../../ABILITY-INVENTORY-EXACT.md", content)
            self.assertIn("../../EXACT-1.7.7-REL0128-ARTIFACT-AUDIT.md", content)
            self.assertIn(
                f"| {ordinal} | \x60{owner}\x60 | \x60{ability}\x60 | {route} | "
                f"[Abrir](abilities/{owner}/{ability}.md) |",
                index,
            )
        self.assertIn("✅ 61/61 fichas materializadas", index)
        self.assertIn("**+0 novas identidades semânticas**", index)
        for filename in ("README.md", "ABILITY-INVENTORY-EXACT.md"):
            self.assertIn(
                "ABILITY-CARDS-1.7.7-REL0128.md",
                (provider / filename).read_text(encoding="utf-8"),
            )
        self.assertIn("ABILITY-CARDS-1.7.7-REL0128.md", self.index)

    def test_reliquified_artifacts_108_52_owner_scoped_cards(self):
        provider = PROVIDERS / "✅-reliquified-artifacts"
        source = (provider / "ABILITY-INVENTORY-1.0.8.md").read_text(
            encoding="utf-8"
        )
        records = re.findall(
            r"^\| (\d+) \| \x60(artifacts:[a-z0-9_]+)\x60 \| "
            r"\x60([a-z0-9_]+)\x60 \| \x60([A-Za-z][A-Za-z0-9]+)\x60 \|$",
            source, re.MULTILINE,
        )
        self.assertEqual(52, len(records), "source-pinned 1.0.8 has 52 roots")
        self.assertEqual([str(i) for i in range(1, 53)], [r[0] for r in records])
        self.assertEqual(52, len({(r[1], r[2]) for r in records}))
        self.assertEqual(48, len({r[1] for r in records}))
        self.assertEqual(47, len({r[3] for r in records}))
        for duplicated_root in ("drinking", "jump", "meal"):
            self.assertEqual(2, sum(r[2] == duplicated_root for r in records))
        self.assertEqual(
            {"artifacts:plastic_drinking_hat", "artifacts:novelty_drinking_hat"},
            {r[1] for r in records if r[3] == "DrinkingHatItem"},
        )
        self.assertEqual(
            ("artifacts:eternal_steak", "meal", "EternalSteakItem"),
            tuple(records[-1][1:]),
        )
        index = (provider / "ABILITY-CARDS-1.0.8.md").read_text(
            encoding="utf-8"
        )
        pages = sorted((provider / "abilities").rglob("*.md"))
        self.assertEqual(52, len(pages), "one page per owner+root")
        for ordinal, owner, ability, klass in records:
            slug = owner.split(":", 1)[1]
            page = provider / "abilities" / slug / (ability + ".md")
            self.assertTrue(page.is_file(), owner + ":" + ability)
            text = page.read_text(encoding="utf-8")
            self.assertIn("**Owner original:** \x60" + owner + "\x60", text)
            self.assertIn("**Ability root do addon:** \x60" + ability + "\x60", text)
            self.assertIn("**Classe de implementação na fonte 1.0.8:** \x60" + klass + "\x60", text)
            self.assertIn("**Ordinal editorial:** " + ordinal + "/52", text)
            self.assertIn("COUNTED_SOURCE_PINNED", text)
            self.assertIn("**+0 novas identidades semânticas**", text)
            self.assertIn("**NÃO VERIFICADOS individualmente**", text)
            self.assertIn("../../ABILITY-INVENTORY-1.0.8.md", text)
            self.assertIn("../../README.md", text)
            self.assertIn(
                f"| {ordinal} | \x60{owner}\x60 | \x60{ability}\x60 | "
                f"\x60{klass}\x60 | [Abrir](abilities/{slug}/{ability}.md) |",
                index,
            )
            if owner == "artifacts:eternal_steak":
                self.assertIn("mixins de forno e fogueira", text)
                self.assertIn("Sem \x60LootTemplate\x60 local", text)
        self.assertIn("✅ 52/52 habilidades individualizadas", index)
        self.assertIn("**+0 novas identidades semânticas**", index)
        self.assertIn("não \x60COUNTED_EXACT\x60", index)
        self.assertIn("ABILITY-CARDS-1.0.8.md", self.index)
        for doc in ("README.md", "ABILITY-INVENTORY-1.0.8.md"):
            self.assertIn(
                "ABILITY-CARDS-1.0.8.md",
                (provider / doc).read_text(encoding="utf-8"),
            )

    def test_ars_additions_2130_binary_structural_gate(self):
        provider = PROVIDERS / "✅-ars-additions"
        name = "BINARY-REGISTRATION-21.3.0.md"
        doc = (provider / name).read_text(encoding="utf-8")
        rows = re.findall(
            r"^\| ([1-5]) \| \x60(GLYPH|RITUAL)\x60 "
            r"\| \x60([A-Za-z]+)\x60 \| \x60(ars_additions:[^|]+?)\x60 "
            r"\| \x60(NO_BRANCH)\x60 \|$", doc, re.MULTILINE,
        )
        self.assertEqual([
            ("1", "GLYPH", "MethodRetaliate",
             "ars_additions:GlyphLib.prependGlyph(retaliate)", "NO_BRANCH"),
            ("2", "GLYPH", "EffectMark",
             "ars_additions:GlyphLib.prependGlyph(mark)", "NO_BRANCH"),
            ("3", "GLYPH", "MethodRecall",
             "ars_additions:GlyphLib.prependGlyph(recall)", "NO_BRANCH"),
            ("4", "RITUAL", "RitualChunkLoading",
             "ars_additions:ritual_chunk_loading", "NO_BRANCH"),
            ("5", "RITUAL", "RitualLocateStructure",
             "ars_additions:ritual_locate_structure", "NO_BRANCH"),
        ], rows)
        self.assertEqual(3, sum(r[1] == "GLYPH" for r in rows))
        self.assertEqual(2, sum(r[1] == "RITUAL" for r in rows))
        self.assertEqual(5, len({r[2] for r in rows}))
        self.assertIn("ReachPerk", doc)
        self.assertIn("não é um sexto objeto mágico", doc)
        self.assertIn("COUNTED_SOURCE_PINNED", doc)
        self.assertIn("0/39", doc)
        self.assertIn("1/39", doc)
        self.assertIn("ce2440b606acb20b79a42bf7c6c24d163c93241f", doc)
        self.assertIn("38261401056", doc)
        self.assertIn("38261976223", doc)
        tracker = (ROOT / "wiki" / "modpack-catalog" / "meta" /
                   "REVALIDACAO-BINARIA-39-PROVIDERS-2026-10-08.md"
                   ).read_text(encoding="utf-8")
        original = [line for line in tracker.splitlines()
                    if line.startswith("| [") and line.count(" | ") >= 4]
        self.assertEqual(39, len(original))
        self.assertIn("COUNTED_EXACT", original[1])
        for f in ("README.md", "REGISTRIES.md"):
            self.assertIn(name, (provider / f).read_text(encoding="utf-8"))
        self.assertIn(name, self.index)
        self.assertIn("1/39", self.index)

    def test_ars_additions_2130_five_exact_ids_with_host_5131(self):
        provider = PROVIDERS / "✅-ars-additions"
        name = "HOST-GLYPH-IDS-EXACT-5.13.1.md"
        contents = (provider / name).read_text(encoding="utf-8")
        final_rows = re.findall(
            r"^\| ([1-5]) \| \x60(GLYPH|RITUAL)\x60 "
            r"\| \x60([A-Za-z]+)\x60 "
            r"\| \x60(ars_additions:[a-z0-9_]+)\x60 "
            r"\| \x60([a-z_]+)\x60 \|$",
            contents, re.MULTILINE,
        )
        expected = [
            ("1", "GLYPH", "MethodRetaliate",
             "ars_additions:glyph_retaliate", "host_prefix_verified"),
            ("2", "GLYPH", "EffectMark",
             "ars_additions:glyph_mark", "host_prefix_verified"),
            ("3", "GLYPH", "MethodRecall",
             "ars_additions:glyph_recall", "host_prefix_verified"),
            ("4", "RITUAL", "RitualChunkLoading",
             "ars_additions:ritual_chunk_loading", "direct_resource_location"),
            ("5", "RITUAL", "RitualLocateStructure",
             "ars_additions:ritual_locate_structure", "direct_resource_location"),
        ]
        self.assertEqual(expected, final_rows)
        self.assertEqual(5, len({r[3] for r in final_rows}))
        self.assertEqual(3, sum(r[1] == "GLYPH" for r in final_rows))
        self.assertEqual(2, sum(r[1] == "RITUAL" for r in final_rows))
        for s in (
            "02782d071ee5fab3b5c4b8ced67b7e1748277dfd",
            "ce2440b606acb20b79a42bf7c6c24d163c93241f",
            "38266741543", "20107711", "1458261",
            "**✅ 5/5 \x60COUNTED_EXACT\x60 (registro estático).**",
            "**1/39 encerrada para identidade binária**",
            "**38/39 ainda sem prova completa**",
            "**+0** novas",
            "**1851 mínimo global / 1849 mínimo no escopo**",
        ):
            self.assertIn(s, contents)
        self.assertIn("não é uma sexta identidade mágica", contents)
        self.assertIn("⚠️ QA independente não realizada", contents)
        index = (provider / "README.md").read_text(encoding="utf-8")
        self.assertIn(name, index)
        reg = (provider / "REGISTRIES.md").read_text(encoding="utf-8")
        self.assertIn(name, reg)
        tracker = (ROOT / "wiki/modpack-catalog/meta" /
                   "REVALIDACAO-BINARIA-39-PROVIDERS-2026-10-08.md"
                   ).read_text(encoding="utf-8")
        providers = [line for line in tracker.splitlines()
                     if line.startswith("| [") and line.count(" | ") >= 4]
        self.assertEqual(39, len(providers))
        exact = [row for row in providers if "| COUNTED_EXACT |" in row]
        self.assertEqual(15, len(exact))
        self.assertEqual(
            {"Ars Elemental", "Ars Zero", "Ars Technica", "Ars Controle", "Ars Additions", "Ars Hex", "Crystal Chronicles", "Dreamless Spells", "Paladin Spells", "Wind's Spellbooks", "Backported Spellbooks", "Deeper & Darker Spellbooks", "GTBC\'s Geomancy Plus", "Farmer\'s Spell \'n Spellbooks", "Ars \'n\' Spells"},
            {re.search(r"^\| \[([^\]]+)\]", row).group(1) for row in exact},
        )
        other = (ROOT / "wiki/modpack-catalog/meta" /
                 "PENDENCIAS-MAGICAS-ATUAIS.md").read_text(encoding="utf-8")
        self.assertIn("0 novas provas binary-exact", other)
        self.assertIn("JARs fora da categoria Magic", other)
        self.assertIn("2/39", other)
        self.assertIn("37/39", other)
        ledger = (ROOT / "wiki/modpack-catalog/meta" /
                  "SEMANTIC-MAGIC-COVERAGE.md").read_text(encoding="utf-8")
        entry = next(row for row in ledger.splitlines()
                     if row.startswith("| [Ars Additions]"))
        self.assertIn("| 21.3.0 | 5 | \x60COUNTED_EXACT\x60 |", entry)
        self.assertIn(name, ledger)
        self.assertIn(name, self.index)

    def test_ars_hex_504b_single_conditional_physical_binary_registry(self):
        provider = PROVIDERS / "✅-ars-hex"
        name = "EXACT-BINARY-GLYPH-5.0.4b.md"
        note = (provider / name).read_text(encoding="utf-8")
        entries = re.findall(
            r"^\| (1) \| \x60(ars_hex)\x60 \| \x60(EffectSoulShatter)\x60 "
            r"\| \x60(ars_hex:glyph_soul_shatter)\x60 "
            r"\| \x60(ModList\.isLoaded\(malum\))\x60 "
            r"\| \x60(EXACT_BINARY_STATIC)\x60 \|$",
            note, re.MULTILINE,
        )
        self.assertEqual([(
            "1", "ars_hex", "EffectSoulShatter",
            "ars_hex:glyph_soul_shatter", "ModList.isLoaded(malum)",
            "EXACT_BINARY_STATIC",
        )], entries)
        for marker in (
            "38291974275",
            "2354710ea312e2a6e0fbc3eb2dbafb8e06f10cf4",
            "273389",
            "**2/39**", "**37/39**",
            "**+0** novos objetos",
            "PerkRegistry.registerPerk",
            "SoulWardPerk", "MagicProficencyPerk", "SpiritSpoilsPerk",
            "⚠️ Fora do escopo da prova",
            "1851", "1849",
        ):
            self.assertIn(marker, note)
        for filename in ("README.md", "REGISTRIES.md",
                         "GLYPH-CARDS-5.0.4b.md", "glyphs/soul-shatter.md"):
            self.assertIn(name, (provider / filename).read_text(
                encoding="utf-8"
            ))
        tracker = (ROOT / "wiki/modpack-catalog/meta" /
                   "REVALIDACAO-BINARIA-39-PROVIDERS-2026-10-08.md"
                   ).read_text(encoding="utf-8")
        roster = [line for line in tracker.splitlines()
                  if line.startswith("| [") and line.count(" | ") >= 4]
        self.assertEqual(39, len(roster))
        exact = [line for line in roster if "| COUNTED_EXACT |" in line]
        self.assertEqual(15, len(exact))
        self.assertEqual(
            {"Ars Elemental", "Ars Zero", "Ars Technica", "Ars Controle", "Ars Additions", "Ars Hex", "Crystal Chronicles", "Dreamless Spells", "Paladin Spells", "Wind's Spellbooks", "Backported Spellbooks", "Deeper & Darker Spellbooks", "GTBC\'s Geomancy Plus", "Farmer\'s Spell \'n Spellbooks", "Ars \'n\' Spells"},
            {re.search(r"^\| \[([^\]]+)\]", line).group(1) for line in exact},
        )
        self.assertIn(name, tracker)
        ledger = (ROOT / "wiki/modpack-catalog/meta" /
                  "SEMANTIC-MAGIC-COVERAGE.md").read_text(encoding="utf-8")
        hexrow = next(line for line in ledger.splitlines()
                      if line.startswith("| [Ars Hex]"))
        self.assertIn("| 5.0.4b | 1 | \x60COUNTED_EXACT\x60 |", hexrow)
        self.assertIn(name, ledger)
        self.assertIn("2/39", self.index)
        self.assertIn("37/39", self.index)
        self.assertIn(name, self.index)

    def test_crystal_chronicles_static_binary_013_has_exact_registration_only(self):
        provider = PROVIDERS / '✅-crystal-chronicles'
        name = 'EXACT-BINARY-SPELL-0.1.3-alpha.md'
        note = (provider / name).read_text(encoding='utf-8')
        for marker in (
            '8346590', '38298343874',
            'afdc32ab27661cd52160280dc4273d70a2d4a3d2',
            '2192223', 'crystal_chronicles:prismatic_portal',
            'STATIC_BINARY_REGISTRATION_INVOCATIONS=1',
            '3/39', '36/39', '1851', '1849', 'Survival', '+0',
        ):
            self.assertIn(marker, note)
        for path in ('README.md', 'SPELL-CARDS-0.1.3-alpha.md',
                     'spells/prismatic-portal.md'):
            self.assertIn(name, (provider / path).read_text(encoding='utf-8'))
        matrix = (ROOT / 'wiki/modpack-catalog/meta' /
                  'REVALIDACAO-BINARIA-39-PROVIDERS-2026-10-08.md').read_text(encoding='utf-8')
        row = next(x for x in matrix.splitlines() if x.startswith('| [Crystal Chronicles]'))
        self.assertIn('| 0.1.3-alpha | 1 | COUNTED_EXACT |', row)
        ledger = (ROOT / 'wiki/modpack-catalog/meta' /
                  'SEMANTIC-MAGIC-COVERAGE.md').read_text(encoding='utf-8')
        line = next(x for x in ledger.splitlines() if x.startswith('| [Crystal Chronicles]'))
        self.assertIn('| 0.1.3-alpha | 1 | `COUNTED_EXACT` |', line)
        self.assertIn('3/39', self.index)
        self.assertIn('36/39', self.index)

    def test_dreamless_spells_119_exact_four_static_registry_ids(self):
        provider = PROVIDERS / '✅-dreamless-spells'
        name = 'EXACT-BINARY-SPELLS-1.1.9.md'
        note = (provider / name).read_text(encoding='utf-8')
        expected = (
            'dreamless_spells:jadeskin', 'dreamless_spells:drained',
            'dreamless_spells:dullard', 'dreamless_spells:doorway_effect',
        )
        for marker in (
            '7905334', '38302406303',
            'd51960bfb8af1aafa5d716ef9a48c3135f36b956',
            '443506', 'STATIC_SPELL_FACTORY_INVOCATIONS=4',
            'DEFERRED_REGISTER_HELPER_INVOCATIONS=1',
            '4/39', '35/39', '1851', '1849', 'Survival', '+0',
            *expected,
        ):
            self.assertIn(marker, note)
        for file in ('README.md', 'TECHNICAL-AUDIT.md',
                     'ice/jadeskin.md', 'empty/drained.md',
                     'empty/dullard.md', 'empty/mute-doorway-effect.md'):
            self.assertIn(name, (provider / file).read_text(encoding='utf-8'))
        matrix = (ROOT / 'wiki/modpack-catalog/meta' /
                  'REVALIDACAO-BINARIA-39-PROVIDERS-2026-10-08.md').read_text(encoding='utf-8')
        row = next(x for x in matrix.splitlines() if x.startswith('| [Dreamless Spells]'))
        self.assertIn('| 1.1.9 | 4 | COUNTED_EXACT |', row)
        ledger = (ROOT / 'wiki/modpack-catalog/meta' /
                  'SEMANTIC-MAGIC-COVERAGE.md').read_text(encoding='utf-8')
        record = next(x for x in ledger.splitlines() if x.startswith('| [Dreamless Spells]'))
        self.assertIn('| 1.1.9 | 4 | `COUNTED_EXACT` |', record)
        self.assertIn('4/39', self.index)
        self.assertIn('35/39', self.index)

    def test_paladin_spells_111_exact_five_static_binary_registrations(self):
        provider = PROVIDERS / '✅-paladin-spells'
        name = 'EXACT-BINARY-SPELLS-1.1.1.md'
        proof = (provider / name).read_text(encoding='utf-8')
        expected_ids = (
            'paladin_spells:taunt', 'paladin_spells:bulwark',
            'paladin_spells:sworn_protector', 'paladin_spells:bedrock_skin',
            'paladin_spells:ram',
        )
        for marker in (
            '8661566', '38308575364',
            'e4c6f4fa70989f0b9f1819e46e29f68d414ccbaf',
            '1858683', 'STATIC_DEFERRED_REGISTER_INVOCATIONS=5',
            'ENTRYPOINT_TO_REGISTRY=present',
            '5/39', '34/39', '1851', '1849', 'Survival', '+0',
            *expected_ids,
        ):
            self.assertIn(marker, proof)
        for path in ('README.md', 'TECHNICAL-AUDIT.md',
                     'holy/README.md', 'holy/taunt.md', 'holy/bulwark.md',
                     'holy/sworn-protector.md', 'holy/bedrock-skin.md',
                     'holy/ram.md'):
            self.assertIn(name, (provider / path).read_text(encoding='utf-8'))
        roster = (ROOT / 'wiki/modpack-catalog/meta' /
                  'REVALIDACAO-BINARIA-39-PROVIDERS-2026-10-08.md').read_text(encoding='utf-8')
        row = next(x for x in roster.splitlines() if x.startswith('| [Paladin Spells]'))
        self.assertIn('| 1.1.1 | 5 | COUNTED_EXACT |', row)
        ledger = (ROOT / 'wiki/modpack-catalog/meta' /
                  'SEMANTIC-MAGIC-COVERAGE.md').read_text(encoding='utf-8')
        entry = next(x for x in ledger.splitlines() if x.startswith('| [Paladin Spells]'))
        self.assertIn('| 1.1.1 | 5 | `COUNTED_EXACT` |', entry)
        self.assertIn('5/39', self.index)
        self.assertIn('34/39', self.index)

    def test_winds_spellbooks_105_binary_static_registry_seven_ids(self):
        provider = PROVIDERS / '✅-winds-spellbooks'
        name = 'EXACT-BINARY-SPELLS-1.0.5.md'
        proof = (provider / name).read_text(encoding='utf-8')
        expected = (
            'wind_spellbooks:wind_jump', 'wind_spellbooks:tornado',
            'wind_spellbooks:iron_slash', 'wind_spellbooks:aeropic',
            'wind_spellbooks:almighty_push', 'wind_spellbooks:wind_blade',
            'wind_spellbooks:tailwind',
        )
        for marker in (
            '8485822', '38312284152',
            '8744886899bc245ae147a44baa2b183689cec7da',
            '459532', 'STATIC_REGISTER_SPELL_INVOCATIONS=7',
            'ENTRYPOINT_TO_REGISTRY=present', 'ACROBATICS_SPELL',
            '6/39', '33/39', '1851', '1849', '+0', 'Survival', *expected,
        ):
            self.assertIn(marker, proof)
        rows = [x for x in proof.splitlines() if x.startswith('| ')
                and 'wind_spellbooks:' in x]
        self.assertEqual(7, len(rows))
        for path in ('README.md', 'TECHNICAL-AUDIT.md',
                     'wind/wind-jump.md', 'wind/tornado.md',
                     'wind/iron-slash.md', 'wind/aeropic.md',
                     'wind/almighty-push.md', 'wind/wind-blade.md',
                     'wind/tailwind.md'):
            self.assertIn(name, (provider / path).read_text(encoding='utf-8'))
        matrix = (ROOT / 'wiki/modpack-catalog/meta' /
                  'REVALIDACAO-BINARIA-39-PROVIDERS-2026-10-08.md').read_text(encoding='utf-8')
        entry = next(x for x in matrix.splitlines() if x.startswith("| [Wind's Spellbooks]"))
        self.assertIn('| 1.0.5 | 7 | COUNTED_EXACT |', entry)
        ledger = (ROOT / 'wiki/modpack-catalog/meta' /
                  'SEMANTIC-MAGIC-COVERAGE.md').read_text(encoding='utf-8')
        row = next(x for x in ledger.splitlines() if x.startswith("| [Wind's Spellbooks]"))
        self.assertIn('| 1.0.5 | 7 | `COUNTED_EXACT` |', row)
        self.assertIn('6/39', self.index)
        self.assertIn('33/39', self.index)

    def test_backported_spellbooks_012_exact_six_static_binary_registrations(self):
        provider = PROVIDERS / '✅-backported-spellbooks'
        name = 'EXACT-BINARY-SPELLS-0.1.2.md'
        proof = (provider / name).read_text(encoding='utf-8')
        expected = (
            'backportedspellbooks:slime_aspect',
            'backportedspellbooks:sulfur_bomb',
            'backportedspellbooks:sulfur_clouds',
            'backportedspellbooks:sulfur_release',
            'backportedspellbooks:pale_thorn',
            'backportedspellbooks:resin_spray',
        )
        for marker in (
            '8158731', '38318268989',
            '747847c1f38c73250ebac05ea06b41a381187850',
            '209868', '0.1.2', '0.1.0',
            'OWNED_SPELL_CLASS_COUNT=6',
            'STATIC_REGISTER_SPELL_INVOCATIONS=6',
            'ENTRYPOINT_TO_REGISTRY=present',
            'SulfurBombSPell', 'AbstractPaleSpells',
            '7/39', '32/39', '1851', '1849', '+0', 'Survival',
            *expected,
        ):
            self.assertIn(marker, proof)
        rows = [x for x in proof.splitlines() if x.startswith('| ')
                and 'backportedspellbooks:' in x]
        self.assertEqual(6, len(rows))
        paths = ('README.md', 'SPELLS-AND-IRON-RUNTIME.md',
                 'EVIDENCE-AND-PROVENANCE.md', 'spells/README.md',
                 'spells/slime-aspect.md', 'spells/sulfur-bomb.md',
                 'spells/sulfur-clouds.md', 'spells/sulfur-release.md',
                 'spells/pale-thorn.md', 'spells/resin-spray.md')
        for path in paths:
            self.assertIn(name, (provider / path).read_text(encoding='utf-8'))
        matrix = (ROOT / 'wiki/modpack-catalog/meta' /
                  'REVALIDACAO-BINARIA-39-PROVIDERS-2026-10-08.md').read_text(encoding='utf-8')
        row = next(x for x in matrix.splitlines() if x.startswith('| [Backported Spellbooks]'))
        self.assertIn('| physical 0.1.2 / embedded 0.1.0 | 6 | COUNTED_EXACT |', row)
        ledger = (ROOT / 'wiki/modpack-catalog/meta' /
                  'SEMANTIC-MAGIC-COVERAGE.md').read_text(encoding='utf-8')
        entry = next(x for x in ledger.splitlines() if x.startswith('| [Backported Spellbooks]'))
        self.assertIn('| physical 0.1.2 / embedded 0.1.0 | 6 | `COUNTED_EXACT` |', entry)
        self.assertIn('7/39', self.index)
        self.assertIn('32/39', self.index)

    def test_deeper_darker_133_version_b_four_exact_static_summons(self):
        provider = PROVIDERS / '✅-deeper-and-darker-spellbooks'
        name = 'EXACT-BINARY-SUMMONS-1.3.3-VER-B.md'
        proof = (provider / name).read_text(encoding='utf-8')
        expected = (
            'darkermagic:summoned_warden',
            'darkermagic:summoned_shattered',
            'darkermagic:summoned_sculk_centipede',
            'darkermagic:summoned_sculk_snapper',
        )
        for marker in (
            '7897469', '38329132941',
            '783123ae86c91c01527c10f338679caaef42eb42',
            '100219', 'Version B', '1.3.3', '1.3.0',
            'net.rev.darkermagic.registeries.DDISSSpellRegistery',
            'net.rev.darkermagic.item.DDISSSpellRegistery',
            'OWNED_SPELL_CLASS_COUNT=4',
            'STATIC_REGISTER_SPELL_INVOCATIONS=4',
            'ENTRYPOINT_TO_REGISTRY=True',
            '8/39', '31/39', '1851', '1849', '+0', 'Survival',
            *expected,
        ):
            self.assertIn(marker, proof)
        rows = [x for x in proof.splitlines() if x.startswith('| ')
                and 'darkermagic:' in x]
        self.assertEqual(4, len(rows))
        for path in ('README.md', 'TECHNICAL-AUDIT.md',
                     'eldritch/summoned-warden.md',
                     'eldritch/summoned-shattered.md',
                     'eldritch/summoned-sculk-centipede.md',
                     'eldritch/summoned-sculk-snapper.md'):
            self.assertIn(name, (provider / path).read_text(encoding='utf-8'))
        meta = ROOT / 'wiki/modpack-catalog/meta'
        matrix = (meta / 'REVALIDACAO-BINARIA-39-PROVIDERS-2026-10-08.md').read_text(encoding='utf-8')
        row = next(x for x in matrix.splitlines()
                   if x.startswith('| [Deeper & Darker Spellbooks]'))
        self.assertIn('| 1.3.3 Version B | 4 | COUNTED_EXACT |', row)
        ledger = (meta / 'SEMANTIC-MAGIC-COVERAGE.md').read_text(encoding='utf-8')
        entry = next(x for x in ledger.splitlines()
                     if x.startswith('| [Deeper & Darker Spellbooks]'))
        self.assertIn('| 1.3.3 Version B | 4 | `COUNTED_EXACT` |', entry)
        self.assertIn('8/39', self.index)
        self.assertIn('31/39', self.index)

    def test_gtbc_110_binary_static_twelve_spells(self):
        provider = PROVIDERS / '✅-gtbcs-geomancy-plus'
        name = 'EXACT-BINARY-SPELLS-1.1.0-1.21.1.md'
        proof = (provider / name).read_text(encoding='utf-8')
        ids = ('chunker', 'dripstone_bolt', 'eroding_boulder', 'fissure',
               'geo_conductor', 'petrivise', 'pillar_of_the_resounding_earth',
               'seismic_surf', 'tremor_spike', 'tremor_step',
               'solar_beam', 'solar_storm')
        for marker in ('7041615', '38332395627',
                       '67e9652799f35f1fbd09968da6f400d0229f5599',
                       '475333', 'GGSpells', 'GeomancyPlusMod',
                       'EarthshatterSpell', 'STATIC_REGISTER_SPELL_INVOCATIONS=12',
                       'STATIC_INITIALIZER_BRANCHES=0', '9/39',
                       '30/39', '1851', '1849', '+0', 'Survival',
                       *(f'gtbcs_geomancy_plus:{id}' for id in ids)):
            self.assertIn(marker, proof)
        rows = [x for x in proof.splitlines()
                if x.startswith('| ') and 'gtbcs_geomancy_plus:' in x]
        self.assertEqual(12, len(rows))
        for card in ('README.md', 'EXACT-1.1.0-ARTIFACT-AUDIT.md',
                     'SPELL-CARDS-1.1.0-1.21.1.md'):
            self.assertIn(name, (provider / card).read_text(encoding='utf-8'))
        meta = ROOT / 'wiki/modpack-catalog/meta'
        matrix = (meta / 'REVALIDACAO-BINARIA-39-PROVIDERS-2026-10-08.md').read_text(encoding='utf-8')
        row = next(x for x in matrix.splitlines()
                   if x.startswith("| [GTBC's Geomancy Plus]"))
        self.assertIn('| 1.1.0-1.21.1 | 12 | COUNTED_EXACT |', row)
        ledger = (meta / 'SEMANTIC-MAGIC-COVERAGE.md').read_text(encoding='utf-8')
        entry = next(x for x in ledger.splitlines()
                     if x.startswith("| [GTBC's Geomancy Plus]"))
        self.assertIn('| 1.1.0-1.21.1 | 12 | `COUNTED_EXACT` |', entry)
        self.assertIn('9/39', self.index)
        self.assertIn('30/39', self.index)

    def test_farmers_spell_1051_exact_six_static_registry_ids(self):
        provider = PROVIDERS / '✅-farmers-spell'
        name = 'EXACT-BINARY-SPELLS-1.0.5.1.md'
        proof = (provider / name).read_text(encoding='utf-8')
        ids = ('goodberry', 'phantom_loot', 'seal_coat', 'bad_apple',
               'chaos_slash', 'preserve_circle')
        for marker in ('8760428', '38334052069',
                       'f77355e029af39bbaba3854e10cc087a608351ff',
                       '5537418', 'ModSpells', 'FarmersSpell',
                       'BerserkCleaverSpell',
                       'STATIC_DEFERRED_REGISTER_INVOCATIONS=6',
                       'STATIC_INITIALIZER_BRANCHES=0',
                       'ENTRYPOINT_TO_REGISTRY=True',
                       '10/39', '29/39', '1851', '1849', '+0',
                       'Survival', *(f'farmers_spell:{ident}' for ident in ids)):
            self.assertIn(marker, proof)
        rows = [x for x in proof.splitlines()
                if x.startswith('| ') and 'farmers_spell:' in x]
        self.assertEqual(6, len(rows))
        self.assertEqual(6, len(set(rows)))
        for path in ('README.md', 'EXACT-1.0.5.1-SPELL-INVENTORY.md',
                     'SPELL-CARDS-1.0.5.1.md',
                     'spells/goodberry.md', 'spells/phantom-loot.md',
                     'spells/seal-coat.md', 'spells/bad-apple.md',
                     'spells/chaos-slash.md', 'spells/preserve-circle.md'):
            self.assertIn(name, (provider / path).read_text(encoding='utf-8'))
        inventory = (provider / 'EXACT-1.0.5.1-SPELL-INVENTORY.md').read_text(encoding='utf-8')
        registry_rows = [x for x in inventory.splitlines()
                         if x.startswith('| `farmers_spell:')]
        self.assertEqual(6, len(registry_rows))
        self.assertTrue(all('`COUNTED_EXACT`' in x for x in registry_rows))
        meta = ROOT / 'wiki/modpack-catalog/meta'
        matrix = (meta / 'REVALIDACAO-BINARIA-39-PROVIDERS-2026-10-08.md').read_text(encoding='utf-8')
        row = next(x for x in matrix.splitlines()
                   if x.startswith("| [Farmer's Spell 'n Spellbooks]"))
        self.assertIn('| 1.0.5.1-1.21.1 | 6 | COUNTED_EXACT |', row)
        ledger = (meta / 'SEMANTIC-MAGIC-COVERAGE.md').read_text(encoding='utf-8')
        entry = next(x for x in ledger.splitlines()
                     if x.startswith("| [Farmer's Spell 'n Spellbooks]"))
        self.assertIn('| 1.0.5.1-1.21.1 | 6 | `COUNTED_EXACT` |', entry)
        self.assertIn('10/39', self.index)
        self.assertIn('29/39', self.index)

    def test_ars_n_spells_334_exact_five_gated_rituals_and_eight_proxies(self):
        provider = PROVIDERS / '✅-ars-n-spells'
        name = 'EXACT-BINARY-RITUALS-3.3.4.md'
        proof = (provider / name).read_text(encoding='utf-8')
        ids = ('spell_uninscription', 'mana_infusion',
               'spell_transcription', 'mana_well', 'spellbook_binding')
        for marker in (
            '8881108', '38336011675',
            '53966330a468e626cd6469259af6778a5a7d9305',
            '2222971', 'RitualRegistryHandler', 'ArsCrossProxyRegistry',
            'RITUAL_REGISTRATION_CALLS=5',
            'IRON_SPELLBOOKS_RITUAL_GATE=True',
            'RITUAL_GATE_ORDER=UNINSCRIPTION_BEFORE_IRONS_CHECK_BEFORE_FOUR_OTHERS',
            'ENTRYPOINT_TO_RITUAL_REGISTRAR=True',
            'PROXY_POOL_SIZE=8', 'PROXY_SEMANTIC_ROOTS_ADDED=0',
            '11/39', '28/39', '1851', '1849', '+0',
            'Survival', *(f'ars_n_spells:{id}' for id in ids),
        ):
            self.assertIn(marker, proof)
        rows = [x for x in proof.splitlines()
                if x.startswith('| ') and 'ars_n_spells:' in x]
        self.assertEqual(5, len(rows))
        self.assertEqual(5, len(set(rows)))
        self.assertTrue(any('ALWAYS' in x for x in rows))
        self.assertEqual(4, sum('IRONS_GATED' in x for x in rows))
        self.assertEqual(0, sum('ars_cross_' in x for x in rows))
        for path in ('README.md', 'EVIDENCE-AND-PROVENANCE.md',
                     'rituals/README.md', 'rituals/spell-uninscription.md',
                     'rituals/mana-infusion.md', 'rituals/spell-transcription.md',
                     'rituals/mana-well.md', 'rituals/spellbook-binding.md',
                     'systems/cross-casting-and-proxy-pool.md'):
            self.assertIn(name, (provider / path).read_text(encoding='utf-8'))
        meta = ROOT / 'wiki/modpack-catalog/meta'
        matrix = (meta / 'REVALIDACAO-BINARIA-39-PROVIDERS-2026-10-08.md').read_text(encoding='utf-8')
        row = next(x for x in matrix.splitlines()
                   if x.startswith("| [Ars 'n' Spells]"))
        self.assertIn('| 3.3.4 | 5 | COUNTED_EXACT |', row)
        ledger = (meta / 'SEMANTIC-MAGIC-COVERAGE.md').read_text(encoding='utf-8')
        entry = next(x for x in ledger.splitlines()
                     if x.startswith("| [Ars 'n' Spells]"))
        self.assertIn('| 3.3.4 | 5 | `COUNTED_EXACT` |', entry)
        self.assertIn('11/39', self.index)
        self.assertIn('28/39', self.index)

    def test_current_status_does_not_promote_runtime(self):
        self.assertIn("164/164 diretórios", self.index)
        self.assertIn("97/97 dossiês", self.index)
        self.assertIn("denominador semântico final permanece aberto", self.index)
        self.assertIn("COUNTED_RELEASE_BOUNDED", self.cards)
        self.assertIn("não verificados", self.cards)


if __name__ == "__main__":
    unittest.main()
