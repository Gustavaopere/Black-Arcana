#!/usr/bin/env python3
import hashlib, io, json, struct, sys, urllib.request, zipfile
from collections import deque

URL="https://www.cursemaven.com/curse/maven/somake-spells-irons-spells-addon-1461634/8867079/somake-spells-irons-spells-addon-1461634-8867079.jar"
EXPECTED_SHA1="171841ac9f802be9309ecc166c1d972ac6d404c0"
MODSPELLS="com/somake/somakespells/registries/ModSpells.class"

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
    r.u2(); r.u2(); r.u2()
    for _ in range(r.u2()): r.u2()
    for _ in range(r.u2()):
        r.u2(); r.u2(); r.u2()
        for __ in range(r.u2()): r.u2(); r.take(r.u4())
    methods=[]
    for _ in range(r.u2()):
        acc=r.u2(); name=utf(r.u2()); desc=utf(r.u2()); ac=r.u2(); code=None; ex=[]
        for __ in range(ac):
            an=utf(r.u2()); ln=r.u4(); payload=r.take(ln)
            if an=="Code":
                cr=R(payload); cr.u2(); cr.u2(); clen=cr.u4(); code=cr.take(clen)
                for ___ in range(cr.u2()):
                    ex.append((cr.u2(),cr.u2(),cr.u2(),cr.u2()))
        methods.append((name,desc,acc,code,ex))
    return string,ref,methods

FIX=[1]*256
for op,n in {
0x10:2,0x11:3,0x12:2,0x13:3,0x14:3,0x15:2,0x16:2,0x17:2,0x18:2,0x19:2,
0x36:2,0x37:2,0x38:2,0x39:2,0x3a:2,0x84:3,0xa9:2,
0x99:3,0x9a:3,0x9b:3,0x9c:3,0x9d:3,0x9e:3,0x9f:3,0xa0:3,0xa1:3,0xa2:3,0xa3:3,0xa4:3,0xa5:3,0xa6:3,
0xa7:3,0xa8:3,0xb2:3,0xb3:3,0xb4:3,0xb5:3,0xb6:3,0xb7:3,0xb8:3,0xb9:5,0xba:5,
0xbb:3,0xbc:2,0xbd:3,0xc0:3,0xc1:3,0xc5:4,0xc6:3,0xc7:3,0xc8:5,0xc9:5
}.items(): FIX[op]=n

COND=set(range(0x99,0xa7))|{0xc6,0xc7}
RET={0xac,0xad,0xae,0xaf,0xb0,0xb1}
GOTO={0xa7,0xc8}

def insns(code):
    out=[]; p=0
    while p<len(code):
        s=p; op=code[p]; targets=[]
        if op==0xaa:
            p+=1
            while p%4: p+=1
            default=struct.unpack_from(">i",code,p)[0]; p+=4
            lo=struct.unpack_from(">i",code,p)[0]; p+=4
            hi=struct.unpack_from(">i",code,p)[0]; p+=4
            targets=[s+default]
            for _ in range(hi-lo+1): targets.append(s+struct.unpack_from(">i",code,p)[0]); p+=4
        elif op==0xab:
            p+=1
            while p%4: p+=1
            default=struct.unpack_from(">i",code,p)[0]; p+=4
            npairs=struct.unpack_from(">i",code,p)[0]; p+=4
            targets=[s+default]
            for _ in range(npairs):
                p+=4; targets.append(s+struct.unpack_from(">i",code,p)[0]); p+=4
        elif op==0xc4:
            nxt=code[p+1]; p+=6 if nxt==0x84 else 4
        else:
            p+=FIX[op]
            if op in COND or op in (0xa7,0xa8):
                targets=[s+struct.unpack_from(">h",code,s+1)[0]]
            elif op in (0xc8,0xc9):
                targets=[s+struct.unpack_from(">i",code,s+1)[0]]
        out.append({"off":s,"op":op,"raw":code[s:p],"targets":targets})
    return out

def cp_index(raw): return struct.unpack_from(">H",raw,1)[0]

def build_cfg(ins):
    by={x["off"]:x for x in ins}; offs=[x["off"] for x in ins]; nxt={offs[i]:offs[i+1] for i in range(len(offs)-1)}
    succ={}
    for x in ins:
        op=x["op"]; s=[]
        if op in RET or op==0xbf: s=[]
        elif op in GOTO: s=list(x["targets"])
        elif op in COND: s=list(x["targets"])+([nxt[x["off"]]] if x["off"] in nxt else [])
        elif op in (0xaa,0xab): s=list(x["targets"])
        else: s=[nxt[x["off"]]] if x["off"] in nxt else []
        succ[x["off"]]=[t for t in s if t in by]
    return succ

def exit_reachable(succ, start, returns, removed=None):
    q=deque([start]); seen=set()
    while q:
        x=q.popleft()
        if x==removed or x in seen: continue
        seen.add(x)
        if x in returns: return True
        for y in succ.get(x,[]): q.append(y)
    return False

def download():
    req=urllib.request.Request(URL,headers={"User-Agent":"Black-Arcana-clean-room-audit/1"})
    with urllib.request.urlopen(req,timeout=120) as r: return r.read()

def h(data,name):
    x=hashlib.new(name); x.update(data); return x.hexdigest()

