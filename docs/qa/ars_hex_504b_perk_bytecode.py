#!/usr/bin/env python3
"""Bounded, read-only Ars Hex 5.0.4b provider JAR probe for perk integration.

This proves only exact published artifact identity, class presence, and selected
compiled call-site references. It does NOT prove operand data flow, event
execution, installed-pack parity, or live perk/Mastery behavior.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import unittest
import zipfile

EXPECTED_SHA1 = "2354710ea312e2a6e0fbc3eb2dbafb8e06f10cf4"
EXPECTED_BYTES = 273389
ROOT = "com.alexthw.ars_hex"
CLASSES = {
    "registry": ROOT + ".ArsNouveauRegistry",
    "soul_ward": ROOT + ".malum.perks.SoulWardPerk",
    "magic_proficiency": ROOT + ".malum.perks.MagicProficencyPerk",
    "spirit_spoils": ROOT + ".malum.perks.SpiritSpoilsPerk",
    "scythe": ROOT + ".malum.EnchanterScythe",
    "boomerang_bridge": ROOT + ".malum.MalumCompat",
}
METHOD_HEADER = re.compile(r"^  (?:public|protected|private)\b.*\([^)]*\)(?: throws .+)?;$")


def method_block(javap_text: str, name: str) -> str:
    lines = javap_text.splitlines()
    starts = [i for i, line in enumerate(lines)
              if METHOD_HEADER.match(line)
              and re.search(r"\b" + re.escape(name) + r"\([^)]*\)", line)]
    if len(starts) != 1:
        raise ValueError(f"expected exactly one method named {name}, observed {len(starts)}")
    start = starts[0]
    stop = next((i for i in range(start + 1, len(lines))
                 if METHOD_HEADER.match(lines[i]) or lines[i] == "}"), len(lines))
    block = "\n".join(lines[start:stop])
    if "Code:" not in block or "descriptor:" not in block:
        raise ValueError(f"{name} has no bytecode/descriptor")
    return block


def require_terms(block: str, terms: tuple[str, ...], label: str) -> None:
    missing = [term for term in terms if term not in block]
    if missing:
        raise ValueError(f"{label} missing compiled markers: {missing}")


def inspect_disassembly(dis: dict[str, str]) -> dict:
    if set(dis) != set(CLASSES):
        raise ValueError("missing or unexpected class keys")

    reg = method_block(dis["registry"], "registerCompatPerks")
    require_terms(reg, ("malum", "isLoaded", "SoulWardPerk", "MagicProficencyPerk", "SpiritSpoilsPerk", "PerkRegistry.registerPerk"), "Malum-gated perk registry")
    registrations = len(re.findall(r"^\s*\d+:\s+invokestatic\b[^\n]*// Method [^\n]*PerkRegistry\.registerPerk:", reg, re.M))
    if registrations != 3:
        raise ValueError(f"expected exactly 3 direct PerkRegistry calls, observed {registrations}")

    perk_methods = {}
    for key, terms in {
        "soul_ward": ("SOUL_WARD_CAPACITY", "SOUL_WARD_INTEGRITY", "ADD_VALUE", "ADD_MULTIPLIED_BASE", "withModifierAdded"),
        "magic_proficiency": ("MAGIC_PROFICIENCY", "ADD_MULTIPLIED_BASE", "withModifierAdded"),
        "spirit_spoils": ("SPIRIT_SPOILS", "ADD_VALUE", "withModifierAdded"),
    }.items():
        part = method_block(dis[key], "applyAttributeModifiers")
        require_terms(part, terms, key + ".applyAttributeModifiers")
        perk_methods[key] = {
            "attribute_field_refs": [x for x in terms if x.endswith(("CAPACITY", "INTEGRITY", "PROFICIENCY", "SPOILS"))],
            "modifier_operation_refs": [x for x in terms if x in ("ADD_VALUE", "ADD_MULTIPLIED_BASE")],
            "with_modifier_added_reference": True,
            "numerical_formulas": "SOURCE_PINNED_NOT_OPERAND_FLOW_PROVEN",
        }

    on_hit = method_block(dis["scythe"], "hurtEnemy")
    require_terms(on_hit, ("SpellContext", "SpellResolver", "onCastOnEntity", "hurtEnemy"), "EnchanterScythe.hurtEnemy")
    scribe = method_block(dis["scythe"], "scribeModifiedSpell")
    require_terms(scribe, ("MethodTouch",), "EnchanterScythe.scribeModifiedSpell")
    discount = method_block(dis["scythe"], "getManaDiscount")
    require_terms(discount, ("NECROMANCY", "getCastingCost", "ceil"), "EnchanterScythe.getManaDiscount")
    bridge = method_block(dis["boomerang_bridge"], "workaround")
    require_terms(bridge, ("ScytheBoomerangEntity", "getDirectEntity", "hurtEnemy"), "MalumCompat.workaround")
    return {
        "status": "PASS_BOUNDED_BYTECODE_REFERENCES",
        "evidence_class": "PUBLISHER_BINARY_REFERENCES_ONLY",
        "malum_gated_perk_registry": {"registered_calls": registrations, "class_refs": ["SoulWardPerk", "MagicProficencyPerk", "SpiritSpoilsPerk"]},
        "perk_attribute_call_sites": perk_methods,
        "scythe": {"hurt_enemy_calls_ars_resolver": True, "scribing_references_method_touch": True,
                   "discount_references_necromancy_cost_and_ceil": True,
                   "discount_coefficient": "SOURCE_PINNED_NOT_BYTECODE_OPERAND_VERIFIED"},
        "boomerang_bridge": {"post_damage_handler_contains_boomerang_hurt_enemy_calls": True},
    }


def javap(jar: Path, class_name: str) -> str:
    p = subprocess.run(["javap", "-p", "-c", "-s", "-classpath", str(jar), class_name],
                       capture_output=True, text=True, check=False, timeout=45)
    if p.returncode or "Code:" not in p.stdout:
        raise ValueError(f"javap failed or class lacks Code: {class_name} (exit={p.returncode})")
    return p.stdout


def inspect_jar(jar: Path) -> dict:
    if not jar.is_file():
        raise ValueError("provider artifact not found")
    data = jar.read_bytes()
    sha1 = hashlib.sha1(data).hexdigest()
    if sha1 != EXPECTED_SHA1 or len(data) != EXPECTED_BYTES:
        raise ValueError(f"publisher identity mismatch: sha1={sha1}, bytes={len(data)}")
    with zipfile.ZipFile(jar) as f:
        names = set(f.namelist())
        missing = [c.replace(".", "/") + ".class" for c in CLASSES.values()
                   if c.replace(".", "/") + ".class" not in names]
        if missing:
            raise ValueError(f"missing exact provider classfiles: {missing}")
        meta = [m for m in ("META-INF/neoforge.mods.toml", "META-INF/mods.toml") if m in names]
        if not meta or not any(re.search(r"\bmodId\s*=\s*[\"']ars_hex[\"']", f.read(m).decode("utf-8", "replace")) for m in meta):
            raise ValueError("ars_hex NeoForge mod metadata missing")
    output = inspect_disassembly({k: javap(jar, c) for k, c in CLASSES.items()})
    output.update({"publisher_sha1": sha1, "publisher_sha256": hashlib.sha256(data).hexdigest(),
                   "publisher_bytes": len(data), "classes_checked": sorted(CLASSES.values()),
                   "limitations": [
                       "Published CurseForge JAR SHA equal to historically documented physical modlist hash, not a fresh user-profile disk read.",
                       "Static bytecode references only; coefficient operands and arithmetic order remain source-pinned.",
                       "No claims about runtime branch reachability, callback frequency, or mana payment.",
                       "No real player AttributeInstance/equip/unequip, boomerang hit, or Magic Proficiency damage measured.",
                       "No adapter, RPG Mastery, or Black Arcana spell runtime was executed.",
                   ]})
    return output


SAMPLE_REGISTRY = """public class Reg {
  public static void registerCompatPerks();
    descriptor: ()V
    Code:
      0: ldc #1 // String malum
      1: invokevirtual #1 // Method net/neoforged/fml/ModList.isLoaded:(Ljava/lang/String;)Z
      2: getstatic #1 // Field SoulWardPerk.INSTANCE:LSoulWardPerk;
      3: invokestatic #1 // Method com/hollingsworth/arsnouveau/api/registry/PerkRegistry.registerPerk:(LPerk;)V
      4: getstatic #1 // Field MagicProficencyPerk.INSTANCE:LMagicProficencyPerk;
      5: invokestatic #1 // Method com/hollingsworth/arsnouveau/api/registry/PerkRegistry.registerPerk:(LPerk;)V
      6: getstatic #1 // Field SpiritSpoilsPerk.INSTANCE:LSpiritSpoilsPerk;
      7: invokestatic #1 // Method com/hollingsworth/arsnouveau/api/registry/PerkRegistry.registerPerk:(LPerk;)V
}"""
SAMPLE_PERK = """public class Perk {
  public void applyAttributeModifiers();
    descriptor: ()V
    Code:
       0: getstatic #1 // Field SOUL_WARD_CAPACITY:Ljava/lang/Object;
       1: getstatic #1 // Field SOUL_WARD_INTEGRITY:Ljava/lang/Object;
       2: getstatic #1 // Field MAGIC_PROFICIENCY:Ljava/lang/Object;
       3: getstatic #1 // Field SPIRIT_SPOILS:Ljava/lang/Object;
       4: getstatic #1 // Field ADD_VALUE:Ljava/lang/Object;
       5: getstatic #1 // Field ADD_MULTIPLIED_BASE:Ljava/lang/Object;
       6: invokevirtual #1 // Method ItemAttributeModifiers.withModifierAdded:()V
}"""
SAMPLE_SCYTHE = """public class Scythe {
  public boolean hurtEnemy();
    descriptor: ()Z
    Code:
      0: new #1 // class SpellContext
      1: new #1 // class SpellResolver
      2: invokevirtual #1 // Method SpellResolver.onCastOnEntity:()V
      3: invokespecial #1 // Method MagicScytheItem.hurtEnemy:()Z
  public void scribeModifiedSpell();
    descriptor: ()V
    Code:
      0: getstatic #1 // Field MethodTouch.INSTANCE:LMethodTouch;
  public int getManaDiscount();
    descriptor: ()I
    Code:
      0: getstatic #1 // Field SpellSchools.NECROMANCY:LSpellSchool;
      1: invokevirtual #1 // Method SpellPart.getCastingCost:()I
      2: invokestatic #1 // Method Mth.ceil:(D)I
}"""
SAMPLE_BRIDGE = """public class MalumCompat {
  public static void workaround();
    descriptor: ()V
    Code:
      0: instanceof #1 // class ScytheBoomerangEntity
      1: invokevirtual #1 // Method DamageSource.getDirectEntity:()LEntity;
      2: invokevirtual #1 // Method Item.hurtEnemy:()Z
}"""


def fixtures() -> dict[str, str]:
    return {"registry": SAMPLE_REGISTRY, "soul_ward": SAMPLE_PERK,
            "magic_proficiency": SAMPLE_PERK, "spirit_spoils": SAMPLE_PERK,
            "scythe": SAMPLE_SCYTHE, "boomerang_bridge": SAMPLE_BRIDGE}


class Tests(unittest.TestCase):
    def test_positive_control(self):
        self.assertEqual(inspect_disassembly(fixtures())["status"], "PASS_BOUNDED_BYTECODE_REFERENCES")

    def test_absent_class_fail_closed(self):
        d = fixtures()
        del d["scythe"]
        with self.assertRaisesRegex(ValueError, "class keys"):
            inspect_disassembly(d)

    def test_no_method_fail_closed(self):
        with self.assertRaisesRegex(ValueError, "exactly one"):
            method_block(SAMPLE_SCYTHE, "missingMethod")

    def test_duplicate_method_fail_closed(self):
        fake = SAMPLE_SCYTHE.replace("  public boolean hurtEnemy();", "  public boolean hurtEnemy();\n  public boolean hurtEnemy();")
        with self.assertRaisesRegex(ValueError, "exactly one"):
            method_block(fake, "hurtEnemy")

    def test_wrong_registration_count(self):
        d = fixtures()
        d["registry"] = d["registry"].replace("7: invokestatic", "7: invokenop")
        with self.assertRaisesRegex(ValueError, "exactly 3"):
            inspect_disassembly(d)

    def test_missing_malum_gate(self):
        d = fixtures()
        d["registry"] = d["registry"].replace("String malum", "String absent")
        with self.assertRaisesRegex(ValueError, "malum"):
            inspect_disassembly(d)

    def test_missing_soul_ward_second_attribute(self):
        d = fixtures()
        d["soul_ward"] = d["soul_ward"].replace("SOUL_WARD_INTEGRITY", "OTHER")
        with self.assertRaisesRegex(ValueError, "SOUL_WARD_INTEGRITY"):
            inspect_disassembly(d)

    def test_missing_magic_proficiency_operation(self):
        d = fixtures()
        d["magic_proficiency"] = d["magic_proficiency"].replace("ADD_MULTIPLIED_BASE", "ADD_MULTIPLIED_TOTAL")
        with self.assertRaisesRegex(ValueError, "ADD_MULTIPLIED_BASE"):
            inspect_disassembly(d)

    def test_missing_resolver(self):
        d = fixtures()
        d["scythe"] = d["scythe"].replace("onCastOnEntity", "other")
        with self.assertRaisesRegex(ValueError, "onCastOnEntity"):
            inspect_disassembly(d)

    def test_missing_necromancy(self):
        d = fixtures()
        d["scythe"] = d["scythe"].replace("NECROMANCY", "OTHER")
        with self.assertRaisesRegex(ValueError, "NECROMANCY"):
            inspect_disassembly(d)

    def test_missing_boomerang_handler(self):
        d = fixtures()
        d["boomerang_bridge"] = d["boomerang_bridge"].replace("ScytheBoomerangEntity", "OtherEntity")
        with self.assertRaisesRegex(ValueError, "ScytheBoomerangEntity"):
            inspect_disassembly(d)

    def test_incomplete_bytecode_fail_closed(self):
        with self.assertRaisesRegex(ValueError, "bytecode/descriptor"):
            method_block("public class X {\n  public void foo();\n}", "foo")

    def test_no_jar_fail_closed(self):
        with self.assertRaisesRegex(ValueError, "not found"):
            inspect_jar(Path("/nonexistent/fake.jar"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--jar", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.self_test:
        result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Tests))
        return 0 if result.wasSuccessful() else 1
    if not args.jar or not args.output:
        parser.error("--jar and --output required for binary audit")
    try:
        report = inspect_jar(args.jar)
    except (OSError, ValueError, subprocess.TimeoutExpired, zipfile.BadZipFile) as exc:
        report = {"status": "FAIL_CLOSED", "evidence_class": "NO_VERIFIED_BINARY_PROOF", "deviations": [str(exc)]}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "deviations": report.get("deviations", [])}))
    return 0 if report["status"] == "PASS_BOUNDED_BYTECODE_REFERENCES" else 2


if __name__ == "__main__":
    sys.exit(main())
