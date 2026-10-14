#!/usr/bin/env python3
"""Read-only classfile evidence for exact-hash Apprentice's Codex 0.9.7.1.

This checks bytecode shapes, never executes a Minecraft/mod class and never
claims client, dedicated-server, Survival, config, claims or counterspell QA.
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

EXPECTED_SHA1 = "b514315add32b93b0049c8673075627d7ef812e0"
EXPECTED_JAR = "apprentice_codex-0.9.7.1+mc1.21.1.jar"
BASE = "jp.aquafactory.apprenticecodex.spell"
CLASSES = {
    "beam": f"{BASE}.arcanebeam.ArcaneBeamEntity",
    "moon": f"{BASE}.uniteluna.UniteLunaMoonEntity",
    "palette": f"{BASE}.paletteshift.PaletteShiftReceptionEvent",
    "mending": f"{BASE}.manamending.ManaMending$ManaMendingCastData",
}
MAX_JAR_SIZE = 32 * 1024 * 1024
MAX_JAVAP_OUTPUT = 4 * 1024 * 1024
SIGNATURE = re.compile(
    r"^  (?:public|protected|private|static|final|synchronized)[^\n]*\([^\n]*\)(?: throws [^\n]*)?;\s*$",
    re.M,
)


class EvidenceError(Exception):
    """Fail-closed evidence gate; not a provider-runtime finding."""


def get_method(disassembly: str, method: str) -> str:
    matches = list(SIGNATURE.finditer(disassembly))
    for i, match in enumerate(matches):
        signature = match.group(0)
        if re.search(r"\b" + re.escape(method) + r"\(", signature):
            end = matches[i + 1].start() if i + 1 < len(matches) else len(disassembly)
            body = disassembly[match.end():end]
            if "Code:" not in body:
                raise EvidenceError(f"no Code section for {method}")
            return body
    raise EvidenceError(f"method not located: {method}")


def inspect_bytecode(outputs: dict[str, str]) -> dict[str, dict[str, object]]:
    """Narrow, independent checks: missing/unknown is never promoted to PASS."""
    results = {}
    try:
        beam = get_method(outputs["beam"], "tick")
        results["beam_remainder_nonzero_damage_path"] = bool(re.search(
            r"\birem\b(?:(?!\birem\b)[\s\S]){0,450}?\bifeq\b"
            r"(?:(?!\birem\b)[\s\S]){0,450}?// Method (?:[^\n]*\.)?damageHitTarget:",
            beam,
        ))
    except (KeyError, EvidenceError):
        results["beam_remainder_nonzero_damage_path"] = False

    try:
        anti = get_method(outputs["moon"], "onAntiMagic")
        explode = get_method(outputs["moon"], "explodeByAntiMagic")
        results["moon_antimagic_triggers_boosted_burst"] = (
            "explodeByAntiMagic:" in anti
            and bool(re.search(r"// (?:float|Float) 3\.0f?\b", explode))
            and "applyBurstDamage:" in explode
        )
    except (KeyError, EvidenceError):
        results["moon_antimagic_triggers_boosted_burst"] = False

    try:
        precast = get_method(outputs["palette"], "onSpellPreCast")
        results["palette_precast_cancels_event"] = (
            "applyPastelAffinity:" in precast and "setCanceled:" in precast
        )
    except (KeyError, EvidenceError):
        results["palette_precast_cancels_event"] = False

    try:
        matcher = get_method(outputs["mending"], "matchesTarget")
        results["mending_itemstack_reference_identity"] = (
            "targetStack:" in matcher
            and bool(re.search(r"\bif_acmp(?:ne|eq)\b", matcher))
        )
    except (KeyError, EvidenceError):
        results["mending_itemstack_reference_identity"] = False

    return {
        name: {"status": "PASS" if passed else "UNPROVEN_OR_MISMATCH"}
        for name, passed in results.items()
    }


def audit_jar(jar: Path, *, expected_sha1: str = EXPECTED_SHA1,
              javap: str = "javap") -> dict[str, object]:
    if jar.name != EXPECTED_JAR:
        raise EvidenceError("unrecognized JAR filename")
    if jar.is_symlink() or not jar.is_file():
        raise EvidenceError("JAR must be a regular non-symlink file")
    before = jar.stat()
    if not stat.S_ISREG(before.st_mode) or not 0 < before.st_size <= MAX_JAR_SIZE:
        raise EvidenceError("JAR size/type outside bounded audit contract")
    data = jar.read_bytes()
    after = jar.stat()
    if (before.st_ino, before.st_size, before.st_mtime_ns) != (
        after.st_ino, after.st_size, after.st_mtime_ns
    ):
        raise EvidenceError("JAR changed during audit")
    sha1 = hashlib.sha1(data).hexdigest()
    if sha1 != expected_sha1:
        raise EvidenceError(f"JAR SHA-1 mismatch (observed {sha1})")
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)):
            raise EvidenceError("duplicate ZIP entries")
        for classname in CLASSES.values():
            member = classname.replace(".", "/") + ".class"
            if member not in names:
                raise EvidenceError("class not found: " + classname)
        try:
            meta = archive.read("META-INF/neoforge.mods.toml")
        except KeyError as err:
            raise EvidenceError("NeoForge mod metadata missing") from err
        if len(meta) > 256 * 1024 or not re.search(
            rb'\bmodId\s*=\s*["\x27]apprenticecodex["\x27]', meta
        ):
            raise EvidenceError("NeoForge metadata does not certify apprenticecodex mod id")

    disassembly = {}
    for key, classname in CLASSES.items():
        try:
            proc = subprocess.run(
                [javap, "-c", "-p", "-classpath", str(jar.resolve()), classname],
                text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                timeout=30, check=False,
            )
        except (OSError, subprocess.TimeoutExpired) as err:
            raise EvidenceError(f"javap unavailable/timeout for {key}") from err
        if proc.returncode != 0 or len(proc.stdout) > MAX_JAVAP_OUTPUT:
            raise EvidenceError(f"javap failed/oversized output for {key}")
        disassembly[key] = proc.stdout
    final = jar.stat()
    if ((before.st_ino, before.st_size, before.st_mtime_ns)
            != (final.st_ino, final.st_size, final.st_mtime_ns)
            or hashlib.sha1(jar.read_bytes()).hexdigest() != sha1):
        raise EvidenceError("JAR changed during javap disassembly")
    checks = inspect_bytecode(disassembly)
    return {
        "evidence_class": "EXACT_HASH_CLASSFILE_OPCODE_SHAPE_NOT_RUNTIME_QA",
        "provider": "apprenticecodex",
        "version": "0.9.7.1",
        "minecraft": "1.21.1",
        "source_type": "CurseForge official file ID 8768955, NeoForge",
        "filename": jar.name,
        "size_bytes": len(data),
        "sha1": sha1,
        "sha256": hashlib.sha256(data).hexdigest(),
        "checks": checks,
        "result": "PASS" if all(x["status"] == "PASS" for x in checks.values())
                  else "UNPROVEN_OR_MISMATCH",
        "not_proven": [
            "live gameplay", "config effective", "save/restart", "claims/PvP",
            "survival reachability", "adapter interoperability",
            "source/binary full equality",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--jar", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        result = audit_jar(args.jar)
        code = 0 if result["result"] == "PASS" else 1
    except (EvidenceError, OSError, zipfile.BadZipFile) as exc:
        result = {
            "evidence_class": "UNVERIFIED",
            "result": "FAIL_CLOSED",
            "reason": str(exc),
        }
        code = 1
    rendered = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
