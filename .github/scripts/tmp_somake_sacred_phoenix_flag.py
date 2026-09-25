#!/usr/bin/env python3
import hashlib, io, struct, sys, urllib.request, zipfile

URL="https://www.cursemaven.com/curse/maven/somake-spells-irons-spells-addon-1461634/8867079/somake-spells-irons-spells-addon-1461634-8867079.jar"
SHA1="171841ac9f802be9309ecc166c1d972ac6d404c0"
TARGET="com/somake/somakespells/registries/ModSpells.class"

class R:
    def __init__(self,b): self.b=b; self.p=0
    def u1(self): v=self.b[self.p]; self.p+=1; return v
    def u2(self): v=struct.unpack_from(">H",self.b,self.p)[0]; self.p+=2; return v
    def u4(self): v=struct.unpack_from(">I",self.b,self.p)[0]; self.p+=4; return v
    def take(self,n): v=self.b[self.p:self.p+n]; self.p+=n; return v

def parse(data):
    r=R(data)
    if r.u4()!=0xCAFEBABE: raise RuntimeError("bad class")
    r.u2(); r.u2(); n=r.u2(); cp=[None]*n; i=1
    while i<n:
        t=r.u1()
        if t==1:
            ln=r.u2(); cp[i]=("Utf8",r.take(ln).decode("utf-8","replace"))
        elif t in (3,4): cp[i]=("Num",r.u4())
        elif t in (5,6): cp[i]=("Wide",r.u4(),r.u4()); i+=1
        elif t==7: cp[i]=("Class",r.u2())
        elif t==8: cp[i]=("String",r.u2())
        elif t in (9,10,11): cp[i]=("Ref",t,r.u2(),r.u2())
        elif t==12: cp[i]=("NameType",r.u2(),r.u2())
        elif t==15: cp[i]=("MethodHandle",r.u1(),r.u2())
        elif t==16: cp[i]=("MethodType",r.u2())
        elif t in (17,18): cp[i]=("Dynamic",t,r.u2(),r.u2())
        elif t in (19,20): cp[i]=("ModulePkg",t,r.u2())
        else: raise RuntimeError(f"cp tag {t}")
        i+=1
    def utf(idx):
        x=cp[idx]; return x[1] if x and x[0]=="Utf8" else None
    def cls(idx):
        x=cp[idx]; return utf(x[1]) if x and x[0]=="Class" else None
    def string(idx):
        x=cp[idx]; return utf(x[1]) if x and x[0]=="String" else None
    def ref(idx):
        x=cp[idx]
        if not x or x[0]!="Ref": return None
        nt=cp[x[3]]
        return (cls(x[2]),utf(nt[1]),utf(nt[2]),x[1]) if nt and nt[0]=="NameType" else None
    r.u2(); r.u2(); r.u2()
    for _ in range(r.u2()): r.u2()
    for _ in range(r.u2()):
        r.u2(); r.u2(); r.u2()
        for __ in range(r.u2()): r.u2(); r.take(r.u4())
    methods=[]
    for _ in range(r.u2()):
        acc=r.u2(); name=utf(r.u2()); desc=utf(r.u2()); code=None
        for __ in range(r.u2()):
            an=utf(r.u2()); ln=r.u4(); payload=r.take(ln)
            if an=="Code":
                cr=R(payload); cr.u2(); cr.u2(); clen=cr.u4(); code=cr.take(clen)
        methods.append((name,desc,code))
    return cp,string,ref,methods

FIXED=[1]*256
for op,n in {
0x10:2,0x11:3,0x12:2,0x13:3,0x14:3,0x15:2,0x16:2,0x17:2,0x18:2,0x19:2,
0x36:2,0x37:2,0x38:2,0x39:2,0x3a:2,0x84:3,0xa9:2,
0x99:3,0x9a:3,0x9b:3,0x9c:3,0x9d:3,0x9e:3,0x9f:3,0xa0:3,0xa1:3,0xa2:3,0xa3:3,0xa4:3,0xa5:3,0xa6:3,0xa7:3,0xa8:3,
0xb2:3,0xb3:3,0xb4:3,0xb5:3,0xb6:3,0xb7:3,0xb8:3,0xb9:5,0xba:5,0xbb:3,0xbc:2,0xbd:3,0xc0:3,0xc1:3,0xc5:4,0xc6:3,0xc7:3,0xc8:5,0xc9:5
}.items(): FIXED[op]=n

