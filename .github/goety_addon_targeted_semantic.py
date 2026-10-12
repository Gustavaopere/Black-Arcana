from __future__ import annotations

import json
import os
import re
import zipfile
from pathlib import Path

JAR = Path(os.environ["JAR_PATH"])
ROOT = os.environ["RECIPE_ROOT"].rstrip("/") + "/"
OUT = Path(os.environ.get("AUDIT_OUT", "audit-targeted"))
OUT.mkdir(parents=True, exist_ok=True)
RID = re.compile(r"^[a-z0-9_.-]+:[a-z0-9_./-]+$")
SEMANTIC_KEY = re.compile(r"(result|output|entity|summon|convert|target|from|to|mob)", re.I)


def ids(value):
    out = set()
    if isinstance(value, str) and RID.fullmatch(value):
        out.add(value)
    elif isinstance(value, dict):
        for k, v in value.items():
            if SEMANTIC_KEY.search(str(k)):
                out |= ids(v)
            elif str(k).lower() in {"id", "type"} and isinstance(v, str) and RID.fullmatch(v):
                out.add(v)
    elif isinstance(value, list):
        for x in value:
            out |= ids(x)
    return out


def condition_skeleton(obj):
    raw = None
    if isinstance(obj, dict):
        raw = obj.get("neoforge:conditions", obj.get("conditions"))
    if raw is None:
        return []
    records = []
    seq = raw if isinstance(raw, list) else [raw]
    for cond in seq:
        if not isinstance(cond, dict):
            continue
        rec = {}
        typ = cond.get("type")
        if isinstance(typ, str): rec["type"] = typ
        for key in ("modid", "mod_id", "mod"):
            val = cond.get(key)
            if isinstance(val, str): rec["modid"] = val
        # nested NOT/OR conditions: retain only type/mod IDs, no recipe payloads
        nested = []
        for key in ("value", "values", "conditions"):
            val = cond.get(key)
            if isinstance(val, dict): val = [val]
            if isinstance(val, list):
                for sub in val:
                    if isinstance(sub, dict):
                        s = {}
                        if isinstance(sub.get("type"), str): s["type"] = sub["type"]
                        for mk in ("modid", "mod_id", "mod"):
                            if isinstance(sub.get(mk), str): s["modid"] = sub[mk]
                        if s: nested.append(s)
        if nested: rec["nested"] = nested
        if rec: records.append(rec)
    return records

with zipfile.ZipFile(JAR) as z:
    rows = []
    names = sorted(n for n in z.namelist() if n.startswith(ROOT) and n.endswith(".json"))
    for name in names:
        try:
            obj = json.loads(z.read(name).decode("utf-8-sig"))
        except Exception:
            continue
        if not isinstance(obj, dict) or obj.get("type") != "goety:ritual":
            continue
        top_keys = sorted(str(k) for k in obj.keys())
        result = obj.get("result")
        result_ids = sorted(ids(result))
        outcome = set()
        for k, v in obj.items():
            if SEMANTIC_KEY.search(str(k)) and str(k).lower() not in {"ingredients", "ingredient"}:
                outcome |= ids(v)
        focus_result = [x for x in result_ids if x.endswith("_focus")]
        rows.append({
            "path": name,
            "ritual_type": obj.get("ritual_type") if isinstance(obj.get("ritual_type"), str) else None,
            "top_keys": top_keys,
            "result_ids": result_ids,
            "semantic_outcome_ids": sorted(outcome),
            "conditions": condition_skeleton(obj),
            "focus_acquisition": bool(focus_result),
        })

    (OUT / "ritual-targeted.jsonl").write_text("\n".join(json.dumps(r, sort_keys=True) for r in rows) + ("\n" if rows else ""), encoding="utf-8")
    focus = [r for r in rows if r["focus_acquisition"]]
    nonfocus = [r for r in rows if not r["focus_acquisition"]]
    modids = sorted({c.get("modid") for r in rows for c in r["conditions"] if c.get("modid")})
    summary = [
        f"ritual_count={len(rows)}",
        f"focus_acquisition_count={len(focus)}",
        f"non_focus_ritual_count={len(nonfocus)}",
        f"conditioned_ritual_count={sum(bool(r['conditions']) for r in rows)}",
        f"condition_modids={';'.join(modids) if modids else '<none>'}",
    ]
    (OUT / "summary.txt").write_text("\n".join(summary) + "\n", encoding="utf-8")
