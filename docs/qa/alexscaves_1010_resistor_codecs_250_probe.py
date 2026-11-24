#!/usr/bin/env python3
"""Exact distributed stack component codec and enchantment filter boundary discovery.
No gameplay execution, no mutation, no proof of live packet or NBT acceptance.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
from zipfile import ZipFile

from alexscaves_1010_armor_material_audit import ClassReader, canonical, digest, require, verify_artifact, SHA1, SHA256, SIZE
from alexscaves_1010_enchantable_item_probe import disassemble, summarize
from alexscaves_1010_galena_211248_spawn_denial_guards_probe import analyze
from alexscaves_1010_nuclear_explosion_effect_probe import bootstrap, numeric, MATH
from alexscaves_1010_destroyed_item_engine_reference import verify_artifact as verify_universal

MC = "net/minecraft/"
NF = "net/neoforged/neoforge/"
STACK=MC+"world/item/ItemStack"
PATCH=MC+"core/component/DataComponentPatch"
TYPE=MC+"core/component/DataComponentType"
CUSTOM=MC+"world/item/component/CustomData"
COMPONENTS=MC+"core/component/DataComponents"
ENCH=MC+"world/item/enchantment/Enchantment"
CODECS=MC+"network/codec/ByteBufCodecs"
PIN = {
    STACK:"072cd6887595d3f928a3a1a9605662ff547fe3201d6b6d713a43bfd2719f1a13",
    CUSTOM:"23463cf7238fbd2b9ff5bb11bb4a5466fcc06137e89f65d199fe31b7b7d451c9",
    MC+"nbt/CompoundTag":"93a9643a11aa61b666871cadeb14be32ff4f813bf97b05951bae389bada15fe6",
}
UNIVERSAL_SHA = "1f9cc68fe9ec0416475d34ce76e95a696b9721d5d338168563dab0632c3d2956"
UNIVERSAL_SIZE = 3551255
ALL_BODIES = {STACK+"$1",STACK+"$2",PATCH+"$1",PATCH+"$PatchKey",TYPE+"$Builder"}
SELECTED = {
    STACK:{"<init>","lambda$static$4","lambda$static$8","validateStrict","getAllEnchantments","getEnchantmentLevel","save","saveOptional","parse","parseOptional"},
    PATCH:{"<init>","<clinit>","lambda$static$0","lambda$static$1"},
    TYPE:{"<clinit>","builder","codec","streamCodec","isTransient","codecOrThrow"},
    COMPONENTS:{"lambda$static$0","register"},
    CUSTOM:{"<init>","<clinit>","lambda$static$0","lambda$static$2","lambda$static$3"},
    MC+"nbt/CompoundTag":{"<clinit>","write"},
    MC+"nbt/NbtIo":{"readAnyTag","writeAnyTag","readUnnamedTag","writeUnnamedTag","read","write"},
    MC+"nbt/NbtAccounter":{"create","unlimitedHeap","accountBytes","pushDepth","popDepth"},
    MC+"network/FriendlyByteBuf":{"readNbt","writeNbt","readNbtWithCodec","writeNbtWithCodec"},
    CODECS:{"<clinit>","tagCodec","compoundTagCodec","fromCodec","fromCodecTrusted","fromCodecWithRegistries","fromCodecWithRegistriesTrusted","registry","holderRegistry"},
    MC+"network/codec/StreamCodec":{"map","composite"},
    ENCH:{"modifyItemFilteredCount","modifyDurabilityChange","modifyItemDamage"},
    MC+"world/item/enchantment/ItemEnchantments":{"getLevel","entrySet","<clinit>"},
    MC+"world/item/enchantment/EnchantmentHelper":{"runIterationOnItem","processDurabilityChange"},
    NF+"common/extensions/IItemExtension":{"getAllEnchantments","getEnchantmentLevel"},
    NF+"common/extensions/IItemStackExtension":{"getAllEnchantments","getEnchantmentLevel"},
    NF+"common/CommonHooks":{"resolveLookup","getEnchantmentLevel","getAllEnchantments"},
}
REQUIRED = {
    STACK:{"save","parse"},
    STACK+"$1":{"decode","encode"},
    STACK+"$2":{"decode","encode"},
    PATCH+"$1":{"decode","encode"},
    PATCH+"$PatchKey":{"valueCodec"},
    TYPE+"$Builder":{"build"},
    COMPONENTS:{"lambda$static$0","register"},
    CUSTOM:{"<clinit>","<init>"},
    MC+"network/FriendlyByteBuf":{"readNbt","writeNbt"},
    CODECS:{"<clinit>"},
    ENCH:{"modifyItemFilteredCount","modifyDurabilityChange"},
}
LIMITS = {
    "actual_roundtrip":"NOT_TESTED","actual_durability_settlement":"NOT_VERIFIED",
    "runtime_loaded_bytes":"NOT_OBSERVED","effective_enchantments":"NOT_VERIFIED",
    "static_contract":"NOT_CERTIFIED","mutating_hook":"NOT_VERIFIED",
    "physical_qa":"NOT_TESTED","mutation":"NO_MUTATION","provider_universe_closed":False,
    "semantic_magic_roots_delta":0,
}
def selected(owner,name):
    if owner in ALL_BODIES or name in SELECTED.get(owner,()):return True
    return owner==STACK and name.startswith("lambda$static$") or owner==ENCH and name.startswith("lambda$modifyItemFilteredCount")

def scan(installer,server,srg,universal,publisher,javap):
    identity={'neoforge_version':'21.1.250','minecraft_version':'1.21.1'}
    for label,path,expected,expected_size in (
        ('installer',installer,'0e47a91ba2139a8db4bf7627af081f7b5789b508bb039ee8dea1272b79693d60',6972109),
        ('server',server,'1808fab692dc44b2d474295d1cdd9f1fe8a7dceab4f594210873646fafdf1359',5675624),
        ('srg',srg,'26ca9c40d7e1681190b428583c38816852218e78df3f8bdb60a59a78503aec71',14246609)):
        raw=path.read_bytes()
        require(digest(raw)==expected and len(raw)==expected_size,'physical-ledger distribution pin '+label)
        identity[label]={'sha256':expected,'bytes':expected_size}
    verify_universal(universal,'universal')
    verify_artifact(publisher)
    identity['publisher']={'sha1':SHA1,'sha256':SHA256,'size_bytes':SIZE}
    data=universal.read_bytes()
    require(len(data)==UNIVERSAL_SIZE and hashlib.sha256(data).hexdigest()==UNIVERSAL_SHA,"universal pin mismatch")
    identity.update({"universal_sha256":UNIVERSAL_SHA,"universal_bytes":UNIVERSAL_SIZE})
    owners=sorted(ALL_BODIES|set(SELECTED))
    with ZipFile(server) as overlay, ZipFile(universal) as uni, ZipFile(srg) as vanilla, ZipFile(publisher) as mod:
        archives=[("NEOFORGE_OVERLAY",overlay),("NEOFORGE_UNIVERSAL",uni),("INSTALLED_MINECRAFT_SRG",vanilla),("PUBLISHER",mod)]
        for _,z in archives:
            require(len(z.namelist())==len(set(z.namelist())),"duplicate archive entry")
        roster=[(name,z,set(z.namelist())) for name,z in archives]
        classpath=":".join(map(str,(server,universal,srg,publisher)))
        # Discover actual nested codec owners, not a guessed class roster.
        nested=sorted({n[:-6] for _,_,entries in roster for n in entries
                       if n.endswith(".class") and n.startswith((CODECS+"$",TYPE+"$Builder$"))
                       and (n.startswith(TYPE+"$Builder$") or n[len(CODECS)+1:-6].isdigit())})
        require(len(nested)<=80,"nested codec roster budget")
        classes={}
        for owner in owners:
            found=[(name,z) for name,z,entries in roster if owner+".class" in entries]
            if not found:
                require(owner not in REQUIRED,"required owner absent "+owner)
                classes[owner]={"present":False}
                continue
            source,z=found[0]
            raw=z.read(owner+".class")
            sha=digest(raw)
            require(owner not in PIN or sha==PIN[owner],"class SHA drift "+owner)
            reader=ClassReader(raw)
            require(reader.name==owner and reader.major==65,"owner/Java drift "+owner)
            declarations=[m for m in reader.methods if selected(owner,m["name"])]
            missing=REQUIRED.get(owner,set())-{m["name"] for m in declarations}
            require(not missing,"required declared method absent "+owner+" "+str(sorted(missing)))
            require(len(declarations)<=120,"method roster budget "+owner)
            parsed=disassemble(classpath,javap,owner)
            methods=[]
            for d in declarations:
                key=(d["name"],d["descriptor"])
                if "code_sha256" not in d:
                    methods.append({"name":key[0],"descriptor":key[1],"executable":False})
                    continue
                require(key in parsed and bool(parsed[key]),"missing body "+owner+str(key))
                body=parsed[key]
                print("PROJECT_METHOD",owner,*key,flush=True)
                if owner==CODECS and key[0]=="<clinit>":
                    # Full initializer may exceed the semantic member budget. Bound to typed
                    # codec-related field references and adjacent constructor/handle operands.
                    offsets=sorted(body)
                    sites=[]
                    for pos,at in enumerate(offsets):
                        op,arg,sym=body[at]
                        if op=="putstatic" and any("Field "+n+":" in sym for n in ("TAG","TRUSTED_TAG","COMPOUND_TAG","TRUSTED_COMPOUND_TAG","OPTIONAL_COMPOUND_TAG")):
                            sites.append({"offset":at,"symbol":sym,"window":[{"offset":v,"opcode":body[v][0],"operand":body[v][1],"symbol":body[v][2]} for v in offsets[max(0,pos-12):pos+2]]})
                    require(bool(sites),"NBT codec initializer sites absent")
                    methods.append({"name":key[0],"descriptor":key[1],"code_sha256":d["code_sha256"],
                                    "instruction_count":len(body),"instruction_sha256":summarize(reader,key,body)["instruction_sha256"],
                                    "executable":True,"projection":"BOUNDED_NBT_CODEC_INITIALIZER_SITES","sites":sites})
                    continue
                row=analyze(reader,body,d)
                row["instruction_sha256"]=summarize(reader,key,body)["instruction_sha256"]
                row["executable"]=True
                row["numeric_operands"]=[{"offset":at,"opcode":op,"operand":arg,"symbol":sym} for at,(op,arg,sym) in sorted(body.items()) if numeric(op,sym)]
                row["strings"]=[{"offset":at,"symbol":sym} for at,(op,_,sym) in sorted(body.items()) if op.startswith("ldc") and sym.startswith("String ")]
                row["bootstrap_links"]=bootstrap(reader,body)
                row["arithmetic"]=[{"offset":at,"opcode":op} for at,(op,_,_) in sorted(body.items()) if op in MATH]
                row["local_accesses"]=[{"offset":at,"opcode":op,"slot_operand":arg} for at,(op,arg,_) in sorted(body.items()) if op.startswith(("dload","dstore","fload","fstore","iload","istore","aload","astore")) or op=="iinc"]
                methods.append(row)
            classes[owner]={"present":True,"source":source,"available_sources":[name for name,_ in found],"class_sha256":sha,
                            "parent":reader.parent,"interfaces":reader.interfaces,
                            "declared_methods":[{"name":m["name"],"descriptor":m["descriptor"]} for m in reader.methods],
                            "methods":methods}
        # invokevirtual may resolve an inherited default; do not require a
        # declaration on ItemStack just because it is the callsite owner.
        inheritance={}
        for owner in (STACK,NF+"common/extensions/IItemStackExtension",NF+"common/extensions/IItemExtension",NF+"common/CommonHooks"):
            inheritance[owner]=[m for m in classes.get(owner,{}).get("methods",[]) if m["name"]=="getAllEnchantments"]
        require(any(v for v in inheritance.values()),"effective enchantment entrypoint not found")
    return {"schema_version":1,"scope":"RESISTOR_COMPONENT_CODEC_AND_EFFECT_FILTER_250_DISCOVERY_ONLY","artifact":identity,"classes":classes,"nested_codec_candidates":nested,"effective_enchantment_declarations":{o:[{"name":m["name"],"descriptor":m["descriptor"],"code_sha256":m.get("code_sha256")} for m in ms] for o,ms in inheritance.items()},"limits":LIMITS}

def self_test():
    require(selected(STACK+"$1","decode"),"nested stack codec")
    require(selected(PATCH+"$1","encode"),"nested patch codec")
    require(selected(COMPONENTS,"lambda$static$0"),"custom data binding")
    require(selected(ENCH,"modifyItemFilteredCount"),"effect filtering")
    require(not selected("foreign/ItemStack","save"),"namespace")
    require(LIMITS["mutation"]=="NO_MUTATION","policy")
    print("PASS: five scope checks and policy")

if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--installer",type=Path)
    p.add_argument("--server",type=Path)
    p.add_argument("--srg",type=Path)
    p.add_argument("--universal",type=Path)
    p.add_argument("--publisher",type=Path)
    p.add_argument("--javap",default="javap")
    p.add_argument("--output",type=Path)
    p.add_argument("--self-test",action="store_true")
    a=p.parse_args()
    if a.self_test:
        self_test()
    else:
        require(all((a.installer,a.server,a.srg,a.universal,a.publisher,a.output)) and not a.output.exists(),"write-once report and artifacts required")
        result=scan(a.installer,a.server,a.srg,a.universal,a.publisher,a.javap)
        data=canonical(result).encode()
        require(len(data)<=4_000_000,"report budget")
        a.output.parent.mkdir(parents=True,exist_ok=True)
        with a.output.open("xb") as f:
            f.write(data)
        print("REPORT_SHA256",digest(data),"BYTES",len(data))
        print("NESTED_CODEC_CANDIDATES",json.dumps(result["nested_codec_candidates"]))
        for owner,row in result["classes"].items():
            print("OWNER",owner,row.get("source"),row.get("class_sha256"))
            for m in row.get("methods",[]):
                print("METHOD",owner,m["name"],m["descriptor"],m.get("code_sha256"),m.get("instruction_count"))
                if m["executable"]:
                    print("SEMANTIC",json.dumps({"owner":owner,**m},sort_keys=True))
        print("DISCOVERY_ONLY NO_MUTATION WORLD_SAFETY_BLOCKED")
