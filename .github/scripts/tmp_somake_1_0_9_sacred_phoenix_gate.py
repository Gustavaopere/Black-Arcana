#!/usr/bin/env python3
import hashlib, io, json, struct, sys, urllib.request, zipfile

URL="https://www.cursemaven.com/curse/maven/somake-spells-irons-spells-addon-1461634/8867079/somake-spells-irons-spells-addon-1461634-8867079.jar"
EXPECTED_SHA1="171841ac9f802be9309ecc166c1d972ac6d404c0"
TARGET="com/somake/somakespells/config/StartupFeatures.class"

class R:
    def __init__(self,b): self.b=b; self.p=0
    def u1(self): v=self.b[self.p]; self.p+=1; return v
    def u2(self): v=struct.unpack_from(">H",self.b,self.p)[0]; self.p+=2; return v
    def u4(self): v=struct.unpack_from(">I",self.b,self.p)[0]; self.p+=4; return v
    def take(self,n): v=self.b[self.p:self.p+n]; self.p+=n; return v

def parse_class(data):
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
        elif t==15: cp[i]=("MH",r.u1(),r.u2())
        elif t==16: cp[i]=("MT",r.u2())
        elif t in (17,18): cp[i]=("Dyn",t,r.u2(),r.u2())
        elif t in (19,20): cp[i]=("MP",t,r.u2())
        else: raise RuntimeError(f"cp tag {t}")
        i+=1
    def utf(i):
        x=cp[i]; return x[1] if x and x[0]=="Utf8" else None
    def cls(i):
        x=cp[i]; return utf(x[1]) if x and x[0]=="Class" else None
    def string(i):
        x=cp[i]; return utf(x[1]) if x and x[0]=="String" else None
    def ref(i):
        x=cp[i]
        if not x or x[0]!="Ref": return None
        nt=cp[x[3]]
        if not nt or nt[0]!="NameType": return None
        return cls(x[2]),utf(nt[1]),utf(nt[2]),x[1]
    r.u2(); this_idx=r.u2(); r.u2()
    this_name=cls(this_idx)
    for _ in range(r.u2()): r.u2()
    fields=[]
    for _ in range(r.u2()):
        acc=r.u2(); name=utf(r.u2()); desc=utf(r.u2()); ac=r.u2()
        for __ in range(ac): r.u2(); r.take(r.u4())
        fields.append((name,desc,acc))
    methods=[]
    for _ in range(r.u2()):
        acc=r.u2(); name=utf(r.u2()); desc=utf(r.u2()); ac=r.u2(); code=None
        for __ in range(ac):
            an=utf(r.u2()); ln=r.u4(); payload=r.take(ln)
            if an=="Code":
                cr=R(payload); cr.u2(); cr.u2(); clen=cr.u4(); code=cr.take(clen)
        methods.append((name,desc,acc,code))
    return this_name, string, ref, fields, methods

FIX=[1]*256
for op,n in {
0x10:2,0x11:3,0x12:2,0x13:3,0x14:3,0x15:2,0x16:2,0x17:2,0x18:2,0x19:2,
0x36:2,0x37:2,0x38:2,0x39:2,0x3a:2,0x84:3,0xa9:2,
0x99:3,0x9a:3,0x9b:3,0x9c:3,0x9d:3,0x9e:3,0x9f:3,0xa0:3,0xa1:3,0xa2:3,0xa3:3,0xa4:3,0xa5:3,0xa6:3,
0xa7:3,0xa8:3,0xb2:3,0xb3:3,0xb4:3,0xb5:3,0xb6:3,0xb7:3,0xb8:3,0xb9:5,0xba:5,
0xbb:3,0xbc:2,0xbd:3,0xc0:3,0xc1:3,0xc5:4,0xc6:3,0xc7:3,0xc8:5,0xc9:5
}.items(): FIX[op]=n
BR={
0x99:"ifeq",0x9a:"ifne",0x9b:"iflt",0x9c:"ifge",0x9d:"ifgt",0x9e:"ifle",
0x9f:"if_icmpeq",0xa0:"if_icmpne",0xa1:"if_icmplt",0xa2:"if_icmpge",0xa3:"if_icmpgt",0xa4:"if_icmple",
0xa5:"if_acmpeq",0xa6:"if_acmpne",0xc6:"ifnull",0xc7:"ifnonnull",0xa7:"goto",0xc8:"goto_w"
}

