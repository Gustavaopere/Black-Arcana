#!/usr/bin/env python3
"""Bounded exact field-reference, resource and downstream causal audit."""
import argparse, json, re
from pathlib import Path
from zipfile import ZipFile
from alexscaves_1010_armor_material_audit import ClassReader, canonical, digest, require, verify_artifact
from alexscaves_1010_enchantable_item_probe import disassemble
from alexscaves_1010_four_items_downstream_250_probe import projection

ROOT="com/github/alexmodguy/alexscaves/"
REG=ROOT+"server/item/ACItemRegistry"
COMPAT=ROOT+"server/misc/ACCompat"
FIELD_NAMES={"GREEN_SOYLENT","SLAM","SPELUNKIE","RADIANT_ESSENCE","LICOWITCH_RADIANT_ESSENCE","JELLY_BEAN"}
IDS={"alexscaves:"+n.lower() for n in FIELD_NAMES}
ITEM_CLASSES={ROOT+"server/item/"+n for n in ("RadiationRemovingFoodItem","RadiantEssenceItem","JellyBeanItem","KeybindUsingArmor")}
PINS={
ROOT+"server/item/RadiationRemovingFoodItem":"589f2f1732b353a52aed025d20b29d0f4e8234e58c4cb0fe9072df6a5d975dc4",
ROOT+"server/item/RadiantEssenceItem":"eb072027b5797f7b96e83cabd58ebdfd3029e5c1e84fa789c620309dd3a57d92",
ROOT+"server/item/JellyBeanItem":"9842c28cd2eff05621a23be37ce5917ca88a19bf0bd99f0da9b5a5cc62a4355f",
ROOT+"server/item/KeybindUsingArmor":"6ed129bf051acf5b551e2e96ed898c818304fe99e0298fb9f0a5ebf226bc3b86",
REG:"114e4a3576d56cb66d240fa9df9db7693b1df576ebfa86631ef751dd1e7b5bb1"}
SELECTED={
COMPAT:{"food","nutrition","effect","potionEffects","potionColor","applyInstantenousEffect","getTag","getBoolean","setTag"},
ROOT+"server/message/ArmorKeyMessage":None,
ROOT+"server/message/ACNetworkContext":None,
ROOT+"server/message/ACNetwork$NeoForgeContext":None,
ROOT+"server/message/ACNetwork":{"registerPayloads","lambda$registerPayloads$0"},
ROOT+"server/item/DarknessArmorItem":{"onKeyPacket","canChargeUp","acInventoryTick","hasMeter","getMeterProgress"},
ROOT+"server/message/UpdateItemTagMessage":None,
ROOT+"server/item/UpdatesStackTags":None,
}
FACTORIES={"lambda$static$64","lambda$static$65","lambda$static$66","lambda$static$181","lambda$static$182","lambda$static$198"}
ROSTER_SHA="2296d31ecc7fabb375922b8ad23c7a25c3e969bdfd80d5e1aa602034ae5d62ed"
def strings(value,path=()):
    if isinstance(value,dict):
        for k,v in sorted(value.items()):
            if k in IDS:yield [*path,k]
            yield from strings(v,(*path,k))
    elif isinstance(value,list):
        for i,v in enumerate(value):yield from strings(v,(*path,i))
    elif isinstance(value,str) and value in IDS:yield [*path]
def select(rd,body,key):
    decl=next(d for d in rd.methods if (d["name"],d["descriptor"])==key)
    require(len(body[key])<=1600,"selected body over budget")
    return projection(rd,key,body[key],decl)
