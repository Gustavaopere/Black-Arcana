#!/usr/bin/env python3
import hashlib
import json
import re
import struct
import urllib.request
import zipfile
from pathlib import Path

URL = "https://mediafilez.forgecdn.net/files/8098/233/acolyte-1.0.3.jar"
JAR = Path("build/acolyte-1.0.3.jar")
JAR.parent.mkdir(parents=True, exist_ok=True)

with urllib.request.urlopen(URL, timeout=60) as response:
    data = response.read()
JAR.write_bytes(data)
if not data.startswith(b"PK"):
    raise SystemExit("download is not a JAR/ZIP")

print("=== HASHES ===")
print("SHA1", hashlib.sha1(data).hexdigest())
print("SHA256", hashlib.sha256(data).hexdigest())

def u1(b, o):
    return b[o], o + 1

def u2(b, o):
    return struct.unpack_from(">H", b, o)[0], o + 2

def parse_class(data):
    if data[:4] != b"\xca\xfe\xba\xbe":
        raise ValueError("not class")
    o = 8
    cp_count, o = u2(data, o)
    cp = [None] * cp_count
    i = 1
    while i < cp_count:
        tag, o = u1(data, o)
        if tag == 1:
            n, o = u2(data, o)
            cp[i] = ("Utf8", data[o:o+n].decode("utf-8", "replace"))
            o += n
        elif tag in (3, 4):
            cp[i] = ("Num",)
            o += 4
        elif tag in (5, 6):
            cp[i] = ("Wide",)
            o += 8
            i += 1
        elif tag in (7, 8, 16, 19, 20):
            idx, o = u2(data, o)
            cp[i] = ("Idx", tag, idx)
        elif tag in (9, 10, 11):
            a, o = u2(data, o)
            c, o = u2(data, o)
            cp[i] = ("Ref", tag, a, c)
        elif tag == 12:
            a, o = u2(data, o)
            c, o = u2(data, o)
            cp[i] = ("NT", a, c)
        elif tag == 15:
            kind, o = u1(data, o)
            idx, o = u2(data, o)
            cp[i] = ("MH", kind, idx)
        elif tag in (17, 18):
            a, o = u2(data, o)
            c, o = u2(data, o)
            cp[i] = ("Dyn", tag, a, c)
        else:
            raise ValueError(f"unknown cp tag {tag}")
        i += 1

    _, o = u2(data, o)
    this_idx, o = u2(data, o)
    super_idx, o = u2(data, o)

    def utf(idx):
        e = cp[idx]
        return e[1] if e and e[0] == "Utf8" else None

    def cls(idx):
        if idx == 0:
            return None
        e = cp[idx]
        if not e or e[0] != "Idx" or e[1] != 7:
            return None
        return utf(e[2])

    def nt(idx):
        e = cp[idx]
        if not e or e[0] != "NT":
            return (None, None)
        return utf(e[1]), utf(e[2])

    fieldrefs = []
    methodrefs = []
    for e in cp:
        if not e or e[0] != "Ref":
            continue
        owner = cls(e[2])
        name, desc = nt(e[3])
        row = (owner, name, desc)
        if e[1] == 9:
            fieldrefs.append(row)
        else:
            methodrefs.append(row)

    utf8 = [e[1] for e in cp if e and e[0] == "Utf8"]
    return {
        "this": cls(this_idx),
        "super": cls(super_idx),
        "fieldrefs": fieldrefs,
        "methodrefs": methodrefs,
        "utf8": utf8,
    }

