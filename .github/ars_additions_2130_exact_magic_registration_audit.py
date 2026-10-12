"""Isolated clean-room evidence from the exact installed Ars Additions JAR.

Summarize *only* Java method call counts / symbolic class names / static
registry entry counts, no bytecode, recipe payload, classes or assets in logs.
Uses javap locally in the GitHub Actions runner without decompiling source.
"""
import hashlib
import os
import re
import subprocess
from pathlib import Path

jar = Path(os.environ["JAR_PATH"])
sha = "ce2440b606acb20b79a42bf7c6c24d163c93241f"
assert hashlib.sha1(jar.read_bytes()).hexdigest() == sha, "physical SHA1 mismatch"
assert jar.stat().st_size > 0
prefix = "com.github.jarva.arsadditions"
def javap(cls):
    p = subprocess.run(["javap","-classpath",str(jar),"-p","-c",cls],
                       capture_output=True,text=True,check=True)
    return p.stdout

def section(out, signature):
    ls=out.splitlines()
    matches=[i for i,s in enumerate(ls) if s.strip().endswith(signature)]
    assert len(matches)==1,(signature,len(matches))
    start=matches[0]
    stop=len(ls)
    for i in range(start+1,len(ls)):
        s=ls[i]
        if re.match(r"^  (?:public|private|protected|static)\s",s):
            stop=i
            break
        if s=="}":
            stop=i
            break
    return "\n".join(ls[start:stop])

registry=javap(prefix+".setup.registry.ArsNouveauRegistry")
app=javap(prefix+".ArsAdditions")
init=section(registry,"void init();")
glyph=section(registry,"void registerGlyphs();")
ritual=section(registry,"void registerRituals();")
perks=section(registry,"void registerPerks();")
# Only symbolic classes extracted; no third-party implementation emitted.
expected_glyphs=["MethodRetaliate","EffectMark","MethodRecall"]
expected_rituals=["RitualChunkLoading","RitualLocateStructure"]
expected_perks=["ReachPerk"]
branch=re.compile(r"^\s*\d+:\s+(?:if\w*|goto(?:_w)?|tableswitch|lookupswitch)\b", re.M)
def verify_no_branch(s,label):
    assert not branch.search(s), f"Unexpected branch in {label}: fail-closed"
for k,s in [("init",init),("registerGlyphs",glyph),
             ("registerRituals",ritual),("registerPerks",perks)]:
    verify_no_branch(s,k)
for method in ["registerGlyphs", "registerRituals", "registerPerks"]:
    assert len(re.findall(r"// Method (?:(?:\S+/)?)"+method+r":\(\)V",init))==1,method
for k,code,expected,kind in [
   ("GLYPH",glyph,expected_glyphs,"AbstractSpellPart"),
   ("RITUAL",ritual,expected_rituals,"AbstractRitual"),
   ("PERK",perks,expected_perks,"IPerk")]:
    names=[]
    for name in expected:
        # Java compiler references class for INSTANCE or new + constructor.
        if k=="RITUAL":
            evidence=re.findall(r"// class \S*/"+name+r"\b",code)
        else:
            evidence=re.findall(r"// Field \S*/"+name+r"\.INSTANCE:",code)
        assert len(evidence)==1, f"{k}: missing or repeated {name} ({len(evidence)})"
        names.append(name)
    wrapper_count=len(re.findall(
        r"// Method register:\(Lcom/hollingsworth/arsnouveau/api/"
        +(r"ritual/" if k=="RITUAL" else r"spell/" if k=="GLYPH" else r"perk/")
        +kind+r";\)V",code))
    # Different javap output may elide internal package from Method refs.
    assert wrapper_count==len(expected),(k,wrapper_count,len(expected))
    assert len(names)==len(expected)
    print(f"{k}_REGISTRATION_COUNT={len(names)}")
    for name in names:
        print(f"{k}_REGISTRATION_CLASS="+prefix+"."+("common.ritual." if k=="RITUAL" else "common.glyph." if k=="GLYPH" else "common.perk.")+name)
assert len(re.findall(r"// Method com/github/jarva/arsadditions/setup/registry/ArsNouveauRegistry\.init:\(\)V",app))==1, "mod ctor missing init reference"
print("BOOTSTRAP_ARS_NOUVEAU_REGISTRY_INIT_REFERENCES=1")
print("REGISTRATION_HELPER_BRANCHES=0")
print("PHYSICAL_SHA1="+sha)
print("EXACT_JAR_BYTES="+str(jar.stat().st_size))
print("CLEAN_ROOM_SYMBOLIC_REGISTRATION_AUDIT=SUCCESS")
