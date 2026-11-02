#!/usr/bin/env python3
"""Synthetic structural regression tests; *not* a real NeoForge JAR run."""
import copy
import json
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch
from subprocess import CompletedProcess

from neoforge_211248_grief_event_probe import (
    CLASSES, EvidenceError, METHODS, examine_jar, inspect_selected,
    parse_methods, selected, verify_seal,
)


def method(owner, name, descriptor, opcodes):
    ctor = name == '<init>'
    basename = owner if ctor else name
    header = f'  public {basename}(synthetic);' if ctor else f'  public static boolean {basename}(synthetic);'
    lines = [header, f'    descriptor: {descriptor}', '    Code:']
    for i,(opcode,symbol) in enumerate(opcodes):
        if symbol:
            lines.append(f'       {i*3}: {opcode}        #1  // {symbol}')
        else:
            lines.append(f'       {i*3}: {opcode}')
    return '\n'.join(lines)+'\n\n'


HOOKS = [
    ('aload_1',''), ('ifnonnull',''),
    ('invokevirtual','Method net/minecraft/world/level/Level.getGameRules:()Lnet/minecraft/world/level/GameRules;'),
    ('getstatic','Field net/minecraft/world/level/GameRules.RULE_MOBGRIEFING:Lnet/minecraft/world/level/GameRules$Key;'),
    ('invokevirtual','Method net/minecraft/world/level/GameRules.getBoolean:(Lnet/minecraft/world/level/GameRules$Key;)Z'),
    ('ireturn',''),
    ('getstatic','Field net/neoforged/neoforge/common/NeoForge.EVENT_BUS:Lnet/neoforged/bus/api/IEventBus;'),
    ('new','class net/neoforged/neoforge/event/entity/EntityMobGriefingEvent'),
    ('invokespecial','Method net/neoforged/neoforge/event/entity/EntityMobGriefingEvent."<init>":()V'),
    ('invokeinterface','InterfaceMethod net/neoforged/bus/api/IEventBus.post:(...)Lnet/neoforged/bus/api/Event;'),
    ('invokevirtual','Method net/neoforged/neoforge/event/entity/EntityMobGriefingEvent.canGrief:()Z'),
    ('ireturn',''),
]
INIT = [
    ('invokespecial','Method net/neoforged/neoforge/event/entity/EntityEvent."<init>":(...)V'),
    ('invokevirtual','Method net/minecraft/world/level/Level.getGameRules:()Lnet/minecraft/world/level/GameRules;'),
    ('getstatic','Field net/minecraft/world/level/GameRules.RULE_MOBGRIEFING:Lnet/minecraft/world/level/GameRules$Key;'),
    ('invokevirtual','Method net/minecraft/world/level/GameRules.getBoolean:()Z'),
    ('putfield','Field net/neoforged/neoforge/event/entity/EntityMobGriefingEvent.isMobGriefingEnabled:Z'),
    ('putfield','Field net/neoforged/neoforge/event/entity/EntityMobGriefingEvent.canGrief:Z'),
    ('return',''),
]
GET = [('getfield','Field canGrief:Z'),('ireturn','')]
SET = [('putfield','Field canGrief:Z'),('return','')]
IS = [('getfield','Field isMobGriefingEnabled:Z'),('ireturn','')]


def fixtures():
    hook=method('EventHooks','canEntityGrief',METHODS['EventHooks']['canEntityGrief'],HOOKS)
    ev=''.join(method('EntityMobGriefingEvent',name,desc,ops) for (name,desc),ops in zip(
        METHODS['EntityMobGriefingEvent'].items(),[INIT,GET,SET,IS]))
    return {'EventHooks':hook,'EntityMobGriefingEvent':ev}


