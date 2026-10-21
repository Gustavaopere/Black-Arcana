#!/usr/bin/env python3
"""Fail-closed Identity2 NeoForge classfile signature check; not runtime proof."""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import subprocess
import sys
import unittest
import zipfile

MORPH_CLASS = "net.Gabou.identity2.identity.IdentityProgression"
MORPH_FILE = "net/Gabou/identity2/identity/IdentityProgression.class"
MORPH_DESC = ("(Lnet/minecraft/server/level/ServerPlayer;"
              "Lnet/minecraft/resources/ResourceLocation;"
              "Lnet/minecraft/nbt/CompoundTag;)Z")
DECL = re.compile(r"^\s{2}(?:public|protected|private)\s+.*?\b([\w$]+)\([^;]*\);\s*$")
INST = re.compile(r"^\s*(\d+):\s+(\w+)\b.*?(?://\s*(?:InterfaceMethod|Method|Field)\s+(.+))?$")
CASES = {
    "net.Gabou.identity2.ModPackets": ("net/Gabou/identity2/ModPackets.class",
                                      ("resolvePrimaryAbilityCooldown", "handleIdentityAbilityPacket")),
    "net.Gabou.identity2.mixin.EntityMixin": ("net/Gabou/identity2/mixin/EntityMixin.class",
                                              ("identity2$baseTick",)),
    "net.Gabou.identity2.Identity2Client": ("net/Gabou/identity2/Identity2Client.class",
                                           ("onClientTickEnd",)),
}

def method_opcodes(text: str, name: str):
    lines = text.splitlines()
    headers = [(i, m.group(1)) for i, line in enumerate(lines) if (m := DECL.match(line))]
    matches = [i for i, (_, method) in enumerate(headers) if method == name]
    if len(matches) != 1:
        raise ValueError(f"{name}: expected one declared method, found {len(matches)}")
    k = matches[0]
    stop = headers[k + 1][0] if k + 1 < len(headers) else len(lines)
    body = lines[headers[k][0] + 1:stop]
    if not any(line.strip() == "Code:" for line in body):
        raise ValueError(f"{name}: no Code section")
    ins = [(int(m.group(1)), m.group(2), m.group(3) or "")
           for line in body if (m := INST.match(line))]
    if not ins:
        raise ValueError(f"{name}: no bytecode instructions")
    return ins

def invocation_order(ins, refs):
    offsets, last = [], -1
    for ref in refs:
        matches = [pc for pc, op, symbol in ins
                   if pc > last and op.startswith("invoke") and ref in symbol]
        if not matches:
            raise ValueError(f"missing/unordered invocation: {ref}")
        last = matches[0]
        offsets.append(last)
    return offsets

def evaluate(javap_by_class):
    checks, deviations = [], []
    for cls, (_, methods) in CASES.items():
        for method in methods:
            try:
                ins = method_opcodes(javap_by_class[cls], method)
                if method == "resolvePrimaryAbilityCooldown":
                    offsets = invocation_order(ins, ("IdentityAbilityDefinition.cooldown:",
                                                     "IdentityAbilityDefinition.useduration:", "Math.max:"))
                    if not any(op == "iadd" and offsets[1] < pc < offsets[2] for pc, op, _ in ins):
                        raise ValueError("expected iadd between useduration and Math.max")
                elif method == "handleIdentityAbilityPacket":
                    offsets = invocation_order(ins, ("getAbilityCooldown:", "setAbilityCooldown:",
                                                     "BuiltinIdentityAbility.execute:"))
                elif method == "identity2$baseTick":
                    offsets = [pc for pc, op, _ in ins if op == "isub"]
                    if len(offsets) < 2:
                        raise ValueError("expected two counter decrements")
                else:
                    offsets = invocation_order(ins, ("setAbilityCooldown:", "sendIdentityAbilityPacket:"))
                checks.append({"class": cls, "method": method, "offsets": offsets[:4],
                               "status": "PASS_BOUNDED_SIGNATURE"})
            except (ValueError, KeyError) as exc:
                deviations.append(f"{cls}.{method}: {exc}")
                checks.append({"class": cls, "method": method, "status": "FAIL_CLOSED"})
    return {"result": "PASS_BOUNDED_SIGNATURES" if not deviations else "FAIL_CLOSED",
            "checks": checks, "deviations": deviations}

