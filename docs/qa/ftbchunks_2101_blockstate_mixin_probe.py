#!/usr/bin/env python3
"""Read-only classfile annotations / method census for pinned FTB 2101.1.22.

Parses metadata only, not proprietary implementation. Neither mixin metadata nor
constant-pool references prove effective runtime application or claim safety.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import struct
import zipfile
from pathlib import Path

JAR_NAME="ftb-chunks-neoforge-2101.1.22.jar"
JAR_SHA256="4ba1b3352184fa7f6e2aa4bca76edd074867697d62344dfa50dcccdb4dab5217"
CLASS_PATH="dev/ftb/mods/ftbchunks/core/mixin/BlockStateMixin.class"
CLASS_SHA256="2920670a37b9ebf4d7768ddf37f488fd685f2e88d4630a82310b75393039d5ce"
CONFIG="ftbchunks-common.mixins.json"
CONFIG_SHA256="bd5f99632e804411285c53d1d5fc3cf90f938f265c62e2862b0fc790c00d5ad8"
SCOPE="EXACT_FTBCHUNKS_2101_1_22_BLOCKSTATE_MIXIN_CLASSFILE_METADATA"
MAX_LEN=13000

class AuditError(Exception): pass
def require(flag,msg):
    if not flag: raise AuditError(msg)
def digest(data): return hashlib.sha256(data).hexdigest()

class Buffer:
    def __init__(self,data): self.b=memoryview(data);self.i=0
    def take(self,n):
        require(0<=n<=len(self.b)-self.i,"truncated or overrun classfile")
        v=self.b[self.i:self.i+n].tobytes();self.i+=n;return v
    def u1(self):return self.take(1)[0]
    def u2(self):return struct.unpack(">H",self.take(2))[0]
    def u4(self):return struct.unpack(">I",self.take(4))[0]
    def done(self):return self.i==len(self.b)

class Classfile:
    def __init__(self,data):
        require(len(data)<300000,"classfile size budget exceeded")
        self.b=Buffer(data)
        require(self.b.u4()==0xCAFEBABE,"invalid JVM magic")
        self.minor=self.b.u2();self.major=self.b.u2()
        num=self.b.u2();require(1<num<=5000,"unexpected JVM constant pool size")
        self.cp=[None]*num
        i=1
        while i<num:
            tag=self.b.u1()
            if tag==1:
                n=self.b.u2();require(n<16000,"oversized CP utf8")
                val=self.b.take(n).decode("utf-8","replace")
            elif tag in (3,4): val=self.b.take(4).hex()
            elif tag in (5,6):
                val=self.b.take(8).hex()
                self.cp[i]=(tag,val);i+=1
                require(i<num,"invalid two-slot constant")
                self.cp[i]=None;i+=1;continue
            elif tag in (7,8,16,19,20): val=self.b.u2()
            elif tag in (9,10,11,12,17,18): val=(self.b.u2(),self.b.u2())
            elif tag==15:val=(self.b.u1(),self.b.u2())
            else:raise AuditError("unrecognized constant pool tag "+str(tag))
            self.cp[i]=(tag,val);i+=1
        self.access=self.b.u2()
        self.this_class=self.b.u2();self.super_class=self.b.u2()
        self.interfaces=[self.b.u2() for _ in range(self.b.u2())]
        self.fields=[self.member() for _ in range(self.b.u2())]
        self.methods=[self.member() for _ in range(self.b.u2())]
        self.attrs=self.attributes()
        require(self.b.done(),"unexpected classfile trailing bytes")
    def utf(self,i):
        require(0<i<len(self.cp) and self.cp[i] is not None and self.cp[i][0]==1,
                "not a JVM utf8 entry")
        return self.cp[i][1]
    def const(self,i):
        require(0<i<len(self.cp) and self.cp[i] is not None,"invalid JVM constant index")
        tag,value=self.cp[i]
        if tag==1:return value
        if tag in (7,8,16,19,20):return self.utf(value)
        if tag in (3,4,5,6):return value
        return "CP_REFERENCE"
    def annotation(self,b,depth=0):
        require(depth<=5,"annotation nesting too deep")
        kind=self.utf(b.u2())
        pairs={}
        n=b.u2();require(n<=35,"annotation pair budget exceeded")
        for _ in range(n):
            k=self.utf(b.u2())
            require(k not in pairs,"duplicate JVM annotation name")
            pairs[k]=self.element(b,depth+1)
        return {"type":kind,"elements":pairs}
    def element(self,b,depth):
        require(depth<=6,"annotation nesting too deep")
        tag=chr(b.u1())
        if tag in "BCDFIJSZs":return self.const(b.u2())
        if tag=="e":return {"enum_type":self.utf(b.u2()),"enum_name":self.utf(b.u2())}
        if tag=="c":return {"class_descriptor":self.utf(b.u2())}
        if tag=="@":return self.annotation(b,depth+1)
        if tag=="[":
            n=b.u2();require(n<=60,"annotation array budget exceeded")
            return [self.element(b,depth+1) for _ in range(n)]
        raise AuditError("unknown annotation element kind")
    def attributes(self):
        attrs=[]
        count=self.b.u2();require(count<=100,"attribute population exceeded")
        for _ in range(count):
            name=self.utf(self.b.u2());n=self.b.u4()
            require(n<350000,"attribute size budget exceeded")
            data=self.b.take(n)
            attrs.append((name,data))
        return attrs
    def member(self):
        flags=self.b.u2();name=self.utf(self.b.u2());descriptor=self.utf(self.b.u2())
        attrs=self.attributes()
        return {"access_flags":flags,"name":name,"descriptor":descriptor,"attributes":attrs}
    def annotation_records(self,attrs):
        out=[]
        for name,data in attrs:
            if name not in ("RuntimeVisibleAnnotations","RuntimeInvisibleAnnotations"):
                continue
            b=Buffer(data);count=b.u2();require(count<=40,"too many JVM annotations")
            for _ in range(count):
                out.append({"visibility":name,"annotation":self.annotation(b)})
            require(b.done(),"annotation attribute data leftover")
        return out
    def code_summary(self,attrs):
        values=[data for name,data in attrs if name=="Code"]
        require(len(values)<=1,"multiple code attributes")
        if not values:return None
        b=Buffer(values[0]);b.u2();b.u2()
        n=b.u4();require(n<=200000,"method bytecode too large")
        code=b.take(n)
        return {"bytecode_size":len(code),"bytecode_sha256":digest(code)}
    def summary(self):
        require(45<=self.major<=70,"unexpected JVM major version")
        require(len(self.methods)<=180 and len(self.fields)<=120,"class member budget exceeded")
        methods=[]
        for m in self.methods:
            methods.append({"name":m["name"],"descriptor":m["descriptor"],
                            "access_flags":m["access_flags"],
                            "annotations":self.annotation_records(m["attributes"]),
                            "code":self.code_summary(m["attributes"])})
        class_annotations=self.annotation_records(self.attrs)
        return {"jvm_class_major_version":self.major,
                "class_annotations":class_annotations,
                "methods":methods,
                "method_count":len(methods),
                "field_count":len(self.fields),
                "annotation_types":sorted(set(
                    a["annotation"]["type"] for a in class_annotations+
                    [item for m in methods for item in m["annotations"]]))}

def analyze_archive(jar):
    p=Path(jar)
    require(p.name==JAR_NAME,"wrong exact FTB artifact filename")
    require(p.is_file() and 10000<p.stat().st_size<5_000_000,
            "publisher artifact missing or size unexpected")
    raw=p.read_bytes()
    require(digest(raw)==JAR_SHA256,"exact publisher jar hash drift")
    require(zipfile.is_zipfile(p),"invalid JVM jar archive")
    with zipfile.ZipFile(p) as z:
        names=z.namelist()
        require(len(names)==len(set(names)),"duplicate ZIP entries")
        require(CLASS_PATH in names and CONFIG in names,"missing exact mixin")
        clazz=z.read(CLASS_PATH);conf=z.read(CONFIG)
        require(digest(clazz)==CLASS_SHA256,"pinned BlockStateMixin hash drift")
        require(digest(conf)==CONFIG_SHA256,"pinned mixin configuration hash drift")
        config=json.loads(conf)
        require("BlockStateMixin" in config.get("mixins",[]),
                "BlockStateMixin not declared in exact configuration")
    summary=Classfile(clazz).summary()
    report={
        "schema_version":1,"scope":SCOPE,
        "artifact":{"coordinates":"dev.ftb.mods:ftb-chunks-neoforge:2101.1.22",
                    "sha256":JAR_SHA256,"size_bytes":len(raw)},
        "class":{"path":CLASS_PATH,"sha256":CLASS_SHA256,**summary},
        "configuration":{"name":CONFIG,"sha256":CONFIG_SHA256,
                         "blockstate_mixin_declared":True},
        "limits":{
            "runtime_mixin_application":"NOT_OBSERVED",
            "injection_target_behavior":"STATIC_DECLARATION_ONLY",
            "other_mod_listeners":"NOT_VERIFIED",
            "claim_per_affected_block":"NOT_CERTIFIED",
            "native_explosion_dispatch":"NOT_VERIFIED",
            "black_arcana_world_effect_policy":"NOT_VERIFIED",
            "physical_qa":"NOT_TESTED",
            "mutating_hook":"NOT_VERIFIED",
            "mutation":"NO_MUTATION",
            "perk_certification":"NOT_CERTIFIED"
        },
        "interpretation":"ANALYZED_CLASSFILE_METADATA_ONLY_NOT_RUNTIME_PROTECTION"
    }
    require(len(json.dumps(report).encode("utf-8"))<MAX_LEN,"bounded report output exceeded")
    return report

def verify_seal(observed,seal):
    require(seal.get("scope")==SCOPE,"unrecognized manifest scope")
    require(observed==seal,"SHA-exact BlockStateMixin metadata seal drift")
    return True

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--jar",required=True)
    ap.add_argument("--output",required=True)
    ap.add_argument("--seal")
    args=ap.parse_args()
    try:
        report=analyze_archive(args.jar)
        if args.seal:
            verify_seal(report,json.loads(Path(args.seal).read_text(encoding="utf-8")))
        path=Path(args.output);path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        print("PASS: exact FTB BlockStateMixin classfile metadata sha256="+CLASS_SHA256)
        print("methods="+str(report["class"]["method_count"])+
              ", annotations="+json.dumps(report["class"]["annotation_types"]))
        print("NO_MUTATION / NOT_CERTIFIED / runtime injection not observed")
    except (AuditError,ValueError,OSError,KeyError,TypeError,UnicodeDecodeError) as exc:
        ap.exit(1,"FAIL-CLOSED: "+str(exc)+"\n")

if __name__=="__main__":
    main()
