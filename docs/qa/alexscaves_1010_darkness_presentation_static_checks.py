#!/usr/bin/env python3
"""Read-only regression over exact publisher report and javap captures.

This verifies native static branches ONLY. It is not physical QA, hook certification
or proof that an optional third-party implementer exists at runtime.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

JAR_SHA256 = "36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c"
CLASS_SHA = {
    "CustomArmorPostRender":"19c649b8fdd407e51049f8a98dd31dc348a022c148ad3d5a70f2295a544988fd",
    "CustomTabBehavior":"6a77f884be2f7556f8c5085a534bd70968628c52d83687be2efde8237dba6cbe",
    "DarkenedAppleItem":"58e4bd35322bbedbc654519d8a76577f79d964d498a22d372ea452f683b715cb",
    "DarknessArmorItem":"872fc610bac5be6010e3981b001c4088c7227e9cffe7938381c34c2f456c4e9a",
    "ACItemRegistry":"114e4a3576d56cb66d240fa9df9db7693b1df576ebfa86631ef751dd1e7b5bb1",
    "ACArmorMaterial":"478accf7ab37014dc06a8f3d801348948638dc517db0e21b7fd91d2b47ca40a6",
    "ACServerConfig":"67abf51943537e735a08c268607ca08901c2b197f0b278fa4b464887d40ea129",
}
RESOURCE_SHA = {
    "data/alexscaves/recipe/hood_of_darkness.json":"1c3884eb43c47a87062f28461938a1ba4bde0c5af8676623707915c6a0ff7038",
    "data/alexscaves/recipe/cloak_of_darkness.json":"bb5a5e64b2f7a6200e91dd45e877bc4ad6c9c4aa1012e41c31acdfde89bb46e9",
    "data/alexscaves/recipe/darkened_apple.json":"69ee3d764bbc896ba4b08155f3dd73af7456c0164210f87f7637d488b5dd40a3",
}
ARMOR_IMPLEMENTERS = {
    "DarknessArmorItem","DivingArmorItem","GingerbreadArmorItem",
    "HazmatArmorItem","PrimordialArmorItem","RainbounceBootsItem",
}

def demand(ok, why):
    if not ok:
        raise AssertionError(why)

def inspect(folder: Path):
    report = json.loads((folder / "report.json").read_text(encoding="utf-8"))
    demand(report["scope"] == "EXACT_NATIVE_DISCOVERY_NOT_CERTIFIED", "unexpected certification")
    demand(report["artifact"]["sha256"] == JAR_SHA256 and report["artifact"]["class_count"] == 1555, "publisher identity")
    demand(report["mutation"] == "NO_MUTATION"
           and report["mutating_hook"] == "NOT_VERIFIED"
           and report["physical_qa"] == "NOT_TESTED"
           and not report["provider_universe_closed"], "unsafe scope promotion")
    for label, suffix in (("CustomArmorPostRender","/CustomArmorPostRender"),
                          ("CustomTabBehavior","/CustomTabBehavior")):
        demand(report["interface_owners"][label].endswith(suffix), "interface moved")
    for key, row in report["transcripts"].items():
        short = key.rsplit("/", 1)[-1]
        if short not in CLASS_SHA:
            continue
        demand(row["class_sha256"] == CLASS_SHA[short], "class binary drift " + short)
        raw = (folder / row["file"]).read_bytes()
        demand(hashlib.sha256(raw).hexdigest() == row["javap_sha256"], "javap mismatch " + short)
    typed = report["typed_consumer_census"]
    impl = {owner.rsplit("/",1)[-1] for owner, meta in typed["CustomArmorPostRender"].items()
            if meta["direct_implementer"]}
    demand(impl == ARMOR_IMPLEMENTERS, "armor implementers changed")
    demand(any(owner.endswith("/HumanoidArmorLayerMixin") for owner in typed["CustomArmorPostRender"]), "render consumer absent")
    demand(not any(meta["direct_implementer"] for meta in typed["CustomTabBehavior"].values()), "unexpected creative tab implementer")
    demand(any(owner.endswith("/ACCreativeTabRegistry") for owner in typed["CustomTabBehavior"]), "creative tab consumer missing")
    def txt(name):
        pairs=[(owner,row) for owner,row in report["transcripts"].items() if owner.endswith("/"+name)]
        demand(len(pairs)==1, "transcript ambiguous "+name)
        return (folder / pairs[0][1]["file"]).read_text(encoding="utf-8")
    apple=txt("DarkenedAppleItem")
    for m in ("finishUsingItem(", "sipush        600", "MobEffectInstance.getDuration:",
              "MobEffectInstance.getAmplifier:", "LivingEntity.forceAddEffect:",
              "ACAdvancementTriggerRegistry.EAT_DARKENED_APPLE",
              "Item.finishUsingItem:"):
        demand(m in apple, "apple path "+m)
    armor=txt("DarknessArmorItem")
    for m in ("canChargeUp(", "getMeterProgress(", "acArmorTick(", "acInventoryTick(",
              "onKeyPacket(", "getArmorTexture(", "CloakCharge", "CanCharge",
              "LastLightTimestamp", "LastEquipMessageTime", "ArmorKeyMessage",
              "LivingEntity.addEffect:", "UpdateItemTagMessage",
              "DARKNESS_INCARNATE", "darknessCloakChargeTime", "darknessCloakFlightTime"):
        demand(m in armor, "armor branch "+m)
    reg=txt("ACItemRegistry")
    for m in ("lambda$static$134(", "lambda$static$135(", "lambda$static$136(",
              "ArmorItem$Type.HELMET", "ArmorItem$Type.CHESTPLATE",
              "DARKNESS_ARMOR_MATERIAL", "DarkenedAppleItem"):
        demand(m in reg, "factory "+m)
    material=txt("ACArmorMaterial")
    for m in ("Field MAX_DAMAGE_ARRAY:[I", "bipush        13", "bipush        15",
              "Field durability:I", "Item$Properties.durability:"):
        demand(m in material, "durability "+m)
    config=txt("ACServerConfig")
    for m in ("darkness_cloak_charge_time", "darkness_cloak_fly_time",
              "sipush        1000", "sipush        200", "defineInRange:"):
        demand(m in config, "config "+m)
    demand("CustomArmorPostRender.getArmorTexture:" in txt("HumanoidArmorLayerMixin"), "mixin consumer")
    tab=txt("ACCreativeTabRegistry")
    demand("CustomTabBehavior.fillItemCategory:" in tab
           and "CreativeModeTab$Output.accept:" in tab, "creative tab branches")
    for res, expected in RESOURCE_SHA.items():
        demand(report["filename_matched_resources"][res]["sha256"] == expected, "resource hash "+res)
    print("PASS: exact native presentation/Darkness branches; NO_MUTATION / NOT_TESTED / NOT_CERTIFIED")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--transcript-dir", required=True, type=Path)
    inspect(p.parse_args().transcript_dir)
