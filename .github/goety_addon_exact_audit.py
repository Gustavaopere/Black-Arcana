from __future__ import annotations

import json
import os
import re
import zipfile
from pathlib import Path

JAR = Path(os.environ["JAR_PATH"])
PROVIDER_NS = os.environ["PROVIDER_NS"]
OUT = Path(os.environ.get("AUDIT_OUT", "audit-out"))
OUT.mkdir(parents=True, exist_ok=True)

KEYWORDS = ("focus", "ritual", "spell", "summon", "servant", "ability", "registry", "item")
SEMANTIC_KEYWORDS = ("focus", "ritual", "spell", "summon", "ability")


def resource_id(value):
    if isinstance(value, str) and re.fullmatch(r"[a-z0-9_.-]+:[a-z0-9_./-]+", value):
        return value
    if isinstance(value, dict):
        for key in ("id", "item", "name", "entity", "entity_type", "type"):
            v = value.get(key)
            if isinstance(v, str) and re.fullmatch(r"[a-z0-9_.-]+:[a-z0-9_./-]+", v):
                return v
    return None


def printable_identifiers(raw: bytes):
    found = set()
    for m in re.finditer(rb"[A-Za-z0-9_/$.:;<>-]{4,180}", raw):
        s = m.group(0).decode("ascii", "ignore")
        low = s.lower()
        if not any(k in low for k in SEMANTIC_KEYWORDS):
            continue
        if "http" in low or "minecraftforge" in low:
            continue
        found.add(s)
    return sorted(found)


with zipfile.ZipFile(JAR) as z:
    names = sorted(z.namelist())
    classes = [n for n in names if n.endswith(".class") and not n.startswith("META-INF/versions/")]
    data_paths = [n for n in names if n.startswith("data/")]
    json_paths = [n for n in data_paths if n.endswith(".json")]
    relevant_classes = [n for n in classes if any(k in n.lower() for k in KEYWORDS)]

    metadata_sections = []
    for name in ("META-INF/neoforge.mods.toml", "META-INF/mods.toml", "META-INF/MANIFEST.MF"):
        if name in names:
            metadata_sections.append(f"--- {name} ---\n{z.read(name).decode('utf-8', 'replace')}\n")
    (OUT / "metadata.txt").write_text("\n".join(metadata_sections), encoding="utf-8")
    (OUT / "archive-paths.txt").write_text("\n".join(names) + "\n", encoding="utf-8")
    (OUT / "class-paths.txt").write_text("\n".join(classes) + "\n", encoding="utf-8")
    (OUT / "relevant-class-paths.txt").write_text("\n".join(relevant_classes) + "\n", encoding="utf-8")
    (OUT / "data-paths.txt").write_text("\n".join(data_paths) + "\n", encoding="utf-8")

    identifier_lines = []
    indicator_hits = {k: [] for k in ("Focus", "Ritual", "Spell", "Summon", "Ability", "DeferredRegister")}
    for name in classes:
        raw = z.read(name)
        for key in indicator_hits:
            if key.encode() in raw:
                indicator_hits[key].append(name)
        ids = printable_identifiers(raw)
        if ids:
            identifier_lines.append(f"--- {name} ---")
            identifier_lines.extend(ids)
    (OUT / "filtered-class-identifiers.txt").write_text("\n".join(identifier_lines) + "\n", encoding="utf-8")
    for key, paths in indicator_hits.items():
        (OUT / f"indicator-{key}.txt").write_text("\n".join(sorted(paths)) + "\n", encoding="utf-8")

    json_summary = []
    ritual_json = []
    semantic_json = []
    invalid_json = []
    for name in json_paths:
        try:
            obj = json.loads(z.read(name).decode("utf-8-sig"))
        except Exception:
            invalid_json.append(name)
            continue
        typ = obj.get("type") if isinstance(obj, dict) else None
        rec = {"path": name}
        if isinstance(typ, str):
            rec["type"] = typ
        if isinstance(obj, dict):
            for key in ("ritual_type", "result", "output", "entity", "entity_type", "focus", "spell"):
                rid = resource_id(obj.get(key))
                if rid:
                    rec[key] = rid
        json_summary.append(rec)
        low = (name + " " + str(typ or "")).lower()
        if "ritual" in low:
            ritual_json.append(rec)
        if any(k in low for k in SEMANTIC_KEYWORDS):
            semantic_json.append(rec)

    def dump_jsonl(path, rows):
        path.write_text("\n".join(json.dumps(x, sort_keys=True) for x in rows) + ("\n" if rows else ""), encoding="utf-8")

    dump_jsonl(OUT / "json-structural-summary.jsonl", json_summary)
    dump_jsonl(OUT / "ritual-json-summary.jsonl", ritual_json)
    dump_jsonl(OUT / "semantic-json-summary.jsonl", semantic_json)
    (OUT / "invalid-json-paths.txt").write_text("\n".join(invalid_json) + ("\n" if invalid_json else ""), encoding="utf-8")

    summary = [
        f"provider_namespace={PROVIDER_NS}",
        f"class_count={len(classes)}",
        f"relevant_class_count={len(relevant_classes)}",
        f"data_path_count={len(data_paths)}",
        f"json_count={len(json_paths)}",
        f"ritual_json_count={len(ritual_json)}",
        f"semantic_json_count={len(semantic_json)}",
    ]
    for key in indicator_hits:
        summary.append(f"{key}_class_hits={len(indicator_hits[key])}")
    (OUT / "summary.txt").write_text("\n".join(summary) + "\n", encoding="utf-8")
