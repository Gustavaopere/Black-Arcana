#!/usr/bin/env python3
"""Exact-release classfile audit for 24 Reliquified Iron's items / 25 relic roots.

This is a bounded, read-only JAR inspection. No Minecraft classes are loaded,
no publisher binary is committed and no in-game/Survival claim follows.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import stat
import subprocess
import zipfile
from pathlib import Path

EXPECTED_JAR = "reliquified_irons_spells_and_spellbooks-1.21.1-0.2.7.jar"
EXPECTED_SHA1 = "e22fd94c87cb88b3cfa4637c48a1058260d35a9b"
MOD_ID = "reliquified_irons_spells_and_spellbooks"
PACKAGE = "it.hurts.shatterbyte.reliquified_irons_spells_and_spellbooks"
REGISTRY_CLASS = f"{PACKAGE}.init.RISASItems"
ITEM_PACKAGE = f"{PACKAGE}.items"
EVIDENCE = "EXACT_HASH_STATIC_ITEMS_AND_ABILITY_TEMPLATE_CALLS_NOT_RUNTIME_QA"
MAX_BYTES = 16 * 1024 * 1024
MAX_JAVAP_OUTPUT = 3 * 1024 * 1024

# Item ID / class / primary AbilityTemplate.builder(String) IDs, source pinned:
# Octo-Studios/reliquified-irons-spells-n-spellbooks@1dfa5557ae3ae59c793682bd8e386f81d7feaa32.
EXPECTED = (
    ("hat_of_omniscience", "HatOfOmniscienceItem", ()),
    ("bloody_voodoo_doll", "BloodyVoodooDollItem", ("voodoo_mark",)),
    ("cardiac_trap", "CardiacTrapItem", ("cardiac_trap",)),
    ("flask_of_the_red_mist", "FlaskOfTheRedMistItem", ("red_mist",)),
    ("living_flesh", "LivingFleshItem", ("living_flesh",)),
    ("sinner_crown", "SinnerCrownItem", ("sinner_crown",)),
    ("slicer", "SlicerItem", ("slicer_weapon", "slicer")),
    ("cloak_of_the_bloody_feather", "CloakOfTheBloodyFeatherItem", ("blood_feather",)),
    ("mask_of_hunger", "MaskOfHungerItem", ("hunger_mask",)),
    ("ring_of_blades", "RingOfBladesItem", ("ring_of_blades",)),
    ("dimension_key", "DimensionKeyItem", ("dimension_key",)),
    ("dragon_blood_vial", "DragonBloodVialItem", ("dragon_blood",)),
    ("echo_glove", "EchoGloveItem", ("echo_glove",)),
    ("ender_bow", "EnderBowItem", ("ender_bow",)),
    ("galaxy_devourer_diadem", "GalaxyDevourerDiademItem", ("galaxy_devourer_diadem",)),
    ("immaterial_disperser", "ImmaterialDisperserItem", ("immaterial_disperser",)),
    ("lunar_sextant", "LunarSextantItem", ("lunar_sextant",)),
    ("sealed_sword", "SealedSwordItem", ("sealed_sword",)),
    ("sealed_rapier", "SealedRapierItem", ("sealed_rapier",)),
    ("sealed_claymore", "SealedClaymoreItem", ("sealed_claymore",)),
    ("mirror_of_transgression", "MirrorOfTransgressionItem", ("mirror_of_transgression",)),
    ("pulsar_mantle", "PulsarMantleItem", ("pulsar_mantle",)),
    ("ring_of_elusiveness", "RingOfElusivenessItem", ("elusiveness",)),
    ("shadow_claws", "ShadowClawsItem", ("shadow_claws", "shadow_slash")),
)
ID_RE = re.compile(r"^[a-z][a-z0-9_]*$")
INSTRUCTION = re.compile(r"^\s*\d+:\s+([a-z][a-z0-9_]+)\b")
PUBLIC_FIELD = re.compile(
    r"^\s*public static final [^\n]*DeferredHolder[^\n]*\s+([A-Z][A-Z0-9_]*);$",
    re.M,
)


class AuditError(Exception):
    pass


def instructions(disassembly: str) -> list[tuple[str, str]]:
    result = []
    for line in disassembly.splitlines():
        prefix, _, comment = line.partition("//")
        m = INSTRUCTION.match(prefix)
        if m:
            result.append((m.group(1), comment.strip()))
    return result


def static_items(disassembly: str) -> tuple[list[tuple[str, str]], list[str]]:
    """Require source-compatible register(ID,Supplier) followed by putstatic."""
    if disassembly.count("  static {};") != 1:
        raise AuditError("RISASItems static initializer missing/ambiguous")
    head, body = disassembly.split("  static {};", 1)
    fields = PUBLIC_FIELD.findall(head)
    instr = instructions(body)
    pairs = []
    for i in range(len(instr) - 4):
        (p, c), (op0, c0), (op1, c1), (op2, c2), (op3, c3) = instr[i:i + 5]
        if (p != "getstatic" or "ITEMS:" not in c
                or op0 not in ("ldc", "ldc_w") or not c0.startswith("String ")
                or op1 != "invokedynamic"
                or op2 not in ("invokevirtual", "invokeinterface")
                or "DeferredRegister" not in c2 or ".register:" not in c2
                or "(Ljava/lang/String;Ljava/util/function/Supplier;)" not in c2
                or op3 != "putstatic" or "Field " not in c3):
            continue
        ident = c0[len("String "):]
        field = re.search(r"\bField (?:[^\s:]+\.)?([A-Z][A-Z0-9_]*):", c3)
        if not ID_RE.fullmatch(ident) or not field:
            raise AuditError("malformed item ID or field")
        pairs.append((ident, field.group(1)))
    return pairs, fields


def ability_roots(disassembly: str) -> list[str]:
    """Read only AbilityTemplate.builder(String) direct compiled calls."""
    instr = instructions(disassembly)
    result = []
    for before, call in zip(instr, instr[1:]):
        op, comment = before
        next_op, next_comment = call
        if (op in ("ldc", "ldc_w") and comment.startswith("String ")
                and next_op == "invokestatic"
                and "AbilityTemplate.builder:" in next_comment
                and "(Ljava/lang/String;)" in next_comment):
            ident = comment[len("String "):]
            if not ID_RE.fullmatch(ident):
                raise AuditError("invalid primary ability ID constant")
            result.append(ident)
    return result


def verify(outputs: dict[str, str], expected=EXPECTED) -> dict:
    if len(expected) != len({x[0] for x in expected}) or len(expected) != len({x[1] for x in expected}):
        raise AuditError("audited item specification contains duplicate IDs/classes")
    if "registry" not in outputs:
        raise AuditError("registry bytecode not available")
    pairs, fields = static_items(outputs["registry"])
    listed = {id: klass for id, klass, _ in expected}
    want_pairs = {(id, id.upper()) for id in listed}
    observed_pairs = set(pairs)
    deviations = {
        "missing_item_pairs": sorted(f"{a}:{b}" for a,b in want_pairs - observed_pairs),
        "unexpected_item_pairs": sorted(f"{a}:{b}" for a,b in observed_pairs - want_pairs),
        "duplicate_item_pairs": len(pairs) != len(observed_pairs),
        "declared_fields_without_registration": sorted(set(fields) - {b for _,b in pairs}),
        "extra_unexpected_fields": sorted({b for _,b in pairs} - set(fields)),
        "registered_item_count_wrong": len(pairs) != len(expected),
    }
    observed = {}
    for id, klass, expected_abilities in expected:
        if klass not in outputs:
            observed[klass] = []
            deviations[f"{id}_missing_class"] = True
            continue
        actual = ability_roots(outputs[klass])
        observed[klass] = actual
        if len(actual) != len(expected_abilities) or set(actual) != set(expected_abilities):
            deviations[f"{id}_ability_mismatch"] = {
                "expected": list(expected_abilities), "observed": actual,
            }
    all_abilities = [x for values in observed.values() for x in values]
    if len(all_abilities) != len(set(all_abilities)):
        deviations["duplicate_ability_roots"] = True
    if len(all_abilities) != sum(len(row[2]) for row in expected):
        deviations["ability_root_count_wrong"] = len(all_abilities)
    return {
        "status": "PASS" if not any(deviations.values()) else "UNPROVEN_OR_MISMATCH",
        "items_expected": len(expected),
        "items_observed": len(pairs),
        "abilities_expected": sum(len(v[2]) for v in expected),
        "abilities_observed": len(all_abilities),
        "ability_bearing_classes_observed": sum(bool(v) for v in observed.values()),
        "deviations": {k: v for k, v in deviations.items() if v},
    }


def audit(jar: Path, javap="javap", *, expected_sha1=EXPECTED_SHA1, expected=EXPECTED) -> dict:
    if jar.name != EXPECTED_JAR or jar.is_symlink() or not jar.is_file():
        raise AuditError("unrecognized name, non-regular file or symlink")
    before = jar.stat()
    sig = lambda s: (s.st_dev, s.st_ino, s.st_size, s.st_mtime_ns, s.st_ctime_ns)
    if not stat.S_ISREG(before.st_mode) or not 0 < before.st_size <= MAX_BYTES:
        raise AuditError("oversized/empty/nonregular JAR")
    data = jar.read_bytes()
    if sig(jar.stat()) != sig(before):
        raise AuditError("JAR changed during read")
    sha1, sha256 = hashlib.sha1(data).hexdigest(), hashlib.sha256(data).hexdigest()
    if sha1 != expected_sha1:
        raise AuditError(f"publisher/physical SHA-1 mismatch, observed {sha1}")
    klasses = {REGISTRY_CLASS, *(f"{ITEM_PACKAGE}.{name}" for _, name, _ in expected)}
    with zipfile.ZipFile(io.BytesIO(data)) as arc:
        names = arc.namelist()
        if len(names) != len(set(names)):
            raise AuditError("duplicate ZIP member entries")
        for name in klasses:
            if name.replace(".", "/") + ".class" not in names:
                raise AuditError(f"missing required class {name}")
        try:
            metadata = arc.read("META-INF/neoforge.mods.toml")
        except KeyError as ex:
            raise AuditError("NeoForge mod metadata missing") from ex
        if len(metadata) > 256_000 or not re.search(
            rb'\bmodId\s*=\s*["\x27]reliquified_irons_spells_and_spellbooks["\x27]', metadata
        ):
            raise AuditError("NeoForge mod ID mismatch")
    outputs = {}
    for name in sorted(klasses):
        try:
            run = subprocess.run(
                [javap, "-c", "-p", "-classpath", str(jar.resolve()), name],
                capture_output=True, text=True, timeout=25, check=False,
            )
        except (OSError, subprocess.TimeoutExpired) as ex:
            raise AuditError(f"javap unavailable/timeout for {name}") from ex
        if run.returncode or len(run.stdout) > MAX_JAVAP_OUTPUT:
            raise AuditError(f"javap failed/too much output for {name}")
        outputs["registry" if name == REGISTRY_CLASS else name.rsplit(".",1)[1]] = run.stdout
    if sig(jar.stat()) != sig(before) or hashlib.sha1(jar.read_bytes()).hexdigest() != sha1:
        raise AuditError("JAR changed during javap inspection")
    report = verify(outputs, expected)
    return {
        "evidence_class": EVIDENCE,
        "provider": MOD_ID,
        "version": "0.2.7",
        "filename": jar.name,
        "size_bytes": len(data),
        "sha1": sha1, "sha256": sha256,
        "result": report["status"],
        "registry": report,
        "not_proven": [
            "exact source/bytecode equality beyond audited callsites",
            "provider loaded by NeoForge in assembled modpack",
            "real client/dedicated server and item acquisition",
            "Relics rank and progression", "Iron's mana/cooldown",
            "loaded configs, claims and Survival", "RPG Mastery adapter",
        ],
    }


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--jar", type=Path, required=True)
    p.add_argument("--output", type=Path)
    args = p.parse_args()
    try:
        result = audit(args.jar)
        code = 0 if result["result"] == "PASS" else 1
    except (AuditError, OSError, UnicodeError, zipfile.BadZipFile) as ex:
        result = {"evidence_class": "UNVERIFIED", "result": "FAIL_CLOSED", "reason": str(ex)}
        code = 1
    rendered = json.dumps(result, indent=2, sort_keys=True)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
