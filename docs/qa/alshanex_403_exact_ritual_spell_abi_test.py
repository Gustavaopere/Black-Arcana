#!/usr/bin/env python3
"""Synthetic regressions; no third-party JAR or code bundled."""
import io
import json
import sys
import unittest
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from alshanex_403_exact_ritual_spell_abi import (
    AuditError, PREFIX, RITUALS, RITUAL_TYPE, SPELL_PREFIX, SPELLS,
    inspect_zip, parse_javap_abi,
)


def fixture_zip(ritual_change=None):
    b = io.BytesIO()
    with zipfile.ZipFile(b, 'w') as z:
        for name in RITUALS:
            r = {'type': RITUAL_TYPE, 'central_item': {'item': 'minecraft:stone'},
                 'inputs': [{'ingredient': {'item': 'minecraft:stick'}, 'count': 1, 'consume': False}],
                 'result': {'id': 'alshanex_familiars:' + name}}
            if ritual_change and name == RITUALS[0]:
                ritual_change(r)
            z.writestr(PREFIX + name + '.json', json.dumps(r))
        for c in SPELLS.values():
            z.writestr(SPELL_PREFIX + c + '.class', b'fixture is NOT executable')
    b.seek(0)
    return zipfile.ZipFile(b)


class TestAudit(unittest.TestCase):
    def test_good_fixture(self):
        with fixture_zip() as z:
            rows = inspect_zip(z)
        self.assertEqual(len(rows), 11)
        self.assertEqual(rows[0]['inputs_count'], 1)
        self.assertTrue(rows[0]['input_shapes'][0]['consume_false'])
        self.assertNotIn('minecraft:stick', json.dumps(rows))

    def test_reject_result_drift(self):
        with fixture_zip(lambda r: r.update({'result': {'id': 'familiarslib:familiar_egg'}})) as z:
            with self.assertRaises(AuditError):
                inspect_zip(z)

    def test_reject_type_drift(self):
        with fixture_zip(lambda r: r.update({'type': 'minecraft:crafting_shaped'})) as z:
            with self.assertRaises(AuditError):
                inspect_zip(z)

    def test_reject_unexpected_ritual(self):
        b = io.BytesIO()
        with zipfile.ZipFile(b,'w') as z:
            z.writestr(PREFIX + 'not_registered.json', '{}')
        b.seek(0)
        with zipfile.ZipFile(b) as z:
            with self.assertRaises(AuditError):
                inspect_zip(z)

    def test_reject_duplicate_json_keys(self):
        b = io.BytesIO()
        with zipfile.ZipFile(b,'w') as z:
            for name in RITUALS:
                if name == RITUALS[0]:
                    payload = '{"type":"alshanex_familiars:ritual_recipe","type":"alshanex_familiars:ritual_recipe","result":"alshanex_familiars:archmage_shard"}'
                else:
                    payload = json.dumps({'type': RITUAL_TYPE, 'result': 'alshanex_familiars:' + name})
                z.writestr(PREFIX + name + '.json', payload)
            for c in SPELLS.values():
                z.writestr(SPELL_PREFIX + c + '.class', b'placeholder')
        b.seek(0)
        with zipfile.ZipFile(b) as z:
            with self.assertRaises(AuditError):
                inspect_zip(z)

    def test_javap_abi_only(self):
        out = 'public class X {\n  public void cast(java.lang.Object);\n    descriptor: (Ljava/lang/Object;)V\n  private int getLevel();\n    descriptor: ()I\n}'
        self.assertEqual(parse_javap_abi(out, 'X'), [
            {'name': 'cast','descriptor': '(Ljava/lang/Object;)V'},
            {'name': 'getLevel','descriptor': '()I'},
        ])
        with self.assertRaises(AuditError):
            parse_javap_abi('public class X {}', 'X')


if __name__ == '__main__':
    unittest.main()
