#!/usr/bin/env python3
"""SHA-exact read-only discovery of ACEnchantableItem.
No provider classes are loaded; no enchantment, hook or physical QA is executed.
The candidate roster is derived from declared interface signatures, not upstream
source or name inference. External evidence is separately version-pinned.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re
import subprocess
import zipfile

from alexscaves_1010_armor_material_audit import (
    ClassReader, canonical, digest, require, rows, verify_artifact, SHA1, SHA256, SIZE,
)
from alexscaves_1010_action_contract_audit import parse_javap
from alexscaves_1010_destroyed_item_engine_reference import (
    verify_artifact as verify_engine, ARTIFACTS,
)

PREFIX = "com/github/alexmodguy/alexscaves/"
TARGET = PREFIX + "server/item/ACEnchantableItem"
REGISTRY = PREFIX + "server/item/ACItemRegistry"
ENGINE_OWNERS = (
    "net/neoforged/neoforge/common/extensions/IItemExtension",
    "net/neoforged/neoforge/common/extensions/IItemStackExtension",
    "net/neoforged/neoforge/common/CommonHooks",
)
PATCH_BASENAMES = {"Item.java.patch", "ItemStack.java.patch",
                   "EnchantmentMenu.java.patch", "EnchantmentHelper.java.patch",
                   "AnvilMenu.java.patch"}


def disassemble(jar, javap, owner):
    result = subprocess.run(
        [str(javap), "-classpath", str(jar), "-p", "-c", "-s", owner.replace("/", ".")],
        capture_output=True, text=True, check=False, timeout=90)
    require(result.returncode == 0, "javap failed: " + owner + " "+result.stderr[:250])
    return parse_javap(result.stdout, owner)


def summarize(reader, key, body):
    decl = [m for m in reader.methods if (m["name"], m["descriptor"]) == key]
    require(len(decl) == 1, "declaration not unique: " + str(key))
    return {"declaration": decl[0], "instruction_count": len(body),
            "instruction_sha256": digest(canonical(rows(body)).encode()),
            "instructions": rows(body)}


def member_refs(reader, names, signatures):
    results = []
    for i, entry in enumerate(reader.pool):
        if entry is None or entry[0] not in (10,11):
            continue
        tag, owner, signature = reader.resolve(i)
        _, name, descriptor = signature
        if owner == TARGET or name in names:
            results.append({"index":i, "kind":"Methodref" if tag==10 else "InterfaceMethodref",
                            "owner":owner, "name":name, "descriptor":descriptor,
                            "exact_interface_signature":(name,descriptor) in signatures})
    return results


def inherits(owner, hierarchy, chain=()):
    if owner == TARGET:
        return True
    require(owner not in chain, "cycle in class hierarchy")
    data = hierarchy.get(owner)
    return bool(data and any(inherits(parent,hierarchy,(*chain,owner))
                       for parent in [data["parent"],*data["interfaces"]] if parent))


def callsites(parsed, signatures):
    output = []
    pattern = re.compile(r"(?:InterfaceMethod|Method) (?:[^ ]+\.)?([^.: ]+):(\([^ ]+\)[^ ]+)")
    for (method, descriptor), body in sorted(parsed.items()):
        for offset,(op,operand,symbol) in sorted(body.items()):
            if not op.startswith("invoke"):
                continue
            match = pattern.search(symbol)
            if match and (match.group(1),match.group(2)) in signatures:
                output.append({"method":method,"descriptor":descriptor,"offset":offset,
                               "opcode":op,"symbol":symbol})
    return output


def native(jar,javap):
    verify_artifact(jar)
    with zipfile.ZipFile(jar) as z:
        paths=z.namelist()
        require(len(paths)==len(set(paths)),"duplicate ZIP entries")
        class_paths=sorted(p for p in paths if p.endswith(".class"))
        require(len(class_paths)==1555,"class roster drift")
        raw=z.read(TARGET+".class")
        target=ClassReader(raw)
        require(target.access & 512,"target not interface")
        signatures={(m["name"],m["descriptor"]) for m in target.methods}
        names={n for n,_ in signatures}
        require(len(signatures)<=12,"unexpected declared API size")
        hierarchy={}
        census={}
        refs={}
        decls={}
        for path in class_paths:
            reader=ClassReader(z.read(path))
            require(path==reader.name+".class" and reader.major==65,"class identity drift")
            hierarchy[reader.name]={"parent":reader.parent,"interfaces":reader.interfaces,
                                    "access":reader.access}
            typed=reader.typed_refs(TARGET)
            if typed:
                census[reader.name]=typed
            methods=member_refs(reader,names,signatures)
            if methods:
                refs[reader.name]=methods
            declared=[m for m in reader.methods if m["name"] in names]
            if declared:
                decls[reader.name]=declared
        direct=sorted(o for o,h in hierarchy.items() if o!=TARGET and TARGET in h["interfaces"])
        inherited=sorted(o for o in hierarchy if o!=TARGET and o not in direct
                         and inherits(o,hierarchy))
        owners=sorted({TARGET,*direct,*inherited,*refs,*decls})
        require(len(owners)<=100,"candidate roster exceeds discovery budget")
        bodies={}
        calls={}
        for owner in owners:
            raw=z.read(owner+".class")
            reader=ClassReader(raw)
            parsed=disassemble(jar,javap,owner) if any("code_sha256" in m for m in reader.methods) else {}
            selected=[summarize(reader,k,v) for k,v in sorted(parsed.items())
                      if k[0] in names and any((m["name"],m["descriptor"])==k and "code_sha256" in m
                                              for m in reader.methods)]
            declared=[m for m in reader.methods if m["name"] in names]
            for m in declared:
                if "code_sha256" in m:
                    require(any(v["declaration"]["name"]==m["name"] and v["declaration"]["descriptor"]==m["descriptor"]
                                for v in selected),"missing coded method at "+owner)
            bodies[owner]={"class_sha256":digest(raw),"hierarchy":hierarchy[owner],
                           "declared_methods":declared,"methods":selected}
            sites=callsites(parsed,signatures)
            if sites:
                calls[owner]=sites
        # Constructor references and exact bootstrap handles, separate from actual
        # registry execution. Classes in other registry owners are not assumed.
        reader=ClassReader(z.read(REGISTRY+".class"))
        parsed=disassemble(jar,javap,REGISTRY)
        relevant=set(direct+inherited)
        factories=[]
        for key,body in sorted(parsed.items()):
            if key[0]=="<clinit>":
                continue
            matches=[]
            for offset,(op,operand,symbol) in sorted(body.items()):
                if op=="new" and symbol.startswith("class ") and symbol[6:] in relevant:
                    matches.append({"offset":offset,"owner":symbol[6:]})
            if matches:
                factories.append({"name":key[0],"descriptor":key[1],"new_owners":matches,
                                  "instruction_count":len(body),
                                  "instruction_sha256":digest(canonical(rows(body)).encode())})
        names_and_desc={(r["name"],r["descriptor"]) for r in factories}
        clinit=parsed[("<clinit>","()V")]
        offsets=sorted(clinit)
        windows=[]
        for offset,(_,_,symbol) in sorted(clinit.items()):
            match=re.search(r"InvokeDynamic #(\d+):",symbol)
            if not match:
                continue
            idx=int(match.group(1))
            bs=reader.attributes.get("bootstrap_methods",[])
            require(idx<len(bs),"bootstrap index outside table")
            handles=[]
            for arg in bs[idx]["arguments"]:
                if not isinstance(arg,dict):
                    continue
                ref=arg.get("reference")
                if isinstance(ref,list) and len(ref)==3 and ref[1]==REGISTRY and (
                        ref[2][1],ref[2][2]) in names_and_desc:
                    handles.append({"name":ref[2][1],"descriptor":ref[2][2]})
            if handles:
                i=offsets.index(offset)
                windows.append({"offset":offset,"handles":handles,
                                "window":rows({p:clinit[p] for p in offsets[max(0,i-3):i+4]})})
        return {"class_entries_scanned":len(class_paths),
                "class_roster_sha256":digest(("\n".join(class_paths)+"\n").encode()),
                "target":TARGET,"target_class_sha256":digest(z.read(TARGET+".class")),
                "target_fields":target.fields,"target_methods":target.methods,
                "direct_implementers":direct,"inherited_implementers":inherited,
                "typed_reference_census":census,"member_references_by_name":refs,
                "owner_declarations_and_bodies":bodies,"exact_signature_callsites":calls,
                "registry":{"owner":REGISTRY,"class_sha256":digest(z.read(REGISTRY+".class")),
                            "constructor_factories":factories,"clinit_bootstrap_windows":windows,
                            "boundary":"ACItemRegistry only; no registry execution"}}


def engine(universal,userdev,javap,names):
    verify_engine(universal,"universal")
    verify_engine(userdev,"userdev")
    owners={}
    # The stack-aware overloads may not have the same descriptor as provider
    # declarations; match by exact method name and report actual descriptors.
    with zipfile.ZipFile(universal) as z:
        for owner in ENGINE_OWNERS:
            raw=z.read(owner+".class")
            reader=ClassReader(raw)
            parsed=disassemble(universal,javap,owner)
            selected=[summarize(reader,k,v) for k,v in sorted(parsed.items()) if k[0] in names]
            owners[owner]={"class_sha256":digest(raw),
                           "declared_methods":[m for m in reader.methods if m["name"] in names],
                           "methods":selected}
    patches=[]
    matcher=re.compile(r"\b(?:"+"|".join(re.escape(n) for n in sorted(names))+
                       r"|getEnchantmentValue|isEnchantable|canApplyAtEnchantingTable|supportsEnchantment)\b")
    with zipfile.ZipFile(userdev) as z:
        for path in sorted(p for p in z.namelist() if p.startswith("patches/") and Path(p).name in PATCH_BASENAMES):
            raw=z.read(path)
            patches.append({"entry":path,"sha256":digest(raw),
                            "matching_lines":[{"line":i+1,"text":line} for i,line in enumerate(raw.decode("utf8").splitlines())
                                              if matcher.search(line)]})
    return {"version":"21.1.250","artifacts":ARTIFACTS,"universal":owners,"patches":patches,
            "boundary":"official upstream pinned reference, not installed transformed runtime"}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for name in ("jar","universal","userdev","javap","output"):
        p.add_argument("--"+name,type=Path,required=True)
    a=p.parse_args()
    require(not a.output.exists() and a.output.suffix==".json","new JSON required")
    data=native(a.jar,a.javap)
    names={m["name"] for m in data["target_methods"]}
    require(bool(names),"no interface API; inspect marker disposition separately")
    result={"schema":"AC_ENCHANTABLE_ITEM_DISCOVERY_V1","scope":"DISCOVERY_NOT_CERTIFIED",
            "artifact":{"version":"1.0.10","sha1":SHA1,"sha256":SHA256,"size_bytes":SIZE},
            "publisher":data,"engine":engine(a.universal,a.userdev,a.javap,names),
            "mutation":"NO_MUTATION","mutating_hook":"NOT_VERIFIED","physical_qa":"NOT_TESTED",
            "provider_universe_closed":False}
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(canonical(result),encoding="utf8")
    print("REPORT_SHA256",digest(a.output.read_bytes()))
    print("TARGET",data["target"],data["target_class_sha256"],json.dumps(data["target_methods"]))
    print("DIRECT",json.dumps(data["direct_implementers"]))
    print("INHERITED",json.dumps(data["inherited_implementers"]))
    print("TYPED_OWNERS",json.dumps(sorted(data["typed_reference_census"])))
    print("MEMBER_REFS",json.dumps(data["member_references_by_name"]))
    print("CALLSITES",json.dumps(data["exact_signature_callsites"]))
    for owner,entry in data["owner_declarations_and_bodies"].items():
        print("OWNER",owner,entry["class_sha256"],json.dumps(entry["hierarchy"]))
        for d in entry["declared_methods"]:
            print("DECLARATION",json.dumps(d))
        for m in entry["methods"]:
            print("METHOD",m["declaration"]["name"],m["declaration"]["descriptor"],m["instruction_count"])
            for r in m["instructions"]:
                print(" ",r["offset"],r["opcode"],r["operand"],r["symbol"])
    print("FACTORIES",json.dumps(data["registry"]["constructor_factories"]))
    for w in data["registry"]["clinit_bootstrap_windows"]:
        print("REGISTRY_WINDOW",json.dumps(w))
    for owner,entry in result["engine"]["universal"].items():
        print("ENGINE_OWNER",owner,entry["class_sha256"])
        for m in entry["methods"]:
            print("ENGINE_METHOD",m["declaration"]["name"],m["declaration"]["descriptor"],json.dumps(m["instructions"]))
    for patch in result["engine"]["patches"]:
        print("ENGINE_PATCH",patch["entry"],patch["sha256"],json.dumps(patch["matching_lines"]))
    print("END_ENCHANTABLE_DISCOVERY NO_MUTATION")


if __name__=="__main__":
    main()
