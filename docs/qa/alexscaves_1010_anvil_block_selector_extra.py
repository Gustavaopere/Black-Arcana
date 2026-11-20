#!/usr/bin/env python3
"""Exact switch edges, event annotation and block supplier selection; no runtime claims."""
import argparse,json,re,subprocess,zipfile
from pathlib import Path
from alexscaves_1010_armor_material_audit import ClassReader,canonical,digest,require,verify_artifact
from alexscaves_1010_enchantable_item_probe import disassemble,summarize
BASE="com/github/alexmodguy/alexscaves/"
def inspect(jar,javap):
    verify_artifact(jar)
    owner=BASE+"server/event/CommonEvents"
    with zipfile.ZipFile(jar) as z:
        rd=ClassReader(z.read(owner+".class"))
        k=("onUpdateAnvil","(Lnet/neoforged/neoforge/event/AnvilUpdateEvent;)V")
        method=summarize(rd,k,disassemble(jar,javap,owner)[k])
        # javap -v captures annotations and switch case destinations, which the compact parser omits.
        raw=subprocess.check_output([str(javap),"-p","-c","-v","-classpath",str(jar),owner.replace("/",".")],text=True)
        lines=raw.splitlines()
        start=next(i for i,x in enumerate(lines) if re.match(r"  public void onUpdateAnvil\(",x))
        end=next((i for i in range(start+1,len(lines)) if re.match(r"  (public|private|protected|static) ",lines[i]) and lines[i].rstrip().endswith(";")),len(lines))
        method_lines=lines[start:end]
        switch=next(i for i,x in enumerate(method_lines) if re.match(r"\s*284:\s+tableswitch",x))
        edges={}
        for x in method_lines[switch+1:]:
            if x.strip()=="}":break
            m=re.match(r"\s*(\d+|default):\s*(\d+)\s*$",x)
            require(m is not None,"unexpected switch value")
            edges[m[1]]=int(m[2])
        require(set(edges)=={str(i) for i in range(1,11)}|{"default"},"switch coverage")
        ann=[x.strip() for x in method_lines if "SubscribeEvent" in x or "RuntimeVisibleAnnotations:" in x or "priority=" in x or "receiveCanceled=" in x]
        selector=BASE+"server/block/ACBlockRegistry"
        sr=ClassReader(z.read(selector+".class"))
        sm=disassemble(jar,javap,selector)
        methods=[summarize(sr,key,value) for key,value in sorted(sm.items()) if key[0] in {"getBlockSupplier","blockItemProperties"}]
        require({m["declaration"]["name"] for m in methods}=={"getBlockSupplier","blockItemProperties"},"selector coverage")
        # Bootstrap methods resolve factory handles without inventing selector-to-block binding.
        boot=sr.attributes.get("bootstrap_methods",[])
        selected=[{"index":i,"bootstrap":m} for i,m in enumerate(boot) if any("lambda$getBlockSupplier$"+str(n) in json.dumps(m) for n in (437,438,439,445))]
        require(len(selected)==4,"factory bootstrap coverage")
        return {"anvil":{"class_sha256":digest(z.read(owner+".class")),"method":method,"switch_edges":edges,"annotation_lines":ann},"block_selector":{"class_sha256":digest(z.read(selector+".class")),"methods":methods,"factory_bootstraps":selected}}
def main():
    p=argparse.ArgumentParser()
    for k in ("jar","javap","output"):p.add_argument("--"+k,type=Path,required=True)
    a=p.parse_args()
    require(not a.output.exists(),"new report required")
    report={"scope":"DISCOVERY_NOT_CERTIFIED","native":inspect(a.jar,a.javap),"mutation":"NO_MUTATION"}
    a.output.write_text(canonical(report),encoding="utf8")
    print("EXTRA_SHA256",digest(a.output.read_bytes()))
    print("EXTRA_NATIVE",json.dumps(report["native"],sort_keys=True))
if __name__=="__main__":main()
