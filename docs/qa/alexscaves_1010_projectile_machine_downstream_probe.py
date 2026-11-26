#!/usr/bin/env python3
"""Read-only downstream inspection of exact item-produced native entities."""
import argparse,json,re
from pathlib import Path
from zipfile import ZipFile
from alexscaves_1010_armor_material_audit import ClassReader, AuditError, canonical, digest, require, verify_artifact
from alexscaves_1010_enchantable_item_probe import disassemble
from alexscaves_1010_four_items_downstream_250_probe import projection
from alexscaves_1010_nuclear_explosion_effect_probe import bootstrap

GROUPS={
"projectiles":{
"CinderBrickEntity","DepthChargeEntity","GuanoEntity","ThrownIceCreamScoopEntity",
"LimestoneSpearEntity","SeekingArrowEntity","SodaBottleRocketEntity"},
"machines":{"QuarrySmasherEntity","SubmarineEntity"},
}
FIELDS={
"projectiles":{"CINDER_BRICK","DEPTH_CHARGE","GUANO","THROWN_ICE_CREAM_SCOOP","LIMESTONE_SPEAR","SEEKING_ARROW","SODA_BOTTLE_ROCKET"},
"machines":{"QUARRY_SMASHER","SUBMARINE"},
}
TOKENS={
"projectiles":{"cinder_brick","depth_charge","guano","ice_cream_scoop","limestone_spear","seeking_arrow","soda_bottle_rocket"},
"machines":{"quarry_smasher","submarine"},
}
ROSTER_SHA="2296d31ecc7fabb375922b8ad23c7a25c3e969bdfd80d5e1aa602034ae5d62ed"
def simple(owner):return owner.rsplit("/",1)[-1]
def project(rd,key,body):
    decl=next(d for d in rd.methods if (d["name"],d["descriptor"])==key)
    if "code_sha256" not in decl:
        require(not body,"abstract instructions")
        return {"name":key[0],"descriptor":key[1],"executable":False}
    require(bool(body),"missing executable body")
    return {**projection(rd,key,body,decl),"executable":True}
def inspect(jar,javap,group):
    verify_artifact(jar)
    out={"group":group,"scope":"DOWNSTREAM_STATIC_DISCOVERY_ONLY","mutation":"NO_MUTATION","provider_universe_closed":False,"physical_qa":"NOT_TESTED","owners":{},"typed_consumers":{},"registry_candidates":{},"resources":{}}
    with ZipFile(jar) as z:
        paths=z.namelist();roster=sorted(p for p in paths if p.endswith(".class"))
        require(len(paths)==len(set(paths)) and len(roster)==1555,"roster")
        require(digest(("\n".join(roster)+"\n").encode())==ROSTER_SHA,"roster hash")
        targets={}
        for name in sorted(GROUPS[group]|{"ACEntityRegistry"}):
            matches=[p[:-6] for p in roster if simple(p[:-6])==name]
            require(len(matches)==1,"unique native owner "+name)
            targets[name]=matches[0]
        registry=targets.pop("ACEntityRegistry");primary=set(targets.values())
        require(all("/server/entity/" in p for p in primary),"native entity namespace")
        hierarchy={}
        for path in roster:
            rd=ClassReader(z.read(path));require(rd.name+".class"==path,"class path")
            hierarchy[rd.name]=(rd.parent,rd.interfaces)
        own=set(primary)
        for target in sorted(primary):
            parent=hierarchy[target][0]
            while parent in hierarchy and parent not in own:
                own.add(parent);parent=hierarchy[parent][0]
        require(len(own)<=20,"bounded native hierarchy")
        for path in roster:
            raw=z.read(path);rd=ClassReader(raw);owner=rd.name
            refs=[x for target in sorted(primary) for x in rd.typed_refs(target) if x["kind"] in {"class_constant","field_reference","method_reference","interface_method_reference"}]
            registry_refs=[x for x in rd.typed_refs(registry) if x["kind"]=="field_reference" and x["name"] in FIELDS[group]]
            if owner not in own and owner!=registry and not refs and not registry_refs:continue
            parsed=disassemble(jar,javap,owner);cp={x["index"] for x in refs+registry_refs};methods=[];deferred=[];sites=[]
            for key,body in sorted(parsed.items()):
                offsets=sorted(body);hits=[]
                for i,at in enumerate(offsets):
                    op,arg,symbol=body[at];m=re.match(r"#(\d+)(?:\s|,|$)",arg)
                    if m and int(m[1]) in cp:
                        hits.append({"offset":at,"opcode":op,"member":rd.resolve(int(m[1])),"window":[{"offset":q,"opcode":body[q][0],"operand":body[q][1],"symbol":body[q][2]} for q in offsets[max(0,i-6):i+7]]})
                decl=next(d for d in rd.methods if (d["name"],d["descriptor"])==key)
                if hits:sites.append({"name":key[0],"descriptor":key[1],"code_sha256":decl.get("code_sha256"),"sites":hits})
                if owner==registry and key[0]=="<clinit>":
                    links=bootstrap(rd,body)
                    by_offset={x["offset"]:x for x in links}
                    for hit in hits:
                        if hit["opcode"]!="putstatic":continue
                        near=[by_offset[q["offset"]] for q in hit["window"] if q["offset"] in by_offset]
                        out["registry_candidates"][str(hit["offset"])]={"code_sha256":decl["code_sha256"],"site":hit,"nearby_bootstraps":near}
                if owner in own or hits and owner!=registry:
                    try:methods.append(project(rd,key,body))
                    except AuditError as err:
                        deferred.append({"name":key[0],"descriptor":key[1],"code_sha256":decl.get("code_sha256"),"instruction_count":len(body),"reason":str(err)})
            if refs or registry_refs:out["typed_consumers"][owner]={"class_sha256":digest(raw),"refs":refs,"registry_refs":registry_refs,"method_sites":sites}
            out["owners"][owner]={"class_sha256":digest(raw),"parent":rd.parent,"interfaces":rd.interfaces,"primary":owner in primary,"native_ancestor":owner in own and owner not in primary,"fields":rd.fields,"declarations":[{"name":x["name"],"descriptor":x["descriptor"],"code_sha256":x.get("code_sha256")} for x in rd.methods],"methods":methods,"deferred":deferred}
        require(primary<=set(out["owners"]) and len(out["owners"])<=160,"owner coverage/budget")
        require(sum(len(v["methods"])+len(v["deferred"]) for v in out["owners"].values())<=1000,"method budget")
        require(sum(len(s["sites"]) for v in out["typed_consumers"].values() for s in v["method_sites"])<=2000,"site budget")
        for path in sorted(p for p in paths if p.endswith(".json") and any(t in p.lower() for t in TOKENS[group])):
            raw=z.read(path);require(len(raw)<=1000000,"resource size")
            out["resources"][path]={"sha256":digest(raw),"size":len(raw),"decoded":json.loads(raw)}
        require(len(out["resources"])<=250,"resource budget")
    return out
