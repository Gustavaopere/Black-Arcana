#!/usr/bin/env python3
"""Rainbounce Boots: SHA-exact one-object static certification, fail-closed.

Reconstructs full publisher and Mojang official 1.21.1 enum reports. Checks
the previous bounded discovery seal independently, plus the material contract,
item-specific branches/parameters and ledger. Never certifies transformed
mixin, accepted movement, safe mutation, perks or physical QA.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path

import alexscaves_1010_rainbounce_boots_discovery_checks as original

OWNER = 'com/github/alexmodguy/alexscaves/server/item/RainbounceBootsItem'
MIXIN = 'com/github/alexmodguy/alexscaves/mixin/EntityMixin'
REG = 'com/github/alexmodguy/alexscaves/server/item/ACItemRegistry'
RENDER = 'com/github/alexmodguy/alexscaves/client/render/item/ACArmorRenderProperties'
PUBLISHER = '36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c'
REPORT = 'c7e60198eae632614c4a87acda39f385f49347409f47d0b178f5733362a7be60'
OFFICIAL = 'e83bef57b5efb722a17fefb237edb7288b1668d99d7dae67e51c1905c174ff91'
OFF_CLASS = '304d6345c9ed3d0cdeaea281ed1171b98505b266c04e2b25a023dec665197732'
OWNER_CLASS = '12809966af8256aa5c55e56b54d49f5be66e9785d6616ffa934c376f3d6d31bd'
AXES = ('identity','behavior','parameters','targeting','costs','integration','validation')
METHODS = {
 '<init>':(12,'1c59bef51bc767350a0f79f732eac8355d4c7b6c50b864e6b32197f3a1efabf2'),
 'getArmorTexture':(2,'4a16426bec92aef93114cd86a2be5cf59ae72252bde57b2fafc339f2daa20bf9'),
 'initializeClient':(6,'241b312ebd6ff1e8ab0719a7fcbfd71c956258d303ba94e3a602770053402fa8'),
 'onEntityLand':(134,'2005b5721f54d7100266965de674f8f5b22ab8a7c4d0c0936e784383dfe13ae8'),
}
STATES = {'status':'CERTIFIED_STATIC_7_AXES','claim_scope':'STATIC_TECHNICAL_CATALOG_ONLY',
 'mutation':'NO_MUTATION','mutating_hook':'NOT_VERIFIED','perk_certification':'NOT_CERTIFIED',
 'physical_qa':'NOT_TESTED','runtime_dispatch':'NOT_VERIFIED',
 'installed_transformed_runtime':'NOT_VERIFIED','provider_universe_closed':False}
PARAMS = {'resource_id':'alexscaves:rainbounce_boots','factory':'lambda$static$174',
 'native_class':OWNER,'equipment_slot':'FEET','armor_type':'BOOTS','enum_ordinal':3,
 'armor_nominal':2,'max_durability_configured':66,'enchantability':40,
 'toughness':0,'knockback_resistance':0,'repair_material_supplier':'Ingredient.EMPTY',
 'on_entity_land_instruction_count':134,'mixin_move_instruction_count':20,
 'base_min_abs_fall_exclusive':0.2,'strong_bounce_boundary_exclusive':0.42,
 'weak_bounce_multiplier':0.7,'strong_bounce_multiplier':1.05,
 'reduced_bounce_tag_factor':0.15000000596046448,
 'with_sugar_rush_horizontal':1.2,'without_sugar_rush_horizontal':1.9,
 'cloud_particles_requested_min':3,'cloud_particles_requested_max':5,
 'no_offensive_targeting':True,'magic_roots_delta':0,'evidence_axes':list(AXES)}


def require(test, msg):
    if not test: raise ValueError(msg)

def unique(pairs):
    out={}
    for k,v in pairs:
        require(k not in out,'duplicate JSON key: '+str(k));out[k]=v
    return out

def load(path, limit=4000000):
    raw=Path(path).read_bytes()
    require(0<len(raw)<=limit,'invalid source file size: '+str(path))
    return json.loads(raw,object_pairs_hook=unique),hashlib.sha256(raw).hexdigest()

def canonical(obj):
    return (json.dumps(obj,sort_keys=True,indent=2,ensure_ascii=False)+'\n').encode('utf8')

def digest(obj):
    return hashlib.sha256(canonical(obj)).hexdigest()

def mapped(arr):
    out={}
    for x in arr:
        n=x['declaration']['name'];require(n not in out,'duplicate method '+n);out[n]=x
    return out

def text(method):
    return ' '.join(x['opcode']+' '+x['operand']+' '+x['symbol'] for x in method['instructions'])

def contains(method, phrases):
    t=text(method)
    for s in phrases:require(s in t,method['declaration']['name']+' missing semantic pivot: '+s)

def verify_method(method,name,expected):
    size,sha=expected
    require(method['declaration']['name']==name,'method name drift')
    require(method['instruction_count']==size==len(method['instructions']),'method instruction count drift '+name)
    require(method['instruction_sha256']==digest(method['instructions'])==sha,'method body drift '+name)
    offs=[x['offset'] for x in method['instructions']]
    require(offs==sorted(set(offs)),'unordered/duplicated offsets '+name)

def validate(pub,off,mat,prior,cert,*,strict=True):
    if strict:
        require(digest(pub)==REPORT,'original publisher full report drift')
        require(digest(off)==OFFICIAL,'original official full report drift')
    require(prior['report']['sha256']==REPORT and prior['scope']=='RAINBOUNCE_BOOTS_NATIVE_DISCOVERY_NOT_CERTIFIED','old evidence seal')
    require(cert['schema']==1 and cert['scope']=='ALEXSCAVES_1010_RAINBOUNCE_BOOTS_INDIVIDUAL_STATIC_CONTRACT','cert manifest scope')
    require(cert['states']==STATES and cert['item']==PARAMS,'individual static contract: states/parameters')
    src=cert['sources']
    require(src['publisher_sha256']==PUBLISHER and src['publisher_report_sha256']==REPORT and src['publisher_discovery_seal']=='EXACT-RAINBOUNCE-BOOTS-DISCOVERY-1.0.10.json','publisher provenance')
    require(src['owner_class_sha256']==OWNER_CLASS and src['official_enum_report_sha256']==OFFICIAL and src['official_enum_class_sha256']==OFF_CLASS,'class/enum provenance')
    require(src['material_seal']=='EXACT-ARMOR-MATERIAL-1.0.10.json' and src['publisher_version']=='1.0.10' and src['publisher_sha1']=='6960b299a39a039ac8a5eb9b07be4ad0e3e0a570','artifact version')
    require(pub['artifact']['sha256']==PUBLISHER and pub['artifact']['size_bytes']==75279314 and pub['native']['class_entries_scanned']==1555,'publisher full artifact')
    require(pub['scope']=='RAINBOUNCE_BOOTS_NATIVE_DISCOVERY_NOT_CERTIFIED' and pub['static_contract']=='NOT_CERTIFIED' and pub['mutation']=='NO_MUTATION' and pub['physical_qa']=='NOT_TESTED','native discovery ceiling')
    require(set(pub['native']['targets'])=={OWNER},'publisher owner roster')
    own=pub['native']['targets'][OWNER]
    require(own['class_sha256']==OWNER_CLASS and len(own['fields'])==0 and len(own['declarations'])==4,'publisher class')
    methods=mapped(own['methods'])
    require(set(methods)==set(METHODS),'publisher owner methods')
    for k,v in METHODS.items():verify_method(methods[k],k,v)
    require(set(own['consumers'])=={MIXIN,REG,RENDER,OWNER},'typed consumer owner roster')
    cs=own['consumers']
    require(len(cs[MIXIN]['sites'])==1 and len(cs[MIXIN]['bodies'])==1,'movement consumer')
    require(len(cs[REG]['sites'])==2 and len(cs[REG]['bodies'])==1,'registry consumer')
    require(len(cs[RENDER]['sites'])==2 and len(cs[RENDER]['bodies'])==2,'render consumer')
    require(len(cs[OWNER]['sites'])==0,'self-reference excluded')
    move=mapped(cs[MIXIN]['bodies'])['ac_move']
    factory=mapped(cs[REG]['bodies'])['lambda$static$174']
    verify_method(move,'ac_move',(20,'4c47a6571a4ab6492d9275863923b16ff0c7996d58aa6149203f74239e2f772c'))
    verify_method(factory,'lambda$static$174',(6,'5a4f14aa8c35ae1004697b38488cad8c1e3d329bb4485af63bd452fec2b6f55a'))
    contains(move,('LivingEntity','EquipmentSlot.FEET','RAINBOUNCE_BOOTS','ItemStack.is','RainbounceBootsItem.onEntityLand'))
    contains(factory,('RAINBOUNCE_ARMOR_MATERIAL','ArmorItem$Type.BOOTS','RainbounceBootsItem'))
    effect=methods['onEntityLand']
    contains(effect,('Vec3.y','Math.abs','isSuppressingBounce','float 0.2f','double 0.42d',
                     'float 1.05f','float 0.7f','getOnPosLegacy','REDUCE_RAINBOUNCE_BOOTS_EFFECT_ON',
                     '0.15000000596046448d','SUGAR_RUSH','float 1.2f','float 1.9f',
                     'Vec3.multiply','Vec3.add','setDeltaMovement','fallDistance',
                     'RAINBOUNCE_BOOTS_BOUNCE','PLAYER_RAINBOW','ParticleTypes.CLOUD',
                     'RandomSource.nextInt','RandomSource.nextFloat','addParticle'))
    contains(methods['getArmorTexture'],('rainbounce_boots.png',))
    require(pub['filename_matched_resource_hashes']==prior['resources'] and len(prior['resources'])==5,'resources unchanged')
    enum=off['enum']
    require(off['schema']==1 and enum['class_sha256']==OFF_CLASS and enum['mapped_name']=='net.minecraft.world.item.ArmorItem$Type','official vanilla enum')
    sites=enum['value_construction_sites']
    require([v['name'] for v in sites]==['HELMET','CHESTPLATE','LEGGINGS','BOOTS','BODY'],'armor type enum order')
    require([v['numeric_operands_before_ctor'][0][1] for v in sites]==[0,1,2,3,4],'armor type enum numeric ordinals')
    require(enum['initializer_instruction_count']==51,'official enum initializer')
    defs=[x for x in mat['material_definitions'] if x['registry_field']=='RAINBOUNCE_ARMOR_MATERIAL']
    require(len(defs)==1,'specific material not unique')
    m=defs[0]
    for k,v in {'damage_reduction_by_ordinal':[2,2,1,2],'durability_multiplier':6,
                'enchantability':40,'toughness':0,'knockback_resistance':0,
                'setup_repair_item':'Ingredient.EMPTY','equip_sound_field':'ARMOR_EQUIP_GENERIC'}.items():
        require(m[k]==v,'material '+k)
    ar=mat['integration_bounds']['max_damage_array_by_ordinal']
    require(ar==[13,15,16,11] and m['damage_reduction_by_ordinal'][3]==PARAMS['armor_nominal'] and ar[3]*m['durability_multiplier']==PARAMS['max_durability_configured'],'BOOTS ordinal parameters')
    require(mat['claims']['static_technical_contract']=='CERTIFIED_STATIC_7_AXES' and mat['claims']['mutation']=='NO_MUTATION','separate material scope')
    return True

def adversarial(pub,off,mat,prior,cert):
    cases=[]
    def case(label,fn): cases.append((label,fn))
    for field,new in [('mutation','MUTATING'),('mutating_hook','VERIFIED'),('physical_qa','PASSED'),
                      ('perk_certification','CERTIFIED'),('installed_transformed_runtime','VERIFIED'),
                      ('runtime_dispatch','VERIFIED'),('provider_universe_closed',True),
                      ('status','PARTIAL'),('claim_scope','EXECUTABLE_GAMEPLAY')]:
        case('unsafe state '+field,lambda p,o,m,d,c,k=field,v=new:c['states'].__setitem__(k,v))
    for field,new in [('enum_ordinal',0),('armor_nominal',3),('max_durability_configured',78),
                      ('enchantability',50),('base_min_abs_fall_exclusive',0.1),
                      ('strong_bounce_boundary_exclusive',0.43),('strong_bounce_multiplier',1.2),
                      ('weak_bounce_multiplier',0.5),('reduced_bounce_tag_factor',1.0),
                      ('with_sugar_rush_horizontal',1.9),('without_sugar_rush_horizontal',1.2),
                      ('cloud_particles_requested_max',7),('equipment_slot','HEAD'),
                      ('no_offensive_targeting',False),('magic_roots_delta',1)]:
        case('wrong item '+field,lambda p,o,m,d,c,k=field,v=new:c['item'].__setitem__(k,v))
    case('spoof provider sha',lambda p,o,m,d,c:c['sources'].__setitem__('publisher_sha256','0'*64))
    case('spoof original report',lambda p,o,m,d,c:d['report'].__setitem__('sha256','0'*64))
    case('wrong official BOOTS ordinal',lambda p,o,m,d,c:o['enum']['value_construction_sites'][3]['numeric_operands_before_ctor'][0].__setitem__(1,0))
    case('wrong armor defense',lambda p,o,m,d,c:next(x for x in m['material_definitions'] if x['registry_field']=='RAINBOUNCE_ARMOR_MATERIAL')['damage_reduction_by_ordinal'].__setitem__(3,5))
    case('wrong armor multiplier',lambda p,o,m,d,c:next(x for x in m['material_definitions'] if x['registry_field']=='RAINBOUNCE_ARMOR_MATERIAL').__setitem__('durability_multiplier',9))
    def mutate_method(owner,meth,token):
        def change(p,o,m,d,c):
            source=p['native']['targets'][OWNER]
            method=mapped(source['methods'] if owner=='own' else source['consumers'][owner]['bodies'])[meth]
            ins=next(x for x in method['instructions'] if token in (x['symbol']+' '+x['operand']))
            ins['symbol']='SPOOFED.INSTRUCTION'
            method['instruction_sha256']=digest(method['instructions'])
        return change
    for owner,meth,token in [('own','onEntityLand','setDeltaMovement'),('own','onEntityLand','float 0.2f'),
                              ('own','onEntityLand','SUGAR_RUSH'),('own','onEntityLand','ParticleTypes.CLOUD'),
                              ('own','onEntityLand','float 1.05f'),(MIXIN,'ac_move','EquipmentSlot.FEET'),
                              (MIXIN,'ac_move','RainbounceBootsItem.onEntityLand'),(REG,'lambda$static$174','ArmorItem$Type.BOOTS')]:
        case('rehashed JVM pivot '+token,mutate_method(owner,meth,token))
    count=0
    for label,change in cases:
        p,o,m,d,c=copy.deepcopy((pub,off,mat,prior,cert))
        change(p,o,m,d,c)
        try:validate(p,o,m,d,c,strict=False)
        except (ValueError,KeyError,TypeError,IndexError,AssertionError,StopIteration):
            count+=1
        else:raise ValueError('false adversarial accept: '+label)
    require(count==len(cases) and count>=35,'adversarial coverage incomplete')
    return count

def validate_card_and_ledger(cardpath,ledgerpath):
    card=Path(cardpath).read_text(encoding='utf8')
    require('CERTIFIED_STATIC_7_AXES' in card and 'NO_MUTATION' in card and 'BOOTS=3' in card and '66' in card and 'EXACT-RAINBOUNCE-BOOTS-STATIC-1.0.10.md' in card,'card lacks distinct seven-axis seal')
    ledger,_=load(ledgerpath,3000000)
    k='✅-alexs-caves-continued/items/rainbounce-boots.md'
    cert=ledger['objects'].get(k)
    require(cert and cert['status']=='COMPLETE_PERK_READY' and cert['claim_scope']=='STATIC_TECHNICAL_CATALOG_ONLY' and cert['evidence_grade']=='SHA_EXACT_BINARY_BEHAVIOR','not in ledger')
    require(cert['mutating_hook']=='NOT_VERIFIED' and cert['physical_qa']=='NOT_TESTED' and cert['perk_certification']=='NOT_CERTIFIED' and cert['mutation']=='NO_MUTATION' and cert['provider_universe_closed']==False,'unsafe ledger promotion')
    require(set(cert['evidence'])==set(AXES),'seven axis fields')
    for key in AXES:
        ev=cert['evidence'][key]
        require(ev['path']=='wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-RAINBOUNCE-BOOTS-STATIC-1.0.10.md' and len(ev['reason'])>35,'missing evidence '+key)

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    for key in ('publisher','official','material','discovery','manifest'):
        ap.add_argument('--'+key,required=True,type=Path)
    ap.add_argument('--card',required=True,type=Path)
    ap.add_argument('--ledger',required=True,type=Path)
    ap.add_argument('--adversarial',action='store_true')
    a=ap.parse_args()
    original.check(a.publisher,a.discovery)
    pub,ph=load(a.publisher,4000000); off,oh=load(a.official,30000)
    mat,_=load(a.material,300000); prior,_=load(a.discovery,100000); cert,_=load(a.manifest,100000)
    require(ph==REPORT and oh==OFFICIAL,'raw source report hash mismatched')
    validate(pub,off,mat,prior,cert)
    validate_card_and_ledger(a.card,a.ledger)
    n=adversarial(pub,off,mat,prior,cert) if a.adversarial else 0
    print('PASS: Rainbounce one bounded static 7-axis contract; negative fixtures rejected:',n)
    print('LIMITS NO_MUTATION NOT_VERIFIED NOT_TESTED NOT_CERTIFIED no new casts, no physical QA')

if __name__=='__main__':main()
