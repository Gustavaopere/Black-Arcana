#!/usr/bin/env python3
"""Bounded exact-JAR Backported Spellbooks 0.1.2 causal method proof.

Compiled callsites only: no runtime player, host config, gameplay, damage
frequency, effect-clamp, or right to mutate external provider state.
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

EXPECTED_SHA1 = "747847c1f38c73250ebac05ea06b41a381187850"
CLASSES = {
    "sulfur_cloud_projectile": "net.redreaper.backported_spellbooks.entities.spell.sulfur_clouds.SulfurCloudProjectile",
    "sulfur_release": "net.redreaper.backported_spellbooks.spells.nature.SulfurReleaseSpell",
    "resin_spray": "net.redreaper.backported_spellbooks.spells.nature.ResinSpraySpell",
}
METHOD = re.compile(r"^  (?:public|protected|private|static)\b.*\([^)]*\)(?: throws .+)?;$")
OPCODE = re.compile(r"^\s*(\d+):\s+([a-z][a-z0-9_]*)\b(.*)$")


def hash_and_zip(jar: Path) -> str:
    h = hashlib.sha1()
    with jar.open("rb") as file:
        for piece in iter(lambda: file.read(1024 * 1024), b""):
            h.update(piece)
    sha = h.hexdigest()
    if sha != EXPECTED_SHA1:
        raise ValueError(f"JAR_SHA_MISMATCH: expected {EXPECTED_SHA1}, observed {sha}")
    with zipfile.ZipFile(jar) as archive:
        bad = archive.testzip()
        if bad is not None:
            raise ValueError("JAR_ZIP_CRC_FAILURE: " + bad)
        entries = set(archive.namelist())
        for fqcn in CLASSES.values():
            if fqcn.replace(".", "/") + ".class" not in entries:
                raise ValueError("JAR_CLASS_MISSING: " + fqcn)
    return sha


def javap(jar: Path, clazz: str) -> str:
    return subprocess.run(["javap", "-p", "-c", "-classpath", str(jar), clazz],
                          capture_output=True, text=True, check=True).stdout


def blocks(dis: str):
    lines = dis.splitlines()
    result = []
    for i, line in enumerate(lines):
        if not METHOD.match(line):
            continue
        end = next((j for j in range(i + 1, len(lines))
                    if METHOD.match(lines[j]) or lines[j] == "}"), len(lines))
        if "Code:" in "\n".join(lines[i:end]):
            ops = []
            for row in lines[i:end]:
                if m := OPCODE.match(row):
                    ops.append((int(m.group(1)), m.group(2), m.group(3).strip()))
            result.append((line.strip(), ops))
    return result


def unique(dis: str, name: str):
    found = [(header, ops) for header, ops in blocks(dis) if f" {name}(" in header]
    if len(found) != 1 or not found[0][1]:
        raise ValueError(f"METHOD_MISSING_OR_AMBIGUOUS: {name} count={len(found)}")
    return found[0][1]


def callsite(ops, needle: str, minimum: int = 1, maximum: int = 1):
    found = [pc for pc, op, tail in ops if op.startswith("invoke") and needle in tail]
    if not minimum <= len(found) <= maximum:
        raise ValueError(f"CALLSITE_CARDINALITY_DRIFT: {needle} observed={len(found)}")
    return found


def ordered(ops, tokens):
    last = -1
    pcs = []
    for word in tokens:
        found = [pc for pc, op, tail in ops
                 if pc > last and word in tail and op.startswith("invoke")]
        if not found:
            raise ValueError(f"ORDERED_CALLSITE_MISSING: {word} after={last}")
        last = found[0]
        pcs.append(last)
    return pcs


def confirm_cloud_tick(ops):
    ticks = [(pc, tail) for pc, op, tail in ops
             if op == "invokespecial" and ".tick:()V" in tail]
    if len(ticks) != 2:
        raise ValueError(f"SULFUR_CLOUD_SUPER_TICK_DRIFT: {len(ticks)}")
    if ticks[0][1] != ticks[1][1]:
        raise ValueError("SULFUR_CLOUD_SUPER_TICK_OWNER_MISMATCH")
    particles = callsite(ops, "createParticleSphere:")
    if not ticks[0][0] < ticks[1][0] < particles[0]:
        raise ValueError("SULFUR_CLOUD_TICK_ORDER_DRIFT")
    return {"compiled_super_tick_invocations": 2,
            "pcs": [ticks[0][0], ticks[1][0]],
            "particle_call_pc": particles[0],
            "actual_tick_or_damage_multiplier": "NOT_VERIFIED"}


def confirm_release_amplifier(ops):
    sequence = [(op, tail) for _, op, tail in ops]
    if sequence != [("iload_1", ""), ("iconst_2", ""), ("isub", ""), ("ireturn", "")]:
        raise ValueError("SULFUR_RELEASE_AMPLIFIER_ARITHMETIC_DRIFT")
    return {"formula": "spellLevel - 2", "value_at_level_one": -1,
            "runtime_effect_clamp": "NOT_VERIFIED"}


def confirm_resin_session(ops):
    guards = ordered(ops, ["MagicData.isCasting:",
                           "MagicData.getCastingSpellId:",
                           "MagicData.getAdditionalCastData:",
                           "EntityCastData.getCastingEntity:"])
    if not any(op == "instanceof" and "EntityCastData" in tail
               for _, op, tail in ops):
        raise ValueError("RESIN_SPRAY_ENTITY_CAST_DATA_GUARD_MISSING")
    if not any(op == "instanceof" and "AbstractConeProjectile" in tail
               for _, op, tail in ops):
        raise ValueError("RESIN_SPRAY_CONE_PROJECTILE_GUARD_MISSING")
    active = callsite(ops, "AbstractConeProjectile.setDealDamageActive:")
    spawn = callsite(ops, "Level.addFreshEntity:")
    saved = callsite(ops, "MagicData.setAdditionalCastData:")
    if not guards[-1] < active[0] < spawn[0] < saved[0]:
        raise ValueError("RESIN_SPRAY_REUSE_AND_SPAWN_ORDER_DRIFT")
    if not any(op == "new" and "ResinSprayProjectile" in tail
               for pc, op, tail in ops if active[0] < pc < spawn[0]):
        raise ValueError("RESIN_SPRAY_NEW_PROJECTILE_BRANCH_MISSING")
    return {"guard_order_pcs": guards, "reuse_activation_pc": active[0],
            "fresh_entity_pc": spawn[0], "cast_data_store_pc": saved[0],
            "real_player_continuous_cast": "NOT_VERIFIED"}


def analyze(dis: dict[str, str]):
    if set(dis) != set(CLASSES):
        raise ValueError("REQUIRED_CLASS_SET_MISSING")
    return {"status": "PASS_BACKPORTED_012_BOUNDED_COMPILED_PERK_CONSUMERS",
            "evidence_class": "EXACT_PUBLISHER_BYTECODE_BOUNDED_METHODS",
            "cloud_tick": confirm_cloud_tick(unique(dis["sulfur_cloud_projectile"], "tick")),
            "release_amplifier": confirm_release_amplifier(unique(dis["sulfur_release"], "getWitherAmplifier")),
            "resin_continuous_session": confirm_resin_session(unique(dis["resin_spray"], "onCast")),
            "limitations": [
                "No live player, effect amplifier normalization or damage-rate observation.",
                "No source-build identity or installed Iron's config equality proven.",
                "Compiled callsites are not stable mutation APIs and grant no adapter."
            ]}


class Tests(unittest.TestCase):
    def test_cloud_two_ticks(self):
        ops = [(0, "invokespecial", "// Method A.tick:()V"),
               (5, "invokespecial", "// Method A.tick:()V"),
               (10, "invokevirtual", "// Method createParticleSphere:()V")]
        self.assertEqual(confirm_cloud_tick(ops)["compiled_super_tick_invocations"], 2)

    def test_cloud_one_tick_fails(self):
        with self.assertRaisesRegex(ValueError, "SUPER_TICK_DRIFT"):
            confirm_cloud_tick([(0, "invokespecial", "A.tick:()V"),
                                (10, "invokevirtual", "createParticleSphere:")])

    def test_cloud_owner_drift_fails(self):
        with self.assertRaisesRegex(ValueError, "OWNER_MISMATCH"):
            confirm_cloud_tick([(0, "invokespecial", "A.tick:()V"),
                                (5, "invokespecial", "B.tick:()V"),
                                (10, "invokevirtual", "createParticleSphere:")])

    def test_release_level_one(self):
        data = confirm_release_amplifier([(0, "iload_1", ""),
                                          (1, "iconst_2", ""),
                                          (2, "isub", ""),
                                          (3, "ireturn", "")])
        self.assertEqual(data["value_at_level_one"], -1)

    def test_release_changed_constant_fails(self):
        with self.assertRaisesRegex(ValueError, "ARITHMETIC_DRIFT"):
            confirm_release_amplifier([(0, "iload_1", ""),
                                       (1, "iconst_1", ""),
                                       (2, "isub", ""),
                                       (3, "ireturn", "")])

    @staticmethod
    def resin_fixture():
        calls = ["MagicData.isCasting:", "MagicData.getCastingSpellId:",
                 "MagicData.getAdditionalCastData:", "EntityCastData.getCastingEntity:"]
        ops = [(i*4, "invokevirtual", "Method " + v) for i, v in enumerate(calls)]
        return ops + [(20, "instanceof", "EntityCastData"),
                      (24, "instanceof", "AbstractConeProjectile"),
                      (28, "invokevirtual", "AbstractConeProjectile.setDealDamageActive:"),
                      (32, "new", "ResinSprayProjectile"),
                      (36, "invokevirtual", "Level.addFreshEntity:"),
                      (40, "invokevirtual", "MagicData.setAdditionalCastData:")]

    def test_resin_session_calls(self):
        self.assertEqual(confirm_resin_session(self.resin_fixture())["fresh_entity_pc"], 36)

    def test_resin_missing_store_fails(self):
        with self.assertRaisesRegex(ValueError, "CARDINALITY_DRIFT"):
            confirm_resin_session(self.resin_fixture()[:-1])

    def test_bad_sha_fails(self):
        from tempfile import TemporaryDirectory
        with TemporaryDirectory() as d:
            file = Path(d) / "bad.jar"
            file.write_bytes(b"not publisher content")
            with self.assertRaisesRegex(ValueError, "JAR_SHA_MISMATCH"):
                hash_and_zip(file)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--self-test", action="store_true")
    p.add_argument("--jar", type=Path)
    p.add_argument("--output", type=Path)
    args = p.parse_args()
    if args.self_test:
        result = unittest.TextTestRunner(verbosity=2).run(
            unittest.defaultTestLoader.loadTestsFromTestCase(Tests))
        return 0 if result.wasSuccessful() else 1
    if not args.jar or not args.output:
        p.error("--jar and --output required")
    try:
        sha1 = hash_and_zip(args.jar)
        data = analyze({key: javap(args.jar, clazz) for key, clazz in CLASSES.items()})
        data["publisher_sha1"] = sha1
        data["deviations"] = []
    except (OSError, ValueError, subprocess.CalledProcessError, zipfile.BadZipFile) as exc:
        data = {"status": "FAIL_CLOSED", "deviations": [str(exc)]}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": data["status"], "deviations": data["deviations"]}))
    return 0 if data["status"] == "PASS_BACKPORTED_012_BOUNDED_COMPILED_PERK_CONSUMERS" else 2


if __name__ == "__main__":
    sys.exit(main())
