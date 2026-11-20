#!/usr/bin/env python3
"""Official Mojang/NeoForge callback reference; never execute game code."""
import argparse
import json
from pathlib import Path
import re
import zipfile
from alexscaves_1010_armor_material_audit import ClassReader, canonical, digest, require
from alexscaves_1010_enchantable_item_probe import disassemble, summarize
from alexscaves_1010_destroyed_item_engine_reference import verify_artifact, ARTIFACTS
import alexscaves_1010_repairable_item_boundary as reference

TARGETS = {
    "net.minecraft.world.entity.player.Player": {"getAttackStrengthScale", "getCurrentItemAttackStrengthDelay", "attack"},
    "net.minecraft.world.entity.LivingEntity": {"swing", "updateSwingTime"},
    "net.minecraft.client.multiplayer.MultiPlayerGameMode": {"attack"},
}


def neo(universal, userdev, javap):
    verify_artifact(universal, "universal")
    verify_artifact(userdev, "userdev")
    relevant = re.compile(r"swing|onLeftClickEntity|onPlayerAttackTarget|AttackEntityEvent", re.I)
    groups = {}
    with zipfile.ZipFile(universal) as z:
        for owner in ("net/neoforged/neoforge/common/extensions/IItemExtension",
                      "net/neoforged/neoforge/common/extensions/IItemStackExtension",
                      "net/neoforged/neoforge/common/CommonHooks"):
            raw = z.read(owner + ".class")
            rd = ClassReader(raw)
            methods = disassemble(universal, javap, owner)
            groups[owner] = {"class_sha256": digest(raw), "declarations": [m for m in rd.methods if relevant.search(m["name"])],
                             "methods": [summarize(rd, k, body) for k, body in sorted(methods.items()) if body and relevant.search(k[0])]}
    patches = {}
    with zipfile.ZipFile(userdev) as z:
        for owner in ("world/entity/player/Player.java", "world/entity/LivingEntity.java",
                      "world/item/Item.java", "world/item/ItemStack.java",
                      "client/multiplayer/MultiPlayerGameMode.java",
                      "server/network/ServerGamePacketListenerImpl.java"):
            path = "patches/net/minecraft/" + owner + ".patch"
            if path not in z.namelist():
                patches[path] = {"present": False}
                continue
            raw = z.read(path)
            lines = raw.decode("utf8").splitlines()
            hits = {i for i, s in enumerate(lines) if relevant.search(s)}
            selected = {i for n in hits for i in range(max(0, n-4), min(len(lines), n+5))}
            patches[path] = {"present": True, "sha256": digest(raw),
                             "selected": [{"line": i+1, "text": lines[i]} for i in sorted(selected)]}
    return {"artifacts": ARTIFACTS, "classes": groups, "patches": patches}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for name in ("javap", "universal", "userdev", "output"):
        p.add_argument("--" + name, type=Path, required=True)
    a = p.parse_args()
    require(not a.output.exists(), "new report required")
    tmp = a.output.parent / "swing-reference"
    tmp.mkdir()
    # Reuse the pinned official mapping reader in this isolated process only.
    reference.TARGETS = TARGETS
    out = {"scope": "STATIC_REFERENCE_ONLY", "vanilla": reference.vanilla(tmp, a.javap),
           "neoforge": neo(a.universal, a.userdev, a.javap), "mutation": "NO_MUTATION",
           "mutating_hook": "NOT_VERIFIED", "physical_qa": "NOT_TESTED"}
    a.output.write_text(canonical(out), encoding="utf8")
    print("BOUNDARY_SHA256", digest(a.output.read_bytes()))
    for owner, data in out["vanilla"]["classes"].items():
        print("VANILLA_OWNER", owner, data["obfuscated_owner"], data["class_sha256"], data["parent"])
        for m in data["methods"]:
            print("VANILLA_METHOD", owner, json.dumps(m, sort_keys=True))
    for owner, data in out["neoforge"]["classes"].items():
        print("NEO_OWNER", owner, json.dumps(data, sort_keys=True))
    for path, data in out["neoforge"]["patches"].items():
        print("NEO_PATCH", path, json.dumps(data, sort_keys=True))


if __name__ == "__main__":
    main()
