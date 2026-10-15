#!/usr/bin/env python3
"""Hazen 1.4.0.14 read-only classfile registry evidence (not modpack gameplay)."""
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

ROOT = Path(__file__).resolve().parents[2]
INVENTORY = ROOT / "wiki/modpack-catalog/providers/✅-hazen-n-stuff/SOURCE-1.4.0.14-SPELL-INVENTORY.md"
EXPECTED_FILENAME = "hazennstuff-1.4.0.14.jar"
EXPECTED_SHA1 = "3be20bacb44c1923348ab6f61b685eec6aacfdcd"
MOD_ID = "hazennstuff"
REGISTRY_CLASS = "net.hazen.hazennstuff.Spells.HnSSpellRegistries"
MAX_JAR_BYTES = 20 * 1024 * 1024
MAX_DISASSEMBLY = 4 * 1024 * 1024
EVIDENCE_CLASS = "EXACT_HASH_HAZEN_STATIC_38_SPELL_REGISTRATIONS_NOT_RUNTIME_QA"

INVENTORY_LINE = re.compile(
    r"^\|\s*\d+\s*\|[^|\n]+\|\s*`hazennstuff:([a-z][a-z0-9_]*)`\s*\|"
    r"[^|\n]+\|\s*`([A-Za-z][A-Za-z0-9]*)`\s*\|", re.M
)
OPCODE = re.compile(r"^\s*\d+:\s+([a-z][a-z0-9_]*)\b")
FIELD = re.compile(
    r"^\s*public static final java\.util\.function\.Supplier[^\n]*\s+([A-Z][A-Z0-9_]*);$",
    re.M,
)


class AuditError(Exception):
    """Fail-closed evidence gate, not a claim of provider incompatibility."""


def inventory_pairs(content: str, expected_count: int = 38) -> list[tuple[str, str]]:
    pairs = INVENTORY_LINE.findall(content)
    if len(pairs) != expected_count or len(pairs) != len(set(pairs)):
        raise AuditError(f"catalog inventory count/uniqueness mismatch: {len(pairs)}")
    ids, classes = [x for x, _ in pairs], [x for _, x in pairs]
    if len(ids) != len(set(ids)) or len(classes) != len(set(classes)):
        raise AuditError("catalog duplicate spell ID or concrete class")
    return pairs


def opcodes(disassembly: str) -> list[tuple[str, str]]:
    result = []
    for line in disassembly.splitlines():
        before, sep, after = line.partition("//")
        match = OPCODE.match(before)
        if match:
            result.append((match.group(1), after.strip() if sep else ""))
    return result


def static_spell_pairs(disassembly: str) -> tuple[list[tuple[str, str]], list[str]]:
    if disassembly.count("  static {};") != 1:
        raise AuditError("HnSSpellRegistries.<clinit> not uniquely located")
    declaration, clinit = disassembly.split("  static {};", 1)
    fields = FIELD.findall(declaration)
    steps = opcodes(clinit)
    pairs: list[tuple[str, str]] = []
    for i in range(len(steps) - 4):
        (a, ca), (b, cb), (c, cc), (d, cd), (e, ce) = steps[i:i + 5]
        if not (
            a == "new" and ca.startswith("class ")
            and b == "dup"
            and c == "invokespecial" and ('"<init>"' in cc or ".<init>" in cc)
            and d == "invokestatic" and "registerSpell:" in cd
            and e == "putstatic" and "Field " in ce
        ):
            continue
        classname = ca[len("class "):].split("/")[-1]
        name_match = re.search(r"\bField (?:[A-Za-z0-9_/$]+\.)?([A-Z][A-Z0-9_]*):", ce)
        if not name_match:
            raise AuditError("field after registerSpell is not identifiable")
        pairs.append((classname, name_match.group(1)))
    return pairs, fields


def class_identity(disassembly: str, simple_class: str, spell_id: str) -> bool:
    """Require constructor path to install exact ResourceLocation and getter to return it."""
    # Javap classfile listings are not a loaded runtime. Require the semantic
    # name literal together with a ResourceLocation factory and spellId storage.
    ctor = re.search(
        r"(?ms)^  public (?:[A-Za-z0-9_$.]+\.)?"
        + re.escape(simple_class) + r"\(\);\n(?P<body>.*?)(?=^  (?:public|private|protected|static) |\Z)",
        disassembly,
    )
    getter = re.search(
        r"(?ms)^  public net\.minecraft\.resources\.ResourceLocation getSpellResource\(\);\n"
        r"(?P<body>.*?)(?=^  (?:public|private|protected|static) |\Z)",
        disassembly,
    )
    if not ctor or not getter:
        return False
    ops = opcodes(ctor.group("body"))
    found = False
    for i, (opcode, comment) in enumerate(ops):
        if opcode not in ("ldc", "ldc_w") or comment != "String " + MOD_ID:
            continue
        if i + 2 >= len(ops):
            continue
        if ops[i + 1][0] not in ("ldc", "ldc_w") or ops[i + 1][1] != "String " + spell_id:
            continue
        if ops[i + 2][0] != "invokestatic" or "ResourceLocation.fromNamespaceAndPath:" not in ops[i + 2][1]:
            continue
        if any(op == "putfield" and "spellId:" in c for op, c in ops[i + 3:i + 8]):
            found = True
            break
    getter_ops = opcodes(getter.group("body"))
    returns_field = any(op == "getfield" and "spellId:" in c for op, c in getter_ops)
    return found and returns_field and any(op == "areturn" for op, _ in getter_ops)


