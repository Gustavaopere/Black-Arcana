#!/usr/bin/env python3
"""Read-only, fail-closed Identity2 NBT restoration path probe (Java 21).

A direct restoration path proves only a bounded compiled call pattern. It does
not establish when login/respawn calls it, or whether a progression gate holds.
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

TARGET_CLASS = "net.Gabou.identity2.identity.IdentityProgression"
TARGET_FILE = "net/Gabou/identity2/identity/IdentityProgression.class"
RESTORE = "restoreMorphFromSavedData"
RESTORE_DECL = re.compile(
    r"^\s{2}public static void restoreMorphFromSavedData"
    r"\(net\.minecraft\.server\.level\.ServerPlayer\);$"
)
NEXT_METHOD = re.compile(r"^\s{2}(?:public|protected|private)\s+.+\([^;]*\);$")
INSTRUCTION = re.compile(
    r"^\s*(\d+):\s+([a-z][a-z0-9_]*)\b.*?"
    r"(?://\s*(?:InterfaceMethod|Method)\s+(.+))?$"
)
EXPECTED_DESCRIPTOR = "(Lnet/minecraft/server/level/ServerPlayer;)V"


def inspect_restore(javap_text: str) -> dict:
    lines = javap_text.splitlines()
    indexes = [i for i, line in enumerate(lines) if RESTORE_DECL.fullmatch(line)]
    if len(indexes) != 1:
        raise ValueError(f"expected exactly one public restore method, got {len(indexes)}")
    index = indexes[0]
    stop = next(
        (i for i in range(index + 1, len(lines)) if NEXT_METHOD.fullmatch(lines[i])),
        len(lines),
    )
    block = lines[index + 1:stop]
    if f"descriptor: {EXPECTED_DESCRIPTOR}" not in [x.strip() for x in block]:
        raise ValueError("restore(ServerPlayer):void descriptor missing")
    if "Code:" not in [x.strip() for x in block]:
        raise ValueError("restore method lacks bytecode")
    ins = [(int(m.group(1)), m.group(2), m.group(3) or "")
           for line in block if (m := INSTRUCTION.match(line))]
    if not ins:
        raise ValueError("restore method has no decoded instructions")
    direct = [(pc, symbol) for pc, op, symbol in ins
              if op.startswith("invoke") and "setCurrentIdentity:" in symbol]
    morph = [(pc, symbol) for pc, op, symbol in ins
             if op.startswith("invoke") and "IdentityProgression.morph:" in symbol]
    if not direct:
        raise ValueError("no direct EntityAccessor.setCurrentIdentity invocation found")
    if morph:
        raise ValueError("restore method invokes morph; cannot classify as direct-only")
    return {
        "status": "PASS_DIRECT_RESTORE_BOUNDED",
        "class": TARGET_CLASS,
        "method": RESTORE,
        "descriptor": EXPECTED_DESCRIPTOR,
        "direct_set_identity_offsets": [pc for pc, _ in direct],
        "morph_invocations": 0,
        "scope": "THIS_METHOD_ONLY_NOT_A_PROGRESSION_BYPASS_TEST",
    }


def audit(path: Path, sha1_expected: str) -> dict:
    if not re.fullmatch(r"[a-f0-9]{40}", sha1_expected):
        raise ValueError("expected SHA-1 must contain 40 lowercase hex digits")
    data = path.read_bytes()
    sha1 = hashlib.sha1(data).hexdigest()
    if sha1 != sha1_expected:
        raise ValueError(f"SHA-1 mismatch: {sha1}")
    with zipfile.ZipFile(path) as jar:
        if TARGET_FILE not in jar.namelist():
            raise ValueError("IdentityProgression class absent from pinned JAR")
        mods = [p for p in ("META-INF/neoforge.mods.toml", "META-INF/mods.toml")
                if p in jar.namelist()]
        if not mods or not any(
            re.search(r"""modId\s*=\s*["']identity2["']""", jar.read(p).decode("utf-8", "replace"))
            for p in mods
        ):
            raise ValueError("Identity2 NeoForge metadata not found")
    p = subprocess.run(
        ["javap", "-p", "-c", "-s", "-classpath", str(path), TARGET_CLASS],
        capture_output=True, text=True, check=False, timeout=90,
    )
    if p.returncode:
        raise ValueError(f"javap returned {p.returncode}: {p.stderr[:180]}")
    report = inspect_restore(p.stdout)
    report.update({
        "sha1": sha1,
        "sha256": hashlib.sha256(data).hexdigest(),
        "jar_bytes": len(data),
        "evidence_class": "PUBLISHER_BINARY_BOUNDED_RESTORE_ONLY",
        "limitations": [
            "No byte parity with the user's installed JAR was measured.",
            "No live login, respawn, permission revocation, or Mixin application was tested.",
            "A direct restore does not prove absence of policy checks in its callers.",
            "Identity2 owns morph state; RPG Skill Tree owns progression gates only.",
        ],
    })
    return report


