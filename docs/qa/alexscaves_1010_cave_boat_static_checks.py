#!/usr/bin/env python3
"""Exact transcript checks for CaveBoatItem native branches; NOT runtime certification."""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path

SHA = {
    "CaveBoatItem": "6b5bd199a64f5b623fd44c3491b15242b4a44badaab4f4f7c8c0f56335ea8e18",
    "AlexsCavesBoatEntity": "9a54b4edeff25227340f3fe90986869f57c18fb2161ec66ba79637641330e4f1",
    "AlexsCavesChestBoatEntity": "7591cbd52eed9c8dfe3ec8c4b2f740807549bcbb0b1394bd94b091f9f8fec854",
    "AlexsCavesBoat_Type": "8006ebe1e1984fdc106f97c7eecce1f30edae1b0ebf71d65918b22bee4186184",
    "ACCompat": "157b8068d165a9048586c35bfe2c34ad1fc4adbf83c4f2318128498d1ac59f87",
}

def require(ok, reason):
    if not ok:
        raise AssertionError(reason)

def method(text, name, declaration_contains=""):
    lines = text.splitlines(keepends=True)
    signatures = [
        i for i, line in enumerate(lines)
        if re.match(r"^  (?:public|protected|private|static) ", line)
        and name + "(" in line and line.rstrip().endswith(";")
        and declaration_contains in line
    ]
    require(len(signatures) == 1,
            "method missing/ambiguous: " + name + " " + declaration_contains)
    declaration = "".join(lines[signatures[0]:])
    require("    Code:" in declaration, "no Code for " + name)
    return declaration.split("      LineNumberTable:", 1)[0]

def audit(folder):
    report = json.loads((folder / "report.json").read_text(encoding="utf-8"))
    require(report["scope"] == "DISCOVERY_NOT_CERTIFIED"
            and report["mutation"] == "NO_MUTATION"
            and report["physical_qa"] == "NOT_TESTED"
            and not report["provider_universe_closed"], "unverified claims promoted")
    texts = {}
    for name, expected in SHA.items():
        data = (folder / (name + ".javap.txt")).read_bytes()
        require(hashlib.sha256(data).hexdigest() == expected, "javap digest mismatch: " + name)
        require(report["targets"][name]["javap_sha256"] == expected, "manifest mismatch: " + name)
        texts[name] = data.decode("utf-8")
    use = method(texts["CaveBoatItem"], "use")
    for token in ("ClipContext$Fluid.ANY", "HitResult$Type.MISS", "HitResult$Type.BLOCK",
                  "double 5.0d", "AABB.inflate", "AABB.expandTowards", "Level.getEntities",
                  "Level.noCollision", "AlexsCavesBoatEntity", "AlexsCavesChestBoatEntity",
                  "Level.addFreshEntity", "GameEvent.ENTITY_PLACE", "Abilities.instabuild",
                  "ItemStack.shrink", "ACCompat.useFail", "ACCompat.usePass",
                  "ACCompat.useSidedSuccess"):
        require(token in use, "item path missing: " + token)
    require(re.search(r"253: invokevirtual[^\n]*addFreshEntity[^\n]*\n\s*256: pop", use),
            "spawn Boolean must be discarded in publisher")
    require("280: aload" in use and "283: invokevirtual" in use, "stack decrement order")
    for entity in ("AlexsCavesBoatEntity", "AlexsCavesChestBoatEntity"):
        text = texts[entity]
        chest = entity == "AlexsCavesChestBoatEntity"
        require("extends net.minecraft.world.entity.vehicle." +
                ("ChestBoat" if chest else "Boat") in text, "parent mismatch")
        save = method(text, "addAdditionalSaveData")
        read = method(text, "readAdditionalSaveData")
        for body, token in ((save, "CompoundTag.putString"), (read, "Type.byName")):
            require("String ACBoatType" in body and token in body, "type NBT")
            require("invokespecial" not in body, "super NBT method appeared")
        drop = method(text, "getDropItem")
        require(("getChestDropSupplier" if chest else "getDropSupplier") in drop, "drop path")
        fall = method(text, "checkFallDamage")
        for token in ("float 3.0f", "RULE_DOENTITYDROPS", "ACCompat.gameRule",
                      "ACCompat.spawnAtLocation", "getPlankSupplier", "Items.STICK",
                      "iconst_3", "iconst_2", "kill:"):
            require(token in fall, "fall path: " + token)
        vanilla = method(text, "getVariant", "Boat$Type")
        require("Boat$Type.OAK" in vanilla, "vanilla type fallback")
        setter = method(text, "setVariant", "Boat$Type")
        require("return" in setter and "invoke" not in setter, "setter is not no-op")
        add_packet = method(text, "getAddEntityPacket")
        require("ACPlatform.getEntitySpawningPacket" in add_packet, "spawn packet")
    type_class = texts["AlexsCavesBoat_Type"]
    initialization = type_class.split("  static {};", 1)[1].split("      LineNumberTable:", 1)[0]
    require(initialization.count("ACBlockRegistry.PEWEN_PLANKS") == 2,
            "publisher plank mapping changed")
    require("ACItemRegistry.PEWEN_CHEST_BOAT" in initialization
            and "ACItemRegistry.THORNWOOD_CHEST_BOAT" in initialization, "suppliers")
    for name in ("byId", "byName"):
        body = method(type_class, name)
        require("iconst_0" in body and "values:" in body, "invalid boat type fallback")
    print("PASS: SHA-exact Cave Boat local pathways; hooks and physical QA remain unverified")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--transcript-dir", type=Path, required=True)
    args = parser.parse_args()
    audit(args.transcript_dir)
