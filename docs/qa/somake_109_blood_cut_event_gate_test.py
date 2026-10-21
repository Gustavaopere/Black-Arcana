#!/usr/bin/env python3
"""Synthetic Java 21 annotation-scope and damage-callsite regression tests."""
from pathlib import Path
import subprocess
import tempfile
import unittest
from somake_109_blood_cut_event_gate import annotation_scopes, event_callsite_survey


class AnnotationScopeTests(unittest.TestCase):
    def test_java21_annotation_scopes(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            (d / 'SubscribeEvent.java').write_text(
                'import java.lang.annotation.*;'
                '@Retention(RetentionPolicy.RUNTIME) '
                '@Target(ElementType.METHOD) public @interface SubscribeEvent {}\n')
            (d / 'EventBusSubscriber.java').write_text(
                'import java.lang.annotation.*;'
                '@Retention(RetentionPolicy.RUNTIME) '
                '@Target(ElementType.TYPE) public @interface EventBusSubscriber {}\n')
            (d / 'Probe.java').write_text(
                '@EventBusSubscriber public class Probe { '
                '@SubscribeEvent public static void onLivingDamage(Object value) {} '
                'public static void ordinary() {} }\n')
            compile_result=subprocess.run(['javac', *map(str,d.glob('*.java'))],
                                          text=True,capture_output=True)
            self.assertEqual(compile_result.returncode,0,compile_result.stderr)
            process=subprocess.run(['javap','-v','-p','-classpath',str(d),'Probe'],
                                   text=True,capture_output=True)
            self.assertEqual(process.returncode,0,process.stderr)
            proof=annotation_scopes(process.stdout)
            self.assertIn('SubscribeEvent',proof['method_annotations'])
            self.assertIn('EventBusSubscriber',proof['class_annotations'])
            self.assertNotIn('EventBusSubscriber',proof['method_annotations'])
            self.assertNotIn('SubscribeEvent',proof['class_annotations'])

    def test_exact_registration_certificate_rejects_missing_annotations(self):
        from somake_109_blood_cut_event_gate import certify_registration_annotations
        exact = {"class_annotations": ["net.neoforged.fml.common.EventBusSubscriber"],
                 "method_annotations": ["net.neoforged.bus.api.SubscribeEvent"]}
        self.assertTrue(certify_registration_annotations(exact))
        with self.assertRaises(ValueError):
            certify_registration_annotations(dict(exact, class_annotations=[]))
        with self.assertRaises(ValueError):
            certify_registration_annotations(dict(exact, method_annotations=[]))

    def test_malformed_or_missing_method_fails_closed(self):
        with self.assertRaises(ValueError):
            annotation_scopes('public class Empty {}')


class EventCallsiteTests(unittest.TestCase):
    def test_real_event_callsite_keys(self):
        rows=[(0,'aload_0','',''),
            (1,'invokevirtual','','Method net/neoforged/neoforge/event/entity/living/LivingDamageEvent$Post.getNewDamage:()F'),
            (2,'ifeq','8',''),
            (3,'invokestatic','','Method io/redspace/ironsspellbooks/damage/DamageSources.applyDamage:(Lnet/minecraft/world/entity/Entity;FLnet/minecraft/world/damagesource/DamageSource;)Z'),
            (8,'return','','')]
        summary=event_callsite_survey(rows)
        self.assertEqual(1,summary['branch_count'])
        self.assertEqual([3],summary['damage_call_sites'])
        self.assertEqual([1],summary['host_damage_reads'])

    def test_no_damage_call_never_certifies(self):
        with self.assertRaises(ValueError):
            event_callsite_survey([(0,'return','','')])


if __name__ == '__main__':
    unittest.main()
