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
        self.assertIn("0/12 fichas nominais", index)
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
        self.assertEqual(12, len(pages))
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

    def test_ars_hex_one_source_pinned_glyph_card(self):
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
        self.assertIn("COUNTED_SOURCE_PINNED", card)
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

    def test_current_status_does_not_promote_runtime(self):
        self.assertIn("164/164 diretórios", self.index)
        self.assertIn("97/97 dossiês", self.index)
        self.assertIn("denominador semântico final permanece aberto", self.index)
        self.assertIn("COUNTED_RELEASE_BOUNDED", self.cards)
        self.assertIn("não verificados", self.cards)


if __name__ == "__main__":
    unittest.main()
