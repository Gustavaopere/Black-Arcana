#!/usr/bin/env python3
"""Read-only bytecode check for GazingPearlItem.getPearlColor (publisher 1.0.10).

This checks a SHA-exact prior discovery and JVM operations only. It does not
execute the game, reproduce renderer behavior or certify perk mutating hooks.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path

OWNER = 'com/github/alexmodguy/alexscaves/server/item/GazingPearlItem'
PUBLISHER_SHA256 = '36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c'
CLASS_SHA256 = '2519bc5aed494deccc0423053ea42904314511094b29cd1e4025cc65a08a5a07'
REPORT_SHA256 = 'd73959ca968bd23e57240d2fb3943e400362af9da92940af7343e93f47ff01c5'
REPORT_BYTES = 301601
METHOD_DESCRIPTOR = '(Lnet/minecraft/world/item/ItemStack;)I'
METHOD_CODE_SHA256 = '0b2790fa924d0e99c0acf32b85906e4b9ea72ca3a8807ec0c14419e33e400630'
METHOD_INSTRUCTION_SHA256 = 'e4bffbeaf3e572d06916a5e34bb84399f8114cf52c203cda0d2d67ebfac6c6cc'

# Each row: JVM offset, exact opcode, operand substring (or None), symbol substring (or None).
PIVOTS = [
    (1, 'invokestatic', None, 'ACCompat.getTag:'),
    (6, 'ifnull', '71', None),
    (10, 'ldc', 'HasReputation', None),
    (12, 'invokestatic', None, 'ACCompat.getBoolean:'),
    (15, 'ifeq', '71', None),
    (18, 'invokestatic', None, 'System.currentTimeMillis:'),
    (21, 'l2f', None, None),
    (22, 'ldc', '4000.0f', None),
    (24, 'fdiv', None, None),
    (25, 'f2d', None, None),
    (26, 'invokestatic', None, 'Math.sin:'),
    (29, 'dconst_1', None, None),
    (30, 'dadd', None, None),
    (31, 'd2f', None, None),
    (32, 'ldc', '0.5f', None),
    (34, 'fmul', None, None),
    (39, 'invokestatic', None, 'ACCompat.getInt:'),
    (43, 'bipush', '100', None),
    (46, 'isub', None, None),
    (47, 'istore', '4', None),
    (49, 'iload', '4', None),
    (51, 'i2f', None, None),
    (52, 'ldc', '200.0f', None),
    (54, 'fdiv', None, None),
    (56, 'ldc', '0.3f', None),
    (58, 'fmul', None, None),
    (59, 'ldc', '0.7f', None),
    (61, 'fadd', None, None),
    (62, 'fconst_1', None, None),
    (63, 'invokestatic', None, 'Color.HSBtoRGB:'),
    (71, 'invokestatic', None, 'System.currentTimeMillis:'),
    (74, 'ldc2_w', '10000l', None),
    (77, 'lrem', None, None),
    (78, 'l2f', None, None),
    (79, 'ldc', '10000.0f', None),
    (81, 'fdiv', None, None),
    (83, 'invokestatic', None, 'System.currentTimeMillis:'),
    (86, 'l2f', None, None),
    (87, 'ldc', '4000.0f', None),
    (89, 'fdiv', None, None),
    (90, 'f2d', None, None),
    (91, 'invokestatic', None, 'Math.sin:'),
    (99, 'fmul', None, None),
    (103, 'ldc', '0.3f', None),
    (105, 'fmul', None, None),
    (106, 'ldc', '0.7f', None),
    (108, 'fadd', None, None),
    (109, 'fconst_1', None, None),
    (110, 'invokestatic', None, 'Color.HSBtoRGB:'),
]


def no_duplicates(pairs):
    out = {}
    for key, value in pairs:
        assert key not in out, 'duplicate report JSON key: '+key
        out[key] = value
    return out


def verify_color_method(method):
    declaration = method['declaration']
    assert (declaration['name'], declaration['descriptor']) == (
        'getPearlColor', METHOD_DESCRIPTOR)
    assert declaration['access'] == 9  # public static, not a mutating hook
    assert declaration['code_sha256'] == METHOD_CODE_SHA256
    assert declaration['code_size'] == 118
    assert method['instruction_count'] == len(method['instructions']) == 73
    assert method['instruction_sha256'] == METHOD_INSTRUCTION_SHA256
    ins = method['instructions']
    at = {v['offset']: v for v in ins}
    assert len(at) == len(ins) and sorted(at) == [v['offset'] for v in ins]
    for offset, opcode, operand, symbol in PIVOTS:
        assert offset in at, ('missing JVM pivot', offset)
        row = at[offset]
        assert row['opcode'] == opcode, ('opcode drift', offset)
        if operand is not None:
            assert operand in row['operand'] or operand in row['symbol'], ('constant/operand drift', offset)
        if symbol is not None:
            assert symbol in row['symbol'], ('method ref drift', offset)
    assert [(x['offset'], x['opcode']) for x in ins if x['opcode'] in ('ifnull','ifeq')] == [
        (6, 'ifnull'), (15, 'ifeq')]
    assert [x['offset'] for x in ins if 'System.currentTimeMillis:' in x['symbol']] == [18,71,83]
    assert [x['offset'] for x in ins if 'Color.HSBtoRGB:' in x['symbol']] == [63,110]


def check(report_path: Path):
    raw = report_path.read_bytes()
    assert len(raw) == REPORT_BYTES and hashlib.sha256(raw).hexdigest() == REPORT_SHA256
    report = json.loads(raw, object_pairs_hook=no_duplicates)
    assert report['schema_version'] == 1
    assert report['scope'] == 'GAZING_PEARL_PUBLISHER_DISCOVERY_NOT_CERTIFIED'
    assert report['artifact']['sha256'] == PUBLISHER_SHA256
    assert report['static_contract'] == 'NOT_CERTIFIED'
    assert report['mutating_hook'] == 'NOT_VERIFIED'
    assert report['mutation'] == 'NO_MUTATION'
    cls = report['native']['targets'][OWNER]
    assert cls['class_sha256'] == CLASS_SHA256
    assert len(cls['methods']) == 5
    matches = [m for m in cls['methods'] if m['declaration']['name'] == 'getPearlColor']
    assert len(matches) == 1
    method = matches[0]
    verify_color_method(method)
    for offset, bad_value in [(21, 'l2d'),(83, 'different_clock')]:
        altered = copy.deepcopy(method)
        modified = next(x for x in altered['instructions'] if x['offset'] == offset)
        if offset == 21:
            modified['opcode'] = bad_value
        else:
            modified['symbol'] = bad_value
        try:
            verify_color_method(altered)
        except AssertionError:
            pass
        else:
            raise AssertionError('forged JVM path accepted at offset '+str(offset))
    print('PASS: GazingPearlItem.getPearlColor exact two-path HSB formula and negative pivots')
    print('NO_MUTATION NOT_CERTIFIED PHYSICAL_QA_NOT_TESTED')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path, required=True)
    check(parser.parse_args().report)
