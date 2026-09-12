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


def split_methods(text):
    lines = text.splitlines()
    out = []
    current = None
    for line in lines:
        if re.match(r"^  (public|private|protected|static)", line) and line.strip().endswith(";"):
            if current:
                out.append(current)
            current = {"header": line.strip(), "lines": [line]}
        elif current is not None:
            current["lines"].append(line)
    if current:
        out.append(current)
    return out


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


def instructions(method):
    inst = []
    for line in method["lines"]:
        m = re.match(r"\s*(\d+):\s+([a-z0-9_]+)(?:\s+([^/]+?))?(?:\s+//\s+(.*))?$", line)
        if not m:
            continue
        offset = int(m.group(1))
        op = m.group(2)
        operand = (m.group(3) or "").strip()
        comment = (m.group(4) or "").strip()
        inst.append((offset, op, operand, comment))
    return inst


def field_from_comment(comment):
    m = re.search(r"Field ([A-Za-z0-9_/$]+)\.([A-Za-z0-9_$]+):", comment)
    return None if not m else f"{m.group(1).replace('/', '.')}.{m.group(2)}"


def method_from_comment(comment):
    m = re.search(r"Method ([A-Za-z0-9_/$]+)\.([A-Za-z0-9_$<>]+):", comment)
    return None if not m else f"{m.group(1).replace('/', '.')}.{m.group(2)}"


def string_from_comment(comment):
    m = re.search(r"String ([A-Za-z0-9_./:-]+)$", comment)
    return None if not m else m.group(1)


def branch_guard(methods, field_suffix, guarded_needles):
    findings = []
    for method in methods:
        ins = instructions(method)
        for i, (off, op, operand, comment) in enumerate(ins):
            fld = field_from_comment(comment)
            if not fld or not fld.endswith(field_suffix):
                continue
            branch = None
            for j in range(i + 1, min(i + 5, len(ins))):
                if ins[j][1] in ("ifeq", "ifne") and ins[j][2].isdigit():
                    branch = ins[j]
                    break
            if not branch:
                continue
            target = int(branch[2])
            fallthrough_refs = []
            for roff, rop, roperand, rcomment in ins:
                if branch[0] < roff < target:
                    ref = field_from_comment(rcomment) or method_from_comment(rcomment)
                    if ref and any(n in ref for n in guarded_needles):
                        fallthrough_refs.append(ref)
            if fallthrough_refs:
                findings.append({
                    "method": method["header"].split("(")[0],
                    "branch_opcode": branch[1],
                    "branch_target": target,
                    "guarded_fallthrough_refs": sorted(set(fallthrough_refs)),
                    "inference": (
                        "true_skips_guarded_fallthrough" if branch[1] == "ifne" else
                        "false_skips_guarded_fallthrough"
                    ),
                })
    return findings


def loaded_mod_guards(methods, mod_id, guarded_needles):
    findings = []
    for method in methods:
        ins = instructions(method)
        string_indexes = [i for i, x in enumerate(ins) if string_from_comment(x[3]) == mod_id]
        for si in string_indexes:
            load_call = None
            branch = None
            for j in range(si, min(si + 8, len(ins))):
                ref = method_from_comment(ins[j][3])
                if ref and ref.endswith("ModList.isLoaded"):
                    load_call = ins[j]
                if load_call and ins[j][1] in ("ifeq", "ifne") and ins[j][2].isdigit():
                    branch = ins[j]
                    break
            if not branch:
                continue
            target = int(branch[2])
            refs_between = []
            for roff, rop, roperand, rcomment in ins:
                if branch[0] < roff < target:
                    ref = field_from_comment(rcomment) or method_from_comment(rcomment)
                    if ref and any(n in ref for n in guarded_needles):
                        refs_between.append(ref)
            if refs_between:
                findings.append({
                    "method": method["header"].split("(")[0],
                    "mod_id": mod_id,
                    "branch_opcode": branch[1],
                    "guarded_fallthrough_refs": sorted(set(refs_between)),
                    "inference": (
                        "loaded_false_skips_guarded_fallthrough" if branch[1] == "ifeq" else
                        "loaded_true_skips_guarded_fallthrough"
                    ),
                })
    return findings


