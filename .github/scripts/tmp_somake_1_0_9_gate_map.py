#!/usr/bin/env python3
import hashlib, io, json, re, struct, sys, urllib.request, zipfile

URL="https://www.cursemaven.com/curse/maven/somake-spells-irons-spells-addon-1461634/8867079/somake-spells-irons-spells-addon-1461634-8867079.jar"
SHA1="171841ac9f802be9309ecc166c1d972ac6d404c0"
MODSPELLS="com/somake/somakespells/registries/ModSpells.class"

SPECIAL={
 "fragmented_requiem":"com/somake/somakespells/spells/blood/FragmentedRequiemSpell.class",
 "rose_secret":"com/somake/somakespells/spells/blood/RoseSecretSpell.class",
 "comforting_lullaby":"com/somake/somakespells/spells/sound/ComfortingLullabySpell.class",
 "funeral_bloom":"com/somake/somakespells/spells/blood/FuneralBloomSpell.class",
 "withered_rose_vortex":"com/somake/somakespells/spells/blood/WitheredRoseVortexSpell.class",
 "custodia_caeli":"com/somake/somakespells/spells/holy/CustodiaCaeliSpell.class",
 "jingle_bell":"com/somake/somakespells/spells/sound/JingleBellSpell.class",
}

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
  elif t==15: cp[i]=("MethodHandle",r.u1(),r.u2())
  elif t==16: cp[i]=("MethodType",r.u2())
  elif t in (17,18): cp[i]=("Dynamic",t,r.u2(),r.u2())
  elif t in (19,20): cp[i]=("ModulePkg",t,r.u2())
  else: raise RuntimeError(f"unknown cp tag {t}")
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
  if not nt or nt[0]!="NameType": return None
  return cls(x[2]),utf(nt[1]),utf(nt[2]),x[1]
 r.u2(); r.u2(); r.u2()
 for _ in range(r.u2()): r.u2()
 fields=[]
 for _ in range(r.u2()):
  acc=r.u2(); name=utf(r.u2()); desc=utf(r.u2())
  for __ in range(r.u2()): r.u2(); r.take(r.u4())
  fields.append((name,desc,acc))
 methods=[]
 for _ in range(r.u2()):
  acc=r.u2(); name=utf(r.u2()); desc=utf(r.u2()); code=None
  for __ in range(r.u2()):
   an=utf(r.u2()); ln=r.u4(); payload=r.take(ln)
   if an=="Code":
    cr=R(payload); cr.u2(); cr.u2(); clen=cr.u4(); code=cr.take(clen)
  methods.append((name,desc,acc,code))
 return cp,utf,cls,string,ref,fields,methods

FIXED=[1]*256
for op,n in {
0x10:2,0x11:3,0x12:2,0x13:3,0x14:3,0x15:2,0x16:2,0x17:2,0x18:2,0x19:2,
0x36:2,0x37:2,0x38:2,0x39:2,0x3a:2,0x84:3,0xa9:2,
0x99:3,0x9a:3,0x9b:3,0x9c:3,0x9d:3,0x9e:3,0x9f:3,0xa0:3,0xa1:3,0xa2:3,0xa3:3,0xa4:3,0xa5:3,0xa6:3,0xa7:3,0xa8:3,
0xb2:3,0xb3:3,0xb4:3,0xb5:3,0xb6:3,0xb7:3,0xb8:3,0xb9:5,0xba:5,0xbb:3,0xbc:2,0xbd:3,0xc0:3,0xc1:3,0xc5:4,0xc6:3,0xc7:3,0xc8:5,0xc9:5
}.items(): FIXED[op]=n
BRANCH=set(range(0x99,0xa9))|{0xc6,0xc7,0xc8,0xc9}

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
  elif op==0xc4:
   p+=6 if code[p+1]==0x84 else 4
  else: p+=FIXED[op]
  out.append((s,op,code[s:p]))
 return out

def branch_target(off,op,raw):
 if op in {0xc8,0xc9}: rel=struct.unpack_from(">i",raw,1)[0]
 else: rel=struct.unpack_from(">h",raw,1)[0]
 return off+rel

def method_code(methods,name):
 for m in methods:
  if m[0]==name: return m[3]
 return None

