#!/usr/bin/env python3
"""SHA-exact, read-only partial Candy Cane Hook regression. Not provider certification."""
from __future__ import annotations
import argparse, hashlib, json, re
from pathlib import Path
SHA = {
    "CandyCaneHookItem": "9103113b3719da863dd2fa32c83b21e42d70500db06341af9d8c5e8a189fa479",
    "CandyCaneHookEntity": "db02bb6415b39fc211761eefedb221bdcd3ab275a82978f8c7fd294059661273",
    "GumWormSegmentEntity": "837eebb48fb6c16ecb82d28b9946a848949635b8ca556b2180d235d5d1fde010",
    "ACCompat": "917e2276a9d58628fc07fdddd80c4c6a6f975285922b98edd46be33ffddc1fdd",
    "ACItemPredicates": "9967352bad9506cb99c4ae1e4647ff4bd81c9f5bc7fa504f0abbcd22b17a0402",
    "CandyCaneHookRenderer": "f1e614aa38b19ec946fbea923e12a985b48385de44189f68797de8cca0da8e5a",
    "ClientEvents": "037998c4a136c1a9b7211832b5d03d04627ee9e22c54b17480bceba088769e8b",
}
def require(ok, message):
    if not ok:
        raise AssertionError(message)
def method(source, name):
    hits = list(re.finditer(r'(?m)^  (?:public|private|protected|static) [^\n]+\b' +
                            re.escape(name) + r'\([^\n]*\);$', source))
    require(len(hits) == 1, "missing/ambiguous method " + name)
    begin = hits[0].end()
    next_method = re.search(r'(?m)^  (?:public|private|protected|static) ', source[begin:])
    body = source[begin:begin + next_method.start()] if next_method else source[begin:]
    require("    Code:" in body, "no Code in " + name)
    return body.split("      LineNumberTable:")[0]
def audit(directory):
    report = json.loads((directory / "report.json").read_text())
    require(report["scope"] == "DISCOVERY_NOT_CERTIFIED" and
            report["mutation"] == "NO_MUTATION" and not report["provider_universe_closed"],
            "unverified scope promoted")
    transcript = {}
    for name, expected in SHA.items():
        raw = (directory / (name + ".javap.txt")).read_bytes()
        require(hashlib.sha256(raw).hexdigest() == expected, "transcript changed: " + name)
        require(report["targets"][name]["javap_sha256"] == expected, "report mismatch: " + name)
        transcript[name] = raw.decode("utf-8")
    item, entity, compat = [transcript[name] for name in ("CandyCaneHookItem", "CandyCaneHookEntity", "ACCompat")]
    for name in ("use", "acInventoryTick", "canLaunchHook", "isHookLaunchedInWorld",
                 "canPerformAction", "getEnchantmentValue", "getLaunchedHookUUID",
                 "isActive", "isEnchantable", "isReelingIn",
                 "setLastLaunchedHookUUID", "setReelingIn"):
        method(item, name)
    used = method(item, "use")
    for marker in ("canLaunchHook:", "CandyCaneHookEntity", "GumWormSegmentEntity",
                   "addFreshEntity:", "setLastLaunchedHookUUID:", "setReelingIn:",
                   "hurtAndBreak:", "ACCompat.useConsume:", "ACCompat.usePass:",
                   "ITEM_INTERACT_START", "ITEM_INTERACT_FINISH"):
        require(marker in used, "use missing " + marker)
    require(re.search(r'172: invokevirtual.*addFreshEntity.*\n\s+175: pop', used),
            "spawn Boolean result must be ignored in item use")
    for marker in ("LastLaunchedHookUUID", "ServerLevel.getEntity:",
                   "getOwner:", "getHandLaunchedFrom:", "isAlive:"):
        require(marker in method(item, "canLaunchHook"), "launch gate missing " + marker)
    for marker in ("DataComponents.CUSTOM_DATA", "CustomData.copyTag", "CustomData.of:"):
        require(marker in compat, "CUSTOM_DATA boundary missing " + marker)
    for nbt in ("Reeling", "HookedEntityUUID", "Offhand"):
        require(nbt in method(entity, "readAdditionalSaveData") and
                nbt in method(entity, "addAdditionalSaveData"), "NBT boundary missing " + nbt)
    require("CandyCaneHookEntity(net.minecraft.world.entity.player.Player," in entity, "constructor identity")
    for marker in ("ACEnchantmentRegistry.FAR_FLUNG", "ACEnchantmentRegistry.SHARP_CANE",
                   "ACEnchantmentRegistry.STRAIGHT_HOOK", "double 0.5d", "double 0.2d",
                   "double 0.0045d", "float 3.0f", "setDamage:(F)V"):
        require(marker in entity, "constructor enchantment missing " + marker)
    for marker in ("Level.isClientSide:", "isOwnerHoldingHook:", "isReeling:",
                   "getEntities:", "getDamage:", "DamageSources.thrown:",
                   "Entity.hurt:", "getHookedPosition:", "fling:"):
        require(marker in method(entity, "tick"), "entity tick missing " + marker)
    require("getHeadEntity:" in method(entity, "onHitEntity") and
            "setHookedEntityUUID:" in method(entity, "onHitEntity"), "hooked GumWorm branch")
    require("BlockState.onProjectileHit:" in method(entity, "onHitBlock") and
            "setHookedPosition:" in method(entity, "onHitBlock"), "block collision branch")
    require("double 0.20000000298023224d" in method(entity, "fling") and
            "Entity.setDeltaMovement:" in method(entity, "fling"), "fling motion")
    require("isOffhand:" in method(entity, "getHandLaunchedFrom"), "hand selector")
    require("postReel:" in method(entity, "remove"), "removal cleanup")
    require("setLastLaunchedHookUUID:" in method(entity, "postReel"), "item UUID cleanup")
    require("CandyCaneHookItem.setReelingIn:" in
            method(transcript["GumWormSegmentEntity"], "postDismount"), "GumWorm release")
    print("PASS: exact partial hook pathways / NO_MUTATION / NOT_TESTED")
if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--transcript-dir", required=True, type=Path)
    args = p.parse_args()
    audit(args.transcript_dir)
