"""Ars Hex 5.0.4b physical glyph registry audit, read-only clean-room.
Never print bytecode, implementation method bodies or third-party JSON.
"""
from pathlib import Path
import hashlib,os,re,subprocess,zipfile
P=Path(os.environ["EXACT_JAR"])
SHA="2354710ea312e2a6e0fbc3eb2dbafb8e06f10cf4"
assert hashlib.sha1(P.read_bytes()).hexdigest()==SHA, "JAR vs physical SHA1 mismatch"
assert P.stat().st_size>0
C="com.alexthw.ars_hex."
def javap(cls):
    x=subprocess.run(["javap","-c","-p","-classpath",str(P),cls],capture_output=True,text=True,check=True)
    return x.stdout

def segment(raw, signature):
    ls=raw.splitlines()
    match=[i for i,s in enumerate(ls) if s.strip().endswith(signature)]
    assert len(match)==1,(signature,len(match))
    start=match[0];end=len(ls)
    for i in range(start+1,len(ls)):
        line=ls[i]
        if line=="}" or re.match(r"^  (?:public|private|protected|static)\s",line):
            end=i;break
    return "\n".join(ls[start:end])
registry=javap(C+"ArsNouveauRegistry")
entry=javap(C+"ArsHex")
effect=javap(C+"glyphs.EffectSoulShatter")
init=segment(registry,"void init();")
glyphs=segment(registry,"void registerCompatGlyphs();")
malum=segment(registry,"void registerMalumGlyphs();")
wrapper=segment(registry,"void register(com.hollingsworth.arsnouveau.api.spell.AbstractSpellPart);")
perks=segment(registry,"void registerCompatPerks();")
constructor=segment(effect,"EffectSoulShatter();")
prefix=segment(entry,"net.minecraft.resources.ResourceLocation prefix(java.lang.String);")
assert len(re.findall(r"ArsNouveauRegistry\.init",entry))==1,"ArsHex entrypoint init call count"
assert len(re.findall(r"registerCompatGlyphs",init))==1
assert len(re.findall(r"registerCompatPerks",init))==1
assert len(re.findall(r"// String malum\b",glyphs))==1
assert len(re.findall(r"ModList\.get:",glyphs))==1
assert len(re.findall(r"ModList\.isLoaded",glyphs))==1
assert len(re.findall(r"registerMalumGlyphs:",glyphs))==1
assert len(re.findall(r"EffectSoulShatter\.INSTANCE",malum))==1
assert len(re.findall(r"// Method register:",malum))==1
assert len(re.findall(r"GlyphRegistry\.registerSpell",wrapper))==1
assert len(re.findall(r"registeredSpells",wrapper))==1
assert len(re.findall(r"// String glyph_soul_shatter",constructor))==1
assert len(re.findall(r"ArsHex\.prefix",constructor))==1
assert len(re.findall(r"// String ars_hex",prefix))==1
assert len(re.findall(r"ResourceLocation\.fromNamespaceAndPath",prefix))==1
assert len(re.findall(r"// String malum\b",perks))==1
assert len(re.findall(r"PerkRegistry\.registerPerk",perks))==3
assert all(perk+".INSTANCE" in perks for perk in ["SoulWardPerk","MagicProficencyPerk","SpiritSpoilsPerk"])
assert len(re.findall(r"PerkRegistry\.registerPerk",registry))==3
assert len(re.findall(r"GlyphRegistry\.registerSpell",registry))==1
# Inspect only glyph class file identities, not bytecode or recipe content.
with zipfile.ZipFile(P) as z:
    gl=sorted(s for s in z.namelist() if s.startswith("com/alexthw/ars_hex/glyphs/") and s.endswith(".class") and "$" not in s)
    assert gl==["com/alexthw/ars_hex/glyphs/EffectSoulShatter.class"],"unexpected glyph class inventory"
assert "MoonDial" not in " ".join(gl)
print("PHYSICAL_SHA1="+SHA)
print("PHYSICAL_JAR_BYTES="+str(P.stat().st_size))
print("MOD_ID=ars_hex")
print("BOOTSTRAP_ARS_NOUVEAU_INIT_CALLS=1")
print("GLYPH_GATE=ModList.isLoaded(malum)")
print("GLYPH_OWNER=ars_hex")
print("GLYPH_ID=ars_hex:glyph_soul_shatter")
print("GLYPH_CLASS=EffectSoulShatter")
print("GLYPH_REGISTER_WRAPPER_CALLS=1")
print("HOST_GLYPH_REGISTER_SPELL_CALLS=1")
print("MALUM_CONDITIONAL_PERK_REGISTRATIONS=3")
print("GLYPH_CLASS_FILES=1")
print("IDENTITY_BINARY_AUDIT=SUCCESS")
print("LIMIT=gate static only; ModList runtime result and physical Survival unobserved")
