#!/usr/bin/env python3
"""Reconcile five discoveries and expand typed-only dispatch and native boundaries."""
import argparse,json,re,zipfile
from pathlib import Path
from alexscaves_1010_armor_material_audit import ClassReader,canonical,digest,require,verify_artifact
from alexscaves_1010_enchantable_item_probe import disassemble,summarize
from alexscaves_1010_adjacent_items_probe import PREFIX,TARGETS
BASE="com/github/alexmodguy/alexscaves/"
SELECT={
    BASE+"server/block/ACBlockRegistry": {"lambda$getBlockSupplier$437","lambda$getBlockSupplier$438","lambda$getBlockSupplier$439","lambda$getBlockSupplier$445"},
    BASE+"server/block/MetalScaffoldingBlock":{"getDistance"},
    BASE+"server/misc/ACCompat":{"isEdible","food","canAlwaysEat","getTag","setTag","getString","useConsume","useFail","usePass"},
    BASE+"server/block/ConversionCrucibleBlock":{"acUse"},
    BASE+"server/block/blockentity/ConversionCrucibleBlockEntity":{"tick","calculateBiomeColor"},
    BASE+"server/level/biome/ACBiomeRegistry":{"getBiomeTabletColor"},
}
def inspect(jar,javap,initial):
    verify_artifact(jar)
    with zipfile.ZipFile(jar) as z:
        native=initial["native"]
        out={}
        cache={}
        def parsed(owner):
            if owner not in cache:
                rd=ClassReader(z.read(owner+".class"))
                cache[owner]=(rd,disassemble(jar,javap,owner) if any("code_sha256" in m for m in rd.methods) else {})
            return cache[owner]
        for target in TARGETS:
            sites=[]
            selected={}
            for owner,refs in native["targets"][target]["typed_census"].items():
                idx={x["index"] for x in refs if x["kind"]=="class_constant"}
                if not idx:continue
                rd,body=parsed(owner)
                for k,rows in sorted(body.items()):
                    found=[]
                    for off,(op,operand,symbol) in sorted(rows.items()):
                        cp=re.match(r"#(\d+)",operand)
                        if cp and int(cp[1]) in idx:
                            found.append({"owner":owner,"method":k[0],"descriptor":k[1],"offset":off,"opcode":op,"symbol":symbol})
                    if found:
                        sites+=found
                        selected.setdefault(owner,[]).append(summarize(rd,k,rows))
            out[target]={"class_constant_sites":sites,"consumer_bodies":selected,"attributes":parsed(target)[0].attributes}
        extra={}
        for owner,names in sorted(SELECT.items()):
            rd,body=parsed(owner)
            methods=[summarize(rd,k,v) for k,v in sorted(body.items()) if k[0] in names]
            # Record unresolved names transparently instead of asserting absent class implies no behavior.
            extra[owner]={"class_sha256":digest(z.read(owner+".class")),"requested":sorted(names),"missing":sorted(names-{m["declaration"]["name"] for m in methods}),"methods":methods,"attributes":rd.attributes}
        return {"targets":out,"native_boundaries":extra}
def main():
    p=argparse.ArgumentParser()
    for key in ("jar","javap","initial","output"):p.add_argument("--"+key,type=Path,required=True)
    a=p.parse_args()
    require(not a.output.exists(),"new report required")
    raw=a.initial.read_bytes()
    require(digest(raw)=="357381bd6a9ca6f8df9d79ef274552468033832664a40f59fc04ec2d76d99a6c","discovery hash drift")
    report={"scope":"DISCOVERY_NOT_CERTIFIED","initial_sha256":digest(raw),"native":inspect(a.jar,a.javap,json.loads(raw)),"mutation":"NO_MUTATION"}
    a.output.write_text(canonical(report),encoding="utf8")
    print("BOUNDARY_SHA256",digest(a.output.read_bytes()))
    for target,data in report["native"]["targets"].items():
        print("TYPE_SITES",target,json.dumps(data["class_constant_sites"],sort_keys=True))
        print("ATTRIBUTES",target,json.dumps(data["attributes"],sort_keys=True))
        for owner,methods in data["consumer_bodies"].items():
            if target.endswith("AlwaysCombinableOnAnvil") or owner.endswith("CaveInfoItem"):
                for m in methods:print("TYPE_BODY",target,owner,json.dumps(m,sort_keys=True))
    for owner,data in report["native"]["native_boundaries"].items():
        print("BOUNDARY_OWNER",owner,data["class_sha256"],json.dumps(data["missing"]))
        for m in data["methods"]:
            if len(m["instructions"])>350:
                m={**m,"instructions":[x for x in m["instructions"] if 650<=x["offset"]<=850 or x["opcode"].startswith("if") or x["opcode"] in ("goto","return","areturn")]}
            print("BOUNDARY_METHOD",owner,json.dumps(m,sort_keys=True))
if __name__=="__main__":main()
