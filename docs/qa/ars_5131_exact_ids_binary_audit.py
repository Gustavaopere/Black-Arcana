#!/usr/bin/env python3
"""Clean-room SHA-gated static Ars Nouveau 5.13.1 class-to-ID bytecode audit.

No claim of loaded registry, cast execution, costs or Survival acceptance.
"""
import argparse
import json
from pathlib import Path
import re
import subprocess

import ars_5131_static_registry_audit as prior

HERE=Path(__file__).resolve().parent
GLYPH_LIB="com.hollingsworth.arsnouveau.common.lib.GlyphLib"
RITUAL_LIB="com.hollingsworth.arsnouveau.common.lib.RitualLib"
PREFIX_OWNER="com.hollingsworth.arsnouveau.ArsNouveau"

class AuditError(ValueError):
    pass

def manifests(glyphs=None,rituals=None,readme=None):
    g=json.loads(Path(glyphs or HERE/"ars_5131_glyph_class_id_manifest.json").read_text(encoding="utf8"))
    r=json.loads(Path(rituals or HERE/"ars_5131_ritual_class_id_manifest.json").read_text(encoding="utf8"))
    if not isinstance(g,dict) or not isinstance(r,dict):
        raise AuditError("manifests must be object maps")
    if set(g)!=set(prior.SPELL_CLASSES) or set(r)!=set(prior.RITUAL_CLASSES):
        raise AuditError("manifest does not match previously proven 85+24 class owners")
    if len(g)!=85 or len(r)!=24 or len(set(g.values()))!=85 or len(set(r.values()))!=24:
        raise AuditError("manifest cardinality/unique ID invariant failed")
    if any(not isinstance(v,str) or not re.fullmatch(r"ars_nouveau:[a-z0-9_]+",v)
           for v in [*g.values(),*r.values()]):
        raise AuditError("unqualified ResourceLocation in manifest")
    if any(not (v.startswith("ars_nouveau:glyph_") or
                v in ("ars_nouveau:reset","ars_nouveau:rewind","ars_nouveau:wololo"))
           for v in g.values()):
        raise AuditError("invalid glyph identity family")
    if any(not v.startswith("ars_nouveau:ritual_") for v in r.values()):
        raise AuditError("invalid ritual identity family")
    doc=Path(readme or HERE.parent.parent/"wiki/modpack-catalog/providers/✅-ars-nouveau/README.md").read_text(encoding="utf8")
    documented=set(re.findall(r"(?m)^\|[^\n]+\|\s*\x60(ars_nouveau:[a-z0-9_]+)\x60\s*\|",doc))
    if len(documented)!=85 or documented!=set(g.values()):
        raise AuditError("glyph ID manifest differs from independent catalog README")
    return g,r

def javap(jar,owner,verbose=False):
    cmd=["javap","-c","-p"]
    if verbose: cmd.append("-v")
    cmd+=["-classpath",str(jar.resolve()),owner]
    try:
        p=subprocess.run(cmd,capture_output=True,text=True,check=False,timeout=60)
    except (OSError,subprocess.TimeoutExpired) as e:
        raise AuditError("javap failed "+owner) from e
    if p.returncode or not 0<len(p.stdout)<4500000:
        raise AuditError("compiled class missing/oversize "+owner)
    return p.stdout

def method(text,header):
    m=re.search(header,text,re.M)
    if not m: raise AuditError("method missing "+header)
    rest=text[m.end():]
    c=re.search(r"^\s+Code:\s*$",rest,re.M)
    if not c: raise AuditError("method bytecode missing")
    output=[]
    for line in rest[c.end():].splitlines():
        x=re.match(r"^\s*(\d+):\s+([a-z][a-z0-9_]*)(.*)$",line)
        if x:
            raw=x.group(3)
            output.append((x.group(2),raw.split("//",1)[1].strip() if "//" in raw else ""))
        elif output and not line.strip():
            break
    if not output: raise AuditError("empty instruction list")
    return output

