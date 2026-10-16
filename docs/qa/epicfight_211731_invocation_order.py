#!/usr/bin/env python3
"""Exact-JAR bounded javap method invocation order. Not control-flow or runtime proof."""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import subprocess
import unittest

SHA1 = "fb199b7bbea2fc402da28ab586e73f47e32f8fc0"
SHA256 = "8b882554cf10086398340fbdc741819ee72a801a3adce516c7f4768326a39526"

# These are deliberately bounded call reference sequences inside one method.
# They do not prove that a conditional branch ever executes on server.
METHODS = {
    "yesman.epicfight.skill.Skill": {
        "loadDatapackParameters": [
            "CompoundTag.getFloat:", "CompoundTag.getInt:",
            "Map.clear:", "Codec.parse:", "Optional.ifPresent:",
        ],
    },
    "yesman.epicfight.skill.mover.PhantomAscentSkill": {
        "loadDatapackParameters": [
            "Skill.loadDatapackParameters:", "CompoundTag.getInt:",
            "CompoundTag.getDouble:",
        ],
    },
    "yesman.epicfight.skill.weaponinnate.EviscerateSkill": {
        "executeOnServer": [
            "playAnimationSynchronized:", "WeaponInnateSkill.executeOnServer:",
        ],
    },
    "yesman.epicfight.skill.weaponinnate.RushingTempoSkill": {
        "executeOnServer": [
            "Map.containsKey:", "playAnimationSynchronized:",
            "WeaponInnateSkill.executeOnServer:",
        ],
    },
    "yesman.epicfight.skill.weaponinnate.BladeRushSkill": {
        "checkExecuteCondition": [
            "LivingEntity.isAlive:", "distanceToSqr:",
        ],
    },
}

DECL = re.compile(r"^\s{2}(?:public|protected|private)\s+.*?\b([a-zA-Z_$][\w$]*)\([^;]*\);\s*$")
INST = re.compile(r"^\s*(\d+):\s+(\w+)\s+.*?(?://\s*(?:InterfaceMethod|Method|Field)\s+(.+))?$")


def method_instructions(javap_text: str, method: str) -> list[tuple[int, str, str]]:
    lines = javap_text.splitlines()
    headers = [(i, m.group(1)) for i, line in enumerate(lines) if (m := DECL.match(line))]
    matching = [k for k, (_, name) in enumerate(headers) if name == method]
    if len(matching) != 1:
        raise ValueError(f"{method}: expected one declaration, found {len(matching)}")
    k = matching[0]
    end = headers[k + 1][0] if k + 1 < len(headers) else len(lines)
    body = lines[headers[k][0] + 1:end]
    if not any(line.strip() == "Code:" for line in body):
        raise ValueError(f"{method}: no code section")
    instructions = []
    for line in body:
        m = INST.match(line)
        if m:
            instructions.append((int(m.group(1)), m.group(2), m.group(3) or ""))
    if not instructions:
        raise ValueError(f"{method}: empty code")
    return instructions


def check_order(instructions: list[tuple[int, str, str]], expected: list[str]) -> tuple[list[int], list[str]]:
    invocations = [(pc, ref) for pc, opcode, ref in instructions if opcode.startswith("invoke")]
    offsets = []
    failures = []
    prev = -1
    for fragment in expected:
        candidates = [pc for pc, ref in invocations if fragment in ref and pc > prev]
        if not candidates:
            failures.append(f"missing/unordered invocation: {fragment}")
        else:
            prev = candidates[0]
            offsets.append(prev)
    return offsets, failures


