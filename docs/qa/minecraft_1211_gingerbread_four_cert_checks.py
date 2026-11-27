#!/usr/bin/env python3
"""Fail-closed *static* Gingerbread four-piece ABI composition.

Checks exactly two independently downloaded release artifacts and two earlier
SHA-exact publisher seals. No Minecraft execution, mutable hook, QA, or perks.
Mutations below modify in-memory evidence only and re-seal nested digests.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
from pathlib import Path
import minecraft_1211_armor_type_enum_probe as upstream

ORIGINAL_PUBLISHER_REPORT = '4b6a0709a167e49ffb4bd04b2949facfc3c7b0e55dad80c28842eaf26f1fbae1'
STABLE_OFFICIAL_REPORT = 'e83bef57b5efb722a17fefb237edb7288b1668d99d7dae67e51c1905c174ff91'
CLIENT_SHA256 = '499f6897d1837516680f3114072d8106e11c9adcd933fe5cf051b551089b0c99'
MAPPING_SHA256 = '140c47931cccc8fc9e4c22d7603e2d714d1a953a146f51ea7397d95c955536ec'
VERSION_SHA1 = 'ff7ef54488da4a711f3c8a781a9f79105bbe801a'
ENUM_SHA = '304d6345c9ed3d0cdeaea281ed1171b98505b266c04e2b25a023dec665197732'
ENUM_INS_SHA = 'eba773c06e909e66e48c6aab76af27288097828da5b8a82c9b538e2d5d4af024'
PUBLISHER_SHA = '36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c'
OWNER_SHA = '918cc76cd122605e6ba7aa2e8d26e1f4891b3ad8f26554b960e9b07412884a27'
OWNER = 'com/github/alexmodguy/alexscaves/server/item/GingerbreadArmorItem'
REGISTRY='com/github/alexmodguy/alexscaves/server/item/ACItemRegistry'
METHOD_INS = {
 '<clinit>':('()V',24,'e45a52e9e1256285550e099e31591b090f17d04e0eb47437ae45cdddc79e4fe4'),
 '<init>':('(Lcom/github/alexmodguy/alexscaves/server/item/ACArmorMaterial;Lnet/minecraft/world/item/ArmorItem$Type;)V',62,'3e819e82db652e0b8e629e0c6339590acd84e7eecbeb50333c23586d6e271fce'),
 'acModifiers':('(Lnet/minecraft/world/entity/EquipmentSlot;Lnet/minecraft/world/item/ItemStack;)Lcom/google/common/collect/Multimap;',14,'30cf36d0881c6b8d1c8b03ed1e1d48c35fc91dbe1515cc3639d8c1f57caf17e8'),
 'getArmorTexture':('(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/entity/Entity;Lnet/minecraft/world/entity/EquipmentSlot;Ljava/lang/String;)Ljava/lang/String;',7,'8fe9946fdd40f9b3e888274666495dab8ed7ddac0e3c2c568a8071d0c6393582'),
 'getDefaultAttributeModifiers':('(Lnet/minecraft/world/item/ItemStack;)Lnet/minecraft/world/item/component/ItemAttributeModifiers;',8,'0c89455ac0c9b95fe2a5876a8080cb1d84b19fbadee026e5a3007e038fa87948'),
 'getOrCreateDurabilityAttributes':('(II)Lcom/google/common/collect/Multimap;',73,'9950c3ffe19bdaddeb9b3d2dc4aecdc2b7fad8f0d81f42fa1de1cde7c3fa0881'),
 'initializeClient':('(Ljava/util/function/Consumer;)V',6,'1bbd25dc9fd7e396c606c055345c31e2833ddec3b66253cfc9b01bee53b8ed68'),
 'lambda$getDefaultAttributeModifiers$0':('(Lnet/minecraft/world/item/ItemStack;)Lnet/minecraft/world/item/component/ItemAttributeModifiers;',4,'ed920d60e03a8ae500dbd48d1a60a99bba0767b147870273456892cc87950715'),
}
NAMES=('HELMET','CHESTPLATE','LEGGINGS','BOOTS')
FIELDS={
 'HELMET':('helmet',187,0,2,130,'50a572c0b4cd7c407c678cd6ca77a5b4cfd8195505361488bda17806c7939c6c','gingerbread_armor_0.png'),
 'CHESTPLATE':('chestplate',188,1,4,150,'247f4e8d13124dfb2aa7367bd5e08f45dff4f1b38e01cbbe6cf0d0acc045acf9','gingerbread_armor_0.png'),
 'LEGGINGS':('leggings',189,2,5,160,'d11d46139dede72f1e4b3a75bd3167990bba74a1389ac40aacddbd3b09bedbf2','gingerbread_armor_1.png'),
 'BOOTS':('boots',190,3,2,110,'3301ab3fca58f36d665b035b362bf06943312fa4087f0e5aad6348b6820cd21b','gingerbread_armor_0.png')
}
UUID_BY_SLOT = {
 'HELMET':'845DB27C-C624-495F-8C9F-6020A9A58B77',
 'CHESTPLATE':'D8499B04-0E66-4726-AB29-64469D734E12',
 'LEGGINGS':'9F3D476D-C118-4544-8365-64846904B43F',
 'BOOTS':'2AD3F246-FEE1-4E67-B886-69FD380BB111',
}
POLICY={'scope':'STATIC_TECHNICAL_CATALOG_ONLY','status':'CERTIFIED_STATIC_7_AXES',
        'mutation':'NO_MUTATION','mutating_hook':'NOT_VERIFIED',
        'physical_qa':'NOT_TESTED','perk_certification':'NOT_CERTIFIED',
        'installed_transformed_runtime':'NOT_VERIFIED',
        'provider_universe_closed':False,'new_spell_roots':0}


def check(cond,msg):
    if not cond:raise ValueError(msg)


def digest(raw):return hashlib.sha256(raw).hexdigest()


def uniques(pairs):
    d={}
    for k,v in pairs:
        check(k not in d,'duplicate JSON key '+str(k))
        d[k]=v
    return d


def load(path,cap):
    raw=Path(path).read_bytes()
    check(0<len(raw)<=cap,'oversize/empty input '+str(path))
    return raw,json.loads(raw,object_pairs_hook=uniques)


def canonical(obj):return upstream.canonical(obj)


def site_by_name(method):
    return {x['offset']:x for x in method['instructions']}


def expect(method,off,op,token=''):
    rows=site_by_name(method);entry=rows.get(off)
    check(entry is not None and entry['opcode']==op and token in entry['symbol']+entry['operand'],
          f'JVM pivot drift: {method["declaration"]["name"]} @{off} {op} {token}')


def assert_context(official,publisher,material,discovery,seal,*,strict=True):
    check(seal['schema']==1 and seal['scope']=='ALEXSCAVES_1010_GINGERBREAD_FOUR_INDIVIDUAL_STATIC_CONTRACTS', 'seal scope')
    check(seal['states']==POLICY,'state/claims must remain bounded')
    if strict:
        # Strong immutable pin; mutated, externally re-sealed report changes still fail.
        check(digest(canonical(official).encode())==STABLE_OFFICIAL_REPORT,'official complete report drift')
        check(digest(canonical(publisher).encode())==ORIGINAL_PUBLISHER_REPORT,'publisher complete report drift')
    off=official['enum']
    check(official['scope']=='MINECRAFT_1211_ARMOR_ITEM_TYPE_OFFICIAL_CLIENT_BINARY_DISCOVERY_NOT_INSTALLED_RUNTIME', 'official scope')
    check(official['metadata']['version_sha1']==VERSION_SHA1 and official['metadata']['version_json_sha256']=='ab07658fe972925ed0036e383a09e3b4ca6b3f4ee07634233c02a5a1d49a39c9','mojang version metadata')
    check(official['artifacts']['client']['sha256']==CLIENT_SHA256 and official['artifacts']['client_mappings']['sha256']==MAPPING_SHA256,'Mojang source byte identity')
    check(official['artifacts']['client']['sha1']=='30c73b1c5da787909b2f73340419fdf13b9def88' and official['artifacts']['client_mappings']['sha1']=='2244b6f072256667bcd9a73df124d6c58de77992', 'Mojang SHA1 mismatch')
    check(off['mapped_name']==upstream.CLASS and off['binary_name']=='csf$a' and off['major']==65 and off['class_sha256']==ENUM_SHA,'enum class drift')
    rows=off['full_initializer']
    check(len(rows)==off['initializer_instruction_count']==51 and
          off['initializer_instruction_sha256']==ENUM_INS_SHA and digest(canonical(rows).encode())==ENUM_INS_SHA,
          'enum full initializer body drift')
    sites=json.loads(json.dumps(upstream.inspect_rows(rows)))
    check(sites==off['value_construction_sites'],'enum creation site projection drift')
    check([x['name'] for x in sites]==[*NAMES,'BODY'],'enum roster/ordering drift')
    check([x['numeric_operands_before_ctor'][0][1] for x in sites]==[0,1,2,3,4], 'enum ordinal operand drift')
    check([x['numeric_operands_before_ctor'][0][0] for x in sites]==[6,26,46,66,86],'enum ordinal offsets drift')
    check([x['assignment']['offset'] for x in sites]==[17,37,57,77,97],'enum destination offsets drift')
    check(all(x['constructor']['opcode']=='invokespecial' and '(Ljava/lang/String;ILbsy;ILjava/lang/String;)V' in x['constructor']['operand']
              and x['assignment']['opcode']=='putstatic' and 'Lcsf$a;' in x['assignment']['operand'] for x in sites),'enum constructor identity drift')
    check(official['limits']['mutation']=='NO_MUTATION' and official['limits']['individual_gingerbread_certification']=='NOT_CERTIFIED','scope ceiling in source discovery')
    check(seal['sources']['official_report_sha256']==STABLE_OFFICIAL_REPORT and seal['sources']['publisher_report_sha256']==ORIGINAL_PUBLISHER_REPORT,'source report pins drift')

    check(publisher['scope']=='GINGERBREAD_ARMOR_NATIVE_DISCOVERY_NOT_CERTIFIED' and publisher['artifact']['sha256']==PUBLISHER_SHA
          and publisher['artifact']['size_bytes']==75279314 and publisher['artifact']['sha1']=='6960b299a39a039ac8a5eb9b07be4ad0e3e0a570','publisher artifact drift')
    check(publisher['mutation']=='NO_MUTATION' and publisher['physical_qa']=='NOT_TESTED' and publisher['static_contract']=='NOT_CERTIFIED','publisher discovery status drift')
    check(discovery['scope']==publisher['scope'] and discovery['report']['sha256']==ORIGINAL_PUBLISHER_REPORT and discovery['native_class']['sha256']==OWNER_SHA,
          'original gingerbread discovery seal drift')
    data=publisher['native']['targets']
    check(set(data)=={OWNER},'publisher class roster drift')
    native=data[OWNER]
    check(native['class_sha256']==OWNER_SHA and len(native['methods'])==8 and len(native['declarations'])==8 and len(native['fields'])==7,'native owner surface drift')
    check(len(native['in_jar_ancestors'])==0,'unexpected inherited provider owner')
    ms={x['declaration']['name']:x for x in native['methods']}
    check(set(ms)==set(METHOD_INS),'exact method census drift')
    check([{'name':m['declaration']['name'],'descriptor':m['declaration']['descriptor'],'instruction_count':m['instruction_count'],'instruction_sha256':m['instruction_sha256']} for m in native['methods']]==discovery['native_class']['methods'],'original method seal drift')
    for name,(descriptor,count,sha) in METHOD_INS.items():
        m=ms[name]
        check(m['declaration']['descriptor']==descriptor and m['instruction_count']==count and
              m['instruction_sha256']==sha and digest(canonical(m['instructions']).encode())==sha,
              'method JVM identity drift '+name)
    expect(ms['acModifiers'],20,'invokevirtual','getOrCreateDurabilityAttributes')
    expect(ms['acModifiers'],26,'invokestatic','ImmutableMultimap.of')
    expect(ms['getDefaultAttributeModifiers'],14,'invokestatic','ACCompat.itemAttributes')
    expect(ms['getOrCreateDurabilityAttributes'],37,'fdiv')
    expect(ms['getOrCreateDurabilityAttributes'],39,'ldc2_w','double 0.1d')
    expect(ms['getOrCreateDurabilityAttributes'],42,'ldc2_w','double 0.9d')
    expect(ms['getOrCreateDurabilityAttributes'],149,'invokeinterface','Map.put')
    expect(ms['getOrCreateDurabilityAttributes'],111,'getstatic','MOVEMENT_SPEED')
    expect(ms['getOrCreateDurabilityAttributes'],122,'getstatic','ADD_MULTIPLIED_BASE')
    expect(ms['getArmorTexture'],1,'getstatic','EquipmentSlot.LEGS')
    expect(ms['getArmorTexture'],7,'ldc','gingerbread_armor_1.png')
    expect(ms['getArmorTexture'],10,'ldc','gingerbread_armor_0.png')
    for j,enum in enumerate(NAMES):
        expect(ms['<clinit>'],6+8*j,'ldc',UUID_BY_SLOT[enum])
    expect(ms['<init>'],40,'invokevirtual','ACArmorMaterial.defense')
    expect(ms['<init>'],50,'invokevirtual','ArmorItem$Type.ordinal')
    expect(ms['<init>'],112,'invokestatic','ACCompat.attributeModifier')
    check(set(native['consumers'])=={
        REGISTRY,'com/github/alexmodguy/alexscaves/client/render/item/ACArmorRenderProperties',OWNER},
          'publisher typed consumers drift')
    registry=native['consumers'][REGISTRY]
    check(len(registry['sites'])==8,'Gingerbread factory typed reference census drift')
    found={x['declaration']['name']:x for x in registry['bodies']}
    check(set(found)=={'lambda$static$'+str(n) for n in range(187,191)},'4 factory bodies drift')
    check(discovery['native_class']['typed_consumer_owners']==3,'original consumer census seal')
    check(material['artifact']['sha256']==PUBLISHER_SHA and material['claims']['static_technical_contract']=='CERTIFIED_STATIC_7_AXES', 'material seal identity/scope drift')
    check(material['integration_bounds']['max_damage_array_by_ordinal']==[13,15,16,11], 'base durability ordinal array drift')
    gd=[x for x in material['material_definitions'] if x['name']=='gingerbread']
    check(len(gd)==1,'missing/duplicate material')
    mat=gd[0]
    check(mat['registry_field']=='GINGERBREAD_ARMOR_MATERIAL' and mat['damage_reduction_by_ordinal']==[2,4,5,2] and mat['durability_multiplier']==10
          and mat['enchantability']==25 and mat['toughness']==0 and mat['knockback_resistance']==0 and mat['setup_repair_item']=='GINGERBREAD_CRUMBS',
          'native material operands changed')
    values=seal['objects']
    check(set(values)=={'gingerbread_'+FIELDS[n][0] for n in NAMES},'must certify four distinct objects exactly')
    for name in NAMES:
        slug,fn,ordinal,defense,maxdamage,modelsha,texture=FIELDS[name]
        item='gingerbread_'+slug
        obj=values[item]
        check(obj['resource_id']=='alexscaves:'+item and obj['enum_constant']==name and obj['enum_ordinal']==ordinal and
              obj['factory_method']=='lambda$static$'+str(fn) and obj['armor_add_value']==defense and obj['max_damage_configured']==maxdamage and
              obj['movement_speed_formula']=='0.1D+0.9D*((float)damage/(float)maxDamage)' and
              obj['movement_speed_operation']=='ADD_MULTIPLIED_BASE' and obj['armor_operation']=='ADD_VALUE' and
              obj['model_sha256']==modelsha and obj['armor_texture'].endswith('/'+texture) and
              obj['modifier_uuid']==UUID_BY_SLOT[name] and obj['equipment_slot']=={'HELMET':'HEAD','CHESTPLATE':'CHEST','LEGGINGS':'LEGS','BOOTS':'FEET'}[name],
              'individual parameters/identity drift for '+item)
        check(obj['factory_method'] in found,'factory missing '+item)
        m=found[obj['factory_method']]
        check(m['instruction_count']==6 and len(m['instructions'])==6,'factory method body count drift '+item)
        check(digest(canonical(m['instructions']).encode())==m['instruction_sha256'],'factory body digest drift '+item)
        expect(m,0,'new',OWNER)
        expect(m,4,'getstatic','GINGERBREAD_ARMOR_MATERIAL')
        expect(m,7,'getstatic','ArmorItem$Type.'+name)
        expect(m,10,'invokespecial','GingerbreadArmorItem."<init>"')
        expect(m,13,'areturn')
        model='assets/alexscaves/models/item/'+item+'.json'
        check(publisher['matching_resources'][model]['sha256']==modelsha,'item model hash drift '+item)
        check(obj['evidence_axes']==['identity','behavior','parameters','targeting','costs','integration','validation'],
              'missing static axes '+item)
    check(seal['constraints']['body_type_is_unsupported_by_native_four_slot_arrays'] is True
          and seal['constraints']['body_factory_exists'] is False,
          'BODY external enum non-use must remain explicit')
    return values


def adversarial(official,publisher,material,discovery,seal):
    # Mutate only in-memory reports and reseal transient instruction SHA claims.
    mutations=[]
    for i in range(5):
        x=copy.deepcopy(official)
        at=x['enum']['value_construction_sites'][i]['name_constant_offset']
        row=next(y for y in x['enum']['full_initializer'] if y['offset']==at)
        row['operand']=row['operand'].replace('// String ', '// String FORGED_')
        x['enum']['initializer_instruction_sha256']=digest(canonical(x['enum']['full_initializer']).encode())
        mutations.append((x,publisher,material,discovery,seal))
    for i in range(5):
        x=copy.deepcopy(official)
        x['enum']['value_construction_sites'][i]['numeric_operands_before_ctor'][0][1]=((i+1)%5)
        mutations.append((x,publisher,material,discovery,seal))
    for name in NAMES:
        x=copy.deepcopy(publisher)
        m=next(z for z in x['native']['targets'][OWNER]['consumers'][REGISTRY]['bodies']
               if z['declaration']['name']=='lambda$static$'+str(FIELDS[name][1]))
        row=next(z for z in m['instructions'] if z['offset']==7)
        row['symbol']=row['symbol'].replace('ArmorItem$Type.'+name,'ArmorItem$Type.BODY')
        m['instruction_sha256']=digest(canonical(m['instructions']).encode())
        mutations.append((official,x,material,discovery,seal))
    for name in NAMES:
        x=copy.deepcopy(seal)
        x['objects']['gingerbread_'+FIELDS[name][0]]['max_damage_configured']+=10
        mutations.append((official,publisher,material,discovery,x))
    for key in ('damage_reduction_by_ordinal','durability_multiplier','setup_repair_item'):
        x=copy.deepcopy(material)
        row=next(z for z in x['material_definitions'] if z['name']=='gingerbread')
        if key=='damage_reduction_by_ordinal':row[key][0]+=1
        elif key=='durability_multiplier':row[key]+=1
        else:row[key]='UNVERIFIED'
        mutations.append((official,publisher,x,discovery,seal))
    for key in ('mutation','mutating_hook','physical_qa'):
        x=copy.deepcopy(seal)
        x['states'][key]='VERIFIED'
        mutations.append((official,publisher,material,discovery,x))
    for x in mutations:
        try:assert_context(*x,strict=False)
        except (ValueError,KeyError,TypeError,IndexError):pass
        else:raise ValueError('adversarial forged report accepted')
    return len(mutations)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for k in ('official','publisher','material','discovery','manifest'):
        p.add_argument('--'+k,type=Path,required=True)
    p.add_argument('--adversarial',action='store_true')
    p.add_argument('--cards-root',type=Path)
    a=p.parse_args()
    raw_off,off=load(a.official,25_000)
    raw_pub,pub=load(a.publisher,350_000)
    _,mat=load(a.material,200_000)
    _,dis=load(a.discovery,60_000)
    _,seal=load(a.manifest,35_000)
    check(digest(raw_off)==STABLE_OFFICIAL_REPORT,'new official report raw hash drift')
    check(digest(raw_pub)==ORIGINAL_PUBLISHER_REPORT,'old Gingerbread report raw hash drift')
    objects=assert_context(off,pub,mat,dis,seal)
    if a.cards_root:
        for name,(slug,fn,ordinal,defense,maximum,modelsha,_texture) in FIELDS.items():
            path=a.cards_root/('gingerbread_'+slug+'.md')
            if not path.exists():
                # Existing catalog slugs are hyphenated.
                path=a.cards_root/('gingerbread-'+slug+'.md')
            card=path.read_text(encoding='utf-8')
            for token in ('CERTIFIED_STATIC_7_AXES','NO_MUTATION',
                          'alexscaves:gingerbread_'+slug,
                          'lambda$static$'+str(fn),
                          'ordinal **'+str(ordinal)+'**',
                          'defesa **'+str(defense)+'**',
                          'durabilidade **'+str(maximum)+'**',
                          UUID_BY_SLOT[name],
                          'EXACT-GINGERBREAD-ARMOR-FOUR-PIECES-1.0.10.md'):
                check(token in card,'individual card missing '+token+': '+str(path))
    count=adversarial(off,pub,mat,dis,seal) if a.adversarial else 0
    print('PASS',len(objects),'individually scoped Gingerbread static contracts, official enum 5 constants, 8 native methods, 4 exact registry factories, all 7 axes')
    print('ADVERSARIAL_REPORT_MUTATIONS_REJECTED',count)
    print('NO_MUTATION / NOT_VERIFIED HOOK / NOT_TESTED PHYSICAL QA / PROVIDER OPEN')

if __name__=='__main__':main()