def inspect(jar,javap):
    verify_artifact(jar)
    result={"scope":"STATIC_CLOSURE_CANDIDATE_ONLY","mutation":"NO_MUTATION","provider_universe_closed":False,"mutating_hook":"NOT_VERIFIED","physical_qa":"NOT_TESTED","owners":{},"field_consumers":{},"resource_consumers":{}}
    with ZipFile(jar) as z:
        paths=z.namelist();roster=sorted(p for p in paths if p.endswith(".class"))
        require(len(paths)==len(set(paths)) and len(roster)==1555,"roster")
        require(digest(("\n".join(roster)+"\n").encode())==ROSTER_SHA,"roster digest")
        for path in roster:
            raw=z.read(path);rd=ClassReader(raw);owner=rd.name
            require(owner+".class"==path,"class path")
            refs=[x for x in rd.typed_refs(REG) if x["kind"]=="field_reference" and x["name"] in FIELD_NAMES]
            typed=[x for target in sorted(ITEM_CLASSES) for x in rd.typed_refs(target) if x["kind"] in {"class_constant","method_reference","interface_method_reference"}]
            if owner not in SELECTED and owner not in ITEM_CLASSES and owner!=REG and not refs and not typed:continue
            if owner in PINS:require(digest(raw)==PINS[owner],"class pin "+owner)
            parsed=disassemble(jar,javap,owner)
            methods=[];field_sites=[];cp={x["index"] for x in refs};selected_cp={x["index"] for x in typed}
            for key,body in sorted(parsed.items()):
                hits=[];typed_hits=[];offsets=sorted(body)
                for i,at in enumerate(offsets):
                    op,arg,sym=body[at];m=re.match(r"#(\d+)(?:\s|,|$)",arg)
                    if not m:continue
                    ci=int(m[1])
                    if ci in cp:
                        hits.append({"offset":at,"opcode":op,"member":rd.resolve(ci),"window":[{"offset":q,"opcode":body[q][0],"operand":body[q][1],"symbol":body[q][2]} for q in offsets[max(0,i-7):i+8]]})
                    if ci in selected_cp:typed_hits.append(at)
                if hits:field_sites.append({"name":key[0],"descriptor":key[1],"code_sha256":next(d["code_sha256"] for d in rd.methods if (d["name"],d["descriptor"])==key),"sites":hits})
                explicit=(owner in ITEM_CLASSES or owner==REG and key[0] in FACTORIES or owner in SELECTED and (SELECTED[owner] is None or key[0] in SELECTED[owner]))
                # The registry initializer is large; preserve causal windows there.
                if explicit or (hits or typed_hits) and owner!=REG and len(body)<=1600:
                    methods.append(select(rd,parsed,key))
            if refs:result["field_consumers"][owner]={"class_sha256":digest(raw),"refs":refs,"sites":field_sites}
            result["owners"][owner]={"class_sha256":digest(raw),"parent":rd.parent,"interfaces":rd.interfaces,"fields":rd.fields,"declarations":[{"name":v["name"],"descriptor":v["descriptor"],"code_sha256":v.get("code_sha256")} for v in rd.methods],"methods":methods}
        require(set(PINS)|set(SELECTED)<=set(result["owners"]),"selected owner absent")
        require(1<=len(result["field_consumers"])<=70 and len(result["owners"])<=100,"owner budget")
        require(sum(len(x["methods"]) for x in result["owners"].values())<=350,"method budget")
        for path in sorted(p for p in paths if p.endswith(".json") and p.startswith(("data/","assets/alexscaves/models/item/"))):
            raw=z.read(path)
            if not any(n.encode() in raw for n in IDS):continue
            require(len(raw)<=1500000,"resource size")
            decoded=json.loads(raw);hits=list(strings(decoded))
            if hits:result["resource_consumers"][path]={"sha256":digest(raw),"size":len(raw),"id_paths":hits}
        require(len(result["resource_consumers"])<=300,"resource budget")
    require(len(result["owners"][REG]["methods"])==6,"factory roster")
    for name in ("food","nutrition","effect","potionEffects","potionColor","applyInstantenousEffect"):
        require(any(x["name"]==name for x in result["owners"][COMPAT]["methods"]),"missing bridge "+name)
    return result
def self_test():
    require(len(PINS)==5 and len(FACTORIES)==6,"scope")
    require(list(strings({"items":["alexscaves:green_soylent","alexscaves:green_soylent_extra"]}))==[["items",0]],"exact resource token")
    require(list(strings({"alexscaves:slam":True}))==[["alexscaves:slam"]],"resource key")
    require(not list(strings({"item":"other:slam"})),"namespace")
    print("PASS four identity scope checks")
if __name__=="__main__":
    ap=argparse.ArgumentParser();ap.add_argument("--jar",type=Path);ap.add_argument("--javap",default="javap");ap.add_argument("--output",type=Path);ap.add_argument("--self-test",action="store_true")
    a=ap.parse_args()
    if a.self_test:self_test()
    else:
        require(a.jar and a.output and not a.output.exists(),"write once")
        report=inspect(a.jar,a.javap);raw=canonical(report).encode();require(len(raw)<=10000000,"report budget")
        with a.output.open("xb") as f:f.write(raw)
        print("REPORT_SHA256",digest(raw),"BYTES",len(raw))
        for owner,row in report["owners"].items():
            print("OWNER",owner,row["class_sha256"],"DECLARATIONS",len(row["declarations"]),"PROJECTED",len(row["methods"]))
            for method in row["methods"]:print("SEMANTIC",json.dumps({"owner":owner,**method},sort_keys=True))
        for owner,row in report["field_consumers"].items():
            for method in row["sites"]:
                for site in method["sites"]:print("FIELD_SITE",json.dumps({"owner":owner,"name":method["name"],"descriptor":method["descriptor"],"code_sha256":method["code_sha256"],**site},sort_keys=True))
        for path,row in report["resource_consumers"].items():print("RESOURCE_ID",json.dumps({"path":path,**row},sort_keys=True))
        print("END_CLOSURE_CANDIDATE NO_MUTATION")
