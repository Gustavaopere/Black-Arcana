#!/usr/bin/env python3
"""Official NeoForge 21.1.248 distributed-JVM denial guards, read-only.

Class SHA-pinned method references, conditions and return sites for UUID
registration and ServerLevel admission. Observes original --installServer
distribution only, NOT loaded ModLauncher, installed modpack or live behavior.
No third-party method bodies are copied. Discovery only, NO_MUTATION.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from zipfile import ZipFile

from alexscaves_1010_armor_material_audit import ClassReader, digest, require
from alexscaves_1010_enchantable_item_probe import disassemble
from neoforge_211248_gazing_pearl_saveddata_engine_probe import verify_distribution

PIN = {
    "ServerLevel": (
        "net/minecraft/server/level/ServerLevel",
        "19b42e51848fd27df3683dacf694baa5126ee9f0665f12afdc65f82493a1e5a3"),
    "PersistentEntitySectionManager": (
        "net/minecraft/world/level/entity/PersistentEntitySectionManager",
        "6351fcb7c7370b77b8d9618474783b58ab3e037c224b5c83481c23908db1fbf4"),
}
METHODS = {
    "ServerLevel": {"addEntity"},
    "PersistentEntitySectionManager":
        {"addEntity", "addEntityWithoutEvent", "addEntityUuid"},
}
PINNED_CODE = {
    ("ServerLevel", "addEntity"):
        "90b05c8f3b8b3044c50d7010fcba7d618fc3972c7216f926aac33028f2975243",
    ("PersistentEntitySectionManager", "addEntity"):
        "c12cfbffb16e15950de4caf3fd5785350b920540c24aed54e3160c9b3f771c7c",
    ("PersistentEntitySectionManager", "addEntityWithoutEvent"):
        "f616e8ec0dd0bcbb1ab3ff9425e9659f41af1d9dbc94f8faf4a255c96b7c5454",
}
SELECT_OPS = {
    "invokevirtual", "invokestatic", "invokeinterface", "invokespecial",
    "getfield", "putfield", "getstatic", "putstatic",
}


def refs(reader: ClassReader, body: dict) -> list[dict]:
    result = []
    for at, (op, arg, _) in sorted(body.items()):
        if op not in SELECT_OPS:
            continue
        candidate = re.match(r"#(\d+)(?:\s|,|$)", arg)
        require(candidate is not None, "no constant pool index for invoked member")
        cp_index = int(candidate.group(1))
        require(0 < cp_index < len(reader.pool), "invalid JVM ref index")
        tag = reader.pool[cp_index][0]
        require(tag in (9, 10, 11), "unexpected member reference kind")
        _, owner, name_and_desc = reader.resolve(cp_index)
        _, name, desc = name_and_desc
        result.append({"offset":at, "opcode":op, "cp_index":cp_index,
                       "owner":owner, "name":name, "descriptor":desc})
    require(len(result) <= 180, "bounded typed member census")
    return result


def analyze(reader: ClassReader, body: dict, decl: dict) -> dict:
    require(0 < len(body) <= 1600 and
            len(decl.get("exception_handlers", [])) <= 30, "method budget")
    offsets = sorted(body)
    branches, terminals = [], []
    for i, at in enumerate(offsets):
        op, arg, _ = body[at]
        if op.startswith("if") or op in ("goto", "goto_w"):
            target_text = arg.split()[0]
            require(target_text.lstrip("-").isdigit(), "unresolved branch target")
            target = int(target_text)
            require(target in body, "branch target not a JVM instruction")
            prior = offsets[max(0, i-5):i]
            # No source text: opcode-only prelude, plus separate typed members.
            branches.append({
                "offset":at, "opcode":op, "target":target,
                "fallthrough":offsets[i+1] if op.startswith("if") and i+1<len(offsets) else None,
                "prelude_opcodes":[body[q][0] for q in prior],
                "prelude_offsets":prior,
            })
        elif op.endswith("return") or op=="athrow":
            terminals.append({
                "offset":at, "opcode":op,
                "previous_opcode":body[offsets[i-1]][0] if i else None,
            })
    require(len(branches) <= 90 and len(terminals) <= 30,
            "branch/return budget")
    result = {
        "name":decl["name"],"descriptor":decl["descriptor"],
        "code_sha256":decl["code_sha256"],"code_bytes":decl["code_size"],
        "instruction_count":len(body),
        "branches":branches, "terminals":terminals,
        "typed_members":refs(reader,body),
        "exception_handler_count":len(decl.get("exception_handlers", [])),
    }
    return result


def scan(server: Path, srg: Path, javap: str) -> dict:
    verified=verify_distribution(server,srg)
    with ZipFile(server) as archive:
        names=archive.namelist()
        require(len(names)==len(set(names)), "duplicate server zip member")
        raw={k:archive.read(owner+".class") for k,(owner,_) in PIN.items()}
    classpath=str(server)+":"+str(srg)
    classes={}
    for key,(owner,expected_sha) in PIN.items():
        data=raw[key]
        require(digest(data)==expected_sha,"publisher class SHA changed "+key)
        reader=ClassReader(data)
        require(reader.name==owner and reader.major==65,
                "JVM owner/Java-version mismatch")
        parsed=disassemble(classpath,javap,owner)
        methods={}
        for name in sorted(METHODS[key]):
            declarations=[m for m in reader.methods
                          if m["name"]==name and "code_sha256" in m]
            require(len(declarations)<=1, "overloaded target needs separate scope")
            if not declarations:
                methods[name]={"present":False,
                    "method_name":name,"not_found_in_declared_executable_methods":True}
                continue
            decl=declarations[0]
            k=(name,decl["descriptor"])
            require(k in parsed and parsed[k],
                    "missing disassembly for executable owner method")
            if (key,name) in PINNED_CODE:
                require(decl["code_sha256"]==PINNED_CODE[(key,name)],
                        "established Code SHA changed")
            methods[name]={"present":True,**analyze(reader,parsed[k],decl)}
        classes[key]={
            "class_sha256":expected_sha,"owner":owner,
            "source":"NEOFORGE_211248_SERVER_OVERLAY_UNTRANSFORMED",
            "methods":methods,
        }
    return {
        "schema":1,
        "scope":"GALENA_NEOFORGE_211248_DISTRIBUTED_DENIAL_GUARD_DISCOVERY_ONLY",
        "artifact":verified,
        "classes":classes,
        "limits":{
            "stack_consumption_order":"PUBLISHER_CALL_ORDER_ONLY",
            "minecraft_modlauncher_classes":"NOT_OBSERVED",
            "real_warehouse_inventory":"NOT_TESTED",
            "runtime_spawn_denial":"NOT_VERIFIED",
            "uuid_duplicate_scenario":"NOT_TESTED",
            "world_protection":"NOT_VERIFIED",
            "all_denial_causes_exhausted":False,
            "galena_static_contract":"NOT_CERTIFIED",
            "mutating_hook":"NOT_VERIFIED",
            "physical_qa":"NOT_TESTED",
            "mutation":"NO_MUTATION",
            "provider_universe_closed":False,
            "semantic_magic_roots_delta":0,
        },
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--server",type=Path,required=True)
    p.add_argument("--srg",type=Path,required=True)
    p.add_argument("--javap",required=True)
    p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    require(args.output.suffix==".json" and not args.output.exists(),
            "report must be write-once JSON")
    result=scan(args.server,args.srg,args.javap)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    raw=(json.dumps(result,sort_keys=True,ensure_ascii=False,indent=2)+"\n").encode()
    require(len(raw)<=110_000,"output budget")
    args.output.write_bytes(raw)
    print("REPORT_SHA256",hashlib.sha256(raw).hexdigest(),"BYTES",len(raw))
    for key,entry in result["classes"].items():
        print("OWNER",key,entry["class_sha256"])
        for name,m in entry["methods"].items():
            if not m["present"]:
                print("METHOD_ABSENT",key,name)
                continue
            print("METHOD",key,name,m["descriptor"],m["code_sha256"],
                  "BRANCHES",len(m["branches"]),"RETURNS",len(m["terminals"]),
                  "MEMBERS",len(m["typed_members"]))
            for call in m["typed_members"]:
                print("REF",key,name,call["offset"],call["opcode"],
                      call["owner"],call["name"],call["descriptor"])
    print("DISCOVERY_ONLY NO_MUTATION NO_PHYSICAL_QA")


if __name__=="__main__":
    main()
