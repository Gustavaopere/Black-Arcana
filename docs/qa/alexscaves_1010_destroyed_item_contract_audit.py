#!/usr/bin/env python3
"""Read-only SHA-exact destroyed-item native contract; no gameplay execution.

The complete publisher class universe is inspected through typed classfile
structures. The native callback, finite constructors/delegates and selected
registry paths are disassembled. NeoForge reference inputs and an installed,
transformed game's execution are distinct evidence boundaries.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import re
import subprocess
import sys
import zipfile

from alexscaves_1010_action_contract_audit import parse_javap
from alexscaves_1010_armor_material_audit import (
    AuditError, ClassReader, SHA1, SHA256, SIZE, canonical, digest, load_seal,
    named, require, rows, verify_artifact,
)

ROOT = Path(__file__).resolve().parents[2]
PROVIDER = ROOT / 'wiki/modpack-catalog/providers/✅-alexs-caves-continued'
SEAL = PROVIDER / 'EXACT-DESTROYED-ITEM-CONTRACT-1.0.10.json'
PREFIX = 'com/github/alexmodguy/alexscaves/'
ITEM = PREFIX + 'server/item/'
TARGET = ITEM + 'ACDestroyedItem'
IMPLEMENTER = ITEM + 'RadioactiveOnDestroyedBlockItem'
PARENT = ITEM + 'RadioactiveBlockItem'
CITADEL = PREFIX + 'citadel/item/BlockItemWithSupplier'
REGISTRY = PREFIX + 'server/block/ACBlockRegistry'
COMPAT = PREFIX + 'server/misc/ACCompat'
IRRADIATED = PREFIX + 'server/potion/IrradiatedEffect'
MOB_EFFECT = PREFIX + 'server/potion/ACMobEffect'
HAZMAT = ITEM + 'HazmatArmorItem'
DAMAGE = PREFIX + 'server/misc/ACDamageTypes'
ONE_ARG = '(Lnet/minecraft/world/entity/item/ItemEntity;)V'
TWO_ARG = '(Lnet/minecraft/world/entity/item/ItemEntity;Lnet/minecraft/world/damagesource/DamageSource;)V'
CTOR = '(Ljava/util/function/Supplier;Lnet/minecraft/world/item/Item$Properties;F)V'
REGISTER = '(Ljava/lang/String;Ljava/util/function/Supplier;I)Ljava/util/function/Supplier;'
FACTORY = '(ILjava/util/function/Supplier;)Ljava/util/function/Supplier;'
OWNERS = {TARGET, IMPLEMENTER, PARENT, CITADEL, REGISTRY, COMPAT,
          IRRADIATED, MOB_EFFECT, HAZMAT, DAMAGE}
CLAIMS = {'claim_scope': 'STATIC_TECHNICAL_CATALOG_ONLY',
    'evidence_grade': 'SHA_EXACT_BINARY_BEHAVIOR',
    'static_technical_contract': 'CERTIFIED_STATIC_7_AXES',
    'mutation': 'NO_MUTATION', 'mutating_hook': 'NOT_VERIFIED',
    'physical_qa': 'NOT_TESTED', 'perk_certification': 'NOT_CERTIFIED',
    'provider_universe_closed': False, 'semantic_magic_roots_delta': 0}
AXES = {
    'identity': 'Publisher 1.0.10 SHA-1/SHA-256/size; abstract two-argument interface declaration and sole concrete publisher implementer, with complete typed hierarchy/member census.',
    'behavior': 'Complete 170-byte native callback: superclass call precedes creative/removed guards; then discard, configured cloud submission and null-source BLOCK explosion request, conditional on normal upstream return.',
    'parameters': 'Cloud GAMMAROACH/color 7853582/IRRADIATED 9600 amplifier 1/radius 2/duration 12000/wait 0/negative-radius-over-duration; explosion 1.8 at Y+0.5. Factory selector 5 constructs with 0.01, an inherited inventory field, not callback RNG.',
    'targeting': 'Callback receives ItemEntity and DamageSource; no owner assignment or entity search in the callback. Cloud and explosion consumers perform external selection. Finite native IRRADIATED consumer is recorded separately from cloud application.',
    'costs': 'Native ItemEntity.discard precedes both submissions; no stack decrement, mana, cooldown or refund path. Submission return values are ignored; accepted world effects or transactional settlement are not established.',
    'integration': 'ACBlockRegistry selector 5/WASTE_DRUM supplier bridge, constructors, relocated Citadel one-argument callback, ACCompat color/effect bridges and bounded native IRRADIATED consumer. Matching-version NeoForge reference proof is a separate boundary.',
    'validation': 'All 1555 class entries, typed owner/declaration/member/hierarchy censuses, reconciled JVM declarations/full selected bodies, explicit operand/branch/switch/bootstrap pivots, immutable seal and twice-run physical-binary CLI. Gameplay remains NOT_TESTED.'}


def at(body, offset, opcode, operand=None, symbol=None, contains=None):
    """Check semantic operands exactly; constant-pool numbers stay in the seal."""
    row = body.get(offset)
    require(row is not None and row[0] == opcode,
            f'native opcode drift at {offset}: {opcode}')
    if operand is not None:
        require(row[1] == operand, f'native operand drift at {offset}: {operand}')
    if symbol is not None:
        require(row[2] == symbol, f'native symbol drift at {offset}: {symbol}')
    if contains is not None:
        require(contains in row[2], f'native target drift at {offset}: {contains}')
    return {'offset': offset, 'opcode': opcode, 'operand': operand,
            'symbol': symbol, 'contains': contains}


def assignable(owner, hierarchy, ancestors=()):
    if owner == TARGET:
        return True
    require(owner not in ancestors, 'cyclic publisher hierarchy')
    row = hierarchy.get(owner)
    return bool(row and any(assignable(parent, hierarchy, (*ancestors, owner))
        for parent in [row['parent'], *row['interfaces']] if parent))


def typed_census(archive):
    paths = archive.namelist()
    require(len(paths) == len(set(paths)), 'duplicate ZIP members')
    class_paths = sorted(p for p in paths if p.endswith('.class'))
    hierarchy, metadata, target_refs, declarations, member_refs, factory_refs = {}, {}, [], [], [], []
    for path in class_paths:
        raw = archive.read(path)
        reader = ClassReader(raw)
        require(path == reader.name + '.class', 'class path/declaration mismatch')
        require(reader.major == 65, 'publisher Java21 class version drift')
        hierarchy[reader.name] = {'parent': reader.parent, 'interfaces': reader.interfaces,
                                  'access': reader.access}
        if reader.name in OWNERS:
            metadata[reader.name] = reader
        refs = reader.typed_refs(TARGET)
        if refs:
            target_refs.append({'owner': reader.name, 'typed_references': refs})
        for method in reader.methods:
            if method['name'] == 'onDestroyed':
                declarations.append({'owner': reader.name, **method})
        for index, entry in enumerate(reader.pool):
            if not entry or entry[0] not in (10, 11):
                continue
            tag, owner, pair = reader.resolve(index)
            _, name, descriptor = pair
            row = {'owner': reader.name, 'index': index, 'kind': tag,
                   'target_owner': owner, 'name': name, 'descriptor': descriptor}
            if name == 'onDestroyed':
                member_refs.append(row)
            if owner == REGISTRY and name in ('getBlockSupplier', 'registerBlockAndItem'):
                factory_refs.append(row)
    direct = sorted(owner for owner, row in hierarchy.items()
                    if owner != TARGET and TARGET in row['interfaces'])
    inherited = sorted(owner for owner in hierarchy if owner != TARGET and owner not in direct
                       and assignable(owner, hierarchy))
    concrete = sorted(owner for owner in [*direct, *inherited]
                      if not hierarchy[owner]['access'] & (0x0200 | 0x0400))
    census = {'class_entries_scanned': len(class_paths),
        'class_path_roster_sha256': digest(('\n'.join(class_paths) + '\n').encode()),
        'method': 'Typed Class/Fieldref/Methodref/InterfaceMethodref/NameAndType/MethodType plus declared JVM descriptors; plain UTF8/String constants do not count.',
        'target': TARGET, 'typed_reference_owners': target_refs,
        'direct_implementers': direct, 'inherited_implementers_within_publisher': inherited,
        'concrete_implementers_within_publisher': concrete,
        'on_destroyed_declarations': declarations,
        'on_destroyed_member_references': member_refs,
        'registry_member_references': factory_refs,
        'selected_hierarchy': {owner: hierarchy[owner] for owner in sorted(OWNERS)},
        'limit': 'Publisher classfile closure only; reflective name construction, external mods, transformed runtime classes and future versions are not closed.'}
    validate_census(census)
    require(set(metadata) == OWNERS, 'selected native owner roster drift')
    return census, metadata


def validate_census(census):
    require(census['class_entries_scanned'] == 1555, 'whole-JAR class census drift')
    require({r['owner'] for r in census['typed_reference_owners']} == {TARGET, IMPLEMENTER},
            'typed target owner census drift')
    require(census['direct_implementers'] == [IMPLEMENTER] and
            census['concrete_implementers_within_publisher'] == [IMPLEMENTER] and
            census['inherited_implementers_within_publisher'] == [], 'implementer hierarchy census drift')
    require({(m['owner'], m['descriptor'], m['access']) for m in census['on_destroyed_declarations']} ==
            {(TARGET, TWO_ARG, 1025), (IMPLEMENTER, TWO_ARG, 1), (CITADEL, ONE_ARG, 1)},
            'global onDestroyed declaration census drift')
    require(census['on_destroyed_member_references'] == [{'owner': IMPLEMENTER, 'index': 7,
        'kind': 10, 'target_owner': PARENT, 'name': 'onDestroyed', 'descriptor': TWO_ARG}],
        'global onDestroyed typed member-reference census drift')
    require({r['owner'] for r in census['registry_member_references']} == {REGISTRY},
            'registry typed member-reference owner drift')
    require(census['selected_hierarchy'][IMPLEMENTER]['parent'] == PARENT and
            census['selected_hierarchy'][PARENT]['parent'] == CITADEL and
            census['selected_hierarchy'][CITADEL]['parent'] == 'net/minecraft/world/item/BlockItem',
            'native superclass chain drift')


def disassemble(jar, javap, owner):
    proc = subprocess.run([str(javap), '-classpath', str(jar), '-p', '-c', '-s',
                           owner.replace('/', '.')], capture_output=True, text=True, timeout=60)
    require(proc.returncode == 0, 'javap failed for ' + owner + ': ' + proc.stderr[:300])
    return parse_javap(proc.stdout, owner), proc.stdout


def parse_factory_switch(raw):
    sections = re.findall(r'private static java.util.function.Supplier<[^\n]* getBlockSupplier\([^\n]*\);\s*'
        r'descriptor: [^\n]+\s*Code:\s*0: iload_0\s*1: tableswitch\s*\{ // 1 to 9\s*([^}]+)\}', raw)
    require(len(sections) == 1, 'bounded factory tableswitch absent/ambiguous')
    pairs = re.findall(r'^\s*(default|[1-9]):\s*(\d+)\s*$', sections[0], re.M)
    require(len(pairs) == 10, 'factory switch case census drift')
    result = {key: int(value) for key, value in pairs}
    require(result == {'1':59,'2':66,'3':73,'4':80,'5':87,'6':94,'7':101,'8':108,'9':115,'default':52},
            'factory selector mapping drift')
    return result


def callback_pivots(methods):
    require(set(methods) == {('<init>', CTOR), ('onDestroyed', TWO_ARG)},
            'complete implementer JVM method roster drift')
    body = named(methods, 'onDestroyed', TWO_ARG)
    checks = [(3, 'invokespecial', None, PARENT+'.onDestroyed:'+TWO_ARG),
        (7,'invokevirtual',None,'DamageSource.isCreativePlayer:()Z'),
        (10,'ifne','169',None),(14,'invokevirtual',None,'ItemEntity.isRemoved:()Z'),
        (17,'ifne','169',None),(21,'invokevirtual',None,'ItemEntity.discard:()V'),
        (24,'new',None,'AreaEffectCloud'),(44,'invokespecial',None,'AreaEffectCloud."<init>":'),
        (49,'getstatic',None,'ACParticleRegistry.GAMMAROACH:'),
        (60,'invokevirtual',None,'AreaEffectCloud.setParticle:'),
        (64,'ldc',None,'int 7853582'),(66,'invokestatic',None,'ACCompat.setCloudColor:'),
        (74,'getstatic',None,'ACEffectRegistry.IRRADIATED:'),
        (85,'invokestatic',None,'ACCompat.effect:'),(88,'sipush','9600',None),
        (91,'iconst_1',None,None),(92,'invokespecial',None,'MobEffectInstance."<init>":(Lnet/minecraft/core/Holder;II)V'),
        (95,'invokevirtual',None,'AreaEffectCloud.addEffect:'),(99,'fconst_2',None,None),
        (100,'invokevirtual',None,'AreaEffectCloud.setRadius:'),(104,'sipush','12000',None),
        (107,'invokevirtual',None,'AreaEffectCloud.setDuration:'),(111,'iconst_0',None,None),
        (112,'invokevirtual',None,'AreaEffectCloud.setWaitTime:'),
        (117,'invokevirtual',None,'AreaEffectCloud.getRadius:()F'),(120,'fneg',None,None),
        (122,'invokevirtual',None,'AreaEffectCloud.getDuration:()I'),(125,'i2f',None,None),
        (126,'fdiv',None,None),(127,'invokevirtual',None,'AreaEffectCloud.setRadiusPerTick:'),
        (135,'invokevirtual',None,'Level.addFreshEntity:'),(138,'pop',None,None),
        (143,'aconst_null',None,None),(152,'ldc2_w',None,'double 0.5d'),
        (155,'dadd',None,None),(160,'ldc',None,'float 1.8f'),
        (162,'getstatic',None,'Level$ExplosionInteraction.BLOCK:'),
        (165,'invokevirtual',None,'Level.explode:'),(168,'pop',None,None),(169,'return',None,None)]
    result = [at(body, o, op, operand=arg, contains=token) for o,op,arg,token in checks]
    require([(o,op,arg) for o,(op,arg,_) in body.items() if op.startswith('if')] ==
            [(10,'ifne','169'),(17,'ifne','169')], 'callback guard census drift')
    require(not any('isClientSide' in sym or 'Random' in sym or 'randomChanceOfRadiation' in sym
                    or '.setOwner:' in sym for _,_,sym in body.values()),
            'callback side/RNG/owner behavior drift')
    at(named(methods,'<init>'), 4, 'invokespecial', contains=PARENT+'."<init>":'+CTOR)
    return result


def native_pivots(parsed):
    result = {IMPLEMENTER: {'onDestroyed': callback_pivots(parsed[IMPLEMENTER])}}
    checks = {
        PARENT: {'<init>': [(3,'invokespecial',None,CITADEL+'."<init>":'),
            (7,'fload_3',None,None),(8,'putfield',None,'randomChanceOfRadiation:F')],
            'acInventoryTick': [(1,'invokevirtual',None,'Level.isClientSide:()Z'),(4,'ifne','166',None),
                (8,'instanceof',None,'LivingEntity'),(11,'ifeq','166',None),(37,'invokevirtual',None,'Player.isCreative:()Z'),
                (40,'ifne','166',None),(44,'invokevirtual',None,'ItemStack.getCount:()I'),
                (49,'getfield',None,'randomChanceOfRadiation:F'),(52,'fmul',None,None),
                (58,'invokestatic',None,'HazmatArmorItem.getWornAmount:'),(62,'ldc',None,'float 4.0f'),
                (64,'fdiv',None,None),(65,'fsub',None,None),(84,'invokevirtual',None,'LivingEntity.hasEffect:'),
                (87,'ifne','166',None),(94,'invokeinterface',None,'RandomSource.nextFloat:()F'),
                (103,'fmul',None,None),(104,'fcmpg',None,None),(105,'ifge','166',None),
                (126,'sipush','1800',None),(138,'invokevirtual',None,'LivingEntity.addEffect:'),(141,'pop',None,None)]},
        CITADEL: {'<init>': [(1,'aconst_null',None,None),(3,'invokespecial',None,'BlockItem."<init>":'),
                (8,'putfield',None,'blockSupplier:')],
            'getBlock': [(1,'getfield',None,'blockSupplier:'),(4,'invokeinterface',None,'Supplier.get:')],
            'onDestroyed': [(9,'instanceof',None,'ShulkerBoxBlock'),(12,'ifeq','44',None),
                (19,'getstatic',None,'DataComponents.CONTAINER:'),(22,'getstatic',None,'ItemContainerContents.EMPTY:'),
                (25,'invokevirtual',None,'ItemStack.set:'),(33,'ifnull','44',None),
                (38,'invokevirtual',None,'ItemContainerContents.nonEmptyItems:'),
                (41,'invokestatic',None,'ItemUtils.onContainerDestroyed:')]},
        COMPAT: {'effect': [(0,'getstatic',None,'BuiltInRegistries.MOB_EFFECT:'),
                (4,'invokeinterface',None,'Registry.wrapAsHolder:')],
            'setCloudColor': [(5,'invokestatic',None,'Optional.empty:'),(8,'iload_1',None,None),
                (9,'invokestatic',None,'Integer.valueOf:'),(12,'invokestatic',None,'Optional.of:'),
                (15,'invokestatic',None,'List.of:'),(18,'invokespecial',None,'PotionContents."<init>":'),
                (21,'invokevirtual',None,'AreaEffectCloud.setPotionContents:')]},
        IRRADIATED: {'<init>': [(1,'getstatic',None,'MobEffectCategory.HARMFUL:'),(4,'ldc',None,'int 7853582')],
            'shouldTick': [(1,'ifgt','6',None),(6,'sipush','200',None),(10,'idiv',None,None),
                (14,'if_icmple','32',None),(19,'irem',None,None),(22,'idiv',None,None),
                (23,'if_icmpne','30',None),(32,'iconst_1',None,None)],
            'tick': [(1,'invokestatic',None,'HazmatArmorItem.getWornAmount:'),(8,'ldc',None,'float 0.25f'),
                (10,'fmul',None,None),(11,'fsub',None,None),(28,'ifne','38',None),
                (33,'ldc',None,'float 0.4f'),(35,'invokevirtual',None,'Player.causeFoodExhaustion:'),
                (39,'instanceof',None,'RaycatEntity'),(42,'ifne','83',None),
                (52,'invokeinterface',None,'RandomSource.nextFloat:()F'),(59,'ldc',None,'float 0.1f'),
                (61,'fadd',None,None),(63,'ifge','83',None),
                (74,'invokestatic',None,'ACDamageTypes.causeRadiationDamage:'),
                (77,'fload', '4',None),(79,'invokevirtual',None,'LivingEntity.hurt:'),(82,'pop',None,None)],
            'getCurativeItems': [(0,'invokestatic',None,'List.of:')]},
        MOB_EFFECT: {'applyEffectTick': [(3,'invokevirtual',None,'tick:'),(6,'iconst_1',None,None)],
            'shouldApplyEffectTickThisTick': [(3,'invokevirtual',None,'shouldTick:')]},
        HAZMAT: {'getWornAmount': [(9,'getstatic',None,'ACItemRegistry.HAZMAT_MASK:'),
            (23,'ifeq','29',None),(26,'iinc','1, 1',None),(36,'getstatic',None,'ACItemRegistry.HAZMAT_CHESTPLATE:'),
            (50,'ifeq','56',None),(53,'iinc','1, 1',None),(63,'getstatic',None,'ACItemRegistry.HAZMAT_LEGGINGS:'),
            (77,'ifeq','83',None),(80,'iinc','1, 1',None),(90,'getstatic',None,'ACItemRegistry.HAZMAT_BOOTS:'),
            (104,'ifeq','110',None),(107,'iinc','1, 1',None)]},
        DAMAGE: {'causeRadiationDamage': [(5,'getstatic',None,'Registries.DAMAGE_TYPE:'),
            (19,'getstatic',None,'RADIATION:'),(22,'invokeinterface',None,'Registry.getHolderOrThrow:'),
            (27,'iconst_2',None,None),(28,'invokespecial',None,'ACDamageTypes$DamageSourceRandomMessages."<init>":')]}}
    for owner, methods in checks.items():
        result[owner] = {name: [at(named(parsed[owner], name), o, op, operand=arg, contains=token)
                               for o,op,arg,token in specs] for name,specs in methods.items()}
    require(not any(key[0]=='onDestroyed' for key in parsed[PARENT]), 'parent gained callback declaration')
    return result


def bootstrap_target(reader, index, owner, name):
    bootstrap = reader.attributes['bootstrap_methods'][index]
    refs = [arg for arg in bootstrap['arguments'] if isinstance(arg,dict) and 'reference' in arg]
    require(len(refs)==1 and refs[0]['reference_kind']==6 and
            refs[0]['reference'][0]==10 and refs[0]['reference'][1]==owner and
            refs[0]['reference'][2][1]==name, 'supplier bootstrap target drift: '+name)
    return {'index':index, **bootstrap}


def factory_pivots(methods):
    """Keep the selector-4 negative control separate from selector-5 creation."""
    factory = named(methods, 'getBlockSupplier', FACTORY)
    at(factory,1,'tableswitch',operand='{',symbol='1 to 9')
    at(factory,81,'invokedynamic',contains='InvokeDynamic #7:get:')
    at(factory,88,'invokedynamic',contains='InvokeDynamic #8:get:')
    for name,owner,chance in [('lambda$getBlockSupplier$441',IMPLEMENTER,'float 0.01f'),
                             ('lambda$getBlockSupplier$440',PARENT,'float 0.001f')]:
        body = named(methods,name)
        at(body,0,'new',symbol='class '+owner)
        at(body,8,'ldc_w',symbol=chance)
        at(body,11,'invokespecial',contains=owner+'."<init>":'+CTOR)


def registration_bridge(methods, reader, switch):
    factory_pivots(methods)
    bridge = named(methods,'registerBlockAndItem',REGISTER)
    at(bridge,9,'getstatic',contains='ACItemRegistry.DEF_REG:')
    at(bridge,13,'iload_2')
    at(bridge,15,'invokestatic',contains='getBlockSupplier:'+FACTORY)
    at(bridge,18,'invokevirtual',contains='ACDeferredRegister.register:')
    factory_calls=[{'name':key[0],'descriptor':key[1],'offset':offset}
        for key,body in sorted(methods.items()) for offset,(opcode,_,symbol) in sorted(body.items())
        if opcode=='invokestatic' and 'getBlockSupplier:'+FACTORY in symbol]
    require(factory_calls==[{'name':'registerBlockAndItem','descriptor':REGISTER,'offset':15}],
            'actual getBlockSupplier invocation census drift')
    clinit = named(methods,'<clinit>')
    ordered = sorted(clinit)
    explicit = []
    for index,offset in enumerate(ordered):
        opcode,_,symbol = clinit[offset]
        if opcode != 'invokestatic' or 'registerBlockAndItem:'+REGISTER not in symbol:
            continue
        prior = ordered[index-1]
        op,arg,_ = clinit[prior]
        require(op.startswith('iconst_') or op in ('bipush','sipush'), 'nonliteral registry selector')
        selector = int(op[-1]) if op.startswith('iconst_') else int(arg)
        start,end = ordered[index-3],ordered[index+1]
        at(clinit,start,'ldc_w')
        at(clinit,ordered[index-2],'invokedynamic')
        at(clinit,end,'putstatic')
        explicit.append({'name':clinit[start][2].removeprefix('String '),'selector':selector,
            'window':[start,end],'selector_offset':prior,'registration_offset':offset,
            'registry_field':clinit[end][2].split(':',1)[0].removeprefix('Field '),
            'instructions':rows({o:clinit[o] for o in ordered if start<=o<=end})})
    require(len(explicit)==43 and dict(Counter(r['selector'] for r in explicit))==
            {1:29,2:2,3:4,4:3,5:1,6:2,7:1,8:1}, 'all explicit selector registration census drift')
    positive = [r for r in explicit if r['selector']==5]
    negative = [r for r in explicit if r['selector']==4]
    require([(r['name'],r['window'],r['registry_field']) for r in positive] ==
            [('waste_drum',[2192,2204],'WASTE_DRUM')], 'destroyed-item positive registration drift')
    require([(r['name'],r['window']) for r in negative] ==
            [('radrock_uranium_ore',[2059,2071]),('block_of_uranium',[2292,2304]),('unrefined_waste',[2321,2333])],
            'ordinary-radioactive negative registration drift')
    at(named(methods,'lambda$static$154'),0,'new',contains='WasteDrumBlock')
    return {'owner':REGISTRY,'selector_switch':switch,'actual_get_block_supplier_invocations':factory_calls,
        'explicit_three_argument_registration_count':len(explicit),
        'explicit_selector_counts':{str(k):v for k,v in sorted(Counter(r['selector'] for r in explicit).items())},
        'destroyed_selector':5,'destroyed_factory':'lambda$getBlockSupplier$441',
        'destroyed_factory_chance_field_input':0.01,'positive_registrations':positive,
        'ordinary_radioactive_selector':4,'ordinary_radioactive_factory':'lambda$getBlockSupplier$440',
        'ordinary_radioactive_chance_field_input':0.001,'negative_registrations':negative,
        'supplier_bootstraps':[bootstrap_target(reader,7,REGISTRY,'lambda$getBlockSupplier$440'),
            bootstrap_target(reader,8,REGISTRY,'lambda$getBlockSupplier$441'),
            bootstrap_target(reader,166,REGISTRY,'lambda$static$154')],
        'limit':'Native registration declarations and supplier construction only; engine registration lifecycle, realized registry instances and installed execution are not physically tested.'}


def select_methods(owner, methods):
    names = {
        TARGET: {'onDestroyed'}, IMPLEMENTER: {'<init>','onDestroyed'},
        PARENT: {'<init>','acInventoryTick'}, CITADEL: {'<init>','getBlock','onDestroyed'},
        REGISTRY: {'getBlockSupplier','registerBlockAndItem','blockItemProperties',
                   'lambda$getBlockSupplier$440','lambda$getBlockSupplier$441','lambda$static$154'},
        COMPAT: {'effect','setCloudColor'}, IRRADIATED: {'<init>','tick','shouldTick','getCurativeItems'},
        MOB_EFFECT: {'<init>','applyEffectTick','shouldApplyEffectTickThisTick'},
        HAZMAT: {'getWornAmount'}, DAMAGE: {'causeRadiationDamage'}}[owner]
    return {key:body for key,body in methods.items() if key[0] in names}


def method_report(key, body, declaration, pivots=(), switch=None):
    require(bool(body) == ('code_sha256' in declaration), 'Code/declaration body mismatch')
    branches = []
    for offset,(opcode,operand,_) in sorted(body.items()):
        if opcode.startswith('if') or opcode in ('goto','goto_w'):
            require(operand.isdecimal() and int(operand) in body, 'invalid native branch target')
            branches.append({'offset':offset,'opcode':opcode,'target':int(operand)})
        if opcode in ('tableswitch','lookupswitch'):
            require(switch is not None and opcode=='tableswitch', 'unbounded native switch')
            require(all(target in body for target in switch.values()), 'invalid switch branch target')
            branches.append({'offset':offset,'opcode':opcode,'targets':switch})
    instructions=rows(body)
    return {'name':key[0],'descriptor':key[1], 'access':declaration['access'],
        'coverage':'FULL_BODY' if body else 'ABSTRACT_DECLARATION',
        'code_size':declaration.get('code_size'),'code_sha256':declaration.get('code_sha256'),
        'exception_handlers':declaration.get('exception_handlers'),
        'instruction_count':len(instructions),'instruction_sha256':digest(canonical(instructions).encode()),
        'branches':branches,'pivots':list(pivots),'instructions':instructions}


def build_report(jar, javap):
    verify_artifact(jar)
    require(javap.is_file(), 'javap executable not found')
    with zipfile.ZipFile(jar) as archive:
        census,metadata=typed_census(archive)
        require(metadata[TARGET].access==1537 and metadata[TARGET].fields==[] and
                {(m['name'],m['descriptor'],m['access']) for m in metadata[TARGET].methods}==
                {('onDestroyed',TWO_ARG,1025)}, 'abstract interface declaration drift')
        parsed,raw={},{}
        for owner in sorted(metadata):
            parsed[owner],raw[owner]=disassemble(jar,javap,owner)
            require(set(parsed[owner])=={(m['name'],m['descriptor']) for m in metadata[owner].methods},
                    'javap/declaration JVM method roster mismatch: '+owner)
        pivots=native_pivots(parsed)
        switch=parse_factory_switch(raw[REGISTRY])
        registration=registration_bridge(parsed[REGISTRY],metadata[REGISTRY],switch)
        native={}
        for owner in sorted(parsed):
            declarations={(m['name'],m['descriptor']):m for m in metadata[owner].methods}
            native[owner]=[method_report(key,body,declarations[key],pivots.get(owner,{}).get(key[0],()),
                switch if owner==REGISTRY and key[0]=='getBlockSupplier' else None)
                for key,body in sorted(select_methods(owner,parsed[owner]).items())]
        callback=next(m for m in native[IMPLEMENTER] if m['name']=='onDestroyed')
        require(callback['code_size']==170 and callback['exception_handlers']==[], 'complete callback Code drift')
        registry_decl=next(m for m in metadata[REGISTRY].methods if m['name']=='<clinit>')
        registration['clinit']={'coverage':'SELECTED_OPERAND_WINDOWS',
            'full_method_code_sha256':registry_decl['code_sha256'],'full_method_code_size':registry_decl['code_size'],
            'full_method_instruction_sha256':digest(canonical(rows(named(parsed[REGISTRY],'<clinit>'))).encode())}
        hashes={owner:digest(archive.read(owner+'.class')) for owner in sorted(metadata)}
    return {'schema_version':1,'artifact':{'mod_id':'alexscaves','version':'1.0.10',
        'size_bytes':SIZE,'sha1':SHA1,'sha256':SHA256},'claims':CLAIMS,'axes':AXES,
        'class_sha256':hashes,'typed_reference_census':census,'native_methods':native,
        'registration_bridge':registration,
        'callback_semantics':{'owner':IMPLEMENTER,'descriptor':TWO_ARG,'code_size':170,
            'upstream_call':{'offset':3,'opcode':'invokespecial','symbolic_owner':PARENT,
                'descriptor':TWO_ARG,'parent_declares_two_argument_method':False,
                'relocated_native_ancestor_one_argument_method':CITADEL,
                'causal_bound':'Every local guard and effect below offset 6 requires normal return from the superclass call. Matching-version NeoForge default bridges are separately evidenced reference inputs; actual installed transformed dispatch remains unverified.'},
            'guards':[{'offset':10,'rejects':'DamageSource.isCreativePlayer()','return_offset':169},
                      {'offset':17,'rejects':'ItemEntity.isRemoved()','return_offset':169}],
            'order':['superclass two-argument call','creative guard','removed guard','ItemEntity.discard',
                     'construct and configure cloud','Level.addFreshEntity return ignored','Level.explode return ignored'],
            'cloud':{'particle_supplier':'GAMMAROACH','color':7853582,'effect_supplier':'IRRADIATED',
                     'effect_input_duration_ticks':9600,'effect_input_amplifier':1,'radius':2.0,
                     'cloud_duration_ticks':12000,'wait_time_ticks':0,'radius_per_tick_expression':'-cloud.getRadius() / (float) cloud.getDuration()',
                     'owner_assignment_in_callback':False,'add_fresh_entity_boolean_checked':False},
            'explosion':{'source_entity':None,'position':'(item.x,item.y+0.5,item.z)',
                         'strength':1.8,'interaction':'BLOCK','returned_explosion_used':False},
            'local_client_side_guard':False,'local_rng':False,'local_dedicated_reentrancy_or_rollback_guard':False,
            'input_policy':'No local null guards or explicit ownership authorization. DamageSource is dereferenced after superclass return; ItemEntity is subsequently dereferenced. No accepted world change, permission decision or settlement follows from those facts.'},
        'integration_bounds':{
            'constructor_chance':'Factory 0.01 is stored as inherited randomChanceOfRadiation; inventory tick multiplies it by stack count and (1 - hazmat_count/4), checks existing IRRADIATED and RNG, requests duration 1800. The destroyed callback neither reads the field nor samples RNG.',
            'native_status_consumer':'IRRADIATED shouldTick rejects amplifier <=0; otherwise interval=200/amplifier, periodic duration%interval==interval/2 if interval>1, else true. At amplifier1 the native predicate is duration%200==100. Engine cloud duration transforms and scheduling are external.',
            'native_status_tick':'Hazmat count is four exact item identities; resistance=1-count*0.25. Unprotected Player requests exhaustion0.4. Raycat bypasses hurt. Other entities request radiation hurt(resistance) only if randomFloat < resistance+0.1; hurt return ignored. Native hurt request is not accepted damage.',
            'color_bridge':'ACCompat.setCloudColor installs PotionContents with empty base potion, Optional.of(color), empty effect list; native callback adds its effect afterwards.',
            'effect_bridge':'ACCompat.effect wraps BuiltInRegistries.MOB_EFFECT through Registry.wrapAsHolder; registry realization and accepted engine effects are external.',
            'relocated_callback':'One-argument BlockItemWithSupplier callback tests the supplied block for ShulkerBoxBlock, resets CONTAINER to EMPTY, and invokes ItemUtils.onContainerDestroyed on prior non-null contents. It has no discard call. It is a different JVM descriptor from ACDestroyedItem.',
            'cost':'Discard is requested before cloud/explosion; no mana/cooldown/cast/stack decrement/refund or transactional world settlement in the callback.',
            'excluded':'Installed class transformation/execution, accepted cloud/entity/effect/explosion/damage outcomes, world destruction and protection rules, event cancellation, network authorization, external consumers, perks/hooks and physical gameplay.'},
        'validation':{'authority':'SHA-exact publisher binary, not adjacent source.',
            'reproduction':'Mandatory exact seal comparison; native semantic/census negatives and twice-run physical-binary CLI idempotence.',
            'physical_cli_is_gameplay':False}}


def validate_report(report):
    require(isinstance(report,dict) and report.get('schema_version')==1, 'invalid destroyed-item report schema')
    require(report.get('claims')==CLAIMS, 'static claim ceiling drift')
    require(report.get('axes')==AXES and len(report['axes'])==7, 'seven static axes drift')
    require(report.get('artifact')=={'mod_id':'alexscaves','version':'1.0.10','size_bytes':SIZE,
                                   'sha1':SHA1,'sha256':SHA256}, 'report artifact identity drift')
    require(set(report.get('native_methods',{}))==OWNERS, 'bounded native owner roster drift')
    validate_census(report['typed_reference_census'])
    require(report['registration_bridge']['destroyed_selector']==5 and
            [r['name'] for r in report['registration_bridge']['positive_registrations']]==['waste_drum'],
            'positive destroyed registration report drift')
    require(report['callback_semantics']['code_size']==170, 'callback byte extent report drift')
    for owner,methods in report['native_methods'].items():
        for method in methods:
            require(method['instruction_count']==len(method['instructions']) and
                method['instruction_sha256']==digest(canonical(method['instructions']).encode()),
                'native full-body instruction integrity drift')


def compare_seal(report,expected):
    validate_report(expected)
    validate_report(report)
    require(report==expected, 'destroyed-item native seal mismatch')


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--jar',required=True,type=Path)
    parser.add_argument('--javap',required=True,type=Path)
    parser.add_argument('--seal',type=Path,default=SEAL)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args(argv)
    try:
        if args.output:
            protected={args.jar.resolve(),args.seal.resolve(),SEAL.resolve(),Path(__file__).resolve(),
                Path(__file__).with_name('alexscaves_1010_destroyed_item_probe.py').resolve(),
                Path(__file__).with_name('alexscaves_1010_armor_material_audit.py').resolve(),
                Path(__file__).with_name('alexscaves_1010_action_contract_audit.py').resolve()}
            require(args.output.resolve() not in protected,
                    'output would overwrite an input/auditor')
            require(args.output.suffix=='.json', 'JSON output required')
        expected=load_seal(args.seal)
        validate_report(expected)
        report=build_report(args.jar,args.javap)
        compare_seal(report,expected)
        payload=canonical(report)
        if args.output:
            args.output.parent.mkdir(parents=True,exist_ok=True)
            args.output.write_text(payload,encoding='utf8')
        else:
            sys.stdout.write(payload)
        return 0
    except (AuditError,ValueError,OSError,subprocess.SubprocessError,zipfile.BadZipFile,KeyError,TypeError) as error:
        print('destroyed-item contract audit failed: '+str(error),file=sys.stderr)
        return 1


if __name__=='__main__':
    raise SystemExit(main())
