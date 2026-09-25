#!/usr/bin/env python3
import hashlib
import io
import json
import re
import struct
import sys
import tempfile
import urllib.request
import zipfile
from pathlib import Path

CURRENT_URL = "https://www.cursemaven.com/curse/maven/somake-spells-irons-spells-addon-1461634/8867079/somake-spells-irons-spells-addon-1461634-8867079.jar"
CURRENT_SHA1 = "171841ac9f802be9309ecc166c1d972ac6d404c0"
OLD_URL = "https://www.cursemaven.com/curse/maven/somake-spells-irons-spells-addon-1461634/8417850/somake-spells-irons-spells-addon-1461634-8417850.jar"
OLD_SHA1 = "b0ad94c1504709662bee2d08700375ccecbb5ec7"
MODSPELLS = "com/somake/somakespells/registries/ModSpells.class"
LANG = "assets/somakespells/lang/en_us.json"

class Reader:
    def __init__(self, data):
        self.data=data; self.p=0
    def u1(self):
        v=self.data[self.p]; self.p+=1; return v
    def u2(self):
        v=struct.unpack_from(">H",self.data,self.p)[0]; self.p+=2; return v
    def u4(self):
        v=struct.unpack_from(">I",self.data,self.p)[0]; self.p+=4; return v
    def take(self,n):
        b=self.data[self.p:self.p+n]; self.p+=n; return b

def parse_class(data):
    r=Reader(data)
    if r.u4()!=0xCAFEBABE: raise ValueError("not a class")
    r.u2(); r.u2()
    n=r.u2()
    cp=[None]*n
    i=1
    while i<n:
        tag=r.u1()
        if tag==1:
            ln=r.u2(); cp[i]=("Utf8",r.take(ln).decode("utf-8","replace"))
        elif tag in (3,4):
            cp[i]=("Num",r.u4())
        elif tag in (5,6):
            cp[i]=("Wide",r.u4(),r.u4()); i+=1
        elif tag==7:
            cp[i]=("Class",r.u2())
        elif tag==8:
            cp[i]=("String",r.u2())
        elif tag in (9,10,11):
            cp[i]=("Ref",tag,r.u2(),r.u2())
        elif tag==12:
            cp[i]=("NameType",r.u2(),r.u2())
        elif tag==15:
            cp[i]=("MethodHandle",r.u1(),r.u2())
        elif tag==16:
            cp[i]=("MethodType",r.u2())
        elif tag in (17,18):
            cp[i]=("Dynamic",tag,r.u2(),r.u2())
        elif tag in (19,20):
            cp[i]=("ModulePkg",tag,r.u2())
        else:
            raise ValueError(f"unknown cp tag {tag} at {i}")
        i+=1
    def utf(idx):
        x=cp[idx]
        if not x or x[0]!="Utf8": return None
        return x[1]
    def cls(idx):
        x=cp[idx]
        return utf(x[1]) if x and x[0]=="Class" else None
    def string(idx):
        x=cp[idx]
        return utf(x[1]) if x and x[0]=="String" else None
    def ref(idx):
        x=cp[idx]
        if not x or x[0]!="Ref": return None
        owner=cls(x[2]); nt=cp[x[3]]
        if not nt or nt[0]!="NameType": return None
        return owner,utf(nt[1]),utf(nt[2]),x[1]
    r.u2(); r.u2(); r.u2()
    interfaces=r.u2()
    for _ in range(interfaces): r.u2()
    fields=[]
    nf=r.u2()
    for _ in range(nf):
        acc=r.u2(); name=utf(r.u2()); desc=utf(r.u2()); na=r.u2()
        for _ in range(na):
            r.u2(); ln=r.u4(); r.take(ln)
        fields.append((name,desc,acc))
    methods=[]
    nm=r.u2()
    for _ in range(nm):
        acc=r.u2(); name=utf(r.u2()); desc=utf(r.u2()); na=r.u2()
        code=None
        for _ in range(na):
            an=utf(r.u2()); ln=r.u4(); payload=r.take(ln)
            if an=="Code":
                cr=Reader(payload)
                cr.u2(); cr.u2(); clen=cr.u4()
                code=cr.take(clen)
        methods.append((name,desc,acc,code))
    utf8={x[1] for x in cp if x and x[0]=="Utf8"}
    return cp,utf,cls,string,ref,fields,methods,utf8

# Fixed lengths including opcode byte. Variable opcodes are handled separately.
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

BRANCH_OPS=set(range(0x99,0xa9))|{0xc6,0xc7,0xc8,0xc9}

