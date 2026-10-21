#!/usr/bin/env python3
"""Exact publisher JAR, bounded Slime Boots vs Slime Aspect behavior audit.

Fail closed on declared item attributes and the fall-event handler. These
method callsites do not prove real movement, installed-event registration,
server cancellation, or public perk hooks. Third-party code is not reused.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys
import unittest
import zipfile

from backported_012_perk_consumer_bytecode import hash_and_zip, javap, unique, blocks
from backported_012_slime_aspect_bytecode import ordered, count

CLASSES = {
    "boots": "net.redreaper.backported_spellbooks.item.armor.SlimeBootsArmorItem",
    "server": "net.redreaper.backported_spellbooks.events.ServerEvents",
    "items": "net.redreaper.backported_spellbooks.init.ModItems",
}

def boot_constructor(dis):
    matches = [(h,ops) for h,ops in blocks(dis) if '.SlimeBootsArmorItem(' in h]
    if len(matches) != 1:
        raise ValueError(f'BOOT_CONSTRUCTOR_NOT_UNIQUE: count={len(matches)}')
    return matches[0][1]

def boot_attributes(ops):
    required = [
        ("getstatic", "Attributes.JUMP_STRENGTH:"),
        ("ldc2_w", "double 0.1d"),
        ("getstatic", "Operation.ADD_MULTIPLIED_BASE:"),
        ("invokespecial", "AttributeContainer."),
        ("getstatic", "ModAttributes.FRICTION_MODIFIER:"),
        ("ldc2_w", "double 0.3d"),
        ("getstatic", "Operation.ADD_MULTIPLIED_BASE:"),
        ("invokespecial", "AttributeContainer."),
        ("getstatic", "ModAttributes.BOUNCINESS:"),
        ("ldc2_w", "double 2.5d"),
        ("getstatic", "Operation.ADD_VALUE:"),
        ("invokespecial", "AttributeContainer."),
        ("getstatic", "ModAttributes.AIR_DRAG_MODIFIER:"),
        ("ldc2_w", "double -0.5d"),
        ("getstatic", "Operation.ADD_MULTIPLIED_BASE:"),
        ("invokespecial", "AttributeContainer."),
        ("invokespecial", "ImbuableChestplateArmorItem.")
    ]
    pcs = ordered(ops,required,"SlimeBootsArmorItem.<init>")
    factory_calls = count(ops,"AttributeContainer.",4,"Slime Boots attributes")
    if factory_calls != pcs[3:16:4]:
        raise ValueError("ATTRIBUTE_CONTAINER_SEQUENCE_DRIFT")
    if count(ops,"ImbuableChestplateArmorItem.",1,"Slime Boots parent") != [pcs[-1]]:
        raise ValueError("PARENT_ATTRIBUTE_CONSUMER_DRIFT")
    return {
        "pc_sequence": pcs,
        "modifiers": [
            {"attribute":"JUMP_STRENGTH","operation":"ADD_MULTIPLIED_BASE","coefficient":0.1},
            {"attribute":"FRICTION_MODIFIER","operation":"ADD_MULTIPLIED_BASE","coefficient":0.3},
            {"attribute":"BOUNCINESS","operation":"ADD_VALUE","coefficient":2.5},
            {"attribute":"AIR_DRAG_MODIFIER","operation":"ADD_MULTIPLIED_BASE","coefficient":-0.5},
        ],
        "consumer":"ImbuableChestplateArmorItem constructor, not SlimeAspectMobEffect",
    }

def fall_guard(ops):
    needed = [
        ("invokevirtual","LivingFallEvent.getEntity:"),
        ("instanceof","Player"),
        ("getstatic","EquipmentSlot.FEET:"),
        ("invokevirtual","Player.getItemBySlot:"),
        ("getstatic","ModItems.SLIME_BOOTS:"),
        ("invokevirtual","ItemStack.is:"),
        ("iconst_1",""),
        ("invokevirtual","setCanceled:")
    ]
    pcs = ordered(ops,needed,"ServerEvents.onFallEvent")
    # Strong negative claim is limited to THIS method.
    if count(ops,"setCanceled:",1,"boots fall cancel")!=[pcs[-1]]:
        raise ValueError("FALL_CANCEL_CALL_COUNT_DRIFT")
    if any("ModMobEffects.SLIME_ASPECT:" in tail for _,_,tail in ops):
        raise ValueError("FALL_HANDLER_UNEXPECTED_SPELL_EFFECT_CHECK")
    if any("getCooldowns:" in tail or "isOnCooldown:" in tail
           for _,_,tail in ops):
        raise ValueError("FALL_HANDLER_UNEXPECTED_COOLDOWN_GATE")
    return {
        "pc_sequence":pcs,
        "observed_guard":"Player, EquipmentSlot.FEET, ModItems.SLIME_BOOTS, ItemStack.is",
        "effect_guard":"no direct ModMobEffects.SLIME_ASPECT reference in onFallEvent",
        "cooldown_gate":"no cooldown callsite in onFallEvent",
        "cancel":"one setCanceled(true) compiled callsite; actual event outcome not observed"
    }

def inspect(dis):
    if set(dis) != set(CLASSES):
        raise ValueError("REQUIRED_CLASS_SET_MISSING")
    if "String slime_boots" not in dis["items"] or "SLIME_BOOTS:" not in dis["items"]:
        raise ValueError("SLIME_BOOTS_ITEM_REGISTRY_REF_MISSING")
    tooltip = unique(dis["boots"],"appendHoverText")
    if not any("Utils.applyCooldownReduction:" in t for _,_,t in tooltip):
        raise ValueError("BOOTS_TOOLTIP_COOLDOWN_HELPER_MISSING")
    if not any("passive_ability_no_cooldown" in t for _,_,t in tooltip):
        raise ValueError("BOOTS_TOOLTIP_LOCALIZATION_MISSING")
    return {
        "status":"PASS_BACKPORTED_012_SLIME_BOOTS_FALL_BOUNDED_BYTECODE",
        "evidence_class":"EXACT_PUBLISHER_BOUNDED_EQUIPMENT_AND_EVENT_METHODS",
        "boots":boot_attributes(boot_constructor(dis["boots"])),
        "fall_event":fall_guard(unique(dis["server"],"onFallEvent")),
        "tooltip":"cooldown helper + localized text exist in appendHoverText only; no observed fall-event cooldown gate",
        "item_registry":"literal slime_boots and SLIME_BOOTS field present; exact lambda linkage not formally proved",
        "limitations":[
            "No real player/fall, loaded event-bus registration or successful cancellation observed.",
            "No final movement/friction/bounce/air-drag values, stacking or server tick QA.",
            "No API for perk-driven changes to Slime Aspect or Slime Boots certified.",
            "No duplicate magical spell/semantic action added for item attributes or fall prevention."
        ],
    }

class Tests(unittest.TestCase):
    @staticmethod
    def ops(*tokens):
        return [(i*3,op,tail) for i,(op,tail) in enumerate(tokens)]

    def test_sequence(self):
        a=self.ops(("getstatic","EquipmentSlot.FEET:"),
                   ("invokevirtual","Player.getItemBySlot:"),
                   ("getstatic","ModItems.SLIME_BOOTS:"),
                   ("invokevirtual","ItemStack.is:"))
        self.assertEqual(ordered(a,[(a,b) for a,b in [
            ("getstatic","EquipmentSlot.FEET:"),
            ("invokevirtual","Player.getItemBySlot:"),
            ("getstatic","ModItems.SLIME_BOOTS:"),
            ("invokevirtual","ItemStack.is:")]],"fall"),[0,3,6,9])

    def test_missing_boots_guard_rejected(self):
        with self.assertRaisesRegex(ValueError,"missing"):
            ordered(self.ops(("getstatic","ModItems.PALE_OBSERVER_BOOTS:")),
                    [("getstatic","ModItems.SLIME_BOOTS:")],"boots")

    def test_wrong_equipment_slot_rejected(self):
        with self.assertRaisesRegex(ValueError,"missing"):
            ordered(self.ops(("getstatic","EquipmentSlot.CHEST:")),
                    [("getstatic","EquipmentSlot.FEET:")],"feet")

    def test_wrong_friction_coefficient_rejected(self):
        with self.assertRaisesRegex(ValueError,"missing"):
            ordered(self.ops(("ldc2_w","double 0.4d")),
                    [("ldc2_w","double 0.3d")],"friction")

    def test_wrong_air_drag_operation_rejected(self):
        with self.assertRaisesRegex(ValueError,"missing"):
            ordered(self.ops(("getstatic","Operation.ADD_MULTIPLIED_TOTAL:")),
                    [("getstatic","Operation.ADD_MULTIPLIED_BASE:")],"air drag")

    def test_duplicate_attribute_constructor_rejected(self):
        with self.assertRaisesRegex(ValueError,"count"):
            count(self.ops(*([("invokespecial","AttributeContainer.")] * 5)),
                  "AttributeContainer.",4,"boot attrs")

    def test_fall_needs_cancel(self):
        with self.assertRaisesRegex(ValueError,"missing"):
            ordered(self.ops(("iconst_0","")), [("iconst_1","")],"cancel")

    def test_effect_check_rejected(self):
        with self.assertRaisesRegex(ValueError,"FALL_HANDLER_UNEXPECTED_SPELL_EFFECT_CHECK"):
            ops=self.ops(
                ("invokevirtual","LivingFallEvent.getEntity:"),
                ("instanceof","Player"),
                ("getstatic","EquipmentSlot.FEET:"),
                ("invokevirtual","Player.getItemBySlot:"),
                ("getstatic","ModItems.SLIME_BOOTS:"),
                ("invokevirtual","ItemStack.is:"),
                ("iconst_1",""),
                ("invokevirtual","setCanceled:"),
                ("getstatic","ModMobEffects.SLIME_ASPECT:"))
            fall_guard(ops)

    def test_no_class_set(self):
        with self.assertRaisesRegex(ValueError,"REQUIRED_CLASS_SET_MISSING"):
            inspect({})

    def test_no_method(self):
        with self.assertRaisesRegex(ValueError,"METHOD_MISSING_OR_AMBIGUOUS"):
            unique("class Blank {}","onFallEvent")

    def test_wrong_hash(self):
        from tempfile import TemporaryDirectory
        with TemporaryDirectory() as t:
            p=Path(t)/"wrong.jar"
            p.write_bytes(b"not the publisher jar")
            with self.assertRaisesRegex(ValueError,"JAR_SHA_MISMATCH"):
                hash_and_zip(p)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--self-test",action="store_true")
    p.add_argument("--jar",type=Path)
    p.add_argument("--output",type=Path)
    a=p.parse_args()
    if a.self_test:
        done=unittest.TextTestRunner(verbosity=2).run(
            unittest.defaultTestLoader.loadTestsFromTestCase(Tests))
        return 0 if done.wasSuccessful() else 1
    if a.jar is None or a.output is None:
        p.error("--jar and --output required")
    try:
        sha=hash_and_zip(a.jar)
        with zipfile.ZipFile(a.jar) as z:
            entries=set(z.namelist())
        for clazz in CLASSES.values():
            if clazz.replace(".","/")+".class" not in entries:
                raise ValueError("CLASS_MISSING: "+clazz)
        report=inspect({key:javap(a.jar,clazz) for key,clazz in CLASSES.items()})
        report["publisher_sha1"]=sha
        report["deviations"]=[]
    except (OSError,ValueError,zipfile.BadZipFile,subprocess.CalledProcessError) as exc:
        report={"status":"FAIL_CLOSED","deviations":[str(exc)]}
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(report,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"status":report["status"],"deviations":report["deviations"]}))
    return 0 if report["status"]=="PASS_BACKPORTED_012_SLIME_BOOTS_FALL_BOUNDED_BYTECODE" else 2

if __name__=="__main__":
    sys.exit(main())
