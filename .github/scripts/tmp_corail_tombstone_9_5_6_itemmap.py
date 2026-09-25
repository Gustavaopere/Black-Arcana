#!/usr/bin/env python3
import hashlib
import re
import subprocess
import tempfile
import urllib.request
import zipfile
from pathlib import Path

URL="https://www.cursemaven.com/curse/maven/corail-tombstone-243707/8842741/corail-tombstone-243707-8842741.jar"

def digest(data,name):
    h=hashlib.new(name);h.update(data);return h.hexdigest()

def main():
    with tempfile.TemporaryDirectory(prefix="black-arcana-tombstone-items-") as tmp:
        jar=Path(tmp)/"tombstone.jar"
        req=urllib.request.Request(URL,headers={"User-Agent":"Black-Arcana-catalog-audit/1"})
        with urllib.request.urlopen(req,timeout=120) as r:
            blob=r.read()
        jar.write_bytes(blob)
        print(f"TOMBSTONE_ITEMMAP_SHA1={digest(blob,'sha1')}")
        with zipfile.ZipFile(jar) as zf:
            classes=[]
            for n in zf.namelist():
                if not n.startswith("ovh/corail/tombstone/item/") or not n.endswith(".class"):
                    continue
                base=n.rsplit("/",1)[1]
                if "$" in base:
                    continue
                classes.append(n[:-6].replace("/","."))
        for cls in sorted(classes):
            p=subprocess.run(["javap","-classpath",str(jar),"-p",cls],text=True,capture_output=True,timeout=60)
            if p.returncode!=0:
                continue
            out=[x.strip() for x in p.stdout.splitlines() if x.strip() and not x.startswith("Compiled from")]
            if not out:
                continue
            decl=next((x for x in out if (" class " in x or " interface " in x or " enum " in x)),out[0])
            action=[x for x in out if re.search(r"\b(use|doEffects|getCastingType|useOn|finishUsingItem|onUseTick|releaseUsing|interactLivingEntity|appendHoverText)\s*\(",x)]
            if action or any(x in decl for x in ("ItemCastableMagic","ItemGraveMagic","ItemScroll","ItemTablet","ItemBook")):
                print(f"TOMBSTONE_ITEM_CLASS={cls}|{decl}")
                for sig in action:
                    print(f"TOMBSTONE_ITEM_ACTION_SIG={cls}|{sig}")
        print("TOMBSTONE_ITEMMAP_COMPLETE=true")

if __name__=="__main__":
    main()