with zipfile.ZipFile(JAR) as z:
    names = z.namelist()
    metadata = z.read("META-INF/neoforge.mods.toml").decode("utf-8", "replace")
    print("=== MOD METADATA ===")
    for line in metadata.splitlines():
        if line.startswith(("modId=", "version=", "displayName=")):
            print(line)

    classes = {}
    for n in names:
        if n.endswith(".class") and not n.startswith("META-INF/versions/"):
            info = parse_class(z.read(n))
            classes[info["this"]] = info

    own = {k: v for k, v in classes.items() if k and "acolyte" in k.lower()}

    def super_chain(name):
        seen = set()
        cur = name
        out = []
        while cur and cur not in seen:
            seen.add(cur)
            sup = classes.get(cur, {}).get("super")
            if not sup:
                break
            out.append(sup)
            cur = sup
        return out

    abstract_spell_chain = []
    iron_spell_super = []
    for name in sorted(own):
        chain = super_chain(name)
        if any(x == "io/redspace/ironsspellbooks/api/spells/AbstractSpell" for x in chain):
            abstract_spell_chain.append(name)
        if any(x and x.startswith("io/redspace/ironsspellbooks/") and "/spell" in x.lower() for x in chain):
            iron_spell_super.append((name, chain))

    spell_like_classes = sorted(x for x in own if "spell" in x.lower())
    iron_spell_fieldrefs = set()
    iron_spell_methodrefs = set()
    resource_literals = set()
    suspicious_markers = set()

    for info in own.values():
        for owner, field, desc in info["fieldrefs"]:
            if owner and owner.startswith("io/redspace/ironsspellbooks/") and "spell" in owner.lower():
                iron_spell_fieldrefs.add((owner, field, desc))
        for owner, method, desc in info["methodrefs"]:
            if owner and owner.startswith("io/redspace/ironsspellbooks/") and "spell" in owner.lower():
                iron_spell_methodrefs.add((owner, method, desc))
        for s in info["utf8"]:
            if re.fullmatch(r"[a-z0-9_.-]+:[a-z0-9_./-]+", s):
                if s.startswith(("irons_spellbooks:", "acolyte:")):
                    resource_literals.add(s)
            if any(token in s for token in ("SPELL_REGISTRY_KEY", "DeferredRegister", "registerSpell", "AbstractSpell")):
                suspicious_markers.add(s)

    lang_keys = []
    for n in names:
        if n.startswith("assets/acolyte/lang/") and n.endswith(".json"):
            obj = json.loads(z.read(n))
            lang_keys.extend(k for k in obj if "spell" in k.lower())

    spell_resources = sorted(
        n for n in names
        if n.startswith(("assets/acolyte/", "data/acolyte/"))
        and any(token in n.lower() for token in ("/spell", "spell_", "/school", "/ritual", "/rite"))
    )

    text_locations = set()
    host_reference_files = {}
    for n in names:
        if n.startswith(("assets/acolyte/", "data/acolyte/")) and n.endswith((".json", ".toml", ".txt", ".mcmeta")):
            try:
                txt = z.read(n).decode("utf-8")
            except Exception:
                continue
            refs = sorted(set(re.findall(r"\b(?:irons_spellbooks|acolyte):[a-z0-9_./-]+\b", txt)))
            text_locations.update(refs)
            iron_refs = [x for x in refs if x.startswith("irons_spellbooks:")]
            if iron_refs:
                host_reference_files[n] = iron_refs

    print("=== STRUCTURAL SUMMARY ===")
    print("TOTAL_CLASSES", len(classes))
    print("PROVIDER_CLASSES", len(own))
    print("SPELL_LIKE_PROVIDER_CLASSES", json.dumps(spell_like_classes))
    print("ABSTRACTSPELL_CHAIN_CLASSES", json.dumps(sorted(abstract_spell_chain)))
    print("IRON_SPELL_SUPER_CLASSES", json.dumps(iron_spell_super))
    print("OWN_SPELL_LANG_KEYS", json.dumps(sorted(set(lang_keys))))
    print("OWN_SPELL_RESOURCE_PATHS", json.dumps(spell_resources))
    print("IRON_SPELL_FIELDREFS", json.dumps(sorted(iron_spell_fieldrefs)))
    print("IRON_SPELL_METHODREFS", json.dumps(sorted(iron_spell_methodrefs)))
    print("RESOURCE_LOCATION_LITERALS", json.dumps(sorted(resource_literals)))
    print("TEXT_RESOURCE_LOCATIONS", json.dumps(sorted(text_locations)))
    print("HOST_REFERENCE_FILES", json.dumps(host_reference_files, sort_keys=True))
    print("SPELL_REGISTRY_FIELDREFS", json.dumps(sorted(
        row for row in iron_spell_fieldrefs
        if row[0] and row[0].endswith("/SpellRegistry")
    )))
    print("SPELL_REGISTRATION_MARKERS", json.dumps(sorted(suspicious_markers)))
