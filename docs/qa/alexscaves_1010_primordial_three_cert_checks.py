#!/usr/bin/env python3
"""Fail-closed read-only seven-axis certification for three Primordial armor items.

Joins the SHA-exact Alex's Caves Continued publisher 1.0.10 report, existing
material/discovery seals and the official Mojang Minecraft 1.21.1 enum ABI.
Never certifies installed transformed runtime, FoodData outcome, mixin applied,
world-write, a mutating hook, perks or physical QA. No third-party code shipped.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
from pathlib import Path

OWNER = 'com/github/alexmodguy/alexscaves/server/item/PrimordialArmorItem'
REGISTRY = 'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry'
MIXIN = 'com/github/alexmodguy/alexscaves/mixin/PlayerMixin'
CHOP = 'com/github/alexmodguy/alexscaves/server/block/DinosaurChopBlock'
RENDER = 'com/github/alexmodguy/alexscaves/client/render/item/ACArmorRenderProperties'
PUB_SHA = '36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c'
PUB_SHA1 = '6960b299a39a039ac8a5eb9b07be4ad0e3e0a570'
PUB_REPORT = '659f60f17d549d8c795becc4d7fa7e6b8968cb546b8af002099b44abb65e4f75'
OFF_REPORT = 'e83bef57b5efb722a17fefb237edb7288b1668d99d7dae67e51c1905c174ff91'
OFF_ENUM_SHA = '304d6345c9ed3d0cdeaea281ed1171b98505b266c04e2b25a023dec665197732'
OFF_ENUM_INS_SHA = 'eba773c06e909e66e48c6aab76af27288097828da5b8a82c9b538e2d5d4af024'
OWNER_SHA = '8833c162d1507aba795b1ff809f5a6f6ddb846da308d809795cf80e69be5d09e'
METHODS = {
 '<init>': (12,'1c59bef51bc767350a0f79f732eac8355d4c7b6c50b864e6b32197f3a1efabf2'),
 'getArmorTexture': (7,'cda97c121e4aa31e0c82fbedb73ce9589c322d3bdefbaa0c7091e474dc815e5a'),
 'getExtraSaturationFromArmor': (31,'2fb7d7a8c00bc1a5b33c525f7da5b7c80d04b373b9c24bed3412fe4d04cc8317'),
 'initializeClient': (6,'241b312ebd6ff1e8ab0719a7fcbfd71c956258d303ba94e3a602770053402fa8'),
}
CONSUMERS = {
 RENDER: {'getACArmorModelBase':(41,'869cf27339be87b5b132d627ad041fe1781ae4a6f64b4923cd9616871a4c4886')},
 MIXIN: {'ac_eat':(31,'3f928fd639c0d5e62a849fdf302ba373fc304d4a4c8fff7cfd65e11a9a2abffd')},
 CHOP: {'eat':(89,'4e2b75751d124247a814dc386551010171bbfdc157b96a80f01c36c74cc4058c')},
 REGISTRY: {
  'lambda$static$42':(6,'a081b4b006913e5debfe0a59bee0ce182c8bf9646cfbec03b5e7def9b08e9e52'),
  'lambda$static$43':(6,'ea5e98aa42d728edfad89f30a2c3ef1b128eb2201de256e7c2d03a3826c0933d'),
  'lambda$static$44':(6,'9de2dc138983464c4e2ec94fcc01eecdc395519070e38407cba553608a54fda9'),
 }, OWNER: {},
}
PIECES = {
 'primordial_helmet': ('HELMET',0,'HEAD',42,3,260,26,'primordial_armor_0.png'),
 'primordial_tunic': ('CHESTPLATE',1,'CHEST',43,4,300,53,'primordial_armor_0.png'),
 'primordial_pants': ('LEGGINGS',2,'LEGS',44,3,320,80,'primordial_armor_1.png'),
}
POLICY = {'status':'CERTIFIED_STATIC_7_AXES','claim_scope':'STATIC_TECHNICAL_CATALOG_ONLY',
          'mutating_hook':'NOT_VERIFIED','physical_qa':'NOT_TESTED','perk_certification':'NOT_CERTIFIED',
          'runtime_dispatch':'NOT_VERIFIED','mutation':'NO_MUTATION','provider_universe_closed':False,
          'installed_transformed_runtime':'NOT_VERIFIED','new_magic_roots':0}
AXES = ('identity','behavior','parameters','targeting','costs','integration','validation')


def require(ok,msg):
    if not ok:raise ValueError(msg)

def unique(pairs):
    out={}
    for k,v in pairs:
        require(k not in out,'duplicate JSON key: '+str(k));out[k]=v
    return out

def load(path,limit=20000000):
    b=Path(path).read_bytes()
    require(0<len(b)<=limit,'untrusted file size '+str(path))
    return json.loads(b,object_pairs_hook=unique), hashlib.sha256(b).hexdigest()

def canonical(obj):return json.dumps(obj,indent=2,sort_keys=True,ensure_ascii=False)+'\n'

def sha(obj):return hashlib.sha256(canonical(obj).encode()).hexdigest()

def method_map(arr):
    res={}
    for m in arr:
        key=m['declaration']['name'];require(key not in res,'duplicate method '+key);res[key]=m
    return res

def pivot(m,offset,opcode,symbol=None):
    hits=[x for x in m['instructions'] if x['offset']==offset]
    require(len(hits)==1,'missing/duplicate offset '+str(offset))
    row=hits[0]
    require(row['opcode']==opcode and (symbol is None or symbol in row['symbol']+' '+row['operand']),
            'JVM pivot drift '+m['declaration']['name']+' @'+str(offset)+' '+opcode+' '+str(symbol))
    return row

def body_hashes(m, count, expected):
    require(m['instruction_count']==count==len(m['instructions']),'method instruction count')
    require(sha(m['instructions'])==m['instruction_sha256']==expected,'method hash drift '+m['declaration']['name'])
    off=[x['offset'] for x in m['instructions']]
    require(off==sorted(set(off)),'duplicate/unsorted code offsets')


def validate(official,report,material,discovery,seal,*,strict=True):
    if strict:
        require(sha(official)==OFF_REPORT,'complete original official report drift')
        require(sha(report)==PUB_REPORT,'complete original publisher report drift')
    require(official['schema']==1 and official['scope']=='MINECRAFT_1211_ARMOR_ITEM_TYPE_OFFICIAL_CLIENT_BINARY_DISCOVERY_NOT_INSTALLED_RUNTIME','official upstream scope')
    require(official['artifacts']['client']['sha256']=='499f6897d1837516680f3114072d8106e11c9adcd933fe5cf051b551089b0c99','official MC client bytes')
    require(official['artifacts']['client_mappings']['sha256']=='140c47931cccc8fc9e4c22d7603e2d714d1a953a146f51ea7397d95c955536ec','official mappings bytes')
    enum=official['enum']
    require(enum['class_sha256']==OFF_ENUM_SHA and enum['major']==65 and enum['mapped_name']=='net.minecraft.world.item.ArmorItem$Type' and enum['binary_name']=='csf$a','official exact enum class')
    require(enum['initializer_instruction_count']==51 and sha(enum['full_initializer'])==enum['initializer_instruction_sha256']==OFF_ENUM_INS_SHA,'official enum body')
    construction=enum['value_construction_sites']
    require([x['name'] for x in construction]==['HELMET','CHESTPLATE','LEGGINGS','BOOTS','BODY'],'official enum names/order')
    require([x['numeric_operands_before_ctor'][0][1] for x in construction]==[0,1,2,3,4],'official ordinals')
    require([x['assignment']['offset'] for x in construction]==[17,37,57,77,97],'official enum bytecode offsets')
    require(all(x['constructor']['opcode']=='invokespecial' and x['assignment']['opcode']=='putstatic' for x in construction),'official initializer control flow')
    require(report['scope']=='PRIMORDIAL_ARMOR_NATIVE_DISCOVERY_NOT_CERTIFIED' and report['schema_version']==1,'publisher report scope')
    require(report['artifact']=={'filename':'alexscaves-1.0.10-neoforge+1.21.1.jar','version':'1.0.10','sha1':PUB_SHA1,'sha256':PUB_SHA,'size_bytes':75279314,'installed_dump_comparison':'NOT_VERIFIED'},'publisher artifact')
    require(report['owner']==OWNER and report['registry_candidates_not_individually_certified']==list(PIECES),'publisher roster')
    require(report['native']['class_entries_scanned']==1555 and report['source_revision_parity']=='NOT_ASSUMED' and not report['other_consumers_complete'],'provider scoping')
    require(report['static_contract']=='NOT_CERTIFIED' and report['physical_qa']=='NOT_TESTED' and report['mutation']=='NO_MUTATION' and report['mutating_hook']=='NOT_VERIFIED' and report['provider_universe_closed']==False,'publisher discovery limits')
    native=report['native']['targets']
    require(set(native)=={OWNER},'native owner roster')
    owner=native[OWNER]
    require(owner['class_sha256']==OWNER_SHA and len(owner['methods'])==4 and len(owner['declarations'])==4 and len(owner['fields'])==0 and len(owner['in_jar_ancestors'])==0,'owner class/member census')
    methods=method_map(owner['methods']);require(set(methods)==set(METHODS),'native own methods')
    for name,(size,expected) in METHODS.items():body_hashes(methods[name],size,expected)
    require(set(owner['consumers'])==set(CONSUMERS),'typed consumer owner roster')
    for name,roster in CONSUMERS.items():
        data=owner['consumers'][name];body=method_map(data['bodies'])
        require(set(body)==set(roster),'consumer method roster '+name)
        require(len(data['sites'])==({'ACItemRegistry':6,'PrimordialArmorItem':0}.get(name.split('/')[-1],1)),'typed site count '+name)
        for meth,(size,expected) in roster.items():body_hashes(body[meth],size,expected)
    require(discovery['scope']==report['scope'] and discovery['report']['sha256']==PUB_REPORT and discovery['native_class']['sha256']==OWNER_SHA,'prior SHA-exact discovery seal')
    require(discovery['static_behavior']['worn_pieces_range']==[0,3] and discovery['static_behavior']['raw_meat_consumer']=='PlayerMixin.ac_eat' and discovery['static_behavior']['block_consumer']=='DinosaurChopBlock.eat','prior semantic discovery seal')
    require(report['filename_matched_resource_hashes']==discovery['resources'] and len(discovery['resources'])==8,'eight publisher resource hashes')
    defs=[x for x in material['material_definitions'] if x['registry_field']=='PRIMORDIAL_ARMOR_MATERIAL']
    require(len(defs)==1,'material registry identity')
    md=defs[0]
    for k,expected in {'damage_reduction_by_ordinal':[3,4,3,2],'durability_multiplier':20,'enchantability':25,'toughness':0,'knockback_resistance':0,'setup_repair_item':'TOUGH_HIDE','equip_sound_field':'ARMOR_EQUIP_LEATHER'}.items():
        require(md[k]==expected,'exact material '+k)
    require(material['integration_bounds']['max_damage_array_by_ordinal']==[13,15,16,11],'material durability array')
    require(material['claims']['static_technical_contract']=='CERTIFIED_STATIC_7_AXES' and material['claims']['mutation']=='NO_MUTATION','material upstream limits')
    require(seal['schema']==1 and seal['scope']=='ALEXSCAVES_1010_PRIMORDIAL_THREE_INDIVIDUAL_STATIC_CONTRACTS','own cert manifest scope')
    require(seal['states']==POLICY,'own cert safety ceiling')
    source=seal['sources']
    require(source['publisher_report_sha256']==PUB_REPORT and source['official_enum_report_sha256']==OFF_REPORT and source['publisher_sha256']==PUB_SHA and source['native_owner_sha256']==OWNER_SHA,'immutable sources')
    require(set(seal['objects'])==set(PIECES),'three object manifest entries')
    counter=methods['getExtraSaturationFromArmor']
    for off,op,word in [(3,'getstatic','EquipmentSlot.HEAD'),(9,'getstatic','PRIMORDIAL_HELMET'),(20,'invokevirtual','ItemStack.is'),(23,'ifeq',None),(26,'iinc','1, 1'),(30,'getstatic','EquipmentSlot.CHEST'),(36,'getstatic','PRIMORDIAL_TUNIC'),(47,'invokevirtual','ItemStack.is'),(50,'ifeq',None),(53,'iinc','1, 1'),(57,'getstatic','EquipmentSlot.LEGS'),(63,'getstatic','PRIMORDIAL_PANTS'),(74,'invokevirtual','ItemStack.is'),(77,'ifeq',None),(80,'iinc','1, 1'),(84,'ireturn',None)]:pivot(counter,off,op,word)
    constructors=method_map(owner['consumers'][REGISTRY]['bodies'])
    for item,(armor,ordinal,slot,fac,defense,dur,inc,texture) in PIECES.items():
        v=seal['objects'][item]
        assertmap={'resource_id':'alexscaves:'+item,'enum_constant':armor,'enum_ordinal':ordinal,
                   'equipment_slot':slot,'factory_method':'lambda$static$'+str(fac),
                   'armor_nominal':defense,'durability_max_configured':dur,
                   'model_sha256':report['filename_matched_resource_hashes']['assets/alexscaves/models/item/'+item+'.json']['sha256'],
                   'recipe_sha256':report['filename_matched_resource_hashes']['data/alexscaves/recipe/'+item+'.json']['sha256'],
                   'texture':'alexscaves:textures/armor/'+texture,
                   'worn_increment_offset':inc,'food_nutrition_argument_delta_per_piece':1,
                   'food_saturation_modifier_argument_delta_per_piece':0.125,
                   'repair_material':'alexscaves:tough_hide','evidence_axes':list(AXES)}
        require(v==assertmap,'static piece data mismatched '+item)
        require(defense==md['damage_reduction_by_ordinal'][ordinal] and dur==material['integration_bounds']['max_damage_array_by_ordinal'][ordinal]*md['durability_multiplier'],'per-piece ordinal bound '+item)
        factory=constructors['lambda$static$'+str(fac)]
        pivot(factory,0,'new','PrimordialArmorItem');pivot(factory,4,'getstatic','PRIMORDIAL_ARMOR_MATERIAL');pivot(factory,7,'getstatic','ArmorItem$Type.'+armor);pivot(factory,10,'invokespecial','PrimordialArmorItem');pivot(factory,13,'areturn')
        require(inc in [x['offset'] for x in counter['instructions'] if x['opcode']=='iinc'],'per-piece count pivot')
    mixin=method_map(owner['consumers'][MIXIN]['bodies'])['ac_eat']
    for off,op,t in [(2,'getstatic','RAW_MEATS'),(5,'invokevirtual','ItemStack.is'),(8,'ifeq',None),(12,'invokestatic','getExtraSaturationFromArmor'),(23,'ifeq',None),(27,'ifnull',None),(32,'invokestatic','ACCompat.nutrition'),(37,'iadd',None),(39,'invokestatic','ACCompat.saturationModifier'),(45,'ldc','0.125f'),(47,'fmul',None),(48,'fadd',None),(49,'invokevirtual','FoodData.eat:(IF)V'),(57,'invokevirtual','FoodData.eat:(Lnet/minecraft/world/food/FoodProperties;)V')]:pivot(mixin,off,op,t)
    chop=method_map(owner['consumers'][CHOP]['bodies'])['eat']
    for off,op,t in [(3,'invokevirtual','canEat'),(6,'ifne',None),(12,'areturn',None),(22,'getstatic','DINOSAUR_CHOP'),(30,'if_acmpne',None),(35,'invokestatic','getExtraSaturationFromArmor'),(53,'iload',None),(55,'iadd',None),(63,'ldc_w','0.125f'),(66,'fmul',None),(67,'fadd',None),(68,'invokevirtual','FoodData.eat:(IF)V'),(101,'if_icmpge',None),(124,'invokeinterface','LevelAccessor.setBlock'),(136,'invokeinterface','LevelAccessor.removeBlock'),(181,'invokeinterface','LevelAccessor.setBlock'),(199,'getstatic','InteractionResult.SUCCESS')]:pivot(chop,off,op,t)
    render=method_map(owner['consumers'][RENDER]['bodies'])['getACArmorModelBase']
    pivot(render,13,'instanceof','PrimordialArmorItem');pivot(render,19,'getstatic','PRIMORDIAL_ARMOR_MODEL')
    texture=methods['getArmorTexture'];pivot(texture,1,'getstatic','EquipmentSlot.LEGS');pivot(texture,7,'ldc','primordial_armor_1.png');pivot(texture,10,'ldc','primordial_armor_0.png')
    ctor=methods['<init>'];pivot(ctor,2,'invokevirtual','ACArmorMaterial.vanilla');pivot(ctor,15,'invokevirtual','ACArmorMaterial.properties');pivot(ctor,18,'invokespecial','ArmorItem')
    return True


def negatives(official,report,material,discovery,seal):
    cases=[]
    def case(label,fn):cases.append((label,fn))
    # Re-seal lower-level instructions to test the semantic check, not just outer hash.
    def corrupt_method(owner_name,meth,off,field,value):
        def func(o,r,m,d,s):
            obj=r['native']['targets'][OWNER]
            if owner_name=='owner':methods=method_map(obj['methods'])
            else:methods=method_map(obj['consumers'][owner_name]['bodies'])
            x=methods[meth];line=next(z for z in x['instructions'] if z['offset']==off)
            line[field]=value;x['instruction_sha256']=sha(x['instructions'])
        return func
    case('spoofed no-mutation contract',lambda o,r,m,d,s:s['states'].__setitem__('mutation','MUTATING'))
    case('spoofed QA',lambda o,r,m,d,s:s['states'].__setitem__('physical_qa','PASSED'))
    case('spoofed installed engine',lambda o,r,m,d,s:s['states'].__setitem__('installed_transformed_runtime','VERIFIED'))
    case('spoofed perk',lambda o,r,m,d,s:s['states'].__setitem__('perk_certification','CERTIFIED'))
    case('spoofed provider closure',lambda o,r,m,d,s:s['states'].__setitem__('provider_universe_closed',True))
    case('phantom fourth item',lambda o,r,m,d,s:s['objects'].__setitem__('primordial_boots',{}))
    case('wrong tunic ordinal',lambda o,r,m,d,s:s['objects']['primordial_tunic'].__setitem__('enum_ordinal',2))
    case('wrong pants defense',lambda o,r,m,d,s:s['objects']['primordial_pants'].__setitem__('armor_nominal',2))
    case('wrong helmet durability',lambda o,r,m,d,s:s['objects']['primordial_helmet'].__setitem__('durability_max_configured',300))
    case('wrong set count',lambda o,r,m,d,s:s['objects']['primordial_helmet'].__setitem__('food_nutrition_argument_delta_per_piece',2))
    case('unsafe Mastery assumption',lambda o,r,m,d,s:s['objects']['primordial_pants'].__setitem__('food_saturation_modifier_argument_delta_per_piece',2))
    case('mismatched original checksum',lambda o,r,m,d,s:s['sources'].__setitem__('publisher_report_sha256','0'*64))
    case('wrong model receipt',lambda o,r,m,d,s:s['objects']['primordial_helmet'].__setitem__('recipe_sha256','0'*64))
    case('wrong material defense',lambda o,r,m,d,s:m['material_definitions'][[x['registry_field'] for x in m['material_definitions']].index('PRIMORDIAL_ARMOR_MATERIAL')]['damage_reduction_by_ordinal'].__setitem__(0,99))
    case('wrong durability multiplier',lambda o,r,m,d,s:m['material_definitions'][[x['registry_field'] for x in m['material_definitions']].index('PRIMORDIAL_ARMOR_MATERIAL')].__setitem__('durability_multiplier',21))
    case('wrong material costs',lambda o,r,m,d,s:s['objects']['primordial_tunic'].__setitem__('repair_material','alexscaves:other'))
    case('corrupt official ordinal',lambda o,r,m,d,s:o['enum']['value_construction_sites'][1]['numeric_operands_before_ctor'][0].__setitem__(1,2))
    case('corrupt official class hash',lambda o,r,m,d,s:o['enum'].__setitem__('class_sha256','0'*64))
    case('corrupt discovery seal',lambda o,r,m,d,s:d['native_class'].__setitem__('sha256','0'*64))
    case('corrupt owner declaration roster',lambda o,r,m,d,s:r['native']['targets'][OWNER]['declarations'].pop())
    case('corrupt registered class hash',lambda o,r,m,d,s:r['native']['targets'][OWNER].__setitem__('class_sha256','0'*64))
    case('corrupt owner counting instructions resealed',corrupt_method('owner','getExtraSaturationFromArmor',26,'opcode','nop'))
    case('corrupt owner slot identity resealed',corrupt_method('owner','getExtraSaturationFromArmor',30,'symbol','Field net/minecraft/world/entity/EquipmentSlot.HEAD'))
    case('corrupt registry factory resealed',corrupt_method(REGISTRY,'lambda$static$43',7,'symbol','Field net/minecraft/world/item/ArmorItem$Type.HELMET'))
    case('corrupt raw meat gate resealed',corrupt_method(MIXIN,'ac_eat',2,'symbol','Field com/github/alexmodguy/alexscaves/server/misc/ACTagRegistry.OTHER'))
    case('corrupt raw meat nutrition resealed',corrupt_method(MIXIN,'ac_eat',37,'opcode','isub'))
    case('corrupt raw meat saturation resealed',corrupt_method(MIXIN,'ac_eat',45,'symbol','float 0.25f'))
    case('corrupt dinosaur gate resealed',corrupt_method(CHOP,'eat',22,'symbol','Field com/github/alexmodguy/alexscaves/server/block/ACBlockRegistry.OTHER'))
    case('corrupt dinosaur bonus resealed',corrupt_method(CHOP,'eat',63,'symbol','float 0.25f'))
    case('corrupt fooddata target resealed',corrupt_method(CHOP,'eat',68,'symbol','Method other.FoodData.eat:(IF)V'))
    case('corrupt Texture selection resealed',corrupt_method('owner','getArmorTexture',7,'symbol','String bad.png'))
    case('corrupt player modeling resealed',corrupt_method(RENDER,'getACArmorModelBase',13,'opcode','nop'))
    case('corrupt mixin branch resealed',corrupt_method(MIXIN,'ac_eat',23,'opcode','nop'))
    case('corrupt dinosaur world effect resealed',corrupt_method(CHOP,'eat',124,'opcode','nop'))
    case('corrupt primordial-count range',lambda o,r,m,d,s:d['static_behavior']['worn_pieces_range'].__setitem__(1,4))
    rejected=0
    for label,fn in cases:
        o,r,m,d,s=copy.deepcopy((official,report,material,discovery,seal))
        fn(o,r,m,d,s)
        try:validate(o,r,m,d,s,strict=False)
        except (ValueError,KeyError,TypeError,IndexError,AssertionError):rejected+=1
        else:raise ValueError('ADVERSARIAL FALSE ACCEPT: '+label)
    require(rejected==len(cases) and rejected>=30,'incomplete adversarial coverage')
    return rejected


def validate_files(cards_root,ledger,seal):
    cards_root=Path(cards_root)
    for name,values in PIECES.items():
        slug=name.replace('_','-');card=(cards_root/(slug+'.md')).read_text()
        require('CERTIFIED_STATIC_7_AXES' in card and 'NO_MUTATION' in card,'individual static card status '+name)
        for token in (name,'EXACT-PRIMORDIAL-ARMOR-THREE-PIECES-1.0.10.md',str(values[4]),str(values[5])):
            require(token in card,'individual static evidence link '+name+' '+token)
    require(ledger is not None,'ledger required')
    for name in PIECES:
        key='✅-alexs-caves-continued/items/'+name.replace('_','-')+'.md'
        item=ledger['objects'].get(key)
        require(item is not None and item['claim_scope']=='STATIC_TECHNICAL_CATALOG_ONLY' and item['evidence_grade']=='SHA_EXACT_BINARY_BEHAVIOR','ledger missing cert '+key)
        require(item['mutating_hook']=='NOT_VERIFIED' and item['physical_qa']=='NOT_TESTED' and item['mutation']=='NO_MUTATION' and item['perk_certification']=='NOT_CERTIFIED','ledger unsafe promotion')
        require(set(item['evidence'])==set(AXES),'ledger 7-axis completeness')


def cli():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--official',required=True,type=Path);p.add_argument('--publisher',required=True,type=Path)
    p.add_argument('--material',required=True,type=Path);p.add_argument('--discovery',required=True,type=Path)
    p.add_argument('--manifest',required=True,type=Path);p.add_argument('--cards-root',type=Path)
    p.add_argument('--ledger',type=Path);p.add_argument('--adversarial',action='store_true')
    a=p.parse_args()
    official,offs=load(a.official,30000);report,pubs=load(a.publisher,3000000);material,_=load(a.material,300000);discovery,_=load(a.discovery,150000);manifest,_=load(a.manifest,150000)
    require(offs==OFF_REPORT and pubs==PUB_REPORT,'raw exact report identity')
    validate(official,report,material,discovery,manifest)
    n=negatives(official,report,material,discovery,manifest) if a.adversarial else 0
    if a.cards_root:
        ledger,_=load(a.ledger,3000000)
        validate_files(a.cards_root,ledger,manifest)
    print('PASS: 3 Primordial individual static 7-axis contracts, exact MC enum & publisher method bodies, adversarial rejected',n)
    print('LIMITS NO_MUTATION NOT_VERIFIED NOT_TESTED NOT_CERTIFIED no new magic roots')

if __name__=='__main__':cli()
