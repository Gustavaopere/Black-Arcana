#!/usr/bin/env python3
import hashlib
import json
import re
import struct
import subprocess
import sys
import zipfile
from pathlib import Path

EXPECTED_SHA1 = "a8cb3190bde157f78160ce65c202ce2d47fb2041"
KEYWORDS = ("geas", "rite", "rune", "spiritrite", "spirit_rite", "deferredregister", "deferredholder")
TYPE_MARKERS = ("SpiritRite", "Geas", "Rune", "DeferredRegister", "DeferredHolder")
SAFE_TOKEN = re.compile(r"^[A-Za-z0-9_.$:/<>;()\[\]-]+$")
ID_TOKEN = re.compile(r"^[a-z0-9_.-]+:[a-z0-9_./-]+$")
SIMPLE_ID = re.compile(r"^[a-z0-9_./-]{3,80}$")


def sha1(path: Path) -> str:
    h = hashlib.sha1()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def cp_utf8(data: bytes):
    if data[:4] != b"\xca\xfe\xba\xbe":
        return []
    pos = 8
    cp_count = struct.unpack_from(">H", data, pos)[0]
    pos += 2
    out = []
    i = 1
    while i < cp_count:
        tag = data[pos]
        pos += 1
        if tag == 1:
            n = struct.unpack_from(">H", data, pos)[0]
            pos += 2
            raw = data[pos:pos+n]
            pos += n
            try:
                out.append(raw.decode("utf-8", "strict"))
            except UnicodeDecodeError:
                pass
        elif tag in (3, 4):
            pos += 4
        elif tag in (5, 6):
            pos += 8
            i += 1
        elif tag in (7, 8, 16, 19, 20):
            pos += 2
        elif tag in (9, 10, 11, 12, 17, 18):
            pos += 4
        elif tag == 15:
            pos += 3
        else:
            raise ValueError(f"unknown constant-pool tag {tag}")
        i += 1
    return out


def safe_constants(values):
    keep = []
    for s in values:
        if len(s) > 180 or not SAFE_TOKEN.fullmatch(s):
            continue
        low = s.lower()
        if (
            any(k in low for k in KEYWORDS)
            or any(m.lower() in low for m in TYPE_MARKERS)
            or ID_TOKEN.fullmatch(s)
            or (SIMPLE_ID.fullmatch(s) and any(k in low for k in ("corrupt", "wicked", "sacred", "aqua", "domain", "malice", "sword", "pact")))
        ):
            keep.append(s)
    return sorted(set(keep))


def walk_json_keys(obj, prefix=""):
    out = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            p = f"{prefix}.{k}" if prefix else str(k)
            low = str(k).lower()
            if any(w in low for w in ("geas", "rite", "rune")):
                out.append(p)
            out.extend(walk_json_keys(v, p))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            out.extend(walk_json_keys(v, f"{prefix}[{i}]"))
    elif isinstance(obj, str):
        if ID_TOKEN.fullmatch(obj) and any(w in obj.lower() for w in ("geas", "rite", "rune", "gaze")):
            out.append(f"{prefix}={obj}")
    return out


def main():
    if len(sys.argv) != 3:
        raise SystemExit("usage: gaze_exact_artifact_audit.py <jar> <outdir>")
    jar = Path(sys.argv[1])
    outdir = Path(sys.argv[2])
    outdir.mkdir(parents=True, exist_ok=True)

    actual = sha1(jar)
    if actual != EXPECTED_SHA1:
        raise SystemExit(f"SHA1 mismatch: expected {EXPECTED_SHA1}, got {actual}")

    summary = {"sha1": actual}
    with zipfile.ZipFile(jar) as z:
        names = sorted(z.namelist())
        summary["entry_count"] = len(names)
        relevant_entries = [n for n in names if any(k in n.lower() for k in ("geas", "rite", "rune", "registry"))]
        (outdir / "relevant-entries.txt").write_text("\n".join(relevant_entries) + "\n", encoding="utf-8")

        metadata = []
        for name in ("META-INF/neoforge.mods.toml", "META-INF/mods.toml"):
            if name in names:
                txt = z.read(name).decode("utf-8", "replace")
                for line in txt.splitlines():
                    if any(k in line for k in ("modId", "version", "displayName", "license")):
                        metadata.append(f"{name}: {line.strip()}")
        (outdir / "identity.txt").write_text(
            f"sha1={actual}\nexpected_sha1={EXPECTED_SHA1}\n" + "\n".join(metadata) + "\n",
            encoding="utf-8",
        )

        json_hits = []
        for name in names:
            low = name.lower()
            if not name.endswith(".json") or not (low.startswith("assets/gaze/") or low.startswith("data/gaze/")):
                continue
            try:
                obj = json.loads(z.read(name).decode("utf-8"))
            except Exception:
                continue
            keys = walk_json_keys(obj)
            if keys:
                json_hits.append(f"[{name}]")
                json_hits.extend(sorted(set(keys)))
        (outdir / "json-key-evidence.txt").write_text("\n".join(json_hits) + "\n", encoding="utf-8")

        selected = []
        class_constants = []
        for name in names:
            if not name.endswith(".class"):
                continue
            try:
                values = cp_utf8(z.read(name))
            except Exception:
                continue
            lows = [v.lower() for v in values]
            structural = any(any(m.lower() in v for m in TYPE_MARKERS) for v in lows)
            path_relevant = any(k in name.lower() for k in ("geas", "rite", "rune", "registr"))
            if structural or path_relevant:
                selected.append(name)
                kept = safe_constants(values)
                if kept:
                    class_constants.append(f"[{name}]")
                    class_constants.extend(kept)
        (outdir / "selected-classes.txt").write_text("\n".join(sorted(set(selected))) + "\n", encoding="utf-8")
        (outdir / "class-constant-evidence.txt").write_text("\n".join(class_constants) + "\n", encoding="utf-8")
        summary["selected_class_count"] = len(set(selected))

    javap_out = []
    selected_classes = []
    for line in (outdir / "selected-classes.txt").read_text(encoding="utf-8").splitlines():
        if line.endswith(".class") and "$" not in line:
            selected_classes.append(line[:-6].replace("/", "."))
    for cls in selected_classes[:120]:
        proc = subprocess.run(
            ["javap", "-classpath", str(jar), "-p", cls],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=20,
        )
        txt = proc.stdout
        if any(marker in txt for marker in TYPE_MARKERS) or any(k in cls.lower() for k in ("geas", "rite", "rune", "registr")):
            javap_out.append(f"===== {cls} =====")
            javap_out.append(txt.strip())
    (outdir / "javap-signatures.txt").write_text("\n".join(javap_out) + "\n", encoding="utf-8")

    (outdir / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