def main():
    blob=download()
    sha1=h(blob,"sha1")
    print(f"SOMAKE_CFG_SIZE={len(blob)}")
    print(f"SOMAKE_CFG_SHA1={sha1}")
    print(f"SOMAKE_CFG_SHA256={h(blob,'sha256')}")
    if sha1!=EXPECTED_SHA1: raise RuntimeError("physical/publisher SHA1 mismatch")
    print("SOMAKE_CFG_PHYSICAL_HASH_MATCH=true")

    with zipfile.ZipFile(io.BytesIO(blob)) as zf:
        string,ref,methods=parse_class(zf.read(MODSPELLS))
        m=next(x for x in methods if x[0]=="<clinit>")
        code=m[3]
        ins=insns(code); by={x["off"]:x for x in ins}
        succ=build_cfg(ins)
        start=ins[0]["off"]
        returns={x["off"] for x in ins if x["op"] in RET}
        if not returns: raise RuntimeError("no normal return in clinit")
        if not exit_reachable(succ,start,returns): raise RuntimeError("normal return unreachable before removals")

        last_string=None; regs=[]; isloads=[]; field_events=[]; branch_events=[]
        for x in ins:
            op=x["op"]; raw=x["raw"]
            if op==0x12:
                s=string(raw[1])
                if s is not None: last_string=s
            elif op in (0x13,0x14):
                s=string(cp_index(raw))
                if s is not None: last_string=s
            elif op in (0xb2,0xb3,0xb4,0xb5):
                rr=ref(cp_index(raw))
                if rr: field_events.append({"off":x["off"],"op":op,"owner":rr[0],"name":rr[1],"desc":rr[2]})
            elif op in (0xb6,0xb7,0xb8,0xb9):
                rr=ref(cp_index(raw))
                if rr:
                    owner,name,desc,_=rr
                    if owner and "DeferredRegister" in owner and name=="register":
                        regs.append({"off":x["off"],"id":last_string})
                    if owner and owner.endswith("/ModList") and name=="isLoaded":
                        isloads.append({"off":x["off"],"modid":last_string})
            if op in COND:
                branch_events.append({"off":x["off"],"target":x["targets"][0],"op":op})

        if len(regs)!=83: raise RuntimeError(f"expected 83 register calls, got {len(regs)}")
        skipped=[]
        for r in regs:
            if exit_reachable(succ,start,returns,removed=r["off"]):
                skipped.append(r)
        print(f"SOMAKE_CFG_REGISTER_COUNT={len(regs)}")
        print(f"SOMAKE_CFG_BRANCH_COUNT={len(branch_events)}")
        print(f"SOMAKE_CFG_REGISTER_CALLS_SKIPPABLE_BY_NORMAL_CFG={len(skipped)}")
        for r in skipped: print(f"SOMAKE_CFG_SKIPPABLE_REGISTER={r['off']}|{r['id']}")

        print(f"SOMAKE_CFG_ISLOADED_COUNT={len(isloads)}")
        for ev in isloads:
            after=[f for f in field_events if ev["off"]<f["off"]<=ev["off"]+24]
            before_br=[b for b in branch_events if ev["off"]<b["off"]<=ev["off"]+40]
            print("SOMAKE_CFG_ISLOADED="+json.dumps({"off":ev["off"],"modid":ev["modid"],"near_fields":after,"near_branches":before_br},separators=(",",":"),sort_keys=True))

        # If isLoaded writes a static boolean field, find every use in this class.
        tracked=set()
        for ev in isloads:
            for f in field_events:
                if ev["off"]<f["off"]<=ev["off"]+24 and f["op"]==0xb3:
                    tracked.add((f["owner"],f["name"],f["desc"]))
        print(f"SOMAKE_CFG_TRACKED_ISLOADED_FIELD_COUNT={len(tracked)}")
        for owner,name,desc in sorted(tracked):
            print(f"SOMAKE_CFG_TRACKED_FIELD={owner}|{name}|{desc}")
            uses=[]
            for mn,md,ma,mc,mex in methods:
                if mc is None: continue
                for ii in insns(mc):
                    if ii["op"] in (0xb2,0xb3,0xb4,0xb5):
                        rr=ref(cp_index(ii["raw"]))
                        if rr and (rr[0],rr[1],rr[2])==(owner,name,desc):
                            uses.append({"method":mn,"desc":md,"off":ii["off"],"op":ii["op"]})
            print("SOMAKE_CFG_TRACKED_FIELD_USES="+json.dumps(uses,separators=(",",":"),sort_keys=True))

        # Bounded branch summary: only branch offsets/targets and how many register calls lie in the linear interval.
        for b in branch_events:
            lo=min(b["off"],b["target"]); hi=max(b["off"],b["target"])
            ids=[r["id"] for r in regs if lo<r["off"]<hi]
            if ids:
                print("SOMAKE_CFG_BRANCH_REGISTER_INTERVAL="+json.dumps({"branch_off":b["off"],"target":b["target"],"ids":ids},separators=(",",":"),sort_keys=True))

        if skipped:
            raise RuntimeError("one or more DeferredRegister.register calls can be skipped by normal clinit control-flow")
        print("SOMAKE_1_0_9_ALL_83_REGISTER_CALLS_UNCONDITIONAL_CFG=true")

if __name__=="__main__":
    try: main()
    except Exception as e:
        print(f"SOMAKE_CFG_AUDIT_ERROR={type(e).__name__}: {e}",file=sys.stderr)
        raise
