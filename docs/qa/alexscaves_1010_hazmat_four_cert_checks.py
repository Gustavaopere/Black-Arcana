#!/usr/bin/env python3
"""SHA-exact read-only static certification: four Hazmat armor instances.

The publisher class, its finite typed consumers, native material and original
Mojang 1.21.1 enum are independent evidence. This never executes Minecraft,
asserts runtime mitigation, claims an installed JAR, or verifies any hook.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
from pathlib import Path

OWNER='com/github/alexmodguy/alexscaves/server/item/HazmatArmorItem'
REG='com/github/alexmodguy/alexscaves/server/item/ACItemRegistry'
SRC='3ef6aeeeb37e0768e206b0777d7193a5ac55a0732ff06d568573c3edf923a033'
OFFICIAL='e83bef57b5efb722a17fefb237edb7288b1668d99d7dae67e51c1905c174ff91'
PUBLISHER='36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c'
OWNER_SHA='289395b93a1a223f2e66a02528ccb4ce3a1a659dd9c82ac071a5b63c32b1c7cb'
NAMES=('HELMET','CHESTPLATE','LEGGINGS','BOOTS')
SLOTS=('HEAD','CHEST','LEGS','FEET')
ITEMS=('hazmat_mask','hazmat_chestplate','hazmat_leggings','hazmat_boots')
ACTIONS=('identity','behavior','parameters','targeting','costs','integration','validation')


def require(ok,msg):
    if not ok: raise ValueError(msg)

def canonical(value):
    return json.dumps(value,indent=2,sort_keys=True,ensure_ascii=False)+'\n'

def sha(data):return hashlib.sha256(data).hexdigest()

def unique(pairs):
    o={}
    for k,v in pairs:
        require(k not in o,'duplicate JSON key '+k);o[k]=v
    return o

def read(path,maxbytes=18_000_000):
    data=Path(path).read_bytes()
    require(0<len(data)<=maxbytes,'missing or excessive evidence')
    return data,json.loads(data,object_pairs_hook=unique)

def method_map(owner):
    out={}
    for m in owner['methods']:
        key=(m['declaration']['name'],m['declaration']['descriptor'])
        require(key not in out,'duplicated method identity')
        out[key]=m
    return out

def expect(m,off,op,token=''):
    r=next((r for r in m['instructions'] if r['offset']==off),None)
    require(r is not None and r['opcode']==op and token in (r['symbol']+' '+r['operand']),
            'JVM pivot drift: '+m['declaration']['name']+' @'+str(off)+' '+op+' '+token)

def check(official,publisher,material,old,seal,*,strict=True):
    if strict:
        require(sha(canonical(official).encode())==OFFICIAL,'official report exact SHA')
        require(sha(canonical(publisher).encode())==SRC,'publisher report exact SHA')
    require(seal['schema_version']==1 and seal['scope']=='ALEXSCAVES_1010_HAZMAT_FOUR_INDIVIDUAL_STATIC_CONTRACTS','manifest scope')
    require(seal['limits']=={'claim_scope':'STATIC_TECHNICAL_CATALOG_ONLY',
      'status':'CERTIFIED_STATIC_7_AXES','mutating_hook':'NOT_VERIFIED','physical_qa':'NOT_TESTED',
      'perk_certification':'NOT_CERTIFIED','runtime_dispatch':'NOT_VERIFIED','transformed_engine':'NOT_VERIFIED',
      'installed_dump_comparison':'NOT_VERIFIED','provider_universe_closed':False,
      'other_radiation_sources_complete':False,'effects_accepted_in_world':'NOT_VERIFIED',
      'mutation':'NO_MUTATION','new_spell_roots':0},'scope/claim boundary')
    sources=seal['sources']
    require(sources['official_report_sha256']==OFFICIAL and sources['publisher_report_sha256']==SRC,'report pins')
    require(sources['official_version_sha1']=='ff7ef54488da4a711f3c8a781a9f79105bbe801a','version pin')
    require(sources['official_enum_class_sha256']=='304d6345c9ed3d0cdeaea281ed1171b98505b266c04e2b25a023dec665197732','enum class seal')
    require(sources['official_client_sha256']=='499f6897d1837516680f3114072d8106e11c9adcd933fe5cf051b551089b0c99','client pin')
    require(sources['official_mappings_sha256']=='140c47931cccc8fc9e4c22d7603e2d714d1a953a146f51ea7397d95c955536ec','mapping pin')
    require(sources['publisher_sha256']==PUBLISHER and sources['native_class_sha256']==OWNER_SHA,'publisher hash/owner pin')
    require(official['scope']=='MINECRAFT_1211_ARMOR_ITEM_TYPE_OFFICIAL_CLIENT_BINARY_DISCOVERY_NOT_INSTALLED_RUNTIME','official scope')
    enum=official['enum']; require(enum['mapped_name']=='net.minecraft.world.item.ArmorItem$Type','class mapping')
    require(enum['class_sha256']==sources['official_enum_class_sha256'] and enum['major']==65,'enum class bytes')
    require(enum['initializer_instruction_count']==51 and len(enum['full_initializer'])==51,'enum full code')
    require(sha(canonical(enum['full_initializer']).encode())==enum['initializer_instruction_sha256']=='eba773c06e909e66e48c6aab76af27288097828da5b8a82c9b538e2d5d4af024','enum code SHA')
    sites=enum['value_construction_sites']
    require([x['name'] for x in sites]==[*NAMES,'BODY'],'five actual values')
    require([x['numeric_operands_before_ctor'][0] for x in sites]==[[6,0],[26,1],[46,2],[66,3],[86,4]],'true enum ordinal offsets')
    require([x['assignment']['offset'] for x in sites]==[17,37,57,77,97],'enum assigned slots')
    require(official['artifacts']['client']['sha256']==sources['official_client_sha256'] and official['artifacts']['client_mappings']['sha256']==sources['official_mappings_sha256'] and official['metadata']['version_sha1']==sources['official_version_sha1'],'actual official artifact identity')
    require(sources['minecraft_version']=='1.21.1' and sources['publisher_version']=='1.0.10','versions')
    require(publisher['scope']=='HAZMAT_ARMOR_NATIVE_DISCOVERY_NOT_CERTIFIED' and publisher['artifact']['sha256']==PUBLISHER
            and publisher['artifact']['sha1']=='6960b299a39a039ac8a5eb9b07be4ad0e3e0a570'
            and publisher['artifact']['size_bytes']==75279314,'exact 1.0.10')
    require(publisher['native']['class_entries_scanned']==1555 and publisher['owner']==OWNER,'publisher census')
    require(publisher['source_revision_parity']=='NOT_ASSUMED' and publisher['static_contract']=='NOT_CERTIFIED'
      and publisher['mutation']=='NO_MUTATION' and publisher['physical_qa']=='NOT_TESTED'
      and publisher['provider_universe_closed'] is False
      and publisher['other_radiation_consumers_complete'] is False,'original discovery limits')
    require(old['scope']==publisher['scope'] and old['report']['sha256']==SRC
      and old['native_class']['sha256']==OWNER_SHA and old['limits']['status']=='PARTIAL','historical evidence')
    require(material['artifact']['sha256']==PUBLISHER and material['claims']['static_technical_contract']=='CERTIFIED_STATIC_7_AXES','material artifact')
    require(material['integration_bounds']['max_damage_array_by_ordinal']==[13,15,16,11],'base durability array')
    mat=[x for x in material['material_definitions'] if x['registry_field']=='HAZMAT_SUIT_ARMOR_MATERIAL']
    require(len(mat)==1,'one exact material');mat=mat[0]
    for k,v in {'name':'hazmat_suit','damage_reduction_by_ordinal':[2,4,5,2],
                'durability_multiplier':20,'enchantability':25,
                'toughness':0.5,'knockback_resistance':0,'setup_repair_item':'POLYMER_PLATE'}.items():
        require(mat[k]==v,'material '+k)
    native=publisher['native']['targets'];require(set(native)=={OWNER},'one native target')
    obj=native[OWNER]
    require(obj['class_sha256']==OWNER_SHA and len(obj['declarations'])==len(obj['methods'])==6
            and len(obj['fields'])==0 and len(obj['consumers'])==7 and len(obj['in_jar_ancestors'])==0,'native surface')
    mmap=method_map(obj);require(len(mmap)==6,'unique native methods')
    check_methods=seal['shared_contract']['owner_methods']
    require(set(k for k,_ in mmap)==set(check_methods),'full Code roster')
    for (name,descriptor),m in mmap.items():
        spec=check_methods[name]
        require(spec=={'descriptor':descriptor,'count':len(m['instructions']),'sha256':m['instruction_sha256']},'owner code identity '+name)
        require(sha(canonical(m['instructions']).encode())==m['instruction_sha256'],'re-sealed native code '+name)
        require(next(x for x in old['native_class']['methods'] if x['name']==name)['instruction_sha256']==m['instruction_sha256'],'old method seal '+name)
    m={key[0]:v for key,v in mmap.items()}
    expect(m['<init>'],2,'invokevirtual','ACArmorMaterial.vanilla');expect(m['<init>'],15,'invokevirtual','ACArmorMaterial.properties')
    expect(m['acInventoryTick'],1,'instanceof','Player');expect(m['acInventoryTick'],16,'invokestatic','ACCompat.isWornArmor');expect(m['acInventoryTick'],27,'invokevirtual','acArmorTick')
    expect(m['acArmorTick'],1,'getstatic','HAZMAT_MASK');expect(m['acArmorTick'],27,'invokestatic','Math.cos')
    expect(m['getArmorTexture'],1,'getstatic','EquipmentSlot.LEGS');expect(m['getArmorTexture'],7,'ldc','hazmat_suit_1.png');expect(m['getArmorTexture'],10,'ldc','hazmat_suit_0.png')
    require(len(m['getWornAmount']['instructions'])==40,'wear count method length')
    for idx,(slot,key) in enumerate(zip(SLOTS,('HAZMAT_MASK','HAZMAT_CHESTPLATE','HAZMAT_LEGGINGS','HAZMAT_BOOTS'))):
        off=(3,30,57,84)[idx];base=(9,36,63,90)[idx];inc=(26,53,80,107)[idx]
        expect(m['getWornAmount'],off,'getstatic','EquipmentSlot.'+slot)
        expect(m['getWornAmount'],base,'getstatic',key)
        expect(m['getWornAmount'],inc,'iinc','1, 1')
    expect(m['getWornAmount'],111,'ireturn')
    all_consumers=obj['consumers'];sealc=seal['shared_contract']['typed_consumers']
    require(set(all_consumers)==set(sealc) and set(all_consumers)==set(old['consumer_methods']),'typed consumer exact roster')
    for class_name,v in all_consumers.items():
        require(len(v['sites'])==sealc[class_name]['sites']==old['consumer_methods'][class_name]['sites'],'consumer sites '+class_name)
        bodies={x['declaration']['name']:x for x in v['bodies']}
        require(set(bodies)==set(sealc[class_name]['methods']),'consumer methods '+class_name)
        for name,body in bodies.items():
            spec=sealc[class_name]['methods'][name]
            require(spec=={'descriptor':body['declaration']['descriptor'],'count':len(body['instructions']),'sha256':body['instruction_sha256']},'consumer fingerprint '+name)
            require(sha(canonical(body['instructions']).encode())==body['instruction_sha256'],'consumer instructions '+class_name+'/'+name)
    registry={m['declaration']['name']:m for m in all_consumers[REG]['bodies']}
    require(set(registry)=={'lambda$static$69','lambda$static$70','lambda$static$71','lambda$static$72'},'four factories')
    common=seal['shared_contract']
    require(common['armor_material_defense_indexed']==[2,4,5,2]
            and common['armor_material_durability_indexed']==[260,300,320,220]
            and common['counting_slots']==list(SLOTS)
            and common['count_min_max']==[0,4]
            and common['radiation_status_duration_ticks_requested']==1800
            and common['irradiated_exhaustion_on_no_piece']==0.4
            and common['irradiated_damage_probability_offset']==0.1
            and common['acid_block_min_height_strict']==0.1
            and common['acid_other_armor_damage_probability']==0.05
            and common['acid_extra_weak_to_acid']==10
            and common['hazmat_armor_durability_not_debited_in_owner_methods'] is True
            and common['no_independent_cast_projectile_world_mutation'] is True,'shared numbers/limits')
    radioactive_names=('com/github/alexmodguy/alexscaves/server/item/RadioactiveItem',
                       'com/github/alexmodguy/alexscaves/server/item/RadioactiveBlockItem')
    for name in radioactive_names:
        r=all_consumers[name]['bodies'][0]
        expect(r,1,'invokevirtual','Level.isClientSide')
        expect(r,58,'invokestatic','getWornAmount')
        expect(r,62,'ldc','float 4.0f')
        expect(r,64,'fdiv');expect(r,65,'fsub')
        expect(r,84,'invokevirtual','LivingEntity.hasEffect')
        expect(r,94,'invokeinterface','RandomSource.nextFloat')
        expect(r,126,'sipush','1800')
        expect(r,138,'invokevirtual','LivingEntity.addEffect')
    irr=all_consumers['com/github/alexmodguy/alexscaves/server/potion/IrradiatedEffect']['bodies'][0]
    for off,op,term in [(1,'invokestatic','getWornAmount'),(8,'ldc','float 0.25f'),(10,'fmul',''),(11,'fsub',''),
                        (33,'ldc','float 0.4f'),(35,'invokevirtual','causeFoodExhaustion'),
                        (59,'ldc','float 0.1f'),(61,'fadd',''),(74,'invokestatic','causeRadiationDamage'),
                        (79,'invokevirtual','LivingEntity.hurt')]:expect(irr,off,op,term)
    acid=all_consumers['com/github/alexmodguy/alexscaves/server/block/AcidBlock']['bodies'][0]
    for off,op,term in [(8,'getstatic','RESISTS_ACID'),(22,'ldc2_w','double 0.1d'),
                        (53,'invokestatic','EquipmentSlot.values'),(104,'invokevirtual','isDamageableItem'),
                        (170,'invokestatic','hurtAndBreak'),(182,'invokestatic','getWornAmount'),
                        (186,'ldc','float 4.0f'),(188,'fdiv',''),(189,'fsub',''),
                        (209,'invokeinterface','RandomSource.nextFloat'),(217,'ifge','278'),
                        (228,'getstatic','WEAK_TO_ACID'),(237,'ldc','float 10.0f'),
                        (261,'ldc2_w','double 0.01d'),(273,'invokestatic','ACCompat.hurt')]:expect(acid,off,op,term)
    expect(m['acArmorTick'],1,'getstatic','HAZMAT_MASK')
    # Mask tick emits particles; it does not confer an intrinsic armor item spell.
    require(any('HAZMAT_BREATHE' in x['symbol'] for x in m['acArmorTick']['instructions']),'breathe particle reference')
    specs={
        'hazmat_mask':('HELMET','HEAD',0,2,260,69,26),
        'hazmat_chestplate':('CHESTPLATE','CHEST',1,4,300,70,53),
        'hazmat_leggings':('LEGGINGS','LEGS',2,5,320,71,80),
        'hazmat_boots':('BOOTS','FEET',3,2,220,72,107)
    }
    require(set(seal['objects'])==set(specs),'exactly four item contracts')
    for name,(typ,slot,idx,defense,max_damage,factory,inc) in specs.items():
        item=seal['objects'][name]
        exact={'resource_id':'alexscaves:'+name,'item_card':'items/'+name.replace('_','-')+'.md',
               'enum_constant':typ,'enum_ordinal':idx,'equipment_slot':slot,
               'armor_defense_by_material':defense,'configured_max_durability':max_damage,
               'enchantability':25,'toughness':0.5,'knockback_resistance':0,
               'factory_method':'lambda$static$'+str(factory),'factory_instruction_sha256':registry['lambda$static$'+str(factory)]['instruction_sha256'],
               'get_worn_amount_iinc_offset':inc,'contribution_to_hazmat_count':1,
               'environmental_factor_formula':'f=1.0F-(float)piece_count/4.0F',
               'radioactive_item_gate':'stackCount*randomChanceOfRadiation*f, no already Irradiated, noncreative, server, random < threshold',
               'irradiated_gate':'random < f+0.1F; hurt requested with amount f, zero when four pieces',
               'acid_gate':'acidHeight>0.1D, !RESISTS_ACID, random < f before acid damage branch; other armor break path separate',
               'armor_texture':'alexscaves:textures/armor/hazmat_suit_'+('1' if slot=='LEGS' else '0')+'.png',
               'model_sha256':old['resources']['models'][name],
               'recipe_sha256':old['resources']['recipes'][name],
               'repair_material':'alexscaves:polymer_plate',
               'axes':list(ACTIONS)}
        require(item==exact,'per item seven axes/params '+name)
        f=registry[item['factory_method']]
        expect(f,0,'new','HazmatArmorItem')
        expect(f,4,'getstatic','HAZMAT_SUIT_ARMOR_MATERIAL')
        expect(f,7,'getstatic','ArmorItem$Type.'+typ)
        expect(f,10,'invokespecial','HazmatArmorItem')
        require(idx==sites[idx]['numeric_operands_before_ctor'][0][1],'enum type mismatch '+name)
        require(13*20==260 and 15*20==300 and 16*20==320 and 11*20==220,'durability basis')
        raw_resources=publisher['filename_matched_resource_hashes']
        require(raw_resources['assets/alexscaves/models/item/'+name+'.json']['sha256']==item['model_sha256'],'model '+name)
        require(raw_resources['data/alexscaves/recipe/'+name+'.json']['sha256']==item['recipe_sha256'],'recipe '+name)
        require(raw_resources['data/alexscaves/tags/item/repairs_hazmat_suit_armor.json']['sha256']==old['resources']['tag']['data/alexscaves/tags/item/repairs_hazmat_suit_armor.json'],'repair tag')
    require('BODY' not in [i['enum_constant'] for i in seal['objects'].values()],'unsupported fifth slot')


def adverse(official,publisher,material,old,seal):
    """30 in-memory mutations plus four nested-digest-resealed JVM adversaries."""
    failures=[]
    def attempt(label,which,mut):
        args=[copy.deepcopy(x) for x in (official,publisher,material,old,seal)]
        mut(args[which]);
        try:check(*args,strict=False)
        except (ValueError,KeyError,TypeError,AssertionError):failures.append(label)
        else:raise AssertionError('FAIL-OPEN synthetic '+label)
    attempt('enum swap',0,lambda x:x['enum']['value_construction_sites'][0].update(name='BOOTS'))
    attempt('enum ordinal shifted',0,lambda x:x['enum']['value_construction_sites'][3]['numeric_operands_before_ctor'][0].__setitem__(1,4))
    attempt('client class version',0,lambda x:x['enum'].update(major=64))
    attempt('official class SHA',0,lambda x:x['enum'].update(class_sha256='0'*64))
    attempt('client mapping hash',0,lambda x:x['artifacts']['client_mappings'].update(sha256='0'*64))
    attempt('publisher class',1,lambda x:x['native']['targets'][OWNER].update(class_sha256='0'*64))
    attempt('installed claim',1,lambda x:x.update(static_contract='CERTIFIED'))
    attempt('namespace alternate owner',1,lambda x:x.update(owner='other/HazmatArmorItem'))
    attempt('missing radiation',1,lambda x:x['native']['targets'][OWNER]['consumers'].pop('com/github/alexmodguy/alexscaves/server/item/RadioactiveItem'))
    attempt('missing native method',1,lambda x:x['native']['targets'][OWNER]['methods'].pop())
    attempt('additional registry factory',1,lambda x:x['native']['targets'][OWNER]['consumers'][REG]['sites'].append({'fake':1}))
    attempt('false init ordinal',1,lambda x:next(m for m in x['native']['targets'][OWNER]['consumers'][REG]['bodies'] if m['declaration']['name']=='lambda$static$69')['instructions'][3].update(symbol='BOOTS'))
    attempt('worn count altered',1,lambda x:next(m for m in x['native']['targets'][OWNER]['methods'] if m['declaration']['name']=='getWornAmount')['instructions'][12].update(opcode='return'))
    attempt('rad effect 1800 gone',1,lambda x:x['native']['targets'][OWNER]['consumers']['com/github/alexmodguy/alexscaves/server/item/RadioactiveItem']['bodies'][0]['instructions'].__setitem__(55,{'offset':126,'opcode':'sipush','operand':'600','symbol':''}))
    attempt('acid branch disappeared',1,lambda x:x['native']['targets'][OWNER]['consumers']['com/github/alexmodguy/alexscaves/server/block/AcidBlock']['bodies'][0]['instructions'][100].update(opcode='return'))
    attempt('material defense',2,lambda x:next(v for v in x['material_definitions'] if v['registry_field']=='HAZMAT_SUIT_ARMOR_MATERIAL')['damage_reduction_by_ordinal'].__setitem__(0,5))
    attempt('material multiplier',2,lambda x:next(v for v in x['material_definitions'] if v['registry_field']=='HAZMAT_SUIT_ARMOR_MATERIAL').update(durability_multiplier=12))
    attempt('old discovery certificate inflation',3,lambda x:x['limits'].update(status='CERTIFIED'))
    attempt('old discovery resource hash',3,lambda x:x['resources']['models'].update(hazmat_mask='0'*64))
    attempt('manifest four to three',4,lambda x:x['objects'].pop('hazmat_boots'))
    attempt('manifest enum order',4,lambda x:x['objects']['hazmat_mask'].update(enum_ordinal=3))
    attempt('manifest defense',4,lambda x:x['objects']['hazmat_chestplate'].update(armor_defense_by_material=2))
    attempt('manifest duration',4,lambda x:x['shared_contract'].update(radiation_status_duration_ticks_requested=300))
    attempt('manifest acid strength',4,lambda x:x['shared_contract'].update(acid_extra_weak_to_acid=3))
    attempt('manifest per tick perk',4,lambda x:x['limits'].update(mutating_hook='VERIFIED'))
    attempt('manifest physical QA',4,lambda x:x['limits'].update(physical_qa='PASSED'))
    attempt('manifest alternate factory',4,lambda x:x['objects']['hazmat_boots'].update(factory_method='lambda$static$70'))
    attempt('manifest missing targeting axis',4,lambda x:x['objects']['hazmat_leggings']['axes'].remove('targeting'))
    attempt('manifest recipe hash',4,lambda x:x['objects']['hazmat_mask'].update(recipe_sha256='0'*64))
    attempt('manifest wrong source hash',4,lambda x:x['sources'].update(publisher_report_sha256='0'*64))
    def resealed_method(label,owner,name,offset,field,value):
        args=[copy.deepcopy(x) for x in (official,publisher,material,old,seal)]
        own=args[1]['native']['targets'][OWNER]
        if owner==OWNER:
            meth=next(x for x in own['methods'] if x['declaration']['name']==name)
        else:
            meth=next(x for x in own['consumers'][owner]['bodies'] if x['declaration']['name']==name)
        row=next(x for x in meth['instructions'] if x['offset']==offset)
        row[field]=value
        new_sha=sha(canonical(meth['instructions']).encode())
        meth['instruction_sha256']=new_sha
        if owner==OWNER:
            args[4]['shared_contract']['owner_methods'][name]['sha256']=new_sha
            next(x for x in args[3]['native_class']['methods'] if x['name']==name)['instruction_sha256']=new_sha
        else:
            args[4]['shared_contract']['typed_consumers'][owner]['methods'][name]['sha256']=new_sha
        try:check(*args,strict=False)
        except (ValueError,KeyError,TypeError,AssertionError):failures.append(label)
        else:raise AssertionError('FAIL-OPEN re-sealed method '+label)
    resealed_method('resealed worn-mask alias',OWNER,'getWornAmount',9,'symbol','Field ACItemRegistry.HAZMAT_BOOTS:Ljava/util/function/Supplier;')
    resealed_method('resealed HELMET factory to BOOTS',REG,'lambda$static$69',7,'symbol','Field net/minecraft/world/item/ArmorItem$Type.BOOTS:Lnet/minecraft/world/item/ArmorItem$Type;')
    resealed_method('resealed radiation duration 60',
        'com/github/alexmodguy/alexscaves/server/item/RadioactiveItem','acInventoryTick',126,'operand','60')
    resealed_method('resealed acid comparator reversal',
        'com/github/alexmodguy/alexscaves/server/block/AcidBlock','entityInside',217,'opcode','iflt')
    require(len(failures)==34,'adversarial count')
    print('PASS',len(failures),'in-memory adversarial alterations rejected (including four nested-digest reseals)')


def main():
    p=argparse.ArgumentParser()
    for key in ('official','publisher','material','discovery','manifest'):
        p.add_argument('--'+key,required=True,type=Path)
    p.add_argument('--cards-root',type=Path)
    p.add_argument('--adversarial',action='store_true')
    a=p.parse_args()
    raw=[];data=[]
    for k in ('official','publisher','material','discovery','manifest'):
        b,o=read(getattr(a,k));raw.append(b);data.append(o)
    require(sha(raw[0])==OFFICIAL and sha(raw[1])==SRC,'exact source reports (raw SHA)')
    check(*data)
    if a.cards_root:
        for name,item in data[4]['objects'].items():
            text=(a.cards_root/Path(item['item_card']).name.replace('_','-')).read_text(encoding='utf8')
            for token in ('CERTIFIED_STATIC_7_AXES',item['resource_id'],str(item['configured_max_durability']),str(item['armor_defense_by_material']),item['factory_method'],
                          'NO_MUTATION','NOT_VERIFIED','NOT_TESTED','EXACT-HAZMAT-ARMOR-FOUR-PIECES-1.0.10.md'):
                require(token in text,'missing evidence in '+name+': '+token)
    if a.adversarial: adverse(*data)
    print('PASS four individually scoped Hazmat static contracts; 6 owner methods, 7 typed consumer owners, exact official enum; NO_MUTATION')

if __name__=='__main__':main()