def audit(jar: pathlib.Path) -> dict:
    raw = jar.read_bytes()
    sha1, sha256 = hashlib.sha1(raw).hexdigest(), hashlib.sha256(raw).hexdigest()
    if (sha1, sha256) != (SHA1, SHA256):
        raise ValueError("publisher JAR does not match exact pack fingerprints")
    cases, failures = [], []
    for cls, methods in METHODS.items():
        p = subprocess.run(["javap", "-classpath", str(jar), "-p", "-c", cls],
                           capture_output=True, text=True, timeout=90, check=False)
        if p.returncode:
            failures.append(f"{cls}: javap returned {p.returncode}")
            continue
        for method, expected in methods.items():
            try:
                opcodes = method_instructions(p.stdout, method)
                offsets, deviations = check_order(opcodes, expected)
                failures.extend(f"{cls}.{method}: {failure}" for failure in deviations)
                cases.append({"class": cls, "method": method, "reference_order": expected,
                              "bytecode_offsets": offsets,
                              "result": "PASS_INVOCATION_ORDER_ONLY" if not deviations else "FAIL_CLOSED"})
            except ValueError as exc:
                failures.append(f"{cls}.{method}: {exc}")
    return {
        "provider": "epicfight", "exact_version": "21.17.3.1",
        "sha1": sha1, "sha256": sha256,
        "scope": "BOUNDED_METHOD_INVOCATION_ORDER_NOT_CONTROL_FLOW_OR_RUNTIME",
        "checked_methods": len(cases), "method_cases": cases,
        "deviations": failures,
        "result": "PASS_BOUNDED_ORDER" if not failures else "FAIL_CLOSED",
        "limits": [
            "Only ordered javap method references, no control-flow graph/branch proof.",
            "No loaded datapack, NBT codec acceptance, provider execution or actual world state.",
            "No event priority, sidedness, damage settlement, safety/adapter/Mastery acceptance.",
            "Reports contain references and instruction offsets only, not class bodies or publisher binaries.",
        ],
    }


SAMPLE = """public class Example {
  public void executeOnServer(yesman.epicfight.skill.SkillContainer);
    Code:
       0: aload_0
       1: invokevirtual #12                 // Method a/Player.playAnimationSynchronized:(I)V
       4: aload_0
       5: invokespecial #16                 // Method a/WeaponInnateSkill.executeOnServer:(II)V
       8: return

  public void other();
    Code:
       0: invokestatic #20                  // Method a/Foo.unrelated:()V
       3: return
}"""


class FlowTests(unittest.TestCase):
    def test_extract_bounded_to_method(self):
        seq = method_instructions(SAMPLE, "executeOnServer")
        self.assertEqual(len(seq), 2)
        self.assertFalse(any("unrelated" in ref for _, _, ref in seq))

    def test_expected_order(self):
        seq = method_instructions(SAMPLE, "executeOnServer")
        self.assertEqual(check_order(seq, ["playAnimationSynchronized:", "WeaponInnateSkill.executeOnServer:"]),
                         ([1, 5], []))

    def test_swapped_order_fails_closed(self):
        seq = method_instructions(SAMPLE, "executeOnServer")
        self.assertTrue(check_order(seq, ["WeaponInnateSkill.executeOnServer:", "playAnimationSynchronized:"])[1])

    def test_owner_independent_distance_method_keeps_invocation_requirement(self):
        ins = [(1, "invokevirtual", "a/LivingEntity.isAlive:()Z"),
               (5, "invokevirtual", "a/Entity.distanceToSqr:(La/LivingEntity;)D")]
        self.assertEqual(check_order(ins, ["LivingEntity.isAlive:", "distanceToSqr:"])[1], [])
        self.assertTrue(check_order(ins, ["LivingEntity.isAlive:", "distanceTo:"])[1])

    def test_another_method_cannot_satisfy(self):
        seq = method_instructions(SAMPLE, "executeOnServer")
        self.assertTrue(check_order(seq, ["unrelated:"])[1])

    def test_missing_method_fails_closed(self):
        with self.assertRaises(ValueError):
            method_instructions(SAMPLE, "absent")

    def test_duplicate_method_fails_closed(self):
        with self.assertRaises(ValueError):
            method_instructions(SAMPLE + "\n" + SAMPLE, "executeOnServer")

    def test_missing_code_fails_closed(self):
        with self.assertRaises(ValueError):
            method_instructions("  public void executeOnServer();", "executeOnServer")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--jar", type=pathlib.Path)
    p.add_argument("--output", type=pathlib.Path)
    p.add_argument("--self-test", action="store_true")
    args = p.parse_args()
    if args.self_test:
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(FlowTests)
        return int(not unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful())
    if not args.jar or not args.output:
        p.error("require --jar and --output")
    report = audit(args.jar)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({key: val for key, val in report.items() if key not in ("method_cases", "limits")}, indent=2))
    return 0 if report["result"] == "PASS_BOUNDED_ORDER" else 1


if __name__ == "__main__":
    raise SystemExit(main())
