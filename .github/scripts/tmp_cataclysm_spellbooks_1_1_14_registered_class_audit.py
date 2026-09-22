#!/usr/bin/env python3
import hashlib
import re
import sys
import tempfile
import urllib.request
import zipfile
from pathlib import Path

BASE = "https://www.cursemaven.com/curse/maven/cataclysm-spellbooks-1099461"
FILES = {
    "1.1.13": ("8792628", "4af8348cc77bbff2ab7057c1fac26a5ab0a5b6a2"),
    "1.1.14": ("8847070", "568d798862a61a374ab1e55dcddf5b2e3326b8b5"),
}
INVENTORY = Path("wiki/modpack-catalog/providers/✅-cataclysm-spellbooks/EXACT-1.1.13-SPELL-INVENTORY.md")
ROW = re.compile(r"^\| [^|]+ \| `[^\`]+` \| `([^\`]+)` \| `cataclysm_spellbooks:[^\`]+` \|$")


def sha1(data: bytes) -> str:
    return hashlib.sha1(data).hexdigest()


def download(version: str, file_id: str, target: Path) -> None:
    url = f"{BASE}/{file_id}/cataclysm-spellbooks-1099461-{file_id}.jar"
    req = urllib.request.Request(url, headers={"User-Agent": "Black-Arcana-catalog-audit/1"})
    with urllib.request.urlopen(req, timeout=60) as response:
        data = response.read()
    target.write_bytes(data)
    actual = sha1(data)
    expected = FILES[version][1]
    print(f"CATACLYSM_CLASS_AUDIT_{version.replace('.', '_')}_SHA1={actual}")
    if actual != expected:
        raise RuntimeError(f"{version} SHA-1 mismatch: expected {expected}, got {actual}")


def class_names() -> list[str]:
    names = []
    for line in INVENTORY.read_text(encoding="utf-8").splitlines():
        match = ROW.match(line)
        if match:
            names.append(match.group(1))
    if len(names) != 59:
        raise RuntimeError(f"expected 59 inventory classes, found {len(names)}")
    if len(set(names)) != 59:
        raise RuntimeError("inventory class names are not unique")
    return names


def locate(zf: zipfile.ZipFile, class_name: str) -> str:
    suffix = "/" + class_name + ".class"
    matches = [name for name in zf.namelist() if name.endswith(suffix)]
    if len(matches) != 1:
        raise RuntimeError(f"{class_name}: expected one class path, found {matches}")
    return matches[0]


def main() -> int:
    classes = class_names()
    with tempfile.TemporaryDirectory(prefix="black-arcana-cataclysm-class-audit-") as tmp:
        root = Path(tmp)
        paths = {}
        for version, (file_id, _) in FILES.items():
            target = root / f"{version}.jar"
            download(version, file_id, target)
            paths[version] = target

        identical = []
        changed = []
        path_changes = []
        with zipfile.ZipFile(paths["1.1.13"]) as old, zipfile.ZipFile(paths["1.1.14"]) as new:
            for class_name in classes:
                old_path = locate(old, class_name)
                new_path = locate(new, class_name)
                if old_path != new_path:
                    path_changes.append((class_name, old_path, new_path))
                if old.read(old_path) == new.read(new_path):
                    identical.append(class_name)
                else:
                    changed.append(class_name)

        print(f"CATACLYSM_REGISTERED_CLASS_EXPECTED_COUNT={len(classes)}")
        print(f"CATACLYSM_REGISTERED_CLASS_IDENTICAL_COUNT={len(identical)}")
        print(f"CATACLYSM_REGISTERED_CLASS_CHANGED_COUNT={len(changed)}")
        for name in changed:
            print(f"CATACLYSM_REGISTERED_CLASS_CHANGED={name}")
        print(f"CATACLYSM_REGISTERED_CLASS_PATH_CHANGE_COUNT={len(path_changes)}")
        for class_name, old_path, new_path in path_changes:
            print(f"CATACLYSM_REGISTERED_CLASS_PATH_CHANGE={class_name}|{old_path}|{new_path}")

        if len(identical) != 59 or changed or path_changes:
            raise RuntimeError("registered spell class surface changed between 1.1.13 and 1.1.14")

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"CATACLYSM_CLASS_AUDIT_ERROR={type(exc).__name__}: {exc}", file=sys.stderr)
        raise
