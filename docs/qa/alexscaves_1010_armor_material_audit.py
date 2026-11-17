#!/usr/bin/env python3
"""Read-only SHA-exact ACArmorMaterial native support audit; no gameplay execution.

The whole JAR is censused through typed constant-pool/declaration references.
Only the material and its finite direct native construction/attribute bridges
are disassembled. Empty ACArmorTickItem is a declaration disposition, not a
second behavior contract. No Minecraft/NeoForge engine implementation is inferred.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import zipfile

from alexscaves_1010_action_contract_audit import parse_javap

ROOT = Path(__file__).resolve().parents[2]
PROVIDER = ROOT / 'wiki/modpack-catalog/providers/✅-alexs-caves-continued'
SEAL = PROVIDER / 'EXACT-ARMOR-MATERIAL-1.0.10.json'
SHA1 = '6960b299a39a039ac8a5eb9b07be4ad0e3e0a570'
SHA256 = '36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c'
SIZE = 75279314
PREFIX = 'com/github/alexmodguy/alexscaves/'
ITEM = PREFIX + 'server/item/'
MATERIAL, MARKER, REGISTRY = (ITEM + name for name in ('ACArmorMaterial', 'ACArmorTickItem', 'ACItemRegistry'))
COMPAT = PREFIX + 'server/misc/ACCompat'
TICKER = ITEM + 'ACTickingItem'
DISPATCH = PREFIX + 'mixin/ItemStackTickMixin'
CONSUMERS = tuple(ITEM + name for name in ('DarknessArmorItem', 'DivingArmorItem',
    'GingerbreadArmorItem', 'HazmatArmorItem', 'PrimordialArmorItem', 'RainbounceBootsItem'))
SHORT_CTOR = '(Ljava/lang/String;I[IILnet/minecraft/sounds/SoundEvent;F)V'
LONG_CTOR = '(Ljava/lang/String;I[IILnet/minecraft/sounds/SoundEvent;FF)V'
MATERIAL_METHODS = {
    ('<init>', SHORT_CTOR), ('<init>', LONG_CTOR), ('vanilla', '()Lnet/minecraft/core/Holder;'),
    ('properties', '(Lnet/minecraft/world/item/Item$Properties;Lnet/minecraft/world/item/ArmorItem$Type;)Lnet/minecraft/world/item/Item$Properties;'),
    ('defense', '(Lnet/minecraft/world/item/ArmorItem$Type;)I'), ('toughness', '()F'),
    ('knockbackResistance', '()F'), ('getRepairIngredient', '()Lnet/minecraft/world/item/crafting/Ingredient;'),
    ('setRepairMaterial', '(Lnet/minecraft/world/item/crafting/Ingredient;)V'), ('<clinit>', '()V')}
CLAIMS = {'claim_scope': 'STATIC_TECHNICAL_CATALOG_ONLY', 'evidence_grade': 'SHA_EXACT_BINARY_BEHAVIOR',
    'static_technical_contract': 'CERTIFIED_STATIC_7_AXES', 'mutating_hook': 'NOT_VERIFIED',
    'physical_qa': 'NOT_TESTED', 'perk_certification': 'NOT_CERTIFIED', 'mutation': 'NO_MUTATION',
    'provider_universe_closed': False, 'semantic_magic_roots_delta': 0}
AXES = {
    'identity': 'Publisher 1.0.10 SHA-1/SHA-256/size; class declarations and all ten ACArmorMaterial JVM methods, including both constructors and separate <clinit>.',
    'behavior': 'Mutable native material configuration; fresh EnumMap/ArmorMaterial/direct Holder on vanilla(); direct native armor constructors and finite attribute handoff.',
    'parameters': 'Six literal registry declarations; MAX_DAMAGE_ARRAY [13,15,16,11]; ordinal-indexed defense/durability; raw array alias; captured repair supplier and five setup writes.',
    'targeting': 'Not applicable: configuration/armor construction has no target query, damage request, projectile or effect application; direct attribute consumers do not create a spell target.',
    'costs': 'No mana, cast or cooldown operation in the material. Item durability is a configured maximum, not a proved wear/repair settlement or gameplay cost.',
    'integration': 'Native constructor, registry, sound-holder and selected attribute bridge calls only; external engine internals, active armor effects and perks remain outside scope.',
    'validation': 'Typed all-class reference census, declaration/body reconciliation, explicit operand/branch pivots, immutable artifact identity and deterministic seal reproduction; physical gameplay remains NOT_TESTED.'}
MATERIAL_VALUES = [
    ('primordial', 'PRIMORDIAL_ARMOR_MATERIAL', 20, [3,4,3,2], 25, 'ARMOR_EQUIP_LEATHER', 0.0, 'TOUGH_HIDE'),
    ('hazmat_suit', 'HAZMAT_SUIT_ARMOR_MATERIAL', 20, [2,4,5,2], 25, 'ARMOR_EQUIP_IRON', 0.5, 'POLYMER_PLATE'),
    ('diving_suit', 'DIVING_SUIT_ARMOR_MATERIAL', 20, [2,6,5,2], 25, 'ARMOR_EQUIP_IRON', 0.0, 'minecraft:copper_ingot'),
    ('darkness', 'DARKNESS_ARMOR_MATERIAL', 15, [4,5,1,1], 40, 'EMPTY', 0.5, 'DARK_TATTERS'),
    ('rainbounce', 'RAINBOUNCE_ARMOR_MATERIAL', 6, [2,2,1,2], 40, 'ARMOR_EQUIP_GENERIC', 0.0, 'Ingredient.EMPTY'),
    ('gingerbread', 'GINGERBREAD_ARMOR_MATERIAL', 10, [2,4,5,2], 25, 'ARMOR_EQUIP_LEATHER', 0.0, 'GINGERBREAD_CRUMBS')]


class AuditError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise AuditError(message)


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + '\n'


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'duplicate JSON key: ' + key)
        result[key] = value
    return result


def load_seal(path):
    require(path.stat().st_size < 2_000_000, 'seal too large')
    return json.loads(path.read_text(encoding='utf8'), object_pairs_hook=unique_pairs)


class ClassReader:
    """Parse class structures and typed constants, never raw substring matches."""
    def __init__(self, raw):
        self.raw, self.pos = raw, 0
        require(self.take(4) == b'\xca\xfe\xba\xbe', 'invalid class magic')
        self.minor, self.major = self.number(), self.number()
        count = self.number()
        self.pool = [None] * count
        index = 1
        while index < count:
            tag = self.number(1)
            if tag == 1:
                value = self.take(self.number()).decode('utf8', errors='replace')
            elif tag in (7, 8, 16, 19, 20):
                value = self.number()
            elif tag in (9, 10, 11, 12, 17, 18):
                value = (self.number(), self.number())
            elif tag == 15:
                value = (self.number(1), self.number())
            elif tag in (3, 4, 5, 6):
                value = self.take(8 if tag in (5, 6) else 4).hex()
            else:
                raise AuditError('unknown constant-pool tag: ' + str(tag))
            self.pool[index] = (tag, value)
            index += 2 if tag in (5, 6) else 1
        self.access = self.number()
        self.name = self.resolve(self.number())
        parent = self.number()
        self.parent = self.resolve(parent) if parent else None
        self.interfaces = [self.resolve(self.number()) for _ in range(self.number())]
        self.fields, self.methods = self.members(), self.members()
        self.attributes = self.attrs()
        require(self.pos == len(raw), 'trailing class bytes')

    def take(self, size):
        require(self.pos + size <= len(self.raw), 'truncated class')
        result = self.raw[self.pos:self.pos + size]
        self.pos += size
        return result

    def number(self, size=2):
        return int.from_bytes(self.take(size), 'big')

    def resolve(self, index):
        require(0 < index < len(self.pool) and self.pool[index] is not None, 'invalid typed constant index')
        tag, value = self.pool[index]
        if tag == 1:
            return value
        if tag in (7, 8, 16, 19, 20):
            return self.resolve(value)
        if tag in (9, 10, 11, 12):
            return [tag, *(self.resolve(i) for i in value)]
        if tag in (17, 18):
            return [tag, value[0], self.resolve(value[1])]
        if tag == 15:
            return {'reference_kind': value[0], 'reference': self.resolve(value[1])}
        return {'tag': tag, 'hex': value}

    def members(self):
        result = []
        for _ in range(self.number()):
            flags, name, desc = self.number(), self.resolve(self.number()), self.resolve(self.number())
            result.append({'access': flags, 'name': name, 'descriptor': desc, **self.attrs()})
        return result

    def attrs(self):
        result = {}
        for _ in range(self.number()):
            name, size = self.resolve(self.number()), self.number(4)
            end = self.pos + size
            require(end <= len(self.raw), 'truncated class attribute')
            if name == 'Code':
                stack, locals_ = self.number(), self.number()
                code = self.take(self.number(4))
                handlers = []
                for _ in range(self.number()):
                    start, stop, target, catch = self.number(), self.number(), self.number(), self.number()
                    handlers.append({'start': start, 'end': stop, 'target': target,
                        'catch': self.resolve(catch) if catch else None})
                result.update(code_sha256=digest(code), code_size=len(code), max_stack=stack,
                    max_locals=locals_, exception_handlers=handlers)
            elif name == 'BootstrapMethods':
                result['bootstrap_methods'] = [{'handle': self.resolve(self.number()),
                    'arguments': [self.resolve(self.number()) for _ in range(self.number())]}
                    for _ in range(self.number())]
            require(self.pos <= end, 'class attribute overrun')
            self.pos = end
        return result

    def typed_refs(self, target):
        refs = []
        token = 'L' + target + ';'
        for index, entry in enumerate(self.pool):
            if entry is None:
                continue
            tag, value = entry
            if tag == 7 and self.resolve(index) == target:
                refs.append({'kind': 'class_constant', 'index': index})
            elif tag in (9, 10, 11) and self.resolve(value[0]) == target:
                refs.append({'kind': {9:'field_reference',10:'method_reference',11:'interface_method_reference'}[tag],
                    'index': index, 'name': self.resolve(value[1])[1], 'descriptor': self.resolve(value[1])[2]})
            elif tag == 12 and token in self.resolve(value[1]):
                refs.append({'kind': 'name_and_type_descriptor', 'index': index,
                    'name': self.resolve(value[0]), 'descriptor': self.resolve(value[1])})
            elif tag == 16 and token in self.resolve(index):
                refs.append({'kind': 'method_type_descriptor', 'index': index, 'descriptor': self.resolve(index)})
        for kind, members in (('field_declaration', self.fields), ('method_declaration', self.methods)):
            for member in members:
                if token in member['descriptor']:
                    refs.append({'kind': kind, 'name': member['name'], 'descriptor': member['descriptor']})
        return refs


def typed_census(archive):
    names = archive.namelist()
    require(len(names) == len(set(names)), 'duplicate ZIP members')
    class_names = sorted(name for name in names if name.endswith('.class'))
    targets, metadata = {MATERIAL: [], MARKER: []}, {}
    for path in class_names:
        parsed = ClassReader(archive.read(path))
        require(path == parsed.name + '.class', 'class path/declaration mismatch: ' + path)
        if parsed.name in (MATERIAL, MARKER, REGISTRY, COMPAT, TICKER, DISPATCH, *CONSUMERS):
            metadata[parsed.name] = parsed
        for target in targets:
            refs = parsed.typed_refs(target)
            if refs:
                targets[target].append({'owner': parsed.name, 'implements_directly': target in parsed.interfaces,
                    'extends_directly': target == parsed.parent, 'typed_references': refs})
    require(len(class_names) == 1555, 'whole-JAR class census drift')
    require({r['owner'] for r in targets[MATERIAL]} == {MATERIAL, REGISTRY, *CONSUMERS}, 'material typed owner census drift')
    require({r['owner'] for r in targets[MARKER]} == {MARKER, CONSUMERS[0]}, 'marker typed owner census drift')
    return {'class_entries_scanned': len(class_names), 'class_path_roster_sha256': digest(('\n'.join(class_names)+'\n').encode()),
        'method': 'CLASS/Fieldref/Methodref/InterfaceMethodref/NameAndType/MethodType plus declared JVM descriptors; plain UTF8/String constants do not count',
        'targets': targets}, metadata


def disassemble(jar, javap, owner):
    result = subprocess.run([str(javap), '-classpath', str(jar), '-p', '-c', '-s', owner.replace('/', '.')],
        capture_output=True, text=True, timeout=60)
    require(result.returncode == 0, 'javap failed for ' + owner + ': ' + result.stderr[:300])
    return parse_javap(result.stdout, owner)


def rows(body):
    return [{'offset': offset, 'opcode': opcode, 'operand': operand, 'symbol': symbol}
        for offset, (opcode, operand, symbol) in sorted(body.items())]


def pivot(body, offset, opcode, token=''):
    row = body.get(offset)
    require(row is not None and row[0] == opcode and token in (row[1] + ' ' + row[2]),
        f'native behavior pivot drift at {offset}: {opcode} {token}')
    return {'offset': offset, 'opcode': opcode, 'contains': token}


def named(methods, name, descriptor=None):
    matches = [body for (n, d), body in methods.items() if n == name and (descriptor is None or descriptor == d)]
    require(len(matches) == 1, 'missing/ambiguous JVM method: ' + name)
    return matches[0]


def material_pivots(methods):
    require(set(methods) == MATERIAL_METHODS, 'complete material JVM method roster drift')
    checks = {
        ('<init>', SHORT_CTOR): [(10,'fconst_0',''), (11,'invokespecial',LONG_CTOR)],
        ('<init>', LONG_CTOR): [(5,'aconst_null',''), (6,'putfield','ingredient:'), (10,'fconst_0',''),
            (16,'putfield','name:'), (21,'putfield','durability:'), (25,'aload_3',''),
            (26,'putfield','damageReduction:[I'), (32,'putfield','encantability:'), (38,'putfield','sound:'),
            (44,'putfield','toughness:'), (50,'putfield','knockbackResistance:')],
        ('vanilla','()Lnet/minecraft/core/Holder;'): [(0,'new','EnumMap'), (10,'invokestatic','ArmorItem$Type.values:'),
            (23,'if_icmpge','73'), (34,'invokevirtual','ArmorItem$Type.ordinal:'), (41,'arraylength',''),
            (42,'if_icmpge','67'), (57,'iaload',''), (61,'invokeinterface','Map.put:'), (70,'goto','20'),
            (73,'new','ArmorMaterial'), (79,'getfield','encantability:'), (83,'getfield','sound:'),
            (86,'invokestatic','ACCompat.soundHolder:'), (90,'invokedynamic','get:'), (95,'invokestatic','List.of:'),
            (99,'getfield','toughness:'), (103,'getfield','knockbackResistance:'),
            (106,'invokespecial','ArmorMaterial."<init>":(Ljava/util/Map;ILnet/minecraft/core/Holder;Ljava/util/function/Supplier;Ljava/util/List;FF)V'),
            (109,'invokestatic','Holder.direct:')],
        ('properties', next(d for n,d in MATERIAL_METHODS if n=='properties')): [(1,'getstatic','MAX_DAMAGE_ARRAY:'),
            (5,'invokevirtual','ordinal:'), (8,'iaload',''), (10,'getfield','durability:'), (13,'imul',''), (14,'invokevirtual','Properties.durability:')],
        ('defense', next(d for n,d in MATERIAL_METHODS if n=='defense')): [(1,'getfield','damageReduction:'),
            (5,'invokevirtual','ordinal:'), (8,'iaload',''), (9,'ireturn','')],
        ('toughness','()F'): [(1,'getfield','toughness:'), (4,'freturn','')],
        ('knockbackResistance','()F'): [(1,'getfield','knockbackResistance:'), (4,'freturn','')],
        ('getRepairIngredient','()Lnet/minecraft/world/item/crafting/Ingredient;'): [(1,'getfield','ingredient:'),
            (4,'ifnonnull','13'), (7,'getstatic','Ingredient.EMPTY:'), (10,'goto','17'), (14,'getfield','ingredient:')],
        ('setRepairMaterial','(Lnet/minecraft/world/item/crafting/Ingredient;)V'): [(1,'aload_1',''), (2,'putfield','ingredient:')],
        ('<clinit>','()V'): [(0,'iconst_4',''), (1,'newarray','int'), (5,'bipush','13'), (10,'bipush','15'),
            (15,'bipush','16'), (20,'bipush','11'), (23,'putstatic','MAX_DAMAGE_ARRAY:')],
    }
    for name in ('properties', 'defense', 'setRepairMaterial'):
        require(not any(op.startswith('if') or op in ('goto','tableswitch','lookupswitch') for op,_,_ in named(methods,name).values()),
            'unexpected guard in raw direct-access method: ' + name)
    ctor = named(methods,'<init>',LONG_CTOR)
    require(not any('clone' in sym or 'copyOf' in sym for _,_,sym in ctor.values()), 'raw array alias changed')
    return {key: [pivot(methods[key], *spec) for spec in specs] for key,specs in checks.items()}


def material_definitions(methods):
    """Decode the literal constructor operand windows, rather than copying labels."""
    body = named(methods, '<clinit>')
    starts = [offset for offset,(op,_,sym) in body.items() if op == 'new' and sym == 'class ' + MATERIAL]
    require(starts == [34,77,121,165,206,249], 'six material construction windows drift')
    definitions = []
    for index, start in enumerate(starts):
        stop = starts[index+1] if index+1 < len(starts) else 292
        window = [(o,*row) for o,row in sorted(body.items()) if start <= o < stop]
        constants = []
        for o,op,arg,sym in window:
            if op.startswith('iconst_'):
                constants.append(int(op[-1]))
            elif op in ('bipush','sipush'):
                constants.append(int(arg))
        expected = MATERIAL_VALUES[index]
        name,field,multiplier,defense,enchant,sound,toughness,repair = expected
        require(constants == [multiplier,4,0,defense[0],1,defense[1],2,defense[2],3,defense[3],enchant], 'registry material integer operands drift: ' + name)
        require(any(sym == 'String '+name for _,_,_,sym in window), 'material name operand drift')
        require(any('SoundEvents.'+sound+':' in sym for _,op,_,sym in window if op=='getstatic'), 'material sound operand drift')
        require(window[-1][1] == 'putstatic' and 'Field '+field+':' in window[-1][3], 'material destination field drift')
        require(SHORT_CTOR in window[-2][3], 'registry must use zero-knockback constructor')
        toughrow = window[-3]
        require((toughness == 0.0 and toughrow[1] == 'fconst_0') or
                (toughness == 0.5 and toughrow[1] == 'ldc' and toughrow[3] == 'float 0.5f'), 'toughness operand drift')
        definitions.append({'name':name,'registry_field':field,'durability_multiplier':multiplier,
            'damage_reduction_by_ordinal':defense,'enchantability':enchant,'equip_sound_field':sound,
            'toughness':toughness,'knockback_resistance':0.0,'setup_repair_item':repair,
            'clinit_window':[start,window[-1][0]], 'constructor':SHORT_CTOR})
    setup = named(methods,'setup')
    writes = [(o,sym) for o,(op,_,sym) in setup.items() if op == 'invokevirtual' and 'ACArmorMaterial.setRepairMaterial:' in sym]
    require([o for o,_ in writes] == [24,51,70,97,124], 'repair setter census drift')
    repair_checks = [(0,'PRIMORDIAL_ARMOR_MATERIAL'),(9,'TOUGH_HIDE'),(27,'HAZMAT_SUIT_ARMOR_MATERIAL'),
        (36,'POLYMER_PLATE'),(54,'DIVING_SUIT_ARMOR_MATERIAL'),(63,'Items.COPPER_INGOT'),
        (73,'DARKNESS_ARMOR_MATERIAL'),(82,'DARK_TATTERS'),(100,'GINGERBREAD_ARMOR_MATERIAL'),(109,'GINGERBREAD_CRUMBS')]
    for offset,token in repair_checks:
        pivot(setup,offset,'getstatic',token+':')
    return definitions


def select_methods(owner, methods):
    if owner == MATERIAL:
        return dict(methods)
    if owner == TICKER:
        return {}  # Abstract declaration is recorded separately, never an executable body.
    if owner == DISPATCH:
        return {key:body for key,body in methods.items() if key[0] == 'ac_inventoryTick'}
    if owner == MARKER:
        require(not methods, 'marker acquired declared method')
        return {}
    if owner == REGISTRY:
        return {key:body for key,body in methods.items() if key[0] in ('setup','<clinit>') or
            any(MATERIAL in symbol for _,_,symbol in body.values())}
    if owner == COMPAT:
        names = {'soundHolder','rawSound','attributeModifier','attribute','itemAttributes',
            'lambda$itemAttributes$0','lambda$itemAttributes$1'}
        return {key:body for key,body in methods.items() if key[0] in names}
    if owner in CONSUMERS:
        names = {'<init>'}
        if owner.endswith(('DivingArmorItem','GingerbreadArmorItem')):
            names |= {'<clinit>','acModifiers','getDefaultAttributeModifiers','lambda$getDefaultAttributeModifiers$0', 'getOrCreateDurabilityAttributes'}
        return {key:body for key,body in methods.items() if key[0] in names}
    raise AuditError('unbounded disassembly owner')


def method_report(owner, key, body, declaration, pivots=()):
    require(bool(body) == ('code_sha256' in declaration), 'Code/declaration mismatch')
    instructions = rows(body)
    offsets = set(body)
    branches = []
    for offset,(op,arg,_) in sorted(body.items()):
        if op.startswith('if') or op in ('goto','goto_w','jsr','jsr_w'):
            require(arg.isdecimal() and int(arg) in offsets, 'invalid native branch target')
            branches.append({'offset':offset,'opcode':op,'target':int(arg)})
        require(op not in ('tableswitch','lookupswitch'), 'unexpected switch requires explicit finite CFG parser')
    return {'name':key[0], 'descriptor':key[1], 'coverage':'FULL_BODY', 'instruction_count':len(body),
        'instruction_sha256':digest(canonical(instructions).encode()), 'code_sha256':declaration['code_sha256'],
        'code_size':declaration['code_size'], 'access':declaration['access'],
        'exception_handlers':declaration['exception_handlers'], 'branches':branches,
        'pivots':list(pivots) if owner == MATERIAL else [
            {'offset':o,'opcode':op,'contains':sym or arg} for o,(op,arg,sym) in sorted(body.items())
            if MATERIAL in sym or op.startswith('if') or 'soundHolder' in sym or 'wrapAsHolder' in sym
                or (owner==DISPATCH and ('ACTickingItem' in sym))],
        'instructions':instructions if owner == MATERIAL else []}


def native_integration_checks(parsed):
    for owner in CONSUMERS:
        body = named(parsed[owner], '<init>')
        pivot(body, 2, 'invokevirtual', 'ACArmorMaterial.vanilla:')
        pivot(body, 21 if owner.endswith('DarknessArmorItem') else 15, 'invokevirtual', 'ACArmorMaterial.properties:')
        pivot(body, 24 if owner.endswith('DarknessArmorItem') else 18, 'invokespecial', 'ArmorItem."<init>":')
    diving = named(parsed[ITEM+'DivingArmorItem'],'<init>')
    for offset,op,token in [(63,'invokevirtual','ACArmorMaterial.defense:'),(81,'if_acmpne','113'),
        (97,'ldc2_w','double 0.5d'),(117,'if_acmpne','145'),(131,'invokevirtual','ACArmorMaterial.toughness:'),
        (146,'invokevirtual','ACArmorMaterial.knockbackResistance:'),(151,'ifle','179'),
        (165,'invokevirtual','ACArmorMaterial.knockbackResistance:'),(184,'putfield','divingArmorAttributes:')]:
        pivot(diving,offset,op,token)
    ginger = named(parsed[ITEM+'GingerbreadArmorItem'],'<init>')
    require(any('ACArmorMaterial.defense:' in sym for _,_,sym in ginger.values()), 'gingerbread defense snapshot missing')
    dispatch = named(parsed[DISPATCH], 'ac_inventoryTick')
    for offset,op,token in [(15,'instanceof','ACTickingItem'),(18,'ifeq','41'),
        (23,'checkcast','ACTickingItem'),(36,'invokeinterface','ACTickingItem.acInventoryTick:')]:
        pivot(dispatch,offset,op,token)
    compat = named(parsed[COMPAT], 'soundHolder')
    pivot(compat,0,'getstatic','BuiltInRegistries.SOUND_EVENT:')
    pivot(compat,4,'invokeinterface','Registry.wrapAsHolder:')


def verify_artifact(jar):
    require(jar.is_file() and jar.stat().st_size == SIZE, 'publisher artifact size mismatch')
    one,two = hashlib.sha1(),hashlib.sha256()
    with jar.open('rb') as handle:
        for block in iter(lambda:handle.read(1024*1024),b''):
            one.update(block);two.update(block)
    require(one.hexdigest() == SHA1 and two.hexdigest() == SHA256, 'publisher artifact digest mismatch')


def build_report(jar, javap):
    verify_artifact(jar)
    with zipfile.ZipFile(jar) as archive:
        census,metadata = typed_census(archive)
        class_hashes = {owner:digest(archive.read(owner+'.class')) for owner in sorted(metadata)}
        require(all(reader.major == 65 for reader in metadata.values()), 'selected class Java21 version drift')
        marker = metadata[MARKER]
        require(marker.access == 1537 and not marker.fields and not marker.methods and not marker.interfaces,
            'empty marker declaration drift')
        parsed = {owner:disassemble(jar,javap,owner) for owner in sorted(metadata)}
        for owner,methods in parsed.items():
            require(set(methods) == {(m['name'],m['descriptor']) for m in metadata[owner].methods}, 'javap/declared JVM method roster mismatch: '+owner)
        pivots = material_pivots(parsed[MATERIAL])
        definitions = material_definitions(parsed[REGISTRY])
        native_integration_checks(parsed)
        dark_tick = named(parsed[ITEM+'DarknessArmorItem'],'acInventoryTick')
        for offset,op,token in [(1,'instanceof','Player'),(4,'ifeq','30'),(16,'invokestatic','ACCompat.isWornArmor:'),
            (19,'ifeq','30'),(27,'invokevirtual','acArmorTick:')]:
            pivot(dark_tick,offset,op,token)
        mixin_raw = archive.read('alexscaves.mixins.json')
        mixin_json = json.loads(mixin_raw,object_pairs_hook=unique_pairs)
        require(mixin_json['package']=='com.github.alexmodguy.alexscaves.mixin' and
            mixin_json['mixins'].count('ItemStackTickMixin')==1, 'native tick mixin registration drift')
        resources = {'alexscaves.mixins.json':{'sha256':digest(mixin_raw),'package':mixin_json['package'],
            'registered_common_mixin':'ItemStackTickMixin'}}
        bootstrap = metadata[MATERIAL].attributes.get('bootstrap_methods',[])
        require(len(bootstrap)==1 and any(isinstance(a,dict) and a.get('reference',[]) ==
            [10,MATERIAL,[12,'getRepairIngredient','()Lnet/minecraft/world/item/crafting/Ingredient;']]
            and a.get('reference_kind') == 5 for a in bootstrap[0]['arguments']), 'repair supplier method-handle drift')
        native = {}
        for owner in sorted(parsed):
            selected = select_methods(owner,parsed[owner])
            declarations = {(m['name'],m['descriptor']):m for m in metadata[owner].methods}
            native[owner] = [method_report(owner,key,body,declarations[key],pivots.get(key,()) if owner==MATERIAL else ())
                for key,body in sorted(selected.items())]
    return {'schema_version':1, 'artifact':{'mod_id':'alexscaves','version':'1.0.10','size_bytes':SIZE,'sha1':SHA1,'sha256':SHA256},
        'claims':CLAIMS, 'axes':AXES, 'resources':resources, 'class_sha256':class_hashes, 'native_methods':native,
        'typed_reference_census':census, 'material_definitions':definitions, 'material_supplier_bootstrap':bootstrap,
        'marker':{'owner':MARKER,'access':1537,'fields':[],'declared_methods':[],
            'direct_implementers':[CONSUMERS[0]],'typed_dispatch_references':[],
            'darkness_inventory_tick_boundary':{'owner':ITEM+'DarknessArmorItem','name':'acInventoryTick',
                'coverage':'OPERAND_WINDOW_ONLY','window':[0,30],
                'instructions':rows({o:r for o,r in dark_tick.items() if o<=30}),
                'full_method_code_sha256':next(m['code_sha256'] for m in metadata[ITEM+'DarknessArmorItem'].methods if m['name']=='acInventoryTick'),
                'private_helper_declaration':next({k:m[k] for k in ('access','name','descriptor')}
                    for m in metadata[ITEM+'DarknessArmorItem'].methods if m['name']=='acArmorTick'),
                'limit':'Only Player/worn-armor gates and helper invocation; active power and cloak suffix are excluded.'},
            'actual_tick_dispatch':{'owner':DISPATCH,'name':'ac_inventoryTick','receiver_interface':TICKER,
                'interface_declaration':metadata[TICKER].methods,'type_check_offset':15,'invokeinterface_offset':36,
                'boundary':'Observed native method tests ACTickingItem; does not dispatch via ACArmorTickItem. Mixin application and gameplay outcomes are not tested.'},
            'disposition':'EMPTY_MARKER_SUPPORT_ONLY',
            'limit':'No typed dispatcher/member/class reference beyond declaration and sole direct implementer in 1555 publisher class entries. Reflective name construction, external mods and future versions are not closed.'},
        'integration_bounds':{'max_damage_array_by_ordinal':[13,15,16,11],
            'array_alias':'Long constructor stores caller int[] directly; no defensive copy or validation.',
            'ordinal_limit':'Only vanilla() skips ordinals >= damageReduction.length. properties() and defense() directly index arrays; null/short arrays or non-four-slot ordinals have no native guard.',
            'snapshot_and_live_state':'vanilla() snapshots defense/enchantability/sound/toughness/knockback in fresh ArmorMaterial+Holder; supplier captures this and reads current ingredient. Later setRepairMaterial including null affects future supplier reads; constructor values and arrays are not perk APIs.',
            'name':'Stored by constructor; not read by vanilla(), which passes List.of() as material layers.',
            'durability':'MAX_DAMAGE_ARRAY[type.ordinal()] * multiplier is JVM int multiplication, passed to supplied Item.Properties.durability; maximum configuration, no observed wear/repair settlement.',
            'native_bridge_ceiling':'Six direct item constructors; Diving/Gingerbread finite attributes and ACCompat sound/attribute bridges. ArmorItem, Item.Properties, Ingredient, registries, attribute engine and accepted gameplay outcomes remain external.',
            'excluded':'Active armor powers and tick behavior beyond the finite dispatch/operand witness, Minecraft/NeoForge engine internals, external consumers, perks/hooks, network authorization, rendering, resource packs, datapack/runtime registry contents and physical gameplay.'},
        'validation':{'authority':'SHA-exact publisher binary; public adjacent source is not used for installed parameters.',
            'reproduction':'Mandatory exact seal comparison; deterministic report, negative pivot/census/declaration tests and twice-run physical binary CLI idempotence.',
            'physical_cli_is_gameplay':False}}


def validate_report(report):
    require(isinstance(report,dict) and report.get('schema_version')==1, 'invalid armor report schema')
    require(report.get('claims')==CLAIMS, 'static claim ceiling drift')
    require(report.get('axes')==AXES, 'seven static axes drift')
    require(report.get('artifact')=={'mod_id':'alexscaves','version':'1.0.10','size_bytes':SIZE,'sha1':SHA1,'sha256':SHA256}, 'report artifact identity drift')
    require(set(report.get('native_methods',{}))=={MATERIAL,MARKER,REGISTRY,COMPAT,TICKER,DISPATCH,*CONSUMERS}, 'bounded native owner roster drift')
    require({(m['name'],m['descriptor']) for m in report['native_methods'][MATERIAL]}==MATERIAL_METHODS, 'report material JVM roster drift')
    require(report['marker']['declared_methods']==[] and report['marker']['direct_implementers']==[CONSUMERS[0]]
        and report['marker']['typed_dispatch_references']==[] and report['native_methods'][MARKER]==[], 'empty marker report drift')
    require(report['typed_reference_census']['class_entries_scanned']==1555, 'seal census total drift')


def compare_seal(report, expected):
    validate_report(expected)
    validate_report(report)
    require(report == expected, 'armor native seal mismatch')


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--jar',required=True,type=Path)
    parser.add_argument('--javap',required=True,type=Path)
    parser.add_argument('--seal',type=Path,default=SEAL)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args(argv)
    try:
        if args.output:
            require(args.output.resolve() not in {args.jar.resolve(),args.seal.resolve(),Path(__file__).resolve()}, 'output would overwrite an input/probe')
        expected=load_seal(args.seal)
        validate_report(expected)
        report=build_report(args.jar,args.javap)
        compare_seal(report, expected)
        payload=canonical(report)
        if args.output:
            args.output.parent.mkdir(parents=True,exist_ok=True)
            args.output.write_text(payload,encoding='utf8')
        else:
            sys.stdout.write(payload)
        return 0
    except (AuditError,ValueError,OSError,subprocess.SubprocessError,zipfile.BadZipFile,KeyError,TypeError) as error:
        print('armor-material audit failed: '+str(error),file=sys.stderr)
        return 1


if __name__=='__main__':
    raise SystemExit(main())
