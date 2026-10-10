#!/usr/bin/env python3
"""Plan binary registry audit for 39 source/release-bounded providers, fail closed.

Consumes only a 69-JAR fingerprint *report*, and never declares registry proof.
It does not inspect the installed modpack, validate report provenance, run mod
code, or count newly discovered spells. All promotion flags remain false.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
MATRIX_PATH = ROOT / 'wiki/modpack-catalog/meta/REVALIDACAO-BINARIA-39-PROVIDERS-2026-10-08.md'
CROSSWALK_PATH = ROOT / 'wiki/modpack-catalog/meta/PHYSICAL-LEDGER-VERSION-RECONCILIATION-2026-10-08.md'
SOURCE_SHA = 'de80b186357cad20ba5b81892a8682777e96e35a'
REPORT_SOURCE = 'PHYSICAL-LEDGER-VERSION-RECONCILIATION-2026-10-08.md'
REPORT_EVIDENCE = 'READ_ONLY_JAR_FINGERPRINT_NOT_REGISTRY_PROOF'
CROSSWALK_LINE = re.compile(r'^\| (?P<provider>[^|]+) \| #\d{3} \| \x60(?P<filename>[^|\x60]+\.jar)\x60 \|')
MATRIX_LINE = re.compile(r'^\| \[(?P<provider>[^|\]]+)\]\([^|)]+\) \| (?P<version>[^|]+) \| (?P<count>\d+) \| (?P<evidence>COUNTED_SOURCE_PINNED|COUNTED_RELEASE_BOUNDED) \|')
SHA1 = re.compile(r'[a-f0-9]{40}\Z')
SHA256 = re.compile(r'[a-f0-9]{64}\Z')
STATUSES = ('FINGERPRINTED', 'MISSING', 'UNSAFE', 'OVERSIZED', 'INVALID_JAR', 'UNREADABLE', 'CHANGED_DURING_SCAN')


def load_crosswalk(path: Path = CROSSWALK_PATH) -> dict[str, str]:
    source = path.read_text(encoding='utf-8')
    if SOURCE_SHA not in source:
        raise ValueError('physical crosswalk source commit mismatch')
    try:
        table = source.split('## Exact-current physical crosswalk', 1)[1].split('## Historical catalogs excluded', 1)[0]
    except IndexError as exc:
        raise ValueError('crosswalk table missing') from exc
    result: dict[str, str] = {}
    for line in table.splitlines():
        match = CROSSWALK_LINE.match(line)
        if not match:
            continue
        name, filename = match.group('provider').strip(), match.group('filename')
        if name in result:
            raise ValueError('duplicate physical provider')
        result[name] = filename
    if len(result) != 69 or len(set(result.values())) != 69:
        raise ValueError('physical crosswalk must have 69 unique providers and files')
    return result


def load_matrix(path: Path = MATRIX_PATH) -> dict[str, dict]:
    source = path.read_text(encoding='utf-8')
    if SOURCE_SHA not in source:
        raise ValueError('binary registry matrix source commit mismatch')
    try:
        table = source.split('| Provider | Linha/version ledger |', 1)[1].split('## Coleta física reproduzível', 1)[0]
    except IndexError as exc:
        raise ValueError('binary registry matrix missing') from exc
    result: dict[str, dict] = {}
    for line in table.splitlines():
        match = MATRIX_LINE.match(line)
        if not match:
            continue
        name = match.group('provider').strip()
        if name in result:
            raise ValueError('duplicate provider in 39-row matrix')
        result[name] = {
            'version': match.group('version').strip(),
            'semantic_objects': int(match.group('count')),
            'catalog_evidence': match.group('evidence'),
        }
    if len(result) != 39:
        raise ValueError(f'expected 39 source/release-bounded providers, found {len(result)}')
    return result


def build_queue(matrix: dict, crosswalk: dict, fingerprint_report: dict) -> dict:
    """Build a queue of remaining work; never convert a fingerprint into spell proof."""
    if (
        not isinstance(matrix, dict) or len(matrix) != 39
        or not isinstance(crosswalk, dict) or len(crosswalk) != 69
        or len(set(crosswalk.values())) != 69 or not set(matrix).issubset(crosswalk)
        or not all(isinstance(n, str) and n for n in crosswalk)
        or not all(isinstance(f, str) and f.endswith('.jar')
                   and '/' not in f and '\\' not in f and f not in ('.', '..')
                   for f in crosswalk.values())
    ):
        raise ValueError('expected 39 matrix rows mapping into 69 exact physical JAR identities')
    for name, src in matrix.items():
        if (
            not isinstance(src, dict) or not isinstance(src.get('version'), str)
            or not src['version'].strip() or not isinstance(src.get('semantic_objects'), int)
            or isinstance(src['semantic_objects'], bool) or src['semantic_objects'] < 0
            or src.get('catalog_evidence') not in ('COUNTED_SOURCE_PINNED', 'COUNTED_RELEASE_BOUNDED')
        ):
            raise ValueError(f'unrecognized semantic ledger evidence: {name}')
    report = fingerprint_report
    if not isinstance(report, dict) or (
        report.get('source') != REPORT_SOURCE or report.get('evidence_class') != REPORT_EVIDENCE
        or report.get('expected') != 69 or type(report.get('expected')) is not int
    ):
        raise ValueError('unrecognized 69-provider fingerprint report')
    rows = report.get('entries')
    if not isinstance(rows, list) or len(rows) != 69:
        raise ValueError('69-provider report must have exactly 69 rows')
    keyed = {}
    counts: Counter[str] = Counter()
    for item in rows:
        if not isinstance(item, dict):
            raise ValueError('invalid physical fingerprint row')
        name, filename, status = (item.get(k) for k in ('provider', 'filename', 'status'))
        if (
            name not in crosswalk or name in keyed or crosswalk[name] != filename
            or status not in STATUSES
        ):
            raise ValueError('unexpected or duplicate physical provider/filename/status')
        if status == 'FINGERPRINTED':
            if not (isinstance(item.get('sha1'), str) and SHA1.fullmatch(item['sha1'])
                    and isinstance(item.get('sha256'), str) and SHA256.fullmatch(item['sha256'])
                    and type(item.get('size_bytes')) is int and 0 < item['size_bytes'] <= 1024**3):
                raise ValueError('missing or malformed physical fingerprint')
        elif any(field in item for field in ('sha1', 'sha256', 'size_bytes')):
            raise ValueError('blocked artifact cannot carry fingerprint')
        keyed[name] = item
        counts[status] += 1
    declared = report.get('counts')
    if (
        not isinstance(declared, dict) or set(declared) != set(STATUSES)
        or any(type(declared[s]) is not int or declared[s] < 0 for s in STATUSES)
        or any(declared[s] != counts[s] for s in STATUSES)
    ):
        raise ValueError('fingerprint counts inconsistent with 69-row payload')
    result_rows = []
    for name, details in sorted(matrix.items()):
        artifact = keyed[name]
        fingerprinted = artifact['status'] == 'FINGERPRINTED'
        record = {
            'provider': name,
            'filename': crosswalk[name],
            'declared_version': details['version'],
            'catalog_evidence': details['catalog_evidence'],
            'existing_semantic_objects': details['semantic_objects'],
            'physical_status': artifact['status'],
            'status': 'FINGERPRINTED_PENDING_REGISTRY' if fingerprinted else 'PHYSICAL_ARTIFACT_BLOCKED',
            'registry_verified': False,
            'survival_verified': False,
            'promotion_allowed': False,
        }
        if fingerprinted:
            record['jar_sha1'] = artifact['sha1']
            record['jar_sha256'] = artifact['sha256']
        result_rows.append(record)
    return {
        'schema': 'black_arcana_39_provider_registry_evidence_queue_v1',
        'evidence': 'REPORT_ONLY_NOT_REGISTRY_OR_SURVIVAL_PROOF',
        'source_commit': SOURCE_SHA,
        'expected_physical_jars': 69,
        'expected_binary_registry_proofs': 39,
        'fingerprinted_pending_registry': sum(x['status'] == 'FINGERPRINTED_PENDING_REGISTRY' for x in result_rows),
        'blocked_physical_artifact': sum(x['status'] == 'PHYSICAL_ARTIFACT_BLOCKED' for x in result_rows),
        'registry_proofs_completed': 0,
        'providers': result_rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fingerprints', type=Path, required=True, help='Output JSON of physical_provider_fingerprint_collector.py')
    args = parser.parse_args()
    try:
        if args.fingerprints.stat().st_size > 1024 * 1024:
            raise ValueError('fingerprint report larger than 1 MiB')
        report = json.loads(args.fingerprints.read_text(encoding='utf-8'))
        result = build_queue(load_matrix(), load_crosswalk(), report)
    except (OSError, UnicodeError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
