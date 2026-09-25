#!/usr/bin/env python3
import hashlib
import io
import json
import re
import struct
import sys
import urllib.request
import zipfile

URL = "https://www.cursemaven.com/curse/maven/somake-spells-irons-spells-addon-1461634/8867079/somake-spells-irons-spells-addon-1461634-8867079.jar"
EXPECTED_SHA1 = "171841ac9f802be9309ecc166c1d972ac6d404c0"
MODSPELLS = "com/somake/somakespells/registries/ModSpells.class"

class Reader:
    def __init__(self, data): self.data=data; self.p=0
    def u1(self): v=self.data[self.p]; self.p+=1; return v
    def u2(self): v=struct.unpack_from(">H",self.data,self.p)[0]; self.p+=2; return v
    def u4(self): v=struct.unpack_from(">I",self.data,self.p)[0]; self.p+=4; return v
    def take(self,n): b=self.data[self.p:self.p+n]; self.p+=n; return b

def parse_class(data):
    r=Reader(data)
    if r.u4()!=0xCAFEBABE: raise ValueError("not a class")
    r.u2(); r.u2()
    n=r.u2(); cp=[None]*n; i=1
    while i<n:
        tag=r.u1()
        if tag==1:
            ln=r.u2(); cp[i]=("Utf8",r.take(ln).decode("utf-8","replace"))
        elif tag in (3,4): cp[i]=("Num",r.u4())
        elif tag in (5,6): cp[i]=("Wide",r.u4(),r.u4()); i+=1
        elif tag==7: cp[i]=("Class",r.u2())
        elif tag==8: cp[i]=("String",r.u2())
        elif tag in (9,10,11): cp[i]=("Ref",tag,r.u2(),r.u2())
        elif tag==12: cp[i]=("NameType",r.u2(),r.u2())
        elif tag==15: cp[i]=("MethodHandle",r.u1(),r.u2())
        elif tag==16: cp[i]=("MethodType",r.u2())
        elif tag in (17,18): cp[i]=("Dynamic",tag,r.u2(),r.u2())
        elif tag in (19,20): cp[i]=("ModulePkg",tag,r.u2())
        else: raise ValueError(f"unknown cp tag {tag} at {i}")
        i+=1
    def utf(idx):
        x=cp[idx]
        return x[1] if x and x[0]=="Utf8" else None
    def cls(idx):
        x=cp[idx]
        return utf(x[1]) if x and x[0]=="Class" else None
    def string(idx):
        x=cp[idx]
        return utf(x[1]) if x and x[0]=="String" else None
    def ref(idx):
        x=cp[idx]
        if not x or x[0]!="Ref": return None
        nt=cp[x[3]]
        if not nt or nt[0]!="NameType": return None
        return cls(x[2]),utf(nt[1]),utf(nt[2]),x[1]
    r.u2(); r.u2(); r.u2()
    for _ in range(r.u2()): r.u2()
    for _ in range(r.u2()):
        r.u2(); r.u2(); r.u2()
        for _ in range(r.u2()):
            r.u2(); r.take(r.u4())
    methods=[]
    for _ in range(r.u2()):
        acc=r.u2(); name=utf(r.u2()); desc=utf(r.u2()); attrs=r.u2(); code=None
        for _ in range(attrs):
            an=utf(r.u2()); ln=r.u4(); payload=r.take(ln)
            if an=="Code":
                cr=Reader(payload); cr.u2(); cr.u2(); clen=cr.u4(); code=cr.take(clen)
        methods.append((name,desc,acc,code))
    return cp,utf,cls,string,ref,methods

