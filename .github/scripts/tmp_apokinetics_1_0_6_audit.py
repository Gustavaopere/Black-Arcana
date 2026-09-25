#!/usr/bin/env python3
import hashlib
import re
import sys
import tempfile
import urllib.request
import zipfile
from collections import Counter
from pathlib import Path

URL = "https://www.cursemaven.com/curse/maven/apokinetics-1606442/8790422/apokinetics-1606442-8790422.jar"
EXPECTED_SHA1 = "8af4fc7fb17f4d60ead9d0c098d0650d6fdefa68"
MOD_ID = "apokinetics"

SEMANTIC_PATH_RE = re.compile(r"(?:^|[/_.-])(spell|glyph|ritual|rite)(?:[/_.-]|$)", re.I)
SEMANTIC_UTF8_TOKENS = [
    b"abstractspell",
    b"spellregistry",
    b"registerspell",
    b"spelldata",
    b"schoolregistry",
    b"spellpart",
    b"glyphregistry",
    b"ritualrecipe",
    b"riteholder",
    b"spiritrite",
]
MAGIC_API_TOKENS = [
    b"io/redspace/ironsspellbooks",
    b"irons_spellbooks",
    b"com/hollingsworth/arsnouveau",
    b"ars_nouveau",
    b"team/lodestar/lodestone/systems/spell",
    b"malum",
    b"eidolon",
    b"goety",
]

def digest(data: bytes, name: str) -> str:
    h = hashlib.new(name)
    h.update(data)
    return h.hexdigest()

def download(target: Path) -> bytes:
    req = urllib.request.Request(URL, headers={"User-Agent": "Black-Arcana-catalog-audit/1"})
    with urllib.request.urlopen(req, timeout=90) as response:
        data = response.read()
    target.write_bytes(data)
    print(f"APOKINETICS_SIZE={len(data)}")
    print(f"APOKINETICS_SHA1={digest(data, 'sha1')}")
    print(f"APOKINETICS_SHA256={digest(data, 'sha256')}")
    return data

def main() -> int:
    with tempfile.TemporaryDirectory(prefix="black-arcana-apokinetics-") as tmp:
        jar_path = Path(tmp) / "apokinetics-1.0.6.jar"
        blob = download(jar_path)
        actual_sha1 = digest(blob, "sha1")
        if actual_sha1 != EXPECTED_SHA1:
            raise RuntimeError(f"physical hash mismatch: expected {EXPECTED_SHA1}, got {actual_sha1}")
        print("APOKINETICS_PHYSICAL_HASH_MATCH=true")

        with zipfile.ZipFile(jar_path) as zf:
            names = zf.namelist()
            classes = [n for n in names if n.endswith(".class") and not n.startswith("META-INF/versions/")]
            provider_classes = [n for n in classes if MOD_ID in n.lower()]
            if not provider_classes:
                raise RuntimeError("no provider class path containing mod id 'apokinetics' was found")

            provider_resources = [
                n for n in names
                if n.startswith(f"data/{MOD_ID}/") or n.startswith(f"assets/{MOD_ID}/")
            ]
            jarjar = [n for n in names if n.startswith("META-INF/jarjar/") and n.endswith(".jar")]

            semantic_class_paths = sorted(n for n in provider_classes if SEMANTIC_PATH_RE.search(n))
            semantic_resource_paths = sorted(n for n in provider_resources if SEMANTIC_PATH_RE.search(n))

            utf8_hits = []
            magic_api_hits = []
            for name in provider_classes:
                low = zf.read(name).lower()
                tokens = sorted({t.decode("ascii") for t in SEMANTIC_UTF8_TOKENS if t in low})
                api_tokens = sorted({t.decode("ascii") for t in MAGIC_API_TOKENS if t in low})
                if tokens:
                    utf8_hits.append((name, tokens))
                if api_tokens:
                    magic_api_hits.append((name, api_tokens))

            registryish = sorted(
                n for n in provider_classes
                if re.search(r"(registr|deferred|gem|socket|pylon|table|wrench|scanner|locator)", n, re.I)
            )
            data_buckets = Counter()
            for n in provider_resources:
                parts = n.split("/")
                if n.startswith(f"data/{MOD_ID}/") and len(parts) >= 3:
                    data_buckets[parts[2]] += 1
                elif n.startswith(f"assets/{MOD_ID}/") and len(parts) >= 3:
                    data_buckets["assets:" + parts[2]] += 1

            metadata_name = "META-INF/neoforge.mods.toml"
            metadata = zf.read(metadata_name).decode("utf-8", errors="replace") if metadata_name in names else ""
            dep_ids = sorted(set(re.findall(r'modId\s*=\s*"([^"]+)"', metadata)))

            print(f"APOKINETICS_CLASS_COUNT={len(classes)}")
            print(f"APOKINETICS_PROVIDER_CLASS_COUNT={len(provider_classes)}")
            print(f"APOKINETICS_PROVIDER_RESOURCE_COUNT={len(provider_resources)}")
            print(f"APOKINETICS_JARJAR_COUNT={len(jarjar)}")
            print("APOKINETICS_DEPENDENCY_MOD_IDS=" + ",".join(dep_ids))

            print(f"APOKINETICS_SEMANTIC_CLASS_PATH_HIT_COUNT={len(semantic_class_paths)}")
            for item in semantic_class_paths:
                print(f"APOKINETICS_SEMANTIC_CLASS_PATH_HIT={item}")

            print(f"APOKINETICS_SEMANTIC_RESOURCE_PATH_HIT_COUNT={len(semantic_resource_paths)}")
            for item in semantic_resource_paths:
                print(f"APOKINETICS_SEMANTIC_RESOURCE_PATH_HIT={item}")

            print(f"APOKINETICS_SEMANTIC_CLASS_UTF8_HIT_COUNT={len(utf8_hits)}")
            for name, tokens in utf8_hits:
                print(f"APOKINETICS_SEMANTIC_CLASS_UTF8_HIT={name}|{','.join(tokens)}")

            print(f"APOKINETICS_MAGIC_API_REFERENCE_HIT_COUNT={len(magic_api_hits)}")
            for name, tokens in magic_api_hits:
                print(f"APOKINETICS_MAGIC_API_REFERENCE_HIT={name}|{','.join(tokens)}")

            print(f"APOKINETICS_REGISTRYISH_CLASS_COUNT={len(registryish)}")
            for item in registryish[:120]:
                print(f"APOKINETICS_REGISTRYISH_CLASS={item}")

            for bucket, count in sorted(data_buckets.items()):
                print(f"APOKINETICS_RESOURCE_BUCKET={bucket}|{count}")

            if semantic_class_paths:
                raise RuntimeError("spell/glyph/ritual/rite semantic class paths found; manual review required")
            if semantic_resource_paths:
                raise RuntimeError("spell/glyph/ritual/rite semantic resource paths found; manual review required")
            if utf8_hits:
                raise RuntimeError("spell/glyph/ritual/rite classfile semantic tokens found; manual review required")
            if magic_api_hits:
                raise RuntimeError("known external magic API references found; manual review required")

            print("APOKINETICS_ZERO_SPELL_GLYPH_RITUAL_SURFACE_AUDIT=true")
    return 0

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"APOKINETICS_AUDIT_ERROR={type(exc).__name__}: {exc}", file=sys.stderr)
        raise
