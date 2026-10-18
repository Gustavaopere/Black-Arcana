#!/usr/bin/env python3
"""Fail-closed compiled Epic Fight 21.17.3.1 trident registry/bootstrap proof.

Validates javap -v linkage: exact three registry strings -> invokedynamic
LambdaMetafactory bootstrap indices -> corresponding typed supplier lambdas ->
DeferredRegister.register -> exact DeferredHolder fields. Also requires the
separate SHA-gated attack-phase builder proof.
No provider code execution, player gameplay or third-party JAR redistribution.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import subprocess
import sys
import unittest

from epicfight_211731_trident_attack_phase import CONFIG, REGISTRY, evaluate
from epicfight_211731_trident_causal import inspect as inspect_publisher, javap


TARGETS = {
    "wrathful_lighting": (67, "lambda$static$40", "WRATHFUL_LIGHTING", "WrathfulLightingSkill"),
    "tsunami": (68, "lambda$static$42", "TSUNAMI", "ConditionalWeaponInnateSkill"),
    "everlasting_allegiance": (69, "lambda$static$43", "EVERLASTING_ALLEGIANCE", "EverlastingAllegiance"),
}
BYTECODE = re.compile(r"^\s*(\d+):\s+([a-z][a-z0-9_]*)\b(.*)$")
BOOTSTRAP = re.compile(r"^\s*(\d+):\s+#\d+\s+REF_invokeStatic\s+java/lang/invoke/LambdaMetafactory\.metafactory:")


def verify_linkage(verbose: str):
    if "BootstrapMethods:" not in verbose:
        raise ValueError("missing BootstrapMethods table")
    if "static {};" not in verbose:
        raise ValueError("missing class static initializer")
    start = verbose.index("static {};")
    section = verbose[start:verbose.index("BootstrapMethods:", start)]
    instructions = []
    for ln in section.splitlines():
        if m := BYTECODE.match(ln):
            instructions.append((int(m.group(1)), m.group(2), m.group(3).strip()))
    if not instructions or len(instructions) > 900:
        raise ValueError("invalid or excessive initializer instruction count")

    boot = verbose.split("BootstrapMethods:", 1)[1]
    boot = boot.split("\nInnerClasses:", 1)[0]
    lines = boot.splitlines()
    indexes = [(i, int(m.group(1))) for i, ln in enumerate(lines)
               if (m := BOOTSTRAP.match(ln))]
    result = {}
    for name, (want_boot, want_lambda, holder, return_type) in TARGETS.items():
        candidates = [(i, pc) for i, (pc, op, tail) in enumerate(instructions)
                      if op in ("ldc", "ldc_w") and
                      re.search(r"// String " + re.escape(name) + r"\s*$", tail)]
        if len(candidates) != 1:
            raise ValueError(f"{name}: expected exactly one initializer ID constant, got {len(candidates)}")
        i, pc = candidates[0]
        if i+3 >= len(instructions):
            raise ValueError(f"{name}: initializer truncated after ID")
        invoked = instructions[i+1]
        registered = instructions[i+2]
        stored = instructions[i+3]
        match = re.search(r"// InvokeDynamic #(\d+):apply:", invoked[2])
        if invoked[1] != "invokedynamic" or not match or int(match.group(1)) != want_boot:
            raise ValueError(f"{name}: wrong invokedynamic bootstrap")
        if registered[1] != "invokevirtual" or "DeferredRegister.register:" not in registered[2]:
            raise ValueError(f"{name}: not followed by DeferredRegister.register")
        if stored[1] != "putstatic" or f"Field {holder}:" not in stored[2]:
            raise ValueError(f"{name}: wrong registry holder assignment")
        if not (pc < invoked[0] < registered[0] < stored[0]):
            raise ValueError(f"{name}: initializer opcode offsets do not increase")
        matches = [i for i, b in indexes if b == want_boot]
        if len(matches) != 1:
            raise ValueError(f"{name}: missing or duplicate bootstrap #{want_boot}")
        bi = matches[0]
        next_header = next((p for p, _ in indexes if p > bi), len(lines))
        stanza = "\n".join(lines[bi:next_header])
        reference = f"REF_invokeStatic yesman/epicfight/registry/entries/EpicFightSkills.{want_lambda}:"
        if stanza.count(reference) != 1 or f"/{return_type};" not in stanza:
            raise ValueError(f"{name}: bootstrap does not reference expected supplier return type")
        if "LambdaMetafactory.metafactory" not in stanza:
            raise ValueError(f"{name}: missing LambdaMetafactory")
        result[name] = {
            "id_literal_pc": pc,
            "bootstrap_index": want_boot,
            "supplier": want_lambda,
            "return_type": return_type,
            "holder": holder,
            "ordered_initializer_registry_binding": True,
        }
    return {
        "status": "PASS_BOUNDED_TRIDENT_REGISTRY_BOOTSTRAP_LINKAGE",
        "evidence_class": "EXACT_PUBLISHER_COMPILER_GENERATED_ID_TO_SUPPLIER_LINKAGE",
        "bindings": result,
        "limits": [
            "Exact publisher static initializer and BootstrapMethods references only.",
            "No proof of actual world registration, player activation, damage or resource settlement.",
            "Future compiler or release drift must fail closed; IDs and indexes are intentionally pinned.",
        ],
    }


def fixture():
    snippets=[]
    for name,(i,lam,holder,typ) in TARGETS.items():
        p=675+(i-67)*17
        snippets.extend([
          f"       {p}: ldc_w #1 // String {name}",
          f"       {p+3}: invokedynamic #2,  0 // InvokeDynamic #{i}:apply:()Ljava/util/function/Function;",
          f"       {p+8}: invokevirtual #3 // Method net/neoforged/neoforge/registries/DeferredRegister.register:(Ljava/lang/String;Ljava/util/function/Function;)Lnet/neoforged/neoforge/registries/DeferredHolder;",
          f"       {p+11}: putstatic #4 // Field {holder}:Lnet/neoforged/neoforge/registries/DeferredHolder;",
        ])
    b=[]
    for _,(i,lam,holder,typ) in TARGETS.items():
        b.extend([
          f"  {i}: #123 REF_invokeStatic java/lang/invoke/LambdaMetafactory.metafactory:(Ljava/lang/invoke/MethodType;)Ljava/lang/invoke/CallSite;",
          "    Method arguments:",
          "      #958 (Ljava/lang/Object;)Ljava/lang/Object;",
          f"      #567 REF_invokeStatic yesman/epicfight/registry/entries/EpicFightSkills.{lam}:(Lnet/minecraft/resources/ResourceLocation;)Lyesman/epicfight/skill/weaponinnate/{typ};",
          f"      #569 (Lnet/minecraft/resources/ResourceLocation;)Lyesman/epicfight/skill/weaponinnate/{typ};",
        ])
    return ("public class Fixture {\n  static {};\n    descriptor: ()V\n    Code:\n" +
            "\n".join(snippets) + "\n}\nBootstrapMethods:\n" + "\n".join(b) + "\nInnerClasses:")


class Tests(unittest.TestCase):
    def test_control(self):
        self.assertEqual(verify_linkage(fixture())["status"],
                         "PASS_BOUNDED_TRIDENT_REGISTRY_BOOTSTRAP_LINKAGE")

    def test_wrong_registry_literal(self):
        with self.assertRaisesRegex(ValueError, "initializer ID"):
            verify_linkage(fixture().replace("String tsunami", "String tidal_power"))

    def test_wrong_bootstrap_index(self):
        with self.assertRaisesRegex(ValueError, "wrong invokedynamic"):
            verify_linkage(fixture().replace("InvokeDynamic #68:apply", "InvokeDynamic #70:apply"))

    def test_wrong_holder(self):
        with self.assertRaisesRegex(ValueError, "registry holder"):
            verify_linkage(fixture().replace("Field TSUNAMI:", "Field WRONG:"))

    def test_wrong_registry_call(self):
        with self.assertRaisesRegex(ValueError, "DeferredRegister"):
            verify_linkage(fixture().replace("DeferredRegister.register:", "DeferredRegister.notRegister:"))

    def test_wrong_supplier_lambda(self):
        with self.assertRaisesRegex(ValueError, "expected supplier"):
            verify_linkage(fixture().replace("EpicFightSkills.lambda$static$42:", "EpicFightSkills.lambda$static$41:"))

    def test_wrong_supplier_return_type(self):
        with self.assertRaisesRegex(ValueError, "expected supplier"):
            verify_linkage(fixture().replace("ConditionalWeaponInnateSkill;", "WeaponInnateSkill;"))

    def test_duplicate_id_constant(self):
        t=fixture()
        insert="       800: ldc_w #1 // String tsunami\n"
        with self.assertRaisesRegex(ValueError, "exactly one initializer ID"):
            verify_linkage(t.replace("}\nBootstrapMethods:", insert+"}\nBootstrapMethods:"))

    def test_missing_bootstrap_section(self):
        with self.assertRaisesRegex(ValueError, "BootstrapMethods"):
            verify_linkage("public class Fixture {\n  static {};\n}")

    def test_wrong_bootstrap_metafactory(self):
        with self.assertRaisesRegex(ValueError, "missing or duplicate bootstrap"):
            verify_linkage(fixture().replace("LambdaMetafactory.metafactory", "LambdaMetafactory.fake"))


def main() -> int:
    parser=argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--jar",type=Path)
    parser.add_argument("--output",type=Path)
    a=parser.parse_args()
    if a.self_test:
        result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Tests))
        return 0 if result.wasSuccessful() else 1
    if not a.jar or not a.output:
        parser.error("--jar and --output required")
    try:
        prior=inspect_publisher(a.jar)
        phase=evaluate(javap(a.jar,REGISTRY))
        p=subprocess.run(["javap","-p","-c","-v","-classpath",str(a.jar),REGISTRY],
                         capture_output=True,text=True,timeout=90,check=False)
        if p.returncode:
            raise ValueError("javap verbose failed")
        result=verify_linkage(p.stdout)
        result["publisher_sha1"]=prior["sha1"]
        result["publisher_sha256"]=prior["sha256"]
        result["phase_prerequisite"]=phase["status"]
        result["selector_prerequisite"]=prior["status"]
    except (OSError,ValueError,subprocess.TimeoutExpired) as e:
        result={"status":"FAIL_CLOSED","deviations":[str(e)]}
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({"status":result["status"],"deviations":result.get("deviations",[])}))
    return 0 if result["status"]=="PASS_BOUNDED_TRIDENT_REGISTRY_BOOTSTRAP_LINKAGE" else 2


if __name__=="__main__":
    sys.exit(main())
