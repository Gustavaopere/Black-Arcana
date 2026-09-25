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

URL = "https://www.cursemaven.com/curse/maven/relics-mod-445274/8158315/relics-mod-445274-8158315.jar"
EXPECTED_SHA1 = "1fe7d57ebfa56ebd0aeecfed01075f8b55b94ef7"

def digest(data: bytes, name: str) -> str:
    h = hashlib.new(name)
    h.update(data)
    return h.hexdigest()

def download(target: Path) -> bytes:
    req = urllib.request.Request(URL, headers={"User-Agent": "Black-Arcana-catalog-audit/1"})
    with urllib.request.urlopen(req, timeout=90) as response:
        data = response.read()
    target.write_bytes(data)
    print(f"RELICS_SIZE={len(data)}")
    print(f"RELICS_SHA1={digest(data, 'sha1')}")
    print(f"RELICS_SHA256={digest(data, 'sha256')}")
    return data

def main() -> int:
    with tempfile.TemporaryDirectory(prefix="black-arcana-relics-") as tmp:
        jar = Path(tmp) / "relics-0.12.8.jar"
        blob = download(jar)
        actual = digest(blob, "sha1")
        if actual != EXPECTED_SHA1:
            raise RuntimeError(f"physical hash mismatch: expected {EXPECTED_SHA1}, got {actual}")
        print("RELICS_PHYSICAL_HASH_MATCH=true")

        with zipfile.ZipFile(jar) as zf:
            names = zf.namelist()
            classes = sorted(n for n in names if n.endswith(".class") and not n.startswith("META-INF/versions/"))
            resources = sorted(n for n in names if n.startswith("data/relics/") or n.startswith("assets/relics/"))
            jarjar = sorted(n for n in names if n.startswith("META-INF/jarjar/") and n.endswith(".jar"))

            metadata_name = "META-INF/neoforge.mods.toml"
            metadata = zf.read(metadata_name).decode("utf-8", errors="replace") if metadata_name in names else ""
            dep_ids = sorted(set(re.findall(r'modId\s*=\s*"([^"]+)"', metadata)))

            ability_paths = sorted(n for n in names if re.search(r"(?:^|[/_.-])abilit(?:y|ies)(?:[/_.-]|$)", n, re.I))
            relic_paths = sorted(n for n in resources if re.search(r"(?:^|[/_.-])relic(?:s)?(?:[/_.-]|$)", n, re.I))
            ability_classes = sorted(n for n in classes if re.search(r"abilit(?:y|ies)", n, re.I))

            data_buckets = Counter()
            for n in resources:
                parts = n.split("/")
                if n.startswith("data/relics/") and len(parts) >= 3:
                    data_buckets["data:" + parts[2]] += 1
                elif n.startswith("assets/relics/") and len(parts) >= 3:
                    data_buckets["assets:" + parts[2]] += 1

            ability_roots = []
            synergy_roots = []
            relic_item_classes = sorted(
                n for n in classes
                if re.match(r"^it/hurts/sskirillss/relics/items/relics/(?:[^/]+/)*[^/$]+(?:Item)?\.class$", n)
                and "$" not in n
                and "/base/" not in n
            )

            lang_candidates = []
            for lang_path in ["assets/relics/lang/en_us.json", "assets/relics/lang/en_gb.json"]:
                if lang_path in names:
                    try:
                        lang = json.loads(zf.read(lang_path))
                    except Exception:
                        continue
                    for key in sorted(lang):
                        lk = key.lower()
                        if lang_path.endswith("en_us.json"):
                            ma = re.match(r"^relics\.description\.([a-z0-9_]+)\.ability\.([a-z0-9_]+)$", key)
                            if ma:
                                ability_roots.append((ma.group(1), ma.group(2)))
                            ms = re.match(r"^relics\.description\.([a-z0-9_]+)\.synergy\.([a-z0-9_]+)$", key)
                            if ms:
                                synergy_roots.append((ms.group(1), ms.group(2)))
                        if "ability" in lk or "synergy" in lk or ".relic." in lk or lk.startswith("item.relics."):
                            lang_candidates.append((lang_path, key))

            class_utf8_candidates = []
            needles = [b"ability", b"abilities", b"relic", b"synergy", b"cooldown", b"rank", b"experience"]
            for name in classes:
                low = zf.read(name).lower()
                hits = sorted({x.decode("ascii") for x in needles if x in low})
                if hits and ("ability" in hits or "abilities" in hits):
                    class_utf8_candidates.append((name, hits))

            print(f"RELICS_CLASS_COUNT={len(classes)}")
            print(f"RELICS_PROVIDER_RESOURCE_COUNT={len(resources)}")
            print(f"RELICS_JARJAR_COUNT={len(jarjar)}")
            print("RELICS_DEPENDENCY_MOD_IDS=" + ",".join(dep_ids))

            for bucket,count in sorted(data_buckets.items()):
                print(f"RELICS_RESOURCE_BUCKET={bucket}|{count}")

            print(f"RELICS_ABILITY_PATH_COUNT={len(ability_paths)}")
            for n in ability_paths[:400]:
                print(f"RELICS_ABILITY_PATH={n}")

            print(f"RELICS_ABILITY_CLASS_COUNT={len(ability_classes)}")
            for n in ability_classes[:400]:
                print(f"RELICS_ABILITY_CLASS={n}")

            print(f"RELICS_RELIC_RESOURCE_PATH_COUNT={len(relic_paths)}")
            for n in relic_paths[:400]:
                print(f"RELICS_RELIC_RESOURCE_PATH={n}")

            ability_roots = sorted(set(ability_roots))
            synergy_roots = sorted(set(synergy_roots))

            # Targeted clean-room deduplication probe for the only exact synergy roots.
            en_us = json.loads(zf.read("assets/relics/lang/en_us.json"))
            synergy_probe_relics = ["glitchy_mantle", "kinetic_belt"]
            synergy_probe = {}
            for relic_id in synergy_probe_relics:
                prefix = f"relics.description.{relic_id}.synergy.electricity"
                values = {
                    "title": str(en_us.get(prefix, "")),
                    "disabled": str(en_us.get(prefix + ".disabled.description", "")),
                    "enabled": str(en_us.get(prefix + ".enabled.description", "")),
                }
                synergy_probe[relic_id] = {
                    k: digest(v.encode("utf-8"), "sha256") for k, v in values.items()
                }

            probe_classes = {
                "glitchy_mantle": "it/hurts/sskirillss/relics/items/relics/back/GlitchyMantleItem.class",
                "kinetic_belt": "it/hurts/sskirillss/relics/items/relics/belt/KineticBeltItem.class",
            }
            class_probe = {}
            for relic_id, class_path in probe_classes.items():
                raw = zf.read(class_path)
                printable = {
                    m.decode("ascii", errors="ignore")
                    for m in re.findall(rb"[A-Za-z0-9_./:$-]{4,}", raw)
                }
                class_probe[relic_id] = sorted(
                    s for s in printable
                    if re.search(r"electric|synerg|GlitchyMantle|KineticBelt|glitchy_mantle|kinetic_belt", s, re.I)
                )

            print(f"RELICS_BASE_ABILITY_ROOT_COUNT={len(ability_roots)}")
            for relic_id, ability_id in ability_roots:
                print(f"RELICS_BASE_ABILITY_ROOT={relic_id}|{ability_id}")

            print(f"RELICS_SYNERGY_ROOT_COUNT={len(synergy_roots)}")
            for relic_id, synergy_id in synergy_roots:
                print(f"RELICS_SYNERGY_ROOT={relic_id}|{synergy_id}")

            print(f"RELICS_RELIC_ITEM_CLASS_COUNT={len(relic_item_classes)}")
            for name in relic_item_classes:
                print(f"RELICS_RELIC_ITEM_CLASS={name}")

            synergy_owner_signatures = {}
            relic_constant_re = re.compile(
                r"(?:MANTLE|BELT|NECKLACE|BOOT|SKATE|STAFF|MASK|RING|SPHERE|FLUTE|HAT|CLOT|SHIELD|DISPERSER)",
                re.I,
            )
            for relic_id, class_path in probe_classes.items():
                raw = zf.read(class_path)
                printable = sorted({
                    m.decode("ascii", errors="ignore")
                    for m in re.findall(rb"[A-Za-z0-9_./:$-]{4,}", raw)
                })
                synergy_tokens = sorted(
                    s for s in printable
                    if (
                        "SynergyTemplate" in s
                        or "SynergyData" in s
                        or "AbilityConditionTemplate" in s
                        or "RelicConditionTemplate" in s
                        or "electricity" in s.lower()
                        or relic_constant_re.search(s)
                    )
                )
                synergy_owner_signatures[relic_id] = {
                    "class_sha256": digest(raw, "sha256"),
                    "tokens": synergy_tokens,
                }

            print(f"RELICS_SYNERGY_OWNER_COUNT={len(synergy_owner_signatures)}")
            for relic_id in sorted(synergy_owner_signatures):
                sig = synergy_owner_signatures[relic_id]
                print(f"RELICS_SYNERGY_OWNER_CLASS_SHA256={relic_id}|{sig['class_sha256']}")
                print(f"RELICS_SYNERGY_OWNER_TOKEN_COUNT={relic_id}|{len(sig['tokens'])}")
                for token in sig["tokens"]:
                    print(f"RELICS_SYNERGY_OWNER_TOKEN={relic_id}|{token}")
            print("RELICS_SYNERGY_OWNER_CLASS_HASH_EQUAL=" + str(
                synergy_owner_signatures["glitchy_mantle"]["class_sha256"]
                == synergy_owner_signatures["kinetic_belt"]["class_sha256"]
            ).lower())
            print("RELICS_SYNERGY_OWNER_TOKEN_SET_EQUAL=" + str(
                synergy_owner_signatures["glitchy_mantle"]["tokens"]
                == synergy_owner_signatures["kinetic_belt"]["tokens"]
            ).lower())

            print("RELICS_SYNERGY_TITLE_HASH_EQUAL=" + str(
                synergy_probe["glitchy_mantle"]["title"] == synergy_probe["kinetic_belt"]["title"]
            ).lower())
            print("RELICS_SYNERGY_DISABLED_DESCRIPTION_HASH_EQUAL=" + str(
                synergy_probe["glitchy_mantle"]["disabled"] == synergy_probe["kinetic_belt"]["disabled"]
            ).lower())
            print("RELICS_SYNERGY_ENABLED_DESCRIPTION_HASH_EQUAL=" + str(
                synergy_probe["glitchy_mantle"]["enabled"] == synergy_probe["kinetic_belt"]["enabled"]
            ).lower())
            for relic_id in synergy_probe_relics:
                for field, value in sorted(synergy_probe[relic_id].items()):
                    print(f"RELICS_SYNERGY_VALUE_SHA256={relic_id}|{field}|{value}")
                for value in class_probe[relic_id]:
                    print(f"RELICS_SYNERGY_CLASS_TOKEN={relic_id}|{value}")

            print(f"RELICS_LANG_CANDIDATE_COUNT={len(lang_candidates)}")
            for lang_path,key in lang_candidates[:1200]:
                print(f"RELICS_LANG_CANDIDATE={lang_path}|{key}")

            print(f"RELICS_ABILITY_CLASS_UTF8_CANDIDATE_COUNT={len(class_utf8_candidates)}")
            for name,hits in class_utf8_candidates[:400]:
                print(f"RELICS_ABILITY_CLASS_UTF8_CANDIDATE={name}|{','.join(hits)}")

            if not classes:
                raise RuntimeError("no classes found")
            print("RELICS_EXACT_BINARY_INVENTORY_AUDIT=true")
    return 0

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"RELICS_AUDIT_ERROR={type(exc).__name__}: {exc}", file=sys.stderr)
        raise