def libfields(text,prefix):
    ins=method(text,r"^\s+static \{\};\s*$")
    out={}
    for i,(op,c) in enumerate(ins):
        if op!="putstatic": continue
        m=re.search(r"\bField\s+([A-Za-z][A-Za-z0-9_]*):Ljava/lang/String;",c)
        if not m: continue
        if i<2 or ins[i-2][0] not in ("ldc","ldc_w") or not ins[i-2][1].startswith("String ") or ins[i-1][0]!="invokestatic" or "prepend"+prefix+":" not in ins[i-1][1]:
            raise AuditError("unresolved library literal "+m.group(1))
        suffix=ins[i-2][1][7:]
        if not re.fullmatch(r"[a-z][a-z0-9_]*",suffix) or m.group(1) in out:
            raise AuditError("invalid/duplicate library constant")
        out[m.group(1)]=prefix.lower()+"_"+suffix
    if len(out)<24: raise AuditError("incomplete compiled library")
    return out

def check_prepend(text,method_name,recipe):
    ins=method(text,r"^\s+public static java\.lang\.String "+re.escape(method_name)+r"\(java\.lang\.String\);$")
    if [op for op,_ in ins]!=["aload_0","invokedynamic","areturn"]:
        raise AuditError("unexpected "+method_name+" implementation")
    if recipe+r"\u0001" not in text and recipe+"\x01" not in text:
        raise AuditError(method_name+" bootstrap concat recipe mismatch")

def check_namespace(text):
    ins=method(text,r"^\s+public static net\.minecraft\.resources\.ResourceLocation prefix\(java\.lang\.String\);$")
    if len(ins)!=4 or ins[0]!=("ldc","String ars_nouveau") or ins[1][0]!="aload_0" or ins[2][0]!="invokestatic" or "ResourceLocation.fromNamespaceAndPath:" not in ins[2][1] or ins[3][0]!="areturn":
        raise AuditError("physical namespace method differs from ars_nouveau")

def spell_owner(name):
    folder="method" if name.startswith("Method") else "augment" if name.startswith("Augment") else "effect"
    return "com.hollingsworth.arsnouveau.common.spell."+folder+"."+name

def glyph_id(dis,name,fields):
    if name=="EffectSenseMagic":
        ins=method(dis,r"^\s+static \{\};\s*$")
    else:
        ins=method(dis,r"^\s+(?:public|protected|private)\s+[^\n;]*\b"+re.escape(name)+r"\(\);$")
    refs=[]
    for i,(op,c) in enumerate(ins):
        m=re.search(r"\bGlyphLib\.([A-Za-z0-9_]+):Ljava/lang/String;",c)
        if op=="getstatic" and m:
            refs.append((i,m.group(1)))
    if name in ("EffectReset","EffectRewind","EffectWololo"):
        if refs: raise AuditError("special glyph carries unexpected field "+name)
        val={"EffectReset":"reset","EffectRewind":"rewind","EffectWololo":"wololo"}[name]
        indices=[i for i,(op,c) in enumerate(ins) if op in ("ldc","ldc_w") and c=="String "+val]
        if len(indices)!=1: raise AuditError("special literal missing "+name)
        pos=indices[0];path=val
    else:
        if len(refs)!=1: raise AuditError(name+" must have one compiled GlyphLib producer")
        pos,key=refs[0]
        if key not in fields: raise AuditError(name+" unknown compiled glyph constant "+key)
        path=fields[key]
    window=ins[pos+1:pos+5]
    if name=="EffectSenseMagic":
        # Same-class constructor bytecode abbreviates owner to Method "<init>".
        # Require the exact static new/dup/field/name/ctor/INSTANCE chain.
        if (pos<2 or len(ins)<pos+4 or
            [x[0] for x in ins[pos-2:pos+4]]!=
            ["new","dup","getstatic","ldc","invokespecial","putstatic"] or
            "EffectSenseMagic" not in ins[pos-2][1] or
            ins[pos+1][1]!="String Sense Magic" or
            '"<init>":(Ljava/lang/String;Ljava/lang/String;)V' not in ins[pos+2][1] or
            "Field INSTANCE:" not in ins[pos+3][1]):
            raise AuditError(name+" no exact static initializer constructor chain")
    elif not any(op=="invokespecial" and '"<init>":' in c and "Abstract" in c
                 for op,c in window):
        raise AuditError(name+" literal not causally tied to constructor")
    if any(op.startswith(("if","goto","jsr")) for op,_ in ins):
        raise AuditError(name+" identity path has branch")
    return "ars_nouveau:"+path