FIXED=[1]*256
for op,n in {
0x10:2,0x11:3,0x12:2,0x13:3,0x14:3,
0x15:2,0x16:2,0x17:2,0x18:2,0x19:2,
0x36:2,0x37:2,0x38:2,0x39:2,0x3a:2,
0x84:3,0xa9:2,
0x99:3,0x9a:3,0x9b:3,0x9c:3,0x9d:3,0x9e:3,
0x9f:3,0xa0:3,0xa1:3,0xa2:3,0xa3:3,0xa4:3,0xa5:3,0xa6:3,
0xa7:3,0xa8:3,
0xb2:3,0xb3:3,0xb4:3,0xb5:3,0xb6:3,0xb7:3,0xb8:3,
0xb9:5,0xba:5,0xbb:3,0xbc:2,0xbd:3,0xc0:3,0xc1:3,
0xc5:4,0xc6:3,0xc7:3,0xc8:5,0xc9:5
}.items(): FIXED[op]=n

COND_NAMES={
0x99:"ifeq",0x9a:"ifne",0x9b:"iflt",0x9c:"ifge",0x9d:"ifgt",0x9e:"ifle",
0x9f:"if_icmpeq",0xa0:"if_icmpne",0xa1:"if_icmplt",0xa2:"if_icmpge",
0xa3:"if_icmpgt",0xa4:"if_icmple",0xa5:"if_acmpeq",0xa6:"if_acmpne",
0xc6:"ifnull",0xc7:"ifnonnull"
}

def instructions(code):
    out=[]; p=0
    while p<len(code):
        start=p; op=code[p]
        if op==0xaa:
            p+=1
            while p%4: p+=1
            p+=4
            low=struct.unpack_from(">i",code,p)[0]; p+=4
            high=struct.unpack_from(">i",code,p)[0]; p+=4
            p+=4*(high-low+1)
        elif op==0xab:
            p+=1
            while p%4: p+=1
            p+=4
            npairs=struct.unpack_from(">i",code,p)[0]; p+=4
            p+=8*npairs
        elif op==0xc4:
            nxt=code[p+1]; p+=6 if nxt==0x84 else 4
        else:
            p+=FIXED[op]
        raw=code[start:p]
        target=None
        if op in COND_NAMES or op in (0xa7,0xa8):
            target=start+struct.unpack_from(">h",raw,1)[0]
        elif op in (0xc8,0xc9):
            target=start+struct.unpack_from(">i",raw,1)[0]
        out.append({"off":start,"op":op,"raw":raw,"target":target})
    return out

def download():
    req=urllib.request.Request(URL,headers={"User-Agent":"Black-Arcana-clean-room-audit/1"})
    with urllib.request.urlopen(req,timeout=120) as resp: return resp.read()

def sha(data,name):
    h=hashlib.new(name); h.update(data); return h.hexdigest()

