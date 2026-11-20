#!/usr/bin/env python3
"""Read-only exact supplier-holder and default instance constructor boundary."""
import argparse
import json
from pathlib import Path
import zipfile

from alexscaves_1010_armor_material_audit import ClassReader, canonical, digest, require, verify_artifact
from alexscaves_1010_enchantable_item_probe import disassemble, summarize
from alexscaves_1010_enchantable_item_boundary import download, CLIENT_SHA1
from minecraft_1211_mojang_mixin_target_mappings import CLASS, official_version_downloads

OWNER = "com/github/alexmodguy/alexscaves/server/misc/ACCompat"
KEY = ("effect", "(Lnet/minecraft/world/effect/MobEffect;)Lnet/minecraft/core/Holder;")
EFFECT = "net.minecraft.world.effect.MobEffectInstance"


def native(jar, javap):
    verify_artifact(jar)
    with zipfile.ZipFile(jar) as z:
        raw = z.read(OWNER + ".class")
        rd = ClassReader(raw)
        parsed = disassemble(jar, javap, OWNER)
        require(KEY in parsed, "holder adapter absent")
        return {"class_sha256": digest(raw), "method": summarize(rd, KEY, parsed[KEY])}


def vanilla(tmp, javap):
    info = official_version_downloads()["downloads"]
    require(info["client"]["sha1"] == CLIENT_SHA1, "client version drift")
    jar, maps = tmp / "client.jar", tmp / "client.txt"
    c = download(jar, info["client"], 35000000)
    m = download(maps, info["client_mappings"], 15000000)
    require(c["sha256"] == "499f6897d1837516680f3114072d8106e11c9adcd933fe5cf051b551089b0c99", "client drift")
    require(m["sha256"] == "140c47931cccc8fc9e4c22d7603e2d714d1a953a146f51ea7397d95c955536ec", "mappings drift")
    names = dict(line[:-1].split(" -> ") for line in maps.read_text(encoding="utf8").splitlines() if CLASS.fullmatch(line))
    owner = names[EFFECT].replace(".", "/")
    holder = names["net.minecraft.core.Holder"].replace(".", "/")
    with zipfile.ZipFile(jar) as z:
        raw = z.read(owner + ".class")
        rd = ClassReader(raw)
        parsed = disassemble(jar, javap, owner)
        key = ("<init>", "(L" + holder + ";I)V")
        require(key in parsed, "default effect constructor absent")
        methods = [summarize(rd, k, b) for k, b in sorted(parsed.items()) if k[0] == "<init>"]
        return {"client": c, "mappings": m, "owner": owner, "holder": holder,
                "class_sha256": digest(raw), "constructors": methods}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for n in ("jar", "javap", "output"):
        p.add_argument("--" + n, type=Path, required=True)
    a = p.parse_args()
    require(not a.output.exists(), "new output required")
    tmp = a.output.parent / "effect-reference"
    tmp.mkdir()
    result = {"scope": "STATIC_REFERENCE_ONLY", "native": native(a.jar, a.javap),
              "vanilla": vanilla(tmp, a.javap), "mutation": "NO_MUTATION",
              "physical_qa": "NOT_TESTED", "mutating_hook": "NOT_VERIFIED"}
    a.output.write_text(canonical(result), encoding="utf8")
    print("BOUNDARY_SHA256", digest(a.output.read_bytes()))
    print("NATIVE_BOUNDARY", json.dumps(result["native"], sort_keys=True))
    print("VANILLA_BOUNDARY", json.dumps(result["vanilla"], sort_keys=True))


if __name__ == "__main__":
    main()
