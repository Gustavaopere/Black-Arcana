#!/usr/bin/env python3
import hashlib
import re
import subprocess
import sys
import tempfile
import urllib.request
import zipfile
from pathlib import Path

URL = "https://www.cursemaven.com/curse/maven/tombstone-243707/8842741/tombstone-243707-8842741.jar"
EXPECTED_SHA1 = "d830d16caa20b0d23a44ed6b1d339bc22afc2460"

CLASSES = [
    "ovh.corail.tombstone.item.ItemTabletOfAssistance",
    "ovh.corail.tombstone.item.ItemTabletOfCupidity",
    "ovh.corail.tombstone.item.ItemTabletOfGuard",
    "ovh.corail.tombstone.item.ItemTabletOfHome",
    "ovh.corail.tombstone.item.ItemTabletOfRecall",
    "ovh.corail.tombstone.item.ItemGemstoneOfFamiliar",
    "ovh.corail.tombstone.item.ItemGemstoneOfGuardian",
    "ovh.corail.tombstone.item.ItemGemstoneOfMerchant",
    "ovh.corail.tombstone.item.ItemGraveKey",
    "ovh.corail.tombstone.item.ItemLostTablet",
    "ovh.corail.tombstone.item.ItemMagicScroll",
    "ovh.corail.tombstone.item.ItemScrollOfKnowledge",
]

METHODS = {"doEffects", "use", "setEnchant", "getCastingType", "canBlockInteractFirst"}

def sha1(data: bytes) -> str:
    return hashlib.sha1(data).hexdigest()

def get(url: str, target: Path) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "Black-Arcana-clean-room-audit/1"})
    with urllib.request.urlopen(req, timeout=120) as r:
        data = r.read()
    target.write_bytes(data)
    print(f"TOMBSTONE_CASTABLE_BYTES={len(data)}")
    print(f"TOMBSTONE_CASTABLE_SHA1={sha1(data)}")
    return data

def javap(jar: Path, cls: str, code: bool) -> str:
    args = ["javap", "-classpath", str(jar), "-p"]
    if code:
        args.append("-c")
    args.append(cls)
    return subprocess.check_output(args, text=True, stderr=subprocess.STDOUT)

def method_sections(text: str):
    lines = text.splitlines()
    out = []
    current_sig = None
    current = []
    for line in lines:
        stripped = line.strip()
        sig_match = re.match(r"(?:public|protected|private).+\s([\w$<>]+)\([^)]*\).*;", stripped)
        if sig_match:
            if current_sig:
                out.append((current_sig, current))
            current_sig = sig_match.group(1)
            current = [line]
        elif current_sig:
            if stripped == "" and current:
                out.append((current_sig, current))
                current_sig = None
                current = []
            else:
                current.append(line)
    if current_sig:
        out.append((current_sig, current))
    return out

def normalize_comment(comment: str) -> str:
    comment = re.sub(r"\s+", " ", comment.strip())
    return comment[:500]

def main() -> int:
    with tempfile.TemporaryDirectory(prefix="tombstone-castable-") as tmp:
        jar = Path(tmp) / "tombstone-9.5.6.jar"
        data = get(URL, jar)
        if sha1(data) != EXPECTED_SHA1:
            raise RuntimeError(f"hash mismatch: expected {EXPECTED_SHA1}, got {sha1(data)}")
        print("TOMBSTONE_CASTABLE_HASH_MATCH=true")

        with zipfile.ZipFile(jar) as zf:
            names = set(zf.namelist())
            for cls in CLASSES:
                path = cls.replace(".", "/") + ".class"
                if path not in names:
                    raise RuntimeError(f"missing target class {cls}")
                nested = sorted(
                    n[:-6].replace("/", ".")
                    for n in names
                    if n.startswith(path[:-6] + "$") and n.endswith(".class")
                )
                print(f"TOMBSTONE_CASTABLE_CLASS={cls}")
                print(f"TOMBSTONE_CASTABLE_NESTED_COUNT={cls}|{len(nested)}")
                for n in nested:
                    print(f"TOMBSTONE_CASTABLE_NESTED={cls}|{n}")

                decl = javap(jar, cls, False)
                superclass = ""
                m = re.search(r"class\s+" + re.escape(cls) + r"\s+extends\s+([^\s{]+)", decl)
                if m:
                    superclass = m.group(1)
                print(f"TOMBSTONE_CASTABLE_SUPER={cls}|{superclass}")

                code = javap(jar, cls, True)
                found = set()
                for method, section in method_sections(code):
                    if method not in METHODS:
                        continue
                    found.add(method)
                    calls = set()
                    strings = set()
                    fields = set()
                    classes = set()
                    for line in section:
                        if "//" not in line:
                            continue
                        comment = line.split("//", 1)[1].strip()
                        if comment.startswith(("Method ", "InterfaceMethod ")):
                            calls.add(normalize_comment(comment))
                        elif comment.startswith("Field "):
                            fields.add(normalize_comment(comment))
                        elif comment.startswith("String "):
                            val = normalize_comment(comment[len("String "):])
                            if any(k in val.lower() for k in [
                                "tablet", "gemstone", "grave", "scroll", "knowledge", "familiar",
                                "guardian", "merchant", "home", "recall", "assist", "cupidity",
                                "teleport", "soul", "village", "treasure", "exploration", "effect",
                                "lost", "magic", "player", "ally", "owner", "target"
                            ]):
                                strings.add(val)
                        elif comment.startswith("class "):
                            classes.add(normalize_comment(comment))
                    print(f"TOMBSTONE_CASTABLE_METHOD={cls}|{method}")
                    for x in sorted(calls):
                        print(f"TOMBSTONE_CASTABLE_CALL={cls}|{method}|{x}")
                    for x in sorted(fields):
                        print(f"TOMBSTONE_CASTABLE_FIELD={cls}|{method}|{x}")
                    for x in sorted(strings):
                        print(f"TOMBSTONE_CASTABLE_STRING={cls}|{method}|{x}")
                    for x in sorted(classes):
                        print(f"TOMBSTONE_CASTABLE_CLASSREF={cls}|{method}|{x}")
                print(f"TOMBSTONE_CASTABLE_RELEVANT_METHODS={cls}|{','.join(sorted(found))}")

            # Focus nested enum declarations for Lost Tablet and any nested item classes.
            for cls in sorted({
                "ovh.corail.tombstone.item.ItemLostTablet$Type",
            }):
                try:
                    decl = javap(jar, cls, False)
                except subprocess.CalledProcessError:
                    continue
                enum_consts = []
                for line in decl.splitlines():
                    m = re.match(r"\s*public static final " + re.escape(cls) + r"\s+([A-Z0-9_]+);", line)
                    if m:
                        enum_consts.append(m.group(1))
                print(f"TOMBSTONE_CASTABLE_ENUM={cls}|{','.join(enum_consts)}")

        print("TOMBSTONE_CASTABLE_AUDIT_COMPLETE=true")
    return 0

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"TOMBSTONE_CASTABLE_AUDIT_ERROR={type(exc).__name__}: {exc}", file=sys.stderr)
        raise