def main():
    blob=download()
    got=sha(blob,"sha1")
    print(f"SOMAKE_PREDICATE_SIZE={len(blob)}")
    print(f"SOMAKE_PREDICATE_SHA1={got}")
    print(f"SOMAKE_PREDICATE_SHA256={sha(blob,'sha256')}")
    if got!=EXPECTED_SHA1:
        raise RuntimeError(f"SHA1 mismatch expected {EXPECTED_SHA1} got {got}")
    print("SOMAKE_PREDICATE_PHYSICAL_HASH_MATCH=true")

    with zipfile.ZipFile(io.BytesIO(blob)) as zf:
        cp,utf,cls,string,ref,methods=parse_class(zf.read(MODSPELLS))
        clinit=next((m for m in methods if m[0]=="<clinit>"),None)
        if not clinit or clinit[3] is None: raise RuntimeError("ModSpells <clinit> code missing")
        ins=instructions(clinit[3])

        last_string=None
        events=[]
        isloaded_events=[]
        register_events=[]
        for idx,it in enumerate(ins):
            op=it["op"]; raw=it["raw"]; off=it["off"]
            if op==0x12:
                s=string(raw[1])
                if s is not None: last_string=s
            elif op in (0x13,0x14):
                s=string(struct.unpack_from(">H",raw,1)[0])
                if s is not None: last_string=s
            elif op in (0xb6,0xb7,0xb8,0xb9):
                rr=ref(struct.unpack_from(">H",raw,1)[0])
                if rr:
                    owner,name,desc,tag=rr
                    if owner and owner.endswith("/ModList") and name=="isLoaded":
                        e={"kind":"isloaded","off":off,"modid":last_string,"ins_index":idx}
                        isloaded_events.append(e); events.append(e)
                    if owner and "DeferredRegister" in owner and name=="register":
                        e={"kind":"register","off":off,"id":last_string,"ins_index":idx}
                        register_events.append(e); events.append(e)

        gates=[]
        for ev in isloaded_events:
            idx=ev["ins_index"]
            # Boolean result normally feeds the next conditional branch; allow a few non-branch ops.
            branch=None
            for j in range(idx+1,min(idx+5,len(ins))):
                if ins[j]["op"] in COND_NAMES:
                    branch=ins[j]; break
                if ins[j]["op"] in (0xa7,0xc8):
                    break
            if not branch:
                print(f"SOMAKE_PREDICATE_UNMAPPED_ISLOADED={ev['off']}|{ev['modid']}")
                continue
            bname=COND_NAMES[branch["op"]]
            target=branch["target"]
            gated=[]
            polarity="manual"
            # Common javac pattern: isLoaded -> ifeq skipTarget -> gated registrations.
            if branch["op"]==0x99 and target is not None and target>branch["off"]:
                gated=[r["id"] for r in register_events if branch["off"] < r["off"] < target]
                polarity="present"
            # Less-common inverse pattern: isLoaded -> ifne target. Report but do not infer.
            elif branch["op"]==0x9a and target is not None and target>branch["off"]:
                gated=[r["id"] for r in register_events if branch["off"] < r["off"] < target]
                polarity="absent_or_else_manual"
            gates.append({
                "modid":ev["modid"],"isloaded_off":ev["off"],"branch":bname,
                "branch_off":branch["off"],"target":target,"polarity":polarity,"ids":gated
            })

        print(f"SOMAKE_PREDICATE_REGISTER_COUNT={len(register_events)}")
        print(f"SOMAKE_PREDICATE_ISLOADED_COUNT={len(isloaded_events)}")
        print(f"SOMAKE_PREDICATE_GATE_COUNT={len(gates)}")
        for g in gates:
            print("SOMAKE_PREDICATE_GATE="+json.dumps(g,separators=(",",":"),sort_keys=True))

        all_gated=set()
        for g in gates:
            if g["polarity"]=="present":
                all_gated.update(x for x in g["ids"] if x)
        unconditional=[r["id"] for r in register_events if r["id"] not in all_gated]
        print(f"SOMAKE_PREDICATE_POSITIVE_GATED_ID_COUNT={len(all_gated)}")
        print("SOMAKE_PREDICATE_POSITIVE_GATED_IDS="+",".join(sorted(all_gated)))
        print(f"SOMAKE_PREDICATE_UNCONDITIONAL_OR_UNRESOLVED_COUNT={len(unconditional)}")
        print("SOMAKE_PREDICATE_UNCONDITIONAL_OR_UNRESOLVED_IDS="+",".join(unconditional))

        # Full event stream is factual and bounded to registry control-flow.
        for ev in sorted(events,key=lambda x:x["off"]):
            if ev["kind"]=="isloaded":
                print(f"SOMAKE_PREDICATE_EVENT=ISLOADED|off={ev['off']}|modid={ev['modid']}")
            else:
                print(f"SOMAKE_PREDICATE_EVENT=REGISTER|off={ev['off']}|id={ev['id']}")

        if len(register_events)!=83:
            raise RuntimeError(f"expected 83 registrations, got {len(register_events)}")
        if any(g["polarity"]!="present" for g in gates):
            raise RuntimeError("non-standard optional gate polarity observed; manual review required")
        if any(not g["ids"] for g in gates):
            raise RuntimeError("optional gate with no mapped registrations; manual review required")
        print("SOMAKE_1_0_9_PREDICATE_MAP_AUDIT=true")

if __name__=="__main__":
    try:
        main()
    except Exception as exc:
        print(f"SOMAKE_PREDICATE_AUDIT_ERROR={type(exc).__name__}: {exc}",file=sys.stderr)
        raise