def insns(code):
    out=[]; p=0
    while p<len(code):
        s=p; op=code[p]; target=None
        if op==0xaa:
            p+=1
            while p%4: p+=1
            default=struct.unpack_from(">i",code,p)[0]; p+=4
            lo=struct.unpack_from(">i",code,p)[0]; p+=4
            hi=struct.unpack_from(">i",code,p)[0]; p+=4
            p+=4*(hi-lo+1)
            target=s+default
        elif op==0xab:
            p+=1
            while p%4: p+=1
            default=struct.unpack_from(">i",code,p)[0]; p+=4
            np=struct.unpack_from(">i",code,p)[0]; p+=4
            p+=8*np; target=s+default
        elif op==0xc4:
            nxt=code[p+1]; p+=6 if nxt==0x84 else 4
        else:
            p+=FIX[op]
            if op in BR and op!=0xaa and op!=0xab:
                target=s+(struct.unpack_from(">i" if op==0xc8 else ">h",code,s+1)[0])
        out.append((s,op,code[s:p],target))
    return out

def cpi(raw): return struct.unpack_from(">H",raw,1)[0]

def summarize(label, data, wanted=None):
    this_name,string,ref,fields,methods=parse_class(data)
    print(f"SOMAKE_SACRED_CLASS={this_name}")
    print(f"SOMAKE_SACRED_FIELD_COUNT={len(fields)}")
    for name,desc,acc in fields:
        if "SACRED" in name.upper() or "PHOENIX" in name.upper():
            print(f"SOMAKE_SACRED_FIELD={name}|{desc}|access={acc}")
    for name,desc,acc,code in methods:
        if wanted and name not in wanted: continue
        if code is None: continue
        events=[]
        last_string=None
        for off,op,raw,target in insns(code):
            if op==0x12:
                s=string(raw[1])
                if s is not None: last_string=s; events.append({"kind":"string","off":off,"value":s})
            elif op in (0x13,0x14):
                s=string(cpi(raw))
                if s is not None: last_string=s; events.append({"kind":"string","off":off,"value":s})
            elif op in (0xb2,0xb3,0xb4,0xb5):
                rr=ref(cpi(raw))
                if rr: events.append({"kind":"field","off":off,"op":op,"owner":rr[0],"name":rr[1],"desc":rr[2]})
            elif op in (0xb6,0xb7,0xb8,0xb9):
                rr=ref(cpi(raw))
                if rr: events.append({"kind":"method","off":off,"owner":rr[0],"name":rr[1],"desc":rr[2],"last_string":last_string})
            if op in BR:
                events.append({"kind":"branch","off":off,"op":BR[op],"target":target})
            if op in (0x03,0x04,0xac,0xb0,0xb1):
                events.append({"kind":"simple","off":off,"op":op})
        print(f"SOMAKE_SACRED_METHOD={name}|{desc}|access={acc}|code_len={len(code)}")
        print("SOMAKE_SACRED_EVENTS="+json.dumps(events,separators=(",",":"),sort_keys=True))

def download():
    req=urllib.request.Request(URL,headers={"User-Agent":"Black-Arcana-clean-room-audit/1"})
    with urllib.request.urlopen(req,timeout=120) as r: return r.read()

def h(data,n):
    x=hashlib.new(n); x.update(data); return x.hexdigest()

def main():
    blob=download()
    print(f"SOMAKE_SACRED_SIZE={len(blob)}")
    print(f"SOMAKE_SACRED_SHA1={h(blob,'sha1')}")
    print(f"SOMAKE_SACRED_SHA256={h(blob,'sha256')}")
    if h(blob,"sha1")!=EXPECTED_SHA1: raise RuntimeError("hash mismatch")
    print("SOMAKE_SACRED_PHYSICAL_HASH_MATCH=true")
    with zipfile.ZipFile(io.BytesIO(blob)) as zf:
        if TARGET not in zf.namelist(): raise RuntimeError("StartupFeatures.class missing")
        summarize("startup",zf.read(TARGET),wanted={"isSacredPhoenixBlessingEnabled","<clinit>"})
        print("SOMAKE_1_0_9_SACRED_PHOENIX_GATE_AUDIT=true")

if __name__=="__main__":
    try: main()
    except Exception as e:
        print(f"SOMAKE_SACRED_AUDIT_ERROR={type(e).__name__}: {e}",file=sys.stderr)
        raise
