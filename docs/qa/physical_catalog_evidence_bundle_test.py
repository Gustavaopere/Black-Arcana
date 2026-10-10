#!/usr/bin/env python3
"""End-to-end guards for the physical catalog evidence bundle orchestration."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SOURCE = Path(__file__).with_name('physical_catalog_evidence_bundle.py')
spec = importlib.util.spec_from_file_location('physical_catalog_evidence_bundle', SOURCE)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)


class EvidenceBundleTests(unittest.TestCase):
    def setup_dirs(self, root):
        instance = root / 'instance'
        (instance / 'mods').mkdir(parents=True)
        qa = root / 'qa'
        qa.mkdir()
        return instance, qa

    def fake_run(self, calls, fail_script=None, metadata_status='MISSING_JAR',
                 valid=True):
        def runner(argv, **kwargs):
            script = Path(argv[1]).name
            calls.append((script, tuple(argv[2:])))
            if script == fail_script:
                return mock.Mock(returncode=1)
            pin = 'de80b186357cad20ba5b81892a8682777e96e35a'
            if script == 'provider-catalog-deployed-evidence-collector.py':
                destination = Path(argv[argv.index('--output') + 1])
                data = {'schema': 3,
                        'collector': 'Black Arcana provider catalog deployed evidence'}
                if valid:
                    data.update(instance_root_redacted=True, worlds_scanned=[],
                                mods={}, notes=['This collector is read-only.'])
                destination.write_text(json.dumps(data))
                return mock.Mock(returncode=0)
            if script == 'nonmagic_272_metadata_probe.py':
                payload = {'status': metadata_status}
                ret = 2 if metadata_status != 'MATCHED_EMBEDDED_MOD_ID' else 0
                if valid:
                    payload.update(
                        schema='black_arcana_nonmagic_272_metadata_probe_v1',
                        evidence='EMBEDDED_MOD_ID_ONLY_NOT_SPELL_REGISTRY_OR_RUNTIME_PROOF',
                        physical_number=272,
                        filename='factory_construction_registry_probe-0.1.0.jar',
                        source_commit=pin,
                        expected_mod_id='factory_construction_registry_probe',
                        expected_version='0.1.0',
                        version_evidence='NOT_EXAMINED',
                        registry_entries_verified=False,
                        survival_acquisition_verified=False,
                        spell_count=None)
            elif script == 'nonmagic_272_report_reconcile.py':
                payload = {'status': 'COLLECTOR_BLOCKED'}
                ret = 2
                if valid:
                    payload.update(
                        schema='black_arcana_nonmagic_272_cross_report_reconciliation_v1',
                        source_commit=pin,
                        evidence='REPORT_CONSISTENCY_ONLY_NOT_REAL_INSTANCE_OR_REGISTRY_PROOF',
                        physical_number=272,
                        filename='factory_construction_registry_probe-0.1.0.jar',
                        catalog_status='BLOCKED_MISSING_DOSSIER_AND_REGISTRY_PROOF',
                        registry_entries_verified=False,
                        survival_acquisition_verified=False,
                        spell_count=None)
            elif script == 'provider_39_evidence_queue.py':
                payload = {
                    'registry_proofs_completed': 0,
                    'expected_binary_registry_proofs': 39,
                    'providers': [{'promotion_allowed': False} for _ in range(39)],
                }
                ret = 0
                if valid:
                    payload.update(
                        schema='black_arcana_39_provider_registry_evidence_queue_v1',
                        evidence='REPORT_ONLY_NOT_REGISTRY_OR_SURVIVAL_PROOF',
                        source_commit=pin, expected_physical_jars=69,
                        fingerprinted_pending_registry=0,
                        blocked_physical_artifact=39,
                        providers=[dict(provider=f'Provider {i}',
                                        physical_status='MISSING',
                                        status='PHYSICAL_ARTIFACT_BLOCKED',
                                        registry_verified=False,
                                        survival_verified=False,
                                        promotion_allowed=False)
                                   for i in range(39)])
            elif script == 'nonmagic_physical_jar_triage.py':
                payload = {'schema': 'synthetic'}
                ret = 0
                if valid:
                    rows = [{'physical_number': i, 'filename': f'other-{i}.jar',
                             'status': 'MISSING'} for i in range(2, 491)]
                    rows[270].update(filename='factory_construction_registry_probe-0.1.0.jar',
                                     triage_group='OTHER')
                    payload = {
                        'schema': 'black_arcana_nonmagic_jar_triage_v1',
                        'evidence': 'ZIP_MEMBER_NAME_HINTS_AND_SHA_NOT_REGISTRY_OR_RUNTIME_PROOF',
                        'source_commit': pin, 'attempted': 489,
                        'statuses': {'MISSING': 489}, 'rows': rows,
                    }
            elif script == 'physical_provider_fingerprint_collector.py':
                payload = {'schema': 'synthetic'}
                ret = 0
                if valid:
                    statuses = ('FINGERPRINTED','MISSING','UNSAFE','OVERSIZED',
                                'INVALID_JAR','UNREADABLE','CHANGED_DURING_SCAN')
                    payload = {
                        'source': 'PHYSICAL-LEDGER-VERSION-RECONCILIATION-2026-10-08.md',
                        'evidence_class': 'READ_ONLY_JAR_FINGERPRINT_NOT_REGISTRY_PROOF',
                        'expected': 69,
                        'counts': {s:(69 if s=='MISSING' else 0) for s in statuses},
                        'entries': [{'provider': f'Provider {i}',
                                     'filename': f'provider-{i}.jar',
                                     'status': 'MISSING'} for i in range(69)],
                    }
            else:
                raise AssertionError(f'unrecognized script: {script}')
            if 'stdout' in kwargs and hasattr(kwargs['stdout'], 'write'):
                json.dump(payload, kwargs['stdout'])
            return mock.Mock(returncode=ret)
        return runner

    def test_all_six_reports_are_collected_with_explicit_catalog_block(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            inst, qa = self.setup_dirs(root)
            calls = []
            with mock.patch.object(module.subprocess, 'run', side_effect=self.fake_run(calls)):
                report = module.capture(inst, root / 'out', qa_dir=qa)
            self.assertEqual(6, len(calls))
            self.assertEqual('REPORTS_CAPTURED_CATALOG_UNVERIFIED', report['status'])
            self.assertEqual('BLOCKED', report['steps']['physical_272_metadata']['status'])
            self.assertEqual('BLOCKED', report['steps']['physical_272_reconciliation']['status'])
            self.assertEqual(0, report['registry_proofs_completed'])
            self.assertEqual(0, report['catalog_spells_added'])
            self.assertFalse(report['stage_promotion_allowed'])
            self.assertTrue((root / 'out' / 'bundle-index.json').is_file())
            self.assertNotIn(str(inst), (root / 'out' / 'bundle-index.json').read_text())

    def test_failed_dependency_is_skipped_but_independent_collection_continues(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            inst, qa=self.setup_dirs(root)
            calls=[]
            with mock.patch.object(module.subprocess, 'run', side_effect=self.fake_run(calls, fail_script='physical_provider_fingerprint_collector.py')):
                result=module.capture(inst, root/'out', qa_dir=qa)
            self.assertEqual('COLLECTION_INCOMPLETE', result['status'])
            self.assertEqual('SKIPPED', result['steps']['registry_39_queue']['status'])
            self.assertEqual('COLLECTED', result['steps']['deployed_config_survival']['status'])
            self.assertFalse(any(x[0]=='provider_39_evidence_queue.py' for x in calls))

    def test_does_not_overwrite_output_or_modify_instance(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            inst,qa=self.setup_dirs(root)
            (root/'out').mkdir()
            with self.assertRaises(FileExistsError):
                module.capture(inst, root/'out',qa_dir=qa)
            with self.assertRaises(ValueError):
                module.capture(inst,inst/'report',qa_dir=qa)
            self.assertFalse((inst/'report').exists())

    def test_passes_world_and_probe_log_as_literal_argv(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            inst,qa=self.setup_dirs(root)
            calls=[]
            w=root/'world with spaces'
            log=root/'logs with spaces'/'latest.log'
            with mock.patch.object(module.subprocess,'run',side_effect=self.fake_run(calls)):
                module.capture(inst,root/'out',worlds=(w,),probe_log=log,qa_dir=qa)
            deploy=next(c for c in calls if c[0]=='provider-catalog-deployed-evidence-collector.py')[1]
            self.assertEqual(str(w),deploy[deploy.index('--world')+1])
            self.assertEqual(str(log),deploy[deploy.index('--probe-log')+1])

    def test_rejects_symlinked_mods_directory(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            inst=root/'instance'; inst.mkdir()
            other=root/'other';other.mkdir()
            (inst/'mods').symlink_to(other,target_is_directory=True)
            with self.assertRaises(ValueError):
                module.capture(inst,root/'out')
            self.assertFalse((root/'out').exists())

    def test_forged_registry_queue_cannot_be_considered_collected(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            inst,qa=self.setup_dirs(root)
            calls=[]
            def malicious(argv,**kwargs):
                r=self.fake_run(calls)(argv,**kwargs)
                if Path(argv[1]).name=='provider_39_evidence_queue.py':
                    dest = kwargs['stdout']
                    dest.seek(0)
                    dest.truncate(0)
                    json.dump({'registry_proofs_completed':39,
                               'expected_binary_registry_proofs':39,
                               'providers':[{'promotion_allowed':True} for _ in range(39)]},dest)
                return r
            with mock.patch.object(module.subprocess,'run',side_effect=malicious):
                output=module.capture(inst,root/'out',qa_dir=qa)
            self.assertEqual('FAILED',output['steps']['registry_39_queue']['status'])
            self.assertEqual('COLLECTION_INCOMPLETE',output['status'])


    def test_actual_collectors_are_composable_on_empty_synthetic_instance(self):
        # End-to-end integration: all six versioned scripts execute; no JARs are
        # real or present, so this can never be evidence of spell completeness.
        self.assertTrue((module.QA / 'provider_39_evidence_queue.py').is_file())
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            instance = root / 'fake-instance'
            (instance / 'mods').mkdir(parents=True)
            outcome = module.capture(instance, root / 'bundle')
            self.assertEqual('REPORTS_CAPTURED_CATALOG_UNVERIFIED', outcome['status'])
            self.assertEqual('BLOCKED', outcome['steps']['physical_272_metadata']['status'])
            self.assertEqual('BLOCKED', outcome['steps']['physical_272_reconciliation']['status'])
            triage = json.loads((root / 'bundle' / 'nonmagic-489.json').read_text())
            self.assertEqual(489, triage['attempted'])
            fingerprint = json.loads((root / 'bundle' / 'providers-69.json').read_text())
            self.assertEqual(69, fingerprint['expected'])
            queue = json.loads((root / 'bundle' / 'provider-39-queue.json').read_text())
            self.assertEqual(39, len(queue['providers']))
            self.assertEqual(0, queue['registry_proofs_completed'])


    def test_rejects_success_exit_with_unrecognized_489_and_69_json(self):
        # Regression: the current bundle accepts any JSON dict as successful evidence.
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            inst,qa=self.setup_dirs(root)
            calls=[]
            with mock.patch.object(module.subprocess,'run',side_effect=self.fake_run(calls,valid=False)):
                report=module.capture(inst,root/'out',qa_dir=qa)
            self.assertEqual('FAILED',report['steps']['nonmagic_489']['status'])
            self.assertEqual('FAILED',report['steps']['providers_69']['status'])
            self.assertEqual('SKIPPED',report['steps']['physical_272_reconciliation']['status'])
            self.assertEqual('SKIPPED',report['steps']['registry_39_queue']['status'])
            self.assertEqual('COLLECTION_INCOMPLETE',report['status'])

    def test_rejects_272_missing_metadata_without_pinned_evidence_fields(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            inst,qa=self.setup_dirs(root)
            calls=[]
            with mock.patch.object(module.subprocess,'run',side_effect=self.fake_run(calls,valid=False)):
                report=module.capture(inst,root/'out',qa_dir=qa)
            self.assertEqual('FAILED',report['steps']['physical_272_metadata']['status'])

    def test_rejects_272_cross_report_block_without_provenance(self):
        # The triage/metadata inputs are valid, only reconciliation is forged.
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            inst, qa = self.setup_dirs(root)
            calls = []
            runner = self.fake_run(calls)

            def malformed_reconciliation(argv, **kwargs):
                result = runner(argv, **kwargs)
                if Path(argv[1]).name == 'nonmagic_272_report_reconcile.py':
                    stream = kwargs['stdout']
                    stream.seek(0)
                    stream.truncate(0)
                    json.dump({'status': 'COLLECTOR_BLOCKED'}, stream)
                return result

            with mock.patch.object(module.subprocess, 'run', side_effect=malformed_reconciliation):
                report = module.capture(inst, root / 'out', qa_dir=qa)
            self.assertEqual('COLLECTED', report['steps']['nonmagic_489']['status'])
            self.assertEqual('BLOCKED', report['steps']['physical_272_metadata']['status'])
            self.assertEqual('FAILED', report['steps']['physical_272_reconciliation']['status'])
            self.assertEqual('COLLECTION_INCOMPLETE', report['status'])

    def test_rejects_deployed_output_without_canonical_schema(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            inst,qa=self.setup_dirs(root)
            calls=[]
            with mock.patch.object(module.subprocess,'run',side_effect=self.fake_run(calls,valid=False)):
                report=module.capture(inst,root/'out',qa_dir=qa)
            self.assertEqual('FAILED',report['steps']['deployed_config_survival']['status'])

    def test_rejects_39_queue_without_schema_even_if_promotion_false(self):
        # Keep the 69-JAR prerequisite valid; corrupt only the queue's JSON.
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            inst, qa = self.setup_dirs(root)
            calls = []
            runner = self.fake_run(calls)

            def malformed_queue(argv, **kwargs):
                result = runner(argv, **kwargs)
                if Path(argv[1]).name == 'provider_39_evidence_queue.py':
                    stream = kwargs['stdout']
                    stream.seek(0)
                    stream.truncate(0)
                    json.dump({'registry_proofs_completed': 0,
                               'expected_binary_registry_proofs': 39,
                               'providers': [{'promotion_allowed': False}
                                             for _ in range(39)]}, stream)
                return result

            with mock.patch.object(module.subprocess, 'run', side_effect=malformed_queue):
                report = module.capture(inst, root / 'out', qa_dir=qa)
            self.assertEqual('COLLECTED', report['steps']['providers_69']['status'])
            self.assertEqual('FAILED', report['steps']['registry_39_queue']['status'])
            self.assertEqual('COLLECTION_INCOMPLETE', report['status'])


if __name__ == '__main__':
    unittest.main()
