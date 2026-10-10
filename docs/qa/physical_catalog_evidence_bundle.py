#!/usr/bin/env python3
"""Run the existing bounded, read-only physical catalog evidence collectors.

This is a report-capture orchestrator, not a spell/registry certification tool.
All evidence classes, gates, and catalog statuses remain with their owners.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
QA = ROOT / 'docs/qa'
SNAPSHOT = 'de80b186357cad20ba5b81892a8682777e96e35a'


def _load_report(path: Path) -> dict | None:
    try:
        if not path.is_file() or path.stat().st_size > 16 * 1024 * 1024:
            return None
        result = json.loads(path.read_text(encoding='utf-8'))
    except (OSError, UnicodeError, ValueError):
        return None
    return result if isinstance(result, dict) else None



def _valid_collector_report(name: str, doc: dict | None, exit_code: int) -> bool:
    """Validate report identity/shape, not claimed physical or spell provenance."""
    if not isinstance(doc, dict):
        return False
    if name == 'nonmagic_489':
        rows, statuses = doc.get('rows'), doc.get('statuses')
        if not (exit_code == 0
                and doc.get('schema') == 'black_arcana_nonmagic_jar_triage_v1'
                and doc.get('source_commit') == SNAPSHOT
                and doc.get('evidence') == 'ZIP_MEMBER_NAME_HINTS_AND_SHA_NOT_REGISTRY_OR_RUNTIME_PROOF'
                and type(doc.get('attempted')) is int and doc['attempted'] == 489
                and isinstance(rows, list) and len(rows) == 489
                and isinstance(statuses, dict)):
            return False
        seen = set()
        counted = {}
        for row in rows:
            if not isinstance(row, dict):
                return False
            num, filename, status = (row.get(k) for k in ('physical_number', 'filename', 'status'))
            if (type(num) is not int or num < 2 or num > 587 or num in seen
                    or not isinstance(filename, str) or not filename.endswith('.jar')
                    or '/' in filename or '\\' in filename or not isinstance(status, str)):
                return False
            seen.add(num)
            counted[status] = counted.get(status, 0) + 1
            if num == 272 and (filename != 'factory_construction_registry_probe-0.1.0.jar'
                               or row.get('triage_group') != 'OTHER'):
                return False
        return 272 in seen and counted == statuses

    if name == 'providers_69':
        rows, counts = doc.get('entries'), doc.get('counts')
        if not (exit_code == 0
                and doc.get('source') == 'PHYSICAL-LEDGER-VERSION-RECONCILIATION-2026-10-08.md'
                and doc.get('evidence_class') == 'READ_ONLY_JAR_FINGERPRINT_NOT_REGISTRY_PROOF'
                and type(doc.get('expected')) is int and doc['expected'] == 69
                and isinstance(rows, list) and len(rows) == 69 and isinstance(counts, dict)):
            return False
        providers, seen = set(), {}
        for row in rows:
            if not isinstance(row, dict):
                return False
            provider, filename, status = (row.get(k) for k in ('provider', 'filename', 'status'))
            if (not isinstance(provider, str) or not provider or provider in providers
                    or not isinstance(filename, str) or not filename.endswith('.jar')
                    or '/' in filename or '\\' in filename or not isinstance(status, str)):
                return False
            providers.add(provider)
            seen[status] = seen.get(status, 0) + 1
        return (all(type(n) is int and n >= 0 for n in counts.values())
                and all(seen.get(k, 0) == value for k, value in counts.items())
                and all(key in counts for key in seen) and sum(counts.values()) == 69)

    if name == 'physical_272_metadata':
        status, ver = doc.get('status'), doc.get('version_evidence')
        if not (doc.get('schema') == 'black_arcana_nonmagic_272_metadata_probe_v1'
                and doc.get('evidence') == 'EMBEDDED_MOD_ID_ONLY_NOT_SPELL_REGISTRY_OR_RUNTIME_PROOF'
                and doc.get('source_commit') == SNAPSHOT
                and type(doc.get('physical_number')) is int and doc['physical_number'] == 272
                and doc.get('filename') == 'factory_construction_registry_probe-0.1.0.jar'
                and doc.get('expected_mod_id') == 'factory_construction_registry_probe'
                and doc.get('expected_version') == '0.1.0'
                and doc.get('registry_entries_verified') is False
                and doc.get('survival_acquisition_verified') is False
                and doc.get('spell_count', object()) is None
                and isinstance(status, str) and isinstance(ver, str)):
            return False
        if exit_code == 0:
            return (status == 'MATCHED_EMBEDDED_MOD_ID'
                    and ver == 'MATCHED_SOURCE_LITERAL'
                    and doc.get('embedded_version') == '0.1.0')
        return (exit_code == 2
                and (status != 'MATCHED_EMBEDDED_MOD_ID'
                     or ver != 'MATCHED_SOURCE_LITERAL'))

    if name == 'physical_272_reconciliation':
        status = doc.get('status')
        if not (doc.get('schema') == 'black_arcana_nonmagic_272_cross_report_reconciliation_v1'
                and doc.get('evidence') == 'REPORT_CONSISTENCY_ONLY_NOT_REAL_INSTANCE_OR_REGISTRY_PROOF'
                and doc.get('source_commit') == SNAPSHOT
                and type(doc.get('physical_number')) is int and doc['physical_number'] == 272
                and doc.get('filename') == 'factory_construction_registry_probe-0.1.0.jar'
                and doc.get('catalog_status') == 'BLOCKED_MISSING_DOSSIER_AND_REGISTRY_PROOF'
                and doc.get('registry_entries_verified') is False
                and doc.get('survival_acquisition_verified') is False
                and doc.get('spell_count', object()) is None):
            return False
        return (exit_code == 0 and status == 'REPORTED_HASHES_AND_MOD_ID_CONSISTENT'
                or exit_code == 2 and status in (
                    'COLLECTOR_BLOCKED', 'SHA256_MISMATCH',
                    'EMBEDDED_MOD_ID_NOT_CONFIRMED', 'SOURCE_VERSION_MISMATCH',
                    'SOURCE_VERSION_UNVERIFIED'))

    if name == 'registry_39_queue':
        rows = doc.get('providers')
        if not (exit_code == 0
                and doc.get('schema') == 'black_arcana_39_provider_registry_evidence_queue_v1'
                and doc.get('evidence') == 'REPORT_ONLY_NOT_REGISTRY_OR_SURVIVAL_PROOF'
                and doc.get('source_commit') == SNAPSHOT
                and type(doc.get('expected_physical_jars')) is int
                and doc['expected_physical_jars'] == 69
                and type(doc.get('expected_binary_registry_proofs')) is int
                and doc['expected_binary_registry_proofs'] == 39
                and type(doc.get('registry_proofs_completed')) is int
                and doc['registry_proofs_completed'] == 0
                and isinstance(rows, list) and len(rows) == 39):
            return False
        fingerprinted = 0
        for row in rows:
            if (not isinstance(row, dict) or row.get('registry_verified') is not False
                    or row.get('survival_verified') is not False
                    or row.get('promotion_allowed') is not False):
                return False
            if row.get('status') == 'FINGERPRINTED_PENDING_REGISTRY':
                fingerprinted += 1
            elif row.get('status') != 'PHYSICAL_ARTIFACT_BLOCKED':
                return False
        return (type(doc.get('fingerprinted_pending_registry')) is int
                and doc['fingerprinted_pending_registry'] == fingerprinted
                and type(doc.get('blocked_physical_artifact')) is int
                and doc['blocked_physical_artifact'] == 39 - fingerprinted)

    if name == 'deployed_config_survival':
        return (exit_code == 0 and type(doc.get('schema')) is int and doc['schema'] == 3
                and doc.get('collector') == 'Black Arcana provider catalog deployed evidence'
                and doc.get('instance_root_redacted') is True
                and isinstance(doc.get('worlds_scanned'), list)
                and isinstance(doc.get('mods'), dict)
                and isinstance(doc.get('notes'), list))
    return False


def capture(instance: Path, output_dir: Path, worlds: tuple[Path, ...] = (),
            probe_log: Path | None = None, *, qa_dir: Path = QA) -> dict:
    """Capture evidence in a fresh directory outside the Minecraft instance."""
    if instance.is_symlink() or not instance.is_dir() or (instance / 'mods').is_symlink() \
            or not (instance / 'mods').is_dir():
        raise ValueError('instance and mods/ must be existing, non-symlink directories')
    resolved_instance = instance.resolve(strict=True)
    if output_dir.is_symlink() or output_dir.resolve().is_relative_to(resolved_instance):
        raise ValueError('output directory must be outside the Minecraft instance')
    # Fresh output directory prevents stale reports from a different modpack run.
    output_dir.mkdir(parents=True, exist_ok=False)
    report: dict = {
        'schema': 'black_arcana_physical_catalog_evidence_bundle_v1',
        'source_commit': SNAPSHOT,
        'evidence': 'READ_ONLY_REPORT_COLLECTION_NOT_REGISTRY_OR_SURVIVAL_PROOF',
        'instance_path_included': False,
        'registry_proofs_completed': 0,
        'catalog_spells_added': 0,
        'stage_promotion_allowed': False,
        'steps': {},
    }

    def step(name: str, script: str, filename: str, args: list[str],
             blocked_codes: frozenset[int] = frozenset()) -> bool:
        destination = output_dir / filename
        command = [sys.executable, str(qa_dir / script), *args]
        # The deployed evidence collector writes directly to its --output path.
        direct_output = script == 'provider-catalog-deployed-evidence-collector.py'
        try:
            if direct_output:
                proc = subprocess.run(command, stdout=subprocess.DEVNULL,
                                      stderr=subprocess.PIPE, text=True, check=False)
            else:
                with destination.open('w', encoding='utf-8') as out:
                    proc = subprocess.run(command, stdout=out, stderr=subprocess.PIPE,
                                          text=True, check=False)
            payload = _load_report(destination)
            allowed = proc.returncode == 0 or proc.returncode in blocked_codes
            validated = allowed and _valid_collector_report(name, payload, proc.returncode)
            status = ('BLOCKED' if proc.returncode in blocked_codes else 'COLLECTED') \
                if validated else 'FAILED'
            entry = {'status': status, 'exit_code': proc.returncode, 'file': filename}
            if payload is not None and isinstance(payload.get('status'), str):
                entry['collector_status'] = payload['status']
            report['steps'][name] = entry
            return status != 'FAILED'
        except OSError:
            report['steps'][name] = {'status': 'FAILED', 'file': filename}
            return False

    inst = str(resolved_instance)
    triage_ok = step('nonmagic_489', 'nonmagic_physical_jar_triage.py',
                     'nonmagic-489.json', ['--instance', inst])
    fingerprint_ok = step('providers_69', 'physical_provider_fingerprint_collector.py',
                          'providers-69.json', ['--instance', inst])
    metadata_ok = step('physical_272_metadata', 'nonmagic_272_metadata_probe.py',
                       'physical-272-metadata.json', ['--instance', inst], frozenset({2}))
    if triage_ok and metadata_ok:
        step('physical_272_reconciliation', 'nonmagic_272_report_reconcile.py',
             'physical-272-reconciliation.json',
             ['--triage', str(output_dir / 'nonmagic-489.json'),
              '--metadata', str(output_dir / 'physical-272-metadata.json')], frozenset({2}))
    else:
        report['steps']['physical_272_reconciliation'] = {'status': 'SKIPPED', 'reason': 'DEPENDENCY_FAILED'}
    if fingerprint_ok:
        queue_ok = step('registry_39_queue', 'provider_39_evidence_queue.py',
                        'provider-39-queue.json',
                        ['--fingerprints', str(output_dir / 'providers-69.json')])
        if queue_ok:
            queue = _load_report(output_dir / 'provider-39-queue.json')
            if not queue or queue.get('registry_proofs_completed') != 0 \
                    or queue.get('expected_binary_registry_proofs') != 39 \
                    or len(queue.get('providers', [])) != 39 \
                    or any(x.get('promotion_allowed') is not False for x in queue['providers']):
                report['steps']['registry_39_queue']['status'] = 'FAILED'
    else:
        report['steps']['registry_39_queue'] = {'status': 'SKIPPED', 'reason': 'DEPENDENCY_FAILED'}
    deployed_args = [inst, '--output', str(output_dir / 'deployed-evidence.json')]
    for world in worlds:
        deployed_args.extend(['--world', str(world)])
    if probe_log is not None:
        deployed_args.extend(['--probe-log', str(probe_log)])
    step('deployed_config_survival', 'provider-catalog-deployed-evidence-collector.py',
         'deployed-evidence.json', deployed_args)
    report['status'] = ('COLLECTION_INCOMPLETE' if any(
        x['status'] in ('FAILED', 'SKIPPED') for x in report['steps'].values())
        else 'REPORTS_CAPTURED_CATALOG_UNVERIFIED')
    (output_dir / 'bundle-index.json').write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--instance', type=Path, required=True)
    parser.add_argument('--output-dir', type=Path, required=True,
                        help='NEW output directory outside the Minecraft instance')
    parser.add_argument('--world', type=Path, action='append', default=[])
    parser.add_argument('--probe-log', type=Path)
    args = parser.parse_args()
    try:
        result = capture(args.instance.expanduser(), args.output_dir.expanduser(),
                         tuple(args.world), args.probe_log)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result['status'] == 'REPORTS_CAPTURED_CATALOG_UNVERIFIED' else 2


if __name__ == '__main__':
    raise SystemExit(main())
