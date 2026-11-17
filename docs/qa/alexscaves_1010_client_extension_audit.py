#!/usr/bin/env python3
"""Read-only exact-JAR client-extension ABI and finite output audit; no client execution.

The shared armor audit owns the unchanged classfile and javap parsers. This audit
counts declarations separately from typed member references, then follows only
the 19 callback bodies and finite proxy/property outputs. Rendering internals,
external engine callbacks and runtime registration remain outside this seal.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import subprocess
import sys
import zipfile

from alexscaves_1010_armor_material_audit import (
    AuditError, ClassReader, SHA1, SHA256, SIZE, canonical, digest, load_seal,
    parse_javap, require, verify_artifact,
)

ROOT = Path(__file__).resolve().parents[2]
PROVIDER = ROOT / 'wiki/modpack-catalog/providers/✅-alexs-caves-continued'
SEAL = PROVIDER / 'EXACT-CLIENT-EXTENSION-1.0.10.json'
PREFIX = 'com/github/alexmodguy/alexscaves/'
ITEM = PREFIX + 'server/item/'
TARGET = ITEM + 'ACClientExtensionItem'
EXTENSION = 'net/neoforged/neoforge/client/extensions/common/IClientItemExtensions'
CALLBACK = ('initializeClient', '(Ljava/util/function/Consumer;)V')
GENERIC = '(Ljava/util/function/Consumer<L' + EXTENSION + ';>;)V'
ARMOR = tuple(ITEM + name for name in ('DarknessArmorItem', 'DivingArmorItem',
    'GingerbreadArmorItem', 'HazmatArmorItem', 'PrimordialArmorItem', 'RainbounceBootsItem'))
ITEM_RENDER = tuple(ITEM + name for name in ('BlockItemWithISTER', 'CaveMapItem',
    'DreadbowItem', 'GalenaGauntletItem', 'OrtholanceItem', 'PrimitiveClubItem',
    'RaygunItem', 'ResistorShieldItem', 'SeaStaffItem', 'ShotGumItem', 'SpearItem', 'SugarStaffItem'))
CITADEL_ITEM = PREFIX + 'citadel/item/ItemCustomRender'
IMPLEMENTERS = tuple(sorted((*ARMOR, *ITEM_RENDER, CITADEL_ITEM)))
INHERITED = tuple(ITEM+name for name in ('ExtinctionSpearItem','FrostmintSpearItem','LimestoneSpearItem'))
REGISTRATION_EVENT = 'net/neoforged/neoforge/client/event/RegisterClientExtensionsEvent'
COMMON = PREFIX + 'server/CommonProxy'
CLIENT = PREFIX + 'client/ClientProxy'
CITADEL_PROXY = PREFIX + 'citadel/CitadelProxy'
CITADEL_CLIENT = PREFIX + 'citadel/CitadelClientProxy'
ITEM_PROPERTIES = PREFIX + 'client/render/item/ACItemRenderProperties'
ARMOR_PROPERTIES = PREFIX + 'client/render/item/ACArmorRenderProperties'
CITADEL_PROPERTIES = PREFIX + 'citadel/client/CitadelItemRenderProperties'
ITEM_RENDERER = PREFIX + 'client/render/item/ACItemstackRenderer'
CITADEL_RENDERER = PREFIX + 'citadel/client/CitadelItemstackRenderer'
OBJECT = '()Ljava/lang/Object;'
RENDERER_DESC = '()Lnet/minecraft/client/renderer/BlockEntityWithoutLevelRenderer;'
MODEL_DESC = '(Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/client/model/Model;)Lnet/minecraft/client/model/Model;'
BASE_DESC = '(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/client/model/Model;)Lnet/minecraft/client/model/Model;'
ANIMATION_DESC = '(Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/client/model/Model;)Lnet/minecraft/client/model/Model;'
HUMANOID_DESC = '(Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/entity/EquipmentSlot;Lnet/minecraft/client/model/HumanoidModel;)Lnet/minecraft/client/model/HumanoidModel;'
SELECTED = {
    COMMON: {('getISTERProperties', OBJECT), ('getArmorProperties', OBJECT)},
    CLIENT: {('<init>', '()V'), ('getISTERProperties', OBJECT), ('getArmorProperties', OBJECT)},
    CITADEL_PROXY: {('getISTERProperties', OBJECT)},
    CITADEL_CLIENT: {('getISTERProperties', OBJECT)},
    ITEM_PROPERTIES: {('<init>', '()V'), ('getCustomRenderer', RENDERER_DESC)},
    CITADEL_PROPERTIES: {('<init>', '()V'), ('getCustomRenderer', RENDERER_DESC)},
    ARMOR_PROPERTIES: {('<init>', '()V'), ('initializeModels', '()V'),
        ('getHumanoidArmorModel', HUMANOID_DESC), ('getACArmorModel', MODEL_DESC),
        ('getACArmorModelBase', BASE_DESC), ('applyACArmorAnimations', ANIMATION_DESC)},
}
MODEL_ROSTER = (
    ('PrimordialArmorItem', 'PrimordialArmorModel', 'PRIMORDIAL_ARMOR'),
    ('HazmatArmorItem', 'HazmatArmorModel', 'HAZMAT_ARMOR'),
    ('DivingArmorItem', 'DivingArmorModel', 'DIVING_ARMOR'),
    ('DarknessArmorItem', 'DarknessArmorModel', 'DARKNESS_ARMOR'),
    ('RainbounceBootsItem', 'RainbounceArmorModel', 'RAINBOUNCE_ARMOR'),
    ('GingerbreadArmorItem', 'GingerbreadArmorModel', 'GINGERBREAD_ARMOR'),
)
CLAIMS = {'claim_scope': 'STATIC_TECHNICAL_CATALOG_ONLY', 'evidence_grade': 'SHA_EXACT_BINARY_BEHAVIOR',
    'static_technical_contract': 'CERTIFIED_STATIC_7_AXES', 'mutating_hook': 'NOT_VERIFIED',
    'physical_qa': 'NOT_TESTED', 'perk_certification': 'NOT_CERTIFIED', 'mutation': 'NO_MUTATION',
    'provider_universe_closed': False, 'semantic_magic_roots_delta': 0}
AXES = {
    'identity': 'Publisher 1.0.10 SHA-1/SHA-256/size; Java21 class identity, one abstract erased Consumer ABI and generic IClientItemExtensions declaration.',
    'behavior': 'Nineteen direct implementer callbacks delegate to a proxy getter, cast the result and invoke Consumer.accept once; finite property renderer/model outputs only.',
    'parameters': 'Twelve native item-render callbacks, six native armor callbacks and one relocated Citadel callback; exact operands, property/renderer lifetimes, six model selection branches and supplied fallback.',
    'targeting': 'Not applicable: these selected methods configure client presentation and model selection; no target query, damage request, projectile or gameplay effect application is present.',
    'costs': 'Not applicable: no mana, cast, durability settlement or gameplay cooldown in the selected callback/property methods. Object allocations and model baking are presentation work, not certified gameplay costs.',
    'integration': 'Static callback declarations and finite CommonProxy/ClientProxy and relocated Citadel property outputs; zero publisher initializeClient member references. External engine dispatch, proxy selection, registration execution and perks are unverified.',
    'validation': 'Typed 1555-class census, member-reference/declaration separation, complete selected bodies and hashes, explicit pivots, negative checks and deterministic exact-JAR CLI reproduction; physical client execution is NOT_TESTED.',
}


def initialize_member_references(reader):
    """Memberref evidence only; a declared method or UTF8 name is not a caller."""
    result = []
    for index, entry in enumerate(reader.pool):
        if entry is not None and entry[0] in (10, 11):
            tag, owner, signature = reader.resolve(index)
            if signature[1] == CALLBACK[0]:
                result.append({'constant_pool_index': index,
                    'kind': 'method_reference' if tag == 10 else 'interface_method_reference',
                    'receiver_owner': owner, 'name': signature[1], 'descriptor': signature[2]})
    return result


def typed_census(archive):
    names = archive.namelist()
    require(len(names) == len(set(names)), 'duplicate ZIP members')
    paths = sorted(name for name in names if name.endswith('.class'))
    owners, declarations, memberrefs, metadata, hierarchy, event_refs = [], [], [], {}, {}, []
    selected = {TARGET, *IMPLEMENTERS, *INHERITED, *SELECTED}
    for path in paths:
        reader = ClassReader(archive.read(path))
        require(path == reader.name + '.class', 'class path/declaration mismatch: ' + path)
        if reader.name in selected:
            metadata[reader.name] = reader
        hierarchy[reader.name]={'parent':reader.parent,'interfaces':reader.interfaces,'access':reader.access}
        refs = reader.typed_refs(TARGET)
        if refs:
            owners.append({'owner': reader.name, 'implements_directly': TARGET in reader.interfaces,
                'extends_directly': reader.parent == TARGET, 'typed_references': refs})
        for method in reader.methods:
            if method['name'] == CALLBACK[0]:
                declarations.append({'owner': reader.name, 'method': method})
        for reference in initialize_member_references(reader):
            memberrefs.append({'owner': reader.name, **reference})
        if reader.typed_refs(REGISTRATION_EVENT):
            event_refs.append(reader.name)
    require(len(paths) == 1555, 'whole-JAR class census drift')
    require({row['owner'] for row in owners} == {TARGET, *IMPLEMENTERS}, 'target typed owner roster drift')
    require({row['owner'] for row in owners if row['implements_directly']} == set(IMPLEMENTERS),
        'nineteen direct implementers drift')
    require(not memberrefs, 'initializeClient acquired a publisher typed member reference')
    require(not event_refs, 'publisher acquired a typed RegisterClientExtensionsEvent reference')
    expected_declarations = {TARGET, *IMPLEMENTERS, PREFIX+'server/block/fluid/ACClientExtensionFluidType',
        PREFIX+'server/block/fluid/AcidFluidType', PREFIX+'server/block/fluid/PurpleSodaFluidType'}
    require({row['owner'] for row in declarations} == expected_declarations and len(declarations) == 23,
        'all-owner initializeClient declaration roster drift')
    require(all(row['method']['descriptor'] == CALLBACK[1] for row in declarations), 'callback descriptor drift')
    require(set(metadata) == selected, 'bounded native owner missing')
    def assignable(owner, active=()):
        if owner==TARGET:
            return True
        if owner not in hierarchy:
            return False  # External engine hierarchy is not inferred.
        require(owner not in active, 'cyclic publisher class hierarchy')
        info=hierarchy[owner]
        return any(assignable(parent,(*active,owner)) for parent in [info['parent'],*info['interfaces']] if parent)
    concrete=sorted(owner for owner,info in hierarchy.items() if not info['access'] & (512|1024) and assignable(owner))
    require(set(concrete)=={*IMPLEMENTERS,*INHERITED}, 'concrete publisher assignability roster drift')
    inherited=[]
    for owner in INHERITED:
        reader=metadata[owner]
        require(reader.parent==ITEM+'SpearItem' and not any(m['name']==CALLBACK[0] for m in reader.methods),
            'inherited SpearItem callback resolution drift')
        inherited.append({'owner':owner,'parent':reader.parent,'interfaces':reader.interfaces,
            'access':reader.access,'declared_callbacks':[], 'callback_declaring_owner':ITEM+'SpearItem'})
    return {'class_entries_scanned': len(paths),
        'class_path_roster_sha256': digest(('\n'.join(paths)+'\n').encode()),
        'method': 'CLASS/Fieldref/Methodref/InterfaceMethodref/NameAndType/MethodType plus declared JVM descriptors; UTF8/String names alone do not count',
        'target': TARGET, 'target_owners': owners,
        'initialize_client_declarations': declarations,
        'initialize_client_member_references': memberrefs,
        'registration_event':REGISTRATION_EVENT, 'registration_event_typed_owners':event_refs,
        'assignability_census':{'direct_implementers':list(IMPLEMENTERS),'inherited_implementers':inherited,
            'concrete_assignable':concrete,'scope':'Publisher class parent/interface graph only; external subclasses and runtime loading are not enumerated.'},
        'member_reference_scope': 'Every Methodref and InterfaceMethodref named initializeClient, any owner and any descriptor; includes references reachable by method handles but does not infer reflective/external calls'}, metadata


def disassemble(jar, javap, owner):
    result = subprocess.run([str(javap), '-classpath', str(jar), '-p', '-c', '-s', owner.replace('/', '.')],
        capture_output=True, text=True, timeout=60)
    require(result.returncode == 0, 'javap failed for ' + owner + ': ' + result.stderr[:300])
    return parse_javap(result.stdout, owner), result.stdout


def rows(body):
    return [{'offset': offset, 'opcode': op, 'operand': arg, 'symbol': symbol}
        for offset, (op, arg, symbol) in sorted(body.items())]


def pivot(body, offset, opcode, token=''):
    row = body.get(offset)
    require(row is not None and row[0] == opcode and token in (row[1]+' '+row[2]),
        f'client-extension native pivot drift at {offset}: {opcode} {token}')
    return {'offset': offset, 'opcode': opcode, 'contains': token}


def callback_pivots(owner, body):
    require(owner in IMPLEMENTERS, 'unbounded callback owner')
    require(set(body) == {0,1,4,7,10,15}, 'six-instruction callback body drift')
    citadel = owner == CITADEL_ITEM
    proxy = CITADEL_PROXY if citadel else COMMON
    source = PREFIX+'citadel/Citadel' if citadel else PREFIX+'AlexsCaves'
    getter = 'getArmorProperties' if owner in ARMOR else 'getISTERProperties'
    specs = [(0,'aload_1',''), (1,'getstatic', 'Field '+source+'.PROXY:L'+proxy+';'),
        (4,'invokevirtual', 'Method '+proxy+'.'+getter+':'+OBJECT),
        (7,'checkcast','class '+EXTENSION),
        (10,'invokeinterface','InterfaceMethod java/util/function/Consumer.accept:(Ljava/lang/Object;)V'),
        (15,'return','')]
    return [pivot(body, *spec) for spec in specs]


def output_pivots(parsed):
    checks = {}
    def check(owner, name, specs, desc=None):
        keys = [key for key in parsed[owner] if key[0] == name and (desc is None or key[1] == desc)]
        require(len(keys) == 1, 'missing/ambiguous finite output method: '+owner+'.'+name)
        key = keys[0]
        checks[owner,key] = [pivot(parsed[owner][key], *spec) for spec in specs]
        return parsed[owner][key]
    for owner,names in ((COMMON,('getISTERProperties','getArmorProperties')), (CITADEL_PROXY,('getISTERProperties',))):
        for name in names:
            body=check(owner,name,[(0,'aconst_null',''),(1,'areturn','')])
            require(set(body)=={0,1}, 'common proxy null-return body drift')
    check(CLIENT,'<init>',[(5,'new','class '+ITEM_PROPERTIES),(9,'invokespecial',ITEM_PROPERTIES+'."<init>":()V'),
        (12,'putfield','isterProperties:L'+ITEM_PROPERTIES+';'),(16,'new','class '+ARMOR_PROPERTIES),
        (20,'invokespecial',ARMOR_PROPERTIES+'."<init>":()V'),(23,'putfield','armorProperties:L'+ARMOR_PROPERTIES+';'),(26,'return','')])
    for name,field,owner in (('getISTERProperties','isterProperties',ITEM_PROPERTIES),('getArmorProperties','armorProperties',ARMOR_PROPERTIES)):
        body=check(CLIENT,name,[(0,'aload_0',''),(1,'getfield','Field '+field+':L'+owner+';'),(4,'areturn','')])
        require(set(body)=={0,1,4}, 'native proxy getter body drift')
    check(CITADEL_CLIENT,'getISTERProperties',[(0,'new','class '+CITADEL_PROPERTIES),
        (4,'invokespecial',CITADEL_PROPERTIES+'."<init>":()V'),(7,'areturn','')])
    check(ITEM_PROPERTIES,'getCustomRenderer',[(0,'new','class '+ITEM_RENDERER),
        (4,'invokespecial',ITEM_RENDERER+'."<init>":()V'),(7,'areturn','')])
    # Citadel's renderer lives with each newly returned property object.
    constructor=parsed[CITADEL_PROPERTIES]['<init>','()V']
    renderer_types=[sym.removeprefix('class ') for op,_,sym in constructor.values() if op=='new']
    require(renderer_types==[CITADEL_RENDERER], 'Citadel renderer type drift')
    check(CITADEL_PROPERTIES,'<init>',[(5,'new','class '+CITADEL_RENDERER),
        (9,'invokespecial',CITADEL_RENDERER+'."<init>":()V'),(12,'putfield','Field renderer:')])
    check(CITADEL_PROPERTIES,'getCustomRenderer',[(0,'aload_0',''),(1,'getfield','Field renderer:'),(4,'areturn','')])
    init_specs=[(0,'iconst_1',''),(1,'putstatic','Field init:Z'),(136,'return','')]
    base_specs=[(0,'getstatic','Field init:Z'),(3,'ifne','9'),(6,'invokestatic','Method initializeModels:()V'),(93,'aload_1',''),(94,'areturn','')]
    for index,(item,model,field) in enumerate(MODEL_ROSTER):
        start=4+22*index
        init_specs += [(start,'new','class '+PREFIX+'client/model/layered/'+model),
            (start+10,'getstatic','ACModelLayers.'+field+':'),(start+13,'invokevirtual','EntityModelSet.bakeLayer:'),
            (start+16,'invokespecial',model+'."<init>":'),(start+19,'putstatic','Field '+field+'_MODEL:')]
        start=13+14*index
        base_specs += [(start,'instanceof','class '+ITEM+item),(start+3,'ifeq',str(start+10)),
            (start+6,'getstatic','Field '+field+'_MODEL:'),(start+9,'areturn','')]
    check(ARMOR_PROPERTIES,'initializeModels',init_specs)
    check(ARMOR_PROPERTIES,'getACArmorModelBase',base_specs)
    humanoid=check(ARMOR_PROPERTIES,'getHumanoidArmorModel',[(0,'aload_1',''),(1,'aload_2',''),
        (2,'aload','4'),(4,'invokestatic','Method getACArmorModel:'+MODEL_DESC),
        (7,'checkcast','class net/minecraft/client/model/HumanoidModel'),(10,'areturn','')])
    require(set(humanoid)=={0,1,2,4,7,10}, 'armor getter acquired slot-dependent behavior')
    check(ARMOR_PROPERTIES,'getACArmorModel',[(3,'invokestatic','Method getACArmorModelBase:'+BASE_DESC),
        (6,'invokestatic','Method applyACArmorAnimations:'+ANIMATION_DESC),(9,'areturn','')])
    check(ARMOR_PROPERTIES,'applyACArmorAnimations',[(1,'ifnonnull','6'),(4,'aload_1',''),(5,'areturn',''),
        (7,'instanceof','PrimordialArmorModel'),(10,'ifeq','24'),(20,'invokevirtual','PrimordialArmorModel.withAnimations:'),
        (25,'instanceof','HazmatArmorModel'),(28,'ifeq','42'),(38,'invokevirtual','HazmatArmorModel.withAnimations:'),
        (43,'instanceof','DarknessArmorModel'),(46,'ifeq','60'),(56,'invokevirtual','DarknessArmorModel.withAnimations:'),
        (60,'aload_1',''),(61,'areturn','')])
    return checks


def method_report(key, body, declaration, pivots):
    require(bool(body) == ('code_sha256' in declaration), 'Code/declaration mismatch')
    branches=[]
    for offset,(op,arg,_) in sorted(body.items()):
        require(op not in ('tableswitch','lookupswitch'), 'finite output acquired unparsed switch')
        if op.startswith('if') or op in ('goto','goto_w','jsr','jsr_w'):
            require(arg.isdecimal() and int(arg) in body, 'invalid finite output branch target')
            branches.append({'offset':offset,'opcode':op,'target':int(arg)})
    instructions=rows(body)
    return {'name':key[0], 'descriptor':key[1], 'access':declaration['access'], 'coverage':'FULL_BODY',
        'code_sha256':declaration['code_sha256'], 'code_size':declaration['code_size'],
        'instruction_count':len(body), 'instruction_sha256':digest(canonical(instructions).encode()),
        'exception_handlers':declaration['exception_handlers'], 'branches':branches,
        'pivots':pivots, 'instructions':instructions}


def build_report(jar, javap):
    verify_artifact(jar)
    with zipfile.ZipFile(jar) as archive:
        census,metadata=typed_census(archive)
        require(all(reader.major==65 for reader in metadata.values()), 'selected Java21 class version drift')
        interface=metadata[TARGET]
        require(interface.access==1537 and not interface.fields and not interface.interfaces and
            interface.methods==[{'access':1025,'name':CALLBACK[0],'descriptor':CALLBACK[1]}], 'abstract interface ABI drift')
        require(GENERIC in [v for tag,v in interface.pool[1:] if tag==1], 'generic client-extension signature drift')
        disassembly_owners=sorted({TARGET,*IMPLEMENTERS,*SELECTED})
        with ThreadPoolExecutor(max_workers=4) as executor:
            results=dict(zip(disassembly_owners,executor.map(lambda owner:disassemble(jar,javap,owner),disassembly_owners)))
        parsed={owner:result[0] for owner,result in results.items()}
        generic_declaration='public abstract void initializeClient(java.util.function.Consumer<'+EXTENSION.replace('/','.')+'>);'
        require(generic_declaration in results[TARGET][1], 'javap generic method declaration drift')
        for owner,methods in parsed.items():
            require(set(methods)=={(m['name'],m['descriptor']) for m in metadata[owner].methods}, 'javap/declaration roster mismatch: '+owner)
        require(parsed[TARGET]=={CALLBACK:{}}, 'abstract interface acquired executable body')
        checks=output_pivots(parsed)
        callbacks=[]
        for owner in IMPLEMENTERS:
            declaration=next(m for m in metadata[owner].methods if (m['name'],m['descriptor'])==CALLBACK)
            require(declaration['access']==1 and declaration.get('code_size')==16 and not declaration['exception_handlers'],
                'public 16-byte callback declaration drift')
            citadel=owner==CITADEL_ITEM
            callbacks.append({'owner':owner, 'extension_family':'ARMOR_MODEL' if owner in ARMOR else 'ITEM_RENDERER',
                'proxy_field_owner':PREFIX+('citadel/Citadel' if citadel else 'AlexsCaves'),
                'proxy_getter_owner':CITADEL_PROXY if citadel else COMMON,
                'proxy_getter':'getArmorProperties' if owner in ARMOR else 'getISTERProperties',
                'method':method_report(CALLBACK,parsed[owner][CALLBACK],declaration,callback_pivots(owner,parsed[owner][CALLBACK]))})
        native={}
        for owner,keys in sorted(SELECTED.items()):
            declarations={(m['name'],m['descriptor']):m for m in metadata[owner].methods}
            require(keys<=set(parsed[owner]), 'selected finite method missing')
            native[owner]=[method_report(key,parsed[owner][key],declarations[key],checks.get((owner,key),[])) for key in sorted(keys)]
        property_declarations={owner:{'interfaces':metadata[owner].interfaces,'fields':metadata[owner].fields,
            'declared_methods':[{k:m[k] for k in ('access','name','descriptor')} for m in metadata[owner].methods]}
            for owner in (ITEM_PROPERTIES,ARMOR_PROPERTIES,CITADEL_PROPERTIES)}
        require(all(row['interfaces']==[EXTENSION] for row in property_declarations.values()), 'property extension interface drift')
        for field in ('isterProperties','armorProperties'):
            require(next(m['access'] for m in metadata[CLIENT].fields if m['name']==field)==18, 'native private-final property field drift')
        require(next(m['access'] for m in metadata[CITADEL_PROPERTIES].fields if m['name']=='renderer')==18, 'Citadel private-final renderer field drift')
        require(next(m['access'] for m in metadata[ARMOR_PROPERTIES].fields if m['name']=='init')==10, 'mutable static model initialization flag drift')
        for _,_,field in MODEL_ROSTER:
            require(next(m['access'] for m in metadata[ARMOR_PROPERTIES].fields if m['name']==field+'_MODEL')==9, 'mutable public-static armor model field drift')
        hashes={owner:digest(archive.read(owner+'.class')) for owner in sorted(metadata)}
    return {'schema_version':1,
        'artifact':{'mod_id':'alexscaves','version':'1.0.10','size_bytes':SIZE,'sha1':SHA1,'sha256':SHA256},
        'claims':CLAIMS, 'axes':AXES, 'class_sha256':hashes,
        'interface_contract':{'owner':TARGET,'access':1537,'fields':[],'interfaces':[],
            'declared_methods':interface.methods,'generic_signature':GENERIC,
            'generic_declaration':generic_declaration,'executable_code':False},
        'typed_reference_census':census, 'callbacks':callbacks, 'native_methods':native,
        'property_declarations':property_declarations,
        'extension_outputs':{
            'native_properties_lifetime':'ClientProxy constructor creates one ACItemRenderProperties and one ACArmorRenderProperties, stores private final fields; getters return those fields per proxy instance.',
            'native_item_renderer_lifetime':'ACItemRenderProperties.getCustomRenderer creates a fresh ACItemstackRenderer on every call; no renderer cache is declared in this properties class.',
            'citadel_properties_lifetime':'CitadelClientProxy.getISTERProperties creates fresh CitadelItemRenderProperties each call; its constructor stores one private final CitadelItemstackRenderer and getCustomRenderer returns that renderer.',
            'common_proxy_returns':'CommonProxy both getters and CitadelProxy.getISTERProperties return null; a successful client proxy selection or non-null registration is not inferred.',
            'armor_model_roster':[{'item_owner':ITEM+item,'model_owner':PREFIX+'client/model/layered/'+model,
                'layer_field':field,'model_field':field+'_MODEL'} for item,model,field in MODEL_ROSTER],
            'armor_model_selection':'getHumanoidArmorModel ignores EquipmentSlot, passes entity/stack/supplied model to getACArmorModel, casts result to HumanoidModel; six ordered instanceof item branches return mutable public static model fields; unmatched stack returns supplied fallback model.',
            'armor_initialization':'getACArmorModelBase calls initializeModels only while init is false; initializeModels sets mutable static init=true before six Minecraft layer bakes/model allocations. No exception handlers; runtime bake success and recovery are not established.',
            'armor_animation_boundary':'Null entity returns supplied selected model. Primordial/Hazmat/Darkness model instances invoke corresponding withAnimations; other models pass through. Those model bodies and rendering internals are excluded.',
            'slot_argument_used':False,
        },
        'registration_boundary':{
            'publisher_typed_initialize_client_callers':0, 'registration_execution':'NOT_VERIFIED',
            'external_engine_callback_dispatch':'NOT_VERIFIED', 'proxy_selection_and_client_initialization':'NOT_VERIFIED',
            'absence_scope':'Zero typed Methodref/InterfaceMethodref calls named initializeClient in this exact publisher JAR; this does not prove runtime non-use, because external engine dispatch, reflection or external consumers may invoke declarations.',
            'independent_model_property_events':'ClientProxy model-property registration is an independent presentation surface, not evidence of an ACClientExtensionItem dispatcher.',
            'excluded':'External Minecraft/NeoForge Item and IClientItemExtensions engine bodies, runtime event registration, reflective calls, renderer CFG, layer/model/withAnimations internals, resource-pack rendering, active equipment powers, gameplay authorization, mutating hooks, perks and physical client execution.',
        },
        'validation':{'authority':'SHA-exact publisher binary; no adjacent source is used for installed behavior.',
            'reproduction':'Mandatory seal comparison; deterministic full selected method rows/code hashes, typed census and explicit pivots; negative mutation checks and twice-run physical-binary CLI idempotence.',
            'physical_cli_is_gameplay':False}}


def validate_report(report):
    require(isinstance(report,dict) and report.get('schema_version')==1, 'invalid client-extension report schema')
    require(report.get('claims')==CLAIMS, 'static claim ceiling drift')
    require(report.get('axes')==AXES, 'seven static axes drift')
    require(report.get('artifact')=={'mod_id':'alexscaves','version':'1.0.10','size_bytes':SIZE,'sha1':SHA1,'sha256':SHA256}, 'report artifact identity drift')
    interface=report['interface_contract']
    require(interface['owner']==TARGET and interface['access']==1537 and interface['fields']==[] and
        interface['interfaces']==[] and interface['declared_methods']==[{'access':1025,'name':CALLBACK[0],'descriptor':CALLBACK[1]}]
        and interface['generic_signature']==GENERIC and interface['executable_code'] is False, 'report abstract ABI drift')
    census=report['typed_reference_census']
    require(census['class_entries_scanned']==1555 and census['target']==TARGET and
        census['initialize_client_member_references']==[] and len(census['initialize_client_declarations'])==23 and
        census['registration_event']==REGISTRATION_EVENT and census['registration_event_typed_owners']==[],
        'report typed census drift')
    inheritance=census['assignability_census']
    require(inheritance['direct_implementers']==list(IMPLEMENTERS) and
        {r['owner'] for r in inheritance['inherited_implementers']}==set(INHERITED) and
        set(inheritance['concrete_assignable'])=={*IMPLEMENTERS,*INHERITED}, 'report assignability census drift')
    require(all(r['parent']==ITEM+'SpearItem' and r['callback_declaring_owner']==ITEM+'SpearItem' and
        r['declared_callbacks']==[] for r in inheritance['inherited_implementers']), 'report inherited callback declaration drift')
    require({r['owner'] for r in census['target_owners']}=={TARGET,*IMPLEMENTERS}, 'report typed owner drift')
    require({r['owner'] for r in census['target_owners'] if r['implements_directly']}==set(IMPLEMENTERS), 'report direct implementer drift')
    require(len(report['callbacks'])==19 and {r['owner'] for r in report['callbacks']}==set(IMPLEMENTERS), 'report callback roster drift')
    for callback in report['callbacks']:
        method=callback['method']
        require((method['name'],method['descriptor'])==CALLBACK and method['access']==1 and
            method['instruction_count']==6 and method['code_size']==16 and method['exception_handlers']==[], 'report callback body drift')
        callback_pivots(callback['owner'],{r['offset']:(r['opcode'],r['operand'],r['symbol']) for r in method['instructions']})
    require(set(report['native_methods'])==set(SELECTED), 'bounded finite output owner roster drift')
    for owner,keys in SELECTED.items():
        require({(m['name'],m['descriptor']) for m in report['native_methods'][owner]}==keys, 'finite output JVM method roster drift')
    require(report['extension_outputs']['slot_argument_used'] is False, 'armor slot-use ceiling drift')
    require(report['registration_boundary']['publisher_typed_initialize_client_callers']==0 and
        all(report['registration_boundary'][key]=='NOT_VERIFIED' for key in
            ('registration_execution','external_engine_callback_dispatch','proxy_selection_and_client_initialization')), 'unverified registration ceiling drift')
    for method in [r['method'] for r in report['callbacks']]+[m for group in report['native_methods'].values() for m in group]:
        require(method['instruction_count']==len(method['instructions']) and
            method['instruction_sha256']==digest(canonical(method['instructions']).encode()), 'instruction record digest drift')


def compare_seal(report, expected):
    validate_report(expected)
    validate_report(report)
    require(report==expected, 'client-extension native seal mismatch')


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--jar',required=True,type=Path)
    parser.add_argument('--javap',required=True,type=Path)
    parser.add_argument('--seal',type=Path,default=SEAL)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args(argv)
    try:
        if args.output:
            protected={args.jar.resolve(),args.javap.resolve(),args.seal.resolve(),SEAL.resolve(),Path(__file__).resolve(),
                Path(sys.modules[ClassReader.__module__].__file__).resolve(),
                Path(sys.modules[parse_javap.__module__].__file__).resolve()}
            require(args.output.resolve() not in protected, 'output would overwrite an input/probe')
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
        print('client-extension audit failed: '+str(error),file=sys.stderr)
        return 1


if __name__=='__main__':
    raise SystemExit(main())
