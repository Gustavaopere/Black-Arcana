#!/usr/bin/env python3
import hashlib, json, re, tempfile, urllib.request, zipfile
from pathlib import Path

URL="https://www.cursemaven.com/curse/maven/corail-tombstone-243707/8842741/corail-tombstone-243707-8842741.jar"
TOKENS=[
 "ankh_of_prayer","ritual_flute","readable_scroll","elyra_diary","coral_chant",
 "erdos_fragments","rite_of_silent_bond","nights_of_nour",
 "pray_of_dissonance","pray_of_empathy","pray_of_harmonization","pray_of_protection","pray_of_undead"
]
CONFIG_TERMS=["ankh","ritual_flute","prayer","pray","rite","coral_chant","remanence","silent_bond"]

def sha(data,n): h=hashlib.new(n);h.update(data);return h.hexdigest()

def main():
  with tempfile.TemporaryDirectory(prefix="ba-tombstone-reach-") as tmp:
    jar=Path(tmp)/"tombstone.jar"
    req=urllib.request.Request(URL,headers={"User-Agent":"Black-Arcana-catalog-audit/1"})
    with urllib.request.urlopen(req,timeout=120) as r: blob=r.read()
    jar.write_bytes(blob)
    print(f"TOMBSTONE_REACH_SHA1={sha(blob,'sha1')}")
    with zipfile.ZipFile(jar) as zf:
      structured=[n for n in zf.namelist() if n.startswith("data/tombstone/") and (n.endswith(".json") or n.endswith(".mcmeta"))]
      for tok in TOKENS:
        hits=[]
        b=tok.encode()
        for n in structured:
          try: data=zf.read(n).lower()
          except: continue
          if b in data:
            hits.append(n)
        print(f"TOMBSTONE_STRUCTURED_REF_COUNT={tok}|{len(hits)}")
        for n in sorted(hits):
          print(f"TOMBSTONE_STRUCTURED_REF={tok}|{n}")

      cfg_classes=[n for n in zf.namelist() if n.startswith("ovh/corail/tombstone/config/") and n.endswith(".class")]
      for term in CONFIG_TERMS:
        hits=[]
        b=term.encode()
        for n in cfg_classes:
          if b in zf.read(n).lower(): hits.append(n)
        print(f"TOMBSTONE_CONFIG_TOKEN_CLASS_COUNT={term}|{len(hits)}")
        for n in sorted(hits):
          print(f"TOMBSTONE_CONFIG_TOKEN_CLASS={term}|{n}")
    print("TOMBSTONE_REACHABILITY_AUDIT_COMPLETE=true")
if __name__=="__main__": main()
