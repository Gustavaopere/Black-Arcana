#!/usr/bin/env python3
"""Assert exact publisher bytes and causal boundaries; discovery only."""
import argparse,hashlib,json
from pathlib import Path
EXPECTED_REPORT="7e884f85cf998b45be0b17745f0e3e8997a661da6d32ade7d3c91d7a87d1d658"
EXPECTED_JAR="36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c"
OWNERS={
"FloaterItem":"30d98e6b5db3fc977c8e8e66adb82576c934d5a7cdc423bbd258f1e7a3224a05",
"FrostmintSpearItem":"0156bc79eb7c6bc48229c6811a3d5907e05f74b548fba4c1c467369b22a8f0be",
"FloaterEntity":"b675ebd726fc8045610a48fbd310abbd5f6762fe68e1158badd8026e47ac2c30",
"FrostmintSpearEntity":"a01a3cd9dc643326b708635be5f91d96fbe75ad449b05ca6c3c2c7d31f7d1025",
"FrostmintExplosion":"fed381b37be656b0ed4757994674ba5cd613ace025c3f4673ddcbc8144277fb9",
"FrostmintFreezableAccessor":"0ffc4442265c5815d9312614dbbc65ef712433d3969a835ab669f136f2b9a476"
}
RESOURCE={
"data/alexscaves/recipe/floater.json":"379259801117cfd1aba2045bec78b19d55c913f47d33b1e925b4e241f0c0ce51",
"data/alexscaves/recipe/frostmint_spear.json":"4a2f50e9f4d6caf1455d42bc67040f21320b5018923d87d5d32e1e2da2dcbc8a",
"data/alexscaves/weapon_attributes/frostmint_spear.json":"9241e582904b7efffed0c4e197b792033447ad015fd6980e91dbf1dbbab9b7d5",
}
def fail(ok, reason):
    if not ok:raise AssertionError(reason)
def method(j,owner,name):
    matches=[]
    for part in ("native","entity_native","effect_native"):
        for full,x in j[part]["targets"].items():
            if full.endswith("/"+owner):matches += [m for m in x["methods"] if m["declaration"]["name"]==name]
    fail(len(matches)==1,"method absent/ambiguous "+owner+"."+name)
    return matches[0]
def contains(m,*fragments):
    blob=" ".join(v["symbol"]+" "+v["operand"] for v in m["instructions"])
    for f in fragments:fail(f in blob,"missing "+f+" at "+m["declaration"]["name"])
def run(p):
    raw=p.read_bytes()
    fail(hashlib.sha256(raw).hexdigest()==EXPECTED_REPORT,"immutable report fingerprint drift")
    j=json.loads(raw)
    fail(j["artifact"]["sha256"]==EXPECTED_JAR,"artifact mismatch")
    fail(j["scope"]=="DISCOVERY_NOT_CERTIFIED" and j["mutation"]=="NO_MUTATION"
       and j["mutating_hook"]=="NOT_VERIFIED" and j["physical_qa"]=="NOT_TESTED"
       and not j["provider_universe_closed"],"unsafe scope promotion")
    classes={k.split("/")[-1]:v["class_sha256"] for part in ("native","entity_native","effect_native") for k,v in j[part]["targets"].items()}
    fail(classes==OWNERS,"class roster or hashes changed")
    fr=j["native"]["filename_matched_resources"]
    for path,sha in RESOURCE.items():fail(fr[path]["sha256"]==sha,"resource drift: "+path)
    contains(method(j,"FloaterItem","use"),"isInWaterOrBubble","isShiftKeyDown","addFreshEntity","startRiding","shrink")
    contains(method(j,"FloaterEntity","tick"),"wasEyeInWater","double -0.04d","double 0.2d","double 0.9d","timeOutOfWater","discard")
    contains(method(j,"FrostmintSpearItem","releaseUsing"),"float 2.5f","double 0.1d","shootFromRotation","addFreshEntity","shrink")
    contains(method(j,"FrostmintSpearItem","acHurtEnemy"),"setTicksFrozen","setFrostmintFreezing")
    fail(any(x["opcode"]=="sipush" and x["operand"]=="200" for x in method(j,"FrostmintSpearItem","acHurtEnemy")["instructions"]),"freeze 200 ticks drift")
    contains(method(j,"FrostmintSpearEntity","explode"),"BlockInteraction.KEEP","FrostmintExplosion")
    contains(method(j,"FrostmintSpearEntity","onHitEntity"),"float 6.0f","DamageSources.trident","damageBonus")
    contains(method(j,"FrostmintExplosion","explode"),"getSeenPercent","ignoreExplosion","setFrostmintFreezing","getTicksRequiredToFreeze","getDamageSource")
    contains(method(j,"FrostmintExplosion","finalizeExplosion"),"WorldEventMessage","interactsWithBlocks")
    print("PASS: SHA-exact two item classes, two entities, freeze accessor and native explosion; DISCOVERY_NOT_CERTIFIED / NO_MUTATION")
if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--report",required=True,type=Path)
    run(p.parse_args().report)
