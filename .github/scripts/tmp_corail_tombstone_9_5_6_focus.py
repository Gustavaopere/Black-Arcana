#!/usr/bin/env python3
import hashlib
import subprocess
import tempfile
import urllib.request
from pathlib import Path

URL = "https://www.cursemaven.com/curse/maven/corail-tombstone-243707/8842741/corail-tombstone-243707-8842741.jar"
TARGETS = [
    "ovh.corail.tombstone.item.ItemScrollBuff$SpellBuff",
    "ovh.corail.tombstone.item.ItemLostTablet$Type",
    "ovh.corail.tombstone.item.ItemReadableScroll$ReadableScrollType",
    "ovh.corail.tombstone.item.ItemRitualFlute$NoteStep",
    "ovh.corail.tombstone.item.ItemCastableMagic",
    "ovh.corail.tombstone.item.ItemTablet",
    "ovh.corail.tombstone.item.ItemTabletOfAssistance",
    "ovh.corail.tombstone.item.ItemTabletOfCupidity",
    "ovh.corail.tombstone.item.ItemTabletOfGuard",
    "ovh.corail.tombstone.item.ItemTabletOfHome",
    "ovh.corail.tombstone.item.ItemTabletOfRecall",
    "ovh.corail.tombstone.item.ItemScrollBuff",
    "ovh.corail.tombstone.item.ItemAnkhOfPrayer",
    "ovh.corail.tombstone.item.ItemGemstoneOfPrayer",
    "ovh.corail.tombstone.item.ItemBookOfMagicImpregnation",
    "ovh.corail.tombstone.helper.PrayerHelper",
    "ovh.corail.tombstone.registry.ModItems",
    "ovh.corail.tombstone.registry.ModPerks",
    "ovh.corail.tombstone.registry.ModStats",
]

def digest(data, name):
    h=hashlib.new(name); h.update(data); return h.hexdigest()

def main():
    with tempfile.TemporaryDirectory(prefix="black-arcana-tombstone-focus-") as tmp:
        jar=Path(tmp)/"tombstone.jar"
        req=urllib.request.Request(URL,headers={"User-Agent":"Black-Arcana-catalog-audit/1"})
        with urllib.request.urlopen(req,timeout=120) as r:
            blob=r.read()
        jar.write_bytes(blob)
        print(f"TOMBSTONE_FOCUS_SHA1={digest(blob,'sha1')}")
        print(f"TOMBSTONE_FOCUS_SHA256={digest(blob,'sha256')}")
        for target in TARGETS:
            print(f"TOMBSTONE_JAVAP_BEGIN={target}")
            p=subprocess.run(
                ["javap","-classpath",str(jar),"-p","-constants",target],
                text=True,capture_output=True,timeout=60
            )
            if p.returncode != 0:
                print(f"TOMBSTONE_JAVAP_ERROR={target}|{p.stderr.strip()}")
                continue
            for line in p.stdout.splitlines():
                line=line.strip()
                if not line or line.startswith("Compiled from"):
                    continue
                print(f"TOMBSTONE_JAVAP={target}|{line}")
            print(f"TOMBSTONE_JAVAP_END={target}")
        print("TOMBSTONE_FOCUSED_AUDIT_COMPLETE=true")

if __name__=="__main__":
    main()
