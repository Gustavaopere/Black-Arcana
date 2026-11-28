#!/usr/bin/env python3
"""Publisher-exact read-only discovery for Primordial Soup feeding callbacks.
No provider execution, transformed runtime claim, or static certificate.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from zipfile import ZipFile

from alexscaves_1010_armor_material_audit import ClassReader, canonical, digest, require, verify_artifact, SHA1, SHA256, SIZE
from alexscaves_1010_enchantable_item_probe import disassemble
from alexscaves_1010_four_items_downstream_250_probe import projection

P = "com/github/alexmodguy/alexscaves/server/"
IR = P + "item/ACItemRegistry"
ITEM = P + "item/PrehistoricMixtureItem"
FOODS = P + "item/ACFoods"
COMPAT = P + "misc/ACCompat"
ID = "alexscaves:primordial_soup"
ROSTER_SHA = "2296d31ecc7fabb375922b8ad23c7a25c3e969bdfd80d5e1aa602034ae5d62ed"
PINS = {
    IR: "114e4a3576d56cb66d240fa9df9db7693b1df576ebfa86631ef751dd1e7b5bb1",
    ITEM: "53a9a6fde7af563cc592bd05d081813bf22c3f0b628e83fb03ae7079b0cc1d56",
    FOODS: "a52ec981fe51c97003383a46f7c0b2de06baa5e3ca3f73db988655abce51e12e",
    COMPAT: "333738f324e6e9d77a488e14b7e81b169c2b2d4f6db5171206a016ad0271f57b",
}
FACTORY = ("lambda$static$37", "()Lnet/minecraft/world/item/Item;")
CODE_PINS = {
    (IR, FACTORY[0]): "5814d536831c0df71d18745af3571e2420a7881043c4011999201da8e21dc26e",
    (ITEM, "interactLivingEntity"): "502e616a07cf5867ab58bc1ffa79ab16a505a4ddd847b144f7628a06b85c70a9",
    (ITEM, "finishUsingItem"): "92ba9838f2a3397d4111ee8c2eaf6277710f63ba8c45c7054eb52cbb3f70f890",
    (ITEM, "canFeedMob"): "7fefc60255a63f0ded862e18e81e95d91de0bf529e1bf645f440b6785cc68f69",
}
RECIPE = "data/alexscaves/recipe/primordial_soup.json"
RECIPE_SHA = "02968ed3e6687885654aab4e93562f63a814bb6fbcc830cfcb099bc9a65bfb31"
CALLBACK = "onFeedMixture"
STATE_METHODS = {"getPushingTreesFor", "setPushingTreesFor"}
LIMITS = {"static_contract": "NOT_CERTIFIED", "mutating_hook": "NOT_VERIFIED",
          "physical_qa": "NOT_TESTED", "mutation": "NO_MUTATION",
          "semantic_magic_roots_delta": 0, "provider_universe_closed": False,
          "runtime_loaded_bytes": "NOT_OBSERVED",
          "scope": "PUBLISHER_FEEDING_CALLBACKS_AND_FOOD_CONTEXT",
          "food_initializer": "REUSED_EXISTING_CERTIFIED_FOODS_CLASS_NOT_REPROJECTED"}


# Exact member-name/descriptor census across the publisher, including inherited-owner references.
TIMER_MEMBERS = {("getPushingTreesFor","()I"),("setPushingTreesFor","(I)V"),
                 ("PUSHING_TREES_FOR","Lnet/minecraft/network/syncher/EntityDataAccessor;")}
RELICH = P+"entity/living/RelicheirusEntity"
def timer_ref(resolved):
    return (isinstance(resolved,list) and len(resolved)==3 and resolved[0] in (9,10,11)
            and isinstance(resolved[2],list) and tuple(resolved[2][1:]) in TIMER_MEMBERS)

def timer_census(z, roster, jar, javap):
    import re
    out={}
    for path in roster:
        raw=z.read(path);rd=ClassReader(raw)
        cp={i:rd.resolve(i) for i,v in enumerate(rd.pool) if v and v[0] in (9,10,11)}
        hits={i:v for i,v in cp.items() if timer_ref(v)}
        if not hits:continue
        sites=[]
        parsed=disassemble(jar,javap,rd.name)
        for key,body in sorted(parsed.items()):
            matched=[]
            for at,(op,arg,symbol) in sorted(body.items()):
                m=re.match(r"#(\d+)(?:\s|,|$)",arg)
                if m and int(m[1]) in hits:
                    matched.append({"offset":at,"opcode":op,"member":hits[int(m[1])]})
            if not matched:continue
            decl=next(d for d in rd.methods if (d["name"],d["descriptor"])==key)
            # Preserve every matching instruction, with bounded causal neighborhoods.
            # Large methods are not passed to the shared full-projection budget.
            offsets=sorted(body)
            for site in matched:
                pos=offsets.index(site["offset"])
                site["window"]=[{"offset":o,"opcode":body[o][0],"operand":body[o][1],"symbol":body[o][2]}
                                for o in offsets[max(0,pos-12):pos+13]]
            sites.append({"name":key[0],"descriptor":key[1],"code_sha256":decl["code_sha256"],
                          "instruction_count":len(body),"sites":matched})
        # Method handles can represent indirect references not reached by direct CP instructions.
        handles=[{"index":i,"handle":rd.resolve(i)} for i,v in enumerate(rd.pool)
                 if v and v[0]==15 and timer_ref(rd.resolve(i)["reference"])]
        out[rd.name]={"class_sha256":digest(raw),"parent":rd.parent,
                     "constant_pool_candidates":[[i,v] for i,v in sorted(hits.items())],
                     "direct_sites":sites,"method_handle_candidates":handles}
    require(RELICH in out and 1<=len(out)<=80,"timer census bounds")
    require(any(s["name"]=="onFeedMixture" for s in out[RELICH]["direct_sites"]),"known producer absent")
    require(any(s["name"]=="setPushingTreesFor" for s in out[RELICH]["direct_sites"]),"known setter absent")
    return out


GOAL=P+"entity/ai/RelicheirusPushTreesGoal"
GOAL_PINS={RELICH:"50ba008765f00653c630f9c8e4fd28ab45f8c7e97a054a9858995676f007651f",
           GOAL:"9307599bad3302757d4848a25eb74ded440b5bd127d981d234b36df2cbefc3c3"}
GOAL_CODES={(GOAL,"canUse","()Z"):"3495e712e9b5d7dc3955eb23727bc62b68cb2890a33f6b17cd7b03e563dfe458",
            (RELICH,"tick","()V"):"e2fbb728287e9f002a20db59869ff33a08d3ee1730b3d469eb4bf55bdb1c73aa"}
def goal_record(rd,key,body):
    import re
    decl=next(d for d in rd.methods if (d["name"],d["descriptor"])==key)
    require("code_sha256" in decl and 0<len(body)<=5000,"goal body budget "+str(key))
    ops=[]
    for at,(op,arg,symbol) in sorted(body.items()):
        m=re.match(r"#(\d+)(?:\s|,|$)",arg)
        ops.append({"offset":at,"opcode":op,"operand":arg,"symbol":symbol if m else "",
                    "constant":rd.resolve(int(m[1])) if m else None})
    return {"name":key[0],"descriptor":key[1],"code_sha256":decl["code_sha256"],
            "instruction_count":len(body),"instruction_sha256":digest(canonical(ops).encode()),
            "instructions":ops}

def inspect_goal(z,roster,jar,javap):
    entries=set(roster);classes={};selected={};cache={};observed=set()
    def reader(owner):
        require(owner+".class" in entries,"goal owner absent "+owner)
        if owner not in cache:
            raw=z.read(owner+".class");rd=ClassReader(raw)
            require(rd.name==owner and rd.major==65,"goal owner identity "+owner)
            cache[owner]=(rd,digest(raw))
        return cache[owner]
    def add(owner,key):
        rd,_=reader(owner)
        if any((d["name"],d["descriptor"])==key and "code_sha256" in d for d in rd.methods):
            selected.setdefault(owner,set()).add(key)
    for owner,sha in GOAL_PINS.items():
        rd,actual=reader(owner);require(actual==sha,"goal class pin "+owner)
        for d in rd.methods:
            name=d["name"]
            if owner==GOAL or name in {"registerGoals","tick","addAdditionalSaveData","readAdditionalSaveData","onFeedMixture","defineSynchedData"} or ("tree" in name.lower() or "push" in name.lower()):
                add(owner,(name,d["descriptor"]))
    # Exact provider-declared direct callee candidates from the goal's actual instructions.
    goal_rd,_=reader(GOAL)
    parsed=disassemble(jar,javap,GOAL)
    import re
    direct_calls=[]
    for key,body in sorted(parsed.items()):
        for at,(op,arg,_) in sorted(body.items()):
            m=re.match(r"#(\d+)(?:\s|,|$)",arg)
            if not m or not op.startswith("invoke") or op=="invokedynamic":continue
            v=goal_rd.resolve(int(m[1]))
            if not isinstance(v,list) or len(v)!=3 or v[0] not in (10,11):continue
            _,owner,nt=v
            if not owner.startswith(P) or owner+".class" not in entries:continue
            target=(nt[1],nt[2])
            add(owner,target)
            direct_calls.append({"caller":list(key),"offset":at,"owner":owner,
                                 "target":list(target),"declared_body_selected":target in selected.get(owner,set())})
    require(len(selected)<=25 and sum(map(len,selected.values()))<=100,"goal selection budget")
    for owner,keys in sorted(selected.items()):
        rd,sha=reader(owner)
        bodies=parsed if owner==GOAL else disassemble(jar,javap,owner)
        methods=[]
        for key in sorted(keys):
            require(key in bodies,"goal method missing "+owner+str(key))
            rec=goal_record(rd,key,bodies[key])
            pin=(owner,*key)
            if pin in GOAL_CODES:
                require(rec["code_sha256"]==GOAL_CODES[pin],"goal Code pin "+str(pin));observed.add(pin)
            methods.append(rec)
        if owner==GOAL:
            require(keys=={(d["name"],d["descriptor"]) for d in rd.methods if "code_sha256" in d},"goal executable roster")
        classes[owner]={"class_sha256":sha,"parent":rd.parent,"fields":rd.fields,
                        "declarations":rd.methods,"bootstrap_methods":rd.attributes.get("bootstrap_methods",[]),
                        "methods":methods}
    require(observed==set(GOAL_CODES),"goal Code pins not observed")
    return {"classes":classes,"direct_provider_callee_candidates":direct_calls}

def refs_json(value, path=()):
    if isinstance(value, dict):
        for k, v in sorted(value.items()):
            if k == ID:
                yield [list(path+(k,)), "KEY", k]
            yield from refs_json(v, path+(k,))
    elif isinstance(value, list):
        for i, v in enumerate(value):
            yield from refs_json(v, path+(i,))
    elif value == ID:
        yield [list(path), "VALUE", value]

def inspect(jar, javap):
    verify_artifact(jar)
    with ZipFile(jar) as z:
        names = z.namelist()
        roster = sorted(p for p in names if p.endswith(".class"))
        require(len(names) == len(set(names)) and len(roster) == 1555, "publisher roster")
        require(digest(("\n".join(roster)+"\n").encode()) == ROSTER_SHA, "roster hash")
        readers, class_hashes = {}, {}
        declarations, selected = [], {}
        for path in roster:
            raw = z.read(path)
            rd = ClassReader(raw)
            owner = rd.name
            require(owner+".class" == path and rd.major == 65, "class identity "+path)
            class_hashes[owner] = digest(raw)
            if owner in PINS:
                require(class_hashes[owner] == PINS[owner], "class pin "+owner)
            methods = [d for d in rd.methods if d["name"] == CALLBACK]
            if methods:
                declarations.append({"owner": owner, "parent": rd.parent, "methods": methods})
            keys = set()
            for d in rd.methods:
                name, desc = d["name"], d["descriptor"]
                if (name == CALLBACK or
                    name in STATE_METHODS or
                    (owner == IR and (name,desc) == FACTORY) or
                    (owner == ITEM) or
                    (owner == COMPAT and name in {"food", "foodEffects"})):
                    if "code_sha256" in d:
                        keys.add((name,desc))
            if keys:
                readers[owner] = rd
                selected[owner] = keys
        require(set(PINS) <= set(class_hashes), "required class pins")
        require(set(PINS)-{FOODS} <= set(readers), "required projected owners")
        require(any(d["owner"].endswith("/DinosaurEntity") for d in declarations), "base callback declaration")
        require(any(name == "getPushingTreesFor" for keys in selected.values() for name,_ in keys), "state getter")
        require(len(selected) <= 50 and sum(map(len,selected.values())) <= 150, "projection scope")
        projected, observed_pins = [], set()
        for owner in sorted(selected):
            rd = readers[owner]
            parsed = disassemble(jar,javap,owner)
            for key in sorted(selected[owner]):
                decl = [d for d in rd.methods if (d["name"],d["descriptor"]) == key]
                require(len(decl) == 1 and key in parsed, "exact method "+str(key))
                require(0 < len(parsed[key]) <= 5000, "method budget "+str(key))
                pin = (owner,key[0])
                if pin in CODE_PINS:
                    require(decl[0]["code_sha256"] == CODE_PINS[pin], "Code pin "+str(pin))
                    observed_pins.add(pin)
                print("PROJECT_METHOD", owner, *key, flush=True)
                projected.append({"owner": owner, "class_sha256": class_hashes[owner],
                                  **projection(rd,key,parsed[key],decl[0])})
        require(observed_pins == set(CODE_PINS), "all prior Code pins observed")
        # This is a declaration census, not a complete callsite or dispatch census.
        data_paths = sorted(p for p in names if p.startswith("data/") and p.endswith(".json"))
        require(len(data_paths) <= 5000, "resource budget")
        resources = {}
        for path in data_paths:
            raw = z.read(path)
            require(len(raw) <= 2_000_000, "JSON size")
            data = json.loads(raw)
            refs = list(refs_json(data))
            if refs or path.rsplit("/",1)[-1] == "primordial_soup.json":
                resources[path] = {"sha256": digest(raw), "refs": refs, "data": data}
        require(RECIPE in resources and resources[RECIPE]["sha256"] == RECIPE_SHA, "recipe pin")
        require(len(resources) <= 100, "resource hit budget")
        timer=timer_census(z,roster,jar,javap)
        goal=inspect_goal(z,roster,jar,javap)
        return {"schema": 4, "goal_state":goal, "timer_census": timer, "food_class_sha256": class_hashes[FOODS], "artifact": {"sha1": SHA1, "sha256": SHA256, "size_bytes": SIZE},
                "class_roster_sha256": ROSTER_SHA, "callback_declarations": declarations,
                "methods": projected, "data_json_count": len(data_paths),
                "resources": resources, "limits": LIMITS}

def self_test():
    require(list(refs_json({"x":[ID, ID+"_other"], ID:1})) ==
            [[[ID], "KEY", ID], [["x",0], "VALUE", ID]], "exact resource filter")
    require(LIMITS["mutation"] == "NO_MUTATION" and LIMITS["static_contract"] == "NOT_CERTIFIED", "scope")
    require(timer_ref([10,RELICH,[12,"getPushingTreesFor","()I"]]),"timer method match")
    require(not timer_ref([10,RELICH,[12,"getPushingTreesFor","()Z"]]),"descriptor mismatch")
    require(not timer_ref([10,RELICH,[12,"getPushingTreesForOther","()I"]]),"name mismatch")
    print("PASS exact resource and timer member filters and fail-closed discovery policy")

if __name__ == "__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--jar",type=Path)
    p.add_argument("--output",type=Path)
    p.add_argument("--javap",default="javap")
    p.add_argument("--self-test",action="store_true")
    a=p.parse_args()
    if a.self_test:
        self_test()
    else:
        require(a.jar is not None and a.output is not None and not a.output.exists(), "write-once")
        result=inspect(a.jar,a.javap)
        raw=canonical(result).encode()
        require(len(raw)<=8_000_000,"report budget")
        a.output.parent.mkdir(parents=True,exist_ok=True)
        with a.output.open("xb") as out:
            out.write(raw)
        print("REPORT_SHA256",digest(raw),"BYTES",len(raw))
        for key in ("callback_declarations","data_json_count","resources","timer_census"):
            print(key.upper(),json.dumps(result[key],sort_keys=True))
        for method in result["methods"]:
            print("SEMANTIC",json.dumps(method,sort_keys=True))
        for owner,row in result["goal_state"]["classes"].items():
            print("GOAL_OWNER",owner,row["class_sha256"],"DECLARATIONS",len(row["declarations"]),"METHODS",len(row["methods"]))
            for method in row["methods"]:
                print("GOAL_METHOD",json.dumps({"owner":owner,**method},sort_keys=True))
        print("GOAL_DIRECT_CALLS",json.dumps(result["goal_state"]["direct_provider_callee_candidates"],sort_keys=True))
        print("DISCOVERY_ONLY NO_MUTATION NO_PHYSICAL_QA")