def reconcile(catalog: list[tuple[str, str]], registry: str,
              classes: dict[str, str]) -> dict:
    pairs, declared_fields = static_spell_pairs(registry)
    observed_pairs = set(pairs)
    expected_pairs = {(cls, id.upper()) for id, cls in catalog}
    seen_classes = [cls for cls, _ in pairs]
    seen_fields = [field for _, field in pairs]
    errors = {
        "missing_class_field_pairs": sorted(f"{x}/{y}" for x, y in expected_pairs - observed_pairs),
        "unexpected_class_field_pairs": sorted(f"{x}/{y}" for x, y in observed_pairs - expected_pairs),
        "duplicate_registration_classes": len(seen_classes) != len(set(seen_classes)),
        "duplicate_registration_fields": len(seen_fields) != len(set(seen_fields)),
        "declared_fields_without_registration": sorted(set(declared_fields) - set(seen_fields)),
        "registered_fields_not_declared": sorted(set(seen_fields) - set(declared_fields)),
        "registration_count_mismatch": len(pairs) != len(catalog),
        "missing_or_mismatched_class_spell_ids": sorted(
            id for id, cls in catalog if cls not in classes or not class_identity(classes[cls], cls, id)
        ),
    }
    return {
        "status": "PASS" if not any(errors.values()) else "UNPROVEN_OR_MISMATCH",
        "expected": len(catalog),
        "compiled_registration_pairs": len(pairs),
        "compiled_unique_classes": len(set(seen_classes)),
        "exact_spell_id_class_match_count": len(catalog) - len(errors["missing_or_mismatched_class_spell_ids"]),
        "deviations": {k: v for k, v in errors.items() if v},
    }


def audit(jar: Path, inventory: str, *, expected_sha1=EXPECTED_SHA1, javap="javap") -> dict:
    if jar.name != EXPECTED_FILENAME or not jar.is_file() or jar.is_symlink():
        raise AuditError("wrong JAR name, symlink or non-regular file")
    initial = jar.stat()
    signature = lambda st: (st.st_dev, st.st_ino, st.st_size, st.st_ctime_ns, st.st_mtime_ns)
    if not stat.S_ISREG(initial.st_mode) or not 0 < initial.st_size <= MAX_JAR_BYTES:
        raise AuditError("unbounded/empty JAR")
    data = jar.read_bytes()
    if signature(jar.stat()) != signature(initial):
        raise AuditError("JAR changed while reading")
    digest = hashlib.sha1(data).hexdigest()
    if digest != expected_sha1:
        raise AuditError(f"exact physical SHA-1 mismatch (observed {digest})")
    expected = inventory_pairs(inventory)
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)):
            raise AuditError("duplicate ZIP member")
        if REGISTRY_CLASS.replace(".", "/") + ".class" not in names:
            raise AuditError("spell registry class absent")
        try:
            metadata = archive.read("META-INF/neoforge.mods.toml")
        except KeyError as exc:
            raise AuditError("NeoForge mod metadata absent") from exc
        if len(metadata) > 256_000 or not re.search(rb"\bmodId\s*=\s*['\"]hazennstuff['\"]", metadata):
            raise AuditError("mod ID does not match installed Hazen")
        class_paths = {}
        for spell_id, klass in expected:
            suffix = "/Spells/Schools/"
            matches = [n for n in names if suffix in n and n.endswith("/" + klass + ".class")]
            if len(matches) != 1:
                raise AuditError(f"not exactly one compiled concrete class for {klass}")
            class_paths[klass] = matches[0][:-6].replace("/", ".")

    to_read = {"registry": REGISTRY_CLASS, **class_paths}
    outputs = {}
    for key, classname in to_read.items():
        try:
            proc = subprocess.run(
                [javap, "-c", "-p", "-classpath", str(jar.resolve()), classname],
                capture_output=True, text=True, timeout=30, check=False,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise AuditError(f"javap missing/timeout for {key}") from exc
        if proc.returncode or len(proc.stdout) > MAX_DISASSEMBLY:
            raise AuditError(f"javap failed/oversized for {key}")
        outputs[key] = proc.stdout
    if signature(jar.stat()) != signature(initial) or hashlib.sha1(jar.read_bytes()).hexdigest() != digest:
        raise AuditError("JAR changed during classfile inspection")
    result = reconcile(expected, outputs["registry"], outputs)
    return {
        "evidence_class": EVIDENCE_CLASS,
        "provider": MOD_ID,
        "version": "1.4.0.14",
        "jar": jar.name,
        "bytes": len(data),
        "sha1": digest,
        "sha256": hashlib.sha256(data).hexdigest(),
        "result": result["status"],
        "registry": result,
        "not_proven": [
            "running Iron's / NeoForge spell registry",
            "actual classloader/mixin behavior",
            "modpack configurations",
            "Survival crafting and spell reachability",
            "PvP/claims and damage",
            "RPG Skill Tree adapter",
            "full upstream source/binary equivalence",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--jar", required=True, type=Path)
    parser.add_argument("--inventory", type=Path, default=INVENTORY)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        if not args.inventory.is_file() or args.inventory.stat().st_size > 256_000:
            raise AuditError("inventory missing/oversized")
        result = audit(args.jar, args.inventory.read_text(encoding="utf-8"))
        code = 0 if result["result"] == "PASS" else 1
    except (AuditError, OSError, UnicodeError, zipfile.BadZipFile) as exc:
        result = {"evidence_class": "UNVERIFIED", "result": "FAIL_CLOSED", "reason": str(exc)}
        code = 1
    rendered = json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
