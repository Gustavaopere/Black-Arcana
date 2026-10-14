#!/usr/bin/env python3
"""Requiem source-to-publisher discrepancy and global cohort regression."""
from pathlib import Path
import re
import unittest

ROOT=Path(__file__).resolve().parents[2]
META=ROOT/'wiki/modpack-catalog/meta'
PROVIDER=ROOT/'wiki/modpack-catalog/providers/✅-enders-spells-and-stuff-requiem'

class RequiemPhysicalLedgerTests(unittest.TestCase):
    def test_57_compiled_52_semantic_and_source_only_gong(self):
        note=(PROVIDER/'EXACT-BINARY-SPELLS-0.1.7.md').read_text(encoding='utf8')
        source=(PROVIDER/'SOURCE-0.1.7-SPELL-INVENTORY.md').read_text(encoding='utf8')
        rows=re.findall(r'^\\| \\x60ess_requiem:([a-z0-9_]+)\\x60 \\| (COUNTED_SOURCE_PINNED|EXCLUDED) \\|', source, flags=re.M)
        self.assertEqual(58,len(rows))
        self.assertEqual(58,len(set(x for x,_ in rows)))
        self.assertEqual(53,sum(s=='COUNTED_SOURCE_PINNED' for _,s in rows))
        self.assertEqual(5,sum(s=='EXCLUDED' for _,s in rows))
        self.assertIn(('gong','COUNTED_SOURCE_PINNED'),rows)
        for token in ('57/57','52','WEAKENING_GONG','source','38655251099',
                      'c4648cced4f9e96527cfa4e3f5edcdcead43abb1','Stage 06.05'):
            self.assertIn(token,note)
    def test_matrix_29_exact_and_scope_corrected_by_one(self):
        matrix=(META/'REVALIDACAO-BINARIA-39-PROVIDERS-2026-10-08.md').read_text(encoding='utf8')
        entries=[x for x in matrix.splitlines() if x.startswith('| [') and re.search(r' \\| (COUNTED_SOURCE_PINNED|COUNTED_EXACT|COUNTED_RELEASE_BOUNDED) \\|', x)]
        self.assertEqual(39,len(entries))
        self.assertEqual(29,sum('| COUNTED_EXACT |' in x for x in entries))
        row=next(x for x in entries if x.startswith("| [Ender's Spells and Stuff: Requiem]"))
        self.assertIn('| 0.1.7 | 52 | COUNTED_EXACT |',row)
        self.assertIn('gong',row)
        ledger=(META/'SEMANTIC-MAGIC-COVERAGE.md').read_text(encoding='utf8')
        self.assertIn('1856 global / 1854 escopo',ledger)
        self.assertIn('29/39 exatos',ledger)
    def test_provider_queue_does_not_assert_runtime_registry_from_fingerprint(self):
        queue=(ROOT/'docs/qa/provider_39_evidence_queue.py').read_text(encoding='utf8')
        self.assertIn("\"Ender's Spells and Stuff: Requiem\": ('0.1.7', 52)",queue)
        self.assertIn("'registry_proofs_completed': 0",queue)
        self.assertIn("'registry_verified': False",queue)

if __name__=='__main__':
    unittest.main()