def morph_target_check(javap_signatures: str):
    """Exact mixin entry signature, not proof that a Mixin applied."""
    lines = javap_signatures.splitlines()
    found = []
    for i, line in enumerate(lines[:-1]):
        if re.match(r"^\s{2}public static boolean morph\(", line):
            descriptor = lines[i + 1].strip()
            found.append(descriptor)
    if "descriptor: " + MORPH_DESC not in found:
        raise ValueError("IdentityProgression.morph three-argument static descriptor absent")
    return {"class": MORPH_CLASS, "method": "morph", "descriptor": MORPH_DESC,
            "status": "PASS_MIXIN_TARGET_SIGNATURE_ONLY"}

def audit(jar_path, expected_sha1):
    if not re.fullmatch("[a-fA-F0-9]{40}", expected_sha1):
        raise ValueError("expected SHA-1 must be exactly 40 hex characters")
    raw = jar_path.read_bytes()
    sha1 = hashlib.sha1(raw).hexdigest()
    if sha1 != expected_sha1.lower():
        raise ValueError(f"SHA-1 mismatch: {sha1} != {expected_sha1.lower()}")
    with zipfile.ZipFile(jar_path) as archive:
        files = set(archive.namelist())
        absent = [name for name, _ in CASES.values() if name not in files]
        if MORPH_FILE not in files:
            absent.append(MORPH_FILE)
        if absent:
            raise ValueError(f"missing required classfiles: {absent}")
        metadata = [name for name in ("META-INF/neoforge.mods.toml", "META-INF/mods.toml")
                    if name in files]
        if not metadata:
            raise ValueError("missing NeoForge mod metadata")
        contents = "\n".join(archive.read(name).decode("utf-8", "replace") for name in metadata)
        if not re.search(r"""(?i)modId\s*=\s*["']identity2["']""", contents):
            raise ValueError("not an identity2 NeoForge JAR")
    javap = {}
    for cls in CASES:
        p = subprocess.run(["javap", "-classpath", str(jar_path), "-p", "-c", cls],
                           capture_output=True, text=True, check=False, timeout=90)
        if p.returncode:
            raise ValueError(f"{cls}: javap exit {p.returncode}: {p.stderr[:180]}")
        javap[cls] = p.stdout
    report = evaluate(javap)
    target = subprocess.run(["javap", "-classpath", str(jar_path), "-p", "-s", MORPH_CLASS],
                            capture_output=True, text=True, check=False, timeout=90)
    if target.returncode:
        raise ValueError(f"{MORPH_CLASS}: javap -s exit {target.returncode}")
    try:
        report["morph_target"] = morph_target_check(target.stdout)
    except ValueError as exc:
        report["deviations"].append(str(exc))
        report["result"] = "FAIL_CLOSED"
    report.update({"sha1": sha1, "sha256": hashlib.sha256(raw).hexdigest(),
                   "jar_bytes": len(raw), "provider": "identity2",
                   "target": "NeoForge 1.21.1 / reported 2.2.4",
                   "evidence_class": "BOUNDED_CLASSFILE_SIGNATURES_NOT_RUNTIME",
                   "limitations": [
                       "SHA must be independently compared against the installed JAR.",
                       "Morph descriptor proves only a target signature, not Mixin injection or progression gates.",
                       "Ordered method opcodes do not prove branches are reached.",
                       "No accepted casts, client sync, Wixie exception, or Mastery observations.",
                       "No per-player cooldown modification API approved."]})
    return report

