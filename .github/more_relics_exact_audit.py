#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import subprocess
import sys
import zipfile
from collections import defaultdict
from pathlib import Path

if len(sys.argv) != 3:
    raise SystemExit("usage: more_relics_exact_audit.py <jar> <out-dir>")

jar = Path(sys.argv[1])
out = Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)

with zipfile.ZipFile(jar) as z:
    names = sorted(z.namelist())
    classes = [n for n in names if n.endswith(".class") and not n.startswith("META-INF/versions/")]
    provider_classes = [n for n in classes if b"morerelics" in z.read(n).lower()]
    ability_classes = [n for n in provider_classes if b"AbilityTemplate" in z.read(n)]
    loot_classes = [n for n in provider_classes if b"LootTemplate" in z.read(n)]

    metadata = []
    for n in ("META-INF/neoforge.mods.toml", "META-INF/mods.toml", "META-INF/MANIFEST.MF"):
        if n in names:
            metadata.append(f"--- {n} ---\n" + z.read(n).decode("utf-8", "replace") + "\n")
    (out / "metadata.txt").write_text("\n".join(metadata), encoding="utf-8")

    archive_summary = [
        f"archive_entry_count={len(names)}",
        f"class_count={len(classes)}",
        f"provider_class_count={len(provider_classes)}",
        f"ability_template_class_count={len(ability_classes)}",
        f"loot_template_class_count={len(loot_classes)}",
    ]
    (out / "archive-summary.txt").write_text("\n".join(archive_summary) + "\n", encoding="utf-8")
    (out / "ability-template-classes.txt").write_text("\n".join(ability_classes) + ("\n" if ability_classes else ""), encoding="utf-8")
    (out / "loot-template-classes.txt").write_text("\n".join(loot_classes) + ("\n" if loot_classes else ""), encoding="utf-8")

    item_model_ids = []
    for n in names:
        m = re.fullmatch(r"assets/morerelics/models/item/([a-z0-9_./-]+)\.json", n)
        if m:
            item_model_ids.append(m.group(1))
    (out / "item-model-ids.txt").write_text("\n".join(sorted(set(item_model_ids))) + ("\n" if item_model_ids else ""), encoding="utf-8")

    lang_name = "assets/morerelics/lang/en_us.json"
    lang = {}
    if lang_name in names:
        lang = json.loads(z.read(lang_name).decode("utf-8"))
    item_lang = []
    ability_lang = []
    for key, value in sorted(lang.items()):
        if key.startswith("item.morerelics."):
            item_lang.append((key.removeprefix("item.morerelics."), str(value)))
        if ".ability." in key and ("relic" in key.lower() or "description" in key.lower()):
            ability_lang.append((key, str(value)))
    with (out / "lang-item-ids.tsv").open("w", encoding="utf-8") as f:
        for rid, label in item_lang:
            f.write(f"{rid}\t{label}\n")
    with (out / "lang-ability-keys.tsv").open("w", encoding="utf-8") as f:
        for key, label in ability_lang:
            f.write(f"{key}\t{label}\n")


def class_name(path: str) -> str:
    return path[:-6].replace("/", ".")


def javap(path: str) -> list[str]:
    proc = subprocess.run(
        ["javap", "-classpath", str(jar), "-p", "-c", class_name(path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    return proc.stdout.splitlines()


def prior_string(lines: list[str], idx: int, window: int = 12) -> str | None:
    for j in range(idx - 1, max(-1, idx - window - 1), -1):
        m = re.search(r"// String ([^\s]+)", lines[j])
        if m:
            return m.group(1)
    return None


ability_pairs = []
loot_observations = []
for path in ability_classes:
    lines = javap(path)
    for i, line in enumerate(lines):
        if "AbilityTemplate.builder" in line:
            root = prior_string(lines, i)
            ability_pairs.append((path, root or "<UNRESOLVED>"))
for path in loot_classes:
    lines = javap(path)
    for i, line in enumerate(lines):
        if "LootTemplate.builder" in line:
            surrounding = []
            for j in range(max(0, i - 10), min(len(lines), i + 8)):
                s = lines[j].strip()
                if "// Field " in s or "// String " in s:
                    surrounding.append(s.split("// ", 1)[1])
            loot_observations.append((path, " | ".join(surrounding[:12])))

ability_pairs = sorted(set(ability_pairs))
with (out / "ability-builder-roots.tsv").open("w", encoding="utf-8") as f:
    for cls, root in ability_pairs:
        f.write(f"{cls}\t{root}\n")
with (out / "loot-builder-observations.tsv").open("w", encoding="utf-8") as f:
    for cls, obs in sorted(set(loot_observations)):
        f.write(f"{cls}\t{obs}\n")

resolved = [(c, r) for c, r in ability_pairs if r != "<UNRESOLVED>"]
unresolved = [(c, r) for c, r in ability_pairs if r == "<UNRESOLVED>"]
roots = sorted({r for _, r in resolved})

# Normalize localization owner/ability keys when they follow the Relics convention.
lang_roots = []
for key, _ in ability_lang:
    m = re.search(r"(?:relics\.)?description\.([a-z0-9_]+)\.ability\.([a-z0-9_]+)$", key)
    if m:
        lang_roots.append((m.group(1), m.group(2), key))
lang_root_ids = sorted({ability for _, ability, _ in lang_roots})

with (out / "lang-owner-ability-roots.tsv").open("w", encoding="utf-8") as f:
    for owner, ability, key in sorted(set(lang_roots)):
        f.write(f"{owner}\t{ability}\t{key}\n")

summary = [
    f"ability_builder_call_count={len(ability_pairs)}",
    f"ability_builder_resolved_count={len(resolved)}",
    f"ability_builder_unresolved_count={len(unresolved)}",
    f"ability_builder_unique_root_count={len(roots)}",
    f"lang_item_id_count={len(item_lang)}",
    f"lang_ability_key_count={len(ability_lang)}",
    f"lang_owner_ability_pair_count={len(set((o,a) for o,a,_ in lang_roots))}",
    f"lang_unique_ability_root_count={len(lang_root_ids)}",
    f"item_model_id_count={len(set(item_model_ids))}",
]
(out / "semantic-summary.txt").write_text("\n".join(summary) + "\n", encoding="utf-8")

(out / "ability-root-ids.txt").write_text("\n".join(roots) + ("\n" if roots else ""), encoding="utf-8")
(out / "lang-ability-root-ids.txt").write_text("\n".join(lang_root_ids) + ("\n" if lang_root_ids else ""), encoding="utf-8")
(out / "unresolved-builder-classes.txt").write_text("\n".join(c for c, _ in unresolved) + ("\n" if unresolved else ""), encoding="utf-8")

builder_only = sorted(set(roots) - set(lang_root_ids))
lang_only = sorted(set(lang_root_ids) - set(roots))
with (out / "root-diff.txt").open("w", encoding="utf-8") as f:
    f.write("builder_only:\n")
    for x in builder_only:
        f.write(x + "\n")
    f.write("lang_only:\n")
    for x in lang_only:
        f.write(x + "\n")

# Fail only on extraction quality, not on localization equality.
if unresolved:
    raise SystemExit(f"unresolved AbilityTemplate.builder calls: {len(unresolved)}")
if not ability_pairs:
    raise SystemExit("no AbilityTemplate.builder calls found")