def config_default(code_text):
    methods = split_methods(code_text)
    candidates = []
    for method in methods:
        ins = instructions(method)
        for i, item in enumerate(ins):
            if string_from_comment(item[3]) != "disableGazeRites":
                continue
            window = ins[i:i+12]
            bool_const = None
            has_define = False
            for _, op, operand, comment in window:
                if op == "iconst_0":
                    bool_const = False
                elif op == "iconst_1":
                    bool_const = True
                ref = method_from_comment(comment)
                if ref and (ref.endswith("ModConfigSpec$Builder.define") or ref.endswith("ModConfigSpec$Builder.defineListAllowEmpty")):
                    has_define = True
                    break
            if has_define and bool_const is not None:
                candidates.append(bool_const)
    return candidates[0] if len(set(candidates)) == 1 else None


result = {}

progress = javap("com.strawberry.gaze.client.screens.codex.screens.GazeProgressionScreen", code=True)
progress_methods = split_methods(progress)
setup_family = [m for m in progress_methods if "setupEntries" in m["header"]]
setup_text = "\n".join("\n".join(m["lines"]) for m in setup_family)
f, m, s = refs(setup_text)
rite_fields = [x for x in f if ".GazeRiteRegistry.GAZE_" in x]
geas_fields = [x for x in f if ".GazeGeasEffectTypeRegistry." in x]
rune_fields = [x for x in f if ".GazeMod.RUNE_OF_" in x]
result["progression_setup_family"] = {
    "method_count": len(setup_family),
    "rite_fields": rite_fields,
    "geas_fields": geas_fields,
    "rune_fields": rune_fields,
    "rite_field_count": len(rite_fields),
    "geas_field_count": len(geas_fields),
    "rune_field_count": len(rune_fields),
    "has_add_geas_entry_call": any(x.endswith("GazeProgressionScreen.addGeasEntry") for x in m),
    "has_spirit_rite_recipe_page": any("SpiritRiteRecipePage.<init>" in x for x in m),
    "has_spirit_rite_text_page": any("SpiritRiteTextPage.<init>" in x for x in m),
    "has_geas_info_page": any("GeasInfoPage.<init>" in x for x in m),
}

mod = javap("com.strawberry.gaze.GazeMod", code=True)
mod_methods = split_methods(mod)
f, m, s = refs(mod)
result["gaze_mod_refs"] = {
    "config_fields": [x for x in f if "config" in x.lower() or "disable" in x.lower()],
    "rite_refs": [x for x in f + m if "GazeRiteRegistry" in x or "GazeSpiritRiteEffectTypes" in x],
    "geas_refs": [x for x in f + m if "GazeGeasEffectTypeRegistry" in x],
    "irons_refs": [x for x in f + m if "IronsCompat" in x or "SpellRegistry" in x],
}
result["rite_disable_gate"] = branch_guard(
    mod_methods,
    "Config.disableGazeRites",
    ("GazeRiteRegistry", "GazeSpiritRiteEffectTypes"),
)
result["irons_loaded_gate"] = loaded_mod_guards(
    mod_methods,
    "irons_spellbooks",
    ("IronsCompat",),
)

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

config_code = javap("com.strawberry.gaze.Config", code=True)
config_sig = javap("com.strawberry.gaze.Config", code=False)
result["config"] = {
    "matching_signatures": [line.strip() for line in config_sig.splitlines() if "DISABLE_GAZE_RITES" in line or "disableGazeRites" in line],
    "source_default_disable_gaze_rites": config_default(config_code),
    "scope": "COMMON" if "ModConfig$Type.COMMON" in mod else None,
}

with zipfile.ZipFile(JAR) as z:
    names = sorted(z.namelist())
    resource_hits = []
    for name in names:
        if not (name.endswith(".json") or name.endswith(".toml") or name.endswith(".mcmeta")):
            continue
        try:
            text = z.read(name).decode("utf-8", "strict").lower()
        except Exception:
            continue
        hits = [needle for needle in ("soulward_shield", "encyclopedia_unveiled") if needle in text]
        if hits:
            resource_hits.append({"path": name, "tokens": hits})
result["irons_resource_hits"] = resource_hits

OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps(result, indent=2, sort_keys=True))