SAMPLE = """public final class net.Gabou.identity2.identity.IdentityProgression {
  public static void restoreMorphFromSavedData(net.minecraft.server.level.ServerPlayer);
    descriptor: (Lnet/minecraft/server/level/ServerPlayer;)V
    Code:
       0: invokeinterface #1 // InterfaceMethod net/Gabou/identity2/util/EntityAccessor.setCurrentIdentity:(Ljava/lang/String;)V
       4: invokeinterface #2 // InterfaceMethod net/Gabou/identity2/util/EntityAccessor.setCurrentIdentity:(Ljava/lang/String;Lnet/minecraft/nbt/CompoundTag;)V
  public static boolean morph(net.minecraft.server.level.ServerPlayer, net.minecraft.resources.ResourceLocation, net.minecraft.nbt.CompoundTag);
    descriptor: (Lnet/minecraft/server/level/ServerPlayer;Lnet/minecraft/resources/ResourceLocation;Lnet/minecraft/nbt/CompoundTag;)Z
    Code:
       0: iconst_0
       1: ireturn
}"""


class Tests(unittest.TestCase):
    def test_direct_restore(self):
        self.assertEqual(inspect_restore(SAMPLE)["status"], "PASS_DIRECT_RESTORE_BOUNDED")

    def test_wrong_descriptor(self):
        with self.assertRaises(ValueError):
            inspect_restore(SAMPLE.replace(EXPECTED_DESCRIPTOR, "(I)V", 1))

    def test_missing_method(self):
        with self.assertRaises(ValueError):
            inspect_restore(SAMPLE.replace("restoreMorphFromSavedData", "unrelated", 1))

    def test_missing_direct_setter(self):
        with self.assertRaises(ValueError):
            inspect_restore(SAMPLE.replace("setCurrentIdentity:", "otherMethod:"))

    def test_restore_calls_morph(self):
        source = SAMPLE.replace(
            "       4: invokeinterface #2 // InterfaceMethod net/Gabou/identity2/util/EntityAccessor.setCurrentIdentity:",
            "       4: invokestatic #2 // Method net/Gabou/identity2/identity/IdentityProgression.morph:",
        )
        with self.assertRaises(ValueError):
            inspect_restore(source)

    def test_invalid_sha_fails_before_file_access(self):
        with self.assertRaisesRegex(ValueError, "40 lowercase"):
            audit(Path("missing.jar"), "invalid")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--jar", type=Path)
    parser.add_argument("--expected-sha1")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.self_test:
        result = unittest.TextTestRunner(verbosity=2).run(
            unittest.defaultTestLoader.loadTestsFromTestCase(Tests)
        )
        return 0 if result.wasSuccessful() else 1
    if not args.jar or not args.expected_sha1 or not args.output:
        parser.error("--jar, --expected-sha1 and --output are required")
    try:
        result = audit(args.jar, args.expected_sha1)
    except (OSError, ValueError, zipfile.BadZipFile, subprocess.TimeoutExpired) as exc:
        result = {
            "status": "FAIL_CLOSED",
            "evidence_class": "NO_BINARY_PROOF",
            "deviations": [str(exc)],
        }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"],
                      "deviations": result.get("deviations", [])}))
    return 0 if result["status"] == "PASS_DIRECT_RESTORE_BOUNDED" else 2


if __name__ == "__main__":
    sys.exit(main())
