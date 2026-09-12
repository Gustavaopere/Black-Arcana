#!/usr/bin/env python3
import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path

JAR = Path(sys.argv[1])
OUT = Path(sys.argv[2])
OUT.parent.mkdir(parents=True, exist_ok=True)


def javap(cls, code=False):
    args = ["javap", "-classpath", str(JAR), "-p"]
    if code:
        args.append("-c")
    args.append(cls)
    p = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=30)
    return p.stdout


def method_block(text, method_marker):
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if method_marker in line and line.strip().endswith(";"):
            start = i
            break
    if start is None:
        return ""
    block = []
    for line in lines[start:]:
        if block and re.match(r"^  (public|private|protected|static)", line) and line.strip().endswith(";"):
            break
        block.append(line)
    return "\n".join(block)


def refs(text):
    field_refs = set()
    method_refs = set()
    strings = set()
    for line in text.splitlines():
        m = re.search(r"// Field ([A-Za-z0-9_/$]+)\.([A-Za-z0-9_$]+):", line)
        if m:
            field_refs.add(f"{m.group(1).replace('/', '.')}.{m.group(2)}")
        m = re.search(r"// Method ([A-Za-z0-9_/$]+)\.([A-Za-z0-9_$<>]+):", line)
        if m:
            method_refs.add(f"{m.group(1).replace('/', '.')}.{m.group(2)}")
        m = re.search(r"// String ([A-Za-z0-9_./:-]+)$", line)
        if m:
            strings.add(m.group(1))
    return sorted(field_refs), sorted(method_refs), sorted(strings)

result = {}

progress = javap("com.strawberry.gaze.client.screens.codex.screens.GazeProgressionScreen", code=True)
setup = method_block(progress, " setupEntries()")
f, m, s = refs(setup)
result["progression_setup"] = {
    "rite_fields": [x for x in f if ".GazeRiteRegistry.GAZE_" in x],
    "geas_fields": [x for x in f if ".GazeGeasEffectTypeRegistry." in x],
    "rune_fields": [x for x in f if ".GazeMod.RUNE_OF_" in x],
    "rite_field_count": len([x for x in f if ".GazeRiteRegistry.GAZE_" in x]),
    "geas_field_count": len([x for x in f if ".GazeGeasEffectTypeRegistry." in x]),
    "rune_field_count": len([x for x in f if ".GazeMod.RUNE_OF_" in x]),
    "has_spirit_rite_recipe_page": "com.sammy.malum.client.screen.codex.pages.recipe.SpiritRiteRecipePage.<init>" in m,
    "has_geas_info_page": "com.sammy.malum.client.screen.codex.pages.text.GeasInfoPage.<init>" in m,
}

mod = javap("com.strawberry.gaze.GazeMod", code=True)
f, m, s = refs(mod)
result["gaze_mod_refs"] = {
    "config_fields": [x for x in f if "config" in x.lower() or "disable" in x.lower()],
    "rite_refs": [x for x in f + m if "GazeRiteRegistry" in x or "GazeSpiritRiteEffectTypes" in x],
    "irons_refs": [x for x in f + m if "IronsCompat" in x or "SpellRegistry" in x],
    "strings": [x for x in s if "rite" in x.lower() or "iron" in x.lower() or "disable" in x.lower()],
}

irons = javap("com.strawberry.gaze.compat.irons_spellbooks.IronsCompat", code=True)
f, m, s = refs(irons)
result["irons_compat_refs"] = {
    "spell_registry_refs": [x for x in f + m if "SpellRegistry" in x],
    "strings": s,
}

spell = javap("com.strawberry.gaze.compat.irons_spellbooks.registry.SpellRegistry", code=True)
f, m, s = refs(spell)
result["spell_registry"] = {
    "declared_signature": [line.strip() for line in javap("com.strawberry.gaze.compat.irons_spellbooks.registry.SpellRegistry").splitlines() if "Supplier<io.redspace.ironsspellbooks.api.spells.AbstractSpell>" in line],
    "strings": s,
    "field_refs": f,
    "method_refs": [x for x in m if "SpellRegistry" in x or "ironsspellbooks" in x.lower()],
}

with zipfile.ZipFile(JAR) as z:
    config_classes = sorted(n[:-6].replace('/', '.') for n in z.namelist() if n.endswith('.class') and 'config' in n.lower() and '$' not in n)
result["config_classes"] = config_classes
config_hits = []
for cls in config_classes:
    sig = javap(cls, code=False)
    code = javap(cls, code=True)
    if "disableGazeRites" in sig or "disableGazeRites" in code or "disable_gaze" in code.lower():
        f, m, s = refs(code)
        config_hits.append({
            "class": cls,
            "matching_signatures": [line.strip() for line in sig.splitlines() if "disableGazeRites" in line or "disable" in line.lower() and "rite" in line.lower()],
            "field_refs": [x for x in f if "disable" in x.lower() or "config" in x.lower()],
            "strings": [x for x in s if "disable" in x.lower() or "rite" in x.lower()],
        })
result["config_hits"] = config_hits

OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps(result, indent=2, sort_keys=True))
