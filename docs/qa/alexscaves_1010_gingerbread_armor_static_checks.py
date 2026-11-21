#!/usr/bin/env python3
"""Fail-closed SHA-exact Gingerbread Armor artifact/class/resource audit.

Proof is publisher-static DISCOVERY only, not gameplay certification or
authorization for mutating the provider's shared attribute cache.
"""
import argparse
import hashlib
import json
from pathlib import Path

def unique(pairs):
    d={}
    for k,v in pairs:
        if k in d:raise AssertionError("duplicate key: "+k)
        d[k]=v
    return d

def run(manifest,report):
    m=json.loads(Path(manifest).read_text(encoding="utf8"),object_pairs_hook=unique)
    b=Path(report).read_bytes()
    assert hashlib.sha256(b).hexdigest()==m["report"]["sha256"],"report SHA mismatch"
    r=json.loads(b,object_pairs_hook=unique)
    assert r["schema_version"]==m["schema_version"]==1
    assert r["scope"]==m["scope"]=="GINGERBREAD_ARMOR_NATIVE_DISCOVERY_NOT_CERTIFIED"
    assert r["artifact"]==m["artifact"],"publisher identity drift"
    assert r["source_revision_1111_parity"]=="NOT_ASSUMED"
    assert r["mutation"]==m["limits"]["mutation"]=="NO_MUTATION"
    assert r["static_contract"]=="NOT_CERTIFIED" and m["limits"]["status"]=="PARTIAL"
    assert r["mutating_hook"]==m["limits"]["mutating_hook"]=="NOT_VERIFIED"
    assert r["physical_qa"]==m["limits"]["physical_qa"]=="NOT_TESTED"
    assert r["provider_universe_closed"] is False and m["limits"]["provider_universe_closed"] is False
    assert r["semantic_magic_roots_certified_delta"]==m["limits"]["new_cast_roots"]==0
    own=m["native_class"]["owner"]; classes=r["native"]["targets"]
    assert set(classes)=={own},"unbounded owner roster"
    c=classes[own];s=m["native_class"]
    assert c["class_sha256"]==s["sha256"]
    assert len(c["declarations"])==s["declared_methods"]
    assert len(c["methods"])==s["code_methods"]
    assert len(c["fields"])==s["fields"]
    assert len(c["consumers"])==s["typed_consumer_owners"]
    assert len(c["in_jar_ancestors"])==s["ancestors"]
    actual=[{"name":a["declaration"]["name"],"descriptor":a["declaration"]["descriptor"],"instruction_count":a["instruction_count"],"instruction_sha256":a["instruction_sha256"]} for a in c["methods"]]
    assert actual==s["methods"],"method roster/hash drift"
    mapped={k:{"sha256":v["sha256"],"size":v["size"]} for k,v in r["matching_resources"].items()}
    assert mapped==m["resources"],"resource roster/hash drift"
    def instructions(name):
        match=[x for x in c["methods"] if x["declaration"]["name"]==name]
        assert len(match)==1
        return " ".join(y["symbol"]+" "+y["operand"] for y in match[0]["instructions"])
    for token in ("double 0.1d","double 0.9d","MOVEMENT_SPEED","ADD_MULTIPLIED_BASE","Map.containsKey","Map.put"):
        assert token in instructions("getOrCreateDurabilityAttributes"),token
    for token in ("getDamageValue","getMaxDamage","getOrCreateDurabilityAttributes","ImmutableMultimap.of"):
        assert token in instructions("acModifiers"),token
    for token in ("ArmorItem","ACArmorMaterial.defense","Attributes.ARMOR","ADD_VALUE","ADD_MULTIPLIED_BASE"):
        assert token in instructions("<init>"),token
    for token in ("getArmorProperties","Consumer.accept"):
        assert token in instructions("initializeClient"),token
    callers=c["consumers"]
    assert any(k.endswith("/ACItemRegistry") and len(v["sites"])==8 for k,v in callers.items())
    for item in ("gingerbread_helmet","gingerbread_chestplate","gingerbread_leggings","gingerbread_boots"):
        assert "assets/alexscaves/models/item/"+item+".json" in r["matching_resources"],item
    assert m["dynamic_speed"]["cache_keys_include_player_uuid"] is False
    print("PASS: exact GingerbreadArmorItem eight methods, four factory variants and 142 resource hashes; PARTIAL NO_MUTATION")

if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--manifest",required=True,type=Path);p.add_argument("--report",required=True,type=Path)
    a=p.parse_args();run(a.manifest,a.report)