class GriefEventTests(unittest.TestCase):
    def test_parser_and_selected_descriptors(self):
        for owner,code in fixtures().items():
            methods=parse_methods(code)
            for name,desc in METHODS[owner].items():
                m=selected(methods,name,desc)
                self.assertTrue(inspect_selected(owner,m)['method_sha256'])

    def test_wrong_descriptor_rejected(self):
        with self.assertRaisesRegex(EvidenceError,'descriptor'):
            selected(parse_methods(fixtures()['EventHooks']),'canEntityGrief','()Z')

    def test_eventbus_post_replaced_rejected(self):
        code=fixtures()['EventHooks'].replace('IEventBus.post:', 'IEventBus.unrelated:')
        with self.assertRaisesRegex(EvidenceError,'post:'):
            inspect_selected('EventHooks',selected(parse_methods(code),'canEntityGrief',METHODS['EventHooks']['canEntityGrief']))

    def test_gamerule_symbol_missing_rejected(self):
        code=fixtures()['EventHooks'].replace('RULE_MOBGRIEFING', 'RULE_SOMETHING_ELSE')
        with self.assertRaisesRegex(EvidenceError,'RULE_MOBGRIEFING'):
            inspect_selected('EventHooks',selected(parse_methods(code),'canEntityGrief',METHODS['EventHooks']['canEntityGrief']))

    def test_null_branch_missing_rejected(self):
        code=fixtures()['EventHooks'].replace('ifnonnull','nop')
        with self.assertRaisesRegex(EvidenceError,'entity-null branch'):
            inspect_selected('EventHooks',selected(parse_methods(code),'canEntityGrief',METHODS['EventHooks']['canEntityGrief']))

    def test_event_init_defaults_missing_rejected(self):
        code=fixtures()['EntityMobGriefingEvent'].replace('isMobGriefingEnabled:Z','notDefault:Z')
        m=selected(parse_methods(code),'<init>',METHODS['EntityMobGriefingEvent']['<init>'])
        with self.assertRaisesRegex(EvidenceError,'initialization'):
            inspect_selected('EntityMobGriefingEvent',m)

    def test_setter_field_replaced_rejected(self):
        code=fixtures()['EntityMobGriefingEvent'].replace('Field canGrief:Z','Field innocent:Z')
        m=selected(parse_methods(code),'setCanGrief','(Z)V')
        with self.assertRaisesRegex(EvidenceError,'setter'):
            inspect_selected('EntityMobGriefingEvent',m)

    def test_duplicate_descriptor_rejected(self):
        code=fixtures()['EventHooks']*2
        with self.assertRaisesRegex(EvidenceError,'ambiguous'):
            selected(parse_methods(code),'canEntityGrief',METHODS['EventHooks']['canEntityGrief'])

    def test_seal_drift_rejected(self):
        methods=fixtures()
        report={'schema_version':1,'scope':'fake','artifact':{'sha256':'abc'},
                'interpretation':'static','limits':{'mutation':'NO_MUTATION'},'classes':[]}
        for owner,code in methods.items():
            chosen=[inspect_selected(owner,selected(parse_methods(code),name,desc))
                    for name,desc in METHODS[owner].items()]
            report['classes'].append({'owner':owner,'class_path':CLASSES[owner],
                                      'class_sha256':'a'*64,'selected_methods':chosen})
        seal=copy.deepcopy(report)
        self.assertTrue(verify_seal(report,seal))
        changed=copy.deepcopy(report)
        changed['classes'][1]['selected_methods'][2]['method_sha256']='0'*64
        with self.assertRaisesRegex(EvidenceError,'method seal'):
            verify_seal(changed,seal)
        changed=copy.deepcopy(report)
        changed['classes'][0]['selected_methods'][0]['selected_references'][0]['symbol']='injected'
        with self.assertRaisesRegex(EvidenceError,'callsite seal'):
            verify_seal(changed,seal)

    def test_exact_zip_structure_and_bounded_probe(self):
        with tempfile.TemporaryDirectory() as temp:
            p=Path(temp)/'synthetic.jar'
            with zipfile.ZipFile(p,'w') as z:
                for name in CLASSES.values():
                    z.writestr(name,b'\xca\xfe\xba\xbe'+b'\0'*9000)
            def javap(args,**kwargs):
                owner='EventHooks' if args[-1].endswith('.EventHooks') else 'EntityMobGriefingEvent'
                return CompletedProcess(args,0,fixtures()[owner],'')
            with patch('neoforge_211248_grief_event_probe.subprocess.run',side_effect=javap):
                result=examine_jar(p,'javap')
            self.assertEqual(result['limits']['perk_certification'],'NOT_CERTIFIED')
            self.assertEqual(len(result['classes'][1]['selected_methods']),4)

if __name__=='__main__':
    unittest.main()