def analyze_modspells(zf):
 cp,utf,cls,string,ref,fields,methods=parse_class(zf.read(MODSPELLS))
 code=method_code(methods,"<clinit>")
 if code is None: raise RuntimeError("no ModSpells clinit")
 seq=insns(code)

 # Decode only the narrow instruction facts needed for gate->state->branch mapping.
 last_string=None
 decoded=[]
 gate_labels={}
 for off,op,raw in seq:
  info={"off":off,"op":op,"kind":"OTHER","value":None}
  if op==0x12:
   s=string(raw[1])
   if s is not None: last_string=s
   info={"off":off,"op":op,"kind":"LDC","value":s}
  elif op in (0x13,0x14):
   s=string(struct.unpack_from(">H",raw,1)[0])
   if s is not None: last_string=s
   info={"off":off,"op":op,"kind":"LDC","value":s}
  elif op in (0xb2,0xb3,0xb4,0xb5,0xb6,0xb7,0xb8,0xb9):
   rr=ref(struct.unpack_from(">H",raw,1)[0])
   if rr:
    owner,name,desc,tag=rr
    if op==0xb2: info={"off":off,"op":op,"kind":"GETSTATIC","value":(owner,name,desc)}
    elif op==0xb3: info={"off":off,"op":op,"kind":"PUTSTATIC","value":(owner,name,desc)}
    elif op==0xb4: info={"off":off,"op":op,"kind":"GETFIELD","value":(owner,name,desc)}
    elif op==0xb5: info={"off":off,"op":op,"kind":"PUTFIELD","value":(owner,name,desc)}
    else:
     info={"off":off,"op":op,"kind":"INVOKE","value":(owner,name,desc)}
     if name=="isLoaded" and owner:
      label=(f"mod:{last_string}" if owner.endswith("/ModList") else (f"helper:{owner.rsplit('/',1)[-1]}" if "/compat/" in owner else None))
      if label: gate_labels[off]=label
  elif op in BRANCH:
   info={"off":off,"op":op,"kind":"BRANCH","value":branch_target(off,op,raw)}
  elif 0x3b <= op <= 0x4e:
   # fixed astore/istore/lstore/fstore/dstore forms; exact local type is unnecessary here
   info={"off":off,"op":op,"kind":"STORE_LOCAL","value":op}
  elif op in (0x36,0x37,0x38,0x39,0x3a):
   info={"off":off,"op":op,"kind":"STORE_LOCAL","value":raw[1]}
  elif 0x1a <= op <= 0x35:
   info={"off":off,"op":op,"kind":"LOAD_LOCAL","value":op}
  elif op in (0x15,0x16,0x17,0x18,0x19):
   info={"off":off,"op":op,"kind":"LOAD_LOCAL","value":raw[1]}
  decoded.append(info)

 # Registry call list and offsets.
 regs=[]
 last_string=None
 for d in decoded:
  if d["kind"]=="LDC" and d["value"] is not None: last_string=d["value"]
  if d["kind"]=="INVOKE":
   owner,name,desc=d["value"]
   if owner and "DeferredRegister" in owner and name=="register":
    regs.append((d["off"],last_string))

 print(f"SOMAKE_GATE_AUDIT_REGISTER_COUNT={len(regs)}")
 print(f"SOMAKE_GATE_AUDIT_GATE_CALL_COUNT={len(gate_labels)}")

 # Map gate calls to immediate stored state (static field or local) when structurally adjacent.
 gate_state={}
 for idx,d in enumerate(decoded):
  if d["off"] not in gate_labels: continue
  label=gate_labels[d["off"]]
  nxt=decoded[idx+1:idx+4]
  mapped=None
  for x in nxt:
   if x["kind"]=="PUTSTATIC":
    mapped=("STATIC",x["value"][0],x["value"][1])
    break
   if x["kind"]=="STORE_LOCAL":
    mapped=("LOCAL",str(x["value"]),"")
    break
   # stop at unrelated invoke or branch rather than over-associate
   if x["kind"] in ("INVOKE","BRANCH"): break
  gate_state[label]=mapped
  print(f"SOMAKE_GATE_STATE={label}|state={mapped if mapped else 'DIRECT_OR_UNMAPPED'}")

 # Determine branch predicates by a short backwards slice over state reads/direct gate calls.
 branch_rows=[]
 for idx,d in enumerate(decoded):
  if d["kind"]!="BRANCH": continue
  target=d["value"]
  label=None; source=None
  window=decoded[max(0,idx-5):idx]
  for x in reversed(window):
   if x["off"] in gate_labels:
    label=gate_labels[x["off"]]; source=f"direct_gate@{x['off']}"; break
   if x["kind"]=="GETSTATIC":
    owner,name,desc=x["value"]
    for gl,st in gate_state.items():
     if st and st[0]=="STATIC" and st[1]==owner and st[2]==name:
      label=gl; source=f"static:{owner}.{name}"; break
    if label: break
   if x["kind"]=="LOAD_LOCAL":
    for gl,st in gate_state.items():
     if st and st[0]=="LOCAL" and str(st[1])==str(x["value"]):
      label=gl; source=f"local:{x['value']}"; break
    if label: break

  # Count registrations in the forward branch body only; do not infer polarity as enabled/disabled.
  ids=[]
  if target>d["off"]:
   ids=[rid for roff,rid in regs if roff>d["off"] and roff<target and rid]
  if label or ids:
   branch_rows.append((d["off"],d["op"],target,label,source,ids))

 print(f"SOMAKE_GATE_BRANCH_ROW_COUNT={len(branch_rows)}")
 for off,op,target,label,source,ids in branch_rows:
  print(f"SOMAKE_GATE_BRANCH=off={off}|opcode=0x{op:02x}|target={target}|gate={label or 'UNRESOLVED'}|source={source or 'UNRESOLVED'}|register_ids={','.join(ids)}")

 # Provider compat-helper references present in ModSpells, independent of branch mapping.
 helper_refs=set()
 for d in decoded:
  if d["kind"]=="INVOKE":
   owner,name,desc=d["value"]
   if owner and "/compat/" in owner:
    helper_refs.add((owner,name))
 print(f"SOMAKE_MODSPELLS_COMPAT_HELPER_REF_COUNT={len(helper_refs)}")
 for owner,name in sorted(helper_refs):
  print(f"SOMAKE_MODSPELLS_COMPAT_HELPER_REF={owner}.{name}")

 # Narrow diagnostic for any branch that guards registrations but whose predicate source
 # was not resolved above. Emit only symbolic field/method references, not bytecode.
 for off,op,target,label,source,ids in branch_rows:
  if label or not ids:
   continue
  idx=next(i for i,d in enumerate(decoded) if d["off"]==off)
  facts=[]
  for x in decoded[max(0,idx-12):idx]:
   if x["kind"] in ("GETSTATIC","GETFIELD","INVOKE","LOAD_LOCAL","LDC"):
    facts.append(f"{x['kind']}@{x['off']}:{x['value']}")
  print(f"SOMAKE_UNRESOLVED_BRANCH_CONTEXT=off={off}|register_ids={','.join(ids)}|facts={'||'.join(facts)}")

