#!/usr/bin/env python3
import hashlib
import re
import subprocess
import tempfile
import urllib.request
import zipfile
from pathlib import Path

URL="https://www.cursemaven.com/curse/maven/corail-tombstone-243707/8842741/corail-tombstone-243707-8842741.jar"

TOKENS=[
 "pray_of_dissonance","pray_of_empathy","pray_of_harmonization","pray_of_protection",
 "pray_of_undead","prayer_of_empathy","prayer_of_undead","pray_on_grave",
 "rite_of_coral_chant","rite_of_remanence","rite_of_silent_bond","coral_chant",
 "enhanced_grave_prayer","elyra_diary","erdos_fragments","nights_of_nour",
 "gemstone_of_familiar","gemstone_of_guardian","gemstone_of_merchant","gemstone_of_prayer",
 "tablet_of_assistance","tablet_of_cupidity","tablet_of_guard","tablet_of_home","tablet_of_recall",
 "lost_tablet","magic_scroll","scroll_of_knowledge"
]

JAVAP=[
 "ovh.corail.tombstone.config.ConfigTombstone$MagicItem",
 "ovh.corail.tombstone.config.SharedConfigTombstone$AllowedMagicItems",
 "ovh.corail.tombstone.config.SharedConfigTombstone$MagicItem",
 "ovh.corail.tombstone.item.ItemAnkhOfPrayer",
 "ovh.corail.tombstone.item.ItemGemstoneOfPrayer",
 "ovh.corail.tombstone.item.ItemRitualFlute",
 "ovh.corail.tombstone.helper.PrayerHelper",
]

def digest(data,name):
    h=hashlib.new(name);h.update(data);return h.hexdigest()

def printable(data):
    for raw in re.findall(rb"[ -~]{4,240}",data):
        try: yield raw.decode("ascii")
        except UnicodeDecodeError: pass

def main():
  with tempfile.TemporaryDirectory(prefix="ba-tombstone-map-") as tmp:
    jar=Path(tmp)/"tombstone.jar"
    req=urllib.request.Request(URL,headers={"User-Agent":"Black-Arcana-catalog-audit/1"})
    with urllib.request.urlopen(req,timeout=120) as r:
      blob=r.read()
    jar.write_bytes(blob)
    print(f"TOMBSTONE_MAP_SHA1={digest(blob,'sha1')}")
    with zipfile.ZipFile(jar) as zf:
      classes=[n for n in zf.namelist() if n.startswith("ovh/corail/tombstone/") and n.endswith(".class")]
      for token in TOKENS:
        hits=[]
        tb=token.encode()
        for name in classes:
          data=zf.read(name).lower()
          if tb in data:
            hits.append(name)
        print(f"TOMBSTONE_TOKEN_CLASS_COUNT={token}|{len(hits)}")
        for name in sorted(hits):
          print(f"TOMBSTONE_TOKEN_CLASS={token}|{name}")

      for name in classes:
        low=zf.read(name).lower()
        matched=[]
        for token in TOKENS:
          if token.encode() in low:
            matched.append(token)
        if matched:
          cls=name[:-6].replace("/",".")
          strings=sorted({s for s in printable(zf.read(name)) if any(t in s.lower() for t in matched)})
          for s in strings:
            if len(s) <= 220:
              print(f"TOMBSTONE_CLASS_TOKEN_STRING={cls}|{s}")

    for target in JAVAP:
      p=subprocess.run(["javap","-classpath",str(jar),"-p","-constants",target],text=True,capture_output=True,timeout=60)
      print(f"TOMBSTONE_MAP_JAVAP_BEGIN={target}")
      if p.returncode!=0:
        print(f"TOMBSTONE_MAP_JAVAP_ERROR={target}|{p.stderr.strip()}")
      else:
        for line in p.stdout.splitlines():
          line=line.strip()
          if not line or line.startswith("Compiled from"): continue
          print(f"TOMBSTONE_MAP_JAVAP={target}|{line}")
      print(f"TOMBSTONE_MAP_JAVAP_END={target}")

    print("TOMBSTONE_ACTIONMAP_COMPLETE=true")

if __name__=="__main__":
  main()
