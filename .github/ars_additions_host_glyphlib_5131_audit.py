"""Clean-room fingerprint+symbolic Ars Nouveau 5.13.1 glyph normalization audit.

No provider bytecode/text implementation is emitted. Resolves only method
shape, host StringConcatFactory recipe and verified addon path construction.
"""
from pathlib import Path
import hashlib, os, re, subprocess

HOST=Path(os.environ["HOST_JAR"])
ADDON=Path(os.environ["ADDON_JAR"])
expect={
    HOST:"02782d071ee5fab3b5c4b8ced67b7e1748277dfd",
    ADDON:"ce2440b606acb20b79a42bf7c6c24d163c93241f",
}
for path,sha in expect.items():
    assert path.is_file()
    assert hashlib.sha1(path.read_bytes()).hexdigest()==sha, "physical SHA1 differs - FAIL CLOSED"
    print(f"EXACT_SHA1={path.name}|{sha}|{path.stat().st_size}")

def javap(jar, cls, verbose=False):
    cmd=["javap","-classpath",str(jar),"-p","-c"]
    if verbose:cmd+=["-v"]
    cmd.append(cls)
    p=subprocess.run(cmd,capture_output=True,text=True,check=True)
    return p.stdout

def section(raw, signature):
    lines=raw.splitlines()
    hits=[i for i,s in enumerate(lines) if s.strip().endswith(signature)]
    assert len(hits)==1,(signature,len(hits))
    a=hits[0];b=len(lines)
    for i in range(a+1,len(lines)):
        if lines[i]=="}" or re.match(r"^  (?:public|private|protected|static)\s",lines[i]):
            b=i;break
    return "\n".join(lines[a:b])

host=javap(HOST,"com.hollingsworth.arsnouveau.common.lib.GlyphLib",verbose=True)
normalizer=section(host,"java.lang.String prependGlyph(java.lang.String);")
assert "java.lang.String prependGlyph" in normalizer
assert not re.search(r"^\s*\d+:\s+(?:if\w*|goto(?:_w)?|tableswitch|lookupswitch)\b",normalizer,re.M), "branch in host normalizer"
assert "invokedynamic" in normalizer and "makeConcatWithConstants" in normalizer, "concat method requires separate audit"
# StringConcatFactory bootstrap literal glyph_ + parameter marker, rendered by javap
assert re.search(r"glyph_(?:\\u0001|\x01|\\u0001|\u0001)",host), "host prefix concat template not proven"
# exactly one operand plus exactly one return
assert len(re.findall(r"^\s*\d+:\s+areturn\b",normalizer,re.M))==1
addon_names=javap(ADDON,"com.github.jarva.arsadditions.setup.registry.names.AddonGlyphNames")
clinit=section(addon_names,"static {};")
assert len(re.findall(r"GlyphLib\.prependGlyph",clinit))==3
for name,path in [("MethodRetaliate","retaliate"),("EffectMark","mark"),("MethodRecall","recall")]:
    pat=(r"// String "+path+r"\s*\n"
         r"\s*\d+:\s+invokestatic\s+[^\n]*GlyphLib\.prependGlyph[^\n]*\n"
         r"\s*\d+:\s+putstatic\s+[^\n]*"+name+r":")
    assert re.search(pat,clinit),name
    glyph=javap(ADDON,"com.github.jarva.arsadditions.common.glyph."+name)
    ctor=section(glyph,name+"();")
    assert "AddonGlyphNames."+name in ctor and "ArsAdditions.prefix" in ctor, name
    print("RESOLVED_GLYPH_ID=ars_additions:glyph_"+path)
main=javap(ADDON,"com.github.jarva.arsadditions.ArsAdditions")
prefix=section(main,"net.minecraft.resources.ResourceLocation prefix(java.lang.String);")
assert "ars_additions" in prefix and "fromNamespaceAndPath" in prefix
print("ARS_PREFIX_NAMESPACE=ars_additions")
print("HOST_GLIPHLIB_PREFIX=glyph_")
print("HOST_NORMALIZER_BRANCH_COUNT=0")
print("BINARIES_EXACT_AND_THREE_GLYPH_IDS=PASS")
print("LIMIT=static registration and identity only; no live host, config, acquisition or Survival test")