def instructions(code):
    out=[]; p=0
    while p<len(code):
        start=p; op=code[p]
        if op==0xaa: # tableswitch
            p+=1
            while p%4: p+=1
            default=struct.unpack_from(">i",code,p)[0]; p+=4
            low=struct.unpack_from(">i",code,p)[0]; p+=4
            high=struct.unpack_from(">i",code,p)[0]; p+=4
            p+=4*(high-low+1)
        elif op==0xab: # lookupswitch
            p+=1
            while p%4: p+=1
            p+=4
            npairs=struct.unpack_from(">i",code,p)[0]; p+=4
            p+=8*npairs
        elif op==0xc4: # wide
            nxt=code[p+1]
            p+=6 if nxt==0x84 else 4
        else:
            p+=FIXED[op]
        out.append((start,op,code[start:p]))
    return out

def analyze_modspells(data):
    cp,utf,cls,string,ref,fields,methods,utf8=parse_class(data)
    holders=[name for name,desc,_ in fields if desc and "DeferredHolder" in desc]
    clinit=next((m for m in methods if m[0]=="<clinit>"),None)
    if not clinit or clinit[3] is None: raise RuntimeError("ModSpells <clinit> code not found")
    ins=instructions(clinit[3])
    last_string=None
    register_ids=[]
    isloaded_args=[]
    branches=0
    for off,op,raw in ins:
        if op in BRANCH_OPS: branches+=1
        if op==0x12:
            idx=raw[1]; s=string(idx)
            if s is not None: last_string=s
        elif op in (0x13,0x14):
            idx=struct.unpack_from(">H",raw,1)[0]; s=string(idx)
            if s is not None: last_string=s
        elif op in (0xb6,0xb7,0xb8,0xb9):
            idx=struct.unpack_from(">H",raw,1)[0]
            rr=ref(idx)
            if rr:
                owner,name,desc,tag=rr
                if owner and "DeferredRegister" in owner and name=="register":
                    register_ids.append(last_string)
                if owner and owner.endswith("/ModList") and name=="isLoaded":
                    isloaded_args.append(last_string)
    # Bounded conditional-scope topology: pair isLoaded-like calls with the next
    # forward conditional branch and list register calls inside that skipped range.
    events=[]
    last_string=None
    register_events=[]
    call_events=[]
    for off,op,raw in ins:
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
                if owner and "DeferredRegister" in owner and name=="register":
                    register_events.append((off,last_string))
                if name=="isLoaded":
                    call_events.append((off,owner,last_string))
    conditional_ops=set(range(0x99,0xa7))|{0xc6,0xc7}
    gate_scopes=[]
    for call_off,owner,arg in call_events:
        later=[x for x in ins if x[0]>call_off][:4]
        br=next((x for x in later if x[1] in conditional_ops),None)
        if not br or len(br[2])<3:
            continue
        rel=struct.unpack(">h",br[2][1:3])[0]
        target=br[0]+rel
        scoped=[rid for roff,rid in register_events if br[0] < roff < target] if target>br[0] else []
        gate_scopes.append((call_off,owner,arg,br[0],br[1],target,scoped))
    return {
      "holder_fields":holders,
      "register_ids":register_ids,
      "isloaded_args":isloaded_args,
      "branch_count":branches,
      "gate_scopes":gate_scopes,
      "utf8":utf8
    }

def sha(data,name):
    h=hashlib.new(name); h.update(data); return h.hexdigest()

def download(url):
    req=urllib.request.Request(url,headers={"User-Agent":"Black-Arcana-clean-room-audit/1"})
    with urllib.request.urlopen(req,timeout=120) as resp: return resp.read()

def constant_boolean_return(code):
    if code is None:
        return None
    ins=instructions(code)
    ops=[op for _,op,_ in ins if op not in (0x00,)]
    if ops==[0x03,0xac]:
        return False
    if ops==[0x04,0xac]:
        return True
    return None

def spell_class_signatures(zf):
    rows=[]
    for name in zf.namelist():
        if not name.startswith("com/somake/somakespells/") or not name.endswith("Spell.class") or "$" in name:
            continue
        try:
            _,_,_,_,_,fields,methods,utf8=parse_class(zf.read(name))
        except Exception:
            continue
        by_name={m[0]:m for m in methods}
        allow=by_name.get("allowCrafting")
        enabled=by_name.get("isEnabled")
        rows.append((
            name,
            allow is not None,
            isEnabledPresent := (enabled is not None),
            constant_boolean_return(allow[3]) if allow else None,
            constant_boolean_return(enabled[3]) if enabled else None
        ))
    return sorted(rows)

