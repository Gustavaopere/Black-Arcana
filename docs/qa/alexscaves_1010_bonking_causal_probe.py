#!/usr/bin/env python3
"""Read-only SHA-exact Bonking LivingDeathEvent causal branch and loot bridge audit.

Verifies full native method identity, loop edges and branches against the 1.0.10
publisher JAR and the preceding exact resource / selected-window manifest.
Records symbolic references and exception-table metadata only: not game code,
not executed damage/loot, not live Mixin application, not a mutating hook.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path
from alexscaves_1010_damage_consumer_probe import BASE,SHA1,SHA256,SIZE,sha_file,javap,parse_methods
from alexscaves_1010_bonking_probe import only_method,choose_event,inspect_mixin,require
from alexscaves_1010_raygun_local_flow_probe import digest_method

EVENT=BASE+"server/event/CommonEvents.class"
MIXIN=BASE+"mixin/MobMixin.class"
PIVOTS={
    97:("ifeq","432"),110:("ifnull","432"),
    117:("invokevirtual","getDirectEntity"),
    127:("ifeq","432"),143:("getstatic","PRIMITIVE_CLUB"),
    157:("ifeq","432"),167:("getstatic","BONKING"),
    170:("invokestatic","enchantLevel"),173:("ifle","432"),
    183:("invokevirtual","getRandom"),186:("invokeinterface","nextFloat"),
    191:("ldc","0.33"),194:("ifge","432"),
    197:("getstatic","CREEPER"),204:("invokestatic","createEntity"),
    214:("ifnull","432"),231:("ifeq","274"),
    241:("getstatic","LIGHTNING_BOLT"),246:("invokestatic","createEntity"),
    256:("ifnull","274"),262:("invokevirtual","setVisualOnly"),
    271:("invokevirtual","thunderHit"),283:("invokevirtual","mobAttack"),
    303:("invokestatic","EquipmentSlot.values"),
    320:("if_icmpge","366"),338:("invokeinterface","ac_getEquipmentDropChance"),
    346:("invokevirtual","HashMap.put"),
    354:("fconst_0",""),355:("invokeinterface","ac_setDropChance"),
    363:("goto","316"),372:("invokeinterface","ac_dropCustomDeathLoot"),
    377:("invokestatic","EquipmentSlot.values"),
    394:("if_icmpge","432"),412:("invokevirtual","HashMap.get"),
    418:("invokevirtual","Float.floatValue"),
    421:("invokeinterface","ac_setDropChance"),
    429:("goto","390")
}
BRANCH_OPS=("if","goto")
REF_OPS=("invoke","getstatic","putstatic","getfield","putfield")
CHECKED_METHOD_DESC="(Lnet/neoforged/neoforge/event/entity/living/LivingDeathEvent;)V"

def sha(raw):
    return hashlib.sha256(raw).hexdigest()
def strict_pairs(pairs):
    out={}
    for k,v in pairs:
        require(k not in out,"duplicate JSON key "+k)
        out[k]=v
    return out
def select_consumer(methods):
    m=choose_event(methods)
    require(m["descriptor"]==CHECKED_METHOD_DESC and len(m["instructions"])==229,
            "unexpected death event handler version")
    return m
def validate_pivots(method):
    rows=method["instructions"]
    off=[x["offset"] for x in rows]
    require(off==sorted(set(off)),"offset order/uniqueness")
    by={x["offset"]:x for x in rows}
    for o,(op,marker) in PIVOTS.items():
        row=by.get(o)
        require(row and row["opcode"]==op and marker in
                (row["symbol"]+" "+row["operand"]),
                "missing exact Bonking pivot at "+str(o))
    return [dict(offset=o,opcode=by[o]["opcode"],
                 operand=by[o]["operand"],symbol=by[o]["symbol"]) for o in sorted(PIVOTS)]
def branch_edges(method):
    rows=method["instructions"]
    offsets=[x["offset"] for x in rows]
    by={x["offset"]:idx for idx,x in enumerate(rows)}
    require(len(by)==len(rows),"duplicate branches")
    edges=[]
    for i,x in enumerate(rows):
        op=x["opcode"]
        if op in ("tableswitch","lookupswitch","jsr","jsr_w","ret"):
            raise ValueError("unsupported JVM control primitive")
        if not op.startswith(BRANCH_OPS):
            continue
        word=x["operand"].split()[0] if x["operand"] else ""
        require(word.lstrip("-").isdigit(),"unresolved branch operand @"+str(x["offset"]))
        target=int(word)
        require(target in by,"invalid JVM branch target @"+str(x["offset"]))
        e={"offset":x["offset"],"opcode":op,"target":target,
           "back_edge":target<=x["offset"]}
        if op.startswith("if"):
            require(i+1<len(rows),"conditional branch at end of method")
            e["fallthrough"]=rows[i+1]["offset"]
        edges.append(e)
    require(len(edges)<=70,"unbounded JVM branch graph")
    return edges
def extract_exception_table(raw,method_name):
    lines=raw.splitlines()
    starts=[i for i,s in enumerate(lines) if s.startswith("  ") and
            not s.startswith("    ") and (method_name+"(") in s and s.strip().endswith(";")]
    require(len(starts)==1,"method boundary ambiguous")
    start=starts[0]
    end=next((i for i in range(start+1,len(lines)) if
              lines[i].startswith("  ") and not lines[i].startswith("    ") and
              (lines[i].strip().endswith(";") and "(" in lines[i])),len(lines))
    segment=lines[start:end]
    table=[i for i,s in enumerate(segment) if s.strip()=="Exception table:"]
    require(len(table)<=1,"ambiguous exception table")
    if not table:return {"declared_exception_handlers":0,"entries":[]}
    # javap -c prints a header and 'from to target type' rows, where the
    # optional type can be "any"; keep only numeric metadata.
    entries=[]
    for line in segment[table[0]+1:]:
        if re.match(r"^\s*from\s+to\s+target\s+type",line):continue
        m=re.match(r"^\s*(\d+)\s+(\d+)\s+(\d+)\s+(.*)$",line)
        if not m:break
        begin,finish,handler,kind=m.groups()
        entries.append({"start":int(begin),"end_exclusive":int(finish),
                        "handler":int(handler),"kind":kind.strip()})
    require(len(entries)<=24,"exception table exceeds bounds")
    return {"declared_exception_handlers":len(entries),"entries":entries}
def discover_mixin_declarations(archive):
    declarations=[]
    for name in sorted(archive.namelist()):
        if not name.endswith(".json") or "mixin" not in name.lower():continue
        raw=archive.read(name)
        if b"MobMixin" not in raw or len(raw)>100000:continue
        cfg=json.loads(raw,object_pairs_hook=strict_pairs)
        if not isinstance(cfg,dict):continue
        references=[]
        for scope in ("mixins","client","server"):
            val=cfg.get(scope,[])
            if isinstance(val,list) and "MobMixin" in val:references.append(scope)
        declarations.append({"path":name,"sha256":sha(raw),
                             "package":cfg.get("package"),"entries_in":references})
    require(len(declarations)<=12,"unbounded Mixin configuration census")
    return declarations
def audit(jar:Path,manifest:Path,javap_bin:str):
    require(jar.is_file() and sha_file(jar)==(SHA1,SHA256,SIZE),
            "wrong publisher exact JAR")
    parent=json.loads(manifest.read_text(encoding="utf8"),object_pairs_hook=strict_pairs)
    require(parent["artifact"]=={"sha1":SHA1,"sha256":SHA256,"size_bytes":SIZE},
            "parent Bonking manifest from wrong JAR")
    with zipfile.ZipFile(jar) as z:
        paths=z.namelist()
        require(len(paths)==len(set(paths)),"duplicate ZIP member")
        hashes={name:sha(z.read(name)) for name in (EVENT,MIXIN)}
        expected={row["path"]:row["sha256"] for row in parent["classes"]}
        require(all(expected.get(k)==v for k,v in hashes.items()),
                "Bonking event / Mixin class SHA mismatch")
        mixin_config=discover_mixin_declarations(z)
    raw=javap(javap_bin,jar,EVENT[:-6].replace("/","."))
    methods=parse_methods(raw)
    consumer=select_consumer(methods)
    require(digest_method(consumer)==parent["death_consumer"]["parsed_method_sha256"],
            "Bonking death method digest drift")
    expectedBridge={b["name"]:b["parsed_method_sha256"] for b in parent["loot_bridge"]}
    mixinMethods=parse_methods(javap(javap_bin,jar,MIXIN[:-6].replace("/",".")))
    bridges=inspect_mixin(mixinMethods)
    require(all(expectedBridge.get(b["name"])==b["parsed_method_sha256"]
                for b in bridges),"loot bridge method digest drift")
    edge=branch_edges(consumer)
    require(all(any(e["offset"]==o and e["target"]==432 for e in edge)
                for o in (97,110,127,157,173,194,214)),
            "missing death/club/enchant/RNG preconditions")
    require(any(e["offset"]==363 and e["target"]==316 for e in edge) and
            any(e["offset"]==429 and e["target"]==390 for e in edge),
            "expected backup and restore slot loops absent")
    pivots=validate_pivots(consumer)
    return {
      "schema_version":1,
      "scope":"BONKING_FULL_NATIVE_DEATH_HANDLER_BRANCHES_AND_LOOT_BRIDGE",
      "source":"EXACT_INSTALLED_ALEXSCAVES_CONTINUED_1.0.10",
      "artifact":parent["artifact"],
      "classes":hashes,
      "parent_manifest_sha256":sha(manifest.read_bytes()),
      "method":{"class":EVENT,"name":"livingDie",
         "descriptor":consumer["descriptor"],
         "parsed_method_sha256":digest_method(consumer),
         "instruction_count":len(consumer["instructions"]),
         "total_declared_event_methods":len(methods),
         "all_branch_edges":edge,
         "selected_bonking_pivots":pivots,
         "exception_table":extract_exception_table(raw,"livingDie"),
         "post_bonking_region":"@432+ includes independent death event consumers; NOT_ATTRIBUTED_TO_BONKING"},
      "mixin_declarations":mixin_config,
      "loot_bridge":[{"name":b["name"],"descriptor":b["descriptor"],
                       "method_sha256":b["parsed_method_sha256"],
                       "instruction_count":b["instruction_count"]}
                      for b in bridges],
      "limits":{
        "reconstructed_executed_cfg":"NOT_VERIFIED",
        "damage_source_acceptance":"NOT_VERIFIED",
        "live_mixin_application_order":"NOT_VERIFIED",
        "drop_probabilities_and_loot_tables":"NOT_CERTIFIED",
        "equipment_drop_chance_exception_safety":"NOT_CERTIFIED",
        "physical_qa":"NOT_TESTED",
        "safe_mutating_hook":"NOT_VERIFIED",
        "static_certification":"PARTIAL",
        "mutation":"NO_MUTATION"
      }
    }
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--jar",required=True,type=Path)
    ap.add_argument("--manifest",required=True,type=Path)
    ap.add_argument("--snapshot",type=Path)
    ap.add_argument("--output",type=Path)
    ap.add_argument("--javap",default="javap")
    args=ap.parse_args()
    out=audit(args.jar,args.manifest,args.javap)
    if args.snapshot:
        saved=json.loads(args.snapshot.read_text(encoding="utf8"),object_pairs_hook=strict_pairs)
        require(saved==out,"BONKING CAUSAL SNAPSHOT DRIFT")
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n",encoding="utf8")
    if not args.snapshot:
        print("BONKING_CAUSAL_DISCOVERY_JSON="+json.dumps(out,separators=(",",":"),ensure_ascii=False))
    print("BONKING_CAUSAL_STATUS","SEALED" if args.snapshot else "DISCOVERY",
          "INSTRUCTIONS",out["method"]["instruction_count"],
          "BRANCHES",len(out["method"]["all_branch_edges"]),
          "MIXIN_CONFIGS",len(out["mixin_declarations"]),"NO_MUTATION")
if __name__=="__main__":
    main()