EXAMPLE = {
    "net.Gabou.identity2.ModPackets": """class A {
  private static int resolvePrimaryAbilityCooldown(Object, Object);
    Code:
       0: invokevirtual #1 // Method a/IdentityAbilityDefinition.cooldown:()I
       3: invokevirtual #2 // Method a/IdentityAbilityDefinition.useduration:()I
       6: iadd
       7: invokestatic #3 // Method java/lang/Math.max:(II)I
  private static void handleIdentityAbilityPacket(Object, Object);
    Code:
       0: invokeinterface #4 // InterfaceMethod a/EntityAccessor.getAbilityCooldown:()I
       3: invokeinterface #5 // InterfaceMethod a/EntityAccessor.setAbilityCooldown:(I)V
       6: invokeinterface #6 // InterfaceMethod a/BuiltinIdentityAbility.execute:(I)V
}""",
    "net.Gabou.identity2.mixin.EntityMixin": """class B {
  private void identity2$baseTick(Object);
    Code:
       0: iconst_1
       1: isub
       2: iconst_1
       3: isub
}""",
    "net.Gabou.identity2.Identity2Client": """class C {
  private static void onClientTickEnd(Object);
    Code:
       0: invokeinterface #1 // InterfaceMethod a/EntityAccessor.setAbilityCooldown:(I)V
       3: invokestatic #2 // Method a/Identity2Client.sendIdentityAbilityPacket:(I)V
}""",
}

class ContractTests(unittest.TestCase):
    def test_fixture(self):
        self.assertEqual(evaluate(EXAMPLE)["result"], "PASS_BOUNDED_SIGNATURES")
    def test_wrong_method(self):
        altered = dict(EXAMPLE)
        altered["net.Gabou.identity2.ModPackets"] = altered["net.Gabou.identity2.ModPackets"].replace(
            "resolvePrimaryAbilityCooldown", "wrongName")
        self.assertEqual(evaluate(altered)["result"], "FAIL_CLOSED")
    def test_missing_iadd(self):
        altered = dict(EXAMPLE)
        altered["net.Gabou.identity2.ModPackets"] = altered["net.Gabou.identity2.ModPackets"].replace(
            "       6: iadd", "       6: nop")
        self.assertEqual(evaluate(altered)["result"], "FAIL_CLOSED")
    def test_wrong_order(self):
        seq = method_opcodes(EXAMPLE["net.Gabou.identity2.ModPackets"], "handleIdentityAbilityPacket")
        with self.assertRaises(ValueError):
            invocation_order(seq, ("setAbilityCooldown:", "getAbilityCooldown:"))
    def test_missing_second_counter(self):
        altered = dict(EXAMPLE)
        altered["net.Gabou.identity2.mixin.EntityMixin"] = altered[
            "net.Gabou.identity2.mixin.EntityMixin"].replace("       3: isub", "       3: iadd")
        self.assertEqual(evaluate(altered)["result"], "FAIL_CLOSED")
    def test_morph_signature_gate(self):
        good = ("  public static boolean morph(a.ServerPlayer, a.ResourceLocation, a.CompoundTag);\n"
                "    descriptor: " + MORPH_DESC + "\n")
        self.assertEqual(morph_target_check(good)["status"], "PASS_MIXIN_TARGET_SIGNATURE_ONLY")

    def test_wrong_morph_overload_rejected(self):
        wrong = ("  public static boolean morph(a.ServerPlayer, a.ResourceLocation);\n"
                 "    descriptor: (La/Player;La/Location;)Z\n")
        with self.assertRaises(ValueError):
            morph_target_check(wrong)

    def test_bad_checksum_rejected_before_access(self):
        with self.assertRaisesRegex(ValueError, "40 hex"):
            audit(pathlib.Path("missing.jar"), "not-a-hash")

def main():
    args = argparse.ArgumentParser()
    args.add_argument("--self-test", action="store_true")
    args.add_argument("--jar", type=pathlib.Path)
    args.add_argument("--expected-sha1")
    args.add_argument("--output", type=pathlib.Path)
    p = args.parse_args()
    if p.self_test:
        result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(ContractTests))
        return 0 if result.wasSuccessful() else 1
    if not p.jar or not p.expected_sha1 or not p.output:
        args.error("audit requires --jar, --expected-sha1, and --output")
    try:
        result = audit(p.jar, p.expected_sha1)
    except (OSError, ValueError, zipfile.BadZipFile, subprocess.TimeoutExpired) as exc:
        result = {"result": "FAIL_CLOSED", "deviations": [str(exc)],
                  "evidence_class": "UNVERIFIED_BINARY"}
    p.output.parent.mkdir(parents=True, exist_ok=True)
    p.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"result": result["result"], "deviations": result.get("deviations", [])}))
    return 0 if result["result"].startswith("PASS") else 2

if __name__ == "__main__":
    sys.exit(main())
