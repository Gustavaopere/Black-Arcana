"""Check symbolic spell/ritual ResourceLocation construction in physical JAR.

Only emits source-style symbolic ID construction; does not execute host APIs,
infer actual runtime configs, or log bytecode/class bodies.
"""
import hashlib
import os
import re
import subprocess
from pathlib import Path
p=Path(os.environ["JAR_PATH"])
sha="ce2440b606acb20b79a42bf7c6c24d163c93241f"
assert hashlib.sha1(p.read_bytes()).hexdigest()==sha
package="com.github.jarva.arsadditions"
def dump(n):
    return subprocess.run(["javap","-p","-c","-classpath",str(p),n],
                          text=True,capture_output=True,check=True).stdout

def body(raw,name):
    lines=raw.splitlines()
    inds=[i for i,l in enumerate(lines) if l.strip().endswith(name)]
    assert len(inds)==1,(name,len(inds))
    st=inds[0]
    end=len(lines)
    for i in range(st+1,len(lines)):
        if lines[i]=="}" or re.match(r"^  (?:public|private|protected|static)\s",lines[i]):
            end=i;break
    return "\n".join(lines[st:end])
names={
  "MethodRetaliate":"retaliate",
  "EffectMark":"mark",
  "MethodRecall":"recall"
}
glyph_names_class=dump(package+".setup.registry.names.AddonGlyphNames")
clinit=body(glyph_names_class,"static {};")
assert len(re.findall(r"GlyphLib\.prependGlyph",clinit))==3
for cls,path in names.items():
    # The static path literal is fed into GlyphLib.prependGlyph then stored
    # in AddonGlyphNames.<class>; concrete class passes it to prefix.
    pattern=(r"// String "+path+r"\s*\n"
             r"\s*\d+:\s+invokestatic\s+[^\n]*GlyphLib\.prependGlyph[^\n]*\n"
             r"\s*\d+:\s+putstatic\s+[^\n]*"+cls+r":")
    assert re.search(pattern,clinit), f"Missing literal/prepend/store {cls}"
    code=dump(package+".common.glyph."+cls)
    instance_init=body(code,cls+"();")
    assert re.search(r"// Field \S*AddonGlyphNames\."+cls+r":",instance_init),cls
    assert "ArsAdditions.prefix" in instance_init,cls
    print("GLYPH_PATH_CONSTRUCTION="+cls+"|ars_additions:GlyphLib.prependGlyph("+path+")")
rituals={
 "RitualChunkLoading":"ritual_chunk_loading",
 "RitualLocateStructure":"ritual_locate_structure"
}
for cls,path in rituals.items():
    code=dump(package+".common.ritual."+cls)
    static=body(code,"static {};")
    assert re.search(r"// String "+path+r"\s*\n",static),cls
    assert re.search(r"ArsAdditions\.prefix",static),cls
    assert re.search(r"// Field (?:(?:\S*/)?"+cls+r"\.)?RESOURCE_LOCATION:",static),cls
    accessor=body(code,"net.minecraft.resources.ResourceLocation getRegistryName();")
    assert re.search(r"// Field (?:(?:\S*/)?"+cls+r"\.)?RESOURCE_LOCATION:",accessor),cls
    print("RITUAL_ID_CONSTRUCTION="+cls+"|ars_additions:"+path)
print("CONFIRMED_REGISTRATION_CONSTRUCTION_PATHS=5")
print("PHYSICAL_SHA1="+sha)
print("LIMIT=GlyphLib.prependGlyph host method not executed; no runtime configuration inferred")
