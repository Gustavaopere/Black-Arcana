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
          "scope": "PUBLISHER_FEEDING_CALLBACKS_AND_FOOD_CONTEXT"}

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
                    (owner == COMPAT and name in {"food", "foodEffects"}) or
                    (owner == FOODS and name == "<clinit>")):
                    if "code_sha256" in d:
                        keys.add((name,desc))
            if keys:
                readers[owner] = rd
                selected[owner] = keys
        require(set(PINS) <= set(readers), "required owners")
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
        return {"schema": 1, "artifact": {"sha1": SHA1, "sha256": SHA256, "size_bytes": SIZE},
                "class_roster_sha256": ROSTER_SHA, "callback_declarations": declarations,
                "methods": projected, "data_json_count": len(data_paths),
                "resources": resources, "limits": LIMITS}

def self_test():
    require(list(refs_json({"x":[ID, ID+"_other"], ID:1})) ==
            [[[ID], "KEY", ID], [["x",0], "VALUE", ID]], "exact resource filter")
    require(LIMITS["mutation"] == "NO_MUTATION" and LIMITS["static_contract"] == "NOT_CERTIFIED", "scope")
    print("PASS exact resource filter and fail-closed discovery policy")

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
        for key in ("callback_declarations","data_json_count","resources"):
            print(key.upper(),json.dumps(result[key],sort_keys=True))
        for method in result["methods"]:
            print("SEMANTIC",json.dumps(method,sort_keys=True))
        print("DISCOVERY_ONLY NO_MUTATION NO_PHYSICAL_QA")