def insns(code):
    out=[]; p=0
    while p<len(code):
        s=p; op=code[p]
        if op==0xaa:
            p+=1
            while p%4:p+=1
            p+=4; lo=struct.unpack_from(">i",code,p)[0]; p+=4; hi=struct.unpack_from(">i",code,p)[0]; p+=4; p+=4*(hi-lo+1)
        elif op==0xab:
            p+=1
            while p%4:p+=1
            p+=4; n=struct.unpack_from(">i",code,p)[0]; p+=4; p+=8*n
        elif op==0xc4: p+=6 if code[p+1]==0x84 else 4
        else: p+=FIXED[op]
        out.append((s,op,code[s:p]))
    return out


def analyze_startup_features(zf):
    target="com/somake/somakespells/config/StartupFeatures.class"
    cp,string,ref,methods=parse(zf.read(target))
    code=next(c for n,d,c in methods if n=="isSacredPhoenixBlessingEnabled")
    seq=insns(code)
    print("SOMAKE_STARTUP_METHOD=isSacredPhoenixBlessingEnabled")
    for off,op,raw in seq:
        value=None; kind=f"OP_{op:02x}"
        if op==0x12:
            value=string(raw[1]); kind="LDC"
        elif op in (0x13,0x14):
            value=string(struct.unpack_from(">H",raw,1)[0]); kind="LDC"
        elif op in (0xb2,0xb3,0xb4,0xb5,0xb6,0xb7,0xb8,0xb9):
            rr=ref(struct.unpack_from(">H",raw,1)[0])
            if rr:
                value=rr[:3]
                kind={0xb2:"GETSTATIC",0xb3:"PUTSTATIC",0xb4:"GETFIELD",0xb5:"PUTFIELD",0xb6:"INVOKEVIRTUAL",0xb7:"INVOKESPECIAL",0xb8:"INVOKESTATIC",0xb9:"INVOKEINTERFACE"}[op]
        if kind in {"LDC","GETSTATIC","PUTSTATIC","GETFIELD","PUTFIELD","INVOKEVIRTUAL","INVOKESPECIAL","INVOKESTATIC","INVOKEINTERFACE"}:
            print(f"SOMAKE_STARTUP_CONTEXT={off}|{kind}|{value}")
    print("SOMAKE_STARTUP_AUDIT_COMPLETE=true")

def main():
    req=urllib.request.Request(URL,headers={"User-Agent":"Black-Arcana-clean-room-audit/1"})
    with urllib.request.urlopen(req,timeout=120) as resp: blob=resp.read()
    got=hashlib.sha1(blob).hexdigest()
    print(f"SOMAKE_FLAG_SHA1={got}")
    if got!=SHA1: raise RuntimeError(f"sha mismatch {got}")
    with zipfile.ZipFile(io.BytesIO(blob)) as zf:
        analyze_startup_features(zf)
        cp,string,ref,methods=parse(zf.read(TARGET))
    code=next(c for n,d,c in methods if n=="<clinit>")
    seq=insns(code)
    decoded=[]
    for off,op,raw in seq:
        value=None; kind=f"OP_{op:02x}"
        if op==0x12:
            value=string(raw[1]); kind="LDC"
        elif op in (0x13,0x14):
            value=string(struct.unpack_from(">H",raw,1)[0]); kind="LDC"
        elif op in (0xb2,0xb3,0xb4,0xb5,0xb6,0xb7,0xb8,0xb9):
            rr=ref(struct.unpack_from(">H",raw,1)[0])
            if rr:
                value=rr[:3]
                kind={0xb2:"GETSTATIC",0xb3:"PUTSTATIC",0xb4:"GETFIELD",0xb5:"PUTFIELD",0xb6:"INVOKEVIRTUAL",0xb7:"INVOKESPECIAL",0xb8:"INVOKESTATIC",0xb9:"INVOKEINTERFACE"}[op]
        decoded.append((off,kind,value))
    target_idx=None
    for i,(off,kind,value) in enumerate(decoded):
        if kind=="PUTSTATIC" and value and value[1]=="SACRED_PHOENIX_BLESSING_ENABLED":
            target_idx=i; break
    if target_idx is None: raise RuntimeError("flag assignment not found")
    print(f"SOMAKE_FLAG_ASSIGN_OFF={decoded[target_idx][0]}")
    for off,kind,value in decoded[max(0,target_idx-18):target_idx+2]:
        if kind in {"LDC","GETSTATIC","PUTSTATIC","GETFIELD","PUTFIELD","INVOKEVIRTUAL","INVOKESPECIAL","INVOKESTATIC","INVOKEINTERFACE"}:
            print(f"SOMAKE_FLAG_CONTEXT={off}|{kind}|{value}")
    print("SOMAKE_FLAG_AUDIT_COMPLETE=true")

if __name__=="__main__":
    try: main()
    except Exception as exc:
        print(f"SOMAKE_FLAG_AUDIT_ERROR={type(exc).__name__}: {exc}",file=sys.stderr); raise