def self_test():
    require(len(GROUPS["projectiles"])==7 and len(GROUPS["machines"])==2,"scope")
    require(not GROUPS["projectiles"]&GROUPS["machines"],"disjoint")
    require(simple("a/b/CinderBrickEntity")=="CinderBrickEntity","identity suffix")
    class Stub:
        methods=[{"name":"abstract","descriptor":"()V"}]
    require(project(Stub(),("abstract","()V"),{})["executable"] is False,"abstract")
    print("PASS four downstream scope checks")
if __name__=="__main__":
    ap=argparse.ArgumentParser();ap.add_argument("--jar",type=Path);ap.add_argument("--javap",default="javap");ap.add_argument("--output",type=Path);ap.add_argument("--group",choices=sorted(GROUPS));ap.add_argument("--self-test",action="store_true")
    a=ap.parse_args()
    if a.self_test:self_test()
    else:
        require(a.jar and a.output and a.group and not a.output.exists(),"write once")
        report=inspect(a.jar,a.javap,a.group);raw=canonical(report).encode();require(len(raw)<=20000000,"report budget")
        with a.output.open("xb") as f:f.write(raw)
        print("REPORT_SHA256",digest(raw),"BYTES",len(raw))
        for owner,row in report["owners"].items():
            print("OWNER",owner,row["class_sha256"],"PARENT",row["parent"],"PRIMARY",row["primary"],"ANCESTOR",row["native_ancestor"],"DECLARATIONS",len(row["declarations"]),"PROJECTED",len(row["methods"]),"DEFERRED",len(row["deferred"]))
            for method in row["methods"]:print("SEMANTIC",json.dumps({"owner":owner,**method},sort_keys=True))
            for method in row["deferred"]:print("DEFERRED",json.dumps({"owner":owner,**method},sort_keys=True))
        for owner,row in report["typed_consumers"].items():
            for method in row["method_sites"]:
                for site in method["sites"]:print("CONSUMER_SITE",json.dumps({"owner":owner,"name":method["name"],"descriptor":method["descriptor"],"code_sha256":method["code_sha256"],**site},sort_keys=True))
        for at,row in report["registry_candidates"].items():print("REGISTRY_CANDIDATE",json.dumps({"offset":at,**row},sort_keys=True))
        for path,row in report["resources"].items():print("RESOURCE",json.dumps({"path":path,**row},sort_keys=True))
        print("END_DOWNSTREAM_DISCOVERY NO_MUTATION")
