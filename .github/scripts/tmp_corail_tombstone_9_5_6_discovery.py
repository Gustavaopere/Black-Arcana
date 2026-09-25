#!/usr/bin/env python3
import hashlib
import json
import re
import sys
import tempfile
import urllib.request
import zipfile
from collections import Counter
from pathlib import Path

URL = "https://www.cursemaven.com/curse/maven/corail-tombstone-243707/8842741/corail-tombstone-243707-8842741.jar"
KEYWORDS = (
    "prayer", "pray", "rite", "ritual", "scroll", "tablet",
    "knowledge", "flute", "ankh", "soul", "magic", "enchant"
)
SAFE_STRING = re.compile(r"^[A-Za-z0-9_.$:/<>;()\[\]-]{3,180}$")

def digest(data: bytes, name: str) -> str:
    h = hashlib.new(name)
    h.update(data)
    return h.hexdigest()

def ascii_strings(data: bytes):
    for raw in re.findall(rb"[ -~]{4,200}", data):
        try:
            s = raw.decode("ascii")
        except UnicodeDecodeError:
            continue
        yield s

def main() -> int:
    with tempfile.TemporaryDirectory(prefix="black-arcana-tombstone-") as tmp:
        jar_path = Path(tmp) / "tombstone-neoforge-1.21.1-9.5.6.jar"
        req = urllib.request.Request(URL, headers={"User-Agent": "Black-Arcana-catalog-audit/1"})
        with urllib.request.urlopen(req, timeout=120) as response:
            blob = response.read()
        jar_path.write_bytes(blob)

        print(f"TOMBSTONE_SIZE={len(blob)}")
        print(f"TOMBSTONE_SHA1={digest(blob, 'sha1')}")
        print(f"TOMBSTONE_SHA256={digest(blob, 'sha256')}")

        with zipfile.ZipFile(jar_path) as zf:
            names = zf.namelist()
            classes = [n for n in names if n.endswith(".class") and not n.startswith("META-INF/versions/")]
            resources = [n for n in names if not n.endswith(".class")]
            provider_resources = [n for n in resources if n.startswith("data/tombstone/") or n.startswith("assets/tombstone/")]
            jarjar = [n for n in names if n.startswith("META-INF/jarjar/") and n.endswith(".jar")]

            print(f"TOMBSTONE_CLASS_COUNT={len(classes)}")
            print(f"TOMBSTONE_PROVIDER_RESOURCE_COUNT={len(provider_resources)}")
            print(f"TOMBSTONE_JARJAR_COUNT={len(jarjar)}")

            package_counts = Counter()
            for n in classes:
                parts=n.split("/")
                if len(parts)>=3:
                    package_counts["/".join(parts[:3])] += 1
            for pkg,count in package_counts.most_common(20):
                print(f"TOMBSTONE_PACKAGE={pkg}|{count}")

            class_hits = sorted(n for n in classes if any(k in n.lower() for k in KEYWORDS))
            resource_hits = sorted(n for n in provider_resources if any(k in n.lower() for k in KEYWORDS))

            print(f"TOMBSTONE_SEMANTIC_CLASS_PATH_COUNT={len(class_hits)}")
            for n in class_hits[:500]:
                print(f"TOMBSTONE_SEMANTIC_CLASS_PATH={n}")

            print(f"TOMBSTONE_SEMANTIC_RESOURCE_PATH_COUNT={len(resource_hits)}")
            for n in resource_hits[:500]:
                print(f"TOMBSTONE_SEMANTIC_RESOURCE_PATH={n}")

            lang_keys=[]
            lang_name="assets/tombstone/lang/en_us.json"
            if lang_name in names:
                try:
                    obj=json.loads(zf.read(lang_name).decode("utf-8"))
                    for key in obj.keys():
                        low=key.lower()
                        if any(k in low for k in KEYWORDS):
                            lang_keys.append(key)
                except Exception as exc:
                    print(f"TOMBSTONE_LANG_PARSE_ERROR={type(exc).__name__}:{exc}")
            print(f"TOMBSTONE_SEMANTIC_LANG_KEY_COUNT={len(lang_keys)}")
            for key in sorted(lang_keys)[:1000]:
                print(f"TOMBSTONE_SEMANTIC_LANG_KEY={key}")

            string_hits=set()
            registryish=set()
            for name in classes:
                data=zf.read(name)
                if b"register" in data.lower() or b"registry" in data.lower():
                    if any(k.encode() in data.lower() for k in KEYWORDS):
                        registryish.add(name)
                for s in ascii_strings(data):
                    low=s.lower()
                    if any(k in low for k in KEYWORDS) and SAFE_STRING.match(s):
                        string_hits.add(s)

            print(f"TOMBSTONE_SEMANTIC_CLASS_STRING_COUNT={len(string_hits)}")
            for s in sorted(string_hits)[:1200]:
                print(f"TOMBSTONE_SEMANTIC_CLASS_STRING={s}")

            print(f"TOMBSTONE_SEMANTIC_REGISTRYISH_CLASS_COUNT={len(registryish)}")
            for n in sorted(registryish)[:500]:
                print(f"TOMBSTONE_SEMANTIC_REGISTRYISH_CLASS={n}")

            buckets=Counter()
            for n in provider_resources:
                parts=n.split("/")
                if n.startswith("data/tombstone/") and len(parts)>=3:
                    buckets["data:"+parts[2]] += 1
                elif n.startswith("assets/tombstone/") and len(parts)>=3:
                    buckets["assets:"+parts[2]] += 1
            for bucket,count in sorted(buckets.items()):
                print(f"TOMBSTONE_RESOURCE_BUCKET={bucket}|{count}")

            toml="META-INF/neoforge.mods.toml"
            if toml in names:
                txt=zf.read(toml).decode("utf-8", errors="replace")
                dep_ids=sorted(set(re.findall(r'modId\s*=\s*"([^"]+)"',txt)))
                print("TOMBSTONE_DEPENDENCY_MOD_IDS="+",".join(dep_ids))

            print("TOMBSTONE_DISCOVERY_AUDIT_COMPLETE=true")
    return 0

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"TOMBSTONE_AUDIT_ERROR={type(exc).__name__}: {exc}", file=sys.stderr)
        raise