def ritual_id(dis,name,fields):
    ins=method(dis,r"^\s+public net\.minecraft\.resources\.ResourceLocation getRegistryName\(\);$")
    if len(ins)!=3 or ins[0][0]!="getstatic" or ins[1][0]!="invokestatic" or ins[2][0]!="areturn":
        raise AuditError(name+" registry getter not direct")
    m=re.search(r"\bRitualLib\.([A-Za-z0-9_]+):Ljava/lang/String;",ins[0][1])
    if not m or m.group(1) not in fields or "ArsNouveau.prefix:" not in ins[1][1]:
        raise AuditError(name+" registry ID cannot be resolved")
    return "ars_nouveau:"+fields[m.group(1)]

def reconcile(expected,actual,label):
    if set(expected)!=set(actual) or len(set(actual.values()))!=len(actual):
        raise AuditError(label+" owner uniqueness/coverage mismatch")
    errors={name:{"expected":v,"observed":actual.get(name)}
            for name,v in expected.items() if actual.get(name)!=v}
    if errors: raise AuditError(label+" source-vs-binary ID mismatch "+json.dumps(errors,sort_keys=True))

def audit(jar):
    g,r=manifests()
    base=prior.audit(jar)
    if base["status"]!="PASS" or base["count_spell_parts"]!=85 or base["count_rituals"]!=24:
        raise AuditError("prior independent callsite verification not valid")
    gl=javap(jar,GLYPH_LIB,True)
    rl=javap(jar,RITUAL_LIB,True)
    check_prepend(gl,"prependGlyph","glyph_")
    check_prepend(rl,"prependRitual","ritual_")
    check_namespace(javap(jar,PREFIX_OWNER))
    gf=libfields(gl,"Glyph")
    rf=libfields(rl,"Ritual")
    compiled_g={name:glyph_id(javap(jar,spell_owner(name)),name,gf) for name in prior.SPELL_CLASSES}
    compiled_r={name:ritual_id(javap(jar,"com.hollingsworth.arsnouveau.common.ritual."+name),name,rf) for name in prior.RITUAL_CLASSES}
    reconcile(g,compiled_g,"glyph")
    reconcile(r,compiled_r,"ritual")
    if set(compiled_g.values())&set(compiled_r.values()):
        raise AuditError("duplicate glyph/ritual ResourceLocation")
    return {"status":"PASS","evidence_class":"SHA_MATCHED_COMPILED_109_RESOURCELOCATION_CLASS_IDS_NOT_RUNTIME",
            "filename":prior.FILENAME,"mod_id":"ars_nouveau","version":"5.13.1",
            "physical_sha1":base["physical_sha1"],"publisher_sha256":base["publisher_sha256"],
            "size_bytes":base["bytes"],"glyphs":dict(sorted(compiled_g.items())),
            "rituals":dict(sorted(compiled_r.items())),"glyph_count":85,"ritual_count":24,
            "semantic_roots_added":0,
            "not_proven":["loaded registry","effective config/glyph access","mana/Source payment",
                          "casting/effects/ritual gameplay","real modpack/Survival",
                          "cross-provider adapter"]}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--jar",type=Path,required=True)
    p.add_argument("--output",type=Path)
    a=p.parse_args()
    try: out=audit(a.jar);code=0
    except (AuditError,prior.AuditError,OSError,ValueError,KeyError) as e:
        out={"status":"FAIL_CLOSED","reason":str(e)};code=1
    payload=json.dumps(out,indent=2,ensure_ascii=False,sort_keys=True)+"\n"
    if a.output:
        a.output.parent.mkdir(parents=True,exist_ok=True)
        a.output.write_text(payload,encoding="utf8")
    print(payload)
    return code

if __name__=="__main__":
    raise SystemExit(main())
