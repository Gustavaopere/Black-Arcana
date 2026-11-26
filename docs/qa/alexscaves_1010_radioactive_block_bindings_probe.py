#!/usr/bin/env python3
"""Read-only follow-up: ACBlockRegistry item type selector and registration windows."""
import argparse, json, re, subprocess
from pathlib import Path
from zipfile import ZipFile
from alexscaves_1010_armor_material_audit import ClassReader, canonical, digest, require, verify_artifact
from alexscaves_1010_enchantable_item_probe import disassemble
from alexscaves_1010_four_items_downstream_250_probe import projection
P="com/github/alexmodguy/alexscaves/server/block/ACBlockRegistry"
FACTORIES={"lambda$getBlockSupplier$440":"97cdb48022a1d0e97196956a30d852cc346aad92de1c88cc8f6590109bfd71f3","lambda$getBlockSupplier$441":"6659fa766f94d238df90308e900913b9bb93b1edc19ea32f34b4f3a90b6e425f"}
def inspect(jar,javap):
    verify_artifact(jar)
    with ZipFile(jar) as z:
        raw=z.read(P+".class");rd=ClassReader(raw)
        require(rd.name==P and rd.major==65,"block registry identity")
        body=disassemble(jar,javap,P)
        declarations={(v["name"],v["descriptor"]):v for v in rd.methods}
        for n,pin in FACTORIES.items():
            require([v["code_sha256"] for k,v in declarations.items() if k[0]==n]==[pin],"factory pin")
        selectors=[k for k in body if k[0]=="getBlockSupplier"]
        require(len(selectors)==1,"selector identity")
        selected=selectors[0]
        selector=projection(rd,selected,body[selected],declarations[selected])
        # Preserve switch arms omitted by the generic javap instruction parser.
        proc=subprocess.run([javap,"-classpath",str(jar),"-p","-c","-s",P.replace("/","." )],capture_output=True,text=True,timeout=90)
        require(proc.returncode==0,"javap selector")
        lines=proc.stdout.splitlines()
        heads=[i for i,l in enumerate(lines) if re.match(r"^  \\S",l) and " getBlockSupplier(" in l]
        require(len(heads)==1,"selector heading")
        start=heads[0]
        end=next((i for i in range(start+1,len(lines)) if re.match(r"^  \\S",lines[i])),len(lines))
        arms=[l.strip() for l in lines[start:end] if re.fullmatch(r"\\s*(?:-?\\d+|default):\\s+\\d+\\s*",l)]
        helpers=[]
        for k,b in sorted(body.items()):
            if k==selected:continue
            if any(op.startswith("invoke") and re.search(r"(?:\\.| )getBlockSupplier:",sym) for op,_,sym in b.values()):
                require(len(b)<=1200,"selector caller scope")
                helpers.append(projection(rd,k,b,declarations[k]))
        require(len(helpers)<=40,"selector callers budget")
        helper_names={x["name"] for x in helpers}
        windows=[]
        for k,b in sorted(body.items()):
            offsets=sorted(b)
            for i,at in enumerate(offsets):
                op,arg,sym=b[at]
                if not op.startswith("invoke") or not any(re.search(r"(?:\\.| )"+re.escape(n)+":",sym) for n in helper_names):continue
                window=[{"offset":q,"opcode":b[q][0],"operand":b[q][1],"symbol":b[q][2]} for q in offsets[max(0,i-15):i+7]]
                if any(any(token in v["symbol"].lower() for token in ("uranium","radioactive","nuclear","waste","radrock")) for v in window):
                    windows.append({"method":k[0],"descriptor":k[1],"code_sha256":declarations[k]["code_sha256"],"offset":at,"window":window})
        require(len(windows)<=120,"binding candidate budget")
        # Class-specific switch table helpers, if present.
        related={}
        for ref in selector["typed_members"]:
            owner=ref["owner"]
            if not owner.startswith(P+"$") or owner in related or owner+".class" not in z.namelist():continue
            data=z.read(owner+".class");reader=ClassReader(data);parsed=disassemble(jar,javap,owner)
            rows=[]
            for v in reader.methods:
                k=(v["name"],v["descriptor"])
                if k[0]=="<clinit>" and k in parsed:
                    require(len(parsed[k])<=1200,"switch mapping scope")
                    rows.append(projection(reader,k,parsed[k],v))
            related[owner]={"sha256":digest(data),"methods":rows}
        return {"scope":"BINDING_CANDIDATES_NOT_CERTIFIED","class_sha256":digest(raw),"selector":selector,"switch_arms":arms,"helper_methods":helpers,"candidate_windows":windows,"switch_helpers":related,"mutation":"NO_MUTATION"}
if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--jar",type=Path,required=True);ap.add_argument("--javap",default="javap");ap.add_argument("--output",type=Path,required=True)
    a=ap.parse_args();require(not a.output.exists(),"write once")
    report=inspect(a.jar,a.javap);data=canonical(report).encode();require(len(data)<=2000000,"report budget")
    with a.output.open("xb") as f:f.write(data)
    print("BINDING_REPORT_SHA256",digest(data),"BYTES",len(data))
    for k,v in report.items():print("BLOCK_BINDING",json.dumps({"key":k,"value":v},sort_keys=True))