def analyze_allow(zf,spell_id,path):
 cp,utf,cls,string,ref,fields,methods=parse_class(zf.read(path))
 code=method_code(methods,"allowCrafting")
 if code is None:
  print(f"SOMAKE_ALLOW_DETAIL={spell_id}|no_override"); return
 refs=set(); fields_seen=set(); strings=set(); branches=0
 for off,op,raw in insns(code):
  if op in BRANCH: branches+=1
  if op==0x12:
   s=string(raw[1])
   if s: strings.add(s)
  elif op in (0x13,0x14):
   s=string(struct.unpack_from(">H",raw,1)[0])
   if s: strings.add(s)
  elif op in (0xb2,0xb3,0xb4,0xb5,0xb6,0xb7,0xb8,0xb9):
   rr=ref(struct.unpack_from(">H",raw,1)[0])
   if rr:
    owner,name,desc,tag=rr
    if op in (0xb2,0xb3,0xb4,0xb5): fields_seen.add((owner,name))
    else: refs.add((owner,name))
 print(f"SOMAKE_ALLOW_DETAIL={spell_id}|branches={branches}|method_refs={';'.join(f'{o}.{n}' for o,n in sorted(refs))}|field_refs={';'.join(f'{o}.{n}' for o,n in sorted(fields_seen))}|strings={';'.join(sorted(strings))}")

def resource_refs(zf,ids):
 jsons=[n for n in zf.namelist() if n.startswith("data/") and n.endswith(".json")]
 for sid in ids:
  needles=[f"somakespells:{sid}".encode(), sid.encode()]
  paths=[]
  for n in jsons:
   b=zf.read(n)
   if any(x in b for x in needles): paths.append(n)
  print(f"SOMAKE_RESOURCE_REF={sid}|count={len(paths)}|paths={','.join(sorted(paths))}")
 focus="data/somakespells/tags/item/school_focus/aqua.json"
 if focus in zf.namelist():
  try:
   obj=json.loads(zf.read(focus).decode("utf-8"))
   vals=obj.get("values",[])
   print("SOMAKE_AQUA_FOCUS_VALUES="+",".join(str(x) for x in vals))
  except Exception as e:
   print("SOMAKE_AQUA_FOCUS_PARSE_ERROR="+type(e).__name__)

def main():
 req=urllib.request.Request(URL,headers={"User-Agent":"Black-Arcana-clean-room-audit/1"})
 with urllib.request.urlopen(req,timeout=120) as resp: blob=resp.read()
 got=hashlib.sha1(blob).hexdigest()
 print(f"SOMAKE_GATE_AUDIT_SIZE={len(blob)}")
 print(f"SOMAKE_GATE_AUDIT_SHA1={got}")
 print(f"SOMAKE_GATE_AUDIT_SHA256={hashlib.sha256(blob).hexdigest()}")
 if got!=SHA1: raise RuntimeError(f"sha mismatch {got}")
 with zipfile.ZipFile(io.BytesIO(blob)) as zf:
  analyze_modspells(zf)
  for sid,path in SPECIAL.items(): analyze_allow(zf,sid,path)
  resource_refs(zf,SPECIAL.keys())
 print("SOMAKE_GATE_REACHABILITY_AUDIT=true")

if __name__=="__main__":
 try: main()
 except Exception as exc:
  print(f"SOMAKE_GATE_AUDIT_ERROR={type(exc).__name__}: {exc}",file=sys.stderr); raise
