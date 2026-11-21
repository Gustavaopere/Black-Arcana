#!/usr/bin/env python3
"""Check Gazing Pearl publisher report SHA/method/consumer/resource identity only."""
import argparse, hashlib, json
from pathlib import Path

def unique(pairs):
    d={}
    for k,v in pairs:
        if k in d: raise AssertionError("duplicate key "+k)
        d[k]=v
    return d

def check(manifest,report):
    m=json.loads(Path(manifest).read_text(encoding="utf8"),object_pairs_hook=unique)
    raw=Path(report).read_bytes()
    assert hashlib.sha256(raw).hexdigest()==m["report"]["sha256"],"report SHA drift"
    r=json.loads(raw,object_pairs_hook=unique)
    assert r["schema_version"]==m["schema_version"]==1
    assert r["scope"]==m["scope"]=="GAZING_PEARL_PUBLISHER_DISCOVERY_NOT_CERTIFIED"
    assert r["artifact"]==m["artifact"],"artifact mismatch"
    assert r["mutation"]==m["limits"]["mutation"]=="NO_MUTATION"
    assert r["mutating_hook"]==m["limits"]["mutating_hook"]=="NOT_VERIFIED"
    assert r["physical_qa"]==m["limits"]["physical_qa"]=="NOT_TESTED"
    assert r["static_contract"]=="NOT_CERTIFIED" and m["limits"]["static_contract"]=="PARTIAL"
    assert r["provider_universe_closed"] is False
    assert r["semantic_magic_roots_certified_delta"]==0
    targets=r["native"]["targets"]
    assert set(targets)==set(m["classes"])
    for owner,seal in m["classes"].items():
        item=targets[owner]
        assert item["class_sha256"]==seal["sha256"]
        assert len(item["fields"])==seal["fields_count"]
        assert len(item["consumers"])==seal["consumers_count"]
        actual=[{"name":b["declaration"]["name"],"descriptor":b["declaration"]["descriptor"],"instruction_count":b["instruction_count"],"instruction_sha256":b["instruction_sha256"]} for b in item["methods"]]
        assert actual==seal["methods"],"method roster drift: "+owner
    assert r["filename_matched_resources"]==m["filename_matched_resources"]
    item=targets["com/github/alexmodguy/alexscaves/server/item/GazingPearlItem"]
    enum=targets["com/github/alexmodguy/alexscaves/server/entity/util/DeepOneReaction"]
    def body(c,name):
        matches=[x for x in c["methods"] if x["declaration"]["name"]==name]
        assert len(matches)==1
        return " ".join(x["operand"]+" "+x["symbol"] for x in matches[0]["instructions"])
    for token in ("LastReputationTimestamp","long 100l","getGameTime","HasReputation","Reputation","getUUID","getDeepOneReputation","setTag"):
        assert token in body(item,"acInventoryTick"),token
    for token in ("HasReputation","Reputation","fromReputation","translatable"):
        assert token in body(item,"appendHoverText"),token
    for token in ("System.currentTimeMillis","HSBtoRGB"):
        assert token in body(item,"getPearlColor"),token
    for token in ("-10","10","30","AGGRESSIVE","STALKING","NEUTRAL","HELPFUL"):
        assert token in body(enum,"fromReputation"),token
    print("PASS SHA exact 5 item + 9 reaction methods, resources and native callsites; PARTIAL NO_MUTATION")

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--manifest",type=Path,required=True)
    p.add_argument("--report",type=Path,required=True)
    a=p.parse_args();check(a.manifest,a.report)