def modspells_event_trace(data):
    cp,utf,cls,string,ref,fields,methods,utf8=parse_class(data)
    clinit=next((m for m in methods if m[0]=="<clinit>"),None)
    if not clinit or clinit[3] is None:
        return []
    out=[]
    last_string=None
    for off,op,raw in instructions(clinit[3]):
        if op==0x12:
            s=string(raw[1])
            if s is not None:
                last_string=s
        elif op in (0x13,0x14):
            s=string(struct.unpack_from(">H",raw,1)[0])
            if s is not None:
                last_string=s
        elif op in (0xb2,0xb3,0xb4,0xb5,0xb6,0xb7,0xb8,0xb9):
            rr=ref(struct.unpack_from(">H",raw,1)[0])
            if rr:
                owner,name,desc,tag=rr
                if op in (0xb2,0xb3,0xb4,0xb5):
                    if owner and owner.endswith("/ModSpells"):
                        out.append((off,f"FIELD:{['getstatic','putstatic','getfield','putfield'][(op-0xb2)]}:{name}"))
                else:
                    if owner and "DeferredRegister" in owner and name=="register":
                        out.append((off,f"REGISTER:{last_string}"))
                    elif name=="isLoaded":
                        out.append((off,f"ISLOADED:{owner}|arg={last_string}"))
        elif op in set(range(0x99,0xa7))|{0xc6,0xc7}:
            rel=struct.unpack(">h",raw[1:3])[0]
            out.append((off,f"BRANCH:0x{op:02x}->" + str(off+rel)))
        elif op in (0xa7,):
            rel=struct.unpack(">h",raw[1:3])[0]
            out.append((off,f"GOTO->" + str(off+rel)))
    return out

def modlist_isloaded_hits(zf):
    rows=[]
    for name in zf.namelist():
        if not name.startswith("com/somake/somakespells/") or not name.endswith(".class"):
            continue
        try:
            cp,utf,cls,string,ref,fields,methods,utf8=parse_class(zf.read(name))
        except Exception:
            continue
        for mname,mdesc,macc,code in methods:
            if code is None:
                continue
            last_string=None
            for off,op,raw in instructions(code):
                if op==0x12:
                    s=string(raw[1])
                    if s is not None: last_string=s
                elif op in (0x13,0x14):
                    s=string(struct.unpack_from(">H",raw,1)[0])
                    if s is not None: last_string=s
                elif op in (0xb6,0xb7,0xb8,0xb9):
                    rr=ref(struct.unpack_from(">H",raw,1)[0])
                    if rr:
                        owner,rname,rdesc,tag=rr
                        if owner and owner.endswith("/ModList") and rname=="isLoaded":
                            rows.append((name,mname,last_string))
    return sorted(set(rows))

def string_class_hits(zf, token):
    b=token.encode("utf-8")
    return sorted(name for name in zf.namelist()
                  if name.startswith("com/somake/somakespells/") and name.endswith(".class") and b in zf.read(name))

