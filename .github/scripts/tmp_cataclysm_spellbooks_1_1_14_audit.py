#!/usr/bin/env python3
import hashlib
import json
import re
import sys
import tempfile
import urllib.request
import zipfile
from pathlib import Path

BASE = "https://www.cursemaven.com/curse/maven/cataclysm-spellbooks-1099461"
FILES = {
    "1.1.13": ("8792628", "4af8348cc77bbff2ab7057c1fac26a5ab0a5b6a2"),
    "1.1.14": ("8847070", None),
}
ROOT_KEY = re.compile(r"^spell\.cataclysm_spellbooks\.[^.]+$")


def digest(data: bytes, name: str) -> str:
    h = hashlib.new(name)
    h.update(data)
    return h.hexdigest()


def download(version: str, file_id: str, target: Path) -> bytes:
    url = f"{BASE}/{file_id}/cataclysm-spellbooks-1099461-{file_id}.jar"
    request = urllib.request.Request(url, headers={"User-Agent": "Black-Arcana-catalog-audit/1"})
    with urllib.request.urlopen(request, timeout=60) as response:
        data = response.read()
    target.write_bytes(data)
    print(f"CATACLYSM_{version.replace('.', '_')}_SIZE={len(data)}")
    print(f"CATACLYSM_{version.replace('.', '_')}_SHA1={digest(data, 'sha1')}")
    print(f"CATACLYSM_{version.replace('.', '_')}_SHA256={digest(data, 'sha256')}")
    return data


def inspect(path: Path):
    with zipfile.ZipFile(path) as zf:
        names = zf.namelist()
        registry = [n for n in names if n.endswith("/SpellRegistries.class") or n == "SpellRegistries.class"]
        if len(registry) != 1:
            raise RuntimeError(f"expected exactly one SpellRegistries.class in {path.name}, found {registry}")
        registry_name = registry[0]
        registry_bytes = zf.read(registry_name)

        spellish_classes = {
            n for n in names
            if n.endswith(".class")
            and ("spell" in n.lower())
            and n.startswith("net/acetheeldritchking/cataclysm_spellbooks/")
        }

        lang_path = "assets/cataclysm_spellbooks/lang/en_us.json"
        lang = json.loads(zf.read(lang_path))
        root_keys = {k for k in lang if ROOT_KEY.match(k)}

        return {
            "registry_name": registry_name,
            "registry_bytes": registry_bytes,
            "registry_sha256": digest(registry_bytes, "sha256"),
            "spellish_classes": spellish_classes,
            "root_keys": root_keys,
        }


def emit_delta(label: str, old: set[str], new: set[str]) -> None:
    added = sorted(new - old)
    removed = sorted(old - new)
    print(f"{label}_1_1_13_COUNT={len(old)}")
    print(f"{label}_1_1_14_COUNT={len(new)}")
    print(f"{label}_ADDED_COUNT={len(added)}")
    for item in added:
        print(f"{label}_ADDED={item}")
    print(f"{label}_REMOVED_COUNT={len(removed)}")
    for item in removed:
        print(f"{label}_REMOVED={item}")


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="black-arcana-cataclysm-") as tmp:
        root = Path(tmp)
        paths = {}
        blobs = {}
        for version, (file_id, expected_sha1) in FILES.items():
            path = root / f"{version}.jar"
            blobs[version] = download(version, file_id, path)
            paths[version] = path
            if expected_sha1 is not None:
                actual = digest(blobs[version], "sha1")
                if actual != expected_sha1:
                    raise RuntimeError(
                        f"1.1.13 control hash mismatch: expected {expected_sha1}, got {actual}"
                    )

        old = inspect(paths["1.1.13"])
        new = inspect(paths["1.1.14"])

        print(f"CATACLYSM_1_1_13_REGISTRY_CLASS={old['registry_name']}")
        print(f"CATACLYSM_1_1_14_REGISTRY_CLASS={new['registry_name']}")
        print(f"CATACLYSM_1_1_13_REGISTRY_SHA256={old['registry_sha256']}")
        print(f"CATACLYSM_1_1_14_REGISTRY_SHA256={new['registry_sha256']}")
        print(
            "CATACLYSM_REGISTRY_CLASS_IDENTICAL="
            + str(old["registry_bytes"] == new["registry_bytes"]).lower()
        )

        emit_delta(
            "CATACLYSM_SPELLISH_CLASS_PATHS",
            old["spellish_classes"],
            new["spellish_classes"],
        )
        emit_delta(
            "CATACLYSM_ROOT_LANG_KEYS",
            old["root_keys"],
            new["root_keys"],
        )

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"CATACLYSM_AUDIT_ERROR={type(exc).__name__}: {exc}", file=sys.stderr)
        raise