def inspect(label, blob, expected_sha1):
    got=sha(blob,"sha1")
    if got!=expected_sha1: raise RuntimeError(f"{label} SHA1 mismatch expected {expected_sha1} got {got}")
    print(f"SOMAKE_{label}_SIZE={len(blob)}")
    print(f"SOMAKE_{label}_SHA1={got}")
    print(f"SOMAKE_{label}_SHA256={sha(blob,'sha256')}")
    with zipfile.ZipFile(io.BytesIO(blob)) as zf:
        if MODSPELLS not in zf.namelist(): raise RuntimeError(f"{label} ModSpells missing")
        a=analyze_modspells(zf.read(MODSPELLS))
        ids=a["register_ids"]
        if None in ids: raise RuntimeError(f"{label} register call lacked nearby string literal")
        if len(ids)!=len(set(ids)): raise RuntimeError(f"{label} duplicate registry IDs detected")
        holder=len(a["holder_fields"])
        print(f"SOMAKE_{label}_DEFERRED_HOLDER_FIELD_COUNT={holder}")
        print(f"SOMAKE_{label}_REGISTER_CALL_COUNT={len(ids)}")
        print(f"SOMAKE_{label}_BRANCH_OPCODE_COUNT={a['branch_count']}")
        print(f"SOMAKE_{label}_ISLOADED_CALL_ARGS=" + ",".join(x or "<none>" for x in a["isloaded_args"]))
        print(f"SOMAKE_{label}_GATE_SCOPE_COUNT={len(a['gate_scopes'])}")
        for call_off,owner,arg,br_off,br_op,target,scoped in a["gate_scopes"]:
            print(f"SOMAKE_{label}_GATE_SCOPE=call@{call_off}|owner={owner}|arg={arg}|branch@{br_off}:0x{br_op:02x}|target={target}|registrations={','.join(x or '<none>' for x in scoped)}")
        print(f"SOMAKE_{label}_REGISTRY_IDS=" + ",".join(ids))
        if label=="CURRENT_1_0_9":
            trace=modspells_event_trace(zf.read(MODSPELLS))
            print(f"SOMAKE_{label}_MODSPELLS_TRACE_EVENT_COUNT={len(trace)}")
            for off,event in trace:
                print(f"SOMAKE_{label}_MODSPELLS_TRACE={off}|{event}")
        sigs=spell_class_signatures(zf)
        allow=[row for row in sigs if row[1]]
        enabled=[row for row in sigs if row[2]]
        print(f"SOMAKE_{label}_TOPLEVEL_SPELL_CLASS_COUNT={len(sigs)}")
        print(f"SOMAKE_{label}_ALLOWCRAFTING_OVERRIDE_COUNT={len(allow)}")
        for n,a,e,aval,eval_ in allow:
            print(f"SOMAKE_{label}_ALLOWCRAFTING_OVERRIDE={n}|constant_return={aval}")
        print(f"SOMAKE_{label}_ISENABLED_OVERRIDE_COUNT={len(enabled)}")
        for n,a,e,aval,eval_ in enabled:
            print(f"SOMAKE_{label}_ISENABLED_OVERRIDE={n}|constant_return={eval_}")
        mlhits=modlist_isloaded_hits(zf)
        print(f"SOMAKE_{label}_PROVIDER_MODLIST_ISLOADED_HIT_COUNT={len(mlhits)}")
        for cname,mname,arg in mlhits:
            print(f"SOMAKE_{label}_PROVIDER_MODLIST_ISLOADED_HIT={cname}|{mname}|{arg}")
        lock_hits=string_class_hits(zf,"enableSpellLockSystem")
        common_hits=string_class_hits(zf,"somakespells/general/common.toml")
        print(f"SOMAKE_{label}_SPELL_LOCK_TOKEN_CLASS_COUNT={len(lock_hits)}")
        for n in lock_hits: print(f"SOMAKE_{label}_SPELL_LOCK_TOKEN_CLASS={n}")
        print(f"SOMAKE_{label}_COMMON_TOML_TOKEN_CLASS_COUNT={len(common_hits)}")
        for n in common_hits: print(f"SOMAKE_{label}_COMMON_TOML_TOKEN_CLASS={n}")
        if LANG in zf.namelist():
            lang=json.loads(zf.read(LANG).decode("utf-8"))
            base={m.group(1) for k in lang for m in [re.match(r"^spell\.somakespells\.([^.]+)$",k)] if m}
            guide={m.group(1) for k in lang for m in [re.match(r"^spell\.somakespells\.([^.]+)\.guide$",k)] if m}
            print(f"SOMAKE_{label}_LOCALIZATION_BASE_COUNT={len(base)}")
            print(f"SOMAKE_{label}_LOCALIZATION_GUIDE_COUNT={len(guide)}")
            print(f"SOMAKE_{label}_REGISTRY_NOT_IN_BASE=" + ",".join(sorted(set(ids)-base)))
            print(f"SOMAKE_{label}_BASE_NOT_IN_REGISTRY=" + ",".join(sorted(base-set(ids))))
        return set(ids)

def main():
    cur=download(CURRENT_URL)
    old=download(OLD_URL)
    current_ids=inspect("CURRENT_1_0_9",cur,CURRENT_SHA1)
    old_ids=inspect("OLD_1_0_8_FIX",old,OLD_SHA1)
    added=sorted(current_ids-old_ids)
    removed=sorted(old_ids-current_ids)
    print(f"SOMAKE_REGISTRY_DELTA_ADDED_COUNT={len(added)}")
    print("SOMAKE_REGISTRY_DELTA_ADDED=" + ",".join(added))
    print(f"SOMAKE_REGISTRY_DELTA_REMOVED_COUNT={len(removed)}")
    print("SOMAKE_REGISTRY_DELTA_REMOVED=" + ",".join(removed))
    if len(old_ids)!=67:
        raise RuntimeError(f"historical control drift: expected 67 old IDs got {len(old_ids)}")
    if len(current_ids) < 67:
        raise RuntimeError("current registry unexpectedly smaller than historical control; manual review required")
    print("SOMAKE_1_0_9_REGISTRY_STRUCTURAL_AUDIT=true")

if __name__=="__main__":
    try:
        main()
    except Exception as exc:
        print(f"SOMAKE_AUDIT_ERROR={type(exc).__name__}: {exc}",file=sys.stderr)
        raise